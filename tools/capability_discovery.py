#!/usr/bin/env python3
"""
Agent Capability Discovery System
Scans agent definitions and provides intelligent agent selection based on capabilities
"""

import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict


@dataclass
class AgentCapabilities:
    """Structured representation of an agent's capabilities"""
    name: str
    version: str = "1.0.0"
    description: str = ""
    category: str = ""

    # Core capabilities
    file_operations: List[str] = field(default_factory=list)
    command_execution: List[str] = field(default_factory=list)
    external_access: List[str] = field(default_factory=list)

    # Domain specializations
    specializations: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    methodologies: List[str] = field(default_factory=list)

    # Operational parameters
    consultation_available: bool = True
    always_apply: bool = False
    max_parallel_tasks: int = 3
    avg_task_duration_hours: float = 2.0

    # Dependencies and relationships
    requires_agents: List[str] = field(default_factory=list)
    works_well_with: List[str] = field(default_factory=list)
    provides_for: List[str] = field(default_factory=list)

    # Metadata
    keywords: Set[str] = field(default_factory=set)
    file_path: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['keywords'] = list(self.keywords)  # Convert set to list
        return data

    def matches_requirement(self, requirement: str) -> float:
        """
        Calculate match score (0-1) for a given requirement

        Args:
            requirement: Text description of what's needed

        Returns:
            Score between 0 and 1 indicating match quality
        """
        requirement_lower = requirement.lower()
        score = 0.0
        max_score = 0.0

        # Check specializations (high weight)
        max_score += 3.0
        for spec in self.specializations:
            if spec.lower() in requirement_lower:
                score += 3.0
                break

        # Check technologies (medium weight)
        max_score += 2.0
        for tech in self.technologies:
            if tech.lower() in requirement_lower:
                score += 2.0
                break

        # Check keywords (medium weight)
        max_score += 2.0
        keyword_matches = sum(1 for kw in self.keywords if kw.lower() in requirement_lower)
        if keyword_matches > 0:
            score += min(2.0, keyword_matches * 0.5)

        # Check description (low weight)
        max_score += 1.0
        if any(word in self.description.lower() for word in requirement_lower.split()):
            score += 1.0

        return score / max_score if max_score > 0 else 0.0


class CapabilityDiscovery:
    """Discover and index agent capabilities"""

    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = Path(agents_dir)
        self.agents: Dict[str, AgentCapabilities] = {}
        self.categories: Dict[str, List[str]] = defaultdict(list)
        self.specialization_index: Dict[str, List[str]] = defaultdict(list)
        self.technology_index: Dict[str, List[str]] = defaultdict(list)

    def scan_all_agents(self) -> int:
        """
        Scan all .mdc files and extract capabilities

        Returns:
            Number of agents discovered
        """
        print(f"Scanning {self.agents_dir} for agent definitions...")

        mdc_files = list(self.agents_dir.rglob("*.mdc"))
        print(f"Found {len(mdc_files)} agent files")

        for mdc_file in mdc_files:
            try:
                capabilities = self._parse_agent_file(mdc_file)
                if capabilities:
                    self.agents[capabilities.name] = capabilities

                    # Index by category
                    self.categories[capabilities.category].append(capabilities.name)

                    # Index by specializations
                    for spec in capabilities.specializations:
                        self.specialization_index[spec.lower()].append(capabilities.name)

                    # Index by technologies
                    for tech in capabilities.technologies:
                        self.technology_index[tech.lower()].append(capabilities.name)

            except Exception as e:
                print(f"Warning: Failed to parse {mdc_file}: {e}")

        print(f"Successfully indexed {len(self.agents)} agents")
        return len(self.agents)

    def _parse_agent_file(self, file_path: Path) -> Optional[AgentCapabilities]:
        """Parse a single agent .mdc file"""
        content = file_path.read_text()

        # Extract YAML frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if not frontmatter_match:
            return None

        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError:
            return None

        name = frontmatter.get('name')
        if not name:
            return None

        # Determine category from file path
        category = file_path.parent.name

        # Initialize capabilities
        capabilities = AgentCapabilities(
            name=name,
            description=frontmatter.get('description', ''),
            category=category,
            always_apply=frontmatter.get('alwaysApply', False),
            file_path=str(file_path)
        )

        # Extract capabilities from frontmatter if present
        if 'capabilities' in frontmatter:
            cap_data = frontmatter['capabilities']
            capabilities.file_operations = cap_data.get('file_operations', [])
            capabilities.command_execution = cap_data.get('command_execution', [])
            capabilities.external_access = cap_data.get('external_access', [])
            capabilities.specializations = cap_data.get('specializations', [])
            capabilities.technologies = cap_data.get('technologies', [])
            capabilities.methodologies = cap_data.get('methodologies', [])
            capabilities.consultation_available = cap_data.get('consultation_available', True)
            capabilities.max_parallel_tasks = cap_data.get('max_parallel_tasks', 3)
            capabilities.avg_task_duration_hours = cap_data.get('avg_task_duration_hours', 2.0)
            capabilities.version = cap_data.get('version', '1.0.0')

        # Infer capabilities from description and content if not explicitly defined
        if not capabilities.specializations:
            capabilities.specializations = self._infer_specializations(content)

        if not capabilities.technologies:
            capabilities.technologies = self._infer_technologies(content)

        # Extract keywords from description
        capabilities.keywords = self._extract_keywords(capabilities.description)

        return capabilities

    def _infer_specializations(self, content: str) -> List[str]:
        """Infer specializations from content"""
        specializations = []

        # Common specialization patterns
        patterns = {
            'api_design': r'\b(REST|GraphQL|gRPC|API design|API development)\b',
            'database': r'\b(database|SQL|NoSQL|PostgreSQL|MongoDB|Redis)\b',
            'frontend': r'\b(React|Vue|Angular|frontend|UI|user interface)\b',
            'backend': r'\b(backend|server|Node\.js|Python|microservices)\b',
            'security': r'\b(security|authentication|authorization|encryption|OWASP)\b',
            'performance': r'\b(performance|optimization|caching|scalability)\b',
            'testing': r'\b(testing|QA|quality assurance|test automation)\b',
            'devops': r'\b(DevOps|CI/CD|deployment|infrastructure|Docker|Kubernetes)\b',
            'ml_ai': r'\b(machine learning|ML|AI|neural networks|NLP|computer vision)\b',
            'data_engineering': r'\b(data pipeline|ETL|data processing|Apache Spark)\b',
        }

        for spec, pattern in patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                specializations.append(spec)

        return specializations

    def _infer_technologies(self, content: str) -> List[str]:
        """Infer technologies from content"""
        technologies = []

        # Common technology keywords
        tech_keywords = [
            'JavaScript', 'TypeScript', 'Python', 'Java', 'Go', 'Rust', 'Ruby',
            'Node.js', 'React', 'Vue', 'Angular', 'Django', 'Flask', 'Express',
            'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
            'REST', 'GraphQL', 'gRPC', 'WebSocket',
            'Git', 'GitHub', 'GitLab', 'Jenkins', 'CircleCI'
        ]

        for tech in tech_keywords:
            if re.search(rf'\b{re.escape(tech)}\b', content, re.IGNORECASE):
                technologies.append(tech)

        return technologies

    def _extract_keywords(self, description: str) -> Set[str]:
        """Extract important keywords from description"""
        # Remove common words
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have'
        }

        words = re.findall(r'\b\w+\b', description.lower())
        keywords = {w for w in words if len(w) > 3 and w not in stop_words}

        return keywords

    def find_agent(self, requirement: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Find best matching agents for a requirement

        Args:
            requirement: Description of what's needed
            top_n: Number of top matches to return

        Returns:
            List of (agent_name, match_score) tuples, sorted by score
        """
        if not self.agents:
            self.scan_all_agents()

        scores = []
        for name, capabilities in self.agents.items():
            score = capabilities.matches_requirement(requirement)
            scores.append((name, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[:top_n]

    def find_by_specialization(self, specialization: str) -> List[str]:
        """Find agents with a specific specialization"""
        return self.specialization_index.get(specialization.lower(), [])

    def find_by_technology(self, technology: str) -> List[str]:
        """Find agents familiar with a specific technology"""
        return self.technology_index.get(technology.lower(), [])

    def find_by_category(self, category: str) -> List[str]:
        """Find agents in a specific category"""
        return self.categories.get(category, [])

    def get_agent_details(self, agent_name: str) -> Optional[AgentCapabilities]:
        """Get detailed capabilities for a specific agent"""
        return self.agents.get(agent_name)

    def recommend_team(self, project_description: str, max_agents: int = 5) -> List[Dict]:
        """
        Recommend a team of agents for a project

        Args:
            project_description: Description of the project
            max_agents: Maximum number of agents to recommend

        Returns:
            List of agent recommendations with scores and roles
        """
        # Find initial matches
        matches = self.find_agent(project_description, top_n=max_agents * 2)

        # Build team considering dependencies and complementary skills
        team = []
        selected_names = set()
        coverage = set()

        for agent_name, score in matches:
            if len(team) >= max_agents:
                break

            capabilities = self.agents[agent_name]

            # Check if this agent adds new coverage
            agent_coverage = set(capabilities.specializations) | set(capabilities.technologies)
            new_coverage = agent_coverage - coverage

            if new_coverage or score > 0.7:  # High score can justify some overlap
                team.append({
                    'agent': agent_name,
                    'match_score': round(score, 3),
                    'category': capabilities.category,
                    'specializations': capabilities.specializations,
                    'technologies': capabilities.technologies,
                    'new_coverage': list(new_coverage),
                    'avg_duration_hours': capabilities.avg_task_duration_hours
                })

                selected_names.add(agent_name)
                coverage.update(agent_coverage)

        # Add suggested dependencies
        for team_member in team[:]:  # Iterate over copy
            agent = self.agents[team_member['agent']]
            for required in agent.requires_agents:
                if required not in selected_names and len(team) < max_agents:
                    if required in self.agents:
                        dep_capabilities = self.agents[required]
                        team.append({
                            'agent': required,
                            'match_score': 0.5,
                            'category': dep_capabilities.category,
                            'specializations': dep_capabilities.specializations,
                            'technologies': dep_capabilities.technologies,
                            'reason': f"Required by {team_member['agent']}",
                            'avg_duration_hours': dep_capabilities.avg_task_duration_hours
                        })
                        selected_names.add(required)

        return team

    def export_index(self, output_file: str = "agent_capabilities_index.json") -> None:
        """Export capability index to JSON"""
        data = {
            'agents': {name: cap.to_dict() for name, cap in self.agents.items()},
            'categories': dict(self.categories),
            'specialization_index': dict(self.specialization_index),
            'technology_index': dict(self.technology_index),
            'stats': {
                'total_agents': len(self.agents),
                'total_categories': len(self.categories),
                'total_specializations': len(self.specialization_index),
                'total_technologies': len(self.technology_index)
            }
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Exported capability index to {output_file}")

    def generate_capability_report(self) -> str:
        """Generate a human-readable capability report"""
        if not self.agents:
            self.scan_all_agents()

        report = ["=" * 60]
        report.append("AGENT CAPABILITY DISCOVERY REPORT")
        report.append("=" * 60)
        report.append("")

        # Summary statistics
        report.append("📊 SUMMARY")
        report.append(f"  Total Agents: {len(self.agents)}")
        report.append(f"  Categories: {len(self.categories)}")
        report.append(f"  Specializations: {len(self.specialization_index)}")
        report.append(f"  Technologies: {len(self.technology_index)}")
        report.append("")

        # By category
        report.append("📁 BY CATEGORY")
        for category, agents in sorted(self.categories.items()):
            report.append(f"  {category}: {len(agents)} agents")
            for agent in sorted(agents)[:3]:  # Show first 3
                report.append(f"    - {agent}")
            if len(agents) > 3:
                report.append(f"    ... and {len(agents) - 3} more")
        report.append("")

        # Top specializations
        report.append("🎯 TOP SPECIALIZATIONS")
        spec_counts = [(spec, len(agents)) for spec, agents in self.specialization_index.items()]
        spec_counts.sort(key=lambda x: x[1], reverse=True)
        for spec, count in spec_counts[:10]:
            report.append(f"  {spec}: {count} agents")
        report.append("")

        # Top technologies
        report.append("💻 TOP TECHNOLOGIES")
        tech_counts = [(tech, len(agents)) for tech, agents in self.technology_index.items()]
        tech_counts.sort(key=lambda x: x[1], reverse=True)
        for tech, count in tech_counts[:10]:
            report.append(f"  {tech}: {count} agents")
        report.append("")

        # Always-apply agents
        always_apply = [name for name, cap in self.agents.items() if cap.always_apply]
        if always_apply:
            report.append("⭐ ALWAYS-APPLY AGENTS")
            for agent in always_apply:
                report.append(f"  - {agent}")
            report.append("")

        report.append("=" * 60)

        return "\n".join(report)


def main():
    """CLI interface for capability discovery"""
    import argparse

    parser = argparse.ArgumentParser(description='Agent Capability Discovery System')
    parser.add_argument('--scan', action='store_true', help='Scan and index all agents')
    parser.add_argument('--find', type=str, help='Find agents matching requirement')
    parser.add_argument('--specialization', type=str, help='Find agents by specialization')
    parser.add_argument('--technology', type=str, help='Find agents by technology')
    parser.add_argument('--category', type=str, help='Find agents by category')
    parser.add_argument('--details', type=str, help='Show details for specific agent')
    parser.add_argument('--recommend', type=str, help='Recommend team for project')
    parser.add_argument('--report', action='store_true', help='Generate capability report')
    parser.add_argument('--export', type=str, help='Export index to JSON file')
    parser.add_argument('--agents-dir', type=str, default='agents', help='Agents directory')
    parser.add_argument('--top-n', type=int, default=5, help='Number of results to show')

    args = parser.parse_args()

    discovery = CapabilityDiscovery(args.agents_dir)

    # Scan agents
    if args.scan or args.report or args.find or args.recommend:
        discovery.scan_all_agents()
        print()

    # Generate report
    if args.report:
        print(discovery.generate_capability_report())

    # Find agents
    if args.find:
        print(f"🔍 Finding agents for: {args.find}")
        print()
        matches = discovery.find_agent(args.find, top_n=args.top_n)
        for agent_name, score in matches:
            capabilities = discovery.get_agent_details(agent_name)
            print(f"  {score:.2f} - {agent_name}")
            print(f"       Category: {capabilities.category}")
            if capabilities.specializations:
                print(f"       Specializations: {', '.join(capabilities.specializations[:3])}")
            print()

    # Find by specialization
    if args.specialization:
        agents = discovery.find_by_specialization(args.specialization)
        print(f"🎯 Agents with specialization '{args.specialization}': {len(agents)}")
        for agent in agents:
            print(f"  - {agent}")

    # Find by technology
    if args.technology:
        agents = discovery.find_by_technology(args.technology)
        print(f"💻 Agents with technology '{args.technology}': {len(agents)}")
        for agent in agents:
            print(f"  - {agent}")

    # Find by category
    if args.category:
        agents = discovery.find_by_category(args.category)
        print(f"📁 Agents in category '{args.category}': {len(agents)}")
        for agent in agents:
            print(f"  - {agent}")

    # Show agent details
    if args.details:
        capabilities = discovery.get_agent_details(args.details)
        if capabilities:
            print(f"📋 Details for {args.details}")
            print(f"   Category: {capabilities.category}")
            print(f"   Description: {capabilities.description}")
            print(f"   Specializations: {', '.join(capabilities.specializations)}")
            print(f"   Technologies: {', '.join(capabilities.technologies)}")
            print(f"   Consultation Available: {capabilities.consultation_available}")
            print(f"   Avg Duration: {capabilities.avg_task_duration_hours}h")
        else:
            print(f"Agent '{args.details}' not found")

    # Recommend team
    if args.recommend:
        print(f"👥 Recommending team for: {args.recommend}")
        print()
        team = discovery.recommend_team(args.recommend, max_agents=args.top_n)
        total_hours = sum(member['avg_duration_hours'] for member in team)
        print(f"Recommended {len(team)} agents (estimated total: {total_hours:.1f}h)")
        print()
        for i, member in enumerate(team, 1):
            print(f"{i}. {member['agent']} (score: {member.get('match_score', 0):.2f})")
            print(f"   Category: {member['category']}")
            print(f"   Specializations: {', '.join(member['specializations'][:3])}")
            if 'new_coverage' in member and member['new_coverage']:
                print(f"   New Coverage: {', '.join(member['new_coverage'][:3])}")
            if 'reason' in member:
                print(f"   Reason: {member['reason']}")
            print()

    # Export index
    if args.export:
        discovery.export_index(args.export)


if __name__ == '__main__':
    main()
