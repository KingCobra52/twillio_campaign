# Twilio campaign registration — prepared copy

**Internal document.** Not published to GitHub Pages.

**Status: PREPARED, NOT SUBMITTED.** See section 7 before submitting anything.

This file holds the exact text intended for the Twilio A2P campaign
registration form, plus the URLs the form asks for. Everything here must match
the public pages word for word in substance. If a public page changes, this
file changes in the same commit.

Do not paste a Twilio Account SID, Auth Token, API Key, Messaging Service SID,
or any phone number into this file. It is a copy deck, not a credential store.

---

## 1. Brand and campaign identity

| Form field | Value |
| --- | --- |
| Registered identity | Siddarth Thota (sole proprietor / individual) |
| Country | United States |
| State | Pennsylvania |
| Campaign / program name | Siddarth Thota Personal Alerts |
| Use case | Account notification / personal reminder alerts |
| Marketing content | No |
| Embedded links in messages | No |
| Embedded phone numbers in messages | No |
| Age-gated content | No |
| Direct lending or loan arrangement | No |
| Affiliate marketing | No |
| Number pooling | No |
| Support contact | hellotheking52@gmail.com |

---

## 2. Campaign description

> Siddarth Thota Personal Alerts sends personal reminder text messages to a
> single recipient: Siddarth Thota, who is also the operator of the program.
> Messages are short reminders the recipient has set for themselves, such as
> appointment reminders, bill and deadline reminders, and recurring task
> reminders.
>
> This is a private, single-user program. It is not open to public enrollment,
> it has no signup form, and it sends no marketing, advertising, or promotional
> content. It sends no messages on behalf of any other person, business, or
> organization. Mobile numbers and SMS consent data are not sold, rented, or
> shared with third parties or affiliates for marketing or promotional
> purposes.
>
> Message frequency varies, because messages are sent only when a reminder the
> recipient has set becomes due. Message and data rates may apply. The
> recipient can reply STOP at any time to stop all messages, START to
> resubscribe, and HELP for support information. Support is available at
> hellotheking52@gmail.com.

---

## 3. Message flow (call-to-action / opt-in description)

> Opt-in is manual and covers one recipient, who is the operator of the
> program. The operator enrolls their own mobile number directly, outside of
> any website, before any message is sent. That manual enrollment is the
> program's consent record.
>
> There is no web form, no keyword opt-in campaign, no point-of-sale opt-in,
> and no third-party list. The program's public website,
> https://kingcobra52.github.io/twillio_campaign/, publishes the program
> disclosures only; it does not collect mobile numbers and contains no signup
> form of any kind. No person other than the operator is enrolled, and no
> message is sent to any number that has not been manually enrolled by the
> operator.
>
> The disclosures shown at enrollment, and published at
> https://kingcobra52.github.io/twillio_campaign/sms/, state the program name,
> the operator, the purpose of the messages, that message frequency varies,
> that message and data rates may apply, the support contact, and the STOP,
> START, and HELP keywords, and they link to the Privacy Policy and the Terms
> of Service.
>
> On enrollment the recipient receives a single confirmation message:
> "Siddarth Thota Personal Alerts: You are now subscribed to personal reminder
> alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help,
> STOP to cancel."

---

## 4. Sample messages

Both must be entered exactly as written. They match `message-templates.md` and
the public `/sms/` page.

**Sample 1**

```
Siddarth Thota Personal Alerts: Reminder - your dentist appointment is tomorrow at 9:00 AM. Reply STOP to cancel, HELP for help. Msg&data rates may apply.
```

**Sample 2**

```
Siddarth Thota Personal Alerts: Reminder - the electric bill is due this Friday. Reply STOP to cancel, HELP for help. Msg&data rates may apply.
```

---

## 5. Keyword responses

| Field | Keywords | Response |
| --- | --- | --- |
| Opt-in confirmation | (sent on enrollment) | `Siddarth Thota Personal Alerts: You are now subscribed to personal reminder alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help, STOP to cancel.` |
| HELP | `HELP`, `INFO` | `Siddarth Thota Personal Alerts: Personal reminder messages for one enrolled recipient. Support: hellotheking52@gmail.com. Msg frequency varies. Msg&data rates may apply. Reply STOP to cancel.` |
| STOP | `STOP`, `END`, `CANCEL`, `UNSUBSCRIBE`, `QUIT` | `Siddarth Thota Personal Alerts: You have been unsubscribed and will receive no further messages. Reply START to resubscribe. Support: hellotheking52@gmail.com` |
| START | `START`, `UNSTOP`, `YES` | `Siddarth Thota Personal Alerts: You are resubscribed to personal reminder alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help, STOP to cancel.` |

---

## 6. URLs required by the form

GitHub Pages publishes this repository at:

```
https://kingcobra52.github.io/twillio_campaign/
```

No custom domain is configured.

**Deployment status.** Pages is enabled with its source set to GitHub Actions,
and the workflow has deployed successfully — `actions/deploy-pages` reported
`Reported success!` and resolved the environment URL to the address above.

**The pages have not been loaded in a browser.** The environment these
documents were written in cannot reach `github.io`, so every URL below is
confirmed as *deployed*, not as *fetched*. Open each one signed out, in a
private window, on a phone and on a desktop, and confirm it returns the right
page before entering it on the Twilio form.

| Form field | URL |
| --- | --- |
| Privacy Policy URL | `https://kingcobra52.github.io/twillio_campaign/privacy/` |
| Terms of Service URL | `https://kingcobra52.github.io/twillio_campaign/terms/` |
| SMS program disclosure | `https://kingcobra52.github.io/twillio_campaign/sms/` |
| Website | `https://kingcobra52.github.io/twillio_campaign/` |

Open each one in a browser before entering it on the form. A URL that has been
deployed but never loaded is not yet a URL you can attest to.

---

## 7. Submission gate — read before submitting

**Do not submit this campaign yet.**

The campaign asserts that consent was obtained. That assertion has to be
backed by something a reviewer could actually examine. Right now:

- The consent workflow described in `consent-workflow-design.md` **is not
  built**. Nothing in this repository implements verification, a consent
  checkbox, a versioned disclosure record, or a send-time revocation block.
- The only opt-in that exists is the operator manually enrolling their own
  number.

Submit only when **at least one** of these is true, and record which one:

1. **The real consent workflow exists.** Every item in section 6 of
   `consent-workflow-design.md` ("Definition of done") is implemented and
   tested, and the public disclosures have been updated to describe it
   accurately.
2. **There is truthful, reviewable evidence of the manual opt-in.** A
   contemporaneous record of the operator's own enrollment — what disclosure
   wording was shown, when consent was recorded, and that the number was
   verified — that the operator is willing to hand to a reviewer as-is.

Neither of these may be manufactured after the fact. Do not create a
screenshot, a log entry, or a timestamp to satisfy this gate. A fabricated
consent record is worse than a rejected campaign.

### Pre-submission checklist

- [ ] Live site deployed and all four routes return 200 signed out
- [ ] Every URL in sections 3 and 6 opened in a browser and confirmed correct
- [ ] Privacy Policy URL loaded and confirmed public
- [ ] Terms of Service URL loaded and confirmed public
- [ ] `/sms/` disclosure loaded and confirmed public
- [ ] Campaign description, message flow, and sample messages read side by side
      with the public pages, with no contradictions
- [ ] Sample messages match `message-templates.md` exactly
- [ ] Keyword responses configured in the Twilio Console to match section 5
- [ ] Section 7 gate satisfied, and which condition was met is recorded here
- [ ] No credential, SID, or phone number pasted into this repository
