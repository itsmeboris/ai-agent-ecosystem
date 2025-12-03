# AI Agent Ecosystem - Installation Guide

*Complete guide for installing on Cursor, Claude Code, and Claude Desktop*

---

## 🎯 Overview

The AI Agent Ecosystem can be installed on multiple platforms:
- **Cursor IDE** - Full featured installation with hooks and automation
- **Claude Code CLI** - Command-line agent system with Task tool integration
- **Claude Desktop** - Desktop app agent installation

Each platform has different capabilities and installation procedures.

---

## 📊 Platform Comparison

| Feature | Cursor | Claude Code | Claude Desktop |
|---------|--------|-------------|----------------|
| **Agent Format** | `.mdc` files | `.mdc` files | `.md` files |
| **Hooks Support** | ✅ Yes | ❌ No | ❌ No |
| **Custom Commands** | ✅ Yes | ❌ No | ❌ No |
| **Documentation** | ✅ Full | ✅ Full | ⚠️ Limited |
| **Token Efficiency** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Capability Discovery** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Error Handling** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Automation** | ✅ Auto-continue | ⚠️ Manual | ⚠️ Manual |

---

## 🚀 Installation Methods

### Method 1: Cursor IDE (Recommended - Full Features)

**Best for**: Maximum automation and workflow integration

#### Prerequisites
- Cursor IDE installed
- Python 3.8+ installed
- Git (for updates)

#### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-agent-ecosystem.git
cd ai-agent-ecosystem

# 2. Install all agents with full features
python3 install-agents.py ~/.cursor/rules --all

# This installs:
# ✅ All 48 agents
# ✅ 13 protocol documents
# ✅ Custom Cursor commands
# ✅ Automation hooks
# ✅ Agent summaries (token efficiency)
```

#### Selective Installation

```bash
# Install specific categories
python3 install-agents.py ~/.cursor/rules --category coordination core-technical

# Install specific agents
python3 install-agents.py ~/.cursor/rules --agents strategic-task-planner backend-architect

# Install without hooks (if you have custom hooks)
python3 install-agents.py ~/.cursor/rules --all --skip-hooks

# Install without custom commands
python3 install-agents.py ~/.cursor/rules --all --skip-commands
```

#### Verification

```bash
# Check installed agents
ls ~/.cursor/rules/*.mdc | wc -l  # Should show number of agents

# Check documentation
ls ~/.cursor/rules/*.md

# Check hooks
cat ~/.cursor/hooks.json

# Test in Cursor
# Type: @strategic-task-planner: Hello
```

---

### Method 2: Claude Code CLI (Command-Line Power)

**Best for**: Terminal-based workflows, programmatic agent usage

#### Prerequisites
- Claude Code CLI installed
- Python 3.8+ installed
- Git (for updates)

#### Installation Steps

**Option A: Direct Integration (Recommended)**

The agent ecosystem can work alongside Claude Code's built-in agents. Install agents to a custom location and use them programmatically:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-agent-ecosystem.git
cd ai-agent-ecosystem

# 2. Install to a custom location
mkdir -p ~/.claude-agents
python3 install-agents.py ~/.claude-agents --all --skip-hooks --skip-commands

# 3. Generate summaries for token efficiency
python3 tools/generate_summaries.py

# 4. Use capability discovery
python3 tools/capability_discovery.py --find "your requirement"

# 5. Use lazy loading
python3 tools/lazy_loader.py --activate backend-architect
```

**Option B: Integration via Task Tool**

Create a custom agent loader that makes your agents available as Claude Code subagent types:

```bash
# 1. Install agents
cd ai-agent-ecosystem
python3 install-agents.py ~/.claude-agents --all --skip-hooks --skip-commands

# 2. Create bridge script
cat > ~/.claude-agents/agent-bridge.py << 'EOF'
#!/usr/bin/env python3
"""Bridge between custom agents and Claude Code"""

import sys
import os
sys.path.insert(0, os.path.expanduser('~/.claude-agents'))

from tools.lazy_loader import LazyAgentLoader
from tools.capability_discovery import CapabilityDiscovery

# Initialize systems
loader = LazyAgentLoader(summaries_dir='agents/summaries')
discovery = CapabilityDiscovery(agents_dir='agents')

def find_agent(requirement):
    """Find best agent for requirement"""
    matches = discovery.find_agent(requirement, top_n=1)
    if matches:
        agent_name, score = matches[0]
        return loader.load_summary(agent_name)
    return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        requirement = ' '.join(sys.argv[1:])
        agent = find_agent(requirement)
        if agent:
            print(f"Recommended: {agent['name']}")
            print(f"Description: {agent['description']}")
EOF

chmod +x ~/.claude-agents/agent-bridge.py
```

#### Usage in Claude Code

```bash
# Find the right agent
~/.claude-agents/agent-bridge.py "build REST API"

# Use tools directly
cd ~/.claude-agents
python3 tools/capability_discovery.py --recommend "your project"
python3 tools/lazy_loader.py --status
python3 tools/parse-progress.py workspaces/SHARED_PROGRESS.md
```

#### Benefits for Claude Code Users

- **Token Efficiency**: 93% reduction using lazy loading
- **Smart Selection**: Capability discovery for finding right agents
- **Structured Progress**: Parse and analyze progress programmatically
- **Error Handling**: Systematic error handling utilities
- **Parallel Execution**: Use multiple agents in same conversation

---

### Method 3: Claude Desktop (Desktop App)

**Best for**: Claude Desktop app users wanting agent assistance

#### Prerequisites
- Claude Desktop app installed
- Python 3.8+ installed
- Git (for updates)

#### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-agent-ecosystem.git
cd ai-agent-ecosystem

# 2. Install for Claude Desktop (converts format)
python3 install-agents.py ~/.claude/agents --claude --all

# This converts:
# ✅ .mdc → .md format
# ✅ Adds model: sonnet to frontmatter
# ✅ Removes Cursor-specific fields
# ✅ Generates summaries for token efficiency
```

#### Verification

```bash
# Check installed agents
ls ~/.claude/agents/*.md | wc -l

# Test in Claude Desktop
# In chat: "@strategic-task-planner: Hello"
```

**Note**: Claude Desktop has limited documentation support. Core protocols are still installed but may not be directly accessible within the app.

---

## 🎨 Post-Installation Setup

### 1. Generate Agent Summaries (If Not Auto-Generated)

```bash
cd ai-agent-ecosystem
python3 tools/generate_summaries.py --agents-dir agents --output-dir agents/summaries
```

### 2. Test Capability Discovery

```bash
# Run capability report
python3 tools/capability_discovery.py --report

# Find agents for your use case
python3 tools/capability_discovery.py --find "your requirement"

# Get recommendations
python3 tools/capability_discovery.py --recommend "your project description"
```

### 3. Verify Token Efficiency

```bash
# Check summary generation
ls agents/summaries/*.yaml | wc -l  # Should match agent count

# Test lazy loading
python3 tools/lazy_loader.py --list
python3 tools/lazy_loader.py --status
```

### 4. Configure Hooks (Cursor Only)

```bash
# Verify hooks installed
cat ~/.cursor/hooks.json

# Should show:
# - afterAgentResponse → enforce-progress-update.sh
# - beforeShellExecution → command-executor.sh
# - stop → auto-continue.sh

# Test hooks
# In Cursor, run any shell command and check:
tail -f ~/.cursor/command-execution.log
```

### 5. Test Error Handling

```python
# Test error handling utilities
cd ai-agent-ecosystem
python3 tools/error_handling.py

# Should show examples of:
# - Retry with backoff
# - Try alternatives
# - Checkpoint recovery
# - Error reporting
```

---

## 🛠️ Tools Reference

### Core Tools (All Platforms)

#### 1. generate_summaries.py
```bash
# Generate agent summaries for token efficiency
python3 tools/generate_summaries.py

# Options:
--agents-dir agents         # Source directory
--output-dir agents/summaries  # Output directory
--force                      # Overwrite existing
--verbose                    # Detailed output
```

#### 2. capability_discovery.py
```bash
# Find agents by requirement
python3 tools/capability_discovery.py --find "REST API"

# Recommend team
python3 tools/capability_discovery.py --recommend "e-commerce platform"

# Show report
python3 tools/capability_discovery.py --report

# Export index
python3 tools/capability_discovery.py --export capabilities.json
```

#### 3. lazy_loader.py
```bash
# List all agents
python3 tools/lazy_loader.py --list

# Load agent summary
python3 tools/lazy_loader.py --summary backend-architect

# Activate agent
python3 tools/lazy_loader.py --activate backend-architect

# Check status and token usage
python3 tools/lazy_loader.py --status
```

#### 4. parse-progress.py
```bash
# Parse progress file
python3 tools/parse-progress.py workspaces/SHARED_PROGRESS.md

# Filter by agent
python3 tools/parse-progress.py --agent backend-architect

# Export to JSON
python3 tools/parse-progress.py --json report.json

# Export to CSV
python3 tools/parse-progress.py --csv report.csv
```

#### 5. error_handling.py
```bash
# Run examples and tests
python3 tools/error_handling.py

# Use in your code:
from tools.error_handling import retry_with_backoff, CheckpointManager
```

### Shell Tools (Cursor/Terminal)

#### 6. analyze-progress.sh
```bash
# Quick progress analysis
./tools/analyze-progress.sh workspaces/SHARED_PROGRESS.md

# Shows:
# - Total entries
# - Status breakdown
# - Most active agents
# - Recent activity
```

#### 7. validate-progress.sh
```bash
# Validate progress format
./tools/validate-progress.sh workspaces/SHARED_PROGRESS.md

# Checks:
# - Format compliance
# - Required sections
# - Deliverable files
# - No protocol violations
```

---

## 📚 Available Documentation

After installation, you'll have access to:

### Core Protocols
1. **WORKSPACE_PROTOCOLS.md** - How agents manage workspaces
2. **STRUCTURED_OUTPUT_FORMATS.md** - Progress tracking formats
3. **ERROR_HANDLING_PROTOCOL.md** - Systematic error handling
4. **CAPABILITY_DISCOVERY.md** - Agent selection system
5. **TOKEN_EFFICIENCY.md** - Lazy loading and summaries

### Coordination Guides
6. **AGENT_HIERARCHY.md** - Agent priority and execution order
7. **AGENT_DIRECTORY.md** - Complete agent catalog
8. **TEAM_COLLABORATION_CULTURE.md** - Communication guidelines
9. **agent-coordination-guide.md** - Coordination methodologies

### Reference Docs
10. **QUICK_REFERENCE.md** - Fast command reference
11. **IMPROVEMENTS_SUMMARY.md** - Feature overview
12. **STREAMLINED_AGENT_TEMPLATE.md** - Create new agents

### Best Practices
13. **agent-best-practices.md** - Agent development standards

---

## 🔄 Updating Your Installation

### Pull Latest Changes

```bash
cd ai-agent-ecosystem
git pull origin main
```

### Reinstall Agents

```bash
# Cursor
python3 install-agents.py ~/.cursor/rules --all

# Claude Code
python3 install-agents.py ~/.claude-agents --all --skip-hooks --skip-commands

# Claude Desktop
python3 install-agents.py ~/.claude/agents --claude --all
```

### Regenerate Summaries

```bash
python3 tools/generate_summaries.py --force
```

---

## 🐛 Troubleshooting

### Problem: "No agents found in the repository"

**Solution:**
```bash
# Check you're in the right directory
ls agents/coordination/*.mdc

# If empty, you're in the wrong directory
cd /path/to/ai-agent-ecosystem
python3 install-agents.py [target] --all
```

### Problem: "Permission denied" when running hooks

**Solution:**
```bash
# Make hooks executable
chmod +x ~/.cursor/hooks/**/*.sh
```

### Problem: Agent summaries not generated

**Solution:**
```bash
# Generate manually
cd ai-agent-ecosystem
python3 tools/generate_summaries.py --force --verbose

# Check output
ls agents/summaries/*.yaml
```

### Problem: Capability discovery not finding agents

**Solution:**
```bash
# Verify summaries exist
ls agents/summaries/ | wc -l

# Regenerate if needed
python3 tools/generate_summaries.py --force

# Test discovery
python3 tools/capability_discovery.py --report
```

### Problem: Hooks not working in Cursor

**Solution:**
```bash
# 1. Check hooks.json exists
cat ~/.cursor/hooks.json

# 2. Check hooks are executable
ls -la ~/.cursor/hooks/**/*.sh

# 3. Check hook logs
tail -f ~/.cursor/command-execution.log
tail -f ~/.cursor/auto-continue.log

# 4. Reinstall hooks
python3 install-agents.py ~/.cursor/rules --all
```

### Problem: "Agent not found" errors

**Solution:**
```bash
# List available agents
python3 install-agents.py --list-agents

# List by category
python3 install-agents.py --list-by-category

# Reinstall specific agent
python3 install-agents.py ~/.cursor/rules --agents agent-name
```

---

## 🎓 Next Steps

### 1. For Cursor Users

```bash
# Test your installation
@strategic-task-planner: Hello, can you help me plan a project?

# Try custom commands
/code-review path/to/file.ts
/security-audit path/to/file.js

# Monitor hook activity
tail -f ~/.cursor/command-execution.log
```

### 2. For Claude Code Users

```bash
# Use capability discovery
cd ~/.claude-agents
python3 tools/capability_discovery.py --find "build REST API"

# Use lazy loading
python3 tools/lazy_loader.py --activate backend-architect
python3 tools/lazy_loader.py --status

# Parse progress
python3 tools/parse-progress.py workspaces/SHARED_PROGRESS.md
```

### 3. For Claude Desktop Users

```bash
# In Claude Desktop chat:
@strategic-task-planner: Help me plan a web application

# Use external tools:
cd ai-agent-ecosystem
python3 tools/capability_discovery.py --find "your need"
```

### 4. Read the Documentation

Start with:
1. `QUICK_REFERENCE.md` - Fast command reference
2. `IMPROVEMENTS_SUMMARY.md` - What's new
3. `WORKSPACE_PROTOCOLS.md` - How to use agents

---

## 📊 Verification Checklist

After installation, verify:

- [ ] Agents installed (`ls ~/.cursor/rules/*.mdc`)
- [ ] Documentation copied (`ls ~/.cursor/rules/*.md`)
- [ ] Summaries generated (`ls agents/summaries/*.yaml`)
- [ ] Tools executable (`ls -la tools/*.py tools/*.sh`)
- [ ] Capability discovery works (`python3 tools/capability_discovery.py --report`)
- [ ] Lazy loading works (`python3 tools/lazy_loader.py --list`)
- [ ] Progress parsing works (`python3 tools/parse-progress.py --help`)
- [ ] Error handling available (`python3 tools/error_handling.py`)

### For Cursor Only:
- [ ] Hooks installed (`cat ~/.cursor/hooks.json`)
- [ ] Hooks executable (`ls -la ~/.cursor/hooks/**/*.sh`)
- [ ] Commands installed (`ls ~/.cursor/commands/*.md`)

---

## 💡 Pro Tips

1. **Start Small**: Install coordination + core-technical categories first
2. **Use Lazy Loading**: Load summaries during planning, full definitions during execution
3. **Leverage Capability Discovery**: Let the system find the right agents
4. **Monitor Token Usage**: Use `lazy_loader.py --status` regularly
5. **Parse Progress**: Export to JSON for dashboards and analytics
6. **Update Regularly**: Pull latest changes weekly
7. **Customize**: Edit agents to match your workflow
8. **Contribute**: Share your custom agents with the community

---

## 🆘 Getting Help

- **Documentation**: Check `QUICK_REFERENCE.md` first
- **Issues**: Open GitHub issue with installation logs
- **Updates**: Watch repository for new features
- **Community**: Join discussions for tips and tricks

---

*Happy agent orchestrating! 🤖✨*
