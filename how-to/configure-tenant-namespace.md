---
schema: foundry-doc-v1
title: "How to configure a tenant namespace"
slug: configure-tenant-namespace
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: configure-tenant-namespace.es.md
---

A tenant namespace is the isolated partition within the platform that holds a single customer's resources — fleet nodes, sessions, audit records, and capability tokens. Configuring a tenant namespace means registering the tenant with the service layer, defining quota limits, and verifying that isolation is enforced. This guide covers initial namespace configuration for a single tenant.

For the service that enforces tenant isolation, see [[service-vm-tenant]]. For the fleet architecture that namespaces span, see [[ppn-small-business-compute]].

## Prerequisites

- Administrator access to `service-vm-tenant` (the tenant proxy service, port 9221)
- A tenant ID: a stable, lowercase ASCII string that identifies the customer (e.g., `acme-corp`)
- Quota values agreed with the tenant: maximum concurrent VMs, storage quota, API request rate

## Step 1: Register the tenant

Create the tenant record by posting to the tenant service:

```
curl -X POST http://127.0.0.1:9221/v1/tenants \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "acme-corp",
    "display_name": "Acme Corporation",
    "max_vms": 10,
    "storage_quota_gb": 100,
    "api_rate_limit_rpm": 600
  }'
```

A successful response returns the tenant record with a `created_at` timestamp. The tenant ID is immutable after creation — choose it carefully. The WORM ledger records the creation event automatically.

## Step 2: Issue the tenant's root capability token

After the namespace exists, issue a root capability token for the tenant's first administrator session. This token uses scope `service:tenant-admin` and is scoped to the new `tenant_id`:

```
curl -X POST http://127.0.0.1:9221/v1/tenants/acme-corp/tokens \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<tenant-admin-pubkey>",
    "scope": "service:tenant-admin",
    "expires_in_seconds": 86400
  }'
```

Deliver this token to the tenant's designated administrator. They use it to issue sub-tokens and enroll their own devices.

## Step 3: Verify namespace isolation

Confirm the tenant namespace is isolated from other tenants by querying the fleet under the new tenant's credentials:

```
curl -s "http://127.0.0.1:9221/v1/vms" \
  -H "Authorization: Bearer <tenant-admin-token>"
```

The response must contain only VMs belonging to `acme-corp`. If VMs from other tenants appear, namespace enforcement has a defect — do not proceed; review the `service-vm-tenant` configuration.

## Step 4: Verify quota enforcement

Submit a request that would exceed the configured quota to confirm enforcement is active. For example, if `max_vms` is 10, attempt to register an 11th VM. The service must return a `429 Too Many Requests` response with a quota-exceeded error body.

Quota enforcement failure is a billing and fairness defect — resolve it before the tenant begins production use.

## Step 5: Confirm the WORM ledger entry

The tenant creation event is permanently recorded. Verify the entry exists:

```
service-fs read --filter tenant-id=acme-corp --event-type TENANT_CREATED --limit 1
```

The entry confirms when the namespace was created and under which administrator token. This record cannot be altered.

## Key takeaways

- Tenant IDs are immutable after creation — choose descriptive, stable identifiers
- Every tenant namespace has independent quota limits; configure them before the tenant starts enrolling nodes
- Namespace isolation must be verified before handing off credentials to the tenant
- A WORM ledger entry is created for every namespace lifecycle event (creation, quota change, deletion)

## See also

- [[service-vm-tenant]] — the tenant proxy service that enforces namespace boundaries
- [[ppn-small-business-compute]] — the compute fleet architecture that tenant namespaces partition
- [[issue-capability-token]] — how to issue capability tokens once the namespace exists
- [[scale-user-tiers]] — adjusting per-user access tiers within an established namespace
- [[add-a-fleet-node]] — enrolling the tenant's first compute node after namespace setup
