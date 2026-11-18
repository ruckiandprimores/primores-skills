# How to install Primores skills

## Option 1: Claude app (recommended for most people)

Works on the web app, the desktop app and Claude Cowork, on any paid plan (Pro, Max, Ultra, Team, Enterprise).

1. Open Claude and go to **Customize > Plugins**.
2. Click **Add**, then **Add marketplace**, then **Add from a repository**.
3. Enter `ruckiandprimores/primores-skills` and confirm.
4. You'll see the list of skills. Install the one you want.
5. Switch on the connectors the skill needs (Customize > Connectors). Each skill's page says which ones.

Updates: when we change a skill, the marketplace update brings it in; you don't re-upload anything.

Anthropic doesn't review plugins added from a repository. Read the skill's `SKILL.md` before you install; it's short and plain text.

## Option 2: Claude Code

```
claude plugin marketplace add ruckiandprimores/primores-skills
claude plugin install meta-ads-daily-check@primores-skills
```

To get updates later: `claude plugin marketplace update primores-skills`.

## Option 3: upload just the skill (ZIP)

If plugins aren't available to you:

1. Download the skill's folder from GitHub, for example `plugins/meta-ads-daily-check/skills/meta-ads-daily-check/` (the folder that contains `SKILL.md`).
2. Zip that folder.
3. In the Claude app: **Customize > Skills > "+" > "Upload a skill"**, and pick the zip.
4. Make sure code execution is switched on; the skills use a small script for their arithmetic.

With a ZIP you'll need to re-upload to get updates.

## Running a skill every morning

In Claude Cowork you can make any of these a scheduled task, for example: "Every weekday at 8:00, run the Meta ads daily check for my account, target cost per lead €25." Scheduled tasks run even when your computer is asleep.

## Business use and your plan

In the EU, EEA, Switzerland and the UK, Anthropic's consumer terms for Free, Pro and Max don't allow business use. Use Claude Team or Enterprise there. Elsewhere, check the terms that apply to your account.
