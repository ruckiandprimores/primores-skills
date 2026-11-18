---
name: meta-ads-daily-check
description: Morning check of a small business's Meta (Facebook and Instagram) ads in plain language. Yesterday's spend and cost per result against the last 7 days, ads that spent money with no results, costs creeping up, tired audiences, ad sets stuck in learning, budgets not spending, and which ads to consider pausing. Read-only, never changes ads. Use whenever someone asks how their Facebook or Instagram ads did yesterday, wants a daily or morning ads report, asks "which ads should I pause", "am I wasting money on Meta ads", or "check my ads", even without saying "daily check".
---

# Meta ads daily check

A 30-second morning message about someone's Facebook and Instagram ads, written for a business owner, not a media buyer: which ad is wasting money and what to click. The point is to catch money leaking early (an ad spending with nothing to show for it) and to make the next decision obvious. Everything here is read-only: you look and recommend, the owner decides and acts in Ads Manager.

## Why read-only

The Meta Ads connector can also edit and pause ads. Don't use any tool that changes an account, even if asked during the check. One noisy day can make a good ad look bad, and a paused ad restarts its learning when switched back on. If the owner wants to pause something after reading the check, tell them where to do it (Ads Manager > the ad > toggle off) and let them do it. That keeps a person behind every change to their money.

## 1. Get the numbers

**With the Meta Ads connector** (preferred):
1. If you don't know the ad account, call `ads_get_ad_accounts` and use the one the owner names. If there are several and they didn't say, ask once. Skip accounts where `is_queryable` is false and tell them why.
2. Call `ads_get_ad_entities` at `level` = `ad`, filtered to delivering ads (`effective_status` IN `ACTIVE`), with `date_preset` = `last_7d` and `time_increment` = `"1"` (one row per ad per day). Fields: `name`, `adset_name`, `campaign_name`, `amount_spent`, `results`, `impressions`, `link_click`. Write these rows to `daily.csv` with the columns `ad, ad_set, campaign, date, spend, results, impressions, link_clicks`. Page through with `cursor` until there are no more.
3. Call it once more at `level` = `ad`, `date_preset` = `last_7d`, no `time_increment`, for `frequency` (frequency can't be added up from daily rows). And once at `level` = `adset` for `daily_budget`, `learning_stage_info`, `effective_status`. Put these in a summary CSV (one row per ad, columns below) if you want those flags; otherwise skip it.
4. Verify field names with `ads_get_field_context` first if a call rejects one.
5. Run the script.

**Without the connector:** ask the owner to export from Ads Manager. `references/export-from-ads-manager.md` has the clicks; the best export is one with a breakdown by day, because that's what the trend flags need. Map the export's columns to the script's columns.

**Script:** `scripts/daily_check.py [summary.csv] [--daily daily.csv] [--target-cpr N] [--currency EUR]`.
- `--daily` (one row per ad per day, last 7 days): `ad, ad_set, campaign, date, spend, results, impressions, link_clicks`. On its own it's enough; the latest date counts as yesterday.
- summary CSV (one row per ad): `ad, ad_set, campaign, status, spend_yday, results_yday, spend_7d, results_7d, impressions_7d, frequency_7d, daily_budget, learning`. Adds the tired-audience, learning and budget flags.

It prints JSON with totals and flags. Use its numbers as they are; how it decides is in `references/rules.md`.

**How the script decides, in one paragraph** (you'll need it to explain flags): leads and sales are rare events, so a few days of zeros can be pure chance. For each ad the script asks: if this ad were really working at the target cost, how likely is a result this bad by bad luck? Under 10 in 100, it's probably real (pause candidate, or watch). Above that, it's too early to tell, and the script works out how much more spend (and how many days) it takes to know. This is what stops a small account from pausing ads on noise, and a big account from waiting a week on an ad that's clearly broken.

## 2. The target

The flags need a target cost per result (what a lead, purchase or booking is worth paying for). If the owner has told you one (in this chat, or in the project's instructions), pass it with `--target-cpr`. If not, the script falls back to the account's own 7-day average, and you say so in one line and ask them for a real target next time. Suggest they add it to the project's instructions so every check uses it, for example: "Target cost per lead: €25".

If the account mixes result types (leads in one campaign, purchases in another), run the check per campaign type, because one target can't fit both.

## 3. Write the check

The reader runs a business, not ads. They don't know what "cost per result", "frequency" or "learning" mean and shouldn't have to. They want to know one thing: **is any ad wasting my money, and what do I click?** So the report is a short list of instructions, not an analysis. The script does the thinking; you translate its verdicts into actions.

Use exactly this shape:

```
**Your Facebook & Instagram ads, [weekday date]**
Yesterday: [spent] → [n] [leads/sales/bookings, in their word]. [One plain verdict: "A normal day." / "Worse than usual." / "Better than usual."]

1. **[Verb] "[Ad name]"**: [why in one short sentence, with one money number]. [Where to click, if they need to do something.]
2. ...
3. ...

Your best ad right now: "[Ad name]" ([cost] per [lead]).
I don't change anything myself. Ask me "why?" about any line for the details.
```

The numbered lines, at most three, most urgent first. Each starts with a verb the owner can do or consciously not do:
- **Turn off** (from `pause_candidates`): "Turn off "Invisalign reel": €75 spent this week, no customers, and that's not bad luck. → Ads Manager, find the ad, flip the switch to off."
- **Fill in your own form** (when `results_slowing` has `after_click`): "People still click "Whitening video" but nobody has signed up for 3 days. Fill in your own form once today to check it still works."
- **Make a new version of** (from `results_slowing` with `clicks_falling`, or `results_slowing` alone): "Make a new version of "Whitening video" (same offer, new first 3 seconds). People have stopped responding to this one."
- **Keep an eye on** (from `expensive_few_results`, `yesterday_weak`, `clicks_falling` alone): "Keep an eye on "New scents carousel": €84 for one sale, about 4× your usual. If no sale by Friday, turn it off."
- **Leave alone until [date]** (from `too_early`, date = today + `days_left`): "Leave "Implant carousel" alone until 30 Nov. One lead for €45 looks bad but it's too early to judge."
- **Ask whoever set up your ads** (from `underspending`, `learning_limited`): "Ask whoever set up your ads why "Interest gifts" only spent €11 of its €30 a day."

Rules:
- If the script flagged nothing, the list is one line: "1. **Nothing to do today.**" Then the best-ad line and the footer. A quiet report is a good report.
- If there are more than three actions, keep the three that cost the most money and end with "(2 smaller things; ask me "what else?")".
- One money number per line, in their currency. No percentages of percentages, no "7-day average", no odds in numbers. The chance of bad luck becomes words: "and that's not bad luck" (pause), "too early to judge" (too_early).
- Use their word for a result: leads, sales, bookings, calls. Never "results" or "conversions".
- Tired audiences on retargeting, spend jumps under about 50%, and anything else that needs no action: leave out. Mention a spend jump only if it's big and unexplained ("You spent twice your usual yesterday. Did someone raise a budget?").
- No target set: add one line before the footer: "Tell me the most you'd pay for one [lead] and I'll judge your ads against that instead of your own average."
- When they ask "why?", then give the detail: the numbers, the comparison, the odds ("about 8 in 100 that it's bad luck"), and the rule from `references/rules.md`.
- Don't add pause calls of your own on ads the script put under `too_early`. An ad 50% over target on one lead looks bad and usually isn't yet; "leave it alone until [date]" is the most useful thing this check says.
- Don't suggest raising budgets unless asked; if asked, no more than about 20% at a time.

## 4. Things to watch for

- **Yesterday may be incomplete.** Meta's numbers for the last day can still update for a few hours, and conversions can arrive later. If the check runs early in the morning, note that yesterday may still move.
- **Very small spend.** The script already treats small numbers as "too early" rather than flagging them. If even the decision dates are weeks away, say once, plainly: "At [budget] a day, it takes weeks to know which ad works. That's a budget question for whoever runs your ads."
- **Brand-new ads** (running under 3 days) haven't had a fair chance. Never "turn off"; at most "leave alone until [date]".
- **Different currencies or time zones** across accounts: report each account separately.

## Running it every morning

In Claude Cowork, the owner can make this a scheduled task: "Every weekday at 8:00, run the Meta ads daily check for [account] with target cost per lead €25." Scheduled tasks run on their own even when the computer is asleep.
