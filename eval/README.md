# Evaluation

## My own pull requests, month by month

Every pull request I opened on the smol machines organization's repositories from August on, by the month it opened (Pacific time), with its outcome as of 2026-10-22. July was onboarding and is left out.

| Month | Days | Opened | Unmerged share of closed PRs | Merged lines | Unmerged share of changed lines | Merged PR per day |
|---|---|---|---|---|---|---|
| August | 31 | 68 | 62% | 14,367 | 47% | 0.84 |
| September | 30 | 34 | 33% | 21,274 | 21% | 0.73 |
| October | 22 (Oct 1 to 22) | 26 | 14% | 43,784 | 3% | 0.82 |

**Sep 10:** the questions became a required step before any code was written.

## What this shows

Merged output held steady at about 0.7 to 0.85 pull requests a day. What fell was everything else: unmerged pull requests went from 42 in August to 3 in October, the number opened from 68 to 26, and the share of my changed lines that never merged from 47% to 3%. Almost every unmerged pull request was one I withdrew myself. So the questions did not make my merged work faster. They stopped me opening work that was never going to land, which is what they are for: deciding before the code is written.

Three studies on other projects tested something different: whether the questions, scored on a pull request after the fact, tell the ones maintainers rejected apart from the ones they merged. They do not. The questions are a check you run on your own change, not a filter for someone else's.

The limits of my own numbers: they cover one person, with no control group. Some of the change is learning the job, and by October I was working on assigned features with a maintainer who knew my work.

## The three studies

Each study scored outside contributors' pull requests with two models from different providers, blind to the outcome, using the same [rubric](./rubric.md). A pull request counts as flagged when it fails a question. Each comparison uses the pull requests both models agreed on. The bar for a result was set before scoring: Fisher p < 0.05 and a gap of at least 20 points.

| Study | Projects | Pull requests | Flagged, rejected | Flagged, merged | Gap [95% CI] | p |
|---|---|---|---|---|---|---|
| [1](./studies/study-1-godot.md) | Godot | 100 | 60% | 52.5% | +8.0 [−12.9, +27.9] | 0.51 |
| [2](./studies/study-2-no-policy.md) | ollama, excalidraw, helix | 400 | 77% (rejected and stale) | 76% | +1.4 [−7.9, +12.0] | 0.78 |
| [3](./studies/study-3-preregistered.md), pre-registered, required questions only | nest, SvelteKit, Vue | 283 | 40% | 33% | +6.6 [−5.2, +18.2] | 0.30 |

None meets the bar. Godot's rejections were mostly decided by its AI and new-contributor policies, so study 2 chose projects that use no bots or policies. Study 3 then tested, on fresh projects and with the plan written first, a split that study 2's data suggested: an issue first, test evidence and CI green as suggested questions, not required ones.

Two findings outlast the null result:

- **Making those three questions suggested cuts how often merged pull requests are flagged,** from 57% to 33%. Maintainers often waive them for a small, clear change. That is why QUESTIONS.md marks the questions behind them, raising a change first and showing it run or tested, as *Suggested*.
- **A pull request going stale says nobody reviewed it, not that it was bad.** In study 2, stale pull requests were flagged at the same rate as merged ones.

## What is here

| Path | What it holds |
|---|---|
| [rubric.md](./rubric.md) | The 13 scored questions, mapped to QUESTIONS.md, and which were required in study 3 |
| [scorer-instructions.txt](./scorer-instructions.txt) | The text both models scored with, unchanged across the studies apart from internal names removed for publishing |
| [studies/](./studies/) | One write-up per study, and study 3's plan as written before it ran |
| [data/](./data/) | Every score from both models, by blind ID, with no pull request numbers. Columns: `id`, `repo`, `group`, `close_category` (study 1's rejected group only), `scorer`, `Q1` to `Q13` (`P`, `F` or `NA`) |
| [scripts/](./scripts/) | `analyze.py` reproduces every study number above from `data/` (`python3 eval/scripts/analyze.py`, needs scipy). The others are study 3's pipeline: `policycheck.sh` screens a project, `collect.sh`, `closers.py` and `pools.py` build the pools, `fetchall.sh` and `fetch.py` fetch the material a scorer reads, and `blind.py` draws and blinds the sample |

The seeds are in each study's write-up, and study 3's in its plan. They redraw the same samples as long as the pools on GitHub have not changed. The pipeline scripts run from one working folder, in this order: `policycheck.sh`, `collect.sh`, `closers.py`, `pools.py`, `fetchall.sh`, then `blind.py`. The second model read `scorer-instructions.txt` followed by ten pull requests' material, in a fresh conversation for each batch. In studies 2 and 3 the Claude scores came from fresh agents given only the same instructions and the material.

Pull request numbers and the scorers' reasons are left out of `data/`. They would point at individual contributors' work.
