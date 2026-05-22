# ITS Marketplace

A private [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace for the ITS team. It packages the skills our engineers rely on into five installable toolkits, so every teammate gets the same standards with a single command.

The skill files are **vendored** — copied into this repo from their upstream repositories — and refreshed on demand with `make sync`. [`sources.json`](sources.json) records exactly where every skill comes from, so updates are traceable and reviewed before they reach the whole team.

## Quick start

```text
/plugin marketplace add ssh://git@gitlab.its.xyz:2224/ai/marketplace.git
/plugin install django-toolkit@its-marketplace
```

> The marketplace lives at [`ai/marketplace`](https://gitlab.its.xyz/ai/marketplace) on the company GitLab. You can also add it from a local clone:
> `/plugin marketplace add /path/to/marketplace`

## What's inside

Five toolkits bundling **13 skills**:

| Toolkit | Skills | Use it for |
| --- | --- | --- |
| [`django-toolkit`](plugins/django-toolkit) | django-patterns, django-security, django-verification | Building, hardening and verifying Django services |
| [`testing-toolkit`](plugins/testing-toolkit) | python-testing-patterns, e2e-testing-patterns, webapp-testing | Pytest, end-to-end and live web-app testing |
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

### Automated sync (GitLab CI)

The `sync-skills` CI job does this for you on a schedule: it runs `make sync` and, if anything changed, opens a **merge request** with the diff. New skill versions reach the team only when someone reviews and merges that MR — the automation handles the clone-copy-diff grunt work, not the rollout decision.

One-time setup in the GitLab project:

1. **Settings → Access Tokens** — create a Project Access Token, role _Developer_, scope _write_repository_.
2. **Settings → CI/CD → Variables** — add it as a masked variable named `SYNC_TOKEN`.
3. **Settings → CI/CD → Pipeline schedules** — add a schedule (e.g. weekly); each run triggers `sync-skills`.

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
│       └── README.md
├── sources.json                # upstream repo + path for every vendored skill
├── scripts/sync.py             # re-vendors skills from sources.json
├── Makefile
└── .gitlab-ci.yml              # CI: validate manifests + scheduled upstream sync
```

## Adding a skill

1. Register its upstream in [`sources.json`](sources.json) (or `"source": "local"` if there is none).
2. Run `uv run scripts/sync.py <name>` to vendor it (local skills are added by hand under `plugins/<toolkit>/skills/<name>/`).
3. Run `make validate`.

## Adding a plugin

1. Create `plugins/<name>/` with a `.claude-plugin/plugin.json` and a `skills/` directory.
2. Register the plugin in `.claude-plugin/marketplace.json` under `plugins`.
3. Add each skill to `sources.json`, then run `make sync` and `make validate`.

## License

[MIT](LICENSE.txt) © ITS — vendored skills remain under their respective upstream licenses.
