# Meta ads daily check: know every morning which Facebook ad is wasting your money

Every morning, Claude looks at your Facebook and Instagram ads and sends you a short message: which ad to turn off, which to leave alone, and exactly where to click. No dashboards, no marketing words. It takes 30 seconds to read.

It never changes anything in your ads. You stay the one who clicks.

## What the morning message looks like

> **Your Facebook & Instagram ads, Wednesday 18 Nov**
> Yesterday: €68 spent → 1 lead. Worse than usual (you normally get about 2 a day for that).
> 
> 1. **Fill in your own form for "Whitening offer video"**: it was your busiest ad, but €90 over the last 3 days brought no leads while people kept clicking. Send yourself a test lead today. If it arrives fine, make a new version of the ad (same offer, new first 3 seconds), because fewer people are clicking on this one too.
> 2. **Turn off "Invisalign reel"**: €75 spent this week, no leads, and that's not bad luck. → Ads Manager, find the ad, flip the switch to off.
> 3. **Leave "Implant consult carousel" alone until 30 Nov**: one lead for €45 looks bad, but at its small budget it's too early to judge.
> 
> Your best ad right now: "Family dentist static" (€20 per lead).
> I don't change anything myself. Ask me "why?" about any line for the details.

*(Made-up dental clinic. Yours uses your own ads and currency.)*

That's it. If you want the detail behind a line, ask "why?" and Claude explains the numbers.

## Why it's worth having

- **It catches money leaking early.** An ad that's spent €75 and brought nobody is easy to miss when you only look at the weekly total.
- **It stops you turning off good ads too soon.** Two quiet days often mean nothing. It tells you when it's too early to judge, and the date when it won't be.
- **It notices when something breaks.** If people keep clicking but nobody signs up, it tells you to test your own form before you blame the ad.
- **It's the same check every day.** Same rules, same format, so you learn to read it in seconds.

## Set it up (about 5 minutes)

You need a paid Claude plan and access to your Facebook ad account.

1. **Add the skill to Claude.** In Claude, open **Customize**, then **Plugins**, then **Add**. Choose **Add marketplace**, then **Add from a repository**, and type `ruckiandprimores/primores-skills`. Install **meta-ads-daily-check**.
2. **Connect your ad account.** Still in **Customize**, open **Connectors**, switch on **Meta Ads**, and log in with the Facebook account you use for ads.
3. **Tell Claude what a customer is worth.** Type, for example: "The most I'll pay for one lead is €30." (Not sure? Ask Claude to help you work it out from your average sale.)
4. **Ask:** "How did my ads do yesterday?"

**To get it every morning without asking:** in Claude Cowork, create a scheduled task: "Every weekday at 8:00, check my Facebook ads." It runs even when your computer is off.

**No time, or got stuck?** [Send us a message](https://primores.org/contact/) and we'll set it up for you.

## What it never does

- Never turns off, edits or creates an ad. It tells you where to click; you click.
- Never changes your budget.
- Never sends your numbers anywhere outside your own Claude.

## Questions

**Does it work for Instagram ads?** Yes. Instagram ads run from the same Facebook ad account.

**I sell online, not leads.** Same thing: tell it the most you'll pay for one sale.

**Why doesn't it just turn bad ads off for me?** One bad day often looks worse than it is, and an ad you turn off and back on has to start learning again. A person should make that call.

**Is it smarter than asking Claude myself?** Not much, if you know what to ask and paste in the right numbers. What it adds is that it gets the numbers itself, every morning, checks them the same way each time, and knows the difference between bad luck and a real problem. If someone already checks your ads every day, you don't need it.

**Can I use it for my business on Claude Pro?** Depends where you are. In the EU, EEA, Switzerland and the UK, Anthropic's personal plans don't allow business use; use Claude Team or Enterprise there.

**Is it really free?** Yes. It's made by [Primores](https://primores.org). We run Facebook, Instagram and Telegram ads for businesses; if you'd rather someone ran your ads for you, that's what we do.

---

*For the technically curious: how each flag is decided is in [rules.md](skills/meta-ads-daily-check/references/rules.md); the arithmetic is a small script in [scripts/](skills/meta-ads-daily-check/scripts/). Claude Code users: `claude plugin marketplace add ruckiandprimores/primores-skills`, then `claude plugin install meta-ads-daily-check@primores-skills`.*
