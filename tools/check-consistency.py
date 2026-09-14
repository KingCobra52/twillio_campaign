"""Cross-document consistency check for the compliance site."""
import re, html, sys

def text_of(path):
    t = open(path, encoding='utf-8').read()
    if path.endswith('.html'):
        t = re.sub(r'<(script|style)\b.*?</\1>', '', t, flags=re.S)
        t = re.sub(r'<[^>]+>', ' ', t)
    else:
        t = re.sub(r'^\s*>\s?', '', t, flags=re.M)   # markdown blockquote markers
        t = re.sub(r'^\s*[|`#-]+\s*', ' ', t, flags=re.M)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

D = {n: text_of(p) for n, p in {
    'home': 'site/index.html',
    'sms': 'site/sms/index.html',
    'privacy': 'site/privacy/index.html',
    'terms': 'site/terms/index.html',
    'templates': 'docs/message-templates.md',
    'campaign': 'docs/twilio-campaign.md',
}.items()}

MESSAGES = {
 'confirmation': "Siddarth Thota Personal Alerts: You are now subscribed to personal reminder alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help, STOP to cancel.",
 'sample A': "Siddarth Thota Personal Alerts: Reminder - your dentist appointment is tomorrow at 9:00 AM. Reply STOP to cancel, HELP for help. Msg&data rates may apply.",
 'sample B': "Siddarth Thota Personal Alerts: Reminder - the electric bill is due this Friday. Reply STOP to cancel, HELP for help. Msg&data rates may apply.",
 'HELP reply': "Siddarth Thota Personal Alerts: Personal reminder messages for one enrolled recipient. Support: hellotheking52@gmail.com. Msg frequency varies. Msg&data rates may apply. Reply STOP to cancel.",
 'STOP reply': "Siddarth Thota Personal Alerts: You have been unsubscribed and will receive no further messages. Reply START to resubscribe. Support: hellotheking52@gmail.com",
 'START reply': "Siddarth Thota Personal Alerts: You are resubscribed to personal reminder alerts. Msg frequency varies. Msg&data rates may apply. Reply HELP for help, STOP to cancel.",
}

NOSALE = "Mobile numbers and SMS consent data are not sold, rented, or shared with third parties or affiliates for marketing or promotional purposes."

CHECKS = [
    ('message templates identical in /sms/, templates, campaign',
     [(m, d) for m in MESSAGES for d in ('sms', 'templates', 'campaign')],
     lambda m, d: MESSAGES[m] in D[d]),
    ('required no-sale sentence, verbatim',
     [(NOSALE, d) for d in ('home', 'sms', 'privacy', 'campaign')],
     lambda p, d: p in D[d]),
    ('carrier-charge language',
     [("Message and data rates may apply", d) for d in ('home', 'sms', 'terms')],
     lambda p, d: p in D[d]),
    ('variable-frequency language',
     [("aries", d) for d in ('home', 'sms', 'terms', 'campaign')],
     lambda p, d: ('frequency varies' in D[d].lower() or 'Varies' in D[d])),
    ('support address',
     [("hellotheking52@gmail.com", d) for d in ('home', 'sms', 'privacy', 'terms', 'campaign')],
     lambda p, d: p in D[d]),
    ('program name',
     [("Siddarth Thota Personal Alerts", d) for d in D],
     lambda p, d: p in D[d]),
    ('Pennsylvania governing law / location',
     [("Pennsylvania", d) for d in ('home', 'sms', 'privacy', 'terms', 'campaign')],
     lambda p, d: p in D[d]),
    ('keywords STOP / START / HELP',
     [(k, d) for k in ('STOP', 'START', 'HELP') for d in ('sms', 'terms', 'templates', 'campaign')],
     lambda k, d: k in D[d]),
    ('providers named in privacy policy',
     [(p, 'privacy') for p in ('Twilio', 'GitHub Pages')],
     lambda p, d: p in D[d]),
    ('single-recipient / no public enrollment stated',
     [(p, d) for p in ('no public enrollment', 'no signup form') for d in ('sms',)],
     lambda p, d: p.lower() in D[d].lower()),
]

FORBIDDEN_PUBLIC = [
    'sign up now', 'subscribe here', 'enter your number', 'join our list',
    'codex integration is live', 'powered by codex', 'lorem ipsum',
]

fails = []
for title, cases, test in CHECKS:
    print(f"\n{title}")
    for arg, doc in cases:
        ok = test(arg, doc)
        if not ok:
            fails.append(f"{title}: {arg[:50]!r} missing from {doc}")
        print(f"  {doc:12s} {str(arg)[:46]:48s} {'OK' if ok else 'FAIL'}")

print("\nforbidden phrases on public pages")
for d in ('home', 'sms', 'privacy', 'terms'):
    hits = [w for w in FORBIDDEN_PUBLIC if w in D[d].lower()]
    if hits:
        fails.append(f"forbidden phrase in {d}: {hits}")
    print(f"  {d:12s} {'clean' if not hits else hits}")

print("\n" + ("ALL CONSISTENCY CHECKS PASSED" if not fails else "FAILURES:"))
for f in fails:
    print("  " + f)
sys.exit(1 if fails else 0)
