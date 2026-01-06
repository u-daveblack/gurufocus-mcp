# Release Procedure

This document describes how to create a new release for the gurufocus-mcp project.

## Overview

The project uses:
- **bumpver** for version management across all packages
- **GitHub Actions** for automated publishing to PyPI
- **Semantic Versioning** (MAJOR.MINOR.PATCH)

## Pre-Release Checklist

Before releasing, ensure:

1. All tests pass: `uv run pytest`
2. Linting passes: `uv run ruff check .`
3. Type checking passes: `uv run mypy packages/gurufocus-api/gurufocus_api packages/gurufocus-mcp/gurufocus_mcp`
4. The `[Unreleased]` section in `CHANGELOG.md` documents all changes
5. README files are updated if features were added/removed

## Release Steps

### 1. Update CHANGELOG.md

Change the `[Unreleased]` header to include the new version and today's date:

```markdown
## [vX.Y.Z] - YYYY-MM-DD
```

Add a new empty `[Unreleased]` section above it:

```markdown
## [Unreleased]

## [vX.Y.Z] - YYYY-MM-DD
```

Commit this change:

```bash
git add CHANGELOG.md
git commit -m "docs: update changelog for vX.Y.Z"
```

### 2. Bump the Version

Use bumpver to update the version across all packages:

```bash
# For a patch release (0.5.1 -> 0.5.2)
uv run bumpver update --patch

# For a minor release (0.5.1 -> 0.6.0)
uv run bumpver update --minor

# For a major release (0.5.1 -> 1.0.0)
uv run bumpver update --major
```

This will:
- Update version in all three `pyproject.toml` files:
  - `/pyproject.toml` (workspace root)
  - `/packages/gurufocus-api/pyproject.toml`
  - `/packages/gurufocus-mcp/pyproject.toml`
- Create a commit: `chore: bump version X.Y.Z -> A.B.C`
- Create a git tag: `vA.B.C` (the `v` prefix is configured via `tag_name = "v{version}"` in pyproject.toml, which is required for the GitHub Actions publish workflow to trigger)

### 3. Push to Trigger Release

Push the commits and tag to GitHub:

```bash
git push origin main --tags
```

### 4. Automated Publishing

The GitHub Actions workflow (`.github/workflows/publish.yml`) will automatically:

1. Trigger on the `v*` tag push
2. Build both packages using `uv build --all-packages`
3. Publish to PyPI:
   - `gurufocus-api`
   - `gurufocus-mcp`

Publishing uses OIDC trusted publishing (no API tokens needed).

### 5. Verify Release

After the workflow completes:

1. Check the [GitHub Actions](../../actions) tab for successful completion
2. Verify packages on PyPI:
   - https://pypi.org/project/gurufocus-api/
   - https://pypi.org/project/gurufocus-mcp/
3. Optionally create a GitHub Release with release notes from the changelog

## Troubleshooting

### bumpver not found

Ensure dependencies are installed:

```bash
uv sync --all-packages
```

### Publishing fails

- Check GitHub Actions logs for detailed error messages
- Verify PyPI trusted publisher configuration in repository settings
- Ensure the tag matches the expected pattern (`v*`)

### Version mismatch

If versions get out of sync, manually update all three `pyproject.toml` files to match, then run bumpver for the next release.
