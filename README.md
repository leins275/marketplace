# ITS Marketplace

A private [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin marketplace for the ITS team. It packages the skills our engineers rely on globally into installable toolkits, so every teammate gets the same standards with a single command.

## Quick start

Add the marketplace, then install the toolkits you need:

```text
/plugin marketplace add leins275/its-marketplace
/plugin install django-toolkit@its-marketplace
```

> Replace `leins275/its-marketplace` with the repository's location once it is pushed to the company Git host. You can also add it straight from a local clone:
> `/plugin marketplace add /home/leins275/Projects/its/marketplace`

## What's inside

Five toolkits bundling **13 skills**, every skill that is currently available globally in `~/.claude` and `~/.agents`:

| Toolkit | Skills | Use it for |
| --- | --- | --- |
| [`django-toolkit`](plugins/django-toolkit) | django-patterns, django-security, django-verification | Building, hardening and verifying Django services |
| [`testing-toolkit`](plugins/testing-toolkit) | python-testing-patterns, e2e-testing-patterns, webapp-testing | Pytest, end-to-end and live web-app testing |
| [`frontend-toolkit`](plugins/frontend-toolkit) | frontend-design, ui-ux-pro-max | Designing and building polished UIs |
| [`devops-toolkit`](plugins/devops-toolkit) | docker-patterns, postgres-patterns, devops-rollout-plan | Containers, databases and safe rollouts |
| [`content-toolkit`](plugins/content-toolkit) | copywriting, find-skills | Marketing copy and discovering new skills |

## Layout

```text
its-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # the registry — lists every plugin
├── plugins/
│   └── <toolkit>/
│       ├── .claude-plugin/
│       │   └── plugin.json     # plugin manifest
│       ├── skills/             # bundled SKILL.md skills (+ references, scripts, examples)
│       └── README.md
├── Makefile                    # validate / list / tree helpers
├── LICENSE.txt
└── .github/workflows/          # CI validation on push and pull request
```

## Working with the marketplace

```text
make help        # list available targets
make validate    # check that every marketplace.json / plugin.json parses
make list        # list plugins and the skills they bundle
make tree        # print the full repository layout
```

## Adding a plugin

1. Create `plugins/<name>/` with a `.claude-plugin/plugin.json` and a `skills/` directory.
2. Drop each skill into `skills/<skill-name>/SKILL.md` (plus any `references/`, `scripts/` or `examples/`).
3. Register the plugin in `.claude-plugin/marketplace.json` under `plugins`.
4. Run `make validate` and open a pull request.

## License

[MIT](LICENSE.txt) © ITS
