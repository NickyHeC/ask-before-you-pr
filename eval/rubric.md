# The scoring rubric

The studies did not score pull requests against all 43 questions in [QUESTIONS.md](../QUESTIONS.md). Many of them can only be answered by the author before the code exists. The rubric keeps 13 questions that can be judged from what a pull request shows in public: the title, the body, linked issues, the file list, the diff when it is small, the CI result, and the discussion before it closed.

Both scorers were given the same text in all three studies: [scorer-instructions.txt](./scorer-instructions.txt). It is published with internal names removed: its title, the name of the internal document the questions were drawn from, and an internal section number after each question. Nothing that tells a scorer what to do was changed. The original's sha256, as cited in study 3's plan, is `0d8b7f6eb211f883d52f54ef50d770c4b445f17e2eafcdb8f4cc039e94fd68ab`. The table below maps each rubric question to its section of QUESTIONS.md.

| # | Rubric question | Section of QUESTIONS.md | In study 3 |
|---|---|---|---|
| Q1 | Was the change wanted before it was written (an issue or proposal first)? | 1. Should this change exist? | suggested |
| Q2 | Does the title or body say what problem it solves? | 10. Does the write-up answer before they ask? | required |
| Q3 | For a bug fix, is the cause named? | 2. Is it the cause, or a symptom? | required |
| Q4 | Does the fix avoid managing the symptom? | 2. Is it the cause, or a symptom? | required |
| Q5 | Does the change sit at the right layer? | 3. Is it in the right place, with the right owner? | required |
| Q6 | Is the permanent cost proportionate? | 4. What does it cost, permanently? | required |
| Q7 | If it changes behaviour users rely on, is that explained? | 1. Should this change exist? and 5. Are you changing an invariant? | required |
| Q8 | Does the PR show the change was run or tested? | 7. What did you actually observe? and 9. Is it green, honestly? | suggested |
| Q9 | Did CI pass on the final head? | 9. Is it green, honestly? | suggested |
| Q10 | Is the hand-written change a reviewable size (150 changed lines, or a reason it cannot be split)? | 8. What will it cost the reviewer? | required |
| Q11 | Is it one concern, touching only what its purpose needs? | 8. What will it cost the reviewer? | required |
| Q12 | Is the write-up free of filler and unverifiable claims? | 7. What did you actually observe? and 8. What will it cost the reviewer? | required |
| Q13 | Is there no sign it duplicates an existing PR, feature or fix? | 1. Should this change exist? | required |

Studies 1 and 2 flag a pull request when it fails any of the 13. Study 3 flags it only when it fails a required question.

Q10's 150 lines is a stand-in for scoring. QUESTIONS.md measures size against the maintainer's own pull requests, which a scorer reading one pull request cannot see.

The rubric scores the pull request, not the author's process. It cannot see whether the author ran the questions before writing code, which is the use the questions are written for.
