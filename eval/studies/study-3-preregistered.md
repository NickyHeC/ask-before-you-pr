# Study 3: pre-registered, required questions only

Run on 2026-10-22 from 00:37 to about 01:35 PT. The plan was written at 00:36 PT, before any data was drawn: [study-3-preregistration.md](./study-3-preregistration.md).

**Result: the pre-registered bar was not met.** Q1, Q8 and Q9 became suggested, and a pull request counted as flagged only when it failed one of the ten required questions. On the 255 of 283 pull requests where both scorers agreed, the questions flagged 40% of rejected pull requests and 33% of merged ones. That is a gap of +6.6 points (95% CI −5.2 to +18.2), Fisher p = 0.30, against a bar of p < 0.05 and at least 20 points.

## Projects

- **nestjs/nest, sveltejs/kit and vuejs/core,** none used before. Each has no stale or auto-close workflow, no stale bot configuration, no AI, LLM or new-contributor policy, and no bot closing anyone else's pull request.
- **Candidates ruled out:**
  - **an AI or LLM policy:** zulip, Mindustry, shadPS4, obs-studio, TanStack router and query, hono, Vencord, prettier, duckdb, gitea, numpy, pnpm, atuin, docusaurus, egui and mypy.
  - **a stale or auto-close workflow:** FreeCAD, Cataclysm-DDA, lichess, qBittorrent, mastodon, nuxt, go-ethereum, uutils, react-hook-form, zod and fastapi.
  - **bots that close pull requests:** shadcn-ui and vitest.
  - **rules against outside contributors:** Hyprland, Ladybird and bitcoin.
  - **a default branch other than main or master:** laravel, axios, zen-browser and three.js.
  - **too few rejected pull requests:** bluesky-social/social-app.

## Results (agreed pull requests, required set)

| Project (sampled) | Rejected flagged | Merged flagged | Gap [95% CI] | p |
|---|---|---|---|---|
| nest (39 rejected, 50 merged) | 44% | 29% | +15.3 [−5.2, +34.6] | 0.17 |
| kit (44, 50) | 38% | 48% | −9.3 [−29.0, +11.7] | 0.51 |
| vue (50, 50) | 37% | 23% | +13.2 [−5.8, +31.3] | 0.24 |
| **Pooled** | **40%** | **33%** | **+6.6 [−5.2, +18.2]** | **0.30** |

- **The split worked as intended, but did not separate.** Making Q1, Q8 and Q9 suggested cut how often merged pull requests were flagged, from 57% with all 13 questions to 33%. Rejected pull requests were flagged less often by about the same amount, so the gap barely moved: +6.6 points, against +3.7 with all 13.
- **Study 2's best questions did not replicate.** Right layer, cost, size and one concern each separated by 3 points or less.
- **No secondary measure of the required set met the bar.** Neither did Claude alone, the second model alone, nor a strict reading that counts a flag from either scorer.
- **One question ran the wrong way in kit.** "No generated filler" (Q12) failed 35% of merged pull requests and 5% of rejected ones. There, maintainers often push changes to the contributor's branch before merging, so the description no longer matches the final diff.
- **Agreement.** The scorers agreed on 90% of required-set verdicts (kappa 0.79).
- **Spot-check.** 17 pull requests had their material cut. Re-reading them against their full pages would change the verdict of one.

## Deviations from the plan

1. nest had 39 rejected pull requests, not 40. Its pool held exactly 40, and one was superseded by a merged pull request of the same author.
2. The plan excepted only dependabot closing its own pull requests. renovate does the same in all three projects, and it was treated the same way.
3. The core team was built from pull requests closed in the window only. Study 2 also counted members among the authors of older open pull requests, which study 3, with no stale group, did not pull.
4. The base-branch filter came before the seeded shuffle, as the plan's group definitions say. Study 2 had applied it while walking the shuffled list.
5. The window used exact Pacific-time timestamps.

## Limits

- **A rejected pull request is not a low-value one.** Many are well written, and are turned down because the maintainer wanted another approach or did not want the feature, which nothing in the pull request shows.
- **Small groups.** Per-project confidence intervals are about 20 points wide either side.
- **A narrow sample.** All three are JavaScript or TypeScript projects, and two of them have a pull request template that already asks for the problem and the tests.
