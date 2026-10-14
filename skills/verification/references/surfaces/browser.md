# Browser

Browser verification has two modes. Agent-driven browsing explores a flow and
answers judgment questions. Scripted Playwright tests give repeatable verdicts.

## Explore

- Use computer use or a browser-driving tool in Claude or Codex for a new or
  changed flow. Use it also for judgment questions such as "does this layout
  read correctly?"
- Drive against the local instance. Confirm that the client's API proxy points
  at that instance and not at a shared environment.
- Sign in with a local test identity. See [identity.md](identity.md). Never use
  someone's real account.
- Check the rendered content at the relevant viewport sizes. Read the console
  and the network log for errors.

An agent's walkthrough is evidence that the flow worked once. It doesn't give
a verdict that can be repeated.

## Freeze

Before merge, turn each walkthrough worth keeping into a Playwright test:

- Use stable handles: roles, labels, and test IDs. Avoid coordinates and DOM
  order.
- Save the signed-in session with the storage-state feature, so tests skip the
  login form.
- Assert the user-visible result and the backend effect it implies.
- Place the test in the project's existing suite, and run it through the
  `browser` command.

For agent-driven runs, prefer `playwright-cli` with on-disk snapshots over a
browser MCP server, because it uses less of the agent's context. Keep MCP for
long exploratory sessions.

## Artifacts

Capture screenshots, video, and traces when the user asks for them. Playwright
traces are also useful when a frozen test fails. Note that a browser-native
`alert` dialog may be invisible to some drivers.

## Optional Checks

Visual regression with reviewed baselines, and accessibility scans. Treat an
updated baseline as an integrity item.
