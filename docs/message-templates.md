# SMS message templates

**Internal document.** Not published to GitHub Pages.

These are the exact texts the program sends. The two sample messages, the
confirmation, and the HELP, STOP, and START replies also appear verbatim on the
public `/sms/` page. If a template changes here, change it there in the same
commit, and update the Twilio campaign record.

Rules every outbound template follows:

1. It opens with the program name: `Siddarth Thota Personal Alerts:`
2. It carries an opt-out instruction: `Reply STOP to cancel`
3. Opt-in, HELP, and sample messages state `Msg&data rates may apply`
4. It contains no private phone number, no link shortener, and no attachment

Keywords are matched case-insensitively. Each template below is a single line
when sent; line breaks in this file are for readability only.

---

## 1. Opt-in confirmation

Sent once, immediately after a number is enrolled.

```
Siddarth Thota Personal Alerts: You are now subscribed to personal reminder alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help, STOP to cancel.
```

---

## 2. Sample message A — appointment reminder

```
Siddarth Thota Personal Alerts: Reminder - your dentist appointment is tomorrow at 9:00 AM. Reply STOP to cancel, HELP for help. Msg&data rates may apply.
```

## 3. Sample message B — bill reminder

```
Siddarth Thota Personal Alerts: Reminder - the electric bill is due this Friday. Reply STOP to cancel, HELP for help. Msg&data rates may apply.
```

Both samples are representative, not transcripts. The reminder text between the
program name and the opt-out instruction varies with whatever reminder the
recipient set.

---

## 4. HELP reply

Triggered by `HELP` or `INFO`.

```
Siddarth Thota Personal Alerts: Personal reminder messages for one enrolled recipient. Support: hellotheking52@gmail.com. Msg frequency varies. Msg&data rates may apply. Reply STOP to cancel.
```

---

## 5. STOP reply

Triggered by `STOP`, `END`, `CANCEL`, `UNSUBSCRIBE`, or `QUIT`. This is the last
message the number receives until it resubscribes.

```
Siddarth Thota Personal Alerts: You have been unsubscribed and will receive no further messages. Reply START to resubscribe. Support: hellotheking52@gmail.com
```

---

## 6. START reply

Triggered by `START`, `UNSTOP`, or `YES`, after a prior opt-out.

```
Siddarth Thota Personal Alerts: You are resubscribed to personal reminder alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help, STOP to cancel.
```

---

## Notes on keyword handling

Twilio applies default `STOP` and `HELP` handling to US numbers at the carrier
level, and in some configurations replies with its own default text rather than
the wording above. Before relying on these templates, confirm in the Twilio
Console which advanced opt-out configuration the sending number uses, and set
the custom keyword responses to match this file. Whichever path is used, the
behaviour must match what the public pages promise: `STOP` stops all messages,
`START` resumes them, `HELP` returns support information.

The send path must also enforce revocation itself rather than relying only on
carrier-level blocking — see `consent-workflow-design.md`, requirement R6.
