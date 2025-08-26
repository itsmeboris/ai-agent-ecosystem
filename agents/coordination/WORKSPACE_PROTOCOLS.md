# Workspace Management Protocols

*For coordination methodologies and agent selection patterns, see `agent-coordination-guide.md`*

## Streamlined Workspace Structure

### Core File Strategy: **ONE PRIMARY FILE PER AGENT**
- **`SHARED_PROGRESS.md`**: Central coordination hub for ALL agents
- **Agent workspace**: ONLY create additional files when they contain actual deliverables (code, configs, docs)
- **No mandatory PROGRESS.md or CONTEXT.md** - use SHARED_PROGRESS.md instead

### Before Starting Any Task
1. Read `workspaces/SHARED_PROGRESS.md` for context
2. Update `SHARED_PROGRESS.md` with task start status

### During Task Execution
1. Work efficiently, focus on deliverables
2. Update `SHARED_PROGRESS.md` with key milestones only
3. Create files ONLY for actual work products (code, configurations, documentation)

### Task Completion Protocol
1. Update `SHARED_PROGRESS.md` with completion status and key decisions
2. Ensure all deliverable files are in workspace
3. Include brief handoff notes in `SHARED_PROGRESS.md`

## Sequential Delegation Protocol

```
1. Update SHARED_PROGRESS.md with task assignment
2. Delegate to specialist agent with complete context
3. Monitor SHARED_PROGRESS.md for completion updates
4. Review agent workspace for deliverable files only
5. Verify deliverables meet requirements
6. ONLY THEN proceed to next delegation
```

## Persona Switching Protocol

**When user indicates "start" or "begin" after delegation:**

1. **Load Agent Persona**: Switch to the assigned agent's identity and expertise
2. **Announce Identity**: Start response with agent's mandatory identifier
3. **Execute Task**: Work on the assigned task using agent's specialized knowledge
4. **Focus on Deliverables**: Create only essential work products, update SHARED_PROGRESS.md with key milestones
5. **Complete Handoff**: When done, return to coordinator or next agent in sequence

**For Multi-Agent Tasks:**
- Follow AGENT_HIERARCHY.md priority order
- Execute highest priority agents first unless dependencies dictate otherwise
- For concurrent tasks, identify independent streams and work sequentially within each
- Switch personas as you move between agents, maintaining their unique expertise

## Quality Assurance Standards

### Streamlined File Organization
- Create files ONLY for actual deliverables (code, configs, documentation)
- Use clear, descriptive filenames for work products
- Keep workspace clean - avoid administrative files
- Document key decisions in SHARED_PROGRESS.md only

### Communication Standards
- Always announce agent identity when switching
- Maintain agent-specific expertise and tone
- Update SHARED_PROGRESS.md with essential status only
- Focus on deliverables, not bureaucratic overhead

### Validation Requirements
- Verify deliverables meet acceptance criteria
- Ensure essential decisions documented in SHARED_PROGRESS.md
- Validate handoff completeness before proceeding
- Maintain quality standards with minimal administrative burden