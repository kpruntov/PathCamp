# Phase 2: Requirement Specification

## Objective
Detail the functional and non-functional requirements based on the Context. This is the "What".

## Artifacts to Create/Update
*   `03_users/uch_*.json`: User Characteristics (Personas).
*   `03_users/ur_*.json`: User Requirements (User Stories).
*   `04_system/fr_*.json`: Functional Requirements.
*   `04_system/nfr_*.json`: Non-Functional Requirements (Performance, Security).

## Protocol
1.  **Define Users:** Create `UCH-XXX` for each user type derived from Stakeholders.
2.  **Capture User Needs:** Create `UR-XXX` (User Stories) traceable to `UCH-XXX`.
3.  **Derive Functional Reqs:** Create `FR-XXX` traceable to `UR-XXX`. precise inputs, outputs, and behaviors.
4.  **Define Constraints:** Create `NFR-XXX` for performance/security constraints.

## Validation
*   Every `FR` must trace to a `UR`.
*   Every `UR` must trace to a `UCH` or `STK`.
*   Run `loom validate` to check for orphans.
