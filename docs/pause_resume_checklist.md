# Pause / Resume Checklist

## Before Pausing
- Commit all current work
- Push to private GitHub repository
- Add LICENSE
- Add PROJECT_STATUS.md
- Add docs folder
- Tag current state

Suggested commands:

```bash
git status
git add .
git commit -m "Protect and document Phase 2 MVP checkpoint"
git push
git tag phase2-mvp
git push origin phase2-mvp
```

## When Resuming
1. Read PROJECT_STATUS.md
2. Run Docker locally
3. Check README
4. Review automation roadmap
5. Do cleanup audit before adding features
6. Do not start scraping immediately
