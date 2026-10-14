---
name: blast-radius
description: Find what a change could break beyond its diff, and prove the fact it is safe because of by running real code.
disable-model-invocation: true
license: MIT
metadata:
  source: "https://github.com/cursor/plugins/tree/d73344bee8cf22e53b9d5f4cf5749d38ba38c174/pstack/skills/blast-radius"
---

# Blast radius

Find what a change breaks somewhere else, before it ships. Listing the callers
is not the job; a search finds those in seconds. The job is the breakage a
search won't show you. This is read-only analysis plus throwaway proof scripts;
it changes no project code.

## How sure are you

A writeup that sounds right reads as convincing whether or not it is true. So
find the one or two facts the change's safety depends on, and push each as far
down this list as is cheap. Say where it stopped.

1. You said so. Worthless on its own.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You showed the bad case can't happen, by walking the failure step by step.
4. You ran it: a script or test that calls the real code and fails loudly if
   you are wrong.
5. You reproduced it in the running system.

Level 4 is usually one small script that imports the same library version the
project ships and calls the exact function in question.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes, and deletes,
   and what it now does differently, including what the diff doesn't spell
   out. Read the commits and pull request discussion behind it.
2. **Find the fact it is safe because of.** Most risky-looking changes are safe
   because of one fact, such as "this call only drops cache entries that are
   already dead". When that fact holds, most risky cases clear at once. Spend
   your time here, not on a long list of maybes.
3. **Look where search stops.** Read the source of the libraries you call, at
   their pinned version and with any local patches. Work out when things run:
   transaction boundaries, retries, background jobs, startup and shutdown
   order. Follow what a symbol search misses: a JSON response shape, a database
   column, a wire format, another service or language reading the same bytes,
   a feature flag, code three hops downstream.
4. **Be honest about each risk.** Give each a real likelihood and a real cost.
   Keep the risks you confirmed, and list separately the ones you checked and
   cleared. A search that finds nothing is still an answer. Never invent a
   caller or an API.
5. **Prove the fact.** Write a script or test that runs the real code, run it,
   and paste what happened.
6. **For a wide change, get a second opinion.** When the harness offers
   subagents, give the same question to an independent agent in a fresh
   context and merge the answers. Different reviewers catch different real
   bugs. Say whether the second agent was the same model family.

## Reply

- **What it does.** What changed, including the part that isn't obvious.
- **The fact it is safe because of.** State it, the level you reached, and the
  proof. If you couldn't prove it, write "unproven".
- **Risks.** Each names how it breaks, the `file:line`, how likely and how bad,
  and how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or repro that would catch the real
  bug, including the script you wrote.
