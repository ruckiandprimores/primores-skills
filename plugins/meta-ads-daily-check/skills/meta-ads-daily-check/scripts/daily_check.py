"""Meta ads daily check: turn per-ad numbers into flags, the same way every morning.

Two inputs, either or both:

1. A summary CSV, one row per ad (names case-insensitive, extra columns ignored):
     ad, ad_set, campaign, status,
     spend_yday, results_yday, spend_7d, results_7d, impressions_7d, frequency_7d,
     daily_budget   (optional: the ad set's daily budget, repeated on each of its ads)
     learning       (optional: e.g. LEARNING, LEARNING_LIMITED, SUCCESS)

2. --daily: a CSV with one row per ad per day for the last 7 days:
     ad, ad_set, campaign, date (YYYY-MM-DD), spend, results, impressions, link_clicks
   With only this file, the summary is built from it (the last date is "yesterday").
   With it, the script also reads trends inside the week.

Usage:
  python daily_check.py ads.csv --target-cpr 25 --currency EUR
  python daily_check.py --daily daily.csv --target-cpr 25
  python daily_check.py ads.csv --daily daily.csv

Prints JSON with totals and flags; the skill writes the summary from it.

How the flags are decided: results are rare events, so a fixed rule like "pause after
spending 2x target" treats a small account and a big one the same. Instead the script asks
"if this ad were really working at the target cost, how likely is a result this bad by
chance?" (a Poisson probability). Under 10%: unlikely to be bad luck, act. Over that: noise,
wait, and the script works out when there will be enough spend to tell.
"""
import argparse, csv, json, math, sys
from collections import defaultdict

ACT = 0.10      # chance of bad luck at or below which we call it real
YDAY = 0.15     # same for a single day, a bit looser because it's a "watch", not a "pause"


def num(v):
    try:
        return float(str(v).replace(",", "").strip() or 0)
    except ValueError:
        return 0.0


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [{k.strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in rows]


def p_at_most(k, lam):
    """Chance of k or fewer results when lam are expected (Poisson)."""
    if lam <= 0:
        return 1.0
    k = int(k)
    term = total = math.exp(-lam)
    for i in range(1, k + 1):
        term *= lam / i
        total += term
    return min(total, 1.0)


def chance_words(p):
    pct = round(100 * p)
    if pct < 1:
        return "under 1 in 100"
    return f"about {pct} in 100"


def build_from_daily(daily):
    """Summary rows (one per ad) from daily rows; the latest date counts as yesterday."""
    last = max(r.get("date", "") for r in daily)
    by_ad = {}
    for r in daily:
        name = r.get("ad") or "?"
        a = by_ad.setdefault(name, {"ad": name, "ad_set": r.get("ad_set", ""), "campaign": r.get("campaign", ""),
                                    "spend_yday": 0.0, "results_yday": 0.0, "spend_7d": 0.0, "results_7d": 0.0,
                                    "impressions_7d": 0.0})
        s, res = num(r.get("spend")), num(r.get("results"))
        a["spend_7d"] += s
        a["results_7d"] += res
        a["impressions_7d"] += num(r.get("impressions"))
        if r.get("date") == last:
            a["spend_yday"] += s
            a["results_yday"] += res
    return [{k: str(v) for k, v in a.items()} for a in by_ad.values()], last


def trends(days, target):
    """Read one ad's 7 daily rows (sorted by date) for movement the weekly totals hide."""
    out = {}
    if len(days) < 6:
        return out
    early, late = days[:-3], days[-3:]
    se, re_ = sum(d["spend"] for d in early), sum(d["results"] for d in early)
    sl, rl = sum(d["spend"] for d in late), sum(d["results"] for d in late)
    # Results slowing: compare the last 3 days with the ad's own earlier rate.
    if re_ >= 3 and sl > 0:
        lam = sl / (se / re_)
        p = p_at_most(rl, lam)
        if rl < lam and p <= ACT:
            out["results_slowing"] = {
                "early": f"{re_:g} results for {se:.2f} ({se/re_:.2f} each) in the first {len(early)} days",
                "late": f"{rl:g} results for {sl:.2f} in the last 3 days, where about {lam:.1f} were expected",
                "chance": chance_words(p)}
            # Were people still clicking? If clicks kept coming but results didn't, the leak is after
            # the click (form, landing page, tracking), not only a tired creative.
            ce_all = sum(d["clicks"] for d in early)
            cl_late = sum(d["clicks"] for d in late)
            if ce_all and cl_late:
                lam_c = cl_late * re_ / ce_all
                pc = p_at_most(rl, lam_c)
                if rl < lam_c and pc <= ACT:
                    out["results_slowing"]["after_click"] = (
                        f"{cl_late:g} people still clicked in the last 3 days; at the earlier rate of results per click "
                        f"about {lam_c:.1f} results were expected (chance of this by bad luck: {chance_words(pc)}). "
                        "Check the form or landing page and the tracking before blaming the ad")
    # Fewer people clicking: link click rate, first 3 days vs last 3 days.
    first = days[:3]
    ie, ce = sum(d["impressions"] for d in first), sum(d["clicks"] for d in first)
    il, cl = sum(d["impressions"] for d in late), sum(d["clicks"] for d in late)
    if ie >= 500 and il >= 500 and ce >= 10:
        ctr_e, ctr_l = ce / ie, cl / il
        if ctr_l <= 0.7 * ctr_e:
            out["clicks_falling"] = {"early_ctr_pct": round(100 * ctr_e, 2), "late_ctr_pct": round(100 * ctr_l, 2),
                                     "why": f"{100*ctr_e:.2f}% of people clicked in the first 3 days, {100*ctr_l:.2f}% in the last 3"}
    # Days in a row, up to yesterday, spending with no result.
    streak = 0
    for d in reversed(days):
        if d["spend"] > 0 and d["results"] == 0:
            streak += 1
        else:
            break
    if streak >= 2:
        out["days_without_result"] = streak
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="?")
    ap.add_argument("--daily", help="one row per ad per day, last 7 days")
    ap.add_argument("--target-cpr", type=float, default=None, help="target cost per result")
    ap.add_argument("--currency", default="")
    a = ap.parse_args()
    if not a.csv and not a.daily:
        ap.error("give a summary CSV, --daily, or both")

    daily = load(a.daily) if a.daily else []
    yesterday = None
    if a.csv:
        rows = load(a.csv)
    else:
        rows, yesterday = build_from_daily(daily)
    if daily and not yesterday:
        yesterday = max(r.get("date", "") for r in daily)
    if not rows:
        print(json.dumps({"error": "no rows"}))
        return 1

    per_ad_days = defaultdict(list)
    for r in sorted(daily, key=lambda r: r.get("date", "")):
        per_ad_days[r.get("ad") or "?"].append({"spend": num(r.get("spend")), "results": num(r.get("results")),
                                                "impressions": num(r.get("impressions")),
                                                "clicks": num(r.get("link_clicks"))})

    spend_y = sum(num(r.get("spend_yday")) for r in rows)
    res_y = sum(num(r.get("results_yday")) for r in rows)
    spend_7 = sum(num(r.get("spend_7d")) for r in rows)
    res_7 = sum(num(r.get("results_7d")) for r in rows)
    acct_cpr_7 = spend_7 / res_7 if res_7 else None
    target = a.target_cpr or acct_cpr_7
    target_source = "owner" if a.target_cpr else ("account 7-day average" if acct_cpr_7 else None)

    flags = {"pause_candidates": [], "expensive_few_results": [], "yesterday_weak": [], "results_slowing": [],
             "clicks_falling": [], "tired_audience": [], "learning_limited": [], "underspending": [],
             "doing_well": [], "too_early": []}

    adsets = {}
    for r in rows:
        name = r.get("ad") or r.get("ad name") or "?"
        sy, ry = num(r.get("spend_yday")), num(r.get("results_yday"))
        s7, r7 = num(r.get("spend_7d")), num(r.get("results_7d"))
        freq = num(r.get("frequency_7d"))
        budget = num(r.get("daily_budget"))
        learning = (r.get("learning") or "").upper()
        base = {"ad": name, "ad_set": r.get("ad_set", ""), "spend_yday": round(sy, 2),
                "results_yday": ry, "spend_7d": round(s7, 2), "results_7d": r7}
        tr = trends(per_ad_days.get(name, []), target) if target else {}
        if "days_without_result" in tr:
            base["days_without_result"] = tr["days_without_result"]
        flagged = False

        if target and s7 > 0:
            cpr7 = s7 / r7 if r7 else None
            lam7 = s7 / target                      # results expected over the week at target cost
            p7 = p_at_most(r7, lam7)
            if r7 == 0 and p7 <= ACT:
                flags["pause_candidates"].append({**base, "bad_luck_chance": chance_words(p7),
                    "why": f"spent {s7:.2f} in 7 days with no results; at the {target:.2f} target that's {lam7:.1f} expected, "
                           f"and the chance of none by bad luck is {chance_words(p7)}"})
                flagged = True
            elif 1 <= r7 <= 2 and p7 <= ACT:
                flags["expensive_few_results"].append({**base, "bad_luck_chance": chance_words(p7),
                    "why": f"{r7:g} result(s) for {s7:.2f} ({cpr7:.2f} each); at target, {lam7:.1f} were expected, "
                           f"and the chance of this few by bad luck is {chance_words(p7)}"})
                flagged = True
            elif r7 <= 2 and r7 < lam7:
                # Looks bad but could easily be chance: say when there will be enough spend to tell.
                need = s7
                while p_at_most(r7, need / target) > ACT and need < 100 * target:
                    need += target / 10
                per_day = s7 / 7
                days_left = math.ceil((need - s7) / per_day) if per_day else None
                flags["too_early"].append({**base, "bad_luck_chance": chance_words(p7),
                    "spend_needed": round(need, 2), "days_left": days_left,
                    "why": f"{r7:g} result(s) for {s7:.2f}: could easily be chance ({chance_words(p7)}). "
                           f"It needs about {need:.2f} spent to tell"
                           + (f", roughly {days_left} more days at its current spend" if days_left is not None else "")})
                flagged = True

            # Yesterday on its own: weak against the ad's own rate (or the target if it has too few results).
            ref = cpr7 if (cpr7 and r7 >= 3) else target
            lam_y = sy / ref if ref else 0
            py = p_at_most(ry, lam_y)
            if not flagged and sy > 0 and ry < lam_y and py <= YDAY:
                flags["yesterday_weak"].append({**base, "bad_luck_chance": chance_words(py),
                    "why": f"{ry:g} result(s) for {sy:.2f} yesterday where about {lam_y:.1f} were normal for it "
                           f"(chance of this by bad luck: {chance_words(py)})"})
                flagged = True

            if "results_slowing" in tr and r7 >= 3:
                flags["results_slowing"].append({**base, **tr["results_slowing"],
                    "why": f"{tr['results_slowing']['early']}; {tr['results_slowing']['late']} "
                           f"(chance of this by bad luck: {tr['results_slowing']['chance']})"})
                flagged = True

            if cpr7 and r7 >= 3 and cpr7 <= 0.7 * target and not flagged:
                flags["doing_well"].append({**base, "why": f"cost per result {cpr7:.2f} over 7 days vs target {target:.2f}"})

        if "clicks_falling" in tr:
            flags["clicks_falling"].append({**base, **tr["clicks_falling"]})
        if freq >= 3.5:
            flags["tired_audience"].append({**base, "why": f"people saw it {freq:.1f} times on average in 7 days"})
        # Budgets and learning status belong to the ad set, not the ad: collect per ad set.
        aset = adsets.setdefault(r.get("ad_set", "") or "?", {"spend_yday": 0.0, "budget": 0.0, "learning": ""})
        aset["spend_yday"] += sy
        aset["budget"] = max(aset["budget"], budget)
        aset["learning"] = aset["learning"] or learning

    for aname, aset in adsets.items():
        if "LIMITED" in aset["learning"]:
            flags["learning_limited"].append({"ad_set": aname, "why": "ad set is 'Learning limited': too few results for Meta to optimise"})
        if aset["budget"] and aset["spend_yday"] < 0.5 * aset["budget"]:
            flags["underspending"].append({"ad_set": aname, "spend_yday": round(aset["spend_yday"], 2),
                                           "why": f"ad set spent {aset['spend_yday']:.2f} of a {aset['budget']:.2f} daily budget"})

    # Account spend yesterday vs its own 7-day daily average: a budget change or a runaway ad set.
    avg_day = spend_7 / 7 if spend_7 else 0
    spend_change = None
    if avg_day and abs(spend_y - avg_day) >= 0.25 * avg_day:
        spend_change = {"spend_yday": round(spend_y, 2), "avg_day_7d": round(avg_day, 2),
                        "change_pct": round(100 * (spend_y - avg_day) / avg_day),
                        "why": f"spent {spend_y:.2f} yesterday vs {avg_day:.2f} a day over the last 7 days"}

    out = {
        "currency": a.currency,
        "yesterday": yesterday,
        "spend_change": spend_change,
        "totals": {"spend_yday": round(spend_y, 2), "results_yday": res_y,
                   "cpr_yday": round(spend_y / res_y, 2) if res_y else None,
                   "spend_7d": round(spend_7, 2), "results_7d": res_7,
                   "cpr_7d": round(acct_cpr_7, 2) if acct_cpr_7 else None},
        "target_cpr": round(target, 2) if target else None,
        "target_source": target_source,
        "ads_checked": len(rows),
        "daily_trends_read": bool(daily),
        "flags": flags,
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
