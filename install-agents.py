#!/usr/bin/env python3
"""
AI Agent Ecosystem Installer

This script copies AI agents and their required documentation files from the
organized repository structure to your .cursor/rules directory for easy
installation and management.

Required Documentation Files:
- AGENT_HIERARCHY.md (agent coordination hierarchy)
- WORKSPACE_PROTOCOLS.md (workspace management standards)
- TEAM_COLLABORATION_CULTURE.md (communication guidelines)
- AGENT_DIRECTORY.md (agent list and collaboration patterns)
- agent-coordination-guide.md (coordination methodologies)

Usage:
    python install-agents.py <target_directory> [options]
    python install-agents.py /path/to/.cursor/rules --all
    python install-agents.py ~/.cursor/rules --category coordination
    python install-agents.py ~/.cursor/rules --agents strategic-task-planner ai-ml-specialist
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

def validate_target_directory(target_path: str) -> Path:
    """Validate and create target directory if needed."""
    target = Path(target_path).expanduser().resolve()

    try:
        target.mkdir(parents=True, exist_ok=True)
        return target
    except Exception as e:
        print(f"❌ Error: Cannot create target directory {target}: {e}")
        sys.exit(1)

def copy_agent(agent_name: str, source_category: str, target_dir: Path) -> bool:
    """Copy a single agent from source to target directory."""
    agents_dir = get_agents_directory()
    source_file = agents_dir / source_category / f"{agent_name}.mdc"
    target_file = target_dir / f"{agent_name}.mdc"

    if not source_file.exists():
        print(f"⚠️  Warning: Agent {agent_name} not found in {source_category}")
        return False

    try:
        shutil.copy2(source_file, target_file)
        print(f"✅ Copied {agent_name}.mdc")
        return True
    except Exception as e:
        print(f"❌ Error copying {agent_name}.mdc: {e}")
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
        "agent-coordination-guide.md": script_dir / "docs" / "agent-coordination-guide.md"
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

def install_agents(target_dir: Path, agent_list: List[str] = None, categories: List[str] = None) -> None:
    """Install specified agents or all agents to target directory."""
    available_agents = discover_agents()

    if not available_agents:
        print("❌ No agents found in the repository")
        return

    # Always copy required documentation files first
    print("📋 Copying required documentation files...")
    doc_results = copy_documentation_files(target_dir)
    docs_copied = sum(doc_results.values())

    copied_count = 0
    total_count = 0

    # If specific agents are requested
    if agent_list:
        print(f"📋 Installing specific agents: {', '.join(agent_list)}")

        for agent_name in agent_list:
            source_category = get_agent_location(agent_name, available_agents)
            if source_category:
                if copy_agent(agent_name, source_category, target_dir):
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
                if copy_agent(agent_name, category, target_dir):
                    copied_count += 1
                total_count += 1

    # Install all agents
    else:
        print("📋 Installing all available agents...")

        for category, agents in available_agents.items():
            if agents:
                print(f"\n📂 Installing {category} agents:")
                for agent_name in agents:
                    if copy_agent(agent_name, category, target_dir):
                        copied_count += 1
                    total_count += 1

    # Summary
    print(f"\n🎯 Installation Summary:")
    print(f"   ✅ Successfully copied: {copied_count} agents")
    print(f"   ✅ Documentation files: {docs_copied}/5 copied successfully")
    if total_count > copied_count:
        print(f"   ⚠️  Failed or skipped: {total_count - copied_count} agents")
    print(f"   📁 Target directory: {target_dir}")

    if copied_count > 0:
        print(f"\n🚀 Ready to use! Restart your IDE to load the new agents.")
        print(f"   Test with: @strategic-task-planner: Hello")
        if doc_results.get("AGENT_HIERARCHY.md", False):
            print(f"   📋 Agent coordination enabled with full documentation support")
            print(f"   📖 Coordination guide: See agent-coordination-guide.md")

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
        description="Install AI agents from the ecosystem repository to your .cursor/rules directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install all agents
  python install-agents.py ~/.cursor/rules --all

  # Install specific categories
  python install-agents.py ~/.cursor/rules --category coordination core-technical

  # Install specific agents (by name)
  python install-agents.py ~/.cursor/rules --agents strategic-task-planner ai-ml-specialist backend-architect

  # List available options
  python install-agents.py --list-categories
  python install-agents.py --list-agents
  python install-agents.py --list-by-category
        """
    )

    parser.add_argument('target_dir', nargs='?',
                       help='Target .cursor/rules directory path')

    parser.add_argument('--all', action='store_true',
                       help='Install all available agents')

    parser.add_argument('--category', '--categories', nargs='+',
                       help='Install agents from specific categories')

    parser.add_argument('--agents', '--agent', nargs='+',
                       help='Install specific agents by name')

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

    # Validate target directory
    target_dir = validate_target_directory(args.target_dir)

    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be copied\n")

    print(f"🎯 AI Agent Ecosystem Installer")
    print(f"📁 Target: {target_dir}\n")

    # Perform installation
    if not args.dry_run:
        if args.all:
            install_agents(target_dir)
        elif args.category:
            install_agents(target_dir, categories=args.category)
        elif args.agents:
            install_agents(target_dir, agent_list=args.agents)
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

if __name__ == "__main__":
    main()