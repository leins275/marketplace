.DEFAULT_GOAL := help
SHELL := /bin/bash

PLUGINS := $(notdir $(wildcard plugins/*))

# Use uv when available (preferred), else fall back to python3 (e.g. in CI).
PYTHON := $(shell command -v uv >/dev/null 2>&1 && echo 'uv run' || echo 'python3')

.PHONY: help validate sync diff list tree

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

validate: ## Validate marketplace.json, sources.json and every plugin.json
	@python3 -c "import json; json.load(open('.claude-plugin/marketplace.json')); print('OK  .claude-plugin/marketplace.json')"
	@python3 -c "import json; json.load(open('sources.json')); print('OK  sources.json')"
	@for p in $(PLUGINS); do \
		python3 -c "import json; json.load(open('plugins/$$p/.claude-plugin/plugin.json')); print('OK  plugins/$$p/.claude-plugin/plugin.json')" || exit 1; \
	done
	@echo "All manifests are valid JSON."

sync: ## Re-vendor every skill from its upstream repo (see sources.json)
	@$(PYTHON) scripts/sync.py

diff: ## Show what `make sync` changed in the vendored skills
	@git diff --stat -- plugins/ || true

list: ## List plugins and the skills they bundle
	@for p in $(PLUGINS); do \
		echo "$$p"; \
		for s in plugins/$$p/skills/*/; do echo "    - $$(basename $$s)"; done; \
	done

tree: ## Print the repository layout
	@find . -path ./.git -prune -o -print | sort
