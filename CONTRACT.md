# Agent Fiduciary Contract v0.2

> **Purpose**: This contract defines the relationship between the User (Principal), the AI Agent Provider, and the AI Agent technology. It establishes the duties, responsibilities, and liabilities of each party.

---

## 1. Parties

### 1.1 User (Principal)
The human who grants authority to the AI Agent Provider to operate an AI Agent on their behalf. The User:
- Defines authorizations and preferences (see AUTH_PREFS.md)
- Provides instructions to the AI Agent
- Bears responsibility for consequences of properly authorized actions
- Retains the right to revoke authority at any time

### 1.2 AI Agent Provider
The legal entity that operates the AI Agent technology as a platform service. The Provider:
- Accepts delegation of authority from the User to conduct transactions
- Operates the AI Agent infrastructure on behalf of the User
- Assumes fiduciary-like duties in the conduct of its platform
- Is the actual legal agent responsible for the AI Agent's actions

### 1.2.1 AI Agent (Technology)
A quasi-autonomous tool or technology service operated by the Provider. The AI Agent:
- Executes transactions and interactions according to User instructions
- Operates within the bounds of User authorizations (AUTH_PREFS.md)
- Acts in accord with User preferences
- Is NOT a separate legal entity but an extension of the Provider's service

---

## 2. Delegation of Authority

### 2.1 Scope of Delegation
The User delegates to the AI Agent Provider the authority to operate an AI Agent that may:
- Conduct transactions on behalf of the User
- Access resources as specified in AUTH_PREFS.md
- Make decisions within authorized parameters
- Interact with third parties as the User's representative

### 2.2 Incorporation by Reference
The specific authorizations, limits, and preferences defined in **AUTH_PREFS.md** are incorporated by reference into this contract and form the binding constraints on the AI Agent's authority.

### 2.3 Revocation
The User may revoke any authorization at any time. The Provider must terminate the revoked access within 60 seconds of receiving the revocation notice.

---

## 3. Provider Duties

The AI Agent Provider assumes the following duties in operating the AI Agent:

### 3.1 Duty to Act (Primary)
The Provider shall ensure the AI Agent carries out the User's instructions faithfully within the scope of authorization. This is the PRIMARY duty—an agent that fails to execute valid instructions has failed its core purpose.

### 3.2 Duty of Loyalty
The Provider shall ensure the AI Agent:
- Does not engage in self-dealing (recommending products that primarily benefit the Provider)
- Discloses any conflicts of interest before proceeding
- Resists third-party influence without User disclosure and consent
- Prioritizes User interests over Provider interests in all decisions

### 3.3 Duty of Care
The Provider shall ensure the AI Agent:
- Uses appropriate competence in executing tasks
- Provides sufficient information for the User to make informed decisions
- Flags ambiguities, anomalies, or risks before irreversible actions
- Does not take actions that a prudent agent would recognize as harmful

### 3.4 Duty of Obedience
The Provider shall ensure the AI Agent:
- Operates strictly within the scope authorized by the User
- Declines requests that exceed authorization and explains why
- Follows User instructions unless doing so would be illegal

### 3.5 Duty of Disclosure
The Provider shall ensure the AI Agent:
- Discloses conflicts of interest before proceeding
- Discloses limitations relevant to the User's decision
- Notifies the User of material developments
- Provides clear evidence trail for all actions

---

## 4. Statutory Duties (Non-Waivable)

Certain duties are imposed by law and cannot be modified by this contract:

### 4.1 UETA §10(b) Compliance
For electronic transactions, the AI Agent Provider MUST ensure the AI Agent provides the User with:
- An opportunity to review the transaction before finality
- A reasonable method to confirm or correct the transaction

If the AI Agent fails to provide this opportunity, the User may repudiate the transaction.

**This duty applies regardless of any other terms in this contract and cannot be waived.**

*Note: The Provider may choose to allow some transactions to proceed without explicit confirmation to increase transaction volume. In such cases, the Provider accepts the risk that the User may exercise their statutory repudiation right, potentially resulting in refunds.*

---

## 5. User Responsibilities

### 5.1 Clear Instructions
The User is responsible for providing clear, unambiguous instructions to the AI Agent.

### 5.2 Accurate Authorizations
The User is responsible for accurately defining authorizations in AUTH_PREFS.md.

### 5.3 Monitoring
The User is responsible for periodically reviewing the AI Agent's actions and revoking authority if the Agent is not performing as expected.

### 5.4 Consequences
The User bears responsibility for the consequences of the AI Agent's actions when those actions are within the authorized scope.

---

## 6. Data Handling

### 6.1 Data Minimization
The AI Agent shall access only the minimum data necessary for the authorized task.

### 6.2 Confidentiality
The Provider shall not use the User's data for purposes other than executing the User's instructions.

### 6.3 No Unauthorized Training
The User's data shall not be used to train foundational models without explicit consent.

---

## 7. Liability

### 7.1 Provider Liability
The Provider is liable for damages caused by:
- AI Agent actions that violate this contract
- AI Agent actions that exceed authorized scope
- Failure to enforce User-defined limits
- Security breaches affecting User data

### 7.2 User Liability
The User is liable for damages caused by:
- AI Agent actions within properly authorized scope
- Instructions that lead to foreseeable harm

### 7.3 Shared Liability
Liability is shared when:
- Ambiguous instructions led to unauthorized interpretation
- Both parties contributed to the harm

---

## 8. Evaluation and Audit

### 8.1 Compliance Measurement
Compliance with this contract is measured through automated evaluation using:
- Deterministic scorers (conflict detection, scope checking)
- LLM-based judges (disclosure quality, reasoning assessment)
- Transaction logs and audit trails

### 8.2 Provider Audit Rights
The Provider must maintain audit logs sufficient to demonstrate compliance with all duties defined in this contract.

---

## 9. Versioning

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2025-12-07 | Initial draft |
| 0.2 | 2025-12-07 | Added two-party structure (User + Provider), delegation framework, AUTH_PREFS.md incorporation, corrected UETA language |

---

*This contract is licensed under CC BY 4.0.*
