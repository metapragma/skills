# Sketch First

Settle a module's shape before filling in its implementation. Use this when new
code spans more than one function and its shape isn't already set by the
surrounding code. Uses the vocabulary in [SKILL.md](SKILL.md).

## 1. Ground

Build a traced model of every module the new code touches: its callers, its
data, and the interfaces it must fit. Naming a file is not grounding. When the
design changes ownership or layering, recover why the current shape exists
before overriding it.

## 2. Write the usage first

Write what the caller sees before any types: the quickstart or doc comment a
consumer reads, plus two or three realistic call sites. What they import, what
they call, and what comes back. The interface is derived from this usage. When
the two disagree, change the interface, not the usage.

## 3. Sketch the interface

Write the types, signatures, and module seams with bodies that fail
loudly when called (`not implemented`) and pseudocode where logic matters.
Small changes fit in one file. Larger work gets a module map plus type
definitions. For a shape with no precedent, design it twice per
[DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) and compare on depth.

Screen every candidate against [DESIGN-RED-FLAGS.md](DESIGN-RED-FLAGS.md).
Assume the next contributor is an agent that sees only the files it opened,
copies the nearest example, and takes the shortest path that compiles. Prefer
the design where a change that looks right from one file is right for the
whole codebase.

Ship a short rationale with the sketch: the problem and its constraints, the
usage, the shape and the decisions it encodes, the tradeoffs accepted, at
least one rejected alternative and why it lost, and open questions phrased as
questions.

## 4. Implement against the sketch

The sketch is the contract. A deviation is a signal to surface, not friction to
absorb: when a function needs a parameter the sketch didn't anticipate, ask
whether the sketch was wrong, a requirement was missed, or the implementation
is overreaching.

## 5. Scrap when the shape is wrong

When implementation keeps producing friction the sketch can't absorb, throw
the sketch out instead of patching around it. The signal is a pattern, not one
instance:

- The same shape of workaround appears across unrelated code.
- Several unrelated edge cases each need a special-case branch.
- Types need escape hatches (casts, `any`, optional fields that are always
  set) to compile.
- A lock seems necessary where the sketch said the state wasn't shared.
- Callers have to know the module's internal rules to use it.
- Two or more independent deviations from the sketch share one shape.

A few edge cases don't condemn a design; complexity in the data is not
complexity in the design. When you scrap, retrace what was built, redesign as
if the new constraints had been there from the start, make the new sketch
smaller than the old one before it grows, and return to step 3.
