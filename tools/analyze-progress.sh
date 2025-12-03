#!/bin/bash
# Quick analysis of agent progress

PROGRESS_FILE="${1:-workspaces/SHARED_PROGRESS.md}"

if [ ! -f "$PROGRESS_FILE" ]; then
    echo "Error: $PROGRESS_FILE not found"
    exit 1
fi

echo "=== Agent Progress Analysis ==="
echo "File: $PROGRESS_FILE"
echo ""

# Count total entries
echo "📊 Total Entries:"
TOTAL=$(grep -c "^## [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" "$PROGRESS_FILE" 2>/dev/null || echo "0")
echo "  $TOTAL"
echo ""

# Count by status
echo "📈 By Status:"
COMPLETE=$(grep -c "✅ Complete" "$PROGRESS_FILE" 2>/dev/null || echo "0")
IN_PROGRESS=$(grep -c "🔄 In Progress\|🔄 In progress" "$PROGRESS_FILE" 2>/dev/null || echo "0")
BLOCKED=$(grep -c "⚠️ Blocked" "$PROGRESS_FILE" 2>/dev/null || echo "0")
FAILED=$(grep -c "❌ Failed" "$PROGRESS_FILE" 2>/dev/null || echo "0")
PAUSED=$(grep -c "🚧 Paused" "$PROGRESS_FILE" 2>/dev/null || echo "0")
PLANNED=$(grep -c "📋 Planned" "$PROGRESS_FILE" 2>/dev/null || echo "0")

echo "  ✅ Complete: $COMPLETE"
echo "  🔄 In Progress: $IN_PROGRESS"
echo "  ⚠️  Blocked: $BLOCKED"
echo "  ❌ Failed: $FAILED"
echo "  🚧 Paused: $PAUSED"
echo "  📋 Planned: $PLANNED"
echo ""

# Count by agent (top 10)
echo "🤖 Most Active Agents (Top 10):"
grep -oP '(?<=@)[\w-]+(?=:)' "$PROGRESS_FILE" 2>/dev/null | sort | uniq -c | sort -rn | head -10 | while read count agent; do
    printf "  %-40s %3d tasks\n" "$agent" "$count"
done
echo ""

# Recent activity
echo "🕐 Recent Activity (Last 10 entries):"
grep "^## [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" "$PROGRESS_FILE" 2>/dev/null | tail -10 | while read line; do
    # Extract date, agent, and task
    if [[ $line =~ ^##\ ([0-9-]+)\ ([0-9:]+)\ -\ @([a-z-]+):\ (.+)$ ]]; then
        date="${BASH_REMATCH[1]}"
        time="${BASH_REMATCH[2]}"
        agent="${BASH_REMATCH[3]}"
        task="${BASH_REMATCH[4]}"
        printf "  %s %s - @%-30s %s\n" "$date" "$time" "$agent:" "$task"
    fi
done
echo ""

# Task IDs if present
TASK_IDS=$(grep -c "Task ID" "$PROGRESS_FILE" 2>/dev/null || echo "0")
if [ "$TASK_IDS" -gt 0 ]; then
    echo "📋 Task Tracking:"
    echo "  $TASK_IDS entries with Task IDs"
    echo ""
fi

# Duration statistics if present
DURATIONS=$(grep "Duration" "$PROGRESS_FILE" 2>/dev/null | wc -l)
if [ "$DURATIONS" -gt 0 ]; then
    echo "⏱️  Duration Tracking:"
    echo "  $DURATIONS entries with duration info"
    echo ""
fi

# Deliverables count
DELIVERABLES=$(grep -c "^[ \t]*-.*\`.*\`" "$PROGRESS_FILE" 2>/dev/null || echo "0")
if [ "$DELIVERABLES" -gt 0 ]; then
    echo "📦 Deliverables:"
    echo "  $DELIVERABLES files documented"
    echo ""
fi

# Check for consultation pattern usage
CONSULTATIONS=$(grep -c "\[CONSULT\]" "$PROGRESS_FILE" 2>/dev/null || echo "0")
if [ "$CONSULTATIONS" -gt 0 ]; then
    echo "💬 Consultations:"
    echo "  $CONSULTATIONS consultation requests"
    echo ""
fi

echo "==================================="
echo ""
echo "💡 Tip: Use 'python3 tools/parse-progress.py' for detailed analysis"
echo "        or 'tools/validate-progress.sh' to validate format"
