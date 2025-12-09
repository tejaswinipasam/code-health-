# Code Health Dashboard - GitHub Pages Setup Guide

This guide explains how to host your Code Health Dashboard on GitHub Pages with automated weekly updates.

## 🚀 Quick Start

### Prerequisites
- GitHub account
- Git installed locally
- Python files in your repository

### Setup Steps

#### 1. Prepare Your Repository

First, rename the dashboard file:
```powershell
Rename-Item "code-health-dashboard-1.html" "index.html"
```

Your repository structure should look like:
```
your-repo/
├── index.html                    # Your dashboard (renamed)
├── customer_servlet.py
├── invoice_dao.py
├── payment_processor.py
├── .github/
│   └── workflows/
│       └── update-dashboard.yml  # GitHub Action workflow
└── scripts/
    └── update-metrics.py         # Metrics update script
```

#### 2. Commit and Push to GitHub

```powershell
git add .
git commit -m "Set up code health dashboard with automation"
git push origin main
```

#### 3. Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/tejaswinipasam/code-health-`
2. Click **Settings** tab
3. Click **Pages** in the left sidebar
4. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: main
   - **Folder**: / (root)
5. Click **Save**

Your dashboard will be published at:
```
https://tejaswinipasam.github.io/code-health-/
```

*Note: It may take a few minutes for the site to become available.*

## 🤖 Automated Weekly Updates

### How It Works

The GitHub Action workflow (`.github/workflows/update-dashboard.yml`) automatically:

1. **Triggers every Monday at 9:00 AM UTC**
2. **Analyzes your Python code** using:
   - Radon (complexity analysis)
   - Coverage.py (test coverage)
   - Git log (code churn)
3. **Updates the dashboard** with fresh metrics
4. **Commits and pushes** changes back to the repository
5. **GitHub Pages automatically deploys** the updated dashboard

### Manual Trigger

You can also trigger the workflow manually:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select "Update Code Health Dashboard"
4. Click **Run workflow** → **Run workflow**

### Customizing the Schedule

Edit `.github/workflows/update-dashboard.yml`:

```yaml
on:
  schedule:
    # Every Monday at 9 AM UTC
    - cron: '0 9 * * 1'
    
    # Every day at midnight UTC
    # - cron: '0 0 * * *'
    
    # Every Friday at 5 PM UTC
    # - cron: '0 17 * * 5'
```

Cron syntax: `minute hour day-of-month month day-of-week`

## 📊 What Gets Updated

The automation updates:

1. **Last Updated Timestamp** - Current date/time
2. **Code Churn Table** - Git commit counts per file
3. **Test Coverage Chart** - Current coverage percentages
4. **Complexity Trends** - Average complexity scores

## 🔧 Customization

### Adding More Python Files

Edit `scripts/update-metrics.py`:

```python
python_files = [
    'customer_servlet.py',
    'invoice_dao.py',
    'payment_processor.py',
    'your_new_file.py',  # Add here
]
```

### Changing Analysis Tools

The script uses:
- **Radon** for complexity
- **Coverage.py** for test coverage
- **Git log** for churn

Install locally to test:
```powershell
pip install radon pylint coverage pytest
```

### Adjusting Thresholds

Edit the status logic in `scripts/update-metrics.py`:

```python
if changes > 30:
    status = 'status-high">Action Needed'
elif changes > 15:
    status = 'status-medium">Watch'
else:
    status = 'status-low">Healthy'
```

## 🐛 Troubleshooting

### Dashboard Not Updating

1. Check GitHub Actions logs:
   - Go to **Actions** tab
   - Click on the latest workflow run
   - Review the logs for errors

2. Common issues:
   - **Python files not found**: Ensure file paths are correct
   - **Git history too shallow**: Workflow uses `fetch-depth: 0`
   - **Permission denied**: Workflow has `contents: write` permission

### Site Not Loading

1. Verify GitHub Pages settings
2. Check that `index.html` is in the root directory
3. Wait 2-3 minutes after enabling Pages

### Coverage Analysis Failing

If you don't have tests yet, the script falls back to default values. To add real coverage:

1. Create test files (e.g., `test_*.py`)
2. Install pytest: `pip install pytest`
3. The workflow will automatically run them

## 📝 Testing Locally

Before pushing, test the update script:

```powershell
# Install dependencies
pip install radon pylint coverage pytest

# Run the update script
python scripts/update-metrics.py

# Check the updated index.html
# Open in browser to verify changes
```

## 🔐 Security Notes

- The workflow uses `GITHUB_TOKEN` automatically provided by GitHub
- No additional secrets needed
- The bot commits use: `github-actions[bot]@users.noreply.github.com`

## 📅 Next Steps

1. ✅ Rename `code-health-dashboard-1.html` to `index.html`
2. ✅ Push all files to GitHub
3. ✅ Enable GitHub Pages
4. ✅ Wait for the first Monday (or trigger manually)
5. 🎉 Watch your dashboard update automatically!

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Radon Documentation](https://radon.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

---

**Dashboard URL**: https://tejaswinipasam.github.io/code-health-/

**Repository**: https://github.com/tejaswinipasam/code-health-
