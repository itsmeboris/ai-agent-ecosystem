# Streamlined Agent Workspace Template

## Use This Pattern for ALL Agents

Replace the old bloated workspace section with this streamlined version:

```markdown
## WORKSPACE MANAGEMENT

### Agent Identity & Communication
- **MANDATORY**: Always start responses with "[agent-name]:" identifier
- **Role**: [Brief role description]
- **Focus**: [Core responsibility]

*Reference: See `WORKSPACE_PROTOCOLS.md` for streamlined workspace management*
*Reference: See `TEAM_COLLABORATION_CULTURE.md` for communication guidelines*

### Streamlined Work Protocol

**When Assigned a Task:**
1. **Start**: Update `workspaces/SHARED_PROGRESS.md` with task start
2. **Execute**: Focus on creating actual deliverables
3. **Complete**: Update `workspaces/SHARED_PROGRESS.md` with completion and brief summary

### File Creation Rule
**Create files ONLY for:**
- Actual code implementation
- Configuration files
- Technical documentation
- Design artifacts

**Do NOT create:**
- PROGRESS.md (use SHARED_PROGRESS.md instead)
- CONTEXT.md (document key decisions in SHARED_PROGRESS.md)
- Administrative tracking files
- Redundant status files
```

## Key Changes Made
1. **Eliminated mandatory PROGRESS.md and CONTEXT.md**
2. **Centralized all status tracking in SHARED_PROGRESS.md**
3. **Focus on deliverables, not bureaucracy**
4. **Reduced file overhead by ~80%**

## Migration Pattern
For each agent file:
1. Replace entire "Workspace Management" section with streamlined template
2. Remove references to PROGRESS.md and CONTEXT.md creation
3. Keep agent-specific expertise and responsibilities
4. Update file management requirements to focus on deliverables only