#!/usr/bin/env bash
#
# Usage:
#   scripts/cost-eval.sh                 # run all 3 strategies, then build comparison report
#   scripts/cost-eval.sh rfp-02-agent-teams # run just one (report only builds if all 3 exist)
#   scripts/cost-eval.sh --report-only   # skip running strategies; just (re)build the
#                                         # comparison report from existing run-01/02/03 outputs
#
# Requires: claude CLI, jq (claude only needed the first time --report-only judges quality; cached afterward), python3
# Must be run from the task07-claude-code-rfp-agent/ directory (relative
# paths in the commands assume it).

set -euo pipefail

PERMISSION_MODE="${PERMISSION_MODE:-bypassPermissions}"

REPORT_ONLY=0
if [[ "${1:-}" == "--report-only" ]]; then
  REPORT_ONLY=1
  shift
  if [[ $# -gt 0 ]]; then
    echo "error: --report-only does not take additional arguments" >&2
    exit 1
  fi
fi

run_dir_for() {
  case "$1" in
    rfp-01-baseline) echo "run-01-baseline" ;;
    rfp-02-agent-teams) echo "run-02-agent-teams" ;;
    rfp-03-dynamic-workflow) echo "run-03-dynamic-workflow" ;;
    *) echo "cost/$1" ;;
  esac
}

REPORT_RUN_DIRS=(run-01-baseline run-02-agent-teams run-03-dynamic-workflow)
COMPARISON_OUT_DIR="outputs/runs/comparison-cost-eval"

check_report_inputs_ready() {
  local dir
  for dir in "${REPORT_RUN_DIRS[@]}"; do
    if [[ ! -f "outputs/runs/${dir}/cost-eval.metrics.json" ]]; then
      echo "missing: outputs/runs/${dir}/cost-eval.metrics.json" >&2
      return 1
    fi
    if ! compgen -G "outputs/runs/${dir}/risk-assessment-*.html" > /dev/null; then
      echo "missing: outputs/runs/${dir}/risk-assessment-*.html" >&2
      return 1
    fi
  done
  return 0
}

generate_comparison_report() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "error: python3 not found on PATH (required for report generation)" >&2
    return 1
  fi
  if [[ ! -f "${COMPARISON_OUT_DIR}/quality.json" ]] && ! command -v claude >/dev/null 2>&1; then
    echo "error: claude CLI not found on PATH (required to judge quality — no cached ${COMPARISON_OUT_DIR}/quality.json found)" >&2
    return 1
  fi
  python3 scripts/judge_quality.py || return 1
  python3 scripts/generate_comparison_report.py "${COMPARISON_OUT_DIR}/report.html"
}

if [[ ! -d .claude/commands ]]; then
  echo "error: run this from task07-claude-code-rfp-agent/ (no .claude/commands here)" >&2
  exit 1
fi

if [[ $REPORT_ONLY -eq 1 ]]; then
  if ! check_report_inputs_ready; then
    echo "error: --report-only requires cost-eval + risk-assessment outputs for all 3 runs (${REPORT_RUN_DIRS[*]})" >&2
    exit 1
  fi
  generate_comparison_report
  exit 0
fi

COMMANDS=(
  rfp-01-baseline
  rfp-02-agent-teams
  rfp-03-dynamic-workflow
)

if [[ $# -gt 0 ]]; then
  COMMANDS=("$@")
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "error: claude CLI not found on PATH" >&2
  exit 1
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "error: jq not found on PATH" >&2
  exit 1
fi

echo "Permission mode: $PERMISSION_MODE (override with PERMISSION_MODE=... env var)"
echo

for cmd in "${COMMANDS[@]}"; do
  if [[ ! -f ".claude/commands/${cmd}.md" ]]; then
    echo "error: no such command .claude/commands/${cmd}.md" >&2
    exit 1
  fi

  out_dir="outputs/runs/$(run_dir_for "$cmd")"
  mkdir -p "$out_dir"

  raw_file="${out_dir}/cost-eval.json"
  metrics_file="${out_dir}/cost-eval.metrics.json"

  echo "=== Running /${cmd} ==="
  claude -p "/${cmd}" \
    --output-format json \
    --permission-mode "$PERMISSION_MODE" \
    | jq '.' > "$raw_file"

  jq '{
    command: $cmd,
    cost_usd: ([.modelUsage[]] | map(.costUSD) | add // 0),
    orchestrator_cost_usd: .total_cost_usd,
    num_turns,
    duration_ms,
    tokens: (
      [.modelUsage[]] as $models
      | {
          input_tokens: ($models | map(.inputTokens) | add // 0),
          output_tokens: ($models | map(.outputTokens) | add // 0),
          cache_creation_input_tokens: ($models | map(.cacheCreationInputTokens) | add // 0),
          cache_read_input_tokens: ($models | map(.cacheReadInputTokens) | add // 0)
        }
    ),
    per_model: .modelUsage
  }' --arg cmd "$cmd" "$raw_file" > "$metrics_file"

  cost=$(jq -r '.cost_usd' "$metrics_file")
  orch_cost=$(jq -r '.orchestrator_cost_usd' "$metrics_file")
  echo "  cost_usd (all agents): \$${cost}  (orchestrator-only: \$${orch_cost})  ->  ${metrics_file}"
  echo
done

echo "=== Summary ==="
printf "%-24s %10s %12s %12s %14s %14s\n" \
  "command" "cost_usd" "input_tok" "output_tok" "cache_creat" "cache_read"
for cmd in "${COMMANDS[@]}"; do
  m="outputs/runs/$(run_dir_for "$cmd")/cost-eval.metrics.json"
  [[ -f "$m" ]] || continue
  jq -r '[.command, (.cost_usd|tostring), (.tokens.input_tokens|tostring), (.tokens.output_tokens|tostring), (.tokens.cache_creation_input_tokens|tostring), (.tokens.cache_read_input_tokens|tostring)] | @tsv' "$m" \
    | awk -F'\t' '{printf "%-24s %10s %12s %12s %14s %14s\n", $1, $2, $3, $4, $5, $6}'
done

echo
if check_report_inputs_ready; then
  echo "=== Comparison report ==="
  generate_comparison_report
else
  echo "note: skipping comparison report — not all 3 strategy runs have outputs yet" >&2
fi
