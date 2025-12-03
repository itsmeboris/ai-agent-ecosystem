#!/usr/bin/env python3
"""
Generate agent summaries from full agent definitions
Creates lightweight .summary.yaml files for token efficiency
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Optional


def generate_summary(agent_file: Path) -> Optional[Dict]:
    """Generate summary from full agent definition"""
    try:
        content = agent_file.read_text()
    except Exception as e:
        print(f"Error reading {agent_file}: {e}")
        return None

    # Extract frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if not frontmatter_match:
        print(f"No frontmatter found in {agent_file}")
        return None

    try:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
    except yaml.YAMLError as e:
        print(f"YAML error in {agent_file}: {e}")
        return None

    name = frontmatter.get('name')
    if not name:
        print(f"No name field in {agent_file}")
        return None

    # Extract capabilities if present
    capabilities = frontmatter.get('capabilities', {})

    # Create summary
    summary = {
        'name': name,
        'version': capabilities.get('version', '1.0.0'),
        'category': agent_file.parent.name,
        'description': frontmatter.get('description', ''),
        'consultation_available': capabilities.get('consultation_available', True),
        'avg_task_duration_hours': capabilities.get('avg_task_duration_hours', 2.0),
        'full_definition': str(agent_file),
    }

    # Add top specializations (limit to 5)
    if 'specializations' in capabilities:
        summary['specializations'] = capabilities['specializations'][:5]
    else:
        # Infer from description if not specified
        summary['specializations'] = _infer_specializations(content)[:5]

    # Add top technologies (limit to 8)
    if 'technologies' in capabilities:
        summary['technologies'] = capabilities['technologies'][:8]
    else:
        # Infer from content if not specified
        summary['technologies'] = _infer_technologies(content)[:8]

    # Add essential relationships
    if 'requires_agents' in capabilities:
        summary['requires_agents'] = capabilities['requires_agents']

    if 'works_well_with' in capabilities:
        summary['works_well_with'] = capabilities['works_well_with'][:3]  # Top 3 only

    # Generate "use when" keywords from description and specializations
    use_when = []

    # From specializations
    if summary.get('specializations'):
        for spec in summary['specializations'][:3]:
            # Convert snake_case to human readable
            readable = spec.replace('_', ' ')
            use_when.append(f"need {readable}")

    # From description keywords
    desc_lower = summary['description'].lower()
    if 'api' in desc_lower:
        use_when.append("building APIs")
    if 'database' in desc_lower or 'data' in desc_lower:
        use_when.append("working with data")
    if 'frontend' in desc_lower or 'ui' in desc_lower:
        use_when.append("building user interfaces")
    if 'security' in desc_lower:
        use_when.append("security concerns")
    if 'performance' in desc_lower or 'optimization' in desc_lower:
        use_when.append("optimization needed")

    # Limit to 5 use cases
    summary['use_when'] = use_when[:5]

    return summary


def _infer_specializations(content: str) -> list:
    """Infer specializations from content"""
    specializations = []

    patterns = {
        'api_design': r'\b(REST|GraphQL|gRPC|API design|API development)\b',
        'database': r'\b(database|SQL|NoSQL|PostgreSQL|MongoDB|Redis)\b',
        'frontend': r'\b(React|Vue|Angular|frontend|UI|user interface)\b',
        'backend': r'\b(backend|server|Node\.js|Python|microservices)\b',
        'security': r'\b(security|authentication|authorization|encryption|OWASP)\b',
        'performance': r'\b(performance|optimization|caching|scalability)\b',
        'testing': r'\b(testing|QA|quality assurance|test automation)\b',
        'devops': r'\b(DevOps|CI/CD|deployment|infrastructure|Docker|Kubernetes)\b',
        'ml_ai': r'\b(machine learning|ML|AI|neural networks|NLP)\b',
        'data_engineering': r'\b(data pipeline|ETL|data processing)\b',
    }

    for spec, pattern in patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            specializations.append(spec)

    return specializations


def _infer_technologies(content: str) -> list:
    """Infer technologies from content"""
    technologies = []

    tech_keywords = [
        'JavaScript', 'TypeScript', 'Python', 'Java', 'Go', 'Rust',
        'Node.js', 'React', 'Vue', 'Angular', 'Django', 'Flask',
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP',
        'REST', 'GraphQL', 'gRPC',
        'Git', 'GitHub'
    ]

    for tech in tech_keywords:
        if re.search(rf'\b{re.escape(tech)}\b', content, re.IGNORECASE):
            technologies.append(tech)

    return technologies


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate agent summaries')
    parser.add_argument('--agents-dir', default='agents', help='Agents directory')
    parser.add_argument('--output-dir', default='agents/summaries', help='Output directory')
    parser.add_argument('--force', action='store_true', help='Overwrite existing summaries')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    agents_dir = Path(args.agents_dir)
    output_dir = Path(args.output_dir)

    if not agents_dir.exists():
        print(f"Error: Agents directory not found: {agents_dir}")
        return 1

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all agent files
    agent_files = list(agents_dir.rglob('*.mdc'))
    print(f"Found {len(agent_files)} agent definitions in {agents_dir}")

    generated = 0
    skipped = 0
    errors = 0

    for agent_file in agent_files:
        # Generate summary
        summary = generate_summary(agent_file)

        if not summary:
            errors += 1
            continue

        # Output file path
        output_file = output_dir / f"{summary['name']}.summary.yaml"

        # Check if exists
        if output_file.exists() and not args.force:
            if args.verbose:
                print(f"Skipped (exists): {output_file}")
            skipped += 1
            continue

        # Write summary
        try:
            with open(output_file, 'w') as f:
                yaml.dump(summary, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            generated += 1
            if args.verbose or generated % 10 == 0:
                print(f"Generated: {output_file}")

        except Exception as e:
            print(f"Error writing {output_file}: {e}")
            errors += 1

    print(f"\n📊 Summary:")
    print(f"  ✅ Generated: {generated}")
    print(f"  ⏭️  Skipped: {skipped}")
    if errors > 0:
        print(f"  ❌ Errors: {errors}")

    print(f"\n💾 Output directory: {output_dir}")
    print(f"📦 Total summaries: {len(list(output_dir.glob('*.summary.yaml')))}")

    return 0 if errors == 0 else 1


if __name__ == '__main__':
    exit(main())
