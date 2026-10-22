# ask-before-you-pr

Questions to run before a pull request opens on an open-source project.

For contributors, use them to open focused and constructive pull requests.

For maintainers, link them from CONTRIBUTING.md, or copy the ones that fit, so contributors spend their time on changes the project wants.

The questions live in [QUESTIONS.md](./QUESTIONS.md), complemented with reasons and examples. For adopting them in a project, see its "For maintainers" section.

## Install

The repository is the skill: `SKILL.md` sits at its root. Clone it into a skills folder, and keep the folder name equal to the `name` field in `SKILL.md`.

Claude Code, for every project:

```sh
git clone https://github.com/NickyHeC/ask-before-you-pr ~/.claude/skills/ask-before-you-pr
```

Claude Code, for one project: clone it into that project's `.claude/skills/` instead.

Codex, for every project:

```sh
git clone https://github.com/NickyHeC/ask-before-you-pr ~/.agents/skills/ask-before-you-pr
```

Codex, for one repository: clone it into that repository's `.agents/skills/` instead.

## Does it work?

In my own pull requests from August to October, the share closed unmerged fell from 62% to 14%, and the share of my changed lines that never get merged from 47% to 3%.

Starting Sep 10th, running the list of questions became an integral part of my coding process, and I saw significant improvements in reducing wasted effort and saving time.

I also ran 3 studies on other OSS projects, and found that these questions aren't significant in predicting which pull requests maintainers merge. Thus, they are more so a check you run on your own change, rather than a criterion for other people. The numbers, the studies and their data are in [eval/](./eval/).

## Where it comes from

The questions come from the review practice of [smolvm](https://github.com/smol-machines/smolvm).
