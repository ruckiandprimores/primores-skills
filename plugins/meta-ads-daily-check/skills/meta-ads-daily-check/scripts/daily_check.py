"""Meta ads daily check: turn per-ad numbers into flags, the same way every morning.

Input: a CSV with one row per ad and these columns (names are case-insensitive;
extra columns are ignored):
  ad, ad_set, campaign, status,
  spend_yday, results_yday,
  spend_7d, results_7d, impressions_7d, frequency_7d,
  daily_budget            (optional, the ad set's daily budget, repeated on each of its ads; blank if lifetime or campaign budget)
  learning                (optional, e.g. "LEARNING", "LEARNING_LIMITED", "SUCCESS")

Usage:
  python daily_check.py ads.csv --target-cpr 25 --currency EUR
  python daily_check.py ads.csv            # no target: uses the account's own 7-day cost per result

Prints a JSON object with totals and flagged ads. The skill writes the summary from it.
Why a script: the thresholds should be applied identically every day, so the owner
can trust that "this ad is flagged" means the same thing on Monday and Friday.
"""
import argparse, csv, json, sys


def num(v):
    try:
        return float(str(v).replace(",", "").strip() or 0)
    except ValueError:
        return 0.0


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [{k.strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--target-cpr", type=float, default=None, help="target cost per result")
    ap.add_argument("--currency", default="")
    a = ap.parse_args()

    rows = load(a.csv)
    if not rows:
        print(json.dumps({"error": "no rows"}))
        return 1

    spend_y = sum(num(r.get("spend_yday")) for r in rows)
    res_y = sum(num(r.get("results_yday")) for r in rows)
    spend_7 = sum(num(r.get("spend_7d")) for r in rows)
    res_7 = sum(num(r.get("results_7d")) for r in rows)
    acct_cpr_7 = spend_7 / res_7 if res_7 else None
    target = a.target_cpr or acct_cpr_7
    target_source = "owner" if a.target_cpr else ("account 7-day average" if acct_cpr_7 else None)

    flags = {"pause_candidates": [], "watch_no_results": [], "cost_rising": [], "expensive_few_results": [],
             "tired_audience": [], "learning_limited": [], "underspending": [], "doing_well": []}

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

        if target:
            # Spent two "target results" worth over a week and got nothing: a pause candidate.
            if r7 == 0 and s7 >= 2 * target:
                flags["pause_candidates"].append({**base, "why": f"spent {s7:.2f} in 7 days, 0 results (2x target is {2*target:.2f})"})
            # One bad day is noise; worth watching, not pausing.
            elif ry == 0 and sy >= target:
                flags["watch_no_results"].append({**base, "why": f"spent {sy:.2f} yesterday, 0 results"})
            cpr7 = s7 / r7 if r7 else None
            cpry = sy / ry if ry else None
            # Yesterday 50%+ dearer than its own week, with enough results to mean something.
            rising = bool(cpr7 and cpry and r7 >= 3 and cpry > 1.5 * cpr7)
            if rising:
                flags["cost_rising"].append({**base, "why": f"cost per result {cpry:.2f} yesterday vs {cpr7:.2f} over 7 days"})
            # A result or two, but each one cost at least double the target: not zero, still expensive.
            if cpr7 and 1 <= r7 <= 2 and cpr7 >= 2 * target:
                flags["expensive_few_results"].append({**base, "why": f"{r7:g} result(s) in 7 days at {cpr7:.2f} each vs target {target:.2f}"})
            # Doing well over the week; skipped when yesterday got dearer, so an ad is never both "watch" and "doing well".
            if cpr7 and r7 >= 3 and cpr7 <= 0.7 * target and not rising:
                flags["doing_well"].append({**base, "why": f"cost per result {cpr7:.2f} over 7 days vs target {target:.2f}"})
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

    # Account spend yesterday vs its own 7-day daily average: catches a budget change or a runaway ad set.
    avg_day = spend_7 / 7 if spend_7 else 0
    spend_change = None
    if avg_day and abs(spend_y - avg_day) >= 0.25 * avg_day:
        spend_change = {"spend_yday": round(spend_y, 2), "avg_day_7d": round(avg_day, 2),
                        "change_pct": round(100 * (spend_y - avg_day) / avg_day),
                        "why": f"spent {spend_y:.2f} yesterday vs {avg_day:.2f} a day over the last 7 days"}

    out = {
        "currency": a.currency,
        "spend_change": spend_change,
        "totals": {"spend_yday": round(spend_y, 2), "results_yday": res_y,
                   "cpr_yday": round(spend_y / res_y, 2) if res_y else None,
                   "spend_7d": round(spend_7, 2), "results_7d": res_7,
                   "cpr_7d": round(acct_cpr_7, 2) if acct_cpr_7 else None},
        "target_cpr": round(target, 2) if target else None,
        "target_source": target_source,
        "ads_checked": len(rows),
        "flags": flags,
    }
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
