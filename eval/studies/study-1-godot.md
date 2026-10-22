# Study 1: Godot

Run on 2026-10-21. Not pre-registered. The question: do the 13 rubric questions flag pull requests Godot's maintainers rejected more often than ones they merged?

**Result: no.** On the 83 of 100 pull requests where both scorers agreed, the questions flagged 60% of rejected pull requests and 52.5% of merged ones. That is a gap of +8.0 points (95% CI −12.9 to +27.9), Fisher p = 0.51. The bar set before scoring was p < 0.05 and a gap of at least 20 points.

## Sample

- **Repository.** QGIS was the first choice but could not be sampled: in the window, only 14 of its unmerged pull requests were closed by a maintainer. A stale bot, other bots and the authors themselves closed the rest. Godot was used instead.
- **Window.** Pull requests closed from 2026-04-21 to 2026-10-21.
- **Outside contributors only.** Anyone who closed someone else's pull request, merged one, or held member or collaborator status in the window counts as the core team (33 people) and is left out.
- **Rejected.** 50 drawn at random (seed 20261021) from 135: closed unmerged by someone other than the author, not a draft, based on the main branch.
- **Merged.** 50 drawn the same way from 542, leaving out dependency bumps and cherry-pick batches.

## Scoring

- Each pull request was relabelled G001 to G100 (seed 4242) and scored on title, body, linked issues, file list, the diff when 200 changed lines or fewer, the CI result, and up to 10 discussion items from before the close. Labels and the closer's comments in the last 24 hours were removed, since they give the outcome away.
- Two scorers used the same [instructions](../scorer-instructions.txt): Claude and a second model from another provider. In this study the Claude scores came from a single agent that also ran the study. In studies 2 and 3 they came from fresh agents that saw only the instructions and the material.
- The scorers agreed on 93.8% of answers (kappa 0.83) and on 83% of verdicts (kappa 0.66).
- A spot-check of 20 pull requests against their full GitHub pages changed 1 of 260 answers and no verdict.

## Why the gap is small

- **Most rejections were about who or what wrote the pull request.** 32 of the 50 were closed under Godot's 2026 policies: 18 under its AI-authorship policy, 12 labelled spam (agent-submitted), and 2 under "no features from new contributors". The rest were superseded by another pull request (7), not wanted or the wrong approach (5), already fixed or wrong (2), no response (2) or unclear (2).
- **Policy-closed pull requests look like merged ones.** 13 of the 32 passed every question under both scorers. Agent-written pull requests often have tidy write-ups with a cause and testing notes, which is what the questions check.
- **Merged pull requests fail too.** About half failed at least one question, mostly evidence it was run (Q8) and size (Q10). Godot's reviewers often test small fixes themselves and merge them.

The close category of every rejected pull request is in [the data](../data/run1-godot.csv).
