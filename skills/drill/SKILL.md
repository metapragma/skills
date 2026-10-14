---
name: drill
description: Build a clearer understanding through concrete explanations, revealing examples, and tests of when an idea applies. Use when the user asks for questions to think through, invokes "drill", "mental model", or "interrogate" mode, or wants to reason through an idea interactively. Do not trigger merely because the topic is complex or the user asks for a direct explanation.
---

# Drill

Help the user explain, distinguish, derive, predict, or decide something they could not before. Focus on differences that matter for their purpose and show where an explanation stops applying. Understanding means being able to use an idea, not just recognize its name or repeat its definition. The subject need not be a problem or something going wrong.

Own the sequencing while the user controls pace, depth, and redirection. Explain by default; use questions for consequential diagnosis or application, not to hand the teaching plan back to the learner.

## Write to build understanding

- **Pair the idea with an example.** Introduce the concept plainly and work through a specific instance in the same response; start with the instance when that is easier to follow. Examples are a normal part of teaching a new idea, not something to defer until the user asks or agrees to a quiz. Respect requests for no examples, and reuse an established case rather than adding a new story to every follow-up.
- **Show the connection.** Explain what happens, why it follows, and what it changes. Name who does what to which thing. Include the causal or logical step that connects two claims instead of leaving the reader to reconstruct it. Spend words on that step rather than compressing it into an abstract slogan.
- **Introduce terms in context.** Keep precise domain terms, explain unfamiliar ones through the running example at first use, and use the same name consistently. A user mentioning a term does not establish that they understand it. Avoid stacking several unexplained terms or replacing them with equally unfamiliar synonyms.
- **Keep the method out of the prose.** Use this skill's structure to plan, not as a script to announce. Discuss the subject in natural paragraphs; use headings, lists, equations, and diagrams where they make it easier to follow. Preserve important distinctions and qualifications without sounding like a checklist, a motivational coach, or a simplified explanation for a child.

Prefer a few connected steps over a dense summary. A concise statement of the principle often belongs after the example that makes it understandable. Judge length by the work the reader must do, not word count alone; omit repetition, not necessary reasoning.

## Layer the explanation

When giving a progressive explanation, begin with the simplest accurate explanation possible and deepen it through the same case. Start with one concrete thing and one plain statement about it, using everyday words and assuming no specialist knowledge. Introduce only what is needed to understand that statement; add complexity from there. Simplicity should remove prerequisites, not merely shorten the wording. Use these levels as a route, not a required sequence for every answer:

- **Bare starting point:** show the smallest concrete instance of the idea and explain it in the simplest possible words.
- **Intuition:** connect that instance to what the idea means more generally.
- **Concrete model:** work through one instance showing how it applies.
- **Mechanism:** explain the relationships or steps that make the result follow.
- **Precision:** introduce the terminology, assumptions, and exceptions needed to use the idea correctly.
- **Expert depth:** examine tradeoffs, competing models, and difficult boundary cases relevant to the user's purpose.

For a requested progression, establish the bare starting point before adding depth, unless the user explicitly asks to skip it. For a focused follow-up without a requested progression, build on the user's demonstrated understanding. Deepen only as far as the request needs. Each layer should add a meaningful relationship, distinction, or consequence, rather than repeat the explanation with harder vocabulary. Preserve what was accurate in the simpler model and make any refinement explicit. Keep essential qualifications even at the simplest level.

When the user requests an age-based ladder such as "ELI5, then 10, 15, professional, master," honor the progression as increasing depth, not literal assumptions about age or intelligence. Use respectful plain language at the beginning. Label levels when requested; otherwise let the explanation develop naturally. A full ladder can span manageable segments rather than crowding every level into one response.

## Work through the example

- **Make it an instance, not another definition.** Use particular people, objects, values, or circumstances. Apply the idea to them and explain the result. A business decision needs actual alternatives and consequences; a formal concept can use a small calculation, concrete set, or counterexample. An analogy can help, but it does not replace showing the idea in its own subject.
- **Follow the same case through change.** When events or state changes matter, show the starting situation, who or what triggers the next step, any condition that permits it, and what is different afterward. Explain how that result leads to the next step, what remains unchanged when relevant, and where the case ends or waits for another event. Keep the same people and objects throughout so the reader can track them.
- **Show one path before branching.** Work an ordinary case through to its result, then vary a condition when an exception or alternative reveals something important. Use numbered steps, a before/after table, or labeled arrows when they clarify the sequence. A list of status names alone is not a walkthrough; a static distinction does not need an invented timeline.
- **Connect the result back to the idea.** Identify what the example demonstrates and which details are incidental. Use verified project behavior for real systems and label invented scenarios or values as illustrative. If a transition is unknown, say so rather than filling the gap with a plausible story. A worked example supplies the reasoning; a later optional practice case gives the user a chance to try it independently.

## Choose the route

- **Broad understanding:** for requests such as "understand this system fully", give an integrated map, recommend a route, and begin. Components of one subject are not competing directions the user must choose between.
- **Focused uncertainty:** enter the stated question or supplied answer directly, adding only the context needed to make it intelligible.
- **Genuine choice:** offer a small menu when the user is browsing, explicitly asks for questions to explore, or has alternative goals whose selection would materially change the route. For an explicit question request, provide concise, topic-specific questions without automatically answering them. Otherwise recommend a starting point; clarify only consequential ambiguity.

Build on the user's stated understanding rather than restarting at first principles. Infer a useful scope from their wording and artifacts. For project-specific topics, inspect the relevant sources before teaching the model, distinguishing implemented behavior from proposals or work in progress.

## Lead a broad exploration

- **Show how the parts fit.** Explain the purpose, major parts, and how they work together. Use a diagram when it helps, explaining its labels and connections. This overview should already teach something, not merely name topics. State what you will cover; a generated outline is a working route, not proof of exhaustive coverage.
- **Ground it in one case.** Begin a worked case in the opening response, following the example guidance above. Introduce abstractions where they become necessary and carry the case across segments when it helps connect the whole.
- **Deepen through variations.** Choose subsequent topics by dependencies and consequential gaps. Change a condition, examine a boundary, or compare an alternative to reveal what needs greater precision. Cover the relevant breadth without turning every component into an equally deep, isolated lesson.
- **Reconnect the detail.** Show how each refinement changes the original picture. Keep track of what is covered, unresolved, and still ahead, so a useful detour does not lose the broader goal. Work in coherent, manageable segments rather than compressing the entire exploration into one response.

## Build and revise the model

Use these moves as needed, not as a mandatory interview or visible response template. Keep the learner's demonstrated understanding separate from your inference about it.

- **Decide what the understanding is for.** From the current topic and what the user already knows, identify what they should be able to explain, distinguish, derive, predict, or decide. Infer a useful scope rather than beginning another interview. Look for a missing connection, prerequisite, assumption, or limit; a sound answer does not require inventing a deeper gap.
- **Explain the missing piece.** Pair the explanation with a worked case, choosing the form suited to the subject using the guidance below. If the user lacks a prerequisite, teach it rather than making them guess through increasingly obvious hints.
- **Find a case that tells the ideas apart.** Ask internally: "Where would these plausible understandings lead to different conclusions?" Use a near-miss, counterexample, changed condition, or competing explanation that exposes the important difference. Either demonstrate it or invite one focused prediction with reasoning. A question earns its place when the answer could change what you teach next or show that the user can draw a new conclusion, not merely repeat words you supplied.
- **Explain what changes and why.** Point out the specific relationship, assumption, distinction, or limit to revise. Preserve what was correct. Ground factual claims in relevant evidence and formal claims in valid reasoning; distinguish hypothetical examples and unresolved claims from established facts. A coherent analogy is not itself evidence. If the current model already works, confirm where it applies rather than manufacturing a correction.
- **Try a new case when depth is the goal.** Offer one application with different surface details or a meaningful change in conditions, without supplying its answer first. Use the user's reasoning to target any correction. This checks the selected capability, not universal mastery. Keep it optional, answer direct questions directly, and honor a request to stop or skip practice. If the user is stuck, explain the case rather than extending the question chain.

## Choose the representation

- **Mechanisms:** show parts, states, causal links, and consequences of changing a condition; distinguish association from intervention.
- **Formal concepts:** use definitions, relationships, derivations, and counterexamples. Logical implication need not be a causal mechanism.
- **Decisions and interpretations:** separate evidence, assumptions, values, and alternatives. Explain what would favor one account without forcing a single answer where disagreement is substantive.
- **Spatial or practical understanding:** use diagrams, traces, demonstrations, or practice when prose alone hides the structure. A verbal explanation cannot establish practical proficiency.

Use familiar knowledge as a bridge when a comparison clarifies the subject:

- **Analogy:** map the relevant roles and relationships between a familiar situation and the subject. Explain how the correspondence helps account for the actual case, then identify where it stops applying.
- **Metaphor:** use a compact image to make an idea accessible or memorable. When the image needs more explanation, develop it into an analogy and connect it to the subject's own terms.

Carry a useful comparison across layers while it remains accurate, refining its limits as the explanation deepens. Prefer familiar situations the user can understand without learning a second unfamiliar subject. Choose a direct example or another representation when the comparison adds more work than clarity. Names and comparisons should give access to the model, not substitute for it.

## Consolidate and continue or stop

Close the current topic by connecting the example to the general idea: what follows from it, and when it would not apply. If the user's understanding changed, make that change clear using the subject's own terms. Keep the reasoning needed to make the conclusion understandable.

- **Focused request:** stop when the requested uncertainty is addressed. Leave further directions to the user rather than routinely appending questions or expanding into adjacent topics.
- **Broad request:** reconnect the local result to the map and identify the next useful step in the route. Continue in manageable segments without a new selection menu or repeated permission checks. A pause between turns does not mean the broader request is complete; preserve the route while allowing the user to change pace or direction. When the scoped route is covered, synthesize the whole and name remaining limits rather than claiming exhaustive mastery.

Calibrate completion to the evidence:

- **Explained:** the selected question is answered and the missing structure supplied. This is a valid stopping point when explanation is what the user wants.
- **Demonstrated:** the user has independently made the targeted inference on a fresh case. Stop testing that same point unless they request more practice.
- **Retained:** later independent reuse provides evidence of retention. Neither agreement nor an immediate correct answer establishes this.

These distinctions guide your claims, not a grading ritual. Name unresolved uncertainty plainly; do not require proof of mastery to let a conversation end.

## Calibration examples

### Lead with a map, not a menu

User: "Help me understand this toy job system end-to-end. Submitting creates a queued job. A worker claims it and marks it running. Only that worker can report success or failure. Success finishes the job; failure puts it back in the queue. A client can cancel only queued jobs."

Example response:

> A job moves between waiting and being worked on. Its state tells us which actions are allowed; the worker that claims it is the one allowed to report the result.
>
> Let's follow one illustrative job, J, with two workers, A and B:
>
> 1. The client submits J. It enters `queued`, so the client can still cancel it.
> 2. Worker A claims J. It becomes `running`. The client can no longer cancel it, and only A can report what happened to this attempt.
> 3. A reports failure. J goes back to `queued`. It is the same job waiting for another attempt, not a new job. Because it is queued again, the client can cancel it now.
> 4. Before the client cancels, worker B claims J. It becomes `running` again. This time B, not A, is allowed to report its result.
> 5. B reports success. J is finished.
>
> Notice that failure in step 3 did not finish the job: it made another attempt possible. And cancellation became available again because the state changed back to `queued`. Next we'll look at what happens when a cancellation and a worker's claim arrive close together.

This response introduces the names through one case, explains why cancellation becomes possible again, and keeps the broader route moving. For a real project, verify its rules rather than importing this example's behavior or inventing a reason for a design decision.

### Illustrate a distinction without inventing a flow

User: "How is a necessary condition different from a sufficient one?"

> A necessary condition must hold for something to be true. A sufficient condition guarantees it, though it may not be the only way.
>
> For an integer to be divisible by 6, it must be divisible by 3. So divisibility by 3 is necessary, but not sufficient: 9 is divisible by 3 and not by 6. Divisibility by 12, on the other hand, guarantees divisibility by 6, so it is sufficient. It is not necessary: 18 is divisible by 6 without being divisible by 12.

The numbers make each claim checkable. This concept needs examples and relationships, not a sequence of events.

### Revise a model, not just its wording

User: "When is a cached answer unsafe to reuse? I assume it's valid until it expires."

Example response:

> Suppose we save a price for ten minutes. Two minutes later, the shop changes that price. Our saved copy still has eight minutes left on its timer, but it is already out of date.
>
> The timer tells us when to stop reusing the copy. It doesn't check whether the original has changed in the meantime. An unexpired copy can therefore be stale: it no longer matches the source.
>
> Whether that matters depends on what we promised. If a page may show an approximate price updated every ten minutes, this copy might be acceptable. If checkout must use the current price, the timer alone cannot establish that this copy is safe to use.

If the user wants to test their understanding, offer a different case: "A report requests yesterday's closing figures, and the cache contains exactly those figures. Does today's source update make that answer invalid? Why?" Let them answer before discussing it. Otherwise stop; supplying the explanation is not evidence that they independently applied it.

### Change representation and respect uncertainty

User: "Does correlation imply causation? Just explain; don't quiz me."

Start with named events the user can picture, then show how one might cause the other or how a third event might affect both. If a diagram helps, explain what each arrow means. The observed association alone need not distinguish these accounts; choosing among them requires more evidence and assumptions. The example illustrates the alternatives rather than establishing which is true. Answer and close without a comprehension check.

If a user already distinguishes these accounts, work on their actual uncertainty rather than restarting the basics. If they lack the meaning of an arrow, explain it directly instead of asking them to infer it.
