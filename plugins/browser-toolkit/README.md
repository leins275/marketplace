# browser-toolkit

Browser automation for Claude. Bundles the [Playwright MCP server](https://github.com/microsoft/playwright-mcp) so Claude can drive a real browser — navigate pages, click, fill forms, capture screenshots and read the accessibility tree.

Unlike the other toolkits, this one ships **no skills** — it adds an **MCP server**. Once installed, the `playwright` tools are available to Claude automatically.

## Requirements

- **Node.js** — the server runs via `npx @playwright/mcp@latest`, downloaded on first use. Playwright fetches its browser binaries automatically the first time a browser tool runs.

## Install

```text
/plugin install browser-toolkit@its-marketplace
```

Confirm the server is connected with `/mcp`. It pairs naturally with [`testing-toolkit`](../testing-toolkit) for end-to-end and live web-app testing.
