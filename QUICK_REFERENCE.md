# Quick Reference Guide - Enhanced Agent Ecosystem

*Fast reference for all new features and tools*

---

## 🚀 Quick Commands

### Generate Agent Summaries (Do this first!)
```bash
python3 tools/generate_summaries.py --agents-dir agents --output-dir agents/summaries
```

### Find the Right Agent
```bash
# Find agents for your task
python3 tools/capability_discovery.py --find "your requirement"

# Recommend a team
python3 tools/capability_discovery.py --recommend "project description"

# Show capability report
python3 tools/capability_discovery.py --report
```

### Use Lazy Loading
```bash
# List all agents (lightweight)
python3 tools/lazy_loader.py --list

# Get agent summary
python3 tools/lazy_loader.py --summary agent-name

# Activate agent (load full definition)
python3 tools/lazy_loader.py --activate agent-name

# Check token usage
python3 tools/lazy_loader.py --status
```

### Analyze Progress
```bash
# Parse and show summary
python3 tools/parse-progress.py workspaces/SHARED_PROGRESS.md

# Filter by agent
python3 tools/parse-progress.py --agent backend-architect

# Export to JSON
python3 tools/parse-progress.py --json report.json

# Quick shell analysis
./tools/analyze-progress.sh workspaces/SHARED_PROGRESS.md

# Validate format
./tools/validate-progress.sh workspaces/SHARED_PROGRESS.md
```

---

## 📋 Progress Format (Hybrid - Recommended)

```markdown
---
task_id: TASK-001
agent: agent-name
status: complete
duration_minutes: 135
metrics: {loc: 487, coverage: 92}
---

## 2025-11-30 14:30 - @agent-name: Task Title

**Status**: ✅ Complete | **Duration**: 2h 15m

### Context
What you did and why

### Deliverables
- `path/to/file.ext` - Description

### Key Decisions
- Decision: Rationale

### Handoff to @next-agent
What they need to know
```

**Status Emojis**:
- 🔄 In Progress
- ✅ Complete
- ⚠️ Blocked
- ❌ Failed
- 🚧 Paused
- 📋 Planned

---

## 🛡️ Error Handling Quick Reference

### Type 1: Recoverable (Auto-Fix)
```markdown
## Error Entry
**Status**: 🔄 In Progress (Recovered from error)

**Recoverable Error**:
- Issue: Missing dependency
- Auto-Fix: Installed package
- Impact: 2 min delay
- Continuing: Task proceeding
```

### Type 2: Escalation (Need Help)
```markdown
## Error Entry
**Status**: ⚠️ Blocked - Escalation Required

**Escalation Error**:
- Issue: Security concern detected
- Analysis: [what you found]
- Recommendation: [CONSULT] @specialist-agent
- Impact: Task paused
```

### Type 3: Critical (User Decision)
```markdown
## Error Entry
**Status**: ❌ Failed - User Intervention Required

**Critical Error**:
- Severity: CRITICAL
- Issue: Data loss risk
- Options:
  1. Option A: pros/cons
  2. Option B: pros/cons
- Recommendation: Option A
- User Decision Required: [what to decide]
```

### Python Error Handling

```python
from tools.error_handling import retry_with_backoff, try_alternatives, CheckpointManager

# Retry with backoff
@retry_with_backoff(max_attempts=3, base_delay=1)
def unstable_operation():
    return api.call()

# Try alternatives
name, data = try_alternatives(
    ("Primary", lambda: fetch_from_api()),
    ("Cache", lambda: fetch_from_cache())
)

# Checkpoints
mgr = CheckpointManager("TASK-001")
state = mgr.restore_checkpoint()  # Resume if exists
# ... do work ...
mgr.save_checkpoint(state, "Progress update")
mgr.clear_checkpoint()  # On success
```

---

## 🎯 Agent Capability Schema

```yaml
---
name: agent-name
version: 1.0.0
description: Primary, secondary, tertiary capabilities

capabilities:
  # Core capabilities
  file_operations: [read, write, edit]
  command_execution: [npm, docker, git]
  external_access: [web_search, api_calls]

  # Specializations (snake_case)
  specializations:
    - api_design
    - database_design
    - security_implementation

  # Technologies (PascalCase)
  technologies:
    - Node.js
    - PostgreSQL
    - Docker

  # Operational
  consultation_available: true
  max_parallel_tasks: 3
  avg_task_duration_hours: 2.0

  # Relationships
  requires_agents: [dependency-agent]
  works_well_with: [complementary-agent]
  provides_for: [consumer-agent]
---
```

---

## 📊 Token Efficiency Tips

### DO ✅
```python
# Planning phase - use summaries
loader = LazyAgentLoader()
for agent in candidates:
    summary = loader.load_summary(agent)  # 250 tokens
    # Make decision

# Execution phase - load full definition
loader.activate_agent(selected_agent)  # 1000 tokens
```

### DON'T ❌
```python
# Don't load all agents
for agent in all_48_agents:
    full_def = load_full_definition(agent)  # 48,000 tokens!
```

**Token Budget**:
- Directory: ~100 tokens (always loaded)
- Summaries: ~250 tokens each (load 3-5)
- Full definitions: ~1000 tokens each (load 1-2 active)
- **Target total: <5,000 tokens**

---

## 🔍 Capability Discovery Examples

### Find Agents
```bash
# By requirement
python3 tools/capability_discovery.py --find "REST API authentication"

# By specialization
python3 tools/capability_discovery.py --specialization api_design

# By technology
python3 tools/capability_discovery.py --technology Node.js

# By category
python3 tools/capability_discovery.py --category core-technical

# Agent details
python3 tools/capability_discovery.py --details backend-architect
```

### Python API
```python
from tools.capability_discovery import CapabilityDiscovery

discovery = CapabilityDiscovery()
discovery.scan_all_agents()

# Find agents
matches = discovery.find_agent("build GraphQL API", top_n=5)
for agent_name, score in matches:
    print(f"{agent_name}: {score:.2f}")

# Recommend team
team = discovery.recommend_team("Build auth system", max_agents=3)
for member in team:
    print(f"{member['agent']}: {member['match_score']}")

# Export index
discovery.export_index("capabilities.json")
```

---

## 📁 Directory Structure

```
ai-agent-ecosystem/
├── agents/
│   ├── coordination/           # Coordination agents + protocols
│   │   ├── strategic-task-planner.mdc
│   │   ├── WORKSPACE_PROTOCOLS.md
│   │   ├── STRUCTURED_OUTPUT_FORMATS.md ⭐ NEW
│   │   ├── ERROR_HANDLING_PROTOCOL.md   ⭐ NEW
│   │   ├── CAPABILITY_DISCOVERY.md      ⭐ NEW
│   │   ├── TOKEN_EFFICIENCY.md          ⭐ NEW
│   │   └── STREAMLINED_AGENT_TEMPLATE.md (updated)
│   ├── core-technical/         # 13 core agents
│   ├── data-intelligence/      # 7 data agents
│   ├── user-experience/        # 7 UX agents
│   ├── security-operations/    # 7 security agents
│   ├── business-marketing/     # 8 business agents
│   ├── specialized-domains/    # 2 domain agents
│   └── summaries/              # ⭐ NEW: Agent summaries
├── tools/
│   ├── parse-progress.py       # ⭐ NEW: Parse progress
│   ├── analyze-progress.sh     # ⭐ NEW: Quick analysis
│   ├── validate-progress.sh    # ⭐ NEW: Validate format
│   ├── error_handling.py       # ⭐ NEW: Error utilities
│   ├── capability_discovery.py # ⭐ NEW: Find agents
│   ├── generate_summaries.py   # ⭐ NEW: Create summaries
│   └── lazy_loader.py          # ⭐ NEW: Lazy loading
├── workspaces/
│   ├── SHARED_PROGRESS.md      # Central progress file
│   ├── .checkpoints/           # ⭐ NEW: Recovery checkpoints
│   └── .logs/                  # ⭐ NEW: Error logs
├── IMPROVEMENTS_SUMMARY.md     # ⭐ NEW: Complete summary
├── QUICK_REFERENCE.md          # ⭐ NEW: This file
└── README.md
```

---

## 🎓 Learning Path

### 1. Start Simple
```bash
# Generate summaries
python3 tools/generate_summaries.py

# Try finding agents
python3 tools/capability_discovery.py --find "what you need"

# Check capability report
python3 tools/capability_discovery.py --report
```

### 2. Add Structure
- Start using task IDs in progress entries
- Add metrics to your updates
- Use status emojis consistently

### 3. Add Capabilities
- Update 2-3 agents with capability definitions
- Test capability discovery
- Refine specializations and technologies

### 4. Optimize Tokens
- Use lazy loading for agent selection
- Load summaries for planning
- Activate only when executing

### 5. Handle Errors Systematically
- Classify errors (Type 1/2/3)
- Use structured error reports
- Implement recovery workflows

---

## 📖 Documentation Map

**For Users**:
- `QUICK_REFERENCE.md` - This file (quick commands)
- `IMPROVEMENTS_SUMMARY.md` - Complete overview
- `README.md` - Original ecosystem docs

**For Coordination**:
- `WORKSPACE_PROTOCOLS.md` - Progress tracking
- `STRUCTURED_OUTPUT_FORMATS.md` - Format specs
- `ERROR_HANDLING_PROTOCOL.md` - Error handling
- `CAPABILITY_DISCOVERY.md` - Agent selection
- `TOKEN_EFFICIENCY.md` - Lazy loading

**For Agents**:
- `STREAMLINED_AGENT_TEMPLATE.md` - Agent template
- Individual agent `.mdc` files

---

## 💡 Pro Tips

1. **Always generate summaries first** before using lazy loading
2. **Use hybrid format** for SHARED_PROGRESS.md (best of both worlds)
3. **Add capabilities gradually** to agents (backward compatible)
4. **Type 1 errors should auto-recover** - log and continue
5. **Use [CONSULT] for Type 2** - get expert input
6. **Stop immediately for Type 3** - user decision required
7. **Keep token usage under 5,000** for optimal performance
8. **Export progress to JSON** for dashboards and analytics
9. **Validate progress format** before committing
10. **Use capability discovery** instead of manual agent selection

---

## 🔢 Key Numbers

- **48 agents** in ecosystem
- **7 new tools** added
- **4 major protocols** created
- **93% token reduction** achieved
- **3-tier loading** system
- **3 error types** classification
- **250 tokens** per summary
- **~3,100 tokens** typical usage (vs 48,000)

---

## ⚡ Most Common Commands

```bash
# Daily workflow
python3 tools/capability_discovery.py --find "requirement"
python3 tools/lazy_loader.py --activate agent-name
python3 tools/parse-progress.py workspaces/SHARED_PROGRESS.md

# Weekly maintenance
python3 tools/generate_summaries.py --force
python3 tools/capability_discovery.py --report
./tools/validate-progress.sh workspaces/SHARED_PROGRESS.md

# Export and analyze
python3 tools/parse-progress.py --json weekly-report.json
python3 tools/capability_discovery.py --export capabilities.json
```

---

*For complete details, see `IMPROVEMENTS_SUMMARY.md` and individual protocol documents.*
