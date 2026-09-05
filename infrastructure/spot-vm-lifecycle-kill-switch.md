---
schema: foundry-doc-v1
title: "Spot VM lifecycle — single controller and kill switch pattern"
slug: spot-vm-lifecycle-kill-switch
short_description: "Single-controller lifecycle for the Yo-Yo spot VM — why one timer owns both start and stop, plus the sentinel-file kill switch for immediate operator override."
category: infrastructure
index_group: compute-and-vm-fabric
type: topic
content_type: topic
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-07-18
editor: pointsav-engineering
paired_with: spot-vm-lifecycle-kill-switch.es.md
---

When an automated pipeline depends on a preemptible or spot VM, the lifecycle of that VM
must be owned by a single controller. Two independent timers that each hold the authority
to start the VM will eventually fire at the same time, leaving the VM running between
cycles at full cost with no automated stop path. This document describes the single-controller
architecture used for the [[yoyo-compute-substrate|Yo-Yo batch node]] and the sentinel file kill switch that provides
immediate operator control.

## The two-timer problem

The Yo-Yo batch pipeline initially had two timers operating independently:

- a **daily-cycle timer**, which ran the [[yoyo-daily-enrichment-cycle|daily enrichment cycle]] and both started and stopped the VM
- a **corpus-threshold timer**, which checked the training corpus on its own schedule and started the VM if a threshold was exceeded

Both timers could start the VM. Only the daily-cycle timer stopped it. When the
corpus-threshold timer fired on its own, it could start the VM but had no path to stop it.
If the daily cycle did not fire shortly afterward, the VM would remain running indefinitely.

An uncapped start event from the threshold timer meant real, unbudgeted cost accrual for
every hour the VM ran beyond its intended window — and if the daily cycle was itself
skipped (a holiday, or a kill switch left active), the VM could run for a full day or more
before anything stopped it.

## The single-controller fix

The fix is architectural: exactly one scheduled unit owns the full VM lifecycle for each
VM. All VM lifecycle operations — start, data extraction, corpus-threshold check,
training, stop — are now performed within a single invocation of one orchestrator script,
triggered once daily. A separate weekly trigger for the training step still exists as an
installable unit in the repository, but its own cadence is superseded by the orchestrator's
own training phase, which already runs every night — it reads as leftover documentation for
the scheme this single-controller design replaced, not a second live start path.

The daily orchestrator runs two mandatory phases every night: a data-extraction phase, then
a training phase run against the corpus-threshold check. Both run while the VM is already
up, adding no additional start cost beyond the one nightly boot.

The rule generalises: for any spot VM that performs multiple automated tasks, consolidate
all tasks into a single orchestrator script invoked by a single timer. Do not give
multiple timers start authority over the same VM.

## The sentinel file kill switch

A kill switch is a file whose presence or absence controls whether an automated process
runs. The pattern is:

```
presence of /path/to/flag-file  →  suppress the operation
absence of /path/to/flag-file   →  normal operation
```

For the Yo-Yo batch node, the kill switch is a single sentinel file at a fixed,
reboot-durable path.

The daily cycle script checks for this file as its first action (Phase 0), before issuing
any VM-lifecycle commands:

```bash
if [[ -e "$KILL_SWITCH" ]]; then
    log "KILL SWITCH ACTIVE — $KILL_SWITCH present; aborting all VM lifecycle"
    exit 0
fi
```

Creating the file is a one-command action that takes effect on the next timer firing:

```bash
touch "$KILL_SWITCH"
```

Removing the file resumes normal operation:

```bash
rm "$KILL_SWITCH"
```

The pattern is appropriate for any automated process where:
- The operator needs an instant brake that survives a reboot
- The suppression should be persistent across multiple timer firings until explicitly reversed
- No service restart or configuration change should be required to activate or deactivate control

An environment variable (`export SUPPRESS=true`) would not survive a reboot or a service
restart. A systemd unit mask requires root and a `daemon-reload`. The sentinel file
approach is reversible, auditable (its presence or absence is visible with `ls`), and
requires no elevated privileges to activate.

## Defense in depth: the idle monitor

The kill switch prevents starts. A separate safety layer stops a VM that is running when
it should not be. This isn't a standalone timer — it's an in-process background task
inside the Doorman itself, polling every five minutes for whether the Yo-Yo batch VM has
been running for more than 30 minutes without an active inference request. If that
condition is met, the monitor deletes the instance directly (its boot disk survives, since
auto-delete is disabled on it — the VM is re-created, not resumed, on the next nightly run).

The idle monitor is a backstop, not the primary controller. Its role is to bound the cost
exposure if the nightly run fails to complete its stop sequence — for example, if the
controlling host loses connectivity mid-run, or if the run is interrupted by a process
signal before the stop step executes.

The combination of single-controller daily cycle, sentinel file kill switch, and idle
monitor provides three independent layers:

1. The daily cycle stops the VM as its final phase (intended path)
2. The idle monitor stops the VM if the cycle fails (first backstop)
3. The kill switch prevents the VM from starting if the operator needs to pause all
   activity (operator override at Phase 0)

## The threshold-check guard

The corpus-threshold script contains a start-trainer function that was originally called
directly by the corpus-threshold timer. After that timer was masked, this function was
modified to check the kill switch file before issuing any VM-start command. This is a
defense-in-depth measure: if the function is ever called from a code path that bypasses
the daily cycle, the kill switch still takes effect.

The guard pattern:

```python
if os.path.exists(KILL_SWITCH_PATH):
    print(f"[kill switch] {KILL_SWITCH_PATH} present — VM start suppressed")
    return
```

Any script that has the authority to start a spot VM should implement this check.

## Applying the pattern

To apply single-controller + kill switch to any spot VM pipeline:

1. Identify all timers and scripts that hold authority to start the VM.
2. Consolidate all work into a single orchestrator script. The script starts the VM,
   performs all tasks in sequence, and stops the VM as its final step.
3. Disable all other start paths (mask the timers; modify any scripts that had start
   authority to check the kill switch file instead).
4. Create the kill switch file path in a directory that survives reboots.
5. Add the kill switch check as the first statement in the orchestrator script.
6. Add an idle monitor as a cost backstop, targeting the specific VM name and zone.
