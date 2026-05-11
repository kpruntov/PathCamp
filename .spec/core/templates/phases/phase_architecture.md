# Phase 3: System Architecture

## Objective
Design the technical solution to meet the Requirements. This is the "How".

## Artifacts to Create/Update
*   `05_design/lcomp_*.json`: Logical Components.
*   `05_design/pcomp_*.json`: Physical Components.
*   `05_design/api_*.json`: API Contracts (OpenAPI/Interface definitions).
*   `05_design/data_*.json`: Data Models (Schema definitions).
*   `05_design/adr_*.json`: Architecture Decision Records.

## Protocol
1.  **High-Level Design:** Create `LCOMP-XXX` and `PCOMP-XXX` to define system components and their interactions.
2.  **API Design:** Define `API-XXX` for boundaries between components.
3.  **Data Design:** Define `DATA-XXX` for persistent entities.
4.  **Decision Records:** If multiple options exist (e.g., SQL vs NoSQL), write an `ADR-XXX`.

## Validation
*   Every `API` and `DATA` element must trace to an `FR`.
*   Run `loom validate` to ensure coverage.
