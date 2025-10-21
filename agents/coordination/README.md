# Coordination Agents

Strategic planning and agent ecosystem orchestration specialists who coordinate complex multi-domain projects.

## Overview

The Coordination category contains the **"brain" of the AI Agent Ecosystem** - these 5 agents are responsible for understanding project requirements, selecting the right specialist agents, and orchestrating their collaboration to achieve complex goals.

This category is typically the **first point of contact** for any significant project. These agents analyze what needs to be done, break it down into manageable pieces, select the optimal specialists, and ensure smooth handoffs between them.

**Agent Count**: 5 orchestration specialists
**Typical Project Phase**: Planning & Coordination (throughout project lifecycle)
**Dependencies**: None (these are your starting point)
**Enables**: All other categories - coordination agents decide which specialists to engage

---

## Agents in This Category

### Primary Orchestrators

#### strategic-task-planner
**Role**: Primary coordinator for project planning and task decomposition
**Use When**:
- Starting any multi-step project (3+ tasks)
- Need to break down complex requirements
- Uncertain which agents to use
- Sequential workflow with dependencies

**Delivers**: Detailed execution plan with agent sequence, dependencies, success criteria
**Integrates With**: All agents - serves as primary orchestrator
**Typical Timeline**: 15-30 minutes for planning phase

**Key Capabilities**:
- Task decomposition and dependency mapping
- Agent selection and sequencing
- Risk assessment and mitigation planning
- Quality gate definition
- Persona switching for execution

**Example Usage**:
```
@strategic-task-planner: We need to build a SaaS application for project management

→ Output: Complete execution plan with 6-phase approach, agent sequence,
          timeline estimates, success criteria, and risk mitigation
```

#### leverage-ai-agents
**Role**: Meta-coordinator for complex multi-agent orchestration
**Use When**:
- Projects require 4+ agents with complex dependencies
- Parallel workflows needed
- Cross-domain integration challenges
- Performance optimization of agent collaboration
- Ecosystem-wide coordination

**Delivers**: Optimized agent collaboration workflows, parallel execution plans, performance improvements
**Integrates With**: Receives delegation from strategic-task-planner for complex projects
**Typical Timeline**: 20-40 minutes for complex coordination design

**Key Capabilities**:
- Multi-agent workflow optimization
- Parallel stream management
- Complex coordination patterns
- Agent utilization analysis
- Consultation mode orchestration

**Example Usage**:
```
@leverage-ai-agents: Design optimal workflow for e-commerce platform with
AI recommendations, global localization, and real-time analytics

→ Output: 3 parallel work streams with 12 agents, synchronization points,
          integration strategy, and performance optimization plan
```

### Specialized Coordinators

#### auto-agent-generator
**Role**: Dynamic agent creation for specialized domains
**Use When**:
- Need expertise not covered by existing 48 agents
- Industry-specific requirements (healthcare, finance, etc.)
- Emerging technology domains
- Custom workflow requirements

**Delivers**: New agent .mdc file following ecosystem standards
**Integrates With**: strategic-task-planner (when gaps identified)
**Typical Timeline**: 10-20 minutes for agent creation

**Key Capabilities**:
- Requirement analysis for new agents
- Agent specification creation
- Ecosystem integration
- Documentation generation

#### web-server-pm
**Role**: Project management for web server development initiatives
**Use When**:
- Web server or API project management
- Backend infrastructure projects
- Server deployment coordination

**Delivers**: Project plans, milestone tracking, resource allocation
**Integrates With**: backend-architect, devops-infrastructure-specialist
**Typical Timeline**: Ongoing throughout backend projects

#### product-manager
**Role**: Product strategy, roadmap planning, and stakeholder management
**Use When**:
- Product strategy definition
- Roadmap planning
- Feature prioritization
- Stakeholder communication

**Delivers**: Product requirements, roadmaps, prioritization frameworks
**Integrates With**: strategic-task-planner, business-analyst
**Typical Timeline**: Ongoing throughout product lifecycle

---

## When to Use This Category

### Scenario 1: Starting Any Multi-Step Project
**Situation**: You have a project idea but aren't sure where to begin
**Agent Sequence**: `@strategic-task-planner` (analyze and plan)
**Timeline**: 15-30 minutes
**Outcome**: Clear execution plan with agent sequence

**Step-by-Step**:
1. **@strategic-task-planner**: Analyzes requirements, creates execution plan
2. *Then*: Follow the plan to engage specific specialist agents

**Example**:
```
User: "I need to build a real-time chat application"

@strategic-task-planner: "Here's the execution plan:
1. @system-architecture-designer - WebSocket architecture
2. @database-implementation-specialist - Message storage
3. @backend-architect - Real-time API
4. @frontend-ux-expert - Chat interface
5. @web-security-specialist - Authentication & encryption
6. @devops-infrastructure-specialist - Deployment"

Result: Clear roadmap for 6-agent sequential execution
```

### Scenario 2: Complex Multi-Domain Project
**Situation**: Project requires 4+ agents with parallel work streams
**Agent Sequence**: `@strategic-task-planner → @leverage-ai-agents`
**Timeline**: 30-60 minutes
**Outcome**: Optimized multi-agent workflow with parallel execution

**Step-by-Step**:
1. **@strategic-task-planner**: Initial analysis and planning
2. **@strategic-task-planner**: Recognizes complexity, escalates to leverage-ai-agents
3. **@leverage-ai-agents**: Designs optimal multi-agent coordination
4. *Then*: Execute with parallel work streams

**Example**:
```
User: "Build enterprise e-commerce with AI, analytics, and global support"

@strategic-task-planner: "This requires advanced coordination..."
@leverage-ai-agents: "Designing 3 parallel streams:
  Stream 1: Architecture → Backend → Database (sequential)
  Stream 2: AI/ML → Data pipeline (sequential)
  Stream 3: Frontend → Localization (sequential)
  Sync Point: Integration after all 3 streams complete"

Result: Efficient parallel execution reducing timeline by 40%
```

### Scenario 3: Missing Specialized Expertise
**Situation**: Need domain expertise not covered by existing agents
**Agent Sequence**: `@strategic-task-planner → @auto-agent-generator`
**Timeline**: 20-40 minutes
**Outcome**: New specialized agent created and integrated

**Example**:
```
User: "Need blockchain smart contract development"

@strategic-task-planner: "No existing agent covers this. Engaging generator..."
@auto-agent-generator: "Creating blockchain-development-specialist agent
with expertise in: Solidity, Web3, DeFi protocols, gas optimization..."

Result: New agent ready for immediate use
```

### Scenario 4: Product Strategy & Planning
**Situation**: Need product-level planning before technical execution
**Agent Sequence**: `@product-manager → @strategic-task-planner`
**Timeline**: 1-2 hours
**Outcome**: Product requirements and technical execution plan

**Example**:
```
User: "Plan a new SaaS product for team collaboration"

@product-manager: "Defining product strategy, features, target market..."
@strategic-task-planner: "Converting product requirements into technical plan..."

Result: Product roadmap + technical execution strategy
```

---

## Usage Patterns

### Pattern 1: Simple Sequential Coordination

```mermaid
graph LR
    A[User Request] --> B[@strategic-task-planner]
    B --> C[@specialist-1]
    C --> D[@specialist-2]
    D --> E[@specialist-3]
    E --> F[Completion]
```

**Best For**: Traditional projects with clear dependencies
**Timeline**: Days to weeks depending on scope
**Success Criteria**: Each agent completes before next begins

**Real-World Example**:
```
Project: Company website redesign

@strategic-task-planner → Plans 4-phase approach
@ui-ux-designer → New designs
@frontend-ux-expert → Implementation
@web-security-specialist → Security review
@devops-infrastructure-specialist → Deployment

Timeline: 2 weeks
Result: Redesigned website live with security compliance
```

### Pattern 2: Complex Parallel Coordination

```mermaid
graph TD
    A[User Request] --> B[@strategic-task-planner]
    B --> C{Complexity Check}
    C -->|Complex| D[@leverage-ai-agents]
    D --> E[Stream 1: Architecture]
    D --> F[Stream 2: Data & AI]
    D --> G[Stream 3: Frontend]
    E --> H[Integration Point]
    F --> H
    G --> H
    H --> I[Completion]
```

**Best For**: Enterprise projects, multi-domain systems
**Timeline**: Weeks to months
**Success Criteria**: Parallel streams complete and integrate successfully

**Real-World Example**:
```
Project: AI-powered e-commerce platform

@strategic-task-planner → Initial analysis
@leverage-ai-agents → Designs 3 parallel streams:

Stream 1 (Backend):
  @system-architecture-designer
  @backend-architect
  @database-implementation-specialist

Stream 2 (AI):
  @data-engineering-specialist
  @ai-ml-specialist
  @mlops-engineer

Stream 3 (Frontend):
  @ui-ux-designer
  @frontend-ux-expert
  @localization-specialist

Integration: All streams merge for testing and deployment

Timeline: 8 weeks
Result: Full-featured AI e-commerce platform with 40% faster delivery
```

### Pattern 3: Iterative Planning & Execution

```mermaid
graph LR
    A[User Request] --> B[@strategic-task-planner]
    B --> C[Execute Phase 1]
    C --> D[Review & Adjust]
    D --> B
    B --> E[Execute Phase 2]
    E --> F[Final Delivery]
```

**Best For**: Exploratory projects, R&D, evolving requirements
**Timeline**: Variable, with regular checkpoints
**Success Criteria**: Continuous improvement and adaptation

---

## Integration with Other Categories

### Coordination → All Other Categories
**Flow**: Coordination agents analyze requirements → Select specialists → Orchestrate execution

**Examples**:
- Coordination → Core Technical (most common)
- Coordination → Data & Intelligence (AI projects)
- Coordination → User Experience (design-heavy projects)
- Coordination → Security & Operations (infrastructure projects)

### Escalation Patterns

**strategic-task-planner → leverage-ai-agents**:
- When: 4+ agents, parallel workflows, complex dependencies
- Handoff: Complete strategic plan with identified complexity
- Result: Optimized multi-agent coordination

**strategic-task-planner → auto-agent-generator**:
- When: Required expertise not available in ecosystem
- Handoff: Gap analysis with expertise requirements
- Result: New specialized agent created

---

## Success Criteria

### For strategic-task-planner
- [ ] Requirements clearly understood and documented
- [ ] All dependencies identified
- [ ] Optimal agent sequence selected
- [ ] Timeline and milestones defined
- [ ] Risk mitigation strategies in place
- [ ] Success criteria established

### For leverage-ai-agents
- [ ] Parallel work streams identified and optimized
- [ ] Agent coordination workflows designed
- [ ] Synchronization points defined
- [ ] Performance optimization achieved
- [ ] Quality gates established across streams

### For auto-agent-generator
- [ ] New agent created following ecosystem standards
- [ ] Integration with existing agents documented
- [ ] Agent .mdc file under 400 lines
- [ ] Proper category placement
- [ ] Documentation updated

### Overall Coordination Success
- [ ] Right agents selected for the task
- [ ] Efficient workflow (no bottlenecks)
- [ ] Clear communication between agents
- [ ] Quality maintained throughout
- [ ] Project delivered on timeline

---

## Common Issues & Solutions

### Issue 1: Not Sure Where to Start
**Symptom**: Have project idea but overwhelmed by 48 agents

**Solution**:
1. Always start with `@strategic-task-planner`
2. Describe your project in plain language
3. Let the planner analyze and create execution strategy
4. Follow the recommended agent sequence

**Example**:
```
Instead of: "Which agents do I need for my app?"
Do this: "@strategic-task-planner: I want to build a mobile fitness tracking app"
Result: Clear plan with agent sequence and timeline
```

### Issue 2: Project More Complex Than Expected
**Symptom**: Started simple but requirements growing

**Solution**:
1. Pause current work
2. Engage `@strategic-task-planner` for reassessment
3. May escalate to `@leverage-ai-agents` for complex coordination
4. Get updated plan before continuing

### Issue 3: Agent Coordination Breaks Down
**Symptom**: Agents not working together smoothly

**Solution**:
1. Return to coordination agent for review
2. Check workspace protocols being followed
3. Verify handoffs include complete context
4. May need `@leverage-ai-agents` for workflow optimization

### Issue 4: Missing Specialized Knowledge
**Symptom**: None of the 48 agents cover your specific domain

**Solution**:
1. Engage `@auto-agent-generator`
2. Describe required expertise clearly
3. New agent created in 10-20 minutes
4. Continue with expanded agent ecosystem

---

## Best Practices

1. **Always Start with Coordination**: Don't guess which specialist to use - let `@strategic-task-planner` analyze and recommend

2. **Trust the Escalation Process**: If strategic-task-planner escalates to leverage-ai-agents, there's good reason - accept the coordination upgrade

3. **Provide Complete Context**: Give coordinators full project context upfront - better planning with complete information

4. **Follow the Plan**: Once you have an execution plan, follow it sequentially - resist urge to skip ahead

5. **Use Milestones**: Break large projects into phases with clear milestones and quality gates

6. **Document Progress**: Keep clear notes as you move between agents - helps with handoffs and future sessions

7. **Ask for Clarification**: If plan unclear or seems wrong, ask coordinator to explain before executing

---

## Quick Reference

### When to Use Each Agent

| Your Need | Use This Agent |
|-----------|----------------|
| Start any multi-step project | @strategic-task-planner |
| Complex project (4+ agents) | @strategic-task-planner → @leverage-ai-agents |
| Missing specialized expertise | @auto-agent-generator |
| Product strategy & planning | @product-manager |
| Web server project management | @web-server-pm |

### Decision Tree

```
Need help? → @strategic-task-planner
  ├─ Simple (1-3 agents)? → strategic-task-planner handles
  └─ Complex (4+ agents)? → strategic-task-planner escalates to @leverage-ai-agents

Missing expertise? → @auto-agent-generator

Product planning? → @product-manager → @strategic-task-planner

Web/API project? → @web-server-pm + technical agents
```

### Typical Timelines
- **Simple project planning**: 15-30 minutes
- **Complex coordination design**: 30-60 minutes
- **New agent generation**: 10-20 minutes
- **Product strategy session**: 1-2 hours

---

## Examples

### Example 1: Building a Portfolio Website
**Complexity**: Simple
**Coordinator**: @strategic-task-planner only

```
@strategic-task-planner: "Build a personal portfolio website"

Plan:
1. @ui-ux-designer: Design layouts and branding
2. @frontend-ux-expert: Implement responsive site
3. @web-performance-specialist: Optimize performance
4. @devops-infrastructure-specialist: Deploy

Timeline: 3-5 days
Result: Professional portfolio site live
```

### Example 2: Enterprise SaaS Platform
**Complexity**: High
**Coordinators**: strategic-task-planner → leverage-ai-agents

```
@strategic-task-planner: "Build enterprise project management SaaS"
@strategic-task-planner: "Escalating to @leverage-ai-agents for complex coordination"

@leverage-ai-agents: "Designing 4 parallel streams:

Stream 1 - Architecture (Week 1-2):
  @system-architecture-designer → @cloud-architecture-specialist

Stream 2 - Backend (Week 2-4):
  @backend-architect → @database-implementation-specialist → @api-design-specialist

Stream 3 - Frontend (Week 3-5):
  @ui-ux-designer → @frontend-ux-expert → @accessibility-specialist

Stream 4 - DevOps (Week 1-6):
  @devops-infrastructure-specialist → @monitoring-observability-specialist

Integration Point (Week 6):
  @qa-reliability-engineer → @production-validation-specialist

Timeline: 6 weeks with parallel execution (vs 12 weeks sequential)
Result: Enterprise SaaS platform delivered in half the time
```

### Example 3: AI Recommendation Engine
**Complexity**: Moderate with specialized need
**Coordinators**: strategic-task-planner + auto-agent-generator

```
@strategic-task-planner: "Build recommendation engine for art gallery"

Analysis: Requires art domain + AI expertise

@auto-agent-generator: Creating art-recommendation-specialist

Updated Plan:
1. @data-engineering-specialist: Data pipeline
2. @ai-ml-specialist: Base recommendation model
3. @art-recommendation-specialist: Art-specific optimization
4. @mlops-engineer: Deployment

Timeline: 3-4 weeks
Result: Art-specific recommendation engine with 30% better accuracy
```

---

*For detailed coordination patterns, see [`agent-coordination-guide.md`](../../docs/agent-coordination-guide.md)*
*For quick start guide, see [`quick-start-guide.md`](../../docs/quick-start-guide.md)*
