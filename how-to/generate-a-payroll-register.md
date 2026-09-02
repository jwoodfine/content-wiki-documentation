---
schema: foundry-doc-v1
title: "Generate a payroll register"
slug: generate-a-payroll-register
short_description: "Runs the payroll binary to aggregate budgeted labour hours by division into an HTML and PDF register — a narrow report that computes no gross pay, no pay frequency, and no remittance, and prints an em dash rather than a number wherever it has none."
category: how-to
index_group: financial-construction-tools
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-09-01
editor: pointsav-engineering
paired_with: generate-a-payroll-register.es.md
research_trail:
  sources: [tool-payroll-tco-26/src/main.rs (the four file reads, the compiled-in jurisdiction constant, the output path, and the single console line), tool-payroll-tco-26/src/compute/labour_by_division.rs (the longest-prefix cost-code join, the field indices actually read from each input, and the silent-drop behaviour on an unmatched or unparseable row), tool-payroll-tco-26/src/compute/wage_rules.rs (the jurisdiction table schema and its panic on an unrecognised day_counting value), tool-payroll-tco-26/src/report/register.rs (the five-column table, the em-dash cells, and the conditional basis-of-preparation paragraph), tool-payroll-tco-26/data/wage_payment_rules.csv (the real header and the single populated jurisdiction row), tool-payroll-tco-26/Cargo.toml and the workspace manifest (bin target and workspace membership), tool-construction-tco-26/data/division_crosswalk.csv and crew_assumptions.csv (the two reference-data headers this crate reads out of its sibling)]
  verification_method: "read the Rust source directly rather than any design document's description of it, which matters more than usual here because the crate went from an empty stub to a shipping report inside two days and prose about it dates quickly; confirmed by reading main.rs end to end that no command-line argument is parsed anywhere and that the jurisdiction is a compile-time constant, so no flag exists to document; the em-dash columns were traced from the renderer's own cell construction rather than inferred from a screenshot, and the modules' comments confirm both are deliberately deferred rather than unfinished; the silent-drop edge case was derived from the aggregation loop's own control flow, which increments no counter and emits no warning on either miss; every figure and path in the examples below is invented, and the deployment's compiled-in project label is described rather than reproduced because it names a real site"
---

## Prerequisites

- A working Rust toolchain (see [[install-toolchain]])
- A checkout of the workspace containing the construction crates — the payroll crate is a member of it, and reads two reference files out of the construction crate's own directory at a path resolved when it compiles
- A construction data directory holding `work_packages.csv`
- Write permission on the output directory

No services need to be running. This is a batch task on the command line, and the command line is the whole interface — there is no console screen, no F-key slot, and nothing to click.

One prerequisite is not configurable and will surprise you: **the output directory is a hard-coded absolute path with no environment-variable override.** The run creates it and fails outright if it cannot. The *input* data directory is redirectable; the output is not. That asymmetry is the reverse of the sibling accounting tool's, and it is a real gap rather than a design position.

## Purpose

Produce the Payroll Register (by Division) — a single working schedule of budgeted labour hours and crew size, one row per construction division, as HTML and PDF.

Read the next paragraph before running anything, because the report's name promises considerably more than the report delivers.

**This command computes no pay.** It does not calculate gross pay, net pay, or any deduction. It does not determine a pay frequency, a pay date, or a remittance schedule. It does not read a timecard — the hours it aggregates are *budgeted* hours from work-package estimates, not hours anyone worked. It has no concept of an employee: its rows are divisions, and the crew size beside each one is a planning assumption, not a headcount. The columns headed *Pay Freq.* and *Gross Pay* exist on the page and every cell in both of them is an em dash.

That is deliberate, and the document says so on its own face. The gross-to-net computation and the pay-frequency data model are both explicitly undesigned at this stage, and the renderer prints a dash rather than a fabricated number. What the register is genuinely useful for is what its two populated columns say: how many budgeted labour hours each division carries, and what crew size the plan assumes for it.

For the design this report is a first slice of, see [[tool-payroll]]. For the tool the hours come from, see [[tool-construction]].

## Procedure

### 1. Point the tool at the construction data directory

```bash
export TCO26_DATA_DIR=/data/construction/example-project
```

This is the same variable the construction reporting binary uses, and it behaves the same way: unset, the binary falls back to a hard-coded absolute path belonging to the deployment it was first built for, and the run fails on a file read naming a directory you have never heard of.

### 2. Confirm the four inputs

The run reads four CSV files from three different places. Two arrive with the checkout, one comes from the directory you just exported, and one lives in the payroll crate's own data directory.

| File | Where it comes from | What is read from it |
|---|---|---|
| `division_crosswalk.csv` | The construction crate's tracked reference data | Cost-code prefix and division name |
| `crew_assumptions.csv` | The construction crate's tracked reference data | Division name and crew size |
| `work_packages.csv` | `TCO26_DATA_DIR` | Cost code and budgeted labour hours |
| `wage_payment_rules.csv` | The payroll crate's own tracked reference data | The jurisdiction row printed in the note |

`division_crosswalk.csv`:

```
uniformat_prefix,csi_division,division_name
```

`crew_assumptions.csv`:

```
csi_division,division_name,crew_size,hours_per_day
```

`wage_payment_rules.csv`:

```
jurisdiction_code,max_pay_period_days,max_days_to_pay_after_period_end,day_counting,remitting_authority,comp_authority,source_ref,effective_from
```

From `work_packages.csv` — a wider file the construction tool owns — this run reads exactly two fields: `cost_code` and `labor_hours_budget`. Everything else in the row is ignored.

Three details are worth knowing before a first run:

- **`hours_per_day` is loaded and never used.** The crew-assumptions loader parses it into memory; this report consumes only `crew_size`. It is not a column you need to get right for this task.
- **A cost code joins to a division by longest matching prefix.** Each crosswalk row declares a prefix; a work package's cost code is matched against every prefix and the longest match wins. A code matching no prefix at all joins to nothing — see the third verification check below for why that matters more than it sounds.
- **The jurisdiction is compiled in.** There is no flag, no environment variable, and no column anywhere that selects which jurisdiction row is read. One jurisdiction code is a constant in the binary, and only that row is looked up.

### 3. Run the binary

From the workspace root:

```bash
cargo run -p tool-payroll-tco-26
```

That is the complete command. There are no flags, no subcommands, and no positional arguments — the binary does not parse a command line at all, so there is no `--help` to consult, no `--jurisdiction` to override, and no way to render only part of the report. Every configurable thing it has is the one environment variable from step 1.

### 4. Read the console line

A successful run prints exactly one line:

```
[payroll_register] 9 division(s), 4820 total budgeted hour(s) — written to <output directory>
```

The counts are invented for this guide; the shape is real. Both numbers are worth reading rather than skipping — they are the only summary the run produces, and the division count is the first thing that reveals a broken crosswalk.

## Expected outcome

Two files in the compiled-in output directory, which the run creates if it is absent:

| File | What it is |
|---|---|
| `payroll_register.html` | The register as a web page |
| `payroll_register.pdf` | The same register as a print document |

The document has three parts: a masthead carrying the deployment's own project label, the report title, and the division count; a *Basis of preparation* note; and one table.

The table has five columns — Division, Crew Size, Budgeted Hours, Pay Freq., Gross Pay — and repeats its header across pages. Two of those five are populated. The register is typeset as a working document rather than as a filed statement, which is the correct classification for a schedule of budgeted figures.

The *Basis of preparation* note states in the document itself that crew size and budgeted hours are real and sourced from the construction tool's work-package data, that pay frequency and gross pay are not shown because neither has been designed, and that no timecard or payroll transaction has ever been recorded for the project. A second paragraph, present only when the jurisdiction row is found, states that jurisdiction's wage-payment ceiling in days, whether those days are counted as calendar or working days, which authority administers remittance, which administers workers'-compensation reporting, and the citation behind all of it.

That second paragraph is a *statement of the rule*, not an application of it. Nothing in this run computes a pay date, and nothing checks one against the ceiling.

## Verification

**Check the division count against the crosswalk.** The number in the console line is how many distinct divisions received at least one matched work package. If it is lower than the number of divisions you expect to see work in, the crosswalk is not matching what you think it is.

**Check the total against the table.** The total budgeted hours in the console line is the sum of the Budgeted Hours column. It should also agree with the man-hours figure the sibling construction status report produces from the same work-package data — the join and aggregation here deliberately mirror that report's own logic so the two can never quietly disagree about the same underlying numbers. If they differ, one of the two has drifted, and that is a finding worth chasing.

**Sum `labor_hours_budget` yourself and compare.** This check is not optional, and it is the only way to catch the report's one silent failure. A work-package row whose cost code matches no crosswalk prefix, or whose `labor_hours_budget` is blank or does not parse as a number, is dropped from the aggregation with no warning, no counter, and no mention anywhere in the console line or the rendered document. The register will look complete. Add up the column in your source file: if your total is higher than the console line's, the difference is dropped rows, not an arithmetic error.

**Read the em dashes as two different facts.** A dash under Pay Freq. or Gross Pay means the platform does not compute that quantity at all. A dash under Crew Size means something narrower and more actionable: no row in `crew_assumptions.csv` has a division name matching that division. The renderer refuses to print `0` there, precisely so a missing assumption cannot be mistaken for a crew of nobody.

**Confirm the jurisdiction paragraph is present.** If the *Basis of preparation* note ends after its first paragraph, the jurisdiction lookup found nothing and the document has silently lost its entire regulatory disclosure. See the edge cases below.

## What this task does not do

- **It does not compute gross pay.** No wage rate is read from anywhere. The column is structural.
- **It does not compute net pay or any deduction.** Gross-to-net computation — tax brackets, statutory deduction formulas — is explicitly out of scope for this build and is not partially implemented.
- **It does not determine a pay frequency.** No field carrying a per-crew or per-employee pay frequency has a home in any schema this run reads, which is why the column is a dash rather than a default.
- **It does not compute or enforce a pay date.** The jurisdiction's wage-payment ceiling is printed as text in a note. Nothing derives a pay date, and nothing checks one against that ceiling.
- **It does not remit anything, or compute a remittance schedule.** Remitting and workers'-compensation authorities are named in the note as facts about the jurisdiction. No schedule is calculated.
- **It does not read timecards.** Every hour in this report is a budgeted estimate attached to a work package. No hour anyone actually worked appears anywhere.
- **It is not per-employee.** There is no employee record, no roster, and no name in this pipeline at any point. Rows are divisions.
- **It does not select a jurisdiction.** One jurisdiction code is a compile-time constant; an operator in another jurisdiction currently needs a code change, not a configuration change.
- **It writes no ledger entries.** The run reads four files and writes two.

## Edge cases

- **Any missing input file** aborts the run with `read <path>: <error>` and a non-zero exit. Nothing is written. The message is a raw panic rather than a formatted error — it names the path, which is the part you need.
- **A short row in either reference file** aborts the run the same abrupt way. Both reference loaders index fixed column positions, so a row with fewer fields than expected is an index failure, not a skipped line.
- **A comma inside a division name will break the crosswalk.** The work-package reader handles quoted fields; the two reference loaders split on plain commas and do not. A division name containing a comma silently shifts every field after it.
- **An unrecognised `day_counting` value** in the jurisdiction table aborts the run naming the offending value. Only two spellings are accepted.
- **No row for the compiled-in jurisdiction is not an error.** The run succeeds, the two files are written, and the *Basis of preparation* note simply omits its jurisdiction paragraph. This is the most dangerous failure in the tool, because the document looks finished and has quietly dropped its entire regulatory disclosure. Check for the paragraph rather than assuming it.
- **Divisions are ordered alphabetically by name**, not by division number. If you expect a numeric ordering, the report is not wrong — it is sorted on the other key.
- **Output files are overwritten in place.** No versioning, no timestamped directory, no prompt, and no environment variable to send them elsewhere. Copy anything you need to keep before re-running.

## Rollback

Nothing to undo in the source data: the run reads four files and never writes to any of them. Its only writes are `payroll_register.html` and `payroll_register.pdf`. Delete them, or re-run to replace them.

## Next steps

- [[generate-a-construction-cost-estimate]] — the report that produces the work-package data this register aggregates
- [[generate-a-financial-statement-package]] — the sibling accounting task on the same shared renderer
- [[install-toolchain]] — if `cargo run` is not yet available on your machine

## See also

- [[tool-payroll]] — the pay-cadence, remittance, and jurisdiction design this register is a first slice of, including everything it does not yet compute
- [[tool-construction]] — the ledger whose work-package data feeds this report one way
- [[tool-accounting]] — the destination the computed payroll dollars are designed to land in, once they exist
- [[financial-and-construction-tools-overview]] — where this tool sits among the financial and construction tools
