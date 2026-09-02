---
schema: foundry-doc-v1
title: "Generate a financial statement package"
slug: generate-a-financial-statement-package
short_description: "Runs the statements binary for one fiscal year and one period to render a consolidated statement package as HTML and PDF, recomputed from journal CSVs on every run — the tool refuses to render rather than publish a figure that does not tie."
category: how-to
index_group: financial-construction-tools
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-09-01
editor: pointsav-engineering
paired_with: generate-a-financial-statement-package.es.md
research_trail:
  sources: [tool-accounting-pro-01/src/bin/statements.rs (the real argument loop, the Presentation resolver, the three pre-render guards, the output stem and the stdout summary), tool-accounting-pro-01/src/config.rs (every input and output path the run resolves, and the single environment variable that redirects one of them), tool-accounting-pro-01/src/subsequent_events.rs (the periods.csv and event-register reads the statement package makes beyond its journals), tool-accounting-core/src/chart.rs (the 9-column accounts.csv schema and the sign-confirmation gate), tool-accounting-core/src/journal.rs (the 17-column journal schema and the per-account file discovery pattern), tool-accounting-core/src/periods_registry.rs (the 6-column periods.csv schema), tool-accounting-core/src/money.rs (exact-integer parsing, the two-decimal refusal, and the whole-dollar display format the console summary uses), tool-accounting-pro-01/Cargo.toml and tool-accounting-core/Cargo.toml (the real bin layout and the deliberate zero-dependency posture)]
  verification_method: "read the Rust source directly rather than a design document's description of it; the flag set was taken from the binary's own argument loop and its USAGE constant rather than from a --help transcript, and confirmed to be the complete set (four accepted tokens, everything else rejected by name); the input schemas are the loaders' own header constants, which are compared for exact equality at load time, not a schema table that could have drifted from them; the three refusal conditions are the source's own early returns, quoted by behaviour rather than by message; a stale module comment claiming two of the four periods are refused rather than rendered was checked against the resolver and found to be out of date, so this guide documents the code; every figure, entity code, path and year in the examples below is invented, because the real deployment's data is private financial content and none of it belongs in a public guide"
---

## Prerequisites

- A working Rust toolchain (see [[install-toolchain]])
- A checkout of the three accounting crates — the engine library, this deployment's binary crate, and the shared renderer
- Read access to the accounting data repository the binary crate resolves at startup
- Write permission on the output directory, or `ACCOUNTING_OUTPUT_DIR` set to somewhere you can write

No services need to be running. All three crates declare zero third-party dependencies, deliberately, so a first build compiles the workspace's own code and downloads nothing.

One prerequisite cannot be satisfied by configuration, and it is worth knowing before the first run: **the input data repository's location is compiled into the binary as an absolute path.** There is no `--data-dir`, no positional argument, and no environment variable that moves it. A checkout whose data repository sits somewhere else fails at the first file read, naming a directory that is not yours. Only the *output* location is redirectable.

## Purpose

Render one entity's consolidated financial statement package — Statement of Financial Position, Statement of Income (Loss), Statement of Changes in Unitholders' Equity, Statement of Cash Flows, and the Notes — as HTML and PDF, for one fiscal year and one period.

Nothing in the package is stored between runs. Every figure is recomputed from the journal CSVs each time: journals fold into per-account ledgers, ledgers fold into a trial balance, the trial balance consolidates across the group, and the consolidated lines are picked up by the statement layout. A rendered statement is a view of the journals as they stand at that moment, not a saved report that can drift from them.

For the ledger design underneath, see [[tool-accounting]].

## Procedure

### 1. Work from the binary crate's own directory

```bash
cd <checkout>/tool-accounting-pro-01
```

These crates are not a Cargo workspace. They are three sibling packages joined by path dependencies, each with its own lockfile — a deliberate choice, since the crate holding real financial data is meant to be handed to a reviewer in isolation. There is no workspace root to run `cargo run -p` from, which is the one thing an engineer arriving from [[generate-a-construction-cost-estimate]] will reach for and not find.

### 2. Confirm the inputs

The run reads six things. Four are master files at the root of the data repository, one is a directory of journals, and one is an event register.

| Input | What it carries |
|---|---|
| `accounts.csv` | The chart of accounts, one row per entity-and-account |
| `entities.csv` | The entity registry — legal name, and the rest of each entity's standing facts |
| `consolidation.csv` | Which entities consolidate into the reporting entity, and from when |
| `periods.csv` | Period end and completion date per entity, fiscal year, and period |
| `journals/<year>/*.csv` | Every posted transaction for that fiscal year |
| `register/<year>/events.csv` | The disclosable-event register the subsequent-events note derives from |

Three of these have schemas the loaders check for exact equality against their own header constants — a file whose columns have drifted is refused with both the found and the wanted header printed, rather than parsed on a best-effort basis.

`accounts.csv`, nine columns:

```
entity_code,account_code,ledger_account,statement,periods,sign,posting_tag,sourced,notes
```

`periods.csv`, six columns:

```
entity,fiscal_year,period,period_end_date,completion_date,lock_status
```

Each journal file, seventeen columns:

```
entity_code,account_code,fiscal_year,period,txn_date,counterparty_type,counterparty_id,description,ref_no,ref_source,subtotal_cad,gst_number,gst_amount,currency_code,amount_foreign,amount_cad,invoice_number
```

Two of these fields behave less simply than their names suggest:

- **`sign`** in the chart of accounts takes `+1`, `-1`, `TBD`, or blank. `TBD` and blank are not defaults — they mean the account's sign convention has not been confirmed, and every such account is excluded from every computed figure in the package and reported by name in the run's own summary. An unconfirmed sign is a visible gap, never a guess.
- **`period`** on a journal row is always a disjoint quarter. Year-to-date is a property of the *statement*, assembled by summing quarters at report time; it is never a value a journal row is allowed to carry.

Journal files are discovered by filename prefix — `<entity>_<account>_<year>_<quarter>_*.csv` — and the quarter in the filename is what decides whether a file is in scope for the period being rendered. The filename duplicates what is inside the file on purpose, so the two can be cross-checked.

### 3. Choose a year and a period

```bash
cargo run --bin statements -- --year 2024 --period Q1
```

The complete flag set is `--year YYYY`, `--period Q1|Q2|Q3|YE`, and `-h`/`--help`. Anything else is rejected by name with the usage line. The period argument is trimmed and upper-cased, so `q1` works. The `--` separator is required: without it, cargo consumes the flags itself.

All four periods render. `YE` is the annual package with a single money column. `Q1` is a condensed interim package with two — the current quarter beside a prior-year comparative. `Q2` and `Q3` are condensed interim packages whose flow statements carry four money columns: a discrete three-month window and the year-to-date span, each beside its own comparative. The discrete window is a second, complete pass of the same pipeline, not a subtraction of one cumulative figure from another, and it is subjected to the same guards described under Verification.

**Pass both flags explicitly.** Each has a default compiled in — the period defaults to the annual package, and the year defaults to whichever fiscal year this deployment was first built for. Relying on either means a command whose output depends on a constant you cannot see from the command line.

### 4. Read the console summary

Unlike the sibling construction reporting binary, which deliberately prints no money to the terminal, this one prints its headline figures. The intent is different: these are the numbers you compare against the rendered PDF to confirm you are looking at the run you just made.

```
EXAMPLE-LP-01 consolidated (EXAMPLE-LP-01 + EXAMPLE-TC-01 + EXAMPLE-TC-02) — FY2024 Q1: 26 account(s) computed, 2 skipped (sign unconfirmed), 3 note-only
  BS: Cash 40,000  |  AP 12,500  |  Deficit (57,500)  |  Total equity (deficit) 27,500  |  Total liabilities and equity 40,000
  IS: Share-based comp 30,000  |  Professional 18,000  |  Advisory 9,000  |  Bank 500  |  Opex 57,500  |  Income (loss) (57,500)
  -> /tmp/statements-scratch/2024/EXAMPLE-LP-01_statements_Q1.html
  -> /tmp/statements-scratch/2024/EXAMPLE-LP-01_statements_Q1.pdf
```

Every figure, entity code and path above is invented for this guide. The *shape* is real: whole dollars, thousands separators, negatives in parentheses, and a nil figure as an en dash — the same convention the rendered statements use, so the terminal and the page can be compared line for line without mental arithmetic.

Read the second and third counts on the first line before anything else. `skipped (sign unconfirmed)` is the number of accounts excluded from every figure in the package. A nonzero count does not invalidate the run — it means the package is knowingly incomplete in a way the document itself discloses.

## Expected outcome

Two files in the output directory, which the run creates if it is absent:

| File | What it is |
|---|---|
| `<entity-code>_statements.html` / `.pdf` | The annual package |
| `<entity-code>_statements_Q1.html` / `.pdf` | An interim package, suffixed with its period key |

The annual document carries no suffix and every interim period does. That asymmetry is not an oversight — the annual document is referenced by that exact path elsewhere, and keeping it stable was the point.

`ACCOUNTING_OUTPUT_DIR` redirects the whole tree to somewhere else, with the fiscal year appended as a subdirectory. Use it. The default output location is inside a shared, version-tracked data repository, and a rendering pass you make to look at a PDF should not dirty a committed artifact or race another process writing the same two paths.

## Verification

Most of the verification is done by the run itself, before anything is written. Three guards stand between a computed population and a rendered page, and each refuses outright rather than rendering with a warning:

**The population must balance, or the imbalance must be attributable.** The computed double-entry population is summed; a nonzero residual means it does not tie. If no account was excluded for an unconfirmed sign, that residual is an arithmetic defect with nothing to attribute it to, and the run refuses. If accounts *were* excluded — each named — then the residual is the measured consequence of an already-disclosed gap, and the run proceeds and discloses it on the face of the statement of financial position. Refusing in that second case would suppress the very document that makes the gap visible.

**Every nonzero computed line must appear somewhere on the layout.** Each statement caption declares which consolidated lines it consumes. Any line carrying real money that no caption ever claims is an orphan, and the run refuses, naming it and its balance. A statement that silently drops a figure is wrong, not merely incomplete.

**The cash flow statement must tie to the computed cash line.** The derived change in cash is compared against the period's own computed Cash balance. A mismatch refuses the render and prints both figures.

So a package that exists has already passed all three. What remains for you:

- **Compare the console summary against the rendered page.** They use the same format for the same reason; a mismatch means you are reading an older PDF.
- **Read the skipped-account names.** They are printed by the consolidation step. Each is a real open item in the chart of accounts, not a tool limitation.
- **Look for `POPULATION DOES NOT BALANCE`** in the console output. It appears only when the disclosed-gap branch above fires, and the same residual appears in the document.
- **Open the PDF.** Comparative columns on an interim package print `n/a`, never a dash — a dash on a filed statement asserts that the line is zero, and the comparative period here is unmeasured rather than zero. If a comparative column shows dashes, something has changed and the distinction has been lost.

## What this task does not do

- **It does not audit, certify, or file anything.** It renders a document. Whether that document is filed, reviewed, or relied on is entirely outside this command.
- **It does not compute opening balances.** Opening positions are not yet sourced, so every balance-sheet figure is activity measured from a zero opening. The rendered document says so in a visible note immediately after the balance-sheet table. The income statement is flow-only and carries no such caveat, because none applies to it. This means the balance sheet is a real template with provisional figures — treat it as one.
- **It does not compute the comparative period.** Comparative columns are rendered because the filed interim statements carry them, and every figure cell in them reads `n/a`. The shape is real; the period behind it is unmeasured.
- **It does not render any other entity's statements.** Sibling binaries in the same crate render the general partner's standalone package and the subsidiary packages. Each takes its own arguments and is a different task.
- **It does not render the management discussion and analysis.** That is a separate binary.
- **It does not print a trial balance or ledger detail.** The crate's default binary does that, and it is worth running when a statement figure surprises you.
- **It writes no journal entries.** Against the data repository this command is strictly read-only. Its only writes are the two output files.

## Edge cases

- **An unrecognized `--period` value** is rejected by name, with the usage line, exit status 1. Nothing is computed.
- **`--year` with a missing or non-numeric value** fails the same way. So does any unrecognized argument — there are no positional arguments to fall through to.
- **A missing `periods.csv` row** for the entity, fiscal year, and period you asked for is a hard error naming `periods.csv`. The subsequent-events window cannot be classified without a period end and a completion date, and the run will not guess them. This is the most common first failure when rendering a period for the first time.
- **A missing event register for the following year is not an error.** The subsequent-events window opens the day after period end, so qualifying events live in the *next* year's register; the run loads it when it exists and proceeds without it when it does not.
- **A header that has drifted** — in the chart of accounts, a journal file, or the period registry — refuses the run and prints the found header beside the wanted one. Repair the file rather than working around it.
- **A row with the wrong field count** is not skipped with a warning. It aborts the run, naming the file and the row number.
- **A money value with more than two decimal places is refused, not rounded.** Sub-cent precision in a CSV is float noise from something upstream, and the error message says so. Quantize at the source.
- **Adding two different currencies is refused.** Conversion is a named, source-cited operation elsewhere; it never happens implicitly inside an addition.
- **Output files are overwritten in place.** No versioning, no timestamped directory, no prompt. Copy anything you need to keep, or point `ACCOUNTING_OUTPUT_DIR` somewhere disposable.

## Rollback

Nothing to undo in the source data: the run reads the master files, the journals, and the register, and never writes to any of them. Its only writes are the two output files. Delete them, or re-run to replace them.

If you rendered into the default location and dirtied a tracked artifact, the fix is the ordinary one for a tracked file — restore it from version control, then re-run with `ACCOUNTING_OUTPUT_DIR` set.

## Next steps

- [[generate-a-construction-cost-estimate]] — the sibling construction ledger's own reporting task, which shares this tool's renderer
- [[generate-a-payroll-register]] — the labour-hours register on the construction side of the same family
- [[export-structured-data]] — moving rendered output or its source records somewhere else

## See also

- [[tool-accounting]] — the double-entry design, the data model, and the audit-readiness posture these statements render
- [[tool-construction]] — the sibling development-and-construction ledger built on the same design
- [[financial-and-construction-tools-overview]] — where this tool sits among the financial and construction tools
