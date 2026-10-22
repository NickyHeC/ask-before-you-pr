> Published as written at 00:36 PT on 2026-10-22, before study 3 started at 00:37 PT. "Run N" is study N in this folder. Two changes: a private local script's path and name are replaced by "[a local script]" and "as in run 2". The paths it names are the study's working folders, not this repository. The rubric it hashes is the working copy, whose scored text is [scorer-instructions.txt](../scorer-instructions.txt). The instructions hash it cites is of that file before internal names were removed for publishing.

# Run 3 pre-registration (written 2026-10-22 00:36 PT, before any run-3 data is drawn)

Nothing below changes after the first fetch. A deviation is reported as a deviation, with its reason.

## Hypothesis
Splitting the questions into required and suggested, a PR flagged as failing a **required** question is
more likely to be one maintainers rejected than one they merged, in projects that use no bots or policies.

## The instrument (fixed)
- Scoring instructions: `run3/instructions.txt`, byte-identical to run 2's
  (sha256 `0d8b7f6eb211f883d52f54ef50d770c4b445f17e2eafcdb8f4cc039e94fd68ab`); rubric `../rubric.md`
  (sha256 `f9774e75e2570c13e4fc1045af0e3edc74f0d7eac4b561bf512b22b150b4cc52`). Every PR is scored on all 13 questions.
- **Suggested (soft), ignored by the verdict:** Q1 wanted (issue first), Q8 evidence it was run, Q9 CI green.
- **Required:** Q2, Q3, Q4, Q5, Q6, Q7, Q10, Q11, Q12, Q13.
- **Verdict:** a PR is *flagged* when it scores F on at least one required question.

## Repos
- Three repos not used in runs 1 or 2 (not godot, qgis, ollama, excalidraw, helix), each with no stale or
  auto-close workflow, no stale.yml, no AI, LLM or new-contributor policy in CONTRIBUTING, its linked pages,
  the PR template, AGENTS.md or pinned issues, and no bot among the closers of unmerged PRs (dependabot closing
  its own PRs excepted). Evidence copied into `run3/repo_checks/`.
- Each must have at least 40 external rejected and 40 external merged PRs in the window, so both groups are
  full size (run 2's merged groups were small).
- Window 2026-04-22 to 2026-10-21 PT.

## Groups and sample (definitions as run 2's `method_notes.md`, except as stated)
- **Rejected:** closed unmerged by a non-author, non-bot; external author; non-draft; base main or master;
  supersession by a merged PR of the same author checked.
- **Merged:** external author, no bot authors, no bump or dependency titles; base main or master.
- **No stale group.** Staleness was not a quality signal in run 2.
- 50 per group per repo (the whole pool when smaller, reported). Core-team filter as run 2.
- Seeds: draw `random.Random(20261022)` over each pool sorted by number; blinding `random.Random(5353)`;
  spot-check `random.Random(888)`.

## Scoring
- Second model through [a local script], 10 PRs per fresh conversation, as in run 2.
- Claude: fresh Claude subagents given only `instructions.txt` and the blinded material, two per repo.
- Material from run 2's fetcher (`data/fetch2.py`), state, labels and close comments not shown.

## Analysis (fixed)
- **Primary:** pooled over the three repos, PRs where both models agree on the required-set verdict;
  flagged share of rejected minus flagged share of merged; Fisher's exact test, two-sided; Newcombe 95% CI.
- **Success bar:** p < 0.05 **and** a gap of at least 20 percentage points. Anything else is reported as
  not significant.
- **Secondary, reported whatever they show:** each repo alone; Claude alone; the second model alone; strict
  (flagged if either model flags); the all-13 verdict for comparison; per-question fail rates; Cohen's kappa.
- No other question set is tested as a result. Any set suggested by run-3 data is labelled exploratory.
