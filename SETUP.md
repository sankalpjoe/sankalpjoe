# Sankalp's observatory

A graphical GitHub profile with original, repository-hosted SVG artwork. Its public-data snapshot is already included, so the profile displays immediately after the files are published together.

## Publish

Copy the contents of this repository into **sankalpjoe/sankalpjoe**, preserving the `assets`, `data`, `scripts`, `tests` and `.github` directories. Replace the existing `readme.md` and old snake workflow. Commit to `main`. The new workflow runs on that push and then daily at **04:23 UTC / 09:53 IST**; it also supports **Actions → Refresh profile → Run workflow**.

The workflow uses GitHub's automatically provided `GITHUB_TOKEN` with `contents: write` for this profile repository. No personal token, external stats host or extra secret is required. If branch rules prevent bot pushes, the workflow will fail visibly; grant the workflow the appropriate repository policy or use a pull-request-based update process. GitHub can delay scheduled runs, or disable schedules after extended inactivity. Existing graphics remain visible when a refresh fails.

## Edit

- `profile.json`: featured projects, copy, illustration choices and accent colors. Only public repositories present in the fetched snapshot are featured. An absent or empty repository is removed from the featured panels on refresh.
- `scripts/render_profile.py`: layout, introduction, visual styling and accessible mobile artwork. SVGs have no scripts, remote fonts, external images or embedded HTML. Motion respects `prefers-reduced-motion`.
- `data/public-repos.json`: source snapshot with its retrieval timestamp. Generated automatically.
- `readme.md` and `assets/`: generated outputs. Change their sources to keep edits after refresh.

Run `python scripts/refresh.py` to fetch current public data and rebuild. Set `GITHUB_TOKEN` in the environment if you need authenticated rate limits. Run `python scripts/refresh.py --offline` to rebuild from the saved snapshot. Python 3.10+ is sufficient; there are no third-party dependencies.

## What the numbers mean

The index includes **every public repository owned by sankalpjoe**, with pagination. Repository state comes from GitHub. New public repositories automatically join the index; featured panels are intentionally curated. Repository totals include this profile. Project counts and project stars exclude this profile and forks. “Projects with content” uses GitHub's repository `size` and includes archived work; it is not a claim that a project is complete or maintained.

The language graphic sums GitHub's language-byte counts across public repositories, excluding forks, archived repositories and this profile. Notebook bytes include notebook JSON and outputs. The percentages represent stored content, not skill, time spent, commits or lines of code. Missing language data is not inferred from prose.

Descriptions were checked against the public repository READMEs. Delhi uses a **synthetic** dataset; qcbm-indian uses **Amazon Braket**; QCBM-Options-Pricing is **archived**, with options-pricing expansion described as future work. billyzer was empty at the initial snapshot. The illustrations are original conceptual artwork, not screenshots, benchmark results or scientific plots.

Every rendered image is stored in this repository and has a mobile composition plus alternative text. The complete repository index remains ordinary, selectable text. All project panels link to their corresponding GitHub repository. Placeholder social/contact links have been removed; add verified links when available.

## Verify

`python -m unittest discover -s tests -v`

Checks include new/deleted repository handling, pagination, snapshot validation, language exclusions, failed-request behavior, SVG validity and referenced-asset completeness.

GitHub references: [relative image paths](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token), [scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
