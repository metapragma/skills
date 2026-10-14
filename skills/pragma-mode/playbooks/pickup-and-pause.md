### Pickup and pause

**You own the boundary.** Pause leaves a checkpoint a fresh agent can resume
from. Pickup resumes from one without redoing it. Pick the branch the request
names.

#### Pause

Run this only when the user asks to pause, or before an interruption you can
see coming. "Keep going" or "don't stop" is not a pause.

1. Stop at a safe point: finish the current atomic step or back it out. Start
   nothing new, and stop any delegates you started.
2. Take no irreversible action to pause. Leave the changes in the working
   tree; commit a `wip:` checkpoint only with the user's go-ahead.
3. Write the checkpoint with [handoff](../../handoff/SKILL.md). Point at an
   existing [decision log](../references/decision-log.md) instead of repeating
   it.

#### Pickup

1. Find the prior trail: the handoff file, the branch, the decision log, or a
   session record the user points at. Read its decisions and last state
   first.
2. Rebuild the operating state from the trail and the live checkout: the
   branch, what already landed (`git log` and `git diff` against the base),
   the pending work, and the decisions made. Treat the trail as authoritative
   input; don't re-derive it.
3. Compare done with pending and name the resume point. Don't rerun work the
   trail shows complete.
4. Check the inherited claims that the next step depends on, on the real
   artifact, per [prove-it-works](../principles/prove-it-works.md). A passing
   report from the previous session is not proof.
5. Route the remaining work to its playbook in [pragma-mode](../SKILL.md#routes)
   and continue there.

**Reply:** for a pause, where you stopped, what is on disk versus only in the
handoff, whether the tree is clean, and the first action on resume. For a
pickup, where the previous session stopped, what you inherited versus redid
(ideally nothing), the resume point, and the playbook you routed to.
