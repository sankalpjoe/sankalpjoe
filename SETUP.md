# Sankalp's observatory

A graphical GitHub profile with original, repository-hosted SVG artwork. Its public-data snapshot is already included, so the profile displays immediately after the files are published together.

## Publish

Copy the contents of this repository into **sankalpjoe/sankalpjoe**, preserving the `assets`, `data`, `scripts`, `tests` and `.github` directories. Replace the existing `readme.md` and old snake workflow. Commit to `main`. The new workflow runs on that push and then **every 30 minutes**, at minutes 17 and 47 of each UTC hour. It also supports **Actions → Refresh profile → Run workflow**.

The workflow uses GitHub's automatically provided `GITHUB_TOKEN` with `contents: write` for this profile repository. No personal token, external stats host or extra secret is required. If branch rules prevent bot pushes, the workflow will fail visibly; grant the workflow the appropriate repository policy or use a pull-request-based update process. GitHub can delay scheduled runs, or disable schedules after extended inactivity. Existing graphics remain visible when a refresh fails.

## Edit

### When a repository becomes private

The next successful online refresh rebuilds the homepage from GitHub's current public repository list. Repositories that become private, are deleted or leave this account disappear from featured panels, the repository index, counts, language totals and the saved public-data snapshot. Their previously generated desktop and mobile card files are also removed. Public repositories that return to the list are included again, and curated panels reappear when applicable.

GitHub schedules can be delayed, so this is not an instant visibility-change notification or a guaranteed 30-minute deadline. To refresh sooner, open **Actions → Refresh profile → Run workflow**. If GitHub fails to provide the public list, the previous homepage remains until a successful run. Offline rendering cannot detect visibility changes. If a listed repository becomes inaccessible with a 404 while its languages are being read, it is excluded from that refresh instead of blocking cleanup of the page.

This updates the current generated homepage and assets; existing commit history and the manually curated descriptions in `profile.json` are not erased.

### Customize the profile

- `profile.json`: featured projects, copy, illustration choices and accent colors. Featured cards require a public repository with content. Every other public repository receives an automatically generated panel, including clearly labelled empty and archived repositories. Rename a featured repository here when its GitHub name changes.
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

Checks include public-to-private transitions and reappearance, obsolete-card cleanup, visibility changes during API requests, pagination, snapshot validation, language exclusions, failed-request behavior, SVG validity and referenced-asset completeness.

GitHub references: [relative image paths](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax), [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token), [scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
