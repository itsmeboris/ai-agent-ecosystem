#!/bin/bash
# Validate SHARED_PROGRESS.md format

PROGRESS_FILE="${1:-workspaces/SHARED_PROGRESS.md}"
ERRORS=0
WARNINGS=0

if [ ! -f "$PROGRESS_FILE" ]; then
    echo "❌ Error: $PROGRESS_FILE not found"
    exit 1
fi

echo "🔍 Validating $PROGRESS_FILE..."
echo ""

# Check for required sections
echo "Checking project structure..."
if ! grep -q "^# Project:" "$PROGRESS_FILE" 2>/dev/null; then
    echo "  ⚠️  Warning: Missing 'Project:' header (recommended)"
    ((WARNINGS++))
else
    echo "  ✅ Project header found"
fi

# Check for valid agent entry format
echo ""
echo "Checking agent entries..."
ENTRY_COUNT=0
MALFORMED_COUNT=0

while IFS= read -r line; do
    if [[ $line =~ ^##\ [0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
        ((ENTRY_COUNT++))

        # Check if agent name is present
        if ! [[ $line =~ @[a-z][a-z0-9-]+ ]]; then
            echo "  ❌ Entry missing agent identifier: ${line:0:80}..."
            ((ERRORS++))
            ((MALFORMED_COUNT++))
        fi

        # Check if task title is present
        if ! [[ $line =~ :[[:space:]]+.+ ]]; then
            echo "  ⚠️  Entry missing task title: ${line:0:80}..."
            ((WARNINGS++))
        fi

        # Check date format
        if ! [[ $line =~ ^##\ [0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]) ]]; then
            echo "  ❌ Invalid date format: ${line:0:80}..."
            ((ERRORS++))
        fi
    fi
done < "$PROGRESS_FILE"

echo "  Found $ENTRY_COUNT entries"
if [ $MALFORMED_COUNT -eq 0 ]; then
    echo "  ✅ All entries have valid format"
else
    echo "  ❌ $MALFORMED_COUNT malformed entries"
fi

# Check for status markers
echo ""
echo "Checking status markers..."
STATUS_COUNT=$(grep -c "\*\*Status\*\*:" "$PROGRESS_FILE" 2>/dev/null || echo "0")
if [ $STATUS_COUNT -eq 0 ]; then
    echo "  ⚠️  No status markers found (recommended to add)"
    ((WARNINGS++))
else
    echo "  ✅ $STATUS_COUNT entries with status markers"

    # Check for valid status emojis
    VALID_STATUS=$(grep "\*\*Status\*\*:" "$PROGRESS_FILE" | grep -c "🔄\|✅\|⚠️\|❌\|🚧\|📋" || echo "0")
    if [ $VALID_STATUS -lt $STATUS_COUNT ]; then
        INVALID=$((STATUS_COUNT - VALID_STATUS))
        echo "  ⚠️  $INVALID entries with non-standard status markers"
        ((WARNINGS++))
    fi
fi

# Check for orphaned deliverable files
echo ""
echo "Checking deliverables..."
DELIVERABLE_COUNT=0
MISSING_COUNT=0

while IFS= read -r filepath; do
    ((DELIVERABLE_COUNT++))
    # Only check files in workspaces/ directory
    if [[ $filepath == workspaces/* ]] && [[ ! -f $filepath ]]; then
        echo "  ⚠️  Missing deliverable: $filepath"
        ((WARNINGS++))
        ((MISSING_COUNT++))
    fi
done < <(grep -oP '(?<=`)[^`]+(?=`)' "$PROGRESS_FILE" 2>/dev/null | grep "^workspaces/")

if [ $DELIVERABLE_COUNT -eq 0 ]; then
    echo "  ℹ️  No deliverables documented yet"
else
    echo "  Found $DELIVERABLE_COUNT documented deliverables"
    if [ $MISSING_COUNT -eq 0 ]; then
        echo "  ✅ All deliverable files exist"
    else
        echo "  ⚠️  $MISSING_COUNT deliverable files not found (may be in progress)"
    fi
fi

# Check for duplicate task IDs
echo ""
echo "Checking task IDs..."
TASK_IDS=$(grep -oP '(?<=\*\*Task ID\*\*:)\s*\S+' "$PROGRESS_FILE" 2>/dev/null | tr -d ' ')
TASK_ID_COUNT=$(echo "$TASK_IDS" | grep -v '^$' | wc -l)

if [ $TASK_ID_COUNT -eq 0 ]; then
    echo "  ℹ️  No task IDs in use (optional feature)"
else
    DUPLICATE_IDS=$(echo "$TASK_IDS" | sort | uniq -d)
    if [ -n "$DUPLICATE_IDS" ]; then
        echo "  ❌ Duplicate task IDs found:"
        echo "$DUPLICATE_IDS" | while read id; do
            echo "    - $id"
        done
        ((ERRORS++))
    else
        echo "  ✅ $TASK_ID_COUNT unique task IDs, no duplicates"
    fi
fi

# Check for proper workspace protocol adherence
echo ""
echo "Checking workspace protocols..."

# Check for forbidden separate PROGRESS.md files in agent workspaces
if find workspaces/ -name "PROGRESS.md" -type f 2>/dev/null | grep -q .; then
    echo "  ❌ Found separate PROGRESS.md files (should use SHARED_PROGRESS.md only):"
    find workspaces/ -name "PROGRESS.md" -type f 2>/dev/null | while read file; do
        echo "    - $file"
    done
    ((ERRORS++))
else
    echo "  ✅ No separate PROGRESS.md files (correct protocol)"
fi

# Check for proper agent identifiers in entries
MISSING_IDENTIFIER=0
grep "^## [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}" "$PROGRESS_FILE" | while read line; do
    # Extract the full entry to check for agent identifier pattern
    if ! [[ $line =~ @[a-z][a-z0-9-]+: ]]; then
        ((MISSING_IDENTIFIER++))
    fi
done

# Check for YAML frontmatter validity (if used)
echo ""
echo "Checking YAML frontmatter (if present)..."
YAML_ENTRIES=$(grep -c "^---$" "$PROGRESS_FILE" 2>/dev/null || echo "0")
if [ $YAML_ENTRIES -gt 0 ]; then
    YAML_PAIRS=$((YAML_ENTRIES / 2))
    echo "  Found $YAML_PAIRS entries with YAML frontmatter"

    # Try to validate YAML syntax if Python is available
    if command -v python3 &> /dev/null; then
        python3 -c "
import re
import yaml
import sys

with open('$PROGRESS_FILE', 'r') as f:
    content = f.read()

# Find all YAML sections
yaml_sections = re.findall(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
errors = 0

for i, yaml_content in enumerate(yaml_sections, 1):
    try:
        yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        print(f'  ❌ YAML syntax error in entry {i}: {e}')
        errors += 1
        sys.exit(1)

if errors == 0:
    print('  ✅ All YAML frontmatter is valid')
" || ((ERRORS++))
    else
        echo "  ℹ️  Python not available, skipping YAML syntax validation"
    fi
else
    echo "  ℹ️  No YAML frontmatter in use (using markdown format)"
fi

# Summary
echo ""
echo "==================================="
echo "VALIDATION SUMMARY"
echo "==================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo "✅ Validation passed with no issues!"
    echo ""
    echo "Your SHARED_PROGRESS.md follows all protocols correctly."
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo "✅ Validation passed"
    echo "⚠️  Found $WARNINGS warnings (non-critical)"
    echo ""
    echo "Your file is valid but could be enhanced by addressing the warnings above."
    exit 0
else
    echo "❌ Validation failed"
    echo "   Errors: $ERRORS"
    echo "   Warnings: $WARNINGS"
    echo ""
    echo "Please fix the errors above before proceeding."
    exit 1
fi
