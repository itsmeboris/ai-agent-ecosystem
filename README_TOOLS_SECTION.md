## 🛠️ Tools & Automation

The ecosystem includes powerful tools for intelligent agent discovery, token efficiency, and progress tracking. All tools are automatically installed and can be used by both agents and users.

### **🔍 Available Tools**

#### **1. Capability Discovery** (`tools/capability_discovery.py`)
**Purpose:** Find the right agents for your requirements automatically

**Agent Usage:**
```bash
# Find agents by requirement
tools/capability_discovery.py --find "REST API design"
# Returns: api-design-specialist (0.95), backend-architect (0.87)

# Recommend optimal team for project
tools/capability_discovery.py --recommend "e-commerce platform"
# Returns: 5-7 agent team with dependencies

# Generate capability report
tools/capability_discovery.py --report
```

**How Agents Use It:**
Agents can discover specialists by executing this tool via Bash:
```markdown
I'll find the right specialist for database work:
<execute via Bash tool>
./tools/capability_discovery.py --find "database optimization"
</execute>
```

---

#### **2. Lazy Loader** (`tools/lazy_loader.py`)
**Purpose:** Token-efficient agent loading (93% token reduction)

**Agent Usage:**
```bash
# List all available agents (lightweight directory)
tools/lazy_loader.py --list
# Returns: All 48 agents, ~100 tokens

# Load agent summary only (~250 tokens vs ~1000)
tools/lazy_loader.py --summary backend-architect

# Activate full agent definition when needed
tools/lazy_loader.py --activate backend-architect

# Check what's currently loaded
tools/lazy_loader.py --status
```

**Token Efficiency:**
```
Traditional: Load all 48 agents = 48,000 tokens
With Lazy Loading:
  - Directory: ~100 tokens
  - Summaries (5 agents): ~1,250 tokens
  - Full (2 active): ~2,000 tokens
  → Total: ~3,350 tokens (93% savings!)
```

**How Agents Use It:**
Coordination agents should load summaries first, then activate full definitions only when executing:
```markdown
First, I'll check available backend specialists:
<execute via Bash tool>
./tools/lazy_loader.py --list | grep backend
</execute>

Now I'll load the backend architect's summary:
<execute via Bash tool>
./tools/lazy_loader.py --summary backend-architect
</execute>

Since we need full expertise, activating complete definition:
<execute via Bash tool>
./tools/lazy_loader.py --activate backend-architect
</execute>
```

---

#### **3. Progress Tracking** (`tools/parse-progress.py`)
**Purpose:** Parse and analyze workspace progress files

**Agent Usage:**
```bash
# Parse progress markdown
tools/parse-progress.py workspaces/SHARED_PROGRESS.md

# Export to JSON for programmatic access
tools/parse-progress.py workspaces/SHARED_PROGRESS.md --json report.json

# Quick shell analysis
tools/analyze-progress.sh workspaces/SHARED_PROGRESS.md

# Validate format compliance
tools/validate-progress.sh workspaces/SHARED_PROGRESS.md
```

---

#### **4. Summary Generation** (`tools/generate_summaries.py`)
**Purpose:** Regenerate agent summaries after modifications

```bash
# Regenerate all summaries
tools/generate_summaries.py

# Regenerate for specific category
tools/generate_summaries.py --category core-technical
```

---

#### **5. Error Handling** (`tools/error_handling.py`)
**Purpose:** Reusable error handling utilities for consistent recovery patterns

---

### **📚 How Agents Know About Tools**

**1. Documentation Files:**
All installations include these protocol documents:
- `TOKEN_EFFICIENCY.md` - Explains lazy loading and how to use `lazy_loader.py`
- `CAPABILITY_DISCOVERY.md` - Explains agent selection and how to use `capability_discovery.py`
- `QUICK_REFERENCE.md` - Quick command reference for all tools

**2. Agent Instructions:**
Coordination agents (like `strategic-task-planner`) have built-in knowledge:
```yaml
# In agent frontmatter:
capabilities:
  command_execution: [bash, python]

# In agent prompt:
"When you need to find specialists, use: ./tools/capability_discovery.py --find <requirement>"
"For token efficiency, load summaries first: ./tools/lazy_loader.py --summary <agent>"
```

**3. Runtime Discovery:**
Agents can list available tools:
```bash
ls tools/
# Shows: capability_discovery.py, lazy_loader.py, parse-progress.py, etc.
```

---

### **🎯 Tool Usage Patterns**

**Pattern 1: Agent Discovery**
```
strategic-task-planner:
  → Uses capability_discovery.py to find specialists
  → Loads summaries of candidates via lazy_loader.py
  → Selects best match
  → Activates full definition when delegating
```

**Pattern 2: Token Optimization**
```
leverage-ai-agents:
  → Loads directory (all 48 agents, ~100 tokens)
  → Loads summaries for relevant agents (~250 tokens each)
  → Activates only agents that will execute (~1000 tokens each)
  → Result: 93% token savings
```

**Pattern 3: Progress Coordination**
```
Any agent:
  → Checks SHARED_PROGRESS.md via parse-progress.py
  → Identifies completed vs pending tasks
  → Updates progress after completing work
  → Validates format with validate-progress.sh
```

---

### **Installation**

Tools are automatically installed with agents:

```bash
# Standard installation (includes tools)
python3 install-agents.py .cursor/rules --all

# For Claude Code
python3 install-agents.py <your-dir> --all

# For Claude Desktop
python3 install-agents.py .claude/agents --claude --all
```

**Verification:**
```bash
# Check tools are installed
ls <installation-dir>/tools/

# Test capability discovery
<installation-dir>/tools/capability_discovery.py --find "test"

# Test lazy loader
<installation-dir>/tools/lazy_loader.py --list
```

---

### **🔗 See Also**

- **TOKEN_EFFICIENCY.md** - Detailed lazy loading architecture
- **CAPABILITY_DISCOVERY.md** - Agent selection system details
- **QUICK_REFERENCE.md** - Quick command reference
