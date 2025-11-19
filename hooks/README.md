# Cursor Hooks for AI Agent Ecosystem

This directory contains Cursor hooks that enhance the AI agent ecosystem with automated workspace management, command execution, and task continuation.

## 📋 Available Hooks

### 1. **Workspace Progress Enforcement** (`afterAgentResponse`)
**Script**: `workspace/enforce-progress-update.sh`

**Purpose**: Reminds agents to update `SHARED_PROGRESS.md` after completing tasks

**How it works**:
- Triggers after every agent response
- Detects agent identity from response format
- Sends a reminder message about updating workspace progress
- Ensures compliance with `WORKSPACE_PROTOCOLS.md`

**Value**: ✅ Maintains consistent documentation without manual enforcement

---

### 2. **Command Execution & Output Capture** (`beforeShellExecution`)
**Script**: `execution/command-executor.sh`

**Purpose**: Intercepts shell commands, executes them safely, and returns output to the agent

**How it works**:
- Intercepts every shell command before execution
- Executes command with 30-second timeout
- Captures both stdout and stderr
- Returns formatted output to agent for analysis
- Logs all command execution to `~/.cursor/command-execution.log`

**Value**: ✅ Agents can see command output and make informed decisions

**Features**:
- ⏱️ 30-second timeout prevents hanging
- 📝 Full output capture (stdout + stderr)
- 📊 Exit code reporting
- 🔒 Execution logging for audit trail

---

### 3. **Auto-Continue Execution** (`stop`)
**Script**: `automation/auto-continue.sh`

**Purpose**: Automatically continues with pending tasks without user intervention

**How it works**:
- Triggers when agent loop completes
- Scans `SHARED_PROGRESS.md` for pending tasks (🔄, "In Progress", "Pending", "TODO")
- If pending tasks found, automatically submits followup message
- Respects loop limit (max 4 auto-continues, Cursor enforces 5 total)
- Logs all decisions to `~/.cursor/auto-continue.log`

**Value**: ✅ Enables unattended multi-task project execution

**Safety Features**:
- ✅ Only continues on successful completion
- ✅ Enforces loop limits to prevent infinite execution
- ✅ Clear logging for debugging
- ✅ Respects explicit completion signals

---

## 🚀 Installation

### Quick Install

```bash
# Run the install script (coming soon)
./install-hooks.sh ~/.cursor
```

### Manual Install

1. Copy hooks directory:
```bash
cp -r hooks ~/.cursor/
```

2. Copy hooks.json:
```bash
cp hooks/hooks.json ~/.cursor/hooks.json
```

3. Restart Cursor IDE

4. Verify hooks are active:
   - Open Cursor Settings → Hooks tab
   - Check that all 3 hooks are listed

---

## 📊 Monitoring & Logs

### Log Files

All hooks create log files for monitoring and debugging:

| Log File | Purpose | Hook |
|----------|---------|------|
| `~/.cursor/command-execution.log` | Command execution audit trail | command-executor.sh |
| `~/.cursor/auto-continue.log` | Auto-continue decisions | auto-continue.sh |

### Viewing Logs

```bash
# Watch command execution in real-time
tail -f ~/.cursor/command-execution.log

# View auto-continue decisions
tail -f ~/.cursor/auto-continue.log

# Check recent command activity
tail -n 50 ~/.cursor/command-execution.log
```

---

## 🔧 Configuration

### Adjusting Timeouts

Edit `execution/command-executor.sh`:
```bash
TIMEOUT=30  # Change to desired timeout in seconds
```

### Adjusting Auto-Continue Loop Limit

Edit `automation/auto-continue.sh`:
```bash
MAX_LOOPS=4  # Change to desired max loops (Cursor enforces 5 total)
```

### Customizing Reminder Messages

Edit `workspace/enforce-progress-update.sh` to customize the reminder text sent to agents.

---

## 🎯 How Hooks Enhance Your Workflow

### Before Hooks:
- ❌ Agents sometimes forget to update SHARED_PROGRESS.md
- ❌ Command output only visible in terminal
- ❌ Manual intervention needed to continue multi-task projects
- ❌ No audit trail of command execution

### After Hooks:
- ✅ Automatic reminders ensure workspace documentation
- ✅ Agents see command output and can analyze results
- ✅ Unattended execution of complex multi-agent workflows
- ✅ Complete audit trail of all command execution
- ✅ Safe command execution with timeouts

---

## 🔒 Security Considerations

### Command Execution Safety
- ✅ 30-second timeout prevents infinite loops
- ✅ All commands logged for audit
- ✅ Working directory properly set
- ✅ Exit codes captured and reported

### Auto-Continue Safety
- ✅ Only continues on successful completion
- ✅ Loop limit prevents infinite execution
- ✅ Clear logging of all decisions
- ✅ Respects explicit stop signals

### Recommended Additional Security

For production use, consider adding to `command-executor.sh`:
- Resource limits (memory, CPU)
- Command whitelisting/blacklisting
- Dangerous operation detection (e.g., `rm -rf`, `force push`)
- User approval for risky commands

See the main hooks documentation for examples: https://cursor.com/docs/agent/hooks

---

## 🐛 Troubleshooting

### Hooks Not Working

1. **Check Cursor Settings**:
   - Open Settings → Hooks tab
   - Verify hooks are listed and enabled

2. **Verify Hook Scripts Are Executable**:
```bash
ls -la ~/.cursor/hooks/*/
# Should show -rwxr-xr-x (executable)
```

3. **Check Script Paths**:
```bash
cat ~/.cursor/hooks.json
# Verify paths are relative to hooks.json location
```

4. **View Hook Output**:
   - Check Cursor's "Hooks" output channel
   - Review log files in `~/.cursor/`

5. **Restart Cursor**:
   - Close and reopen Cursor IDE completely

### Command Execution Issues

**Problem**: Commands timing out

**Solution**: Increase timeout in `command-executor.sh`

**Problem**: Output too verbose

**Solution**: Add output truncation to the script:
```bash
output=$(timeout $TIMEOUT bash -c "$command" 2>&1 | head -n 100)
```

### Auto-Continue Issues

**Problem**: Auto-continue not triggering

**Solution**: Check that `SHARED_PROGRESS.md` exists and contains status markers:
- Must have `Status` keyword followed by emoji or status text
- Supported: `🔄`, `In Progress`, `Pending`, `TODO`

**Problem**: Too many auto-continue loops

**Solution**: Reduce `MAX_LOOPS` in `auto-continue.sh`

---

## 📚 Further Reading

- [Cursor Hooks Documentation](https://cursor.com/docs/agent/hooks)
- [AI Agent Ecosystem Documentation](../README.md)
- [Workspace Protocols](../agents/coordination/WORKSPACE_PROTOCOLS.md)
- [Agent Coordination Guide](../docs/agent-coordination-guide.md)

---

## 🤝 Contributing

Have ideas for new hooks? Found a bug? 

1. Test your hook locally first
2. Ensure it follows security best practices
3. Add clear documentation
4. Submit a PR with examples

---

## 📝 License

Same as the main AI Agent Ecosystem project.

