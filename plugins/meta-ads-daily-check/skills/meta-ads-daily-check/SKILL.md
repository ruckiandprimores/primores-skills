---
name: meta-ads-daily-check
description: Morning check of a small business's Meta (Facebook and Instagram) ads in plain language. Yesterday's spend and cost per result against the last 7 days, ads that spent money with no results, costs creeping up, tired audiences, ad sets stuck in learning, budgets not spending, and which ads to consider pausing. Read-only, never changes ads. Use whenever someone asks how their Facebook or Instagram ads did yesterday, wants a daily or morning ads report, asks "which ads should I pause", "am I wasting money on Meta ads", or "check my ads", even without saying "daily check".
---

# Meta ads daily check

A two-minute morning read of someone's Meta ads, written for a business owner, not a media buyer. The point is to catch money leaking early (an ad spending with nothing to show for it) and to make the next decision obvious. Everything here is read-only: you look and recommend, the owner decides and acts in Ads Manager.

## Why read-only

The Meta Ads connector can also edit and pause ads. Don't use any tool that changes an account, even if asked during the check. One noisy day can make a good ad look bad, and a paused ad restarts its learning when switched back on. If the owner wants to pause something after reading the check, tell them where to do it (Ads Manager > the ad > toggle off) and let them do it. That keeps a person behind every change to their money.

## 1. Get the numbers

**With the Meta Ads connector** (preferred):
1. If you don't know the ad account, call `ads_get_ad_accounts` and use the one the owner names. If there are several and they didn't say, ask once. Skip accounts where `is_queryable` is false and tell them why.
2. Call `ads_get_ad_entities` at `level` = `ad`, filtered to delivering ads (`effective_status` IN `ACTIVE`), twice:
   - `date_preset` = `yesterday`, fields: `name`, `adset_name`, `campaign_name`, `effective_status`, `amount_spent`, `results`, `cost_per_result`
   - `date_preset` = `last_7d`, fields: `amount_spent`, `results`, `cost_per_result`, `impressions`, `frequency`
   Verify field names with `ads_get_field_context` first if the call rejects one. Page through with `cursor` until there are no more.
3. For daily budgets and learning status, call it once more at `level` = `adset` with `daily_budget`, `learning_stage_info`, `effective_status`.
4. Write one CSV row per ad with the columns the script expects (see below) and run the script.

**Without the connector:** ask the owner to export from Ads Manager. `references/export-from-ads-manager.md` has the exact clicks; it takes them about a minute. Map the export's columns to the script's columns.

**Script:** `scripts/daily_check.py <file.csv> [--target-cpr N] [--currency EUR]`. Columns: `ad, ad_set, campaign, status, spend_yday, results_yday, spend_7d, results_7d, impressions_7d, frequency_7d, daily_budget, learning`. It prints JSON with totals and flags. Use its numbers as they are; the thresholds are explained in `references/rules.md`.

## 2. The target

The flags need a target cost per result (what a lead, purchase or booking is worth paying for). If the owner has told you one (in this chat, or in the project's instructions), pass it with `--target-cpr`. If not, the script falls back to the account's own 7-day average, and you say so in one line and ask them for a real target next time. Suggest they add it to the project's instructions so every check uses it, for example: "Target cost per lead: €25".

If the account mixes result types (leads in one campaign, purchases in another), run the check per campaign type, because one target can't fit both.

## 3. Write the check

Keep it to one screen. Use this structure, and leave out any section that has nothing in it:

```
**Meta ads, [weekday date] (yesterday)**
Spent [x] · [n] results · [cost] per result (7-day average: [cost])
[Only if spend_change is set: "That's [n]% more/less than your usual [avg] a day." plus the likeliest reason if you can see it]

**Do today:** [the one action that matters most, with the decision date if it's a wait: "pause X", or "leave X until Thursday; pause if still no leads"]

**Consider pausing**
- [Ad name] ([ad set]): [why, with the number]

**Watch today**
- [Ad name]: [why]

**Doing well**
- [Ad name]: [cost per result] vs target [target]

**Also worth knowing**
- [tired audience / learning limited / budget not spending, one line each]

Nothing here changes your ads. To pause one: Ads Manager > Ads > switch it off.
```

Where the script's flags go: `pause_candidates` under Consider pausing; `watch_no_results`, `cost_rising` and `expensive_few_results` under Watch (an expensive ad that also spent at least two target results' worth in the week can go under Consider pausing, say why); `doing_well` under Doing well; the ad-set flags under Also worth knowing. Each ad appears in one section only: if it fits two, put it in the more urgent one.

The "Do today" line is there because a list of flags still leaves the owner to work out what to do first. Pick one thing. If the honest answer is "nothing", say "Nothing to do today" and still give a date: when the next real decision comes (for example "by Friday Before after photos will have spent about two leads' worth; pause it then if still nothing"). Work it out from the ad's daily spend and the pause threshold. A quiet report with a date tells the owner when to pay attention again; without one they keep checking.

How to write it:
- Lead with money. "Spent €43 in a week and brought no leads" lands; "zero conversion rate" doesn't.
- Every flag has its number and the comparison behind it, so the owner can disagree.
- Say what each flag means for a decision: "pause candidate", "give it until tomorrow", "fine, leave it".
- No jargon without a plain word next to it: frequency becomes "people saw it 4 times on average"; learning limited becomes "too few results for Meta to optimise".
- If nothing is flagged, say so in one line ("Nothing to act on today") and stop. A quiet day is a good report.
- Don't recommend raising budgets by more than about 20% at a time on "doing well" ads; bigger jumps send an ad set back into learning. Mention it only when the owner asks what to do with a winner.

## 4. Things to watch for

- **Yesterday may be incomplete.** Meta's numbers for the last day can still update for a few hours, and conversions can arrive later. If the check runs early in the morning, note that yesterday may still move.
- **Very small spend.** If the whole account spent less than about two target results yesterday, most flags are noise. Say that instead of listing them.
- **Brand-new ads** (running under 3 days) haven't had a fair chance. Don't put them in "consider pausing"; put them in "watch".
- **Different currencies or time zones** across accounts: report each account separately.

## Running it every morning

In Claude Cowork, the owner can make this a scheduled task: "Every weekday at 8:00, run the Meta ads daily check for [account] with target cost per lead €25." Scheduled tasks run on their own even when the computer is asleep.
