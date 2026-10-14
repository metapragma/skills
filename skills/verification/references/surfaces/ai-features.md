# AI Features

Code that calls a model produces nondeterministic output. Assertions that
expect an exact output fail on valid variation, and loose assertions pass on
bad output. Use evals.

## Practice

1. **Error analysis first.** Read real traces, or realistic synthetic ones.
   Name the failure modes you actually observe before you write any metric.
2. **Deterministic checks.** Use them wherever they apply: schema validity,
   tool-call arguments, refusal on disallowed input, required fields, length,
   and banned content.
3. **Judges for the rest.** An LLM judge grades one named failure mode with a
   pass or fail result. Before you trust it, validate it against examples a
   human has labeled. Report how often it agrees with the human labels.
4. **Datasets.** Keep a versioned eval set that includes the cases that failed
   before. Pin the model and the prompt versions in the evidence record.

## Verdict

An eval run reports pass rates per failure mode against agreed thresholds,
and it compares them with the previous baseline. A drop in any guarded failure
mode fails the check. Lowering a threshold is an integrity item.
