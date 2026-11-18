# Using an Ads Manager export instead of the connector

If the Meta Ads connector isn't switched on, the owner can export the numbers themselves. The best export is **one file, Ads tab, Last 7 days, broken down by day**: one row per ad per day. That gives both yesterday and the trend inside the week.

Ask them to:
1. Open Ads Manager (adsmanager.facebook.com), go to the **Ads** tab, and set the date range to **Last 7 days**.
2. Add a breakdown **By time > Day** (in the Breakdown menu).
3. Make sure these columns are there: ad name, ad set name, campaign name, amount spent, results, impressions, link clicks.
4. Export the table (the export option in the reporting menu gives a CSV or Excel file) and upload it to the chat.

Meta moves menu items now and then, so if the owner can't find something, ask them to describe what they see rather than guessing a path.

**Mapping to the script's `--daily` columns:**
- ad ← "Ad name"
- ad_set ← "Ad set name"
- campaign ← "Campaign name"
- date ← "Day" (or "Reporting starts" in some exports), as YYYY-MM-DD
- spend ← "Amount spent"
- results ← "Results"
- impressions ← "Impressions"
- link_clicks ← "Link clicks"

**If they can only send two plain exports** (Yesterday and Last 7 days, no breakdown): build the summary CSV instead. Join on ad name; spend_yday and results_yday from the Yesterday file, spend_7d, results_7d, impressions_7d and frequency_7d from the 7-day file. An ad only in the 7-day file didn't run yesterday: set its yesterday columns to 0. The trend flags are then skipped; say so in one line.

Frequency, daily budget and learning status don't come with the daily export. Those flags are skipped unless the owner adds a second, plain 7-day export with the frequency column.
