---
schema: foundry-doc-v1
title: "Generate a construction cost estimate report"
slug: generate-a-construction-cost-estimate
short_description: "Runs the construction reporting binary against a CSV data directory to produce costing and schedule reports as HTML and PDF, with reconciliation and validation logs — the only interface that exists, since the tool has no console screen and parses no command-line arguments at all."
category: how-to
index_group: financial-construction-tools
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-09-01
editor: pointsav-engineering
paired_with: generate-a-construction-cost-estimate.es.md
research_trail:
  sources: [tool-construction-tco-26/src/main.rs (both report stages and the write_doc output path), tool-construction-tco-26/src/compute/cost_estimate.rs (input schema and the reconcile tolerance), tool-construction-tco-26/src/compute/schedule.rs (input schema, date-format parsing, validate checks), tool-construction-tco-26/Cargo.toml (the real bin targets), tool-construction-tco-26/src/bin/*.rs (the pipeline binaries this guide deliberately does not cover)]
  verification_method: "read the Rust source directly rather than a design document's prose description of it; confirmed by grep across the whole crate that no binary parses a command-line argument, links an argument-parsing crate, or implements --help, so every 'flag' a guide could plausibly document does not exist; input-file schemas taken from the loader modules' own field indices rather than from a schema table that could have drifted; the console-output example carries structural counts only, matching the source's own deliberate refusal to print money or dates to stdout"
---

## Prerequisites

- A working Rust toolchain (see [[install-toolchain]])
- A checkout of the workspace containing the construction crates
- A data directory holding `cost_estimate.csv` and `schedule.csv` in the schemas below
- Write permission on that directory — the run creates an output subdirectory inside it

No services need to be running for this task. Other binaries in the same crate do depend on archive-resident services; this one reads two files and writes six.

## Purpose

Produce the two kick-off documents for a construction project — a costing report and a schedule with a Gantt timeline — as HTML and PDF, alongside two machine-checkable logs that state whether the source data is internally consistent.

This is a batch task on the command line, and the command line is the whole interface. `tool-construction` has no terminal screen, no F-key slot, and no graphical surface of any kind. There is nothing to click and no view to open; a guide describing one would be describing something that does not exist.

For the ledger design these reports sit on top of, see [[tool-construction]].

## Procedure

### 1. Point the tool at your data directory

```bash
export TCO26_DATA_DIR=/data/construction/example-project
```

Set this. If the variable is unset the binary falls back to a hard-coded absolute path belonging to the deployment it was first built for — a path that will not exist on your machine, so the run fails on the first file read with an error naming a directory you have never heard of. That fallback is a convenience for one machine, not a default worth relying on.

### 2. Confirm the two input files

The tool reads exactly two files from that directory, both plain CSV with a header row.

`cost_estimate.csv`:

```
category,component,quantity,unit,unit_cost,price,rate_per_sf,rate_per_sm,pct_of_total,tier,excluded_flag,source_doc,source_page
```

`schedule.csv`:

```
task_id,task_name,parent_id,indent_level,task_type,duration_days,start_date,finish_date,phase,source_doc,source_page
```

Two fields behave less simply than their names suggest, and both are worth checking before a first run:

- **`quantity`** in the cost estimate is genuinely four different things depending on the row: a measured amount with a unit, a rate applied to a basis, the literal string `Excluded`, or empty. The loader models all four. It is not a number column with some blanks.
- **`start_date`** and **`finish_date`** accept ISO `2026-06-13`, US `6/13/2026` or `6/13/26`, a weekday-prefixed form such as `Mon 6/13/26` (what a scheduling tool's default export commonly emits), and `Jun 13, 2026`. Anything else parses as absent. The parser returns nothing rather than guessing — see the verification step below for why that matters more than it sounds.

### 3. Run the report binary

From the workspace root:

```bash
cargo run -p tool-construction-tco-26
```

That is the complete command. There are no flags, no subcommands, and no positional arguments — the binary does not parse a command line at all, so there is no `--help` to consult, no `--output` to redirect with, and no way to run only the costing stage or only the schedule stage. One invocation always runs both, cost estimate first, then schedule. Every knob the tool has is an environment variable.

### 4. Read the console summary

A successful run prints structural counts and file paths, and nothing else:

```
[cost estimate] 0 variance(s) — see /data/construction/example-project/outputs/2026/cost_estimate_reconciliation.log
Wrote /data/construction/example-project/outputs/2026/cost_estimate.html
Wrote /data/construction/example-project/outputs/2026/cost_estimate.pdf
[cost estimate] categories: 7, allowances: 4
[schedule] 0 defect(s) — see /data/construction/example-project/outputs/2026/schedule_validation.log
Wrote /data/construction/example-project/outputs/2026/schedule.html
Wrote /data/construction/example-project/outputs/2026/schedule.pdf
[schedule] tasks: 118, phases: 8
```

The absence of money and dates is deliberate, not an oversight. An early build printed reconciliation totals to the terminal; the behavior was changed so that stdout carries only counts, and anything substantive lands in a file. Do not add a print statement to "just check a number quickly" — write it to the output directory instead.

## Expected outcome

Six files in `<data-dir>/outputs/<year>/`, which the run creates if it is absent:

| File | What it is |
|---|---|
| `cost_estimate.html` / `.pdf` | The costing report — categories, line items, allowances, exclusions, totals |
| `schedule.html` / `.pdf` | The schedule report, including a Gantt timeline and per-phase pages |
| `cost_estimate_reconciliation.log` | Whether every total in the source ties to the lines beneath it |
| `schedule_validation.log` | Structural defects found in the task tree and task dates |

## Verification

Three checks, in this order. The third is not optional.

**Read the reconciliation log.** The tool re-adds each category's non-excluded line prices and compares the result to that category's own printed total, then does the same for the base total, the allowances total, and the grand total against base plus allowances. The tolerance is two cents. An empty variance list means the source document is internally consistent. A non-empty list is a real finding about the input data, not a bug in the tool — each entry names the scope, the computed figure, the printed figure, and the difference.

**Read the validation log.** The schedule check reports a task whose declared parent does not exist, a task whose indent level disagrees with its parent's depth, and a task that finishes before it starts, plus any defect the loader recorded while parsing.

**Open the PDF and look at it.** Both real defects this reporting path has produced were invisible to the logs and obvious on the page. A too-narrow column silently truncated identifiers to an ellipsis while every count and check reported success. Separately, a date format the parser did not yet accept produced empty Start and Finish columns and a blank timeline — and because the inverted-span check only runs when *both* dates parse, that failure reported as **zero defects**. A clean log next to an empty date column is the signature of that failure, not evidence of a clean schedule.

## What this task does not do

- **It does not estimate.** The costing report renders and cross-checks the figures the CSV already states. It does not build a bottom-up estimate from work packages, quantities, and labour rates. That pipeline exists — it is the `calibrate`, `solve_rate`, and `post_ledger` binaries in the same crate — but it depends on archive-resident materials, schedule, and notification services being reachable, and it is a different task from this one.
- **It does not report earned value.** Independently observed installed quantity is the input every earned-value and cost-performance figure depends on, and no source for it exists in this data model today. Reports that would consume it are planned; none is produced by this command.
- **It is not yet multi-project.** The reporting crate is per-deployment, and its name carries a deployment-specific suffix. A second deployment currently means a second bin crate rather than a project argument — which is the honest reason step 3 has no `--project` flag to document.
- **It writes no ledger entries.** This command reads two files and renders documents. Posting to the ledger is `post_ledger`'s job.

## Edge cases

- **A missing or unreadable `cost_estimate.csv`** prints `Failed to load <path>: <error>` to stderr and exits with status 1. Nothing is written.
- **A missing `schedule.csv`** fails the same way — but only after the costing report has already been written. Half an output set is the expected result of that failure, not corruption. Fix the input and re-run; the files are overwritten.
- **A row with fewer fields than the header** is not skipped with a warning. Both loaders index fixed column positions, so a short row aborts the run. Repair the CSV rather than working around it.
- **Output files are overwritten in place.** There is no versioning, no timestamped directory, and no prompt. Copy anything you need to keep before re-running.
- **A date the parser cannot read is left empty rather than coerced.** This is correct behavior and it is also how an entire empty timeline can render without a single error — hence the visual check above.

## Rollback

Nothing to undo in the source data: the run reads `cost_estimate.csv` and `schedule.csv` and never writes to them. Its only writes are the six files under `outputs/<year>/`. Delete them, or re-run to replace them.

## Next steps

- [[export-structured-data]] — moving the rendered output or its source records somewhere else
- [[install-toolchain]] — if `cargo run` is not yet available on your machine

## See also

- [[tool-construction]] — the ledger design, cost-code model, and earned-value approach these reports render
- [[tool-accounting]] — the sibling accounting engine designed to receive cost from this ledger
- [[financial-and-construction-tools-overview]] — where this tool sits among the financial and construction tools
