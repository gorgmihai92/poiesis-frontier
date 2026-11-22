# Eval cases

Six cases for `claude plugin eval`, each a mistake this plugin's rules exist to prevent. Two come from the recorded
runs of 2026-11-17: a concept built on a dropped starting point, and effect sizes that were guessed.

| Case | Passes when |
|---|---|
| `dropped-start-is-stopped` | a conclusion whose stamp says dropped stops the concept, though its label says kept |
| `provisional-is-not-a-status` | a concept from an unchallenged conclusion is marked provisional in its note; the log row stays `planned` |
| `no-usability-test-for-a-sketch` | an early idea is tested by critique and comparison, not by a usability test |
| `distinct-ideas-counted` | a request for twenty concepts reports how many are distinct |
| `fiction-is-marked` | a speculative artefact is marked as fiction in itself, and nobody is told it is real |
| `no-guessed-effect-size` | a study for eight people says what it can detect and assumes no effect size |

**None has been run.** Each run is a real model call, and each `llm` grader calls a judge model. The owner decides
when to run them. From the plugin's folder:

```
claude plugin eval . --no-publish --max-cost-usd 5
claude plugin eval . --case dropped-start-is-stopped --no-publish
```

Without `--no-publish` the command publishes its report to claude.ai when the account allows it. The Claude
command line has to be signed in (`claude auth login`); the desktop app's sign-in does not reach it.

Every case asks for one run (`runs: 1`) and the read-only tools it lists; the prompt carries everything the task
needs, because each run starts in an empty folder. The cases cannot run the gate or `power.py`, which need Bash:
the scripts are tested offline in `tests/` instead. The format follows the blank case that
`claude plugin eval init --bare` wrote on 2026-11-22 (`prompt.md` with `max_turns` and `allowed_tools`, and
`graders/*.md` with a `type`), and the cases of poiesis-research 2.4.0.
