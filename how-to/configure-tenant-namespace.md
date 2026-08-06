---
schema: foundry-doc-v1
title: "Configure a tenant namespace"
slug: configure-tenant-namespace
short_description: "Configures a tenant namespace on service-vm-tenant via environment variables and a restart — the real config-driven mechanism, since no runtime tenant-registration API exists."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: configure-tenant-namespace.es.md
research_trail:
  sources: [pointsav-monorepo service-vm-tenant/src/main.rs, service-vm-tenant/src/tenant.rs, service-vm-tenant/src/quota.rs, infrastructure/virt/local-vm-tenant.service]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; this guide's own prior Major Correction note (2026-07-18) had already confirmed no /v1/tenants API exists, but flagged the actual provisioning mechanism as needing further investigation before rewriting — this pass completes that investigation"
---

## Prerequisites

- Administrator access to the machine running `service-vm-tenant` (default port 9221)
- A tenant ID: a stable, lowercase ASCII string identifying the customer (e.g., `acme-corp`)
- Quota values agreed with the tenant: maximum concurrent VMs, maximum RAM

## Purpose

Add a tenant namespace to `service-vm-tenant` the way the service actually supports today — editing its environment configuration and restarting it. There is no runtime registration API; provisioning is config-driven.

## Procedure

1. Add the tenant to the allowlist. `TENANT_IDS` is a bare comma-separated list of tenant IDs — it carries no quota data itself:

   ```
   TENANT_IDS=acme-corp,existing-tenant
   ```

2. Set the new tenant's quotas as separate, per-tenant environment variables, named by uppercasing the tenant ID:

   ```
   TENANT_ACME_CORP_MAX_VMS=10
   TENANT_ACME_CORP_MAX_RAM_MB=16384
   ```

   Both are optional — if omitted, they default to 5 VMs and 8192 MB.

3. Set an authentication token for the tenant. `service-vm-tenant` uses a plain Bearer token, not a signed capability token:

   ```
   TOKEN_MAP=<a-generated-token>:acme-corp
   ```

   > **Warning:** if `TOKEN_MAP` is left unset entirely, the service falls back to an explicitly-logged **insecure mode** where the bearer token literally *is* the tenant ID (`Authorization: Bearer acme-corp` authenticates as that tenant, no secret required). Set `TOKEN_MAP` for anything beyond local testing.

4. Restart `service-vm-tenant` to load the new configuration. There is no hot-reload, no admin endpoint, and no signal-based config refresh — `TENANT_IDS` and the per-tenant variables are read exactly once, at process startup.

## Expected outcome

`service-vm-tenant` recognizes requests bearing the new tenant's token, scopes every response to that tenant's own VMs automatically, and enforces the quotas you set.

## Verification

Confirm the tenant is recognized and see its current usage in one call:

```bash
curl -s http://127.0.0.1:9221/v1/status \
  -H "Authorization: Bearer <acme-corp-token>"
```

This returns `tenant_id`, `vms_running`, `ram_used_mb`, `max_vms`, and `max_ram_mb` — a real, working quota-usage endpoint.

Confirm isolation by listing VMs — there is no client-supplied tenant filter; the server scopes results to whichever tenant the Bearer token authenticates as:

```bash
curl -s http://127.0.0.1:9221/v1/vms \
  -H "Authorization: Bearer <acme-corp-token>"
```

Confirm quota enforcement by attempting to exceed `max_vms` or `max_ram_mb` via `POST /v1/vms`. Both limits are enforced synchronously, before the request reaches the fleet controller, and return `429 Too Many Requests` with a plain-text body describing the limit.

## Rollback

Remove the tenant's ID from `TENANT_IDS` (and its `TOKEN_MAP` entry, if set) and restart the service. Existing VMs the tenant owns are not automatically destroyed — deallocate them explicitly first via `DELETE /v1/vms/:vm_id` if that's the intent, since a removed tenant simply loses the ability to authenticate, not its running resources.

## Next steps

- [[issue-capability-token]] — a related but distinct credential system, for service-to-service authentication rather than tenant-scoped VM access
- [[add-a-fleet-node]] — add compute capacity for tenants to place VMs on

## See also

- [[service-vm-tenant]] — the tenant proxy service that enforces namespace boundaries
- [[ppn-small-business-compute]] — the compute fleet architecture that tenant namespaces partition
- [[scale-user-tiers]] — a separate, unrelated access-tier system for individual users within an archive
