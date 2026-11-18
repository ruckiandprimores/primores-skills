# Using an Ads Manager export instead of the connector

If the Meta Ads connector isn't switched on, the owner can export the numbers themselves. Ask them for two exports from the **Ads** tab in Ads Manager (adsmanager.facebook.com), with one row per ad:

1. Date range **Yesterday**.
2. Date range **Last 7 days**.

In each, the columns needed are: ad name, ad set name, campaign name, delivery, amount spent, results, and for the 7-day one also impressions and frequency. Then they export the table (the export option in Ads Manager's reporting menu gives a CSV or Excel file) and upload both files to the chat.

Meta moves menu items now and then, so if the owner can't find the export, ask them to describe what they see rather than guessing a path.

**Mapping to the script's columns:**
- ad ← "Ad name"
- ad_set ← "Ad set name"
- campaign ← "Campaign name"
- status ← "Delivery" (or "Ad delivery")
- spend_yday, results_yday ← "Amount spent", "Results" from the Yesterday export
- spend_7d, results_7d, impressions_7d, frequency_7d ← from the Last 7 days export
- daily_budget, learning ← leave blank if the export doesn't have them; those two flags are then skipped

Join the two exports on ad name. If an ad appears only in the 7-day export, it didn't run yesterday: set its yesterday columns to 0.
