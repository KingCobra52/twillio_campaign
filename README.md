# Siddarth Thota Personal Alerts — compliance site

Static website publishing the required SMS compliance disclosures for
**Siddarth Thota Personal Alerts**, a private, single-recipient SMS reminder
program operated by Siddarth Thota in Pennsylvania, United States.

The site has no backend, no build step, no framework, no analytics, and no
cookies. It is deployed with GitHub Pages.

## Public pages

| Route | Purpose |
| --- | --- |
| `/` | Program overview |
| `/sms/` | SMS program disclosure: purpose, enrollment, frequency, charges, keywords |
| `/privacy/` | Privacy Policy |
| `/terms/` | Terms of Service |

## Repository layout

- `site/` — the only directory that is deployed
- `docs/` — internal notes; **not** published
- `tools/` — validation scripts; **not** published
- `CLAUDE.md` — service facts, compliance rules, and validation steps; **not** published
- `.github/workflows/pages.yml` — GitHub Actions Pages deployment

## Validating

```bash
./tools/check-site.sh
```

Checks markup, internal links and anchors, absolute-path links, external
resource loads, credentials and phone numbers, leftover placeholders, and
cross-document wording consistency. The same script runs in CI and blocks the
deployment if it fails.

## Working in this repository

Read **[`CLAUDE.md`](CLAUDE.md) first.** It holds the service facts that every
document must agree on, the compliance wording that must stay verbatim, the
validation commands, and the rules against publishing unbuilt functionality or
committing credentials.

## Deploying

Deployment is automatic on every push to the repository's default branch. One
piece of setup has to be done once by a human:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

The workflow only deploys from the default branch, and it fails the build if
internal notes or anything resembling a credential appear inside `site/`.

## Status

The Twilio campaign has **not** been submitted. See
`docs/twilio-campaign.md` section 7 for the conditions that must be met first.

## Support

hellotheking52@gmail.com
