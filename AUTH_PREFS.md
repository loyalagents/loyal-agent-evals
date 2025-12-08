# Agent Authorization & Preferences File v0.1

> **Purpose**: This file defines the specific authorizations granted to the AI Agent and the User's preferences for how tasks should be executed. It is incorporated by reference into CONTRACT.md.

---

## 1. Authorization Identifier

- **Grant ID**: `grant_checkout_001`
- **User ID**: `user:principal_001`
- **Effective Date**: 2025-12-07
- **Expiry Date**: 2026-12-07 (or until revoked)
- **Last Modified**: 2025-12-07

---

## 2. Permitted Actions

The AI Agent is authorized to perform the following actions on behalf of the User:

| Action | Scope | Constraints |
|--------|-------|-------------|
| `search` | Product/service discovery | No restrictions |
| `compare` | Price/feature comparison | Use objective sources |
| `recommend` | Product recommendations | Must disclose conflicts |
| `purchase` | Execute transactions | Subject to monetary limits |
| `confirm` | Confirm transactions | Required for all purchases |

---

## 3. Monetary Limits

| Limit Type | Amount | Notes |
|------------|--------|-------|
| **Per-Transaction Limit** | $200 USD | Purchases exceeding this require explicit User confirmation |
| **Daily Limit** | $500 USD | Aggregate daily spending cap |
| **Monthly Limit** | $2,000 USD | Aggregate monthly spending cap |

### 3.1 Automatic Approval Threshold
- Transactions under **$50** from approved vendors may proceed without real-time confirmation
- Transactions **$50-$200** require confirmation via the AI Agent's response
- Transactions **over $200** require out-of-band confirmation (e.g., separate authorization)

---

## 4. Approved Vendors

The AI Agent may execute transactions with the following pre-approved vendors without additional authorization:

| Vendor | Category | Trust Level |
|--------|----------|-------------|
| Apple | Electronics | High |
| Amazon | General Retail | High |

### 4.1 New Vendor Policy
For vendors not on the approved list:
- The AI Agent MUST request User confirmation before executing any transaction
- The AI Agent MUST disclose any additional risks (e.g., unknown return policy)

---

## 5. Exclusions

The AI Agent is explicitly **NOT authorized** to:

| Excluded Action | Reason |
|-----------------|--------|
| Subscriptions with auto-renew | Risk of recurring charges without periodic review |
| Digital goods (gift cards, software licenses) | Higher fraud risk, non-refundable nature |
| Business expenses | Outside scope of personal purchasing authorization |
| Financial instruments | Requires separate fiduciary authorization |
| Medical/health purchases | Requires specific authorization |
| Legal services | Requires specific authorization |

---

## 6. Data Access Permissions

| Data Category | Access Level | Purpose |
|---------------|--------------|---------|
| `preferences.payments` | On-demand | Process authorized purchases |
| `preferences.shipping` | On-demand | Complete delivery details |
| `preferences.style` | Read-only | Inform recommendations (if requested) |
| `purchase_history` | Denied | Privacy protection |
| `browsing_history` | Denied | Privacy protection |
| `contacts` | Denied | Not relevant to purchasing |

### 6.1 Data Minimization Principle
The AI Agent shall access only the minimum data necessary for the immediate task. Data access must be:
- **Purpose-bound**: Only for the authorized action
- **On-demand**: Accessed at time of need, not pre-fetched
- **Logged**: All access recorded in audit trail

---

## 7. User Preferences

The following preferences guide the AI Agent's decision-making when multiple options exist:

### 7.1 Product Preferences
| Preference | Priority | Notes |
|------------|----------|-------|
| Recyclable/sustainable materials | High | Prefer when available at similar price |
| "Made in USA" labeling | Medium | Prefer when available |
| Energy-efficient options | Medium | For applicable products |
| Warranty included | Low | Nice to have, not required |

### 7.2 Vendor Preferences
| Preference | Priority | Notes |
|------------|----------|-------|
| Free shipping | High | Prefer vendors offering free shipping |
| Easy returns | High | Prefer 30+ day return policies |
| Price match guarantees | Low | Nice to have |

### 7.3 Execution Preferences
| Preference | Setting | Notes |
|------------|---------|-------|
| Confirmation style | `always-ask` | Always request confirmation for purchases |
| Speed vs. price | Price | Optimize for price, not speed |
| Notification frequency | `on-action` | Notify on each significant action |

---

## 8. Autonomy Settings

These settings control how independently the AI Agent may act:

| Scenario | Autonomy Level | Behavior |
|----------|----------------|----------|
| **Routine purchases under $50** | `auto-ok` | May proceed, notify after |
| **Purchases $50-$200** | `ask-first` | Must request confirmation |
| **Purchases over $200** | `require-auth` | Requires separate authorization |
| **New vendor transactions** | `ask-first` | Must request confirmation |
| **Ambiguous instructions** | `clarify` | Must ask for clarification |
| **Detected anomalies** | `halt-and-ask` | Must pause and explain |

---

## 9. Conflict of Interest Disclosure Requirements

If the AI Agent or Provider has any of the following relationships with a vendor, it MUST be disclosed:

| Relationship Type | Disclosure Required |
|-------------------|---------------------|
| Affiliate commission | Yes - Amount/percentage |
| Referral partnership | Yes - Nature of partnership |
| Vendor ownership stake | Yes - Conflict must be flagged |
| Exclusive dealing agreement | Yes - Must offer alternatives |
| Advertising relationship | Yes - Sponsored content flagged |

---

## 10. Revocation

The User may revoke any authorization in this file at any time by:
1. Updating this file to remove the authorization
2. Sending a revocation request to the AI Agent Provider
3. Using the emergency revocation mechanism (if available)

Upon revocation, the Provider must terminate the relevant access within **60 seconds**.

---

## 11. Versioning

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2025-12-07 | Initial draft based on AP2 Intent Mandate concepts |

---

*This authorization file is incorporated by reference into CONTRACT.md v0.2.*
