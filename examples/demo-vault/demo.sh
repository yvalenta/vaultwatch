#!/usr/bin/env bash
# Run the demo vault's two auditors, and break it on purpose to watch them go red.
#
#   ./demo.sh              run both audits on the vault as it is (green)
#   ./demo.sh --drift      the WORLD moves, the docs stay put   -> world audit red
#   ./demo.sh --contradict the DOC contradicts itself           -> coherence audit red
#   ./demo.sh --orphan     a note nobody links to               -> coherence audit red
#   ./demo.sh --proof      all of the above, with the exit codes checked
#
# Every mutation is applied to a throwaway COPY. The vault itself is never edited.
set -u
here=$(cd "$(dirname "$0")" && pwd)

# run both audits on $1; sets $c and $w to their exit codes (no pipes: a pipe would
# report the exit code of the last stage, not of the audit)
audit() {
  python3 -I "$1/audit/coherence.py" "$1"; c=$?
  echo
  python3 -I "$1/audit/world.py" "$1"; w=$?
  echo
}

with_copy() {  # with_copy MUTATION: run the audits on a mutated copy of the vault
  local tmp; tmp=$(mktemp -d)
  cp -R "$here"/. "$tmp"/
  case "$1" in
    drift)       # the world raises the price; nobody touches the docs
      sed -i 's/"price_usd": "[0-9.]*"/"price_usd": "3.00"/' "$tmp/world/served.json" ;;
    contradict)  # a hand-copied figure outside its assertion site
      fig=$(sed -n 's/.*\([0-9][0-9]*\.[0-9][0-9]\) USD.*/\1/p' "$here/state/price.md" | head -1)
      printf '\nThe price is %s USD.\n' "$fig" >> "$tmp/HANDOFF.md" ;;
    orphan)      # a new note that no index links to
      printf '# Stray note\n' > "$tmp/laws/stray-note.md" ;;
  esac
  audit "$tmp"
  rm -rf "$tmp"
}

fingerprint() { (cd "$here" && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -c1-12); }

case "${1:-}" in
  "")          audit "$here"; echo "exit codes: coherence=$c world=$w"; [ "$c$w" = "00" ] ;;
  --drift)     with_copy drift; echo "exit codes: coherence=$c world=$w" ;;
  --contradict) with_copy contradict; echo "exit codes: coherence=$c world=$w" ;;
  --orphan)    with_copy orphan; echo "exit codes: coherence=$c world=$w" ;;
  --proof)
    before=$(fingerprint)
    fail=0
    rows=""
    for case_ in base drift contradict orphan; do
      if [ "$case_" = base ]; then audit "$here"; want="00"; else with_copy "$case_"
        case "$case_" in drift) want="01" ;; *) want="10" ;; esac
      fi
      got="$c$w"
      [ "$got" = "$want" ] && v=ok || { v=WRONG; fail=1; }
      rows="$rows$(printf '%-12s coherence=%s world=%s  expected %s/%s  %s' "$case_" "$c" "$w" "${want:0:1}" "${want:1:1}" "$v")\n"
    done
    after=$(fingerprint)
    [ "$before" = "$after" ] && t=untouched || { t=CHANGED; fail=1; }
    echo "================ negative proof ================"
    printf "%b" "$rows"
    echo "vault fingerprint before/after: $before / $after ($t)"
    [ $fail = 0 ] && echo "proof: every red fired where it should, and the vault is untouched." \
                  || echo "proof: FAILED"
    exit $fail ;;
  *) sed -n '2,10p' "$0"; exit 64 ;;
esac
