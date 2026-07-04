#!/usr/bin/env bash
#
# Runs the 4 rfp-0X-* commands headlessly via `claude -p` and captures total
# cost + token usage for each — including every subagent/Task-tool call the
# orchestrator spins up.
#
# NOTE: the top-level `total_cost_usd` field in Claude Code's JSON output only
# covers the orchestrator's own session — it does NOT include cost incurred by
# spawned subagents. `modelUsage` is the field that rolls up token usage (and
# per-model `costUSD`) across the orchestrator + every subagent, so that's what
# this script sums to get the true total cost of a run. For subagent-spawning
# strategies (rfp-02/03/04) that total can be several times `total_cost_usd`.
#
# Cost/metrics JSON files are saved alongside each command's own outputs
# (the .docx/.html each command writes under outputs/run-N-*/), so everything
# for a given run lives in one folder.
#
# Usage:
#   scripts/cost-eval.sh                 # run all 3 strategies
#   scripts/cost-eval.sh rfp-02-agent-teams # run just one
#
# Requires: claude CLI, jq
# Must be run from the task07-claude-code-rfp-agent/ directory (relative
# paths in the commands assume it).

set -euo pipefail

PERMISSION_MODE="${PERMISSION_MODE:-bypassPermissions}"

run_dir_for() {
  case "$1" in
    rfp-01-baseline) echo "run-1-baseline" ;;
    rfp-02-agent-teams) echo "run-2-agent-teams" ;;
    rfp-02-dynamic-workflow) echo "run-3-dynamic-workflow" ;;
    *) echo "cost/$1" ;;
  esac
}

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
if [[ ! -d .claude/commands ]]; then
  echo "error: run this from task07-claude-code-rfp-agent/ (no .claude/commands here)" >&2
  exit 1
fi

echo "Permission mode: $PERMISSION_MODE (override with PERMISSION_MODE=... env var)"
echo

for cmd in "${COMMANDS[@]}"; do
  if [[ ! -f ".claude/commands/${cmd}.md" ]]; then
    echo "error: no such command .claude/commands/${cmd}.md" >&2
    exit 1
  fi

  out_dir="outputs/$(run_dir_for "$cmd")"
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
  m="outputs/$(run_dir_for "$cmd")/cost-eval.metrics.json"
  [[ -f "$m" ]] || continue
  jq -r '[.command, (.cost_usd|tostring), (.tokens.input_tokens|tostring), (.tokens.output_tokens|tostring), (.tokens.cache_creation_input_tokens|tostring), (.tokens.cache_read_input_tokens|tostring)] | @tsv' "$m" \
    | awk -F'\t' '{printf "%-24s %10s %12s %12s %14s %14s\n", $1, $2, $3, $4, $5, $6}'
done
