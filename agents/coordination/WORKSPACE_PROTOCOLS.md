# Workspace Management Protocols

*For coordination methodologies and agent selection patterns, see `agent-coordination-guide.md`*

## 🎯 Purpose

This protocol defines how agents manage tasks, track progress, and create deliverables with **minimal bureaucratic overhead**.

**Key Principle**: Focus on delivering actual work products, not administrative tracking files.

---

## Streamlined Workspace Structure

### Core File Strategy: **ONE PRIMARY FILE PER AGENT**
- **`SHARED_PROGRESS.md`**: Central coordination hub for ALL agents
- **Agent workspace**: ONLY create additional files when they contain actual deliverables (code, configs, docs)
- **Do NOT create**: `PROGRESS.md`, `CONTEXT.md`, or other administrative tracking files

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

---

## 📝 Concrete Examples

### Example 1: Task Start (Good ✅)

```markdown
<!-- In workspaces/SHARED_PROGRESS.md -->

## 2025-10-21 14:30 - @backend-architect: User Management API

**Status**: 🔄 Started
**Task**: Implement REST API for user authentication and profile management
**Estimated Time**: 3 hours
**Dependencies**: Database schema complete (by @database-implementation-specialist)
**Approach**: RESTful API with JWT authentication, rate limiting, pagination
```

### Example 2: Progress Update (Good ✅)

```markdown
## 2025-10-21 16:00 - @backend-architect: User Management API

**Status**: 🔄 In Progress (60% complete)
**Milestone**: Authentication endpoints complete, working on profile management
**Key Decision**: Using JWT with 15-minute expiry and refresh tokens (90-day expiry)
**Files Created**:
- `/workspaces/backend-architect/api-spec.yaml` (OpenAPI specification)
- `/workspaces/backend-architect/auth-service.js` (Authentication logic)
```

### Example 3: Task Completion (Good ✅)

```markdown
## 2025-10-21 17:30 - @backend-architect: User Management API

**Status**: ✅ Complete

**Deliverables**:
- `/workspaces/backend-architect/api-spec.yaml` (Complete OpenAPI 3.0 spec)
- `/workspaces/backend-architect/auth-service.js` (Authentication service)
- `/workspaces/backend-architect/user-service.js` (User profile service)
- `/workspaces/backend-architect/middleware/rate-limiter.js` (Rate limiting: 100 req/min per IP)

**Key Decisions**:
- JWT authentication with short-lived access tokens (15 min) and long-lived refresh tokens (90 days)
- Rate limiting: 100 requests/minute per IP address
- Pagination: Cursor-based for user lists (better performance at scale)
- Password requirements: Min 12 chars, 1 uppercase, 1 number, 1 special char

**Testing**: All endpoints tested with Postman collection (included in workspace)

**Next Steps**:
- Ready for @web-security-specialist security review
- Recommend @qa-reliability-engineer for integration testing
- API documented and ready for @frontend-ux-expert integration
```

### Example 4: Multi-Agent Handoff (Good ✅)

```markdown
## 2025-10-21 18:00 - @web-security-specialist: Security Review Complete

**Status**: ✅ Complete
**Reviewed**: @backend-architect's User Management API

**Security Assessment**:
- ✅ Authentication: JWT implementation follows OWASP best practices
- ✅ Authorization: Role-based access control properly implemented
- ✅ Input Validation: All inputs sanitized, SQL injection protected
- ⚠️ Recommendation: Add Content Security Policy headers (not blocking)
- ✅ Rate Limiting: Appropriate for production use

**Files Updated**:
- `/workspaces/backend-architect/auth-service.js` (Added CSP headers)
- `/workspaces/web-security-specialist/security-checklist.md` (Audit trail)

**Handoff**: Ready for @devops-infrastructure-specialist deployment
```

### ❌ Anti-Pattern: Too Much Administrative Overhead

```markdown
<!-- DON'T DO THIS -->

## workspaces/backend-architect/PROGRESS.md
## workspaces/backend-architect/CONTEXT.md
## workspaces/backend-architect/TODO.md
## workspaces/backend-architect/NOTES.md
## workspaces/backend-architect/DECISIONS.md

<!-- This creates 5 administrative files with overlapping content! -->
```

**Why This Is Bad**:
- Duplication of information across multiple files
- Time wasted on administrative tasks instead of actual work
- Harder to find information (spread across files)
- Increases cognitive load for next agent

**Do This Instead**:
- ONE entry in `SHARED_PROGRESS.md` with all key information
- Create only actual deliverable files (code, configs, docs)

---

## ✅ Success Criteria

### A Well-Managed Workspace Has:
- ✅ Clear task status in `SHARED_PROGRESS.md`
- ✅ Only actual deliverable files (no administrative clutter)
- ✅ Key decisions documented inline in `SHARED_PROGRESS.md`
- ✅ Clear handoff notes for next agent
- ✅ Minimal overhead - agents spend 90%+ time on actual work
- ✅ Easy to understand workspace structure (next agent can jump in quickly)

### Red Flags (Poor Workspace Management):
- ❌ Multiple `PROGRESS.md`, `CONTEXT.md`, `NOTES.md` files
- ❌ Unclear task status - have to hunt through files
- ❌ No handoff notes - next agent doesn't know what was done
- ❌ Too many administrative files relative to actual deliverables
- ❌ Duplicate information across files
- ❌ Vague updates ("made progress") without specifics

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "Too Many Files in Workspace"

**Symptom**: Workspace has 10+ files but only 2-3 are actual deliverables

**Solution**:
1. Delete administrative files (`PROGRESS.md`, `CONTEXT.md`, `NOTES.md`)
2. Move key information to `SHARED_PROGRESS.md`
3. Keep only actual work products (code, configs, documentation)

**Prevention**: Review `.mdc` file - ensure it has explicit "Do NOT create" statement

### Issue 2: "Lost Context Between Agents"

**Symptom**: Next agent doesn't know what previous agent did or why

**Solution**:
1. Previous agent updates `SHARED_PROGRESS.md` with:
   - What was completed
   - Key decisions made (and rationale)
   - What next agent needs to know
   - Where deliverables are located
2. Use **handoff notes** section in completion update

**Prevention**: Follow task completion protocol (Example 3 above)

### Issue 3: "Agent Created PROGRESS.md Despite Instructions"

**Symptom**: Agent creates `PROGRESS.md` even though `.mdc` says not to

**Root Cause**: `.mdc` file missing explicit "Do NOT create" statement

**Solution**:
1. Check agent's `.mdc` file for workspace management section
2. Ensure it contains: "Do NOT create PROGRESS.md, CONTEXT.md, or administrative tracking files"
3. If missing, add to agent's `.mdc` file

**Example Fix** (add to agent `.mdc`):
```markdown
## Workspace Management

**Use `SHARED_PROGRESS.md`** for all task tracking and status updates.

**Do NOT create**: `PROGRESS.md`, `CONTEXT.md`, `TODO.md`, or other administrative files. Focus on delivering actual work products.

**Files to create**: Only actual deliverables (code, configurations, documentation)
```

### Issue 4: "Can't Find Agent's Deliverables"

**Symptom**: Agent said task is complete but files are missing or unclear

**Solution**:
1. Check `SHARED_PROGRESS.md` completion entry for file list
2. Files should be explicitly listed with paths
3. If missing, ask agent to update completion entry with deliverable locations

**Prevention**: Follow Example 3 format with explicit file paths

### Issue 5: "Updates Too Verbose / Not Enough Detail"

**Symptom A**: `SHARED_PROGRESS.md` entries are 500+ lines of detailed logs
**Solution**: Focus on key milestones only (start, significant progress, completion). Skip minutiae.

**Symptom B**: `SHARED_PROGRESS.md` entries are too vague ("made progress")
**Solution**: Include specifics - what was completed, key decisions, deliverable file locations.

**Sweet Spot**: 5-20 lines per significant update (see Examples 1-4 above)

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