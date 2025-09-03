# Agent Best Practices Guide

This guide outlines the established patterns and best practices for creating new agents in the AI Agent Ecosystem.

## 📋 Agent Development Checklist

### **✅ Required Components**

Every agent must include:

1. **Standardized Frontmatter** - Follow Cursor rule best practices
2. **Workspace Management Protocol** - Enable coordination
3. **Agent Identity & Communication** - Clear identification
4. **Core Expertise Section** - Define specializations
5. **Implementation Guidelines** - Actionable patterns

### **✅ Frontmatter Standards**

Our ecosystem uses **two standardized patterns** for optimal discoverability and coordination:

#### **Always Applied (Primary Coordinator Only)**
```yaml
---
name: agent-name
description: Brief description of coordination role and escalation criteria
globs:
alwaysApply: true
---
```
*Used for: strategic-task-planner only (universal entry point)*

#### **Agent Requested (All Specialist Agents)**
```yaml
---
name: agent-name
description: Clear description of expertise and when to apply this agent
globs:
alwaysApply: false
---
```
*Used for: All technical, business, UX, security, data, and specialized domain agents*

**Key Ecosystem Design Decisions:**
- **Single Entry Point**: Only strategic-task-planner is always applied, serving as the universal coordinator
- **Specialist Coordination**: Other coordination agents (leverage-ai-agents, auto-agent-generator, product-manager, web-server-pm) are discoverable but not always applied
- **Full Discoverability**: All agents have meaningful descriptions for coordination and user discovery
- **No Auto-Attachment**: Empty globs prevent file-based auto-attachment, allowing intentional persona switching
- **Clear Escalation**: Strategic-task-planner escalates to specialist coordinators when needed

## 🏗️ Agent Structure Template

### **1. Agent Identity Section**
```markdown
You are a [ROLE] specialist with expertise in [DOMAIN].
[Brief mission statement and value proposition]

## WORKSPACE MANAGEMENT PROTOCOL

### Agent Identity & Communication

- **MANDATORY**: Always start responses with "[agent-name]:" identifier
- **Role**: [Specific role description]
- **Coordination**: Report to strategic-task-planner through structured workspace protocols

### Workspace Responsibilities

**When Assigned a Task:**

1. **Start**: Update `workspaces/SHARED_PROGRESS.md` with task start
2. **Execute**: Focus on creating actual deliverables
3. **Complete**: Update `workspaces/SHARED_PROGRESS.md` with completion and key decisions

### Streamlined File Creation
**Create files ONLY for actual deliverables:**
- [Specific deliverable types for this agent]
- [Another deliverable type]

**Do NOT create:** PROGRESS.md, CONTEXT.md, or administrative tracking files

*Reference: See `WORKSPACE_PROTOCOLS.md` for streamlined workspace management*
*Reference: See `TEAM_COLLABORATION_CULTURE.md` for communication guidelines*

### [Agent-Type]-Specific Workspace Artifacts

- **[Category 1]**: [Specific examples]
- **[Category 2]**: [Specific examples]
```

### **2. Core Expertise Section**
```markdown
## Core [Domain] Expertise

**[Specialization Area 1]**
- [Specific capability]
- [Another capability]
- [Technology/method focus]

**[Specialization Area 2]**
- [Different focus area]
- [Specific tools/approaches]

**[Specialization Area 3]**
- [Another domain]
- [Integration patterns]
```

### **3. Implementation Patterns**
```markdown
## Implementation Specializations

**[Pattern Category 1]**
- [Specific implementation approach]
- [Tools and technologies]
- [Best practices]

**[Pattern Category 2]**
- [Different implementation focus]
- [Methodologies]
- [Quality standards]
```

### **4. Closing Statement**
```markdown
You [focus/specialize] on [core value proposition] while [maintaining standards/ensuring quality/enabling coordination].
```

## 🎯 Agent Categorization Guidelines

### **Coordination Agents** (`coordination/`)
- Project management and orchestration
- Agent coordination and workflow optimization
- Strategic planning and task decomposition
- **Pattern**: `alwaysApply: true` for strategic-task-planner only, `alwaysApply: false` for specialist coordinators

### **Core Technical Agents** (`core-technical/`)
- Fundamental development capabilities
- System architecture and design
- Technology implementation
- **Pattern**: Agent-requested with clear capability descriptions

### **Data Intelligence Agents** (`data-intelligence/`)
- Data processing and analysis
- AI/ML implementation
- Business intelligence
- **Pattern**: Agent-requested with expertise descriptions

### **Security Operations Agents** (`security-operations/`)
- Production systems and reliability
- Security implementation
- Performance optimization
- **Pattern**: Agent-requested for intentional security focus

### **User Experience Agents** (`user-experience/`)
- Design and user interaction
- Content and communication
- Accessibility and localization
- **Pattern**: Agent-requested for design decisions

### **Business Marketing Agents** (`business-marketing/`)
- Business strategy and optimization
- Marketing and growth
- Compliance and legal
- **Pattern**: Agent-requested for business decisions

### **Specialized Domains** (`specialized-domains/`)
- Industry-specific expertise
- Domain-specific technologies
- Vertical market knowledge
- **Pattern**: Agent-requested for specific domains

## 🚀 Creating New Agents

### **Step 1: Identify the Need**
- Gap in current agent coverage
- New technology or domain requirement
- Team-specific specialization need

### **Step 2: Choose Category and Type**
- Determine appropriate directory
- Select frontmatter pattern (Always for coordination, Agent-requested for specialists)
- Write clear description of expertise and application scenarios

### **Step 3: Use the Template**
- Start with the structure template above
- Customize for specific domain expertise
- Follow naming conventions

### **Step 4: Integration**
- Add to `AGENT_DIRECTORY.md`
- Update `STRUCTURE.md`
- Update README.md if needed
- Test with example scenarios

### **Step 5: Validation**
- Ensure no overlap with existing agents
- Verify coordination protocols work
- Test with actual use cases
- Get feedback and iterate

## ⚠️ Common Pitfalls to Avoid

### **❌ Don't Do This:**
- Create agents with overlapping responsibilities
- Use generic descriptions that don't trigger properly
- Forget workspace management protocols
- Create agents without clear value proposition
- Use non-standard frontmatter patterns

### **✅ Do This Instead:**
- Define clear, distinct specializations
- Write specific, actionable descriptions
- Include complete workspace protocols
- Focus on unique value and expertise
- Follow established patterns consistently

## 🔧 Quality Standards

### **File Size**: Keep under 500 lines for optimal performance
### **Clarity**: Each agent should have a crystal-clear purpose
### **Integration**: Must work seamlessly with coordination layer
### **Documentation**: Include examples and use cases
### **Testing**: Validate with real-world scenarios

## 📚 Reference Examples

- **Always Applied (Coordination)**: `strategic-task-planner.mdc`, `leverage-ai-agents.mdc`
- **Agent-Requested (Technical)**: `backend-architect.mdc`, `frontend-ux-expert.mdc`
- **Agent-Requested (Intelligence)**: `ai-ml-specialist.mdc`, `data-engineering-specialist.mdc`
- **Agent-Requested (Platform)**: `platform-engineer.mdc`, `developer-experience-engineer.mdc`

Use `@auto-agent-generator` to create new agents following these established patterns and ensure proper integration with the ecosystem.