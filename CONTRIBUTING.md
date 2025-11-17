# Contributing to AI Agent Ecosystem

Thank you for your interest in improving the AI Agent Ecosystem! This document provides guidelines for contributing new agents, improving existing agents, and enhancing documentation.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Creating New Agents](#creating-new-agents)
- [Improving Existing Agents](#improving-existing-agents)
- [Documentation](#documentation)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

We expect all contributors to:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs
1. Check if the issue already exists in GitHub Issues
2. Create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Cursor version, etc.)
   - Relevant agent .mdc file

### Suggesting Enhancements
1. Open a GitHub Discussion or Issue
2. Describe the enhancement and use case
3. Explain why it benefits the community
4. Consider implementation approach

### Creating Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes following our guidelines
4. Test thoroughly
5. Commit with clear messages
6. Push and create Pull Request

## Creating New Agents

### When to Create a New Agent

**Create a new agent when**:
- Specialized domain expertise not covered by existing agents
- Distinct, non-overlapping responsibility area
- Sufficient complexity to warrant dedicated agent (not a simple task)

**DON'T create a new agent if**:
- Existing agent can handle with minor enhancement
- Responsibility overlaps significantly with existing agent
- Task is too narrow (can be handled as part of larger agent)

### Agent Creation Process

#### Step 1: Use Auto-Agent-Generator (Recommended)
```
@auto-agent-generator: Create a [domain]-specialist agent for [specific expertise]
```

The generator will:
- Create properly formatted .mdc file
- Follow ecosystem standards
- Integrate with coordination protocols
- Update documentation

#### Step 2: Manual Creation (Advanced)
If creating manually, follow this structure:

**File Location**: `agents/[category]/[agent-name].mdc`

**Required Frontmatter**:
```yaml
---
name: agent-name
description: Primary capability, secondary capability, tertiary capability, and quaternary capability
globs:
alwaysApply: false
---
```

**Description Format**:
- Use **Simple pattern**: List 3-5 key capabilities separated by commas
- Length: 50-150 characters (concise but informative)
- Action-oriented: Focus on what the agent DOES
- Specific: Include concrete technologies, methodologies, or outcomes
- NO "USE WHEN": Let capabilities speak for themselves

**Examples**:
```yaml
# Technical Implementation
description: API design and implementation, REST/GraphQL endpoints, documentation generation, and integration testing

# Strategic/Analysis
description: System architecture design, technology stack evaluation, scalability planning, and architectural pattern establishment

# Business/Domain
description: E-commerce platform development, payment integration, shopping cart systems, and order management
```

**Required Sections**:
1. Opening paragraph: Expertise statement with mission
2. WORKSPACE MANAGEMENT PROTOCOL
3. Agent-specific expertise areas
4. Coordination patterns
5. Quality standards
6. Advanced capabilities (if applicable)

**See**: `agents/coordination/STREAMLINED_AGENT_TEMPLATE.md` for complete template

### Agent Quality Standards

All agents must:
- ✅ Have distinct, non-overlapping specialization
- ✅ Include mandatory identifier in communication protocol
- ✅ Reference WORKSPACE_PROTOCOLS.md
- ✅ Reference TEAM_COLLABORATION_CULTURE.md
- ✅ Follow streamlined file creation guidelines
- ✅ Document coordination patterns with other agents
- ✅ Include quality assurance standards
- ✅ Maintain professional, expert tone
- ✅ Be comprehensive but focused
- ✅ **Stay under 400 lines for optimal Cursor performance**

### Critical Constraint: File Length

**All .mdc files MUST stay under 400 lines**. This ensures:
- Fast Cursor IDE loading
- Efficient token usage
- Better performance
- Easier maintenance

If your agent needs more content:
- Keep core instructions in .mdc file (under 400 lines)
- Create companion `agent-name.README.md` for detailed examples
- Add usage patterns to category README

### Category Selection

Place agents in appropriate category:
- **coordination**: Orchestration and meta-coordination
- **core-technical**: Fundamental software development
- **data-intelligence**: Data processing and AI/ML
- **security-operations**: Security, deployment, reliability
- **user-experience**: UI/UX and communication
- **business-marketing**: Business value and marketing
- **specialized-domains**: Industry-specific expertise

If creating new category, discuss with maintainers first.

## Improving Existing Agents

### Enhancement Guidelines

When improving agents:
1. Read entire agent file to understand scope
2. Ensure changes align with agent's core mission
3. Don't add responsibilities that overlap other agents
4. Update references if changing protocols
5. **Keep file under 400 lines** - if adding content would exceed limit, create companion README instead
6. Test changes in real scenarios
7. Update documentation if behavior changes

### Common Improvements
- Clarifying expertise descriptions
- Improving communication protocols
- Adding coordination patterns
- Updating technology recommendations
- Enhancing quality standards
- **Do NOT**: Add usage examples to .mdc (put in README)
- **Do NOT**: Add troubleshooting to .mdc (put in category README)

## Documentation

### README Improvements

**Main README**: Ecosystem-level changes
- Update table of contents if adding sections
- Keep FAQ and troubleshooting current
- Add new workflow patterns

**Category READMEs**: Category-specific patterns
- Expand with usage examples
- Add troubleshooting for category
- Include visual workflows
- Document integration patterns

**Individual Agent READMEs** (agent-name.README.md):
- Detailed usage examples
- Troubleshooting specific to agent
- Integration patterns
- Best practices
- Code samples

### Documentation Standards
- Use clear, concise language
- Include examples for complex concepts
- Add visual aids where helpful
- Keep documentation in sync with implementation
- Follow markdown best practices
- Use consistent formatting

## Testing

### Agent Testing Process
1. Install agent using installation script
2. Test with @agent-name in Cursor
3. Verify agent responds with correct identifier
4. Test coordination with related agents
5. Validate deliverables match documentation
6. Test edge cases and error scenarios

### Integration Testing
- Test agent in realistic project scenarios
- Verify handoffs to/from other agents
- Check workspace management compliance
- Validate progress updates

## Submitting Changes

### Pull Request Process
1. Create descriptive PR title
2. Reference related issues
3. Describe changes clearly
4. List testing performed
5. Note any breaking changes
6. Update CHANGELOG if significant

### PR Template
```markdown
## Description
[Clear description of changes]

## Type of Change
- [ ] Bug fix
- [ ] New agent
- [ ] Agent enhancement
- [ ] Documentation
- [ ] Infrastructure

## Testing
- [ ] Tested agent independently
- [ ] Tested coordination with other agents
- [ ] Updated documentation
- [ ] No breaking changes (or documented)
- [ ] .mdc file stays under 400 lines

## Related Issues
Fixes #[issue number]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Tests added/updated
```

### Review Process
1. Automated checks run (linting, formatting)
2. Maintainer reviews changes
3. Feedback provided if changes needed
4. Approval and merge when ready

## Style Guidelines

### .mdc File Structure
```markdown
---
name: agent-name
description: One-line with USE WHEN (under 150 chars)
globs:
alwaysApply: false
---

[Opening paragraph] (2-3 sentences)

## WORKSPACE MANAGEMENT PROTOCOL
[Standard structure]

## Core Competencies
[Bullet point lists]

## Quality Standards
[Concise standards]

[Closing statement] (1-2 sentences)
```

### Writing Style
- Professional and expert tone
- Concise bullet points
- Clear section headers
- Actionable directives
- No redundant information
- Focus on "what" and "why", not lengthy "how"

### What Belongs Where

**In .mdc files** (for Cursor):
- ✅ Agent identity and role
- ✅ Core competencies (bullet points)
- ✅ Communication protocols
- ✅ Workspace management (references)
- ✅ Quality standards
- ❌ NOT: Detailed examples
- ❌ NOT: Troubleshooting scenarios
- ❌ NOT: Code samples
- ❌ NOT: Visual diagrams

**In README files** (for humans):
- ✅ Detailed usage examples
- ✅ Troubleshooting scenarios
- ✅ Integration patterns
- ✅ Visual workflows
- ✅ Code samples
- ✅ Best practices details

## Questions?

- Open a GitHub Discussion for questions
- Tag @maintainer for urgent issues
- Check existing documentation first

Thank you for contributing! 🎉

