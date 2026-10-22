# Ask before you PR

Here are helpful questions to run before a pull request opens on an open-source project you do not maintain.

They serve two readers. A contributor (or the coding agent writing the change) runs them so the pull request is actually usable, and nobody spends a week on work that was never going to merge. A maintainer links them from CONTRIBUTING.md (or adapts their own version), so contributors spend their time on changes the project wants.

Almost none of the questions ask whether the code is correct. They ask whether the change should exist, whether it fixes the cause, whether it sits in the right place, and whether the evidence is real. Correct code in the wrong place is the most common way a pull request gets closed.

They were drawn from about six months of review comments of the lead maintainer of [smolvm](https://github.com/smol-machines/smolvm), an open-source microVM runtime written in Rust. Each example below is one of those comments on a public thread. Most questions were asked more than once.

Run the questions twice: at discovery, before any code is written, and again before the pull request opens. An unanswered question is a round trip, and a round trip on a quiet PR can cost a week. The answer to common questions should belong in the pull request body, before anyone even asks.

Most questions are required: a pull request that fails one is not ready to open. Six are marked *Suggested*. They ask whether you raised the change first and whether you showed it running or tested. Maintainers often waive these for a small, clear change, so skipping one does not make a pull request unwelcome. Answering them still saves a round trip.

## 1. Should this change exist?

### Is this surface about to be redesigned, or frozen?

Correct code on a surface headed for a redesign gets closed with a one-line reason.

**Passing:** you checked open issues, the roadmap and recent maintainer pull requests for plans that touch this surface.

### Does the current main branch already do this?

On an active project the fix can land under you in a day.

**Passing:** you re-read the code on today's main branch, not on the commit you branched from, and checked whether the maintainer has work open on the same files.

### Is the current behaviour intentional?

Some failures are deliberate, and a fix for one costs the maintainer an explanation. **Example:** [#113](https://github.com/smol-machines/smolvm/pull/113) gated Linux-only system calls so a component would build on macOS. The maintainer closed it the same day: that component is meant to build only on Linux, and an explicit failure is preferred to conditional compilation.

**Passing:** you can point to code, docs or a past thread showing the behaviour is unintended.

### Is the bug in this project at all?

The right fix sometimes belongs to the other tool. **Example:** [#506](https://github.com/smol-machines/smolvm/issues/506) reported that an install through a version manager failed on sparse disk files. The maintainer replied that the sparse files are intentional, so a large disk only takes up the space it uses, and that the other tool's extractor should support them.

**Passing:** you can name the component that breaks its own contract, and it is this one.

### Is it a defect, or a footgun?

A defect breaks the code's own stated contract and gets a code fix. A footgun works as designed but surprises people, and its fix is usually documentation, because changing the behaviour can break someone who relies on it. **Example:** on [#1003](https://github.com/smol-machines/smolvm/issues/1003), the maintainer described part of the report as a footgun rather than a bug: `localhost` passed to the guest resolves to the guest's own loopback.

**Passing:** you can quote the contract the behaviour breaks. If you cannot, start with an issue or a docs change.

### Are you silencing a warning instead of fixing what it points at?

Then the reason is the whole pull request, and it has to be in the body. **Example:** [#1006](https://github.com/smol-machines/smolvm/pull/1006) allowed two new lints at the workspace level after a toolchain update turned CI red. The maintainer asked for the reason within about three hours, and the same day merged [#1008](https://github.com/smol-machines/smolvm/pull/1008), which rewrote the flagged code with no suppression.

**Passing:** the body says why the warning is wrong for this code, or the change fixes the code.

### Is this big enough to ask about first?

*Suggested.*

Code is cheap for a maintainer. A design question they have not settled is not. **Example:** [#219](https://github.com/smol-machines/smolvm/issues/219) asked whether the project could build a local Containerfile. The maintainer answered before any code was written: not planned, because the project's own machine format is meant to replace that file.

**Passing:** for anything beyond a clear bug, an issue exists and the maintainer has reacted to it.

### Does it tie a core part of the project to another vendor's platform?

Which platform a core part sits on is the maintainer's decision. Building the integration first can waste all the work built on it.

**Passing:** before any integration code exists, the maintainer has read one paragraph naming the platform and the alternative of keeping it in the project's own code.

## 2. Is it the cause, or a symptom?

### Can you state the causal chain in one sentence?

"X happens because Y, caused by Z." A gap in the chain means you are patching the gap.

**Passing:** the sentence is in the body, and the fix acts on Y or Z, not on X.

### Is your fix a bigger number?

A raised limit makes the repro pass and leaves the cause in place. **Example:** [#699](https://github.com/smol-machines/smolvm/pull/699) first raised a timeout for a slow start. The maintainer asked to dig deeper. The merged version streams progress while the work runs and removes the increase.

**Passing:** no limit moved, or the new value traces to a real constraint the body names.

### Are you shipping part of the fix?

A partial fix, such as a better error message now and the real support later, is a round trip. **Example:** the first version of [#1797](https://github.com/smol-machines/smolvm/pull/1797) improved a hint for an input the command did not accept. The maintainer asked to fix the issue instead of a partial, and the full support merged within a day.

**Passing:** the change fixes the problem the user hit, or the body says why the rest cannot ship now.

### Did you fix every sibling of the site you found?

A fix at one of several identical sites reads as unfinished. **Example:** [#967](https://github.com/smol-machines/smolvm/pull/967) rolled back state after one kind of failure. The maintainer merged it with a note to apply the same handling to other cases as a follow-up.

**Passing:** the body lists the sibling sites, which ones you fixed, and why you left the others.

### Why did the bug survive?

If the answer is a discarded error, an ignored return value, output sent to `/dev/null` or a branch no test asserts, that line is part of the fix.

**Passing:** the line that hid the failure is fixed in the same change.

### Is there a smaller containment fix that protects more cases?

Sometimes the right first change is not the root cause. A small change that leaves the system in a recoverable state, and makes the failure visible, can protect every future case of the class, including ones nobody has found yet. It does not license a bigger number. If it only makes your one repro pass, it is a symptom patch.

**Passing:** the containment fix is small, makes the failure both survivable and visible, covers cases beyond yours, and ships on its own, with the cause fix referencing it.

## 3. Is it in the right place, with the right owner?

### Can an existing component, or a lower layer, own this?

New responsibility in the wrong layer is a forever cost. **Example:** [#316](https://github.com/smol-machines/smolvm/pull/316) added archive handling for booting from a local image. The maintainer asked whether that work could be delegated to the container runtime the project already uses.

**Passing:** the body names the lower layers and existing components you considered, and why each one could not do it.

### Does it belong in this repository?

Some material has a home of its own. **Example:** [#1664](https://github.com/smol-machines/smolvm/pull/1664) added a benchmark suite. The maintainer replied that benchmarks are run and stored in a separate repository, and the pull request was closed.

**Passing:** you checked where the project keeps this kind of material.

## 4. What does it cost, permanently?

### What does every user pay, on every run, forever?

A maintainer prices the forever cost, not the cost today. **Example:** [#86](https://github.com/smol-machines/smolvm/issues/86) asked for first-boot bootstrap support. The maintainer replied that it would multiply boot time roughly tenfold, and the request was closed.

**Passing:** the body states the runtime, size or maintenance cost the change adds for everyone.

### Is the machinery proportionate to the failure?

A rare failure that the user caused, seen only on a developer's machine, may not deserve new enforcement. Correct code guarding against a real failure can still be closed because it does not earn its keep.

**Passing:** the body says how often the failure happens, who hits it, and why the guard is worth its permanent cost.

### Does an existing dependency already do this?

**Example:** [#657](https://github.com/smol-machines/smolvm/pull/657) added a crate to expand `~` in paths. The maintainer pointed to a crate the project already depends on that covers the same need.

**Passing:** no new dependency, or the body says why the existing ones cannot do it.

### Does an example or a doc now depend on a third-party tool?

In an example, a dependency becomes the recommended path. **Example:** on [#600](https://github.com/smol-machines/smolvm/pull/600), whose first version built its worker image with Docker, the maintainer said a project example should not depend on Docker and a Dockerfile, because that adds a third party and more to manage.

**Passing:** the example runs with the project's own tools.

### Could the artifact carry this guarantee instead of CI?

A CI job is a cost every future pull request pays. **Example:** on [#1122](https://github.com/smol-machines/smolvm/pull/1122), the maintainer rejected a new CI check for the install: CI is not the place to catch it, and the build and install steps should be made more robust instead.

**Passing:** you can name the regression the job catches, and why the build script or installer cannot assert it itself.

## 5. Are you changing an invariant?

### Does this change an execution model?

**Example:** [#216](https://github.com/smol-machines/smolvm/pull/216) moved the guest agent from one thread to a thread per connection. The maintainer spelled out what that touches, starting with the single channel all host and guest traffic passes through.

**Passing:** the body says the model changes and lists the consequences before the reviewer does.

### What happens if it runs twice?

**Example:** on [#350](https://github.com/smol-machines/smolvm/pull/350), which enabled GPUs for interactive sessions, the maintainer asked for an idempotency guard, a check that the mounts are not already present, so they are never added twice.

**Passing:** a second run is a no-op, and you have run it twice.

### Do you treat terminal and transient errors differently?

Retrying a permanent failure and giving up on a temporary one are both bugs. **Example:** [#247](https://github.com/smol-machines/smolvm/pull/247) proposed carrying on with a pull when a manifest failed to parse. The maintainer asked whether any such failure is one where continuing is wise.

**Passing:** each error path says whether it is retried, and why.

## 6. Are the bounds, defaults and names defensible?

### Is every limit tied to a real constraint, and is it yours to set?

Arbitrary numbers get challenged every time. **Example:** [#957](https://github.com/smol-machines/smolvm/pull/957) widened a fixed timeout for large inputs. The maintainer asked about a user-configurable value instead, since the input size is not something the project controls.

**Passing:** each number traces to a real limit, or the user sets it.

### When the value cannot be computed, which way does the fallback fail?

A default is a direction as well as a number. **Example:** [#1322](https://github.com/smol-machines/smolvm/pull/1322) sized a disk from the image. The maintainer noted that over-sizing is free because the disk is sparse and under-sizing fails, so a failed size probe should fall back to a generous floor.

**Passing:** you can name the cheap side of being wrong, and the failure path lands there.

### Are you rejecting input you could simply accept?

An explicit failure suits an unsupported platform. It does not suit awkward user input. **Example:** [#277](https://github.com/smol-machines/smolvm/issues/277) reported a crash on short machine names. The maintainer chose to pad the name rather than reject it.

**Passing:** the change errors only on input it cannot handle.

### Is a knob that users turn a named flag?

A flag is public interface. An environment variable is for what nobody should need to touch. **Example:** [#1511](https://github.com/smol-machines/smolvm/pull/1511) added a tuning setting as an environment variable, and the maintainer asked for named flags instead.

**Passing:** every user-facing setting is a documented flag.

## 7. What did you actually observe?

### Did you run it where the behaviour lives?

*Suggested.*

Real hardware is the scarcest thing a contributor brings. A laptop cannot honestly validate behaviour on another architecture or inside a Linux guest. **Example:** on [#601](https://github.com/smol-machines/smolvm/pull/601), the maintainer asked to verify a cross-compiled link on an ARM machine first, because iterating through CI is slower and flaky.

**Passing:** every claim in the body was seen on the platform it is about, and the body says which claims were reasoned rather than run.

### Is every gap you declare one you can close?

Declaring a limit is right. The reviewer will hand it back as a work item. **Example:** the body of [#1005](https://github.com/smol-machines/smolvm/pull/1005) said one case had not been run. The maintainer's whole review was a request to validate it and add an end-to-end test. Both were done the same day and it merged.

**Passing:** each "not validated" line says what it would take, and you have budgeted the run.

### Does the body match what the diff does?

The body is a claim about the diff, so check it against the diff, not only against the repro. A body that promises one path, flag or limit while the code ships another loses the reviewer's trust in the rest.

**Passing:** every specific noun in the body, each path, flag, limit and status code, reads back out of the diff unchanged.

### Does your check verify content, or only that a path exists?

A cache hit or a skipped step that trusts a name can reuse the wrong thing. **Example:** on [#1442](https://github.com/smol-machines/smolvm/pull/1442), the maintainer asked to validate artifact checksums rather than just checking paths.

**Passing:** reuse is keyed on content, not location.

## 8. What will it cost the reviewer?

### Is it one concern, and only its stated purpose?

**Example:** [#233](https://github.com/smol-machines/smolvm/pull/233) combined two unrelated features, and the maintainer asked for two separate pull requests.

**Passing:** the title names one problem, every file in the diff serves it, and the diff is small enough to read in one sitting, or the body says why it cannot be.

### Is the size measured against the maintainer's own pull requests?

When a maintainer wants a feature as one pull request, compare its size and share of test code with their own recent feature pull requests, not a fixed line count. One far over that may not be read until it is cut.

**Passing:** you compared the diff's size and test share with the maintainer's recent feature pull requests, and cut before asking for review.

### Is generated code declared as generated?

A diff that is mostly generated code gets priced by its line count unless the body says so.

**Passing:** the first paragraph says how many lines are generated, by what, and where the hand-written change is.

## 9. Is it green, honestly?

### Did you run the project's own test suite and post the results?

*Suggested.*

**Example:** on [#195](https://github.com/smol-machines/smolvm/pull/195), the maintainer asked for the results of running the project's end-to-end suite.

**Passing:** the body has the command you ran and its result, read from the full log.

### Is the test at the level the reviewer trusts?

*Suggested.*

**Example:** on [#958](https://github.com/smol-machines/smolvm/pull/958), a CLI change, the maintainer noted that unit tests for command-line options are often unreliable for real usage, and asked for end-to-end CLI tests.

**Passing:** a user-facing change has a test that drives it the way a user does.

### Did you extend the existing test file?

*Suggested.*

The suite that already covers the surface should grow, not get a shadow beside it. **Example:** on [#1066](https://github.com/smol-machines/smolvm/pull/1066), the maintainer called out the updates to the existing tests with approval before merging.

**Passing:** new cases sit in the file that already tests this surface.

### Can you show the user's need met through the surface they use?

*Suggested.*

A test plan that drives an internal API answers a different question from the one a maintainer means by "how do I test this". If users reach the feature through a CLI, an API or a UI, that is where the proof belongs.

**Passing:** the body walks through the user's own steps, on the surface they will use, and shows the result they wanted.

### Does any test need a key or credential the repository would carry?

Then the test goes, not the key. A test that only runs with a secret either leaks it into the repository or never runs in anyone else's checkout, and generating the secret at run time does not fix that.

**Passing:** no test depends on a committed or generated secret, and the body says what loses coverage.

## 10. Does the write-up answer before they ask?

### Does the body say what problem it solves?

A body that opens with the state of things leaves the reviewer to guess the problem. **Example:** [#935](https://github.com/smol-machines/smolvm/pull/935) opened with a count of test suites that CI did not run. After a long reply on the mechanism, the maintainer asked what problem the pull request solves. It closed unmerged.

**Passing:** the first line says what breaks for a user, then the mechanism, then the alternative you rejected.

### Are you removing something? Say why first.

**Example:** [#1822](https://github.com/smol-machines/smolvm/pull/1822) was a docs update that also deleted a source file. The maintainer asked whether that was intentional.

**Passing:** every deletion is named in the body's opening lines, with its reason.

## 11. Is it a reply to a person?

### Would a maintainer type this?

A reply to someone who reported a problem is a conversation, not a report. Tables, bold lead-ins and internal labels read as a document filed at them. **Example:** in [#922](https://github.com/smol-machines/smolvm/issues/922), the maintainer's first reply to the reporter was a single question: whether the binary ran under WSL2 or natively.

**Passing:** it answers what they asked first, makes one ask, stays under about 600 characters, and thanks them for what they did.

## For maintainers

To adopt these questions in your own project:

- Link this file from your CONTRIBUTING.md, next to your own rules, as the questions to answer before opening a pull request.
- Or copy the questions that fit your project into CONTRIBUTING.md, and swap the examples for threads from your own reviews.
- Point coding agents at SKILL.md. It is a short digest of this file in the skill format that Claude Code and Codex load, and the README says where to install it.

Questions you add from your own reviews are the most useful ones, because they are the ones your contributors will actually be asked.

## Limits

These questions do not replace a project's own CONTRIBUTING file, its review history or its CI configuration. Read those first. Every project prices things differently, and these examples come from one project and one maintainer's review.

They are a floor, not a style guide. Passing all of them does not mean a pull request will merge. Failing one is a reason to stop and ask before writing the code. If a question has no good answer, say so in the body. A weakness stated first costs less than one the reviewer finds.
