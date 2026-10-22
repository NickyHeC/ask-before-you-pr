---
name: ask-before-you-pr
description: "Use before writing a fix, a feature or a pull request for an open-source project you do not maintain, and again before opening the pull request: questions a maintainer's review has asked, run against the planned change so the answers are in the body before anyone asks."
---

# Ask before you PR

Run these against the planned change twice: at discovery, before any code, and again before the
pull request opens. Each line digests a section of `QUESTIONS.md` in this folder, which has the
reason, a public example where one exists, and what passing looks like. That file wins on any
disagreement.

For each question, write the answer in one sentence. If a question has no good answer, stop and
tell the user before writing code. A question that cannot be answered is the finding, and it goes
in the pull request body, not in a comment below it.

Lines marked (suggested) may be skipped for a small, clear change. Say so in the body. Every
other question is required.

## 1. Should this change exist?
- Is the surface about to be redesigned, or frozen? Check issues and recent maintainer work.
- Does today's main branch already do it? Re-read the code there, not on your branch point.
- Is the current behaviour intentional? Look for code, docs or a thread that says it is.
- Is the bug in this project, or in a tool it uses?
- Defect or footgun? If the change alters behaviour a user may rely on, propose docs or an issue.
- Silencing a warning? Then the reason is the whole pull request. Prefer fixing the code.
- (suggested) Beyond a clear bug? An issue and a maintainer's reaction come first.
- A core feature on another vendor's platform? The maintainer decides before any integration exists.

## 2. Is it the cause, or a symptom?
- State the causal chain in one sentence. The fix acts on the cause.
- Is the fix a bigger number? Then the cause is still there.
- Is it part of the fix, such as a hint now and support later? Ship the whole fix or say why not.
- List the sibling sites. Say which you fixed and why you left the others.
- Why did the bug survive? A discarded error or unasserted branch is part of the fix.
- A smaller containment fix can ship first if it makes the failure survivable and visible and
  covers more than your repro.

## 3. Right place, right owner?
- Could an existing component or a lower layer own this?
- Does the material belong in this repository at all?

## 4. What does it cost, permanently?
- What every user pays on every run, forever.
- Machinery proportionate to the failure. A rare, user-caused failure may not earn a guard.
- An existing dependency before a new one. No third-party tool in an example or doc.
- A CI job only for a named regression the build or installer cannot assert itself.

## 5. Are you changing an invariant?
- An execution model change is said out loud, with its consequences listed.
- Running it twice is a no-op.
- Terminal and transient errors are handled differently, and each path says why.

## 6. Bounds, defaults and names
- Every limit traces to a real constraint, or the user sets it.
- When the value cannot be computed, the fallback lands on the cheap side of being wrong.
- Accept awkward user input instead of rejecting it.
- A setting users turn is a named flag, not an environment variable.

## 7. What did you actually observe?
- (suggested) Every claim was seen on the platform it is about. Mark what was reasoned, not run.
- Each declared gap says what it would take to close, and the run is budgeted.
- The body matches the diff: read every path, flag and limit in the body back out of the code.
- Reuse and skip checks verify content, not only a path.

## 8. Review cost
- One concern, its stated purpose only, small enough to read in one sitting.
- For a large feature, measure the size and test share against the maintainer's own pull requests.
- Declare generated code, and where the hand-written change is, in the first paragraph.

## 9. Green, honestly
- (suggested) Run the project's own suite and post the command and result, read from the full log.
- (suggested) A user-facing change gets a test that drives it as a user does.
- (suggested) Extend the existing test file for the surface.
- (suggested) Show the user's need met through the surface they use, not only an internal API.
- No test that needs a committed or generated key or credential.

## 10. The write-up
- The first line says what breaks for a user. Then the mechanism, then the alternative rejected.
- Every deletion is named in the opening lines, with its reason.

## 11. A reply to a person
- Answer what they asked first. One ask. No tables or internal labels. Under about 600
  characters. Thank them for what they did.

Before opening, read the project's CONTRIBUTING file. These questions are a floor, not a style
guide.
