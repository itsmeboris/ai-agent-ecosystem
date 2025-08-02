# AI Agent Ecosystem Hierarchy

## Agent Priority & Execution Order

This document defines the hierarchical priority order for agent execution when multiple agents are involved in a task. Agents are organized by priority level (1 being highest) and execution sequence within each level.

### **Priority Level 1: Coordination & Planning**
1. **strategic-task-planner** - Primary orchestrator, always executes first
2. **leverage-ai-agents** - Meta-coordinator for multi-agent workflows
3. **auto-agent-generator** - Agent creation when specialized capabilities needed

### **Priority Level 2: Research & Requirements**
4. **web-search-specialist** - Market research and competitive intelligence
5. **documentation-research-specialist** - Technical documentation and knowledge gathering

### **Priority Level 3: Architecture & Design**
6. **system-architecture-designer** - High-level system design
7. **ui-ux-designer** - User interface design and experience architecture

### **Priority Level 4: Data Foundation**
8. **data-engineering-specialist** - Data pipeline design
9. **database-implementation-specialist** - Database design and implementation

### **Priority Level 5: Core Development**
10. **backend-architect** - Server-side architecture and APIs
11. **frontend-ux-expert** - User interface development
12. **fullstack-dev-expert** - Full-stack implementation

### **Priority Level 6: Specialized Features**
13. **ai-ml-specialist** - Machine learning implementation
14. **data-science-specialist** - Analytics and business intelligence
15. **real-time-systems-specialist** - Performance optimization
16. **messaging-platform-specialist** - Communication systems
17. **ecommerce-specialist** - E-commerce features

### **Priority Level 7: Enhancement & Optimization**
18. **localization-specialist** - Internationalization
19. **content-management-specialist** - Content organization
20. **seo-marketing-specialist** - Search optimization
21. **web-performance-specialist** - Performance optimization

### **Priority Level 8: Quality & Security**
22. **code-reviewer** - Code quality assurance
23. **web-security-specialist** - Security implementation
24. **qa-reliability-engineer** - Testing and reliability

### **Priority Level 9: Deployment & Operations**
25. **devops-infrastructure-specialist** - Infrastructure and CI/CD
26. **production-validation-specialist** - Production readiness
27. **web-server-pm** - Project management

### **Priority Level 10: Specialized Domains**
28. **art-gallery-specialist** - Art and creative industries
29. **image-ai-specialist** - Image processing and computer vision

## Execution Rules

### **Sequential Execution**
When agents are assigned sequentially:
1. Follow the priority order above
2. Complete higher priority agent tasks before lower priority
3. Within same priority level, execute in listed order
4. Wait for completion signals before switching personas

### **Concurrent Execution**
When agents work in parallel:
1. Identify independent work streams
2. Group agents by dependencies
3. Execute highest priority agent in each stream
4. Merge results at synchronization points

### **Persona Switching Protocol**
1. Save current context to workspace
2. Load new agent persona and workspace
3. Execute assigned tasks
4. Document completion in SHARED_PROGRESS.md
5. Return to coordination agent or next in sequence

### **Consultation Protocol**
Agents can consult other specialists without full persona switching:

1. **Lead agent** maintains primary task ownership
2. **Consultant agent** provides focused expertise
3. **Format**: `[CONSULT] agent-name: "specific recommendation"`
4. **Documentation**: Record consultations in lead agent's workspace
5. **Context**: Lead agent incorporates advice and continues

**Common Consultation Patterns:**
- Technical agents consult `web-security-specialist` for security concerns
- All agents consult `code-reviewer` for quality assurance
- Business agents consult `web-search-specialist` for market intelligence
- Frontend agents consult `ui-ux-designer` for design decisions
- Data agents consult `ai-ml-specialist` for ML recommendations

### **Dynamic Priority Adjustment**
Priorities can be adjusted based on:
- Project-specific requirements
- Critical path dependencies
- Resource availability
- Time constraints

## Maintenance

This hierarchy must be updated when:
- New agents are created by auto-agent-generator
- Agent capabilities significantly change
- New priority patterns emerge from usage

Last Updated: [Current Date]
Total Agents: 29