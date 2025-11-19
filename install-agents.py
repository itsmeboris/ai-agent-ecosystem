#!/usr/bin/env python3
"""
AI Agent Ecosystem Installer

This script copies AI agents from the organized repository structure to your
IDE's agent directory for easy installation and management.

Supports both:
- Cursor (.cursor/rules directory, .mdc format with documentation files)
- Claude Desktop (.claude/agents directory, .md format with model field)

Documentation Files (Cursor only):
- AGENT_HIERARCHY.md (agent coordination hierarchy)
- WORKSPACE_PROTOCOLS.md (workspace management standards)
- TEAM_COLLABORATION_CULTURE.md (communication guidelines)
- AGENT_DIRECTORY.md (agent list and collaboration patterns)
- agent-coordination-guide.md (coordination methodologies)
- agent-best-practices.md (agent development standards)

Cursor Hooks (Cursor only):
- Workspace progress enforcement (afterAgentResponse)
- Command execution with output capture (beforeShellExecution)
- Auto-continuation of pending tasks (stop)

Usage:
    # Cursor installation (default)
    python install-agents.py ~/.cursor/rules --all
    python install-agents.py ~/.cursor/rules --category coordination
    python install-agents.py ~/.cursor/rules --all --skip-hooks

    # Claude Desktop installation (with --claude flag)
    python install-agents.py ~/.claude/agents --claude --all
    python install-agents.py ~/.claude/agents --claude --agents strategic-task-planner
"""

import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Dict

def get_script_directory() -> Path:
    """Get the directory where this script is located."""
    return Path(__file__).parent.absolute()

def get_agents_directory() -> Path:
    """Get the agents directory relative to the script location."""
    return get_script_directory() / 'agents'

def discover_agents() -> Dict[str, List[str]]:
    """Dynamically discover all agents by scanning the agents directory structure."""
    agents_dir = get_agents_directory()
    discovered_agents = {}

    if not agents_dir.exists():
        print(f"❌ Error: Agents directory not found at {agents_dir}")
        return {}

    # Scan each category directory
    for category_dir in agents_dir.iterdir():
        if category_dir.is_dir():
            category_name = category_dir.name
            agent_files = list(category_dir.glob('*.mdc'))
            discovered_agents[category_name] = [f.stem for f in agent_files]

    return discovered_agents

def get_agent_location(agent_name: str, available_agents: Dict[str, List[str]]) -> str:
    """Find which category directory contains the specified agent."""
    for category, agents in available_agents.items():
        if agent_name in agents:
            return category
    return None

def get_category_description(category: str) -> str:
    """Get category description from README or infer from name."""
    agents_dir = get_agents_directory()
    readme_file = agents_dir / category / "README.md"

    if readme_file.exists():
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                # Read first non-empty line as description
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        return line
        except Exception:
            pass

    # Fallback to category name formatting
    return category.replace('-', ' ').title()

def validate_target_directory(target_path: str, is_claude: bool = False) -> Path:
    """Validate and create target directory, with smart path suggestions."""
    target = Path(target_path).expanduser().resolve()

    # Check if path already has the expected structure
    expected_agent_dir = "agents" if is_claude else "rules"
    expected_parent_dir = ".claude" if is_claude else ".cursor"

    if target.name == expected_agent_dir and target.parent.name == expected_parent_dir:
        # Path is already correct
        try:
            target.mkdir(parents=True, exist_ok=True)
            return target
        except Exception as e:
            print(f"❌ Error: Cannot create target directory {target}: {e}")
            sys.exit(1)

    # Path doesn't match expected patterns - provide suggestions
    install_type_name = "Claude Desktop" if is_claude else "Cursor"
    print(f"⚠️  Warning: Target path doesn't match expected {install_type_name} structure")
    print(f"📁 Current path: {target}")
    print()
    print("What would you like to do?")

    # Smart suggestions based on current path and installation type
    if target.name == expected_parent_dir:
        # User provided ~/.cursor or ~/.claude - suggest adding the agent directory
        suggestion = target / expected_agent_dir
        print(f"1. Append '{expected_agent_dir}' to create: {suggestion} (Recommended)")
        print("2. Use the given directory as-is")
        print("3. Cancel installation")
        print()

        while True:
            try:
                choice = input("Enter your choice (1/2/3): ").strip()
                if choice == "1":
                    target = suggestion
                    print(f"✅ Updated target path: {target}")
                    break
                elif choice == "2":
                    print(f"✅ Using original path: {target}")
                    break
                elif choice == "3":
                    print("❌ Installation cancelled by user")
                    sys.exit(0)
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3")
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Installation cancelled by user")
                sys.exit(0)
        print()
    else:
        # User provided some other path - suggest adding full structure
        full_suggestion = target / expected_parent_dir / expected_agent_dir
        print(f"1. Append '{expected_parent_dir}/{expected_agent_dir}' to create: {full_suggestion} (Recommended)")
        print("2. Use the given directory as-is")
        print("3. Cancel installation")
        print()

        while True:
            try:
                choice = input("Enter your choice (1/2/3): ").strip()
                if choice == "1":
                    target = full_suggestion
                    print(f"✅ Updated target path: {target}")
                    break
                elif choice == "2":
                    print(f"✅ Using original path: {target}")
                    break
                elif choice == "3":
                    print("❌ Installation cancelled by user")
                    sys.exit(0)
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3")
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Installation cancelled by user")
                sys.exit(0)
        print()

    try:
        target.mkdir(parents=True, exist_ok=True)
        return target
    except Exception as e:
        print(f"❌ Error: Cannot create target directory {target}: {e}")
        sys.exit(1)

def convert_mdc_to_claude_format(content: str) -> str:
    """Convert .mdc format to Claude Desktop .md format."""
    lines = content.split('\n')
    result_lines = []
    in_frontmatter = False
    frontmatter_ended = False

    for line in lines:
        if line.strip() == '---' and not frontmatter_ended:
            if not in_frontmatter:
                in_frontmatter = True
                result_lines.append(line)
            else:
                # End of frontmatter - add model field before closing
                result_lines.append('model: sonnet')
                result_lines.append(line)
                frontmatter_ended = True
        elif in_frontmatter and not frontmatter_ended:
            # Skip globs and alwaysApply fields
            if not line.strip().startswith(('globs:', 'alwaysApply:')):
                result_lines.append(line)
        else:
            result_lines.append(line)

    return '\n'.join(result_lines)

def copy_agent(agent_name: str, source_category: str, target_dir: Path, install_type: str = "cursor") -> bool:
    """Copy a single agent from source to target directory, converting format if needed."""
    agents_dir = get_agents_directory()
    source_file = agents_dir / source_category / f"{agent_name}.mdc"

    if not source_file.exists():
        print(f"⚠️  Warning: Agent {agent_name} not found in {source_category}")
        return False

    try:
        if install_type == "claude":
            # Convert format for Claude Desktop
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            converted_content = convert_mdc_to_claude_format(content)
            target_file = target_dir / f"{agent_name}.md"

            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)

            print(f"✅ Copied {agent_name}.md (converted for Claude Desktop)")
        else:
            # Standard copy for Cursor
            target_file = target_dir / f"{agent_name}.mdc"
            shutil.copy2(source_file, target_file)
            print(f"✅ Copied {agent_name}.mdc")

        return True
    except Exception as e:
        extension = ".md" if install_type == "claude" else ".mdc"
        print(f"❌ Error copying {agent_name}{extension}: {e}")
        return False

def copy_documentation_files(target_dir: Path) -> dict:
    """Copy all required documentation files to target directory."""
    script_dir = get_script_directory()
    agents_dir = get_agents_directory()

    # Define required documentation files
    doc_files = {
        "AGENT_HIERARCHY.md": agents_dir / "coordination" / "AGENT_HIERARCHY.md",
        "WORKSPACE_PROTOCOLS.md": agents_dir / "coordination" / "WORKSPACE_PROTOCOLS.md",
        "TEAM_COLLABORATION_CULTURE.md": agents_dir / "coordination" / "TEAM_COLLABORATION_CULTURE.md",
        "AGENT_DIRECTORY.md": agents_dir / "coordination" / "AGENT_DIRECTORY.md",
        "agent-coordination-guide.md": script_dir / "docs" / "agent-coordination-guide.md",
        "agent-best-practices.md": script_dir / "docs" / "agent-best-practices.md"
    }

    results = {}

    for filename, source_file in doc_files.items():
        target_file = target_dir / filename

        if not source_file.exists():
            print(f"⚠️  Warning: {filename} not found at {source_file}")
            results[filename] = False
            continue

        try:
            shutil.copy2(source_file, target_file)
            print(f"✅ Copied {filename}")
            results[filename] = True
        except Exception as e:
            print(f"❌ Error copying {filename}: {e}")
            results[filename] = False

    return results

def copy_cursor_commands(base_dir: Path) -> int:
    """Copy custom Cursor commands to the commands directory."""
    script_dir = get_script_directory()
    commands_source_dir = script_dir / "commands"

    # Determine target commands directory
    # If base_dir is ~/.cursor/rules, commands go to ~/.cursor/commands
    cursor_parent = base_dir.parent
    target_commands_dir = cursor_parent / "commands"

    if not commands_source_dir.exists():
        print(f"⚠️  Warning: Commands directory not found at {commands_source_dir}")
        return 0

    # Create target commands directory
    try:
        target_commands_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"⚠️  Warning: Failed to create commands directory {target_commands_dir}: {e}")
        return 0

    commands_copied = 0

    # Copy all command files
    for command_file in commands_source_dir.glob("*.md"):
        target_file = target_commands_dir / command_file.name

        try:
            shutil.copy2(command_file, target_file)
            print(f"✅ Copied command: {command_file.name}")
            commands_copied += 1
        except Exception as e:
            print(f"❌ Error copying command {command_file.name}: {e}")

    return commands_copied

def copy_cursor_hooks(base_dir: Path) -> dict:
    """Copy Cursor hooks to enable automated workflow features."""
    script_dir = get_script_directory()
    hooks_source_dir = script_dir / "hooks"

    # Determine target directories
    # If base_dir is ~/.cursor/rules, hooks go to ~/.cursor/hooks and ~/.cursor/hooks.json
    cursor_parent = base_dir.parent
    target_hooks_dir = cursor_parent / "hooks"
    target_hooks_json = cursor_parent / "hooks.json"

    results = {
        'hooks_directory': False,
        'hooks_json': False,
        'scripts_count': 0
    }

    if not hooks_source_dir.exists():
        print(f"⚠️  Warning: Hooks directory not found at {hooks_source_dir}")
        return results

    # Create target hooks directory structure
    try:
        target_hooks_dir.mkdir(parents=True, exist_ok=True)
        (target_hooks_dir / "workspace").mkdir(exist_ok=True)
        (target_hooks_dir / "execution").mkdir(exist_ok=True)
        (target_hooks_dir / "automation").mkdir(exist_ok=True)
        results['hooks_directory'] = True
    except Exception as e:
        print(f"⚠️  Warning: Failed to create hooks directory {target_hooks_dir}: {e}")
        return results

    # Copy hook scripts
    hook_scripts = [
        ("workspace", "enforce-progress-update.sh"),
        ("execution", "command-executor.sh"),
        ("automation", "auto-continue.sh")
    ]

    for subdir, script_name in hook_scripts:
        source_file = hooks_source_dir / subdir / script_name
        target_file = target_hooks_dir / subdir / script_name

        if not source_file.exists():
            print(f"⚠️  Warning: Hook script not found: {script_name}")
            continue

        try:
            shutil.copy2(source_file, target_file)
            # Make script executable
            target_file.chmod(0o755)
            print(f"✅ Copied hook: {subdir}/{script_name}")
            results['scripts_count'] += 1
        except Exception as e:
            print(f"❌ Error copying hook {script_name}: {e}")

    # Copy hooks.json configuration
    source_hooks_json = hooks_source_dir / "hooks.json"
    if source_hooks_json.exists():
        try:
            shutil.copy2(source_hooks_json, target_hooks_json)
            print(f"✅ Copied hooks.json configuration")
            results['hooks_json'] = True
        except Exception as e:
            print(f"❌ Error copying hooks.json: {e}")
    else:
        print(f"⚠️  Warning: hooks.json not found at {source_hooks_json}")

    return results

def install_agents(target_dir: Path, install_type: str = "cursor", agent_list: List[str] = None, categories: List[str] = None, skip_commands: bool = False, skip_hooks: bool = False) -> None:
    """Install specified agents or all agents to target directory."""
    available_agents = discover_agents()

    if not available_agents:
        print("❌ No agents found in the repository")
        return

    # Always copy required documentation files first (only for Cursor)
    if install_type == "cursor":
        print("📋 Copying required documentation files...")
        doc_results = copy_documentation_files(target_dir)
        docs_copied = sum(doc_results.values())

        # Copy custom Cursor commands (unless skipped)
        if not skip_commands:
            print("\n⚡ Installing Cursor custom commands...")
            commands_copied = copy_cursor_commands(target_dir)
        else:
            print("ℹ️  Skipping Cursor custom commands (--skip-commands flag set)")
            commands_copied = 0

        # Copy Cursor hooks (unless skipped)
        if not skip_hooks:
            print("\n🪝 Installing Cursor hooks for workflow automation...")
            hooks_results = copy_cursor_hooks(target_dir)
        else:
            print("ℹ️  Skipping Cursor hooks (--skip-hooks flag set)")
            hooks_results = {'hooks_directory': False, 'hooks_json': False, 'scripts_count': 0}
    else:
        print("📋 Installing for Claude Desktop (documentation files not needed)...")
        doc_results = {}
        docs_copied = 0
        commands_copied = 0
        hooks_results = {'hooks_directory': False, 'hooks_json': False, 'scripts_count': 0}

    copied_count = 0
    total_count = 0

    # If specific agents are requested
    if agent_list:
        print(f"📋 Installing specific agents: {', '.join(agent_list)}")

        for agent_name in agent_list:
            source_category = get_agent_location(agent_name, available_agents)
            if source_category:
                if copy_agent(agent_name, source_category, target_dir, install_type):
                    copied_count += 1
                total_count += 1
            else:
                print(f"⚠️  Warning: Agent {agent_name} not found in any category")
                total_count += 1

    # If specific categories are requested
    elif categories:
        print(f"📋 Installing agent categories: {', '.join(categories)}")

        for category in categories:
            if category not in available_agents:
                print(f"⚠️  Warning: Category '{category}' not found")
                continue

            if not available_agents[category]:
                print(f"⚠️  Warning: No agents found in category '{category}'")
                continue

            print(f"\n📂 Installing {category} agents:")
            for agent_name in available_agents[category]:
                if copy_agent(agent_name, category, target_dir, install_type):
                    copied_count += 1
                total_count += 1

    # Install all agents
    else:
        print("📋 Installing all available agents...")

        for category, agents in available_agents.items():
            if agents:
                print(f"\n📂 Installing {category} agents:")
                for agent_name in agents:
                    if copy_agent(agent_name, category, target_dir, install_type):
                        copied_count += 1
                    total_count += 1

    # Summary
    print(f"\n🎯 Installation Summary:")
    print(f"   ✅ Successfully copied: {copied_count} agents")
    print(f"   ✅ Documentation files: {docs_copied}/6 copied successfully")
    if install_type == "cursor" and commands_copied > 0:
        print(f"   ✅ Cursor commands: {commands_copied} custom commands installed")
    if install_type == "cursor" and hooks_results['scripts_count'] > 0:
        print(f"   ✅ Cursor hooks: {hooks_results['scripts_count']}/3 hooks installed")
    if total_count > copied_count:
        print(f"   ⚠️  Failed or skipped: {total_count - copied_count} agents")
    print(f"   📁 Target directory: {target_dir}")

    if copied_count > 0:
        print(f"\n🚀 Ready to use! Restart your IDE to load the new agents.")
        print(f"   Test with: @strategic-task-planner: Hello")
        if doc_results.get("AGENT_HIERARCHY.md", False):
            print(f"   📋 Agent coordination enabled with full documentation support")
            print(f"   📖 Coordination guide: See agent-coordination-guide.md")
        if install_type == "cursor" and commands_copied > 0:
            print(f"\n⚡ Cursor Commands Ready:")
            print(f"   • Type / in Cursor chat to see available commands")
            print(f"   • Try: /code-review @yourfile.ts")
            print(f"   • Available commands: code-review, add-tests, security-audit,")
            print(f"     optimize-performance, generate-api-docs")
        if install_type == "cursor" and hooks_results['scripts_count'] > 0:
            print(f"\n🪝 Cursor Hooks Enabled:")
            print(f"   • afterAgentResponse: Enforces workspace progress updates")
            print(f"   • beforeShellExecution: Captures command output for agents")
            print(f"   • stop: Auto-continues with pending tasks")
            print(f"\n   📊 Monitor hook activity:")
            print(f"   tail -f ~/.cursor/command-execution.log")
            print(f"   tail -f ~/.cursor/auto-continue.log")
            print(f"\n   🔧 Verify hooks: Cursor Settings → Hooks tab")

def list_available_categories():
    """List all available agent categories and their agents."""
    available_agents = discover_agents()

    if not available_agents:
        print("❌ No agent categories found")
        return

    print("📋 Available Agent Categories:\n")

    for category in sorted(available_agents.keys()):
        agents = available_agents[category]
        agent_count = len(agents)
        description = get_category_description(category)

        print(f"📂 {category} ({agent_count} agents)")
        print(f"   {description}")

        if agents:
            for agent in sorted(agents):
                print(f"   • {agent}")
        print()

def list_all_agents():
    """List all available agents."""
    available_agents = discover_agents()

    if not available_agents:
        print("❌ No agents found")
        return

    all_agents = []
    agent_locations = {}

    for category, agents in available_agents.items():
        for agent in agents:
            all_agents.append(agent)
            agent_locations[agent] = category

    print(f"🤖 All Available Agents ({len(all_agents)} total):\n")

    for i, agent in enumerate(sorted(all_agents), 1):
        category = agent_locations[agent]
        print(f"{i:2d}. {agent:<35} (from {category})")

def list_available_agents_in_categories():
    """List agents organized by categories."""
    available_agents = discover_agents()

    if not available_agents:
        print("❌ No agents found")
        return

    print("🤖 Available Agents by Category:\n")

    for category in sorted(available_agents.keys()):
        agents = available_agents[category]
        if agents:
            print(f"📂 {category}:")
            for agent in sorted(agents):
                print(f"   • {agent}")
            print()

def main():
    parser = argparse.ArgumentParser(
        description="Install AI agents from the ecosystem repository to your IDE agent directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cursor installation (default - includes agents, docs, commands, and hooks)
  python install-agents.py ~/.cursor/rules --all
  python install-agents.py ~/.cursor/rules --category coordination core-technical
  python install-agents.py ~/.cursor/rules --agents strategic-task-planner backend-architect

  # Skip optional components
  python install-agents.py ~/.cursor/rules --all --skip-commands
  python install-agents.py ~/.cursor/rules --all --skip-hooks
  python install-agents.py ~/.cursor/rules --all --skip-commands --skip-hooks

  # Claude Desktop installation (with --claude flag)
  python install-agents.py ~/.claude/agents --claude --all
  python install-agents.py ~/.claude/agents --claude --category coordination
  python install-agents.py ~/.claude/agents --claude --agents strategic-task-planner ai-ml-specialist

  # List available options
  python install-agents.py --list-categories
  python install-agents.py --list-agents
  python install-agents.py --list-by-category
        """
    )

    parser.add_argument('target_dir', nargs='?',
                       help='Target directory path (.cursor/rules for Cursor or .claude/agents for Claude Desktop)')

    parser.add_argument('--all', action='store_true',
                       help='Install all available agents')

    parser.add_argument('--category', '--categories', nargs='+',
                       help='Install agents from specific categories')

    parser.add_argument('--agents', '--agent', nargs='+',
                       help='Install specific agents by name')

    parser.add_argument('--claude', action='store_true',
                       help='Install for Claude Desktop (.md format with model field)')

    parser.add_argument('--skip-commands', action='store_true',
                       help='Skip installing Cursor custom commands (installed by default)')

    parser.add_argument('--skip-hooks', action='store_true',
                       help='Skip installing Cursor hooks (installed by default)')

    parser.add_argument('--list-categories', action='store_true',
                       help='List all available agent categories with descriptions')

    parser.add_argument('--list-agents', action='store_true',
                       help='List all available agents (flat list)')

    parser.add_argument('--list-by-category', action='store_true',
                       help='List all agents organized by category')

    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be copied without actually copying')

    args = parser.parse_args()

    # Handle list commands
    if args.list_categories:
        list_available_categories()
        return

    if args.list_agents:
        list_all_agents()
        return

    if args.list_by_category:
        list_available_agents_in_categories()
        return

    # Validate required arguments
    if not args.target_dir:
        print("❌ Error: Target directory is required")
        parser.print_help()
        sys.exit(1)

    # Validate that we have agents to install
    if not (args.all or args.category or args.agents):
        print("❌ Error: Must specify --all, --category, or --agents")
        parser.print_help()
        sys.exit(1)

    # Validate mutually exclusive options
    options_count = sum([bool(args.all), bool(args.category), bool(args.agents)])
    if options_count > 1:
        print("❌ Error: --all, --category, and --agents are mutually exclusive")
        sys.exit(1)

    # Validate categories exist if specified
    if args.category:
        available_agents = discover_agents()
        for category in args.category:
            if category not in available_agents:
                print(f"❌ Error: Category '{category}' not found")
                print("Available categories:")
                for cat in sorted(available_agents.keys()):
                    print(f"  • {cat}")
                sys.exit(1)

    # Determine installation type based on flag
    install_type = "claude" if args.claude else "cursor"

    # Validate target directory with installation type context
    target_dir = validate_target_directory(args.target_dir, args.claude)

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be copied\n")

    install_type_name = "Claude Desktop" if install_type == "claude" else "Cursor"
    print(f"🎯 AI Agent Ecosystem Installer")
    print(f"📁 Target: {target_dir}")
    print(f"🔧 Type: {install_type_name} Installation\n")

    # Perform installation
    if not args.dry_run:
        if args.all:
            install_agents(target_dir, install_type, skip_commands=args.skip_commands, skip_hooks=args.skip_hooks)
        elif args.category:
            install_agents(target_dir, install_type, categories=args.category, skip_commands=args.skip_commands, skip_hooks=args.skip_hooks)
        elif args.agents:
            install_agents(target_dir, install_type, agent_list=args.agents, skip_commands=args.skip_commands, skip_hooks=args.skip_hooks)
    else:
        print("📋 Would install agents based on your selection")
        if args.agents:
            available_agents = discover_agents()
            print("Agents to install:")
            for agent_name in args.agents:
                category = get_agent_location(agent_name, available_agents)
                if category:
                    print(f"  • {agent_name} (from {category})")
                else:
                    print(f"  • {agent_name} (NOT FOUND)")

        if args.skip_commands:
            print("  • Cursor commands will be skipped (--skip-commands)")
        else:
            print("  • Cursor commands will be installed to ~/.cursor/commands")

        if args.skip_hooks:
            print("  • Cursor hooks will be skipped (--skip-hooks)")
        else:
            print("  • Cursor hooks will be installed to ~/.cursor/hooks")

if __name__ == "__main__":
    main()