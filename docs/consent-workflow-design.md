# Design: private consent workflow

**Status: PROPOSAL — NOT BUILT.** Nothing described in this document exists
today. No code implements it, no interface renders it, and no data is stored by
it. Do not describe any part of it on the public website, in the Twilio
campaign, or to a carrier as though it were operational.

**Internal document.** Not published to GitHub Pages.

---

## 1. Why this is written down before it is built

Today, enrollment is manual and covers one person: the operator enrolls their
own verified mobile number, outside of any web interface. That is truthful,
it is what the public pages say, and it is sufficient for a single-recipient
program.

It is not sufficient for anyone else. The moment a second person could receive
a message, the program needs a consent record it can show to Twilio, to a
carrier, or to a regulator — one that proves who agreed, to what wording, and
when. This document specifies that record and the workflow that produces it, so
the workflow can be built correctly rather than improvised under pressure.

Until it is built, the program stays single-recipient.

---

## 2. Scope

- **In scope:** a private, authenticated, operator-only interface for enrolling
  a mobile number with a durable consent record; keyword handling; revocation;
  and the send-time block that enforces revocation.
- **Out of scope:** public enrollment of any kind. This workflow is not a
  public signup form and must never become one without a separate review.
- **Also out of scope:** the Codex-driven reminder data flow. Its architecture
  and retention behaviour are not known yet. It is not part of this design and
  must not be described as operational anywhere.

---

## 3. Requirements

### R1 — Verified operator number

A number cannot be enrolled on the strength of someone typing it in. Before a
number is eligible for enrollment:

- The number is normalised to E.164 and checked for validity.
- A one-time verification code is sent to the number by SMS.
- The code is entered back into the interface, within a short expiry window,
  with a small fixed number of attempts.
- Only on a correct code does the number reach `verified` state and become
  eligible for the consent step.

Rationale: verification proves the person completing the form actually controls
the handset. Without it, the consent record proves nothing.

### R2 — Separate, unchecked consent checkbox

Consent is captured by a checkbox that is:

- **Separate.** It is its own control, not bundled with terms acceptance, not
  bundled with account creation, and not bundled with any other agreement.
- **Unchecked by default.** It is never pre-checked, never checked by script,
  and never inferred from any other action on the page.
- **Explicitly labelled**, with the full disclosure text visible next to it —
  not behind a link, not behind a tooltip, not in a collapsed section.
- **Required.** The submit control stays disabled until the checkbox is checked
  and the number is in `verified` state. The server re-checks both; a request
  that arrives without consent is rejected regardless of what the client sent.

Consent is never a condition of anything else. The program sells nothing, so
there is nothing to condition it on.

### R3 — Disclosure version and timestamp

Every consent record stores enough to reconstruct exactly what the person
agreed to:

| Field | Description |
| --- | --- |
| `phone_e164` | The enrolled number, normalised |
| `consent_granted` | Boolean; `true` only on an explicit check |
| `disclosure_version` | Immutable version identifier of the disclosure text shown |
| `disclosure_text_hash` | Hash of the exact wording rendered on screen |
| `consented_at` | UTC timestamp, ISO 8601, of the submission |
| `consent_method` | How consent was captured, e.g. `web_form_operator_private` |
| `verification_id` | Reference to the completed R1 verification |
| `revoked` | Boolean; see R5 |
| `revoked_at` | UTC timestamp, ISO 8601, or null |
| `revocation_source` | e.g. `sms_stop`, `operator`, `email_request`, or null |

Disclosure text is versioned and append-only. Editing published disclosure
wording means minting a new version; it never rewrites an old one, because old
records must keep pointing at what was actually shown. The hash exists so a
claim about past wording can be checked rather than trusted.

### R4 — Confirmation message

On a successful enrollment, exactly one confirmation SMS is sent, immediately,
to the number that was just verified and consented:

```
Siddarth Thota Personal Alerts: You are now subscribed to personal reminder
alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help,
STOP to cancel.
```

(Sent as a single line. Wording must match `docs/message-templates.md`
verbatim.)

The confirmation is sent once per enrollment, is not retried into a duplicate,
and is not batched with any reminder content.

### R5 — Revocation state

Revocation is a first-class field on the consent record, not the absence of a
record. Deleting a record must never be the way a number is unsubscribed,
because a deleted record cannot stop a future send.

- `STOP` (or `END`, `CANCEL`, `UNSUBSCRIBE`, `QUIT`) sets `revoked = true`,
  stamps `revoked_at`, and sets `revocation_source = sms_stop`.
- An operator action or an emailed request sets the same fields with the
  matching source.
- `START` (or `UNSTOP`, `YES`) creates a **new** consent record for a new
  opt-in. It does not edit the revoked record. History stays intact.
- Revocation records are retained indefinitely, which is exactly what the
  published Privacy Policy says.

### R6 — Outbound blocking after STOP

The block is enforced at the last possible moment, in the send path itself:

1. Immediately before any outbound message is handed to the messaging
   provider, the send path looks up the current consent record for the
   destination number.
2. If no record exists, or `consent_granted` is false, or `revoked` is true,
   the send is **refused**. It is logged as refused with the reason, and it is
   not queued, retried, or rescheduled.
3. Refusal is the default. A lookup failure or a database error also refuses
   the send. The system never falls back to sending.
4. The only messages exempt from this check are the provider-level automatic
   replies to `STOP` and `HELP`, which the provider sends on its own and which
   carriers require.

This check belongs in one place that every send goes through. If a second send
path is ever added, it goes through the same check or it does not ship.

---

## 4. Proposed flow

```
Operator opens the private, authenticated enrollment interface
        │
        ▼
Enters mobile number  ──►  normalise to E.164, validate
        │
        ▼
Verification code sent by SMS  ──►  operator enters code
        │                              │ wrong / expired
        │                              └──►  retry, limited attempts
        ▼
Number reaches `verified` state
        │
        ▼
Disclosure text (version N) rendered in full on screen,
with a separate, unchecked consent checkbox beside it
        │
        ├── checkbox unchecked  ──►  submit stays disabled; nothing is stored
        │
        ▼ checkbox checked, submit pressed
Server re-validates verification + consent, then writes the consent record
(R3 fields, `revoked = false`)
        │
        ▼
Single confirmation SMS sent (R4)
        │
        ▼
Number is enrolled
        │
        ▼
Every later send  ──►  consent check (R6)  ──►  send, or refuse and log
        ▲                                              │
        │                                              │
        └───  STOP received  ──►  revoked = true  ──────┘
```

---

## 5. Non-goals and explicit prohibitions

- **No screenshots.** This document deliberately contains no screenshots or
  mockups presented as evidence. There is no interface to screenshot. Do not
  create an image and present it as a record of an opt-in that did not happen.
- **No claim that this exists.** Nothing on the public site, in the Twilio
  campaign description, or in a carrier response may state or imply that this
  workflow is live.
- **No public enrollment.** Building this workflow does not open the program to
  the public. It stays operator-only and authenticated.
- **No consent by implication.** Not from a reply, not from a prior
  relationship, not from a checkbox that was already checked, not from clicking
  submit.

---

## 6. Definition of done

This design is implemented only when all of the following are true:

1. A number cannot be enrolled without completing SMS verification (R1).
2. The consent checkbox is separate, unchecked by default, and enforced on the
   server (R2).
3. A consent record is written with disclosure version, text hash, and UTC
   timestamp (R3).
4. Exactly one confirmation message is sent, matching the published template
   verbatim (R4).
5. `STOP` sets revocation state rather than deleting anything, and `START`
   creates a new record (R5).
6. A test proves that a send to a revoked number is refused, and that a
   consent-lookup failure also refuses the send (R6).
7. The public disclosures are updated to describe the workflow accurately —
   after it works, not before.

Until every one of these is true, the program remains single-recipient with
manual enrollment, and the public pages continue to say exactly that.
