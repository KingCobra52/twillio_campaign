# CLAUDE.md

Guidance for Claude Code (and any human contributor) working in this repository.

Read this file before changing anything. The site it builds is a **compliance
document set** that Twilio and mobile carriers review. Wording here is not
decorative: changing a sentence can make a published claim untrue.

---

## 1. What this repository is

A static website that publishes the required disclosures for a private SMS
program, deployed with GitHub Pages. There is no backend, no database, no build
step, and no runtime dependency of any kind.

---

## 2. Service facts (the single source of truth)

Every fact below must match everywhere it appears — on the website, in
`docs/`, and in anything submitted to Twilio. If a fact changes, change it in
all of those places in the same commit.

| Fact | Value |
| --- | --- |
| Program name | Siddarth Thota Personal Alerts |
| Operator / registered identity | Siddarth Thota, an individual |
| Location | Commonwealth of Pennsylvania, United States |
| Recipients | One — Siddarth Thota (the operator) |
| Message type | Personal reminders and alerts |
| Marketing content | None |
| Public enrollment | None. No signup form exists anywhere on the site. |
| Enrollment method | Manual, single user, performed by the operator outside this website |
| Message frequency | Varies |
| Cost to recipient | None from the operator; carrier message and data rates may apply |
| Support contact | `hellotheking52@gmail.com` (intentionally public) |
| Messaging provider | Twilio |
| Hosting provider | GitHub Pages |
| Governing law | Commonwealth of Pennsylvania |
| Opt-out keyword | `STOP` (also `END`, `CANCEL`, `UNSUBSCRIBE`, `QUIT`) |
| Resubscribe keyword | `START` (also `UNSTOP`, `YES`) |
| Help keyword | `HELP` (also `INFO`) |

---

## 3. Required compliance language

These strings are load-bearing. Keep them verbatim (capitalisation of keywords
included) unless a compliance requirement changes.

**Must appear, word for word, in the Privacy Policy and on the `/sms/` page:**

> Mobile numbers and SMS consent data are not sold, rented, or shared with
> third parties or affiliates for marketing or promotional purposes.

**Must appear on `/sms/` and in the Terms of Service:**

- "Message and data rates may apply."
- "Message frequency varies." (or "Frequency: Varies")
- Reply `STOP` to cancel, `START` to resubscribe, `HELP` for help.
- The support email address, as a working `mailto:` link.
- Links to both the Privacy Policy and the Terms of Service.

**Every outbound SMS template** in `docs/message-templates.md` must:

1. Start with the program name, `Siddarth Thota Personal Alerts:`.
2. Contain an opt-out instruction (`Reply STOP to cancel`).
3. Contain `Msg&data rates may apply` on opt-in, HELP, and sample messages.

**Governing law** is Pennsylvania. Do not substitute another state, and do not
add an arbitration clause without an explicit instruction to do so.

---

## 4. Hard rules

1. **Never invent functionality that does not exist.** The site must not
   describe a feature, form, workflow, integration, or automation that has not
   been built. In particular:
   - There is **no public signup form**. Never add one or describe one.
   - The planned Codex-driven reminder data flow is **not built**. It must not
     be described anywhere as operational, live, or available. Its design lives
     in `docs/consent-workflow-design.md` and is labelled as a proposal.
   - Do not fabricate screenshots, opt-in records, consent logs, timestamps,
     recipient counts, or message volumes.
2. **Never commit credentials.** No Twilio Account SID (`AC…`), Auth Token,
   API Key (`SK…`), Messaging Service SID (`MG…`), webhook signing secret,
   `.env` file, or private key. No private phone number in any form, including
   the operator's own and the program's sending number. Use placeholders such
   as "the program's sending number" instead.
3. **Never publish internal notes.** Only `site/` is deployed. `docs/` and this
   file stay in the repository and out of the artifact. The workflow fails the
   build if internal files appear under `site/`.
4. **Never let the documents contradict each other.** The `/sms/` disclosure,
   the Privacy Policy, the Terms of Service, and `docs/twilio-campaign.md` must
   describe the same program with the same facts.
5. **Do not submit the Twilio campaign** until a real consent workflow exists,
   or until there is truthful, reviewable evidence of the manual opt-in.
   Writing the campaign copy is fine; submitting it on the strength of a
   workflow that has not been built is not.

---

## 5. Project structure

```
.
├── CLAUDE.md                 # This file. Not published.
├── README.md                 # Repository overview. Not published.
├── .github/workflows/
│   └── pages.yml             # Official GitHub Actions Pages deployment
├── docs/                     # Internal notes. NEVER published.
│   ├── consent-workflow-design.md
│   ├── message-templates.md
│   └── twilio-campaign.md
├── tools/                    # Validation scripts. Not published.
│   ├── check-site.sh         # Runs every automated check
│   ├── check-links.py        # Internal links and anchors
│   └── check-consistency.py  # Cross-document wording consistency
└── site/                     # The ONLY directory that is deployed
    ├── .nojekyll             # Serve files as committed, no Jekyll processing
    ├── 404.html
    ├── index.html            # /
    ├── robots.txt
    ├── assets/
    │   ├── css/styles.css    # All styling; no external fonts or CDNs
    │   └── js/main.js        # Progressive enhancement only
    ├── privacy/index.html    # /privacy/
    ├── sms/index.html        # /sms/
    └── terms/index.html      # /terms/
```

### Conventions

- **Semantic HTML**, one `<h1>` per page, headings in order, no skipped levels.
- **Relative URLs everywhere**, so the site works under the project-pages
  subpath (`/twillio_campaign/`). From `site/index.html` use `sms/`; from
  `site/sms/index.html` use `../privacy/`. Never write a leading-slash link.
  - **One documented exception:** `site/404.html` is served for arbitrary
    paths, so relative URLs cannot resolve there. It uses absolute
    `/twillio_campaign/...` links. If the repository is renamed, update that
    file.
- **Real directories with `index.html`**, so `/privacy/` works on direct
  navigation and refresh without any client-side routing.
- **No framework, no analytics, no cookies, no storage, no third-party
  requests.** Everything the browser loads is served from this repository.
- Every page must work with JavaScript disabled.

---

## 6. Validation

There is no build step, so validation is a set of checks. Run all of them from
the repository root before every commit that touches `site/`:

```bash
./tools/check-site.sh
```

It exits non-zero if anything fails, and the same script runs in CI on every
deployment. It covers:

1. **HTML well-formedness** of every page (`tidy`; install with
   `apt-get install -y tidy`, skipped with a notice if absent).
2. **No absolute-path links**, so the site keeps working under the project-pages
   subpath. `site/404.html` is the one documented exception.
3. **No external resource loads** — no CDNs, fonts, trackers, or iframes. The
   only outbound URL allowed is the informational `https://www.twilio.com/`
   link on the home page.
4. **No credentials, Twilio identifiers, or phone numbers** anywhere in `site/`.
5. **No placeholders** (`TODO`, `TBD`, `{{`, `example.com`, `PAGES_URL`, …).
6. **Every internal link and `#anchor` resolves**, checked against the real
   directory layout as GitHub Pages would serve it (`tools/check-links.py`).
7. **Cross-document consistency** (`tools/check-consistency.py`): the six SMS
   templates are byte-identical in `/sms/`, `docs/message-templates.md`, and
   `docs/twilio-campaign.md`; the no-sale sentence appears verbatim where it is
   required; and the program name, operator, location, support address,
   frequency language, carrier-charge language, and keywords agree everywhere.

### Checks that still need a person

Run a local server and open each route:

```bash
mkdir -p /tmp/pages && cp -r site /tmp/pages/twillio_campaign
python3 -m http.server 8000 --directory /tmp/pages
# then open http://localhost:8000/twillio_campaign/ , /sms/ , /privacy/ , /terms/
# and reload each one directly to confirm real static paths are served
```

- Resize to 360 px wide: no horizontal scrolling, no clipped text.
- Tab through each page: the skip link appears first, every link shows a visible
  focus ring, and focus order matches reading order.
- View each page in both light and dark mode. Body text must stay at or above
  WCAG AA (4.5:1); the current palette is measured at 6.8:1 or better for text
  and 3.5:1 or better for borders and focus rings in both modes.
- Disable JavaScript and confirm every page still works completely.
- Read `/sms/`, the Privacy Policy, the Terms of Service, and
  `docs/twilio-campaign.md` side by side. The automated check catches wording
  drift; only a person catches a claim that is merely untrue.

### After deploying

- Load all four routes on the live Pages URL, signed out, in a private window,
  on both a phone and a desktop browser. All four must return 200.
- Refresh each route directly rather than navigating to it, to confirm static
  paths are served.
- Re-run check 4 against the deployed HTML, not just the source.

## 7. Deployment

GitHub Pages is the only hosting service, deployed by
`.github/workflows/pages.yml` using `actions/configure-pages`,
`actions/upload-pages-artifact`, and `actions/deploy-pages`.

One-time repository setup, done by a human in the GitHub web interface:

1. **Settings → Pages → Build and deployment → Source:** select
   **GitHub Actions**.
2. Make sure the branch carrying this code is the repository's **default
   branch**. The workflow only deploys from the default branch, and the
   `github-pages` environment only accepts deployments from it.

No custom domain is configured or assumed. The published URL is the generated
GitHub Pages URL for this repository:

- Home: `https://<owner>.github.io/<repo>/`
- SMS disclosure: `https://<owner>.github.io/<repo>/sms/`
- Privacy Policy: `https://<owner>.github.io/<repo>/privacy/`
- Terms of Service: `https://<owner>.github.io/<repo>/terms/`

The Privacy Policy and Terms of Service URLs are the two outputs the Twilio
campaign registration form needs. Record them in `docs/twilio-campaign.md`
once the first deployment has succeeded and the URLs have been loaded and
confirmed.
