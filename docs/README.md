# Documentation Guide

Essential documentation for the AI Agent Ecosystem.

---

## 📚 Core Documentation

### Root Level
- **[README.md](../README.md)** - Project overview, agent catalog, quick start guide
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines and agent creation standards
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history and release notes

### Documentation Directory
- **[agent-best-practices.md](agent-best-practices.md)** - Agent development standards and patterns
- **[agent-coordination-guide.md](agent-coordination-guide.md)** - Multi-agent coordination workflows
- **[quick-start-guide.md](quick-start-guide.md)** - Getting started with the ecosystem

---

## 🎯 Quick Links

### For Users
- **Getting Started**: See [quick-start-guide.md](quick-start-guide.md)
- **Agent Catalog**: See [README.md](../README.md) → Agent Architecture section
- **How It Works**: See [README.md](../README.md) → How It Works section

### For Contributors
- **Creating Agents**: See [CONTRIBUTING.md](../CONTRIBUTING.md) → Creating New Agents
- **Development Standards**: See [agent-best-practices.md](agent-best-practices.md)
- **Coordination Patterns**: See [agent-coordination-guide.md](agent-coordination-guide.md)

### For Updates
- **Version History**: See [CHANGELOG.md](../CHANGELOG.md)
- **Recent Changes**: See v2.0.0 standardization updates

---

## 📋 Documentation Standards

### Agent Description Format
All agents use the standardized format:

```yaml
description: Primary capability, secondary capability, tertiary capability, and quaternary capability
```

**Guidelines:**
- 50-150 characters
- Action-oriented
- 3-5 key capabilities
- No "USE WHEN" prefix

### Agent File Structure
```yaml
---
name: agent-name
description: [capabilities]
globs:
alwaysApply: false
---

Opening paragraph with expertise statement

## WORKSPACE MANAGEMENT PROTOCOL
[Standard workspace protocols]

## Core Expertise
[Agent-specific expertise]

## Coordination Patterns
[How agent works with others]
```

---

## 🚀 Common Workflows

### Using Agents

**Simple Projects (1-3 agents):**
```
@strategic-task-planner → Specialist Agents → Complete
```

**Complex Projects (4+ agents):**
```
@strategic-task-planner → @leverage-ai-agents → Multi-Agent Coordination → Complete
```

**Quick Consultation:**
```
[CONSULT] @specialist-name: "Quick expert input needed"
```

### Creating New Agents

**Recommended:**
```
@auto-agent-generator: Create a [domain]-specialist agent for [expertise]
```

**Manual Creation:**
1. Choose category in `agents/[category]/`
2. Create `[agent-name].mdc`
3. Follow template in [agent-best-practices.md](agent-best-practices.md)
4. Keep under 400 lines
5. Test coordination with other agents

---

## 📊 Ecosystem Stats

- **Total Agents**: 48
- **Categories**: 7
- **Documentation Files**: 6 (3 root + 3 docs)
- **Standardized Descriptions**: 100%
- **Version**: 2.0.0

---

*Last Updated: November 17, 2025*
*For questions, see [CONTRIBUTING.md](../CONTRIBUTING.md)*

