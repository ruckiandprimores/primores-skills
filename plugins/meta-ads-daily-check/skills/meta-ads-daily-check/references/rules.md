# How the flags are decided

These are rules of thumb for small accounts, not Meta's rules. They're built to avoid the two most common small-business mistakes: pausing ads after a bad day or two that was just chance, and leaving an ad on for a week that clearly isn't working.

## The core idea: how likely is this by bad luck?

Leads and sales are rare events. If an ad at your target cost should bring one lead per €25, then €25 spent with no lead happens by pure chance about 37 times in 100. €75 with nothing happens about 5 times in 100. So the question isn't "did it spend twice the target?" but "if this ad were working at target, how likely is a result this bad?"

The script answers that with a Poisson probability (the standard model for counts of rare events), and acts only when the chance of bad luck is low:

| Chance it's bad luck | What it means |
|---|---|
| 10 in 100 or less | Probably real. Pause candidate (no results) or watch (a few, too expensive). |
| More than 10 in 100 | Could easily be chance. "Too early to tell", with how much more spend it takes to know, and roughly when. |

10 in 100 is a deliberate middle: stricter and you leave broken ads running for weeks; looser and you pause good ads on noise. With zero results it works out to about 2.3× the target spent.

## The flags

| Flag | When | Why |
|---|---|---|
| Consider pausing | 0 results in 7 days, and the chance of that by bad luck is 10 in 100 or less | A pattern, not a bad day. |
| Expensive on few results | 1-2 results in 7 days, and the chance of that few by bad luck is 10 in 100 or less | Not zero, so it's easy to miss, but it's costing well over target. |
| Too early to tell | 0-2 results, below what the target predicts, but the chance of bad luck is above 10 in 100 | Looks bad, isn't proven. The script gives the spend and days it needs before it's clear. That's the decision date. |
| Yesterday weak | Fewer results yesterday than the ad's own normal rate, with a chance of bad luck of 15 in 100 or less | One day is usually noise; this only fires when even one day is clearly off. A watch, never a pause. |
| Results slowing (needs daily data) | At least 3 results in the first 4 days, then the last 3 days well below that rate (chance of bad luck 10 in 100 or less) | Catches an ad whose weekly average still looks fine but which has stopped working. Weekly totals hide this. |
| After the click (needs daily data) | Part of Results slowing: people kept clicking in the last 3 days, but at the earlier results-per-click rate there should have been results (chance of none by bad luck 10 in 100 or less) | Points at the form, landing page or tracking rather than the ad. A test lead through the owner's own form rules that out in five minutes. |
| Clicks falling (needs daily data) | Link click rate in the last 3 days at least 30% below the first 3 days, with at least 500 impressions in each | People are tiring of the creative. Usually comes before results drop. |
| Doing well | 7-day cost per result at or below 0.7× target, at least 3 results, and no other flag | Clearly better than target, on enough results to trust. |
| Tired audience | 7-day frequency 3.5 or higher | The same people have seen it three or four times in a week. Retargeting runs higher on purpose; say so if the ad set looks like retargeting. |
| Learning limited | Ad set status "Learning limited" | Meta says the ad set isn't getting enough results to finish learning. Usual fixes: a bigger budget, a broader audience, or fewer ad sets sharing the budget. |
| Spend jump | Account spend yesterday at least 25% above or below its 7-day daily average | Usually a budget change, a new ad set, or one ad set delivering much more or less than usual. |
| Not spending | Yesterday's spend under half the ad set's daily budget | Something is holding delivery back: audience too small, bid cap too low, or the ad is in review. |

**No target given:** the script uses the account's own 7-day cost per result as the target. That makes every flag relative to the account's average, not to what the business can afford. Say this in the report and ask for a real number.

**Mixed result types:** cost per lead and cost per purchase can't share one target. Check each campaign type separately.

**What the probability doesn't know:** late-reported conversions (yesterday can still move), seasonality, and whether a lead was any good. It's a filter against noise, not a verdict.
