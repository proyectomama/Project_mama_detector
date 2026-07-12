#!/usr/bin/env bash
# Prueba el hook commit-msg con casos válidos e inválidos.
set -u
HOOK="$(dirname "$0")/commit-msg"
tmp="$(mktemp)"
fail=0

check() { # $1=mensaje  $2=esperado(ok|bad)
  printf '%s\n' "$1" > "$tmp"
  if bash "$HOOK" "$tmp" >/dev/null 2>&1; then res=ok; else res=bad; fi
  if [ "$res" != "$2" ]; then echo "FALLO: '$1' esperaba $2 y dio $res"; fail=1; fi
}

check "feat: agrega servicio de fusion" ok
check "fix(#12): corrige umbral BI-RADS" ok
check "docs: actualiza runbook" ok
check "Merge branch 'main'" ok
check "arreglos varios" bad
check "feat agrega algo" bad
check "wip" bad

rm -f "$tmp"
if [ "$fail" -eq 0 ]; then echo "TODOS LOS CASOS PASAN"; else exit 1; fi
