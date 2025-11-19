#!/bin/bash
# command-executor.sh - Executes shell commands and returns output to agent
# Hook: beforeShellExecution
# Purpose: Intercept commands, execute safely, and provide output back to agent

input=$(cat)
command=$(echo "$input" | jq -r '.command // empty')
cwd=$(echo "$input" | jq -r '.cwd // empty')
workspace_root=$(echo "$input" | jq -r '.workspace_roots[0] // empty')
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Log the command execution
echo "[$timestamp] EXECUTING: $command (CWD: $cwd, WORKSPACE: $workspace_root)" >> ~/.cursor/command-execution.log

# Determine working directory
# Priority: 1) explicit cwd, 2) workspace_root, 3) HOME
if [[ -n "$cwd" ]] && [[ "$cwd" != "~" ]]; then
    # Use provided cwd (unless it's just ~)
    target_dir="$cwd"
elif [[ -n "$workspace_root" ]]; then
    # Use workspace root as default (this is where Cursor would execute)
    target_dir="$workspace_root"
else
    # Fallback to HOME
    target_dir="$HOME"
fi

# Handle tilde expansion if needed
if [[ "$target_dir" == "~" ]] || [[ "$target_dir" == "~/"* ]]; then
    target_dir="${target_dir/#\~/$HOME}"
fi

cd "$target_dir" 2>/dev/null || cd "$HOME"
echo "[$timestamp] Working directory: $(pwd)" >> ~/.cursor/command-execution.log

# Execute command without timeout and capture output
output=$(bash -c "$command" 2>&1)
exit_code=$?

# Log result for debugging
if [[ $exit_code -eq 0 ]]; then
    log_status="SUCCESS"
else
    log_status="ERROR"
fi
echo "[$timestamp] $log_status: exit_code=$exit_code" >> ~/.cursor/command-execution.log

# Return ONLY the raw output to agent using jq to properly escape JSON
# This ensures special characters in output don't break the JSON
# Note: permission="deny" prevents Cursor from executing the command again (we already did it)
jq -n \
  --arg output "$output" \
  '{
    permission: "deny",
    agent_message: $output
  }'

exit 0

