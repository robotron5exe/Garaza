# Deployment Instructions

## Making the Website Live on GitHub Pages

Your code is currently on the feature branch: `claude/maribor-real-estate-research-011CUxxkn1h8aPMJtw3H4Euu`

To deploy to GitHub Pages, follow these steps:

### Option 1: Merge via GitHub UI (Recommended)

1. **Go to GitHub**: https://github.com/robotron5exe/Garaza

2. **Create a Pull Request**:
   - Click "Pull requests" tab
   - Click "New pull request"
   - Base: `main` (or create it if it doesn't exist)
   - Compare: `claude/maribor-real-estate-research-011CUxxkn1h8aPMJtw3H4Euu`
   - Click "Create pull request"
   - Add title: "Deploy website with comprehensive analysis"
   - Click "Create pull request"

3. **Merge the PR**:
   - Review the changes
   - Click "Merge pull request"
   - Click "Confirm merge"

4. **Configure GitHub Pages**:
   - Go to repository Settings
   - Click "Pages" in the left sidebar
   - Source: Deploy from branch
   - Branch: `main`
   - Folder: `/ (root)` or `/web` depending on setup
   - Click "Save"

5. **Wait 1-2 minutes** for deployment

6. **Visit your site**:
   - If repo is `robotron5exe/Garaza`:
     - https://robotron5exe.github.io/Garaza/web/
   - If repo is `garaza.github.io`:
     - https://robotron5exe.github.io/web/
     - Or https://robotron5exe.github.io/ (if web is root)

### Option 2: Deploy to gh-pages branch

```bash
# Create gh-pages branch with only the web directory
git checkout claude/maribor-real-estate-research-011CUxxkn1h8aPMJtw3H4Euu
git subtree push --prefix web origin gh-pages
```

Then configure GitHub Pages to use the `gh-pages` branch.

### Option 3: Use GitHub Actions (Advanced)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./web
```

## Current Status

✅ Website code is ready in `web/` directory
✅ Data is integrated from research
✅ Code is pushed to feature branch
❌ Not yet deployed to GitHub Pages (requires merge to main)

## Testing Locally

Before deploying, test locally:

```bash
cd web
python server.py
# Open http://localhost:8000
```

## Website Features

Once deployed, users can:
- View interactive price charts (2005-2025)
- Analyze garage prices with detailed statistics
- Compare garages, apartments, and houses
- Filter by property type and time period
- See real data from comprehensive research

## Troubleshooting

**404 Error**: Check GitHub Pages settings
**Blank page**: Check browser console for errors
**Old data**: Clear browser cache (Ctrl+F5)
**No charts**: Ensure Chart.js CDN is accessible

## URL Structure

After deployment:
- Homepage: `/` or `/web/` (index.html)
- All assets load relatively from same directory
- No server-side code needed (static site)

## Updating Website Data

To update the website with new data:

```bash
# 1. Update JSON files in data/raw/
# 2. Regenerate website data
python scripts/generate_web_data.py

# 3. Commit and push
git add web/data.js
git commit -m "Update website data"
git push origin your-branch-name

# 4. Merge to main via PR (repeat deployment steps)
```

---

**Note**: The website works standalone - just the `web/` directory is needed for GitHub Pages. All the Python analysis tools are bonus features for developers.
