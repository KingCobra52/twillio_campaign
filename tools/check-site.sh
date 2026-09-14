#!/usr/bin/env bash
# Run every automated check for the compliance site.
# Usage: ./tools/check-site.sh      (from the repository root)
set -uo pipefail

cd "$(dirname "$0")/.."
status=0
fail() { echo "  FAIL: $1"; status=1; }

echo "== 1. HTML well-formedness =="
if command -v tidy >/dev/null 2>&1; then
  while IFS= read -r f; do
    out=$(tidy -qe --show-warnings no "$f" 2>&1) || true
    if [ -n "$out" ]; then fail "$f"; echo "$out"; fi
  done < <(find site -name '*.html')
  echo "  checked $(find site -name '*.html' | wc -l) files"
else
  echo "  SKIPPED (install with: apt-get install -y tidy)"
fi

echo "== 2. no absolute-path links outside 404.html =="
hits=$(grep -rn -E '(href|src)="/' site --include='*.html' | grep -v '^site/404.html' || true)
[ -z "$hits" ] && echo "  none" || { fail "absolute paths found"; echo "$hits"; }

echo "== 3. no external resource loads =="
hits=$(grep -rnoE '(href|src)="(https?:)?//[^"]*"' site --include='*.html' --include='*.css' --include='*.js' \
       | grep -v 'https://www.twilio.com/' || true)
[ -z "$hits" ] && echo "  none beyond the twilio.com informational link" || { fail "external resource"; echo "$hits"; }

echo "== 4. no credentials, Twilio identifiers, or phone numbers in site/ =="
hits=$(grep -rInE 'AC[0-9a-fA-F]{32}|SK[0-9a-fA-F]{32}|MG[0-9a-fA-F]{32}' site/ || true)
[ -z "$hits" ] || { fail "Twilio identifier"; echo "$hits"; }
hits=$(grep -rInE '\+?1?[[:space:]().-]*[0-9]{3}[[:space:]().-]*[0-9]{3}[[:space:]().-]*[0-9]{4}' site/ || true)
[ -z "$hits" ] || { fail "phone-number-shaped string"; echo "$hits"; }
hits=$(grep -rInE '(api|secret|auth)[_-]?(key|token|secret)[[:space:]]*[:=]' site/ || true)
[ -z "$hits" ] || { fail "credential-shaped assignment"; echo "$hits"; }
echo "  clean"

echo "== 5. no placeholders left behind =="
hits=$(grep -rInE 'TODO|FIXME|TBD|XXX|Lorem ipsum|\[insert|\{\{|example\.com|PAGES_URL' site/ || true)
[ -z "$hits" ] && echo "  none" || { fail "placeholder"; echo "$hits"; }

echo "== 6. internal links and anchors =="
python3 tools/check-links.py || status=1

echo "== 7. cross-document consistency =="
python3 tools/check-consistency.py >/tmp/consistency.log 2>&1 \
  && echo "  all consistency checks passed" \
  || { fail "consistency"; cat /tmp/consistency.log; }

echo
[ "$status" -eq 0 ] && echo "ALL CHECKS PASSED" || echo "CHECKS FAILED"
exit "$status"
