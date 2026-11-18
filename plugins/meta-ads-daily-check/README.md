# Meta ads daily check: a Claude skill for your morning Facebook and Instagram ads report

A free Claude skill that checks your Meta ads every morning and tells you, in plain words, what happened yesterday and what to do about it. Read-only: it never changes, pauses or edits an ad.

**Who it's for:** owners of small businesses who run their own Facebook and Instagram ads (or pay someone to) and want to know each morning whether money is leaking, without opening Ads Manager and reading columns.

## What you get every morning

- Yesterday's spend, results and cost per result, next to your 7-day average.
- A line when spend jumped or dropped against your usual day.
- **One thing to do today**, so you don't have to work out the priority yourself.
- Ads to **consider pausing**, only when the numbers say it's unlikely to be bad luck ("about 2 in 100 that this is chance").
- Ads to **watch**: an ad whose weekly average still looks fine but which stopped bringing leads in the last few days, fewer people clicking, or one or two results at well over your target.
- Ads that are **too early to tell**, with the date they'll be clear. This is what stops you pausing a good ad after two quiet days.
- A nudge to **test your own form** when people keep clicking but leads stop.
- Ads **doing well** against your target.
- The ad-set problems that quietly cost money: audiences seeing the same ad too often, ad sets stuck in "learning limited", budgets not spending.

Every flag comes with its number and the reason, so you can disagree. Flags are decided by how likely the result is by chance, not by fixed rules, so a €5-a-day account and a €500-a-day account are judged fairly. The thresholds are written down in [rules.md](skills/meta-ads-daily-check/references/rules.md), and a small script applies them the same way every day.

## Sample output

> **Meta ads, Tuesday 17 November (yesterday)**
> Spent €68 · 1 lead · €68 per lead (7-day average: €31.33, against your €30 target)
> Yesterday's numbers can still move by a few hours' worth of late leads, so treat that €68 as provisional.
> 
> **Do today:** get a fresh version of the Whitening offer video made and into its ad set. It was your best ad and has stopped bringing leads; at €30 a day it's where most of the money is leaking.
> 
> **Consider pausing**
> - Invisalign reel (Adults 20-40 15km): spent €75 in 7 days with no leads. At €30 a lead it should have brought about 2.5, and the chance of none by bad luck is about 8 in 100. That's a pattern, not a bad week.
> 
> **Watch today**
> - Whitening offer video (Women 25-50 10km): 7 leads for €120 (€17 each) in the first four days, then nothing for €90 over the last three, when about 5 were expected. About 1 in 100 that this is bad luck. Clicks fell at the same time: 1.96% of people who saw it clicked in the first three days, 0.91% in the last three. People in that 10 km radius are tiring of this video, so a new cut of the same whitening offer (new opening, new visuals) is a better fix than pausing. If you don't have a new version up by Friday and it still has no leads, pause it then.
> 
> **Too early to tell**
> - Implant consult carousel (Adults 45-70 15km): 1 lead for €45. That looks slow, but there's about a 56 in 100 chance it's just luck. It needs about €117 spent to tell, which at €6-7 a day is around Monday 30 November. Leave it until then.
> 
> **Doing well**
> - Family dentist static (Parents 28-45 10km): €20 per lead over 7 days vs your €30 target, a lead every day.
> 
> Nothing here changes your ads. To pause one: Ads Manager > Ads > switch it off.

*(Made-up account. Your check uses your own ad names and currency.)*

## What it is honestly good at, and what it isn't

We tested it against Claude with no skill on the same numbers, four made-up accounts. Plain Claude spots most of the big problems if you hand it the data and ask well. What the skill adds:
- **The routine.** It pulls the numbers itself through the Meta Ads connector, uses the same rules and the same one-screen format every morning, and stays read-only.
- **The odds.** It says how likely a bad-looking number is to be chance, and when an unproven ad will be clear. Plain Claude tends to say "too early" without saying until when.
- **Day-by-day reading.** With a by-day export or the connector, it catches an ad that stopped working this week while its weekly average still looks fine.

What it can't know: whether your leads were any good. Cost per lead can look great while nobody picks up the phone. If you already have a media buyer reading your account daily, you don't need this.

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
