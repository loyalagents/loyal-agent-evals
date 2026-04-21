# Dated Terms-of-Service Snapshots

Local HTML copies of every Terms-of-Service, Service Agreement, Acceptable Use Policy, Usage Policy, and Privacy Policy referenced in Appendix G of the Loyal Agent Evals report (`docs/report.md`).

**Download date:** 2026-04-21 (Pacific). All files in this directory were retrieved on that date.

**Why these exist.** Appendix G quotes short excerpts from each of these documents. Terms of Service change without notice. This directory preserves a dated snapshot of each referenced document so any reader can verify the quoted language against the version that was live when the report was authored, independent of whether the canonical URL has drifted since.

**Not legal advice, not a complete ToS archive.** These are research-supporting snapshots. For any operative legal purpose, retrieve the live document from the canonical URL at the time of your use.

## Source method

Two retrieval methods were used:

- **Direct fetch (HTTP 200 from canonical URL):** Used for Anthropic and Google documents. The `.html` file in this directory is the raw response body served by the canonical host on 2026-04-21.
- **Wayback Machine fallback:** Used for OpenAI (`openai.com/policies/*`) and xAI (`x.ai/legal/*`) documents. Direct fetches from those hosts returned HTTP 403 (Cloudflare bot-protection challenge pages). The `.html` file in this directory is the closest Web-Archive snapshot to 2026-04-21 for each URL, fetched via `https://web.archive.org/web/<timestamp>id_/<URL>`. Wayback snapshot timestamps are recorded per-entry below.

This asymmetry matches Appendix G §G.8 (Verification caveats). Any reader independently verifying the quoted clauses should use a standard browser from a residential IP for OpenAI and xAI.

## Archived previous-version xAI consumer Terms

xAI publishes and periodically rotates its consumer Terms of Service. Four dated prior versions are cited in Appendix G §G.5 for historical comparison; the closest Wayback snapshot to each publication date is saved here with a date-stamped filename.

## Document index

Each `DOCUMENT TITLE` below links to the local snapshot in this directory. Canonical URLs and effective dates per the provider's own document header are shown for traceability. Classifications (i)–(iv) refer to Appendix G §2.2 / §G.1's four-posture typology (*express disclaimer* / *implicit risk allocation* / *silence* / *express acceptance*).

---

### Anthropic

1. **Company:** Anthropic, PBC
   **Document title:** [Consumer Terms of Service](./anthropic-consumer-terms.html)
   **Canonical URL:** https://www.anthropic.com/legal/consumer-terms
   **Effective date (per document):** October 8, 2025
   **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
   **Factual description:** Governs both Claude.ai (free) and Claude Pro; Pro-tier subscription provisions live in §6 of the same document. Classification (ii) — implicit risk allocation. No express no-agency / no-partnership / no-fiduciary clause. Contains §4 reliance-and-responsibility language, §11 "AS IS" warranty disclaimer, and §11 liability cap (greater of 6 months of fees or $100). Sector-specific prohibition on using the service for securities or investment advice.

2. **Company:** Anthropic, PBC
   **Document title:** [Usage Policy](./anthropic-usage-policy.html) *(formerly the Acceptable Use Policy)*
   **Canonical URL:** https://www.anthropic.com/legal/aup
   **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
   **Factual description:** Defines permitted and prohibited categories of use for Anthropic's consumer and API services. Not separately excerpted in the report body; listed as a canonical source governing what users may do with Claude.

3. **Company:** Anthropic, PBC
   **Document title:** [Privacy Policy](./anthropic-privacy-policy.html)
   **Canonical URL:** https://www.anthropic.com/legal/privacy
   **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
   **Factual description:** Governs collection, use, and retention of user data across Anthropic consumer services. Not separately excerpted in the report body.

---

### OpenAI

4. **Company:** OpenAI OpCo, LLC
   **Document title:** [Terms of Use — United States (consumer)](./openai-terms-of-use-us.html)
   **Canonical URL:** https://openai.com/policies/terms-of-use/
   **Effective date (per document):** January 1, 2026
   **Download date / source:** 2026-04-21, Wayback Machine snapshot `20260404094138` (direct fetch returned HTTP 403, Cloudflare-challenge page)
   **Factual description:** Governs ChatGPT (free) and ChatGPT Plus for US users. Classification (ii) — implicit risk allocation. Appendix G records a correction in earlier drafts: the "no partnership, joint venture or agency" clause in fact lives in the OpenAI **business** Services Agreement (entry #9 below), **not** in this consumer document. Consumer posture relies on "AS IS" warranty disclaimers, a performance disclaimer, and a sole-risk / not-a-substitute-for-professional-advice clause.

5. **Company:** OpenAI OpCo, LLC
   **Document title:** [Terms of Use — Rest of World (consumer)](./openai-terms-of-use-row.html)
   **Canonical URL:** https://openai.com/policies/row-terms-of-use/
   **Download date / source:** 2026-04-21, Wayback Machine snapshot `20260411215204` (canonical host returned HTTP 403)
   **Factual description:** Non-US, non-EU jurisdiction variant of the consumer Terms of Use. Listed as canonical source; not separately excerpted in the report body.

6. **Company:** OpenAI OpCo, LLC
   **Document title:** [Europe Terms of Use (consumer)](./openai-terms-of-use-eu.html)
   **Canonical URL:** https://openai.com/policies/eu-terms-of-use/
   **Download date / source:** 2026-04-21, Wayback Machine snapshot `20260407214524` (canonical host returned HTTP 403)
   **Factual description:** EU-jurisdiction variant of the consumer Terms of Use. Listed as canonical source; not separately excerpted in the report body.

7. **Company:** OpenAI OpCo, LLC
   **Document title:** [Usage Policies](./openai-usage-policies.html)
   **Canonical URL:** https://openai.com/policies/usage-policies/
   **Download date / source:** 2026-04-21, Wayback Machine snapshot `20260412041905` (canonical host returned HTTP 403)
   **Factual description:** Cross-product acceptable-use rules for all OpenAI services. Listed as canonical source; not separately excerpted in the report body.

8. **Company:** OpenAI OpCo, LLC
   **Document title:** [Policies Hub (index)](./openai-policies-hub.html)
   **Canonical URL:** https://openai.com/policies/
   **Download date / source:** 2026-04-21, Wayback Machine snapshot `20260412141617` (canonical host returned HTTP 403)
   **Factual description:** Index page linking to the full set of OpenAI legal and policy documents. Retained here for provenance of which documents are authoritative for OpenAI at a point in time.

9. **Company:** OpenAI OpCo, LLC
   **Document title:** [Services Agreement (business / API / Enterprise)](./openai-services-agreement.html)
   **Canonical URL:** https://openai.com/policies/services-agreement/
   **Effective date (per document):** January 1, 2026
   **Download date / source:** 2026-04-21, Wayback Machine snapshot `~20260421000000` (canonical host returned HTTP 403)
   **Factual description:** Governs API, ChatGPT Enterprise, ChatGPT Business, and developer/business services. **Expressly does NOT apply to consumer ChatGPT / ChatGPT Plus.** Classification (i) — express disclaimer, cited in the report for contrast. Contains §16.8: *"OpenAI and Customer are not legal partners or agents but are independent contractors."* This is the clause Appendix G corrects as miscategorized into the consumer tier in earlier drafts. ("independent contractors" language confirmed present in this local snapshot.)

10. **Company:** OpenAI OpCo, LLC
    **Document title:** [Service Terms (business)](./openai-service-terms.html)
    **Canonical URL:** https://openai.com/policies/service-terms/
    **Download date / source:** 2026-04-21, Wayback Machine snapshot `~20260421000000` (canonical host returned HTTP 403)
    **Factual description:** Product-specific terms layered on top of the Services Agreement for business customers. Listed as canonical source; not separately excerpted in the report body.

---

### Google

11. **Company:** Google LLC
    **Document title:** [Terms of Service (general)](./google-terms-of-service.html)
    **Canonical URL:** https://policies.google.com/terms
    **Effective date (per document):** May 22, 2024 (AI-related topics incorporated as of this update; the older Generative AI Additional Terms of Service no longer apply to consumer Gemini use)
    **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
    **Factual description:** Governs consumer Gemini (free) and Gemini Advanced (Google One AI Premium). Classification (ii) — implicit risk allocation. No express no-agency / no-fiduciary clause. Contains: "AS IS" warranty disclaimer; prominent professional-advice disclaimer naming medical / legal / financial / other professional advice; user-account responsibility; liability cap (greater of $200 or 12 months of fees).

12. **Company:** Google LLC
    **Document title:** [Gemini Apps Privacy Hub](./gemini-apps-privacy-hub.html)
    **Canonical URL:** https://support.google.com/gemini/answer/13594961
    **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
    **Factual description:** Consumer-facing data-handling and transparency page for Gemini Apps. The report quotes two items from this document: an inaccuracy notice (Gemini Apps "may sometimes produce inaccurate, offensive, or inappropriate information that doesn't represent Google's views") and a confidentiality warning advising users not to enter confidential information they would not want reviewed by human reviewers or used to improve services.

13. **Company:** Google LLC
    **Document title:** [Google One Additional Terms](./google-one-additional-terms.html)
    **Canonical URL:** https://one.google.com/terms-of-service
    **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
    **Factual description:** Governs the paid Gemini Advanced tier (Google One AI Premium) subscription. Layered on the general Google Terms. No substantive duty-allocation delta vs. the free tier — adds only subscription and payment terms.

14. **Company:** Google LLC
    **Document title:** [Generative AI Prohibited Use Policy](./google-genai-prohibited-use.html)
    **Canonical URL:** https://policies.google.com/terms/generative-ai/use-policy
    **Download date / source:** 2026-04-21, direct fetch (HTTP 200)
    **Factual description:** Defines categories of use of Google's generative-AI products that are prohibited (e.g. child sexual abuse material, targeted harassment, unauthorized practice of regulated professions, etc.). Listed as canonical source; not separately excerpted in the report body.

---

### xAI

15. **Company:** X.AI LLC
    **Document title:** [Consumer Terms of Service](./xai-consumer-terms.html)
    **Canonical URL:** https://x.ai/legal/terms-of-service
    **Effective date (per document):** April 10, 2026
    **Download date / source:** 2026-04-21, Wayback Machine snapshot `~20260421000000` (canonical host returned HTTP 403, Cloudflare)
    **Factual description:** Governs both free Grok and SuperGrok (consumer paid tier, approximately $30/mo — a correction over an earlier "$20/mo" figure in the source research). Classification (ii) — implicit risk allocation. No express consumer no-agency / no-partnership / no-fiduciary clause. Contains: output-accuracy disclaimer ("Output may not always be accurate. Output from our services is not professional advice."); "AS IS" framing; user-content ownership with user-responsibility; prohibition on *"taking unauthorized actions on behalf of others"*; prohibition on *"high-stakes automated decisions"* affecting safety / legal / material rights / well-being; liability cap (greater of fees paid or $100); user indemnity.

16. **Company:** X.AI LLC
    **Document title:** [Enterprise Terms of Service](./xai-enterprise-terms.html)
    **Canonical URL:** https://x.ai/legal/terms-of-service-enterprise
    **Download date / source:** 2026-04-21, Wayback Machine snapshot `~20260421000000` (canonical host returned HTTP 403)
    **Factual description:** Governs enterprise xAI customers. **Does NOT govern consumer Grok / SuperGrok.** Classification (i) — express disclaimer, cited in the report for contrast. Contains: *"The parties to this Agreement are independent contractors. There is no relationship of partnership, joint venture, employment, franchise or agency created hereby between the parties."*

17. **Company:** X.AI LLC
    **Document title:** [Acceptable Use Policy](./xai-acceptable-use-policy.html)
    **Canonical URL:** https://x.ai/legal/acceptable-use-policy
    **Download date / source:** 2026-04-21, Wayback Machine snapshot `~20260421000000` (canonical host returned HTTP 403)
    **Factual description:** Prohibited-use categories for xAI products. Listed as canonical source; not separately excerpted in the report body.

18. **Company:** X.AI LLC
    **Document title:** [Privacy Policy](./xai-privacy-policy.html)
    **Canonical URL:** https://x.ai/legal/privacy-policy
    **Download date / source:** 2026-04-21, Wayback Machine snapshot `~20260421000000` (canonical host returned HTTP 403)
    **Factual description:** Governs data handling across xAI products. Listed as canonical source; not separately excerpted in the report body.

#### xAI — Archived prior versions of Consumer Terms of Service

Appendix G §G.5 cites four dated prior versions of xAI's consumer Terms of Service for historical comparison. Each is a Wayback Machine snapshot captured on or near the publication date of that prior version.

19. **Company:** X.AI LLC
    **Document title:** [Consumer Terms of Service — prior version dated January 2, 2025](./xai-consumer-terms-prev-20250102.html)
    **Canonical URL (pattern):** https://x.ai/legal/terms-of-service/previous-* (specific per-version URLs rotate)
    **Download date / source:** 2026-04-21, Wayback Machine snapshot timestamped `2025-01-02`
    **Factual description:** Historical snapshot for ToS-drift tracking. Content captured as served on January 2, 2025.

20. **Company:** X.AI LLC
    **Document title:** [Consumer Terms of Service — prior version dated February 14, 2025](./xai-consumer-terms-prev-20250214.html)
    **Canonical URL (pattern):** https://x.ai/legal/terms-of-service/previous-*
    **Download date / source:** 2026-04-21, Wayback Machine snapshot timestamped `2025-02-14`
    **Factual description:** Historical snapshot for ToS-drift tracking. Content captured as served on February 14, 2025.

21. **Company:** X.AI LLC
    **Document title:** [Consumer Terms of Service — prior version dated April 7, 2025](./xai-consumer-terms-prev-20250407.html)
    **Canonical URL (pattern):** https://x.ai/legal/terms-of-service/previous-*
    **Download date / source:** 2026-04-21, Wayback Machine snapshot timestamped `2025-04-07`
    **Factual description:** Historical snapshot for ToS-drift tracking. Content captured as served on April 7, 2025.

22. **Company:** X.AI LLC
    **Document title:** [Consumer Terms of Service — prior version dated June 9, 2025](./xai-consumer-terms-prev-20250609.html)
    **Canonical URL (pattern):** https://x.ai/legal/terms-of-service/previous-*
    **Download date / source:** 2026-04-21, Wayback Machine snapshot timestamped `2025-06-09`
    **Factual description:** Historical snapshot for ToS-drift tracking. Content captured as served on June 9, 2025.

---

## Verification status

Sanity checks performed against these local snapshots on 2026-04-21:

- `anthropic-consumer-terms.html` contains the expected "AS IS" warranty language.
- `openai-services-agreement.html` contains the expected "independent contractors" clause cited in Appendix G.3 / §16.8.
- All 22 files were retrieved with HTTP 200 status (either direct or via Wayback Machine).

## Limitations

- **Format:** These are raw `.html` documents as served. They include provider site-chrome, JavaScript, and markup. Text-only / reading-friendly extracts are not generated here; open any file in a web browser for the rendered version.
- **Drift:** ToS documents change. The Wayback snapshot dates above capture each document as it was on a specific date; the live canonical URL may now serve different text. Cite the canonical URL and the retrieval date in any downstream use.
- **Not a complete archive:** This directory covers only the documents referenced in Appendix G of the Loyal Agent Evals report. It is not a comprehensive ToS repository.
- **Third-party copies:** Wayback Machine snapshots are third-party archival copies operated by the Internet Archive. Their fidelity depends on what the Wayback crawler captured.

## See also

- Appendix G of `docs/report.md` — the report's own dated summary of the terms referenced here.
- `LICENSES.md` — license matrix for the report, code, and dataset.
