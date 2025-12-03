# AI Agent Ecosystem Repository Structure

*Last Updated: November 30, 2025 - Version 2.1.0*

## Overview

This repository contains 48 specialized AI agents (v2.1.0) with comprehensive capability definitions, coordination protocols, automation tools, and supporting documentation.

## Directory Structure

```
ai-agent-ecosystem/
├── agents/                          # 48 specialized AI agents (v2.1.0)
│   ├── coordination/                # 5 coordination agents
│   │   ├── strategic-task-planner.mdc
│   │   ├── leverage-ai-agents.mdc
│   │   ├── auto-agent-generator.mdc
│   │   ├── product-manager.mdc
│   │   ├── web-server-pm.mdc
│   │   ├── AGENT_DIRECTORY.md           # Complete agent catalog
│   │   ├── AGENT_HIERARCHY.md           # Priority-based execution order
│   │   ├── WORKSPACE_PROTOCOLS.md       # Workspace management standards
│   │   ├── TEAM_COLLABORATION_CULTURE.md # Communication guidelines
│   │   ├── STRUCTURED_OUTPUT_FORMATS.md  # Output format specifications
│   │   ├── ERROR_HANDLING_PROTOCOL.md    # Error handling system
│   │   ├── CAPABILITY_DISCOVERY.md       # Agent discovery system
│   │   ├── TOKEN_EFFICIENCY.md           # Lazy loading architecture
│   │   └── README.md                     # Coordination category overview
│   │
│   ├── core-technical/              # 12 core technical agents
│   │   ├── backend-architect.mdc
│   │   ├── frontend-ux-expert.mdc
│   │   ├── fullstack-dev-expert.mdc
│   │   ├── system-architecture-designer.mdc
│   │   ├── cloud-architecture-specialist.mdc
│   │   ├── api-design-specialist.mdc
│   │   ├── database-implementation-specialist.mdc
│   │   ├── mobile-development-specialist.mdc
│   │   ├── platform-engineer.mdc
│   │   ├── code-reviewer.mdc
│   │   ├── prompt-engineer.mdc
│   │   ├── developer-experience-engineer.mdc
│   │   └── README.md
│   │
│   ├── data-intelligence/           # 7 data and AI agents
│   │   ├── ai-ml-specialist.mdc
│   │   ├── data-engineering-specialist.mdc
│   │   ├── data-science-specialist.mdc
│   │   ├── mlops-engineer.mdc
│   │   ├── real-time-systems-specialist.mdc
│   │   ├── integration-specialist.mdc
│   │   ├── ai-ethics-governance-specialist.mdc
│   │   └── README.md
│   │
│   ├── security-operations/         # 7 security and operations agents
│   │   ├── web-security-specialist.mdc
│   │   ├── devops-infrastructure-specialist.mdc
│   │   ├── sre-specialist.mdc
│   │   ├── qa-reliability-engineer.mdc
│   │   ├── web-performance-specialist.mdc
│   │   ├── monitoring-observability-specialist.mdc
│   │   ├── production-validation-specialist.mdc
│   │   └── README.md
│   │
│   ├── user-experience/             # 7 UX and content agents
│   │   ├── ui-ux-designer.mdc
│   │   ├── accessibility-specialist.mdc
│   │   ├── content-management-specialist.mdc
│   │   ├── technical-writing-specialist.mdc
│   │   ├── localization-specialist.mdc
│   │   ├── messaging-platform-specialist.mdc
│   │   ├── developer-relations-engineer.mdc
│   │   └── README.md
│   │
│   ├── business-marketing/          # 8 business and marketing agents
│   │   ├── business-analyst.mdc
│   │   ├── ecommerce-specialist.mdc
│   │   ├── seo-marketing-specialist.mdc
│   │   ├── web-search-specialist.mdc
│   │   ├── documentation-research-specialist.mdc
│   │   ├── legal-compliance-specialist.mdc
│   │   ├── cost-optimization-specialist.mdc
│   │   ├── solutions-engineer.mdc
│   │   └── README.md
│   │
│   ├── specialized-domains/         # 2 specialized domain agents
│   │   ├── art-gallery-specialist.mdc
│   │   ├── image-ai-specialist.mdc
│   │   └── README.md
│   │
│   └── summaries/                   # 48 agent summaries (auto-generated)
│       ├── *.summary.yaml           # Lightweight agent summaries (~250 tokens each)
│       └── README.md                # Summary generation documentation
│
├── templates/                       # Agent creation templates
│   ├── agent_template.mdc           # Main agent structure with placeholders
│   ├── specialist_checklist.yaml   # Execution checklist for specialist agents
│   └── coordinator_checklist.yaml  # Execution checklist for coordinator agents
│
├── tools/                           # Automation and analysis tools
│   ├── capability_discovery.py      # Intelligent agent selection engine
│   ├── lazy_loader.py               # Token-efficient lazy loading system
│   ├── generate_summaries.py        # Agent summary generator
│   ├── parse-progress.py            # Progress tracking parser
│   ├── error_handling.py            # Error handling utilities
│   ├── analyze-progress.sh          # Quick progress analysis
│   └── validate-progress.sh         # Format validation
│
├── docs/                            # Documentation
│   ├── README.md                    # Documentation navigation
│   ├── agent-best-practices.md      # Agent design guidelines
│   ├── agent-coordination-guide.md  # Coordination methodologies
│   └── quick-start-guide.md         # Getting started guide
│
├── examples/                        # Usage examples
│   ├── ecommerce-platform-example.md
│   └── simple-portfolio-website.md
│
├── commands/                        # Cursor custom commands
│   ├── README.md                    # Command documentation
│   ├── add-tests.md                 # Test generation command
│   ├── code-review.md               # Code review command
│   ├── generate-api-docs.md         # API documentation command
│   ├── optimize-performance.md      # Performance optimization command
│   └── security-audit.md            # Security audit command
│
├── hooks/                           # Cursor automation hooks
│   ├── README.md                    # Hooks documentation
│   ├── hooks.json                   # Hooks configuration
│   ├── automation/                  # Automation workflow hooks
│   ├── execution/                   # Execution lifecycle hooks
│   └── workspace/                   # Workspace management hooks
│
├── workspaces/                      # Agent workspace (created at runtime)
│   ├── SHARED_PROGRESS.md           # Centralized progress tracking
│   ├── .checkpoints/                # Checkpoint storage for recovery
│   └── .logs/                       # Error handling logs
│
├── README.md                        # Main documentation
├── STRUCTURE.md                     # This file - repository structure
├── INSTALLATION_GUIDE.md            # Platform-specific installation instructions
├── QUICK_REFERENCE.md               # Quick command reference
├── CHANGELOG.md                     # Version history and changes
├── CONTRIBUTING.md                  # Contribution guidelines
├── IMPROVEMENTS_SUMMARY.md          # Detailed v2.0.0 improvement documentation
├── LICENSE                          # MIT License
├── install-agents.py                # Python installation script
└── install-agents.sh                # Shell installation script
```

## File Statistics

- **Total Agents**: 48 (.mdc files) at version 2.1.0
- **Agent Summaries**: 48 (.summary.yaml files)
- **Protocol Documents**: 9 coordination protocols
- **Tools**: 7 automation and analysis utilities
- **Custom Commands**: 5 Cursor commands
- **Documentation Files**: ~25 markdown files
- **Total Lines of Code**: ~35,000 across all agents

## Key Components

### Agent Files (.mdc)
- **Format**: Markdown with YAML frontmatter
- **Version**: 2.1.0 (all agents updated)
- **Features**: Comprehensive capability definitions, specializations, technologies, methodologies
- **Size**: ~300-800 lines per agent

### Agent Summaries (.summary.yaml)
- **Purpose**: Token-efficient agent discovery
- **Size**: ~250 tokens per summary (vs ~1000 tokens for full agent)
- **Generation**: Automated via `tools/generate_summaries.py`
- **Savings**: 93% token reduction with lazy loading

### Protocol Documents
- **WORKSPACE_PROTOCOLS.md**: Workspace management standards
- **TEAM_COLLABORATION_CULTURE.md**: Communication guidelines
- **STRUCTURED_OUTPUT_FORMATS.md**: Three output format options
- **ERROR_HANDLING_PROTOCOL.md**: Three-tier error handling system
- **CAPABILITY_DISCOVERY.md**: Intelligent agent selection system
- **TOKEN_EFFICIENCY.md**: Lazy loading architecture
- **AGENT_HIERARCHY.md**: Priority-based execution order
- **AGENT_DIRECTORY.md**: Complete agent catalog

### Templates
- **agent_template.mdc**: Main agent structure with placeholders
- **specialist_checklist.yaml**: Execution checklist for specialist agents
- **coordinator_checklist.yaml**: Execution checklist for coordinator agents

### Tools
- **capability_discovery.py**: Find agents by requirements, build teams
- **lazy_loader.py**: Load agents progressively to save tokens
- **generate_summaries.py**: Auto-generate agent summaries
- **parse-progress.py**: Parse and analyze progress tracking
- **error_handling.py**: Reusable error handling utilities
- **analyze-progress.sh**: Quick shell-based progress analysis
- **validate-progress.sh**: Validate progress format compliance

### Installation Scripts
- **install-agents.py**: Python-based installer (recommended)
  - Platform detection (Cursor, Claude Code, Claude Desktop)
  - Selective installation by category
  - Automatic summary generation
  - Verification and validation
- **install-agents.sh**: Shell-based installer (legacy)
  - Basic installation functionality
  - Compatible with all Unix-like systems

## Agent Categories

| Category | Count | Purpose |
|----------|-------|---------|
| **Coordination** | 5 | Orchestration and project management |
| **Core Technical** | 12 | Software development fundamentals |
| **Data Intelligence** | 7 | Data processing and AI/ML |
| **Security Operations** | 7 | Security, deployment, reliability |
| **User Experience** | 7 | UI/UX and communication |
| **Business Marketing** | 8 | Business value and marketing |
| **Specialized Domains** | 2 | Industry-specific expertise |
| **Total** | **48** | Complete ecosystem |

## Version History

### v2.1.0 (Current - November 30, 2025)
- ✅ Added comprehensive capability definitions to all 48 agents
- ✅ Standardized version field across all agents
- ✅ Enhanced agent relationships and dependencies
- ✅ Added operational parameters (consultation, parallel tasks, duration)
- ✅ Defined technologies and methodologies for each agent
- ✅ Full capability discovery support

### v2.0.0 (November 17, 2025)
- ✅ Standardized agent descriptions
- ✅ Added focus principles and consultation patterns
- ✅ Implemented structured output formats
- ✅ Added error handling protocols
- ✅ Introduced token efficiency via lazy loading
- ✅ Created agent summaries system

### v1.0.0 (Initial Release)
- ✅ 48 specialized AI agents
- ✅ Basic coordination architecture
- ✅ Workspace management protocols
- ✅ Documentation and examples

## Platform Compatibility

### Supported Platforms
- **Cursor** (`.mdc` files) - Full support with hooks and commands
- **Claude Code** (`.mdc` files) - Full support with tools
- **Claude Desktop** (`.md` converted) - Agent files only

### Platform-Specific Features

**Cursor**:
- ✅ All 48 agents
- ✅ Custom commands (5)
- ✅ Automation hooks (3 categories)
- ✅ Protocol documents
- ✅ Tools and utilities

**Claude Code**:
- ✅ All 48 agents
- ✅ Protocol documents
- ✅ Tools and utilities
- ⚠️ No custom commands (Cursor-specific)
- ⚠️ No automation hooks (Cursor-specific)

**Claude Desktop**:
- ✅ All 48 agents (converted to .md)
- ✅ Basic functionality
- ⚠️ Limited tooling support
- ⚠️ No platform-specific features

## Repository Maintenance

### Adding New Agents
1. Use `@auto-agent-generator` to create new agents
   - It reads `templates/agent_template.mdc`
   - Fills placeholders with agent-specific content
   - Writes completed agent to `agents/{category}/agent-name.mdc`
2. Agent is automatically placed in appropriate category directory
3. Update category README.md
4. Run `python3 tools/generate_summaries.py` to create summary
5. Update `AGENT_DIRECTORY.md` and `AGENT_HIERARCHY.md`
6. Update this file's agent count

### Updating Documentation
1. All documentation should reference current version (v2.1.0)
2. Update CHANGELOG.md for any significant changes
3. Keep STRUCTURE.md synchronized with actual structure
4. Run validation tools to ensure consistency

### Quality Standards
- All agents must have version 2.1.0
- All agents must have complete capability definitions
- All agents must have corresponding summaries
- All protocol references must be valid
- All file counts must be accurate

## See Also

- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Platform-specific installation
- [README.md](README.md) - Main documentation
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [docs/quick-start-guide.md](docs/quick-start-guide.md) - Getting started
- [docs/agent-best-practices.md](docs/agent-best-practices.md) - Agent design guide

---

*For questions or issues, please refer to the documentation or open an issue on GitHub.*
