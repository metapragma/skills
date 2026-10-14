# Explanation format

## Walkthrough

Use these sections, and drop any that have nothing to say.

- **Overview.** One or two paragraphs: what this is, what it does, and why it
  exists. A reader should be able to stop here and decide whether to go on.
- **Key concepts.** The types, services, or abstractions needed to follow the
  rest, each briefly defined.
- **How it works.** The longest section. What triggers it, what happens step
  by step, where data goes, and where the decision points are. Use prose,
  naming files and functions so the reader knows where to look. Add a diagram
  when several components interact or data passes through stages: Mermaid for
  structured flows, plain text for simple relationships.
- **Where things live.** A short map of the files someone needs to start
  working here.
- **Gotchas.** Surprising behavior, historical context, and pitfalls.

## Map

A layered list or diagram of the relevant modules, each with one line on its
responsibility, followed by the callers that reach into the area and what they
use it for. Name things with the project's domain vocabulary.

## Style

- Be concrete: "`UserService` calls `AuthClient.refresh()`", not "the service
  delegates to the client".
- When something is complex, explain why it is complex. When it is simple,
  keep the explanation short.
- Use an analogy only when one genuinely fits.
- State open questions plainly instead of smoothing over them.
