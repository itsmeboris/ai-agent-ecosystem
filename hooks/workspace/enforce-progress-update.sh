#!/bin/bash
# enforce-progress-update.sh - Reminds agents to update SHARED_PROGRESS.md after completing tasks
# Hook: afterAgentResponse
# Purpose: Ensure workspace protocols are followed

input=$(cat)
text=$(echo "$input" | jq -r '.text // empty')
workspace_roots=$(echo "$input" | jq -r '.workspace_roots[0] // empty')

# Check if this is a substantive response (more than 100 characters)
# This filters out short conversational messages
text_length=${#text}

# Check for agent identifiers (various formats)
# Formats: "agent-name:", "🎯:", "leverage-ai-agents:", etc.
has_agent_id=false
if echo "$text" | grep -qE '^[a-z-]+:' || echo "$text" | grep -qE '^🎯:'; then
    has_agent_id=true
fi

# Only remind if this is a substantive response (likely agent work)
if [[ $text_length -gt 100 ]] || [[ "$has_agent_id" == true ]]; then
    shared_progress="${workspace_roots}/workspaces/SHARED_PROGRESS.md"

    # Build reminder message
    reminder_msg="📝 Reminder: Please ensure you've updated ${shared_progress} with:
- Task status (🔄 In Progress / ✅ Complete)
- Key decisions made
- Deliverables created
- Next steps or handoff notes

Per WORKSPACE_PROTOCOLS.md, all agents should document their work in SHARED_PROGRESS.md."

    # Send a reminder message back to the agent context using jq for proper JSON encoding
    jq -n --arg msg "$reminder_msg" '{agent_message: $msg}'
else
    # Short message or no agent work detected - skip reminder
    echo "{}"
fi

exit 0

