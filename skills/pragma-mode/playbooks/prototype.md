### Prototype

**You own the decision, not the code.** The prototype is a throwaway instrument
that settles one question cheaply. The real build follows [Feature](feature.md).
Speed beats polish here; the rigor is in choosing well.

1. Name the decision the prototype exists to make: which state model, which
   layout, which interaction, or, for an empirical fork, which behavior or
   timing. With no decision to make, there is no prototype; route to Feature.
2. When the design space is open, gather prior art and propose variations the
   user didn't ask for, per [exhaust-the-design-space](../principles/exhaust-the-design-space.md).
   Skip this when the direction is set.
3. Build it with [prototype](../../prototype/SKILL.md), on the branch its
   question calls for. When comparing alternatives, put every variant behind
   one switch, each one labeled.
4. Observe the thing you are deciding: drive each variant, log the timing, or
   print the output. Here the observation is the test.
5. Present the alternatives, the evidence, the tradeoffs, and your
   recommendation. Hand the chosen direction back to Feature, or to the
   playbook that asked the question.

**Reply:** the variants explored, the evidence for each, the tradeoffs, your
recommendation, and the prototype's path and run command. Say plainly that it
is throwaway.
