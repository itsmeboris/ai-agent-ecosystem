#!/usr/bin/env python3
"""
Parser for structured agent progress outputs
Supports all three formats: Markdown, YAML, and Hybrid
"""

import re
import yaml
import sys
from datetime import datetime
from typing import Dict, List, Optional, Union
from pathlib import Path


class AgentProgressParser:
    """Parse agent progress entries from SHARED_PROGRESS.md"""

    def __init__(self, progress_file: str = "workspaces/SHARED_PROGRESS.md"):
        self.progress_file = Path(progress_file)

    def parse_all(self) -> List[Dict]:
        """Parse all entries from the progress file"""
        if not self.progress_file.exists():
            print(f"Warning: {self.progress_file} not found", file=sys.stderr)
            return []

        content = self.progress_file.read_text()
        entries = []

        # Split by agent entry headers (look for ## YYYY-MM-DD or YAML sections)
        # Use a more sophisticated split that preserves structure
        current_entry = []
        in_yaml = False

        for line in content.split('\n'):
            # Start of YAML frontmatter
            if line.strip() == '---' and not in_yaml:
                if current_entry:
                    entry = self._parse_entry('\n'.join(current_entry))
                    if entry:
                        entries.append(entry)
                    current_entry = []
                in_yaml = True
                current_entry.append(line)
            # End of YAML frontmatter
            elif line.strip() == '---' and in_yaml:
                in_yaml = False
                current_entry.append(line)
            # Start of markdown entry
            elif re.match(r'^## \d{4}-\d{2}-\d{2}', line):
                if current_entry and not in_yaml:
                    entry = self._parse_entry('\n'.join(current_entry))
                    if entry:
                        entries.append(entry)
                    current_entry = []
                current_entry.append(line)
            else:
                current_entry.append(line)

        # Don't forget the last entry
        if current_entry:
            entry = self._parse_entry('\n'.join(current_entry))
            if entry:
                entries.append(entry)

        return entries

    def _parse_entry(self, content: str) -> Optional[Dict]:
        """Parse a single entry (auto-detects format)"""
        content = content.strip()
        if not content:
            return None

        # Check if it's YAML format (starts with ---)
        if content.startswith('---'):
            # Check if it's hybrid (has markdown after YAML)
            if re.search(r'---\n\n## \d{4}-\d{2}-\d{2}', content):
                return self._parse_hybrid_entry(content)
            else:
                return self._parse_yaml_entry(content)
        # Check if it's markdown format
        elif re.match(r'^## \d{4}-\d{2}-\d{2}', content):
            return self._parse_markdown_entry(content)

        return None

    def _parse_yaml_entry(self, content: str) -> Dict:
        """Parse YAML format entry"""
        # Extract YAML between --- markers
        yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if yaml_match:
            try:
                return yaml.safe_load(yaml_match.group(1))
            except yaml.YAMLError as e:
                print(f"Warning: YAML parse error: {e}", file=sys.stderr)
                return {}
        return {}

    def _parse_markdown_entry(self, content: str) -> Dict:
        """Parse markdown format entry"""
        entry = {}

        # Extract header: ## 2025-11-30 14:30 - @agent-name: Task Title
        header_match = re.match(
            r'^## (\d{4}-\d{2}-\d{2})(?: (\d{2}:\d{2}))? - @([\w-]+): (.+)$',
            content.split('\n')[0],
            re.MULTILINE
        )

        if header_match:
            date = header_match.group(1)
            time = header_match.group(2) or "00:00"
            entry['timestamp'] = f"{date} {time}"
            entry['agent'] = header_match.group(3)
            entry['task_title'] = header_match.group(4)

        # Extract status
        status_match = re.search(r'\*\*Status\*\*:\s*([^\n|]+)', content)
        if status_match:
            status_text = status_match.group(1).strip()
            if '✅' in status_text or 'Complete' in status_text:
                entry['status'] = 'complete'
            elif '🔄' in status_text or 'Progress' in status_text:
                entry['status'] = 'in_progress'
            elif '⚠️' in status_text or 'Blocked' in status_text:
                entry['status'] = 'blocked'
            elif '❌' in status_text or 'Failed' in status_text:
                entry['status'] = 'failed'
            elif '🚧' in status_text or 'Paused' in status_text:
                entry['status'] = 'paused'
            elif '📋' in status_text or 'Planned' in status_text:
                entry['status'] = 'planned'

        # Extract task ID
        task_id_match = re.search(r'\*\*Task ID\*\*:\s*(\S+)', content)
        if task_id_match:
            entry['task_id'] = task_id_match.group(1)

        # Extract duration
        duration_match = re.search(r'\*\*Duration\*\*:\s*(?:(\d+)h\s*)?(?:(\d+)m)?', content)
        if duration_match:
            hours = int(duration_match.group(1) or 0)
            minutes = int(duration_match.group(2) or 0)
            entry['duration_minutes'] = hours * 60 + minutes

        # Extract progress percentage
        progress_match = re.search(r'\*\*Progress\*\*:\s*(\d+)%', content)
        if progress_match:
            entry['progress_percent'] = int(progress_match.group(1))

        # Extract deliverables
        deliverables = []
        deliverables_section = re.search(
            r'\*\*Deliverables\*\*:\n((?:^[ \t]*-.*\n?)+)',
            content,
            re.MULTILINE
        )
        if deliverables_section:
            for line in deliverables_section.group(1).split('\n'):
                if line.strip().startswith('-'):
                    # Parse: - `path` (type: X) - description
                    deliv_match = re.search(r'`([^`]+)`(?:\s*\(type:\s*(\w+)\))?\s*-?\s*(.*)', line)
                    if deliv_match:
                        deliverables.append({
                            'path': deliv_match.group(1),
                            'type': deliv_match.group(2) or 'unknown',
                            'description': deliv_match.group(3).strip()
                        })
        if deliverables:
            entry['deliverables'] = deliverables

        # Extract metrics
        metrics = {}
        metrics_section = re.search(
            r'\*\*Metrics\*\*[^:]*?:\n((?:^[ \t]*-.*\n?)+)',
            content,
            re.MULTILINE
        )
        if metrics_section:
            for line in metrics_section.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip('- ').strip()
                    value = value.strip().rstrip('%')
                    # Try to convert to number
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                    metrics[key] = value
        if metrics:
            entry['metrics'] = metrics

        return entry

    def _parse_hybrid_entry(self, content: str) -> Dict:
        """Parse hybrid format (YAML frontmatter + markdown)"""
        # Parse YAML frontmatter
        entry = self._parse_yaml_entry(content)

        # Parse markdown body for additional context
        markdown_section = re.search(r'---\n\n(.+)', content, re.DOTALL)
        if markdown_section:
            markdown_content = markdown_section.group(1)

            # If YAML didn't have task_title, extract from markdown header
            if 'task_title' not in entry:
                header_match = re.match(
                    r'^## [\d-]+ [\d:]+ - @[\w-]+: (.+)$',
                    markdown_content.split('\n')[0]
                )
                if header_match:
                    entry['task_title'] = header_match.group(1)

            # Extract context section if not in YAML
            context_match = re.search(r'### Context\n(.+?)(?=\n###|\Z)', markdown_content, re.DOTALL)
            if context_match and 'context' not in entry:
                entry['context'] = context_match.group(1).strip()

            # Extract deliverables if not in YAML
            if 'deliverables' not in entry:
                markdown_entry = self._parse_markdown_entry(markdown_content)
                if 'deliverables' in markdown_entry:
                    entry['deliverables'] = markdown_entry['deliverables']

        return entry

    def filter_by_agent(self, entries: List[Dict], agent_name: str) -> List[Dict]:
        """Filter entries by agent name"""
        return [e for e in entries if e.get('agent') == agent_name]

    def filter_by_status(self, entries: List[Dict], status: str) -> List[Dict]:
        """Filter entries by status"""
        return [e for e in entries if e.get('status') == status]

    def filter_by_date_range(self, entries: List[Dict], start_date: str, end_date: str) -> List[Dict]:
        """Filter entries by date range (YYYY-MM-DD format)"""
        filtered = []
        for entry in entries:
            timestamp = entry.get('timestamp', '')
            if timestamp:
                entry_date = timestamp.split()[0]  # Get just the date part
                if start_date <= entry_date <= end_date:
                    filtered.append(entry)
        return filtered

    def get_metrics_summary(self, entries: List[Dict]) -> Dict:
        """Generate summary metrics from entries"""
        summary = {
            'total_entries': len(entries),
            'by_status': {},
            'by_agent': {},
            'total_duration_minutes': 0,
            'total_deliverables': 0,
            'avg_test_coverage': 0
        }

        coverage_count = 0
        coverage_sum = 0

        for entry in entries:
            # Count by status
            status = entry.get('status', 'unknown')
            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1

            # Count by agent
            agent = entry.get('agent', 'unknown')
            summary['by_agent'][agent] = summary['by_agent'].get(agent, 0) + 1

            # Sum duration
            duration = entry.get('duration_minutes', 0)
            if isinstance(duration, (int, float)):
                summary['total_duration_minutes'] += duration

            # Count deliverables
            deliverables = entry.get('deliverables', [])
            summary['total_deliverables'] += len(deliverables)

            # Average test coverage
            metrics = entry.get('metrics', {})
            coverage = None
            for key in ['test_coverage', 'Test Coverage', 'test_coverage_percent']:
                if key in metrics:
                    coverage = metrics[key]
                    break

            if coverage is not None and isinstance(coverage, (int, float)):
                coverage_sum += coverage
                coverage_count += 1

        if coverage_count > 0:
            summary['avg_test_coverage'] = round(coverage_sum / coverage_count, 1)

        return summary

    def export_to_json(self, entries: List[Dict], output_file: str):
        """Export entries to JSON file"""
        import json
        with open(output_file, 'w') as f:
            json.dump(entries, f, indent=2, default=str)

    def export_to_csv(self, entries: List[Dict], output_file: str):
        """Export entries to CSV file"""
        import csv

        if not entries:
            return

        # Flatten nested structures for CSV
        flattened = []
        for entry in entries:
            flat = {
                'timestamp': entry.get('timestamp', ''),
                'agent': entry.get('agent', ''),
                'task_id': entry.get('task_id', ''),
                'task_title': entry.get('task_title', ''),
                'status': entry.get('status', ''),
                'duration_minutes': entry.get('duration_minutes', ''),
                'progress_percent': entry.get('progress_percent', ''),
                'num_deliverables': len(entry.get('deliverables', [])),
            }

            # Add metrics as separate columns
            metrics = entry.get('metrics', {})
            for key, value in metrics.items():
                flat[f'metric_{key}'] = value

            flattened.append(flat)

        # Write CSV
        if flattened:
            keys = flattened[0].keys()
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(flattened)

    def print_summary_report(self, entries: List[Dict]):
        """Print a human-readable summary report"""
        if not entries:
            print("No entries found.")
            return

        summary = self.get_metrics_summary(entries)

        print("=" * 60)
        print("AGENT PROGRESS SUMMARY REPORT")
        print("=" * 60)
        print()

        print(f"📊 Total Entries: {summary['total_entries']}")
        print(f"⏱️  Total Duration: {summary['total_duration_minutes']} minutes ({summary['total_duration_minutes'] / 60:.1f} hours)")
        print(f"📦 Total Deliverables: {summary['total_deliverables']}")
        if summary['avg_test_coverage'] > 0:
            print(f"✅ Average Test Coverage: {summary['avg_test_coverage']}%")
        print()

        print("📈 By Status:")
        for status, count in sorted(summary['by_status'].items()):
            emoji = {'complete': '✅', 'in_progress': '🔄', 'blocked': '⚠️', 'failed': '❌', 'paused': '🚧', 'planned': '📋'}.get(status, '📍')
            print(f"  {emoji} {status.replace('_', ' ').title()}: {count}")
        print()

        print("🤖 By Agent (Top 10):")
        sorted_agents = sorted(summary['by_agent'].items(), key=lambda x: x[1], reverse=True)[:10]
        for agent, count in sorted_agents:
            print(f"  {agent}: {count} tasks")
        print()

        # Recent activity
        print("🕐 Recent Activity (Last 5 entries):")
        recent = sorted(entries, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]
        for entry in recent:
            timestamp = entry.get('timestamp', 'N/A')
            agent = entry.get('agent', 'unknown')
            task = entry.get('task_title', 'Untitled')
            status = entry.get('status', 'unknown')
            emoji = {'complete': '✅', 'in_progress': '🔄', 'blocked': '⚠️', 'failed': '❌', 'paused': '🚧', 'planned': '📋'}.get(status, '📍')
            print(f"  {emoji} {timestamp} - @{agent}: {task}")
        print()
        print("=" * 60)


def main():
    """Main CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description='Parse and analyze agent progress')
    parser.add_argument('file', nargs='?', default='workspaces/SHARED_PROGRESS.md',
                        help='Path to SHARED_PROGRESS.md (default: workspaces/SHARED_PROGRESS.md)')
    parser.add_argument('--agent', help='Filter by agent name')
    parser.add_argument('--status', help='Filter by status (complete, in_progress, blocked, failed)')
    parser.add_argument('--start-date', help='Filter by start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Filter by end date (YYYY-MM-DD)')
    parser.add_argument('--json', help='Export to JSON file')
    parser.add_argument('--csv', help='Export to CSV file')
    parser.add_argument('--quiet', action='store_true', help='Suppress summary output (for exports only)')

    args = parser.parse_args()

    # Parse entries
    progress_parser = AgentProgressParser(args.file)
    entries = progress_parser.parse_all()

    if not entries:
        print(f"No entries found in {args.file}", file=sys.stderr)
        sys.exit(1)

    # Apply filters
    if args.agent:
        entries = progress_parser.filter_by_agent(entries, args.agent)
        if not entries:
            print(f"No entries found for agent: {args.agent}", file=sys.stderr)
            sys.exit(1)

    if args.status:
        entries = progress_parser.filter_by_status(entries, args.status)
        if not entries:
            print(f"No entries found with status: {args.status}", file=sys.stderr)
            sys.exit(1)

    if args.start_date and args.end_date:
        entries = progress_parser.filter_by_date_range(entries, args.start_date, args.end_date)
        if not entries:
            print(f"No entries found between {args.start_date} and {args.end_date}", file=sys.stderr)
            sys.exit(1)

    # Export if requested
    if args.json:
        progress_parser.export_to_json(entries, args.json)
        if not args.quiet:
            print(f"Exported {len(entries)} entries to {args.json}")

    if args.csv:
        progress_parser.export_to_csv(entries, args.csv)
        if not args.quiet:
            print(f"Exported {len(entries)} entries to {args.csv}")

    # Print summary unless quiet mode
    if not args.quiet:
        progress_parser.print_summary_report(entries)


if __name__ == '__main__':
    main()
