#!/usr/bin/env python3
"""
Lazy loading system for agents
Loads agent definitions on-demand to minimize token usage
"""

import yaml
from pathlib import Path
from typing import Dict, Optional, Set, List
from dataclasses import dataclass, field


@dataclass
class AgentCache:
    """Cache for loaded agents"""
    summaries: Dict[str, Dict] = field(default_factory=dict)
    full_definitions: Dict[str, str] = field(default_factory=dict)
    active_agents: Set[str] = field(default_factory=set)


class LazyAgentLoader:
    """Lazy loading system for agents"""

    def __init__(self, summaries_dir: str = "agents/summaries", agents_dir: str = "agents"):
        self.summaries_dir = Path(summaries_dir)
        self.agents_dir = Path(agents_dir)
        self.cache = AgentCache()
        self.directory = {}
        self._load_directory()

    def _load_directory(self):
        """Load agent directory (Tier 1) - always loaded"""
        self.directory = {}

        if not self.summaries_dir.exists():
            print(f"⚠️  Warning: Summaries directory not found: {self.summaries_dir}")
            print("   Run: python3 tools/generate_summaries.py")
            return

        summary_files = list(self.summaries_dir.glob('*.summary.yaml'))
        if not summary_files:
            print(f"⚠️  Warning: No summary files found in {self.summaries_dir}")
            print("   Run: python3 tools/generate_summaries.py")
            return

        for summary_file in summary_files:
            try:
                with open(summary_file, 'r') as f:
                    summary = yaml.safe_load(f)
                    name = summary.get('name')
                    if name:
                        self.directory[name] = {
                            'category': summary.get('category', 'unknown'),
                            'description': summary.get('description', '')[:100],  # First 100 chars
                            'summary_file': str(summary_file)
                        }
            except Exception as e:
                print(f"Warning: Could not load {summary_file}: {e}")

        if self.directory:
            print(f"📚 Loaded directory with {len(self.directory)} agents")

    def get_directory(self) -> Dict[str, Dict]:
        """Get agent directory (lightweight listing)"""
        return self.directory.copy()

    def list_agents(self, category: Optional[str] = None) -> List[str]:
        """List available agents, optionally filtered by category"""
        if category:
            return [
                name for name, info in self.directory.items()
                if info['category'] == category
            ]
        return list(self.directory.keys())

    def list_categories(self) -> List[str]:
        """List all categories"""
        categories = set(info['category'] for info in self.directory.values())
        return sorted(categories)

    def load_summary(self, agent_name: str) -> Optional[Dict]:
        """Load agent summary (Tier 2)"""
        # Check cache
        if agent_name in self.cache.summaries:
            return self.cache.summaries[agent_name]

        # Load from file
        if agent_name not in self.directory:
            print(f"❌ Agent not found: {agent_name}")
            return None

        summary_file = self.directory[agent_name]['summary_file']

        try:
            with open(summary_file, 'r') as f:
                summary = yaml.safe_load(f)

            # Cache it
            self.cache.summaries[agent_name] = summary
            return summary

        except Exception as e:
            print(f"Error loading summary for {agent_name}: {e}")
            return None

    def load_full_definition(self, agent_name: str) -> Optional[str]:
        """Load full agent definition (Tier 3)"""
        # Check cache
        if agent_name in self.cache.full_definitions:
            return self.cache.full_definitions[agent_name]

        # Get summary first
        summary = self.load_summary(agent_name)
        if not summary:
            return None

        # Load full definition
        full_def_path = Path(summary['full_definition'])

        if not full_def_path.exists():
            print(f"⚠️  Warning: Full definition not found: {full_def_path}")
            return None

        try:
            with open(full_def_path, 'r') as f:
                full_definition = f.read()

            # Cache it
            self.cache.full_definitions[agent_name] = full_definition
            self.cache.active_agents.add(agent_name)

            return full_definition

        except Exception as e:
            print(f"Error loading full definition for {agent_name}: {e}")
            return None

    def activate_agent(self, agent_name: str) -> bool:
        """Activate an agent (load full definition)"""
        definition = self.load_full_definition(agent_name)
        if definition:
            print(f"✅ Activated: {agent_name}")
            return True
        else:
            print(f"❌ Failed to activate: {agent_name}")
            return False

    def deactivate_agent(self, agent_name: str):
        """Deactivate agent (remove from active set)"""
        if agent_name in self.cache.active_agents:
            self.cache.active_agents.discard(agent_name)
            print(f"⏸️  Deactivated: {agent_name}")
            # Keep in cache for quick reactivation
        else:
            print(f"⚠️  Agent not active: {agent_name}")

    def get_active_agents(self) -> Set[str]:
        """Get list of currently active agents"""
        return self.cache.active_agents.copy()

    def clear_cache(self):
        """Clear all cached data"""
        self.cache = AgentCache()
        print("🧹 Cache cleared")

    def get_token_estimate(self) -> Dict:
        """Estimate current token usage"""
        # Rough estimates: 1 char ≈ 0.25 tokens (4 chars per token average)

        # Directory size (all agents listed with minimal info)
        directory_tokens = len(str(self.directory)) // 4

        # Summaries size (loaded summaries)
        summaries_tokens = sum(
            len(str(summary)) // 4
            for summary in self.cache.summaries.values()
        )

        # Full definitions size (loaded full agents)
        full_def_tokens = sum(
            len(definition) // 4
            for definition in self.cache.full_definitions.values()
        )

        total_tokens = directory_tokens + summaries_tokens + full_def_tokens

        return {
            'directory_tokens': directory_tokens,
            'summaries_tokens': summaries_tokens,
            'full_definitions_tokens': full_def_tokens,
            'total_tokens': total_tokens,
            'active_agents_count': len(self.cache.active_agents),
            'cached_summaries_count': len(self.cache.summaries),
            'cached_definitions_count': len(self.cache.full_definitions)
        }

    def print_status(self):
        """Print current loading status"""
        estimates = self.get_token_estimate()

        print("\n" + "=" * 60)
        print("LAZY LOADER STATUS")
        print("=" * 60)
        print(f"📂 Directory: {len(self.directory)} agents ({estimates['directory_tokens']} tokens)")
        print(f"📄 Cached Summaries: {estimates['cached_summaries_count']} ({estimates['summaries_tokens']} tokens)")
        print(f"📚 Cached Definitions: {estimates['cached_definitions_count']} ({estimates['full_definitions_tokens']} tokens)")
        print(f"▶️  Active Agents: {len(self.cache.active_agents)}")
        print(f"💾 Total Token Usage: ~{estimates['total_tokens']} tokens")
        print("=" * 60)

        if self.cache.active_agents:
            print("\n▶️  Active Agents:")
            for agent in sorted(self.cache.active_agents):
                summary = self.cache.summaries.get(agent, {})
                desc = summary.get('description', 'No description')[:60]
                print(f"  • {agent}: {desc}")

    def find_agents(self, query: str, limit: int = 5) -> List[tuple]:
        """
        Find agents matching a query (searches summaries)

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            List of (agent_name, relevance_score) tuples
        """
        query_lower = query.lower()
        results = []

        for agent_name in self.directory:
            # Load summary if not cached
            summary = self.load_summary(agent_name)
            if not summary:
                continue

            score = 0.0

            # Check description
            if query_lower in summary.get('description', '').lower():
                score += 2.0

            # Check specializations
            for spec in summary.get('specializations', []):
                if query_lower in spec.lower().replace('_', ' '):
                    score += 3.0

            # Check technologies
            for tech in summary.get('technologies', []):
                if query_lower in tech.lower():
                    score += 2.0

            # Check use_when
            for use_case in summary.get('use_when', []):
                if query_lower in use_case.lower():
                    score += 1.5

            if score > 0:
                results.append((agent_name, score))

        # Sort by score descending
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:limit]


def main():
    """CLI interface for lazy loader"""
    import argparse

    parser = argparse.ArgumentParser(description='Lazy Agent Loader')
    parser.add_argument('--list', action='store_true', help='List all agents')
    parser.add_argument('--categories', action='store_true', help='List all categories')
    parser.add_argument('--category', type=str, help='List agents in category')
    parser.add_argument('--summary', type=str, help='Load summary for agent')
    parser.add_argument('--activate', type=str, nargs='+', help='Activate agents')
    parser.add_argument('--deactivate', type=str, nargs='+', help='Deactivate agents')
    parser.add_argument('--find', type=str, help='Find agents matching query')
    parser.add_argument('--status', action='store_true', help='Show loader status')
    parser.add_argument('--summaries-dir', default='agents/summaries', help='Summaries directory')
    parser.add_argument('--agents-dir', default='agents', help='Agents directory')

    args = parser.parse_args()

    # Initialize loader
    loader = LazyAgentLoader(
        summaries_dir=args.summaries_dir,
        agents_dir=args.agents_dir
    )

    if not loader.directory:
        print("\n❌ No agents found. Please run:")
        print("   python3 tools/generate_summaries.py")
        return 1

    # List all agents
    if args.list:
        print(f"\n📚 Available Agents ({len(loader.directory)}):\n")
        by_category = {}
        for name, info in loader.directory.items():
            category = info['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((name, info['description']))

        for category in sorted(by_category.keys()):
            print(f"📁 {category}:")
            for name, desc in sorted(by_category[category]):
                print(f"  • {name}: {desc}")
            print()

    # List categories
    if args.categories:
        categories = loader.list_categories()
        print(f"\n📁 Categories ({len(categories)}):\n")
        for cat in categories:
            agents = loader.list_agents(category=cat)
            print(f"  • {cat}: {len(agents)} agents")

    # List agents in category
    if args.category:
        agents = loader.list_agents(category=args.category)
        print(f"\n📁 Agents in '{args.category}' ({len(agents)}):\n")
        for agent in sorted(agents):
            desc = loader.directory[agent]['description']
            print(f"  • {agent}: {desc}")

    # Show summary
    if args.summary:
        summary = loader.load_summary(args.summary)
        if summary:
            print(f"\n📄 Summary for {args.summary}:\n")
            print(f"  Version: {summary.get('version', 'unknown')}")
            print(f"  Category: {summary.get('category', 'unknown')}")
            print(f"  Description: {summary.get('description', 'No description')}")

            if summary.get('specializations'):
                print(f"  Specializations: {', '.join(summary['specializations'])}")

            if summary.get('technologies'):
                print(f"  Technologies: {', '.join(summary['technologies'])}")

            if summary.get('use_when'):
                print(f"  Use when:")
                for use_case in summary['use_when']:
                    print(f"    • {use_case}")

            print(f"  Consultation available: {summary.get('consultation_available', True)}")
            print(f"  Avg duration: {summary.get('avg_task_duration_hours', 2.0)}h")

    # Activate agents
    if args.activate:
        print(f"\n▶️  Activating {len(args.activate)} agent(s)...\n")
        for agent in args.activate:
            loader.activate_agent(agent)

    # Deactivate agents
    if args.deactivate:
        print(f"\n⏸️  Deactivating {len(args.deactivate)} agent(s)...\n")
        for agent in args.deactivate:
            loader.deactivate_agent(agent)

    # Find agents
    if args.find:
        print(f"\n🔍 Finding agents for: {args.find}\n")
        results = loader.find_agents(args.find, limit=10)

        if results:
            for agent_name, score in results:
                summary = loader.cache.summaries[agent_name]
                print(f"  {score:.1f} - {agent_name}")
                print(f"       {summary.get('description', 'No description')[:80]}")
                if summary.get('specializations'):
                    print(f"       Specializations: {', '.join(summary['specializations'][:3])}")
                print()
        else:
            print("  No matches found")

    # Show status
    if args.status or args.activate or args.deactivate:
        loader.print_status()

    return 0


if __name__ == '__main__':
    exit(main())
