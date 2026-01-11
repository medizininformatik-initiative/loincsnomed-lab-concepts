# Stakeholder Landscape and Approval Requirements

**Version:** 1.0
**Date:** 2026-01-11
**Purpose:** Map stakeholders and define approval paths for laboratory LOINC ValueSet publication

---

## Executive Summary

This document defines the stakeholder landscape and approval workflow for publishing laboratory LOINC ValueSets in the MII context.

**Key Stakeholders:**
1. **Internal Medical Staff** - Clinical validation
2. **External Technical Contributors** - Technical review
3. **MIO Working Group** - Standardization alignment
4. **MII Governance** - Project oversight (if applicable)

**Critical Path:** Internal Medical Staff → MIO Working Group → Publication

---

## Table of Contents

1. [Stakeholder Overview](#stakeholder-overview)
2. [Approval Authority Matrix](#approval-authority-matrix)
3. [Approval Workflow](#approval-workflow)
4. [Stakeholder Details](#stakeholder-details)
5. [Decision Escalation Paths](#decision-escalation-paths)
6. [Timeline and Dependencies](#timeline-and-dependencies)

---

## Stakeholder Overview

### Stakeholder Map

```
┌─────────────────────────────────────────────────────────┐
│                    MII Governance                       │
│                  (Project Oversight)                    │
└────────────────────┬────────────────────────────────────┘
                     │ Escalation only
                     ↓
┌─────────────────────────────────────────────────────────┐
│              MIO Working Group                          │
│         (Standardization & Alignment)                   │
│    Approves: Methodology alignment with MIO profiles    │
└────────────────────┬────────────────────────────────────┘
                     │ Sequential approval
                     ↓
┌─────────────────────────────────────────────────────────┐
│           Internal Medical Staff                        │
│         (Clinical Validation - BLOCKING)                │
│   Approves: Selection rules, clinical appropriateness   │
└────────────────────┬────────────────────────────────────┘
                     │ Parallel review
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
┌─────────────────┐    ┌──────────────────────┐
│ Lab Medicine    │    │ Clinical Informatics │
│   Specialist    │    │      Specialist      │
│  (REQUIRED)     │    │     (REQUIRED)       │
└─────────────────┘    └──────────────────────┘
        ↓                         ↓
        └────────────┬────────────┘
                     │ Advisory input
                     ↓
┌─────────────────────────────────────────────────────────┐
│       External Technical Contributors                   │
│           (Technical Review - ADVISORY)                 │
│   Reviews: ECL queries, FHIR ValueSet format, tooling  │
└─────────────────────────────────────────────────────────┘
```

---

## Approval Authority Matrix

| Stakeholder | Approval Authority | Blocking? | Scope | Timeline |
|-------------|-------------------|-----------|-------|----------|
| **Lab Medicine Specialist** | Selection rules clinical appropriateness | **YES** | Focused/Moderate/Comprehensive tier definitions | 30-60 min |
| **Clinical Informatician** | Use case definitions, validation strategy | **YES** | Methodology framework | 30-60 min |
| **Quality Measure Expert** | Quality measure tier (Moderate) | Recommended | Moderate tier criteria only | 15-30 min |
| **External Technical Contributor** | ECL queries, FHIR format | **NO (Advisory)** | Technical implementation | 1-2 hours |
| **MIO Working Group** | Alignment with MIO Lab profiles | **YES** | MIO profile integration | 1-2 weeks |
| **MII Governance** | Project alignment | Only if escalated | Strategic fit | As needed |

### Approval Types

**BLOCKING Approval:**
- Required before proceeding to next stage
- Work stops until approval obtained
- Applies to: Internal Medical Staff, MIO Working Group

**ADVISORY Review:**
- Feedback incorporated but not blocking
- Work can proceed in parallel
- Applies to: External Technical Contributors, Quality Measure Expert (if unavailable)

**ESCALATION Approval:**
- Only required if conflicts arise
- Applies to: MII Governance

---

## Approval Workflow

### Phase 1: Internal Clinical Validation (BLOCKING)

**Objective:** Validate that selection rules are clinically sound

**Approvers:**
1. **Laboratory Medicine Specialist** (REQUIRED)
2. **Clinical Informatician** (REQUIRED)
3. **Quality Measure Expert** (RECOMMENDED)

**What They Approve:**
- Selection rules framework (`selection_rules.yaml`)
- Use case definitions (Focused/Moderate/Comprehensive)
- Inclusion/exclusion criteria for each tier
- Spot-check examples (5-10 ValueSets)

**Review Materials:**
- `APPROVAL_PACKAGE_CLINICIANS.md` (30-minute review)
- `selection_rules.yaml` (reference document)
- Spot-check examples (hemoglobin, creatinine, HbA1c, glucose, PSA)

**Timeline:** 1-2 weeks (allow time for scheduling, review, feedback iteration)

**Success Criteria:**
- [ ] Lab Medicine Specialist signs approval statement
- [ ] Clinical Informatician signs approval statement
- [ ] Quality Measure Expert signs (or provides written feedback if unavailable)
- [ ] No unresolved clinical concerns

**Output:** Signed approval statement (included in `APPROVAL_PACKAGE_CLINICIANS.md`)

---

### Phase 2: External Technical Review (ADVISORY - Parallel)

**Objective:** Technical validation of ECL queries and FHIR implementation

**Reviewers:**
- External technical contributors (SNOMED/LOINC experts)
- FHIR terminology server experts

**What They Review:**
- ECL query patterns and logic
- FHIR ValueSet JSON format and metadata
- Automated tooling and generation scripts
- LOINCSNOMED Edition usage

**Review Materials:**
- `ECL_METHODOLOGY.md`
- `CLINICAL_METHODOLOGY_RATIONALE.md` (technical sections)
- Sample generated ValueSet JSON files
- ECL query generation scripts

**Timeline:** 1-2 weeks (parallel with Phase 1)

**Success Criteria:**
- [ ] ECL queries are valid and optimized
- [ ] FHIR ValueSets conform to specifications
- [ ] Tooling is reproducible and documented

**Output:** Technical review report with recommendations

**Note:** This review is ADVISORY - feedback incorporated where feasible, but not blocking for publication.

---

### Phase 3: MIO Working Group Alignment (BLOCKING)

**Objective:** Ensure alignment with MIO Laboratory Observation profiles

**Approvers:**
- MIO Laboratory Module Working Group
- MIO Terminology Workstream (if separate)

**What They Approve:**
- Integration with MII Laboratory Observation profile
- Terminology binding strength recommendations (preferred vs required)
- Multi-tier ValueSet approach (is it acceptable for MIO profiles?)
- Publication strategy (canonical URLs, versioning)

**Review Materials:**
- `APPROVAL_PACKAGE_CLINICIANS.md` (for context)
- `KBV_MIO_ALIGNMENT.md` (alignment strategy)
- Draft MIO profile snippet showing ValueSet binding
- Publication plan with canonical URLs

**Timeline:** 2-4 weeks (depends on working group meeting schedule)

**Success Criteria:**
- [ ] MIO working group approves multi-tier approach
- [ ] Agreement on binding strength (likely "preferred" with alternatives)
- [ ] Canonical URL namespaces approved
- [ ] Publication timeline aligned with MIO release cycle

**Output:** MIO working group decision documented in meeting minutes

---

### Phase 4: MII Governance Review (ESCALATION ONLY)

**Objective:** Resolve conflicts or strategic alignment questions

**When Required:**
- Internal medical staff and MIO working group disagree
- Strategic questions about publication scope (100 parameters vs fewer)
- Resource allocation decisions
- Timeline conflicts with other MII initiatives

**Approvers:**
- MII Steering Committee
- MII Interoperability Workstream Lead

**Timeline:** As needed (escalation path)

**Success Criteria:**
- [ ] Conflict resolved with documented decision
- [ ] Project can proceed with clear direction

**Output:** Governance decision memo

---

## Stakeholder Details

### 1. Internal Medical Staff

#### 1.1 Laboratory Medicine Specialist

**Role:** Clinical validation of laboratory test selection criteria

**Key Responsibilities:**
- Validate that Focused tier is appropriate for CDS alerts
- Confirm that Moderate tier captures real-world clinical variation
- Verify that Comprehensive tier is suitable for research
- Spot-check 5-10 example ValueSets for clinical appropriateness

**Approval Authority:** **BLOCKING** for clinical validation

**Review Burden:** 30-60 minutes

**Qualifications:**
- Board-certified laboratory medicine specialist
- Experience with clinical laboratory interpretation
- Familiar with German healthcare laboratory practices

**Candidate Pool:**
- MII consortium hospital laboratory directors
- Academic laboratory medicine faculty
- Clinical pathology specialists

**Recruitment Strategy:**
- Identify through MII consortium contacts
- Approach laboratory directors at Charité, Heidelberg, Munich
- Offer co-authorship on methodology paper as incentive

---

#### 1.2 Clinical Informatician

**Role:** Validate use case definitions and methodology framework

**Key Responsibilities:**
- Confirm use case definitions (CDS, quality reporting, research) are appropriate
- Validate validation strategy (reference sets, spot-checks)
- Review ECL approach mappings for clinical alignment
- Assess feasibility for real-world implementation

**Approval Authority:** **BLOCKING** for methodology framework

**Review Burden:** 30-60 minutes

**Qualifications:**
- Clinical informatics specialist
- Experience with CDS implementation or quality measures
- Familiar with FHIR and terminology services

**Candidate Pool:**
- MII consortium clinical informatics leads
- CDS implementation specialists
- Quality measure developers

**Recruitment Strategy:**
- MII core dataset working group members
- Hospital IT/informatics departments
- Co-authorship incentive

---

#### 1.3 Quality Measure Expert (Recommended)

**Role:** Validate Moderate tier for quality reporting use cases

**Key Responsibilities:**
- Review Moderate tier inclusion/exclusion criteria
- Confirm quality measure examples are realistic
- Validate that Moderate tier captures appropriate variation

**Approval Authority:** **ADVISORY** (recommended but not blocking)

**Review Burden:** 15-30 minutes

**Qualifications:**
- Quality measure development experience
- Familiar with German quality reporting requirements
- Understanding of laboratory data in quality metrics

**Candidate Pool:**
- IQTIG (Institute for Quality Assurance and Transparency in Healthcare)
- MII quality measure working group members
- Hospital quality departments

**Recruitment Strategy:**
- MII quality measure initiative contacts
- IQTIG collaboration
- If unavailable, proceed with Lab Medicine + Clinical Informatician only

---

### 2. External Technical Contributors

**Role:** Technical review of ECL queries and FHIR implementation

**Key Responsibilities:**
- Review ECL query patterns for correctness and optimization
- Validate FHIR ValueSet JSON format and metadata
- Test generated ValueSets against FHIR terminology servers
- Suggest technical improvements to tooling

**Approval Authority:** **ADVISORY** (not blocking)

**Review Burden:** 1-2 hours

**Qualifications:**
- SNOMED CT and/or LOINC expertise
- ECL query experience
- FHIR terminology server knowledge

**Candidate Pool:**
- SNOMED International collaborators
- Regenstrief Institute (LOINC) contacts
- HL7 FHIR terminology community
- MII OntoServer technical team

**Recruitment Strategy:**
- Reach out through professional networks
- HL7 Germany terminology working group
- SNOMED CT German edition community
- Academic collaborations

**Note:** Technical review is valuable but not blocking for publication.

---

### 3. MIO Working Group

**Role:** Ensure alignment with MIO Laboratory Observation profiles

**Key Responsibilities:**
- Review multi-tier ValueSet approach for compatibility with MIO profiles
- Approve terminology binding strategy (preferred vs required)
- Coordinate with other MIO modules (if dependencies exist)
- Approve canonical URL namespaces and publication plan

**Approval Authority:** **BLOCKING** for MIO integration

**Review Burden:** 1-2 working group meetings

**Timeline Considerations:**
- Working group meets monthly or bi-monthly
- May need to pre-socialize proposal before formal review
- Allow 2-4 weeks for review cycle

**Success Criteria:**
- Documented approval in MIO working group minutes
- Agreement on binding strength and canonical URLs
- Timeline alignment with MIO release cycle

**Escalation Path:**
- If MIO working group raises concerns, iterate on approach
- If fundamental disagreement, escalate to MII Governance

**Key Contacts:**
- MIO Laboratory Module Lead
- MIO Terminology Workstream Lead (if separate)
- MIO Simplifier/Publication Team

---

### 4. MII Governance (Escalation Only)

**Role:** Strategic oversight and conflict resolution

**When to Engage:**
- Conflict between internal medical staff and MIO working group
- Strategic questions about scope (100 parameters vs focused set)
- Resource allocation decisions (development time, tooling)
- Timeline conflicts with other MII initiatives

**Approval Authority:** **ESCALATION** (only if needed)

**Key Contacts:**
- MII Steering Committee
- MII Interoperability Workstream Lead
- MII Consortium Coordination Office

**Escalation Process:**
1. Document the conflict or strategic question
2. Summarize positions from all stakeholders
3. Prepare recommendation with pros/cons
4. Submit to MII governance via formal channels
5. Present at steering committee meeting if required

**Timeline:** Varies (depends on meeting schedule and urgency)

---

## Decision Escalation Paths

### Scenario 1: Clinical Validation Concerns

**Situation:** Lab Medicine Specialist raises concerns about selection criteria

**Decision Path:**
1. **Iterate on criteria** - Address concerns, update `selection_rules.yaml`
2. **Re-review** - Lab Medicine Specialist reviews updated version
3. **If still unresolved** - Escalate to Clinical Informatician for joint review
4. **If fundamental disagreement** - Escalate to MII Governance with recommendation

**Timeline Impact:** +1-2 weeks per iteration

---

### Scenario 2: MIO Working Group Alignment Issues

**Situation:** MIO working group requests changes to approach (e.g., single tier instead of three)

**Decision Path:**
1. **Understand rationale** - Why is three-tier approach problematic for MIO?
2. **Propose alternative** - Can we offer three tiers as "preferred + 2 alternatives"?
3. **Negotiate** - Find middle ground (e.g., publish all three but profile uses one)
4. **If impasse** - Escalate to MII Governance with:
   - Clinical rationale for three tiers
   - MIO concerns documented
   - Proposed compromise solutions

**Timeline Impact:** +2-4 weeks if escalation needed

---

### Scenario 3: Technical Implementation Challenges

**Situation:** External technical contributor identifies ECL query issues

**Decision Path:**
1. **Assess impact** - Does this affect clinical validity or just optimization?
2. **Fix if critical** - Update ECL queries and re-generate ValueSets
3. **Defer if minor** - Document as known limitation, address in future iteration
4. **Re-review if significant** - Internal medical staff reviews updated examples

**Timeline Impact:** +1 week if re-review needed

---

### Scenario 4: Resource Constraints

**Situation:** Requested to reduce scope from 100 to 50 parameters due to resource limits

**Decision Path:**
1. **Prioritize parameters** - Use MII Top 300 frequency data
2. **Phase approach** - Publish 50 now, 50 later
3. **Document decision** - Why these 50 were prioritized
4. **Get stakeholder buy-in** - Medical staff and MIO working group approve prioritization

**Timeline Impact:** Reduces initial development time, but requires phased publication

---

## Approval Workflow Sequence

### Sequential Approval Path

```
START
  ↓
┌─────────────────────────────────────────────┐
│ Phase 1: Internal Clinical Validation      │
│ - Lab Medicine Specialist (BLOCKING)       │
│ - Clinical Informatician (BLOCKING)        │
│ - Quality Measure Expert (ADVISORY)        │
│ Timeline: 1-2 weeks                         │
└────────────────┬────────────────────────────┘
                 ↓
         [APPROVAL OBTAINED?]
                 ↓ YES
┌─────────────────────────────────────────────┐
│ Phase 2: External Technical Review         │
│ - SNOMED/LOINC experts (ADVISORY)          │
│ - FHIR terminology experts (ADVISORY)      │
│ Timeline: 1-2 weeks (parallel with Phase 1)│
└────────────────┬────────────────────────────┘
                 ↓
      [INCORPORATE FEEDBACK]
                 ↓
┌─────────────────────────────────────────────┐
│ Phase 3: MIO Working Group Alignment       │
│ - MIO Laboratory Module (BLOCKING)         │
│ - MIO Terminology Workstream (BLOCKING)    │
│ Timeline: 2-4 weeks                         │
└────────────────┬────────────────────────────┘
                 ↓
         [APPROVAL OBTAINED?]
                 ↓ YES
┌─────────────────────────────────────────────┐
│ Publication Ready                           │
│ - Generate 100 lab parameter ValueSets     │
│ - Publish to FHIR terminology server       │
│ - Document in MIO profile                  │
└─────────────────────────────────────────────┘
  ↓
END (PUBLISHED)


        [IF NO AT ANY BLOCKING STAGE]
                 ↓
┌─────────────────────────────────────────────┐
│ Iterate or Escalate                         │
│ - Address concerns, update materials        │
│ - Re-review with stakeholders               │
│ - Escalate to MII Governance if needed      │
└─────────────────────────────────────────────┘
```

---

## Timeline and Dependencies

### Critical Path Timeline

**Optimistic (6-8 weeks):**
- Week 1-2: Internal clinical validation
- Week 1-2 (parallel): External technical review
- Week 3-6: MIO working group review (1-2 meetings)
- Week 7: Incorporate feedback, finalize
- Week 8: Generate ValueSets and publish

**Realistic (10-12 weeks):**
- Week 1-3: Internal clinical validation (1 iteration)
- Week 1-3 (parallel): External technical review
- Week 4-8: MIO working group review (pre-socialization + formal review)
- Week 9-10: Address MIO feedback, iterate
- Week 11: Final approval and publication prep
- Week 12: Generate and publish

**Pessimistic (16-20 weeks):**
- Week 1-4: Internal clinical validation (2 iterations)
- Week 5-12: MIO working group review (multiple iterations)
- Week 13-14: Escalation to MII Governance
- Week 15-16: Final approval
- Week 17-20: Generate, test, and publish

---

### Dependencies

**Hard Dependencies (BLOCKING):**
1. Internal Medical Staff approval → **BLOCKS** → MIO Working Group review
2. MIO Working Group approval → **BLOCKS** → Publication

**Soft Dependencies (ADVISORY):**
1. External Technical Review → **INFORMS** → Final ValueSet generation
2. Quality Measure Expert → **INFORMS** → Moderate tier refinement

**Parallel Tracks:**
- Internal Clinical Validation **CAN RUN PARALLEL WITH** External Technical Review
- ValueSet generation tooling development **CAN RUN PARALLEL WITH** Approval process

---

## Approval Checklist

### Pre-Approval Checklist (Before Seeking Approvals)

- [ ] **selection_rules.yaml** finalized and documented
- [ ] **APPROVAL_PACKAGE_CLINICIANS.md** created (30-minute review version)
- [ ] **Spot-check examples** generated for 5-10 parameters
- [ ] **Validation metrics** computed (Interpolar overlap, size checks)
- [ ] **MIO alignment strategy** documented
- [ ] **Reviewers identified** and contacted

---

### Phase 1: Internal Clinical Validation Checklist

- [ ] Lab Medicine Specialist identified and contacted
- [ ] Clinical Informatician identified and contacted
- [ ] Quality Measure Expert identified (or documented as unavailable)
- [ ] Review materials sent (APPROVAL_PACKAGE_CLINICIANS.md)
- [ ] Review meeting scheduled (or async review arranged)
- [ ] **APPROVAL OBTAINED:** Lab Medicine Specialist signature
- [ ] **APPROVAL OBTAINED:** Clinical Informatician signature
- [ ] **FEEDBACK RECEIVED:** Quality Measure Expert (if available)
- [ ] Concerns addressed and documented
- [ ] Final approval statement signed

---

### Phase 2: External Technical Review Checklist

- [ ] External reviewers identified (SNOMED, LOINC, FHIR experts)
- [ ] Technical review materials sent (ECL_METHODOLOGY.md, sample ValueSets)
- [ ] Feedback received and documented
- [ ] Critical issues addressed (if any)
- [ ] Minor improvements documented for future iteration

---

### Phase 3: MIO Working Group Alignment Checklist

- [ ] MIO working group meeting schedule identified
- [ ] Pre-socialization completed (informal discussion with MIO leads)
- [ ] Formal review materials submitted to MIO working group
- [ ] Presentation prepared for MIO working group meeting
- [ ] MIO working group meeting attended
- [ ] **APPROVAL OBTAINED:** MIO working group decision documented
- [ ] Canonical URLs and binding strategy finalized
- [ ] Publication timeline aligned with MIO release cycle

---

### Phase 4: Publication Checklist

- [ ] All blocking approvals obtained
- [ ] Advisory feedback incorporated (where feasible)
- [ ] Generate 100 lab parameter ValueSets (or prioritized subset)
- [ ] Publish to FHIR terminology server
- [ ] Update MIO Laboratory Observation profile with ValueSet references
- [ ] Document publication in MIO release notes
- [ ] Announce to MII consortium and stakeholders

---

## Contact Information

### Internal Medical Staff

**Lab Medicine Specialist:**
- TBD (to be recruited)
- Estimated recruitment: 1 week

**Clinical Informatician:**
- TBD (to be recruited)
- Estimated recruitment: 1 week

**Quality Measure Expert:**
- TBD (to be recruited, if available)
- Estimated recruitment: 2 weeks

---

### External Technical Contributors

**SNOMED CT Expertise:**
- MII OntoServer team
- SNOMED CT German Edition community

**LOINC Expertise:**
- Regenstrief Institute contacts
- Academic LOINC researchers

**FHIR Terminology:**
- HL7 Germany terminology working group
- FHIR terminology server vendors

---

### MIO Working Group

**MIO Laboratory Module:**
- Contact via MII coordination office
- Working group meeting schedule: TBD

**MIO Terminology Workstream:**
- Contact via MII coordination office

---

### MII Governance

**Steering Committee:**
- Contact via MII coordination office
- Escalation process: Formal written request

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-11 | Claude (AI Assistant) | Initial stakeholder landscape and approval workflow |

---

## Related Documents

- **`selection_rules.yaml`** - Selection rules framework requiring approval
- **`APPROVAL_PACKAGE_CLINICIANS.md`** - 30-minute clinical review package
- **`CLINICAL_METHODOLOGY_RATIONALE.md`** - Comprehensive methodology documentation
- **`KBV_MIO_ALIGNMENT.md`** - MIO alignment strategy
- **`HIERARCHICAL_CLUSTERING.md`** - Conceptual framework

---

*This document defines the approval workflow and stakeholder landscape for publishing laboratory LOINC ValueSets. It should be reviewed and updated as stakeholders are identified and approval processes evolve.*
