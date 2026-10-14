### Skill change

**You own the skill's behavior, not just its wording.** Use this to write or
edit a skill, an agent instruction file, or a playbook.

1. Write the change with [writing-for-agents](../../writing-for-agents/SKILL.md);
   for a skill, also its `SKILL-MECHANICS.md`. Keep only prose that changes a
   decision, point at structural sources instead of restating them, and call
   other skills by path.
2. Validate it. The frontmatter has a `name` that matches its folder and a
   `description`, every referenced file exists, and every link resolves. Run
   the repository's own checks, such as `scripts/check-skills` in the skills
   repository. When the skill came from elsewhere, record it as forked in the
   provenance file and update its notices.
3. Decide whether the change needs an eval. A behavioral change to a skill
   that runs often, or a claim that a change helps, needs one. A wording or
   link fix doesn't; record `skip: <reason>`.
4. Run a blinded eval:
   - **Frame.** Name the variant under test and the behavior that counts as
     success. Write a rubric of three to six concrete criteria for the judge
     only.
   - **Set up.** One working directory per candidate, with the variant in
     place and the context an ordinary task would have. Use project-shaped
     names; nothing the candidate sees mentions an eval, a test, a rubric, a
     judge, or other candidates.
   - **Prompt.** One request written the way a user would type it, with the
     goal and nothing about what is measured. Don't ask candidates to list the
     skills or principles they applied.
   - **Run.** The same prompt for the variant and for a baseline without it,
     repeated when the result could be noise. When the harness offers
     subagents, run each candidate in a fresh context.
   - **Judge.** One judge scores every output on one scale, seeing outputs only
     by neutral labels. Say whether the judge shares the candidates' model
     family.
   - **Check the work, not the claims.** Read what each candidate actually did:
     the files it opened and the commands it ran, from the session record when
     the harness keeps one. Grade instruction-following from that record and
     from the output, never from the candidate's own account.
   - **Read every output yourself** and compare with the judge. Disagreement
     means a biased judge or an ambiguous rubric; resolve it before
     concluding. Vet any pass rate per [explain-the-number](../principles/explain-the-number.md).
5. After the change has been in use for a while, audit real sessions with
   [skill-doctor](../../skill-doctor/SKILL.md) when the user asks for one.
6. With the user's go-ahead, run [Committing](committing.md).

**Reply:** what the skill now does differently, the key design decisions, the
validation results, and the eval's rubric, results, and verdict on whether to
keep the change.
