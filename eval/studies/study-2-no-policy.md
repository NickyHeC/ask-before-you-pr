# Study 2: three projects with no bots or policies

Run on 2026-10-21 and 22. Not pre-registered. Study 1 found that Godot's policies decided most of its rejections, so this study chose projects where people decide every close.

**Result: no.** On the 367 of 400 pull requests where both scorers agreed, the questions flagged 77% of rejected or stale pull requests and 76% of merged ones. That is a gap of +1.4 points (95% CI −7.9 to +12.0), Fisher p = 0.78. No single project met the bar of p < 0.05 and a gap of at least 20 points.

## Projects

- **ollama/ollama, excalidraw/excalidraw and helix-editor/helix.** None has a stale or auto-close workflow, a stale bot configuration, or an AI, LLM or new-contributor policy in its contributing guide, pull request template, agent instructions or pinned issues. Every unmerged pull request in the window was closed by a person, apart from dependabot closing its own.
- **Ruled out for a policy or a bot:**
  - an AI or LLM policy: neovim, bevy, deno, rust-clippy, ruff, tauri, yt-dlp, immich, julia and ohmyzsh.
  - a stale or close workflow: zed, node, cpython, bun, pytorch, scikit-learn and ComfyUI.
  - other bots: pandas, llama.cpp and tldr.

## Groups

The window, the core-team filter and the definitions follow study 1. Seeds: the draw 20261021, the stale draw 20261022, blinding 4242 and the spot-check 777.

| Project | Rejected | Stale | Merged |
|---|---|---|---|
| ollama | 50 | 49 | 25 |
| excalidraw | 50 | 50 | 32 |
| helix | 44 | 50 | 50 |

- **Rejected:** closed unmerged by a person other than the author. The helix group is its whole pool.
- **Stale:** open, or closed by their own author after 60 days, with no maintainer comment or review in the last 60 days.
- **Merged:** ollama and excalidraw merge few outside pull requests, so their merged groups are their whole pools.

## Results (agreed pull requests)

| Project | Rejected flagged | Stale flagged | Merged flagged | Gap, rejected and stale vs merged | p |
|---|---|---|---|---|---|
| ollama | 71% | 73% | 50% | +22.2 [−1.0, +44.7] | 0.09 |
| excalidraw | 78% | 70% | 79% | −5.4 [−19.8, +14.0] | 0.63 |
| helix | 88% | 85% | 84% | +2.1 [−9.6, +16.4] | 0.80 |
| **Pooled** | **79%** | **76%** | **76%** | **+1.4 [−7.9, +12.0]** | **0.78** |

- **Stale is not a quality signal.** Stale pull requests were flagged at the same rate as merged ones (76% and 76%). Going stale says nobody reviewed it, not that it was bad.
- **The ollama result does not hold up.** Claude alone gave +36 points there. The second model alone gave +5, and the agreed result is p = 0.09.
- **Agreement.** The scorers agreed on 94% of answers (kappa 0.87) and on 92% of verdicts (kappa 0.78).
- **Spot-check.** 90 pull requests were drawn for it, and 11 of them had their material cut. Re-reading those 11 against their full pages changed no score.

## What led to study 3

The questions flag about three in four pull requests everywhere. The two that merged pull requests fail most often are an issue first (Q1, 18%) and evidence it was run (Q8, 29%), and Q9 (CI green) mostly records whether CI ran at all.

Re-scoring after the fact with those three as suggested, rejected-only against merged, gave a gap of +26.9 points (p = 0.0001). The same split on study 1 gave +15.5 points (p = 0.16). The set was chosen after seeing the data, so it was tested again on fresh projects, with the plan written down first. That is study 3.
