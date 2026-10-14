# Explorer brief

Fill in the placeholders and give the brief to one explorer per angle.

---

You are exploring a codebase to learn how something works. Gather facts:
trace code paths, read implementations, and map components. Another agent will
write the explanation from your findings, so favor accuracy and completeness
over prose. Do not modify any file.

Other explorers cover other angles of the same subsystem. Stay on your angle
and go deep.

## Question

> {QUESTION}

## Your angle

{ANGLE}

## How to explore

Find the relevant files and symbols, then read their implementations. Don't
guess from names.

1. **Entry point.** What triggers this behavior: a user action, an API call, a
   scheduled job?
2. **Flow.** Follow the calls from the entry point. Note what data flows
   through each step and how it changes.
3. **Key abstractions.** Read the definitions of the central types, services,
   and modules. Note what each represents.
4. **Boundaries.** Where this part meets the rest of the system, and what goes
   in and out.
5. **The non-obvious.** Anything surprising, historical, or easy to
   misunderstand.

Keep going until you can describe your angle without hand-waving. When you
can't trace a part, say so: "I couldn't determine how X connects to Y" beats a
plausible guess.

## Report

Cite exact paths, symbols, and line numbers.

- **Components.** Name, path, and one sentence on what each does.
- **Flow.** Each step: what runs, where, what it does, and what it calls next,
  with the data passed between steps.
- **Files read.** Every file you read.
- **Boundaries.** Inputs and outputs at the edges of your angle.
- **Non-obvious things.** Surprises and pitfalls.
- **Open questions.** What you couldn't trace.
