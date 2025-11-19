#!/bin/bash
# auto-continue.sh - Automatically continue with pending tasks
# Hook: stop
# Purpose: Enable unattended multi-task execution

input=$(cat)
status=$(echo "$input" | jq -r '.status // empty')
loop_count=$(echo "$input" | jq -r '.loop_count // 0')
workspace_roots=$(echo "$input" | jq -r '.workspace_roots[0] // empty')
timestamp=$(date '+%Y-%m-%d %H:%M:%S')

# Configuration
MAX_LOOPS=4  # Cursor enforces max 5, we use 4 to leave room for final wrap-up
LOG_FILE=~/.cursor/auto-continue.log

# Log the stop event
echo "[$timestamp] STOP EVENT: status=$status, loop_count=$loop_count" >> "$LOG_FILE"

# Only auto-continue on successful completion
if [[ "$status" != "completed" ]]; then
    echo "[$timestamp] Not auto-continuing: status is '$status' (not completed)" >> "$LOG_FILE"
    echo '{"followup_message":""}'
    exit 0
fi

# Check if we've hit the loop limit
if [[ $loop_count -ge $MAX_LOOPS ]]; then
    echo "[$timestamp] Loop limit reached ($loop_count >= $MAX_LOOPS) - stopping" >> "$LOG_FILE"
    echo '{"followup_message":""}'
    exit 0
fi

# Check for pending tasks in SHARED_PROGRESS.md
shared_progress="${workspace_roots}/workspaces/SHARED_PROGRESS.md"

if [[ -f "$shared_progress" ]]; then
    # Look for pending/in-progress tasks (marked with 🔄 emoji or "In Progress" or "Pending")
    pending_tasks=$(grep -c "Status.*🔄\|Status.*In Progress\|Status.*Pending\|Status.*TODO" "$shared_progress" 2>/dev/null || echo "0")

    if [[ $pending_tasks -gt 0 ]]; then
        echo "[$timestamp] Found $pending_tasks pending task(s) - auto-continuing (loop $((loop_count + 1))/$MAX_LOOPS)" >> "$LOG_FILE"

        # Return followup message to trigger next iteration using jq for proper JSON encoding
        followup_msg="🔄 Auto-continuing execution: Detected $pending_tasks pending task(s) in SHARED_PROGRESS.md. Please continue with the next phase of the execution plan. (Auto-loop $((loop_count + 1))/$MAX_LOOPS)"
        jq -n --arg msg "$followup_msg" '{followup_message: $msg}'
        exit 0
    fi

    # Also check for explicit "Next Steps" that aren't empty/complete
    has_next_steps=$(grep -A 2 "Next Steps\|## Next\|**Next" "$shared_progress" 2>/dev/null | grep -v "Complete\|None\|N/A" | wc -l)

    if [[ $has_next_steps -gt 1 ]]; then
        echo "[$timestamp] Found next steps in plan - auto-continuing (loop $((loop_count + 1))/$MAX_LOOPS)" >> "$LOG_FILE"

        # Return followup message using jq for proper JSON encoding
        followup_msg="➡️ Auto-continuing: Next steps detected in execution plan. Please proceed with the next phase. (Auto-loop $((loop_count + 1))/$MAX_LOOPS)"
        jq -n --arg msg "$followup_msg" '{followup_message: $msg}'
        exit 0
    fi

    echo "[$timestamp] No pending tasks found - all tasks complete or SHARED_PROGRESS.md doesn't indicate pending work" >> "$LOG_FILE"
else
    echo "[$timestamp] SHARED_PROGRESS.md not found at: $shared_progress" >> "$LOG_FILE"
fi

# No pending tasks - let the loop end naturally
echo "[$timestamp] Ending auto-continue loop - no pending tasks" >> "$LOG_FILE"
echo '{"followup_message":""}'
exit 0

