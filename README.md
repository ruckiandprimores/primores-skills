# Primores skills: small, free Claude skills for businesses on Meta ads

Each skill here does **one job you'd otherwise do by hand every day**, inside your own Claude account. No dashboards, no new software to learn. You ask Claude ("how did my ads do yesterday?"), the skill does the checking, and you decide what to do.

They're deliberately narrow. A skill that tries to run your whole marketing does nothing well; a skill that checks one thing every morning, the same way every time, actually gets used.

Made by [Primores](https://primores.org). We run Meta and Telegram ads for small and mid-sized businesses, and we built these for our own day-to-day work first.

## The skills

| Skill | The daily job | You need | Status |
|---|---|---|---|
| [**meta-ads-daily-check**](plugins/meta-ads-daily-check/) | Every morning: which Facebook or Instagram ad is wasting your money, which to leave alone, and exactly what to click | Meta Ads connector, or an Ads Manager export | Ready |
| lead-reply-drafts | New leads scored against your rules, with a reply and three free calendar slots drafted in Gmail | Gmail and Google Calendar connectors, a Google Sheet of leads | Planned |
| lead-follow-up | Who hasn't answered in two days, with follow-ups drafted | Same Google Sheet | Planned |
| booked-to-meta | Marks which leads booked, so Meta can optimise your ads for bookings instead of form fills | Google Sheet + a free Zapier step | Planned |

All of them are **read-only or draft-only**: they never change your ads, never send a message for you, and never move money. You stay the one who clicks.

## Install

Three ways, depending on how you use Claude. Full steps with notes: [docs/install.md](docs/install.md).

**Claude app (web, desktop or Cowork, any paid plan)**
1. Customize > Plugins > Add > "Add marketplace" > "Add from a repository".
2. Enter `ruckiandprimores/primores-skills`.
3. Install the plugin you want, for example `meta-ads-daily-check`.

**Claude Code**
```
claude plugin marketplace add ruckiandprimores/primores-skills
claude plugin install meta-ads-daily-check@primores-skills
```

**Skill only (ZIP upload)**: download the skill's folder (for example `plugins/meta-ads-daily-check/skills/meta-ads-daily-check`), zip it, then in the Claude app go to Customize > Skills > "+" > "Upload a skill". Code execution must be switched on.

## Before you use them for your business

These skills run on your own Claude plan, so check that your plan allows business use where you live. In the EU, EEA, Switzerland and the UK, Anthropic's consumer terms (Free, Pro, Max) say: "You agree that you will not use our Services for any commercial or business purposes". There, use a Claude Team or Enterprise plan.

Anthropic doesn't review plugins you add from a repository, so read what a skill does before you install it. Everything here is plain text you can read in a few minutes: start with each skill's `SKILL.md`.

## Questions, ideas, problems

Open an issue on this repo. If you'd rather have someone set this up for you, or run the ads themselves, that's what we do: [primores.org](https://primores.org).

## License

MIT
