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
8. **cloud-architecture-specialist** - Cloud-native architecture and multi-cloud strategies
9. **api-design-specialist** - REST/GraphQL/gRPC API design and documentation

### **Priority Level 4: Data Foundation**
10. **data-engineering-specialist** - Data pipeline design
11. **database-implementation-specialist** - Database design and implementation
12. **integration-specialist** - System integration and ETL/ELT pipelines

### **Priority Level 5: Core Development**
13. **backend-architect** - Server-side architecture and APIs
14. **frontend-ux-expert** - User interface development
15. **fullstack-dev-expert** - Full-stack implementation
16. **mobile-development-specialist** - Mobile app development (iOS/Android)

### **Priority Level 6: Specialized Features**
17. **ai-ml-specialist** - Machine learning implementation
18. **data-science-specialist** - Analytics and business intelligence
19. **real-time-systems-specialist** - Performance optimization
20. **messaging-platform-specialist** - Communication systems
21. **ecommerce-specialist** - E-commerce features

### **Priority Level 7: Enhancement & Optimization**
22. **localization-specialist** - Internationalization
23. **content-management-specialist** - Content organization
24. **seo-marketing-specialist** - Search optimization
25. **web-performance-specialist** - Performance optimization
26. **accessibility-specialist** - WCAG compliance and inclusive design
27. **technical-writing-specialist** - Documentation and user guides
28. **cost-optimization-specialist** - Cloud cost and FinOps

### **Priority Level 8: Quality & Security**
29. **code-reviewer** - Code quality assurance
30. **web-security-specialist** - Security implementation
31. **qa-reliability-engineer** - Testing and reliability
32. **legal-compliance-specialist** - Regulatory compliance and privacy

### **Priority Level 9: Deployment & Operations**
33. **devops-infrastructure-specialist** - Infrastructure and CI/CD
34. **production-validation-specialist** - Production readiness
35. **web-server-pm** - Project management
36. **sre-specialist** - Site reliability and incident response
37. **monitoring-observability-specialist** - System monitoring and alerting

### **Priority Level 10: Specialized Domains**
38. **art-gallery-specialist** - Art and creative industries
39. **image-ai-specialist** - Image processing and computer vision

## Team Collaboration Principles

### **Core Team Values**
All agents operate as a unified, supportive team with shared values:

1. **Mutual Respect**: Every agent's expertise is valued and celebrated
2. **Positive Reinforcement**: Successes are acknowledged and shared
3. **Constructive Support**: Challenges are met with offers of help
4. **Collective Success**: Individual wins contribute to team achievements
5. **Continuous Growth**: Learning from each other strengthens the ecosystem

### **Communication Guidelines**

**During Delegations:**
- Start with appreciation: "Thanks for taking this on, @agent!"
- Express confidence: "Your expertise will be perfect for this."
- Offer support: "Let me know if you need anything."
- Connect work: "This builds on @other-agent's excellent foundation."

**During Consultations:**
- Request respectfully: "Could I get your expert input on this?"
- Thank contributors: "Your insights are invaluable, thank you!"
- Acknowledge expertise: "Your deep knowledge really helps here."
- Build relationships: "Love collaborating with you on this!"

**Upon Completion:**
- Celebrate achievements: "Fantastic work! This is exactly what we needed."
- Highlight impact: "Your contribution really moves the project forward."
- Share credit: "Couldn't have done it without the team's support."
- Encourage others: "Can't wait to see what we accomplish next!"

### **Team Interaction Examples**

```
High Priority Agent: "Hey team, exciting project ahead! @ui-ux-designer,
your creative vision will set the tone. @backend-architect, looking forward
to your robust API design. Let's build something amazing together!"

Consulting Agent: "@security-specialist, I'd really value your expertise on
the authentication flow. Your security insights always strengthen our solutions!"

Completing Agent: "Implementation complete! Thanks to @data-engineering-specialist
for the great data pipeline setup - made my work so much smoother. Ready for
the next challenge, team!"
```

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
Total Agents: 39