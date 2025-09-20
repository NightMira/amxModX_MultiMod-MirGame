
## 🏗️ **`.github/ISSUE_TEMPLATE/build_issue.md`**

```markdown
---
name: "🏗️ Build System Issue"
description: "Report problems with CI/CD, compilation, or versioning"
title: "🏗️ [Build]: "
labels: ["type-build", "priority-medium", "component-ci-cd"]
assignees: ""
---

## 🚨 Build Problem
**Workflow:** [build.yml / auto-label.yml / sync-labels.yml]
**Branch:** [e.g., dev, main, feature/x]
**Run ID:** [e.g., #123]

## 📋 Error Details
```yaml
# Paste relevant workflow section or error
```
## 🔧 Steps to Reproduce
- Push to branch: dev
- Action fails at: [specific step]
- Error: [description]

## 📊 Expected Behavior
Successful workflow execution

## 🏷️ Version Information
<!-- Run: python3 update_version.py info -->