# Install Script Improvements Needed

## Current Issues

### 1. Documentation Files Not Copied for Claude Desktop
**Problem**: Line 441-466 skips documentation for `--claude` installations
```python
if install_type == "cursor":
    # Copy docs
else:
    print("📋 Installing for Claude Desktop (documentation files not needed)...")
    docs_copied = 0  # SKIPPED!
```

**Impact**: Protocol documents (CAPABILITY_DISCOVERY.md, TOKEN_EFFICIENCY.md, etc.) not available

### 2. Summaries Not Copied to Target
**Problem**: `generate_agent_summaries()` creates summaries in repo's `agents/summaries/` but doesn't copy them to target directory

**Impact**: Summaries exist but not accessible in installed location

### 3. Tools Directory Not Copied
**Problem**: No code to copy `tools/` directory

**Impact**: Users can't use:
- `capability_discovery.py`
- `lazy_loader.py`
- `generate_summaries.py`
- `parse-progress.py`
- `error_handling.py`

### 4. Cursor Uses Outdated Hooks/Commands
**Problem**: Current hooks/commands don't leverage new v2.1.0 infrastructure

**Should Instead**:
- Use `capability_discovery.py` for agent selection
- Use `lazy_loader.py` for token efficiency
- Provide easy access to tools from Cursor

---

## Proposed Solutions

### Solution 1: Always Copy Documentation
```python
# Remove Claude Desktop special case
# Copy docs for ALL platforms
if install_type in ["cursor", "claude", "claude-code"]:
    print("📋 Copying documentation and protocols...")
    doc_results = copy_documentation_files(target_dir)
```

### Solution 2: Copy Summaries to Target
```python
def copy_summaries(target_dir: Path) -> int:
    """Copy agent summaries to target directory."""
    script_dir = get_script_directory()
    source_summaries = script_dir / "agents" / "summaries"
    target_summaries = target_dir / "summaries"

    if not source_summaries.exists():
        return 0

    target_summaries.mkdir(exist_ok=True)

    copied = 0
    for summary_file in source_summaries.glob("*.yaml"):
        shutil.copy2(summary_file, target_summaries / summary_file.name)
        copied += 1

    return copied
```

### Solution 3: Copy Tools Directory
```python
def copy_tools(target_dir: Path) -> dict:
    """Copy tools directory to target."""
    script_dir = get_script_directory()
    source_tools = script_dir / "tools"
    target_tools = target_dir / "tools"

    if not source_tools.exists():
        return {'count': 0, 'success': False}

    try:
        if target_tools.exists():
            shutil.rmtree(target_tools)
        shutil.copytree(source_tools, target_tools)

        # Make scripts executable
        for script in target_tools.glob("*.py"):
            script.chmod(0o755)
        for script in target_tools.glob("*.sh"):
            script.chmod(0o755)

        tool_count = len(list(target_tools.glob("*.py")))
        return {'count': tool_count, 'success': True}
    except Exception as e:
        print(f"⚠️  Warning: Failed to copy tools: {e}")
        return {'count': 0, 'success': False}
```

### Solution 4: Create Tool Wrapper Commands for Cursor

Instead of hooks, create simple commands that call tools:

**~/.cursor/commands/discover-agent.md**:
```markdown
---
name: discover-agent
description: Find the right agent for your requirement
---

Run: ~/.cursor/rules/tools/capability_discovery.py --find "${requirement}"
```

**~/.cursor/commands/lazy-load.md**:
```markdown
---
name: lazy-load
description: Load agent summary or activate full agent
---

Run: ~/.cursor/rules/tools/lazy_loader.py --activate "${agent-name}"
```

---

## Implementation Priority

### High Priority (Fix Immediately)
1. ✅ Copy documentation for all platforms
2. ✅ Copy summaries to target directory
3. ✅ Copy tools to target directory

### Medium Priority (Enhance)
4. Create tool wrapper commands for Cursor
5. Add tool verification step
6. Document tool usage in installed location

### Low Priority (Future)
7. Create unified tool interface
8. Add tool auto-discovery
9. Create GUI tool launcher

---

## Updated Installation Flow

```python
def install_agents(target_dir, install_type, ...):
    # 1. Copy documentation (ALL platforms)
    doc_results = copy_documentation_files(target_dir)

    # 2. Copy agents
    for agent in agents:
        copy_agent(agent, ...)

    # 3. Generate summaries (in repo)
    generate_agent_summaries()

    # 4. Copy summaries to target
    summaries_copied = copy_summaries(target_dir)

    # 5. Copy tools to target
    tools_result = copy_tools(target_dir)

    # 6. Create tool wrappers (Cursor only)
    if install_type == "cursor":
        create_tool_commands(target_dir)

    # 7. Summary
    print(f"✅ Agents: {agent_count}")
    print(f"✅ Docs: {docs_copied}")
    print(f"✅ Summaries: {summaries_copied}")
    print(f"✅ Tools: {tools_result['count']}")
```

---

## Cursor Tool Integration

### Option A: Commands That Call Tools
Create command files that execute Python tools:
```bash
~/.cursor/commands/
├── discover-agent.md      # Calls capability_discovery.py
├── load-agent.md          # Calls lazy_loader.py
├── parse-progress.md      # Calls parse-progress.py
└── validate-progress.md   # Calls validate-progress.sh
```

### Option B: Direct Tool Access
Document tools and let users call them:
```bash
# User runs directly
~/.cursor/rules/tools/capability_discovery.py --find "REST API"
```

### Option C: Hybrid Approach (Recommended)
- Copy tools to ~/.cursor/rules/tools/
- Create helper commands for common operations
- Document direct tool usage in QUICK_REFERENCE.md

---

## Testing Plan

After implementing fixes:

```bash
# Test 1: Claude Desktop with everything
python3 install-agents.py .claude/agents --claude --all
ls .claude/agents/  # Should have agents, docs, summaries, tools

# Test 2: Cursor with tools (no hooks)
python3 install-agents.py ~/.cursor/rules --all --skip-hooks
ls ~/.cursor/rules/tools/  # Should have all 7 tools

# Test 3: Claude Code
python3 install-agents.py .claude-code --all --skip-hooks --skip-commands
ls .claude-code/  # Should have agents, docs, summaries, tools

# Test 4: Verify tool execution
.claude/agents/tools/capability_discovery.py --find "test"
.claude/agents/tools/lazy_loader.py --list
```

---

## File Structure After Fix

```
~/.cursor/rules/                    # or .claude/agents/
├── agents/
│   ├── backend-architect.mdc
│   ├── ... (48 agents)
│
├── summaries/                      # NEW! Copied
│   ├── backend-architect.summary.yaml
│   ├── ... (48 summaries)
│
├── tools/                          # NEW! Copied
│   ├── capability_discovery.py
│   ├── lazy_loader.py
│   ├── generate_summaries.py
│   ├── parse-progress.py
│   ├── error_handling.py
│   ├── analyze-progress.sh
│   └── validate-progress.sh
│
├── docs/                           # Protocol docs
│   ├── AGENT_HIERARCHY.md
│   ├── CAPABILITY_DISCOVERY.md
│   ├── TOKEN_EFFICIENCY.md
│   ├── ... (12 docs)
│
└── commands/                       # Cursor only
    ├── discover-agent.md          # NEW! Tool wrapper
    └── ... (tool commands)
```

---

## Next Steps

1. **Immediate**: Update install-agents.py with new functions
2. **Test**: Run installation on all platforms
3. **Document**: Update INSTALLATION_GUIDE.md with tool usage
4. **Cleanup**: Remove outdated hooks (user requested)
5. **Verify**: Test tool execution from installed location
