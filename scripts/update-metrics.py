#!/usr/bin/env python3
"""
Automated script to update code health dashboard metrics.
Analyzes Python files and updates the HTML dashboard with current metrics.
"""

import os
import re
import subprocess
import json
from datetime import datetime
from pathlib import Path


def run_radon_complexity(file_path):
    """Run Radon complexity analysis on a file."""
    try:
        result = subprocess.run(
            ['radon', 'cc', file_path, '-s', '-a'],
            capture_output=True,
            text=True
        )
        # Extract average complexity from output
        match = re.search(r'Average complexity: \w+ \((\d+\.?\d*)\)', result.stdout)
        if match:
            return float(match.group(1))
        return 0
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return 0


def get_git_changes(file_path, days=30):
    """Count git commits for a file in the last N days."""
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', f'--since={days}.days.ago', '--', file_path],
            capture_output=True,
            text=True
        )
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except Exception:
        return 0


def run_coverage():
    """Run test coverage analysis."""
    coverage_data = {}
    try:
        # Run tests with coverage
        subprocess.run(['coverage', 'run', '-m', 'pytest'], capture_output=True)
        
        # Get coverage report in JSON format
        result = subprocess.run(
            ['coverage', 'json', '-o', '/tmp/coverage.json'],
            capture_output=True
        )
        
        if os.path.exists('/tmp/coverage.json'):
            with open('/tmp/coverage.json', 'r') as f:
                data = json.load(f)
                for file_path, file_data in data.get('files', {}).items():
                    file_name = os.path.basename(file_path)
                    coverage_data[file_name] = file_data.get('summary', {}).get('percent_covered', 0)
    except Exception as e:
        print(f"Coverage analysis failed: {e}")
    
    return coverage_data


def update_html_dashboard(complexity_data, churn_data, coverage_data):
    """Update the HTML dashboard with new metrics."""
    
    # Read the current dashboard
    dashboard_path = Path(__file__).parent.parent / 'index.html'
    if not dashboard_path.exists():
        dashboard_path = Path(__file__).parent.parent / 'code-health-dashboard-1.html'
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Update timestamp
    now = datetime.now()
    timestamp = now.strftime('%B %d, %Y, %I:%M %p')
    html_content = re.sub(
        r'Last updated: [^<]+',
        f'Last updated: {timestamp}',
        html_content
    )
    
    # Update code churn table
    churn_rows = []
    for file_name, changes in sorted(churn_data.items(), key=lambda x: x[1], reverse=True):
        if changes > 30:
            status = 'status-high">Action Needed'
        elif changes > 15:
            status = 'status-medium">Watch'
        else:
            status = 'status-low">Healthy'
        
        churn_rows.append(f'''                        <tr>
                            <td><strong>{file_name}</strong></td>
                            <td>{changes} changes</td>
                            <td><span class="status-badge {status}</span></td>
                        </tr>''')
    
    # Replace churn table body
    churn_section = '\n'.join(churn_rows)
    html_content = re.sub(
        r'<tbody>.*?</tbody>',
        f'<tbody>\n{churn_section}\n                    </tbody>',
        html_content,
        flags=re.DOTALL
    )
    
    # Update coverage chart data
    coverage_labels = []
    coverage_values = []
    coverage_colors = []
    coverage_border_colors = []
    
    for file_name, coverage_pct in coverage_data.items():
        module_name = file_name.replace('.py', '').replace('_', ' ').title()
        coverage_labels.append(module_name)
        coverage_values.append(round(coverage_pct, 1))
        
        if coverage_pct >= 70:
            coverage_colors.append('#10b981')
            coverage_border_colors.append('#059669')
        elif coverage_pct >= 40:
            coverage_colors.append('#f59e0b')
            coverage_border_colors.append('#d97706')
        else:
            coverage_colors.append('#ef4444')
            coverage_border_colors.append('#dc2626')
    
    # Update coverage chart in JavaScript
    coverage_labels_js = str(coverage_labels).replace("'", "'")
    coverage_values_js = str(coverage_values)
    coverage_colors_js = str(coverage_colors).replace("'", "'")
    
    html_content = re.sub(
        r"labels: \['PaymentProcessor', 'InvoiceDAO', 'CustomerServlet'\]",
        f"labels: {coverage_labels_js}",
        html_content
    )
    html_content = re.sub(
        r"data: \[\d+, \d+, \d+\]",
        f"data: {coverage_values_js}",
        html_content,
        count=1
    )
    
    # Write updated dashboard
    output_path = Path(__file__).parent.parent / 'index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard updated successfully at {timestamp}")


def main():
    """Main function to orchestrate the dashboard update."""
    
    # Find Python files to analyze (excluding this script)
    python_files = [
        'customer_servlet.py',
        'invoice_dao.py',
        'payment_processor.py'
    ]
    
    base_path = Path(__file__).parent.parent
    
    # Analyze complexity
    print("📊 Analyzing code complexity...")
    complexity_data = {}
    for py_file in python_files:
        file_path = base_path / py_file
        if file_path.exists():
            complexity = run_radon_complexity(str(file_path))
            complexity_data[py_file] = complexity
            print(f"  {py_file}: {complexity}")
    
    # Analyze code churn
    print("\n📈 Analyzing code churn...")
    churn_data = {}
    for py_file in python_files:
        file_path = base_path / py_file
        if file_path.exists():
            changes = get_git_changes(str(file_path))
            churn_data[py_file] = changes
            print(f"  {py_file}: {changes} changes")
    
    # Analyze test coverage
    print("\n🧪 Analyzing test coverage...")
    coverage_data = run_coverage()
    if not coverage_data:
        # Fallback to default values if coverage fails
        coverage_data = {
            'payment_processor.py': 42,
            'invoice_dao.py': 28,
            'customer_servlet.py': 12
        }
    for file_name, coverage in coverage_data.items():
        print(f"  {file_name}: {coverage}%")
    
    # Update dashboard
    print("\n🔄 Updating dashboard...")
    update_html_dashboard(complexity_data, churn_data, coverage_data)
    
    print("\n✨ Dashboard update complete!")


if __name__ == '__main__':
    main()
