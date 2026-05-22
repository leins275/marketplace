# ITS Marketplace

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace for the ITS team. It packages the skills and tools our engineers rely on into six installable toolkits, so every teammate gets the same standards with a single command.

The skill files are **vendored** — copied into this repo from their upstream repositories — and refreshed on demand with `make sync`. [`sources.json`](sources.json) records exactly where every skill comes from, so updates are traceable and reviewed before they reach the whole team.

## Quick start

```text
/plugin marketplace add leins275/marketplace
/plugin install django-toolkit@its-marketplace
```

> The marketplace lives at [`leins275/marketplace`](https://github.com/leins275/marketplace) on GitHub. You can also add it from a local clone:
> `/plugin marketplace add /path/to/marketplace`

## Browsing and managing plugins

Plugins are managed from inside a Claude Code session with `/plugin` commands — there is no `claude plugin` CLI.

**See everything available** — `/plugin` opens an interactive browser (Discover / Installed / Marketplaces / Errors tabs); the **Discover** tab lists every toolkit in this marketplace with its description and context cost:

```text
/plugin
```

**Everyday commands:**

```text
/plugin marketplace list                      # marketplaces you have added
/plugin install <toolkit>@its-marketplace     # install a toolkit
/plugin uninstall <toolkit>@its-marketplace   # remove it
/plugin disable <toolkit>@its-marketplace     # keep it installed but turn it off
/plugin enable <toolkit>@its-marketplace      # turn it back on
/reload-plugins                               # apply changes without restarting
```

`<toolkit>` is one of `django-toolkit`, `testing-toolkit`, `browser-toolkit`, `frontend-toolkit`, `devops-toolkit`, `content-toolkit`.

**Install for the whole team** — add `--scope project` to record the choice in the repo's `.claude/settings.json`, so every collaborator is offered the toolkit:

```text
/plugin install django-toolkit@its-marketplace --scope project
```

**Pull the latest** — after new skill versions are merged here (see [Updating skills from upstream](#updating-skills-from-upstream)), refresh your session with:

```text
/plugin marketplace update its-marketplace
/reload-plugins
```

**Stop using the marketplace:**

```text
/plugin marketplace remove its-marketplace
```

The toolkits are **skill-based**: once installed and enabled, their skills activate automatically when relevant — there are no commands to memorize. Check `/plugin` → **Installed** to confirm a toolkit is active.

## What's inside

Six toolkits — **13 skills** plus a bundled **MCP server**:

| Toolkit | Bundles | Use it for |
| --- | --- | --- |
| [`django-toolkit`](plugins/django-toolkit) | django-patterns, django-security, django-verification | Building, hardening and verifying Django services |
| [`testing-toolkit`](plugins/testing-toolkit) | python-testing-patterns, e2e-testing-patterns, webapp-testing | Pytest, end-to-end and live web-app testing |
| [`browser-toolkit`](plugins/browser-toolkit) | Playwright MCP server | Driving a real browser — navigation, clicks, forms, screenshots |
| [`frontend-toolkit`](plugins/frontend-toolkit) | frontend-design, ui-ux-pro-max | Designing and building polished UIs |
| [`devops-toolkit`](plugins/devops-toolkit) | docker-patterns, postgres-patterns, devops-rollout-plan | Containers, databases and safe rollouts |
| [`content-toolkit`](plugins/content-toolkit) | copywriting, find-skills | Marketing copy and discovering new skills |

## Upstream sources

Every skill is vendored from an upstream repository. [`sources.json`](sources.json) is the source of truth:

| Skill | Upstream |
| --- | --- |
| django-patterns, django-security, django-verification | [affaan-m/ECC](https://github.com/affaan-m/ECC) |
| docker-patterns, postgres-patterns | [affaan-m/ECC](https://github.com/affaan-m/ECC) |
| python-testing-patterns, e2e-testing-patterns | [wshobson/agents](https://github.com/wshobson/agents) |
| webapp-testing, frontend-design | [anthropics/skills](https://github.com/anthropics/skills) |
| ui-ux-pro-max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) |
| copywriting | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) |
| find-skills | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| devops-rollout-plan | _local — no upstream_ |

## Updating skills from upstream

```text
make sync     # re-pull every skill from its upstream repo into plugins/*/skills/
make diff     # review what changed before committing
```

`make sync` shallow-clones each upstream repo, copies the current skill directories in, and prints the commit it pulled from. Review the diff, commit, and push — the update reaches the team only when you push, never silently.

To refresh a single skill: `uv run scripts/sync.py django-patterns`.

### Automated sync (GitHub Actions)

The `sync-skills` workflow does this for you on a weekly schedule: it runs `make sync` and, if anything changed, opens a **pull request** with the diff. New skill versions reach the team only when someone reviews and merges that PR — the automation handles the clone-copy-diff grunt work, not the rollout decision. You can also run it on demand from the repo's **Actions** tab with **Run workflow**.

One-time setup in the GitHub repo — **Settings → Actions → General → Workflow permissions**:

1. Select **Read and write permissions**.
2. Tick **Allow GitHub Actions to create and approve pull requests**.

No tokens to manage: the workflow authenticates with the built-in `GITHUB_TOKEN`. Change the cadence by editing the `cron:` line in [`.github/workflows/sync-skills.yml`](.github/workflows/sync-skills.yml).

## Working with the marketplace

```text
make help        # list available targets
make validate    # check every JSON manifest parses
make list        # list plugins and the skills they bundle
make tree        # print the full repository layout
```

## Layout

```text
marketplace/
├── .claude-plugin/
│   └── marketplace.json        # the registry — lists every plugin
├── plugins/
│   └── <toolkit>/
│       ├── .claude-plugin/plugin.json
│       ├── skills/             # vendored skills — refreshed by `make sync`
│       ├── .mcp.json           # bundled MCP server (browser-toolkit)
│       └── README.md
├── sources.json                # upstream repo + path for every vendored skill
├── scripts/sync.py             # re-vendors skills from sources.json
├── Makefile
└── .github/workflows/         # CI: validate manifests + scheduled upstream sync
```

## Adding a skill

1. Register its upstream in [`sources.json`](sources.json) (or `"source": "local"` if there is none).
2. Run `uv run scripts/sync.py <name>` to vendor it (local skills are added by hand under `plugins/<toolkit>/skills/<name>/`).
3. Run `make validate`.

## Adding a plugin

1. Create `plugins/<name>/` with a `.claude-plugin/plugin.json`, plus a `skills/` directory and/or a `.mcp.json` (to bundle an MCP server).
2. Register the plugin in `.claude-plugin/marketplace.json` under `plugins`.
3. Add each skill to `sources.json`, then run `make sync` and `make validate`.

## License

[MIT](LICENSE.txt) © ITS — vendored skills remain under their respective upstream licenses.
