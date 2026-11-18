# Meta ads daily check: a Claude skill for your morning Facebook and Instagram ads report

A free Claude skill that checks your Meta ads every morning and tells you, in plain words, what happened yesterday and what to do about it. Read-only: it never changes, pauses or edits an ad.

**Who it's for:** owners of small businesses who run their own Facebook and Instagram ads (or pay someone to) and want to know each morning whether money is leaking, without opening Ads Manager and reading columns.

## What you get every morning

- Yesterday's spend, results and cost per result, next to your 7-day average.
- A line when spend jumped or dropped against your usual day.
- **One thing to do today**, so you don't have to work out the priority yourself.
- Ads to **consider pausing**: money spent for a week with nothing to show.
- Ads to **watch**: no results yesterday, cost per result climbing, or one or two results at double your target.
- Ads **doing well** against your target.
- The ad-set problems that quietly cost money: audiences seeing the same ad too often, ad sets stuck in "learning limited", budgets not spending.

Every flag comes with its number and the reason, so you can disagree. The thresholds are written down in [rules.md](skills/meta-ads-daily-check/references/rules.md), and a small script applies them the same way every day.

## Sample output

> **Meta ads, Tuesday 17 November (yesterday)**
> Spent €121.70 · 4 leads · €30.43 per lead (7-day average: €19.62, your target: €25)
> That's 28% more than your usual €95.31 a day. All five ads spent more than their daily average, not just one, which usually means a budget was raised. Your export doesn't include budgets, so check whether someone changed one. Yesterday's numbers can also still move for a few hours, because some leads get counted late.
> 
> **Do today:** Pause the Free survey carousel. It has spent €96.30 this week, €21.10 of it yesterday, and brought no leads.
> 
> **Consider pausing**
> - Free survey carousel (Homeowners 35-65 Vilnius): €96.30 in 7 days and 0 leads. That's almost four leads' worth at your €25 target with nothing to show for it. In the same ad set, the savings video gets leads at €17.21, so the audience isn't the problem. This ad is.
> 
> **Watch today**
> - Grant explainer static (Homeowners 35-65 Kaunas): yesterday's one lead cost €27.90, against €16.69 a lead over the week. One lead is too few to call it, so leave it on and look again tomorrow.
> 
> **Doing well**
> - Heat pump savings video: €17.21 per lead over 7 days (14 leads) vs your €25 target
> - Testimonial reel: €12.20 per lead over 7 days (5 leads) vs €25. People saw it 4.6 times on average this week, which would be a lot for a cold audience. This one is retargeting your site visitors, though, so a high number is normal. Watch it only if the cost per lead starts to climb.
> 
> Yesterday's €30.43 per lead is above your target, but most of that is the €21.10 the survey carousel spent with no leads. Without it, the other four ads got 4 leads for €100.60, about €25 each.
> 
> Nothing here changes your ads. To pause one: Ads Manager > Ads > switch it off.

*(Made-up account. Your check uses your own ad names and currency.)*

## What it is honestly good at, and what it isn't

We tested it against Claude with no skill on the same numbers. Plain Claude spots most of the same problems if you hand it the data and ask well. What the skill adds is the routine: it pulls the numbers itself through the Meta Ads connector, uses the same rules and the same one-screen format every morning, asks for your real target cost per lead instead of guessing, and stays read-only. If you already have a media buyer reading your account daily, you don't need this.

## Setup (5 minutes)

1. Install the plugin: see [install instructions](../../docs/install.md). Short version for the Claude app: Customize > Plugins > Add > "Add marketplace" > "Add from a repository" > `ruckiandprimores/primores-skills`, then install `meta-ads-daily-check`.
2. Switch on the **Meta Ads** connector in Customize > Connectors and sign in with the Facebook account that has access to your ad account. No connector? The skill asks you for two exports from Ads Manager instead ([how](skills/meta-ads-daily-check/references/export-from-ads-manager.md)).
3. Tell Claude your target: "Target cost per lead: €25". Put it in your project's instructions so every check uses it.
4. Ask: "How did my ads do yesterday?"

**Every morning without asking:** in Claude Cowork, create a scheduled task, for example "Every weekday at 8:00, run the Meta ads daily check for [account], target cost per lead €25."

## What it never does

- Never pauses, edits, creates or deletes an ad, even if you ask during the check. It tells you where to click; you click.
- Never changes budgets or bids.
- Never sends your numbers anywhere except your own Claude conversation.

## FAQ

**Does it work with Instagram ads?** Yes. Instagram ads run through Meta Ads Manager, so they're in the same account.

**What if I sell online, not leads?** Use your target cost per purchase instead. If one account has both lead and purchase campaigns, the skill checks them separately.

**Why doesn't it just pause bad ads for me?** One bad day often looks worse than it is, and a paused ad restarts Meta's learning when you switch it back on. A person should make that call.

**Can I use it for my business on a Pro plan?** Depends where you are. In the EU, EEA, Switzerland and the UK, Anthropic's consumer plans don't allow business use; use Claude Team or Enterprise there.

**Is it really free?** Yes, MIT licence. It's made by [Primores](https://primores.org), a Meta and Telegram ads agency; if you'd rather someone ran the ads for you, that's what we do.
