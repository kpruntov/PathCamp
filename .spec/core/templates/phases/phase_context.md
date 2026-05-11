# Phase 1: Context Definition (Requirements)

## Objective
Define the project scope, key stakeholders, and high-level business rules. This is the "Why" and "Who" before the "What".

## Artifacts to Create/Update
*   `01_context/product_context.json`: Define `product_scope` (in_scope / out_of_scope).
*   `01_context/stk_*.json`: Define Stakeholders (Users, Owners, Operators).
*   `01_context/br_*.json`: Define Business Rules (Legal, Financial, Compliance).

## Protocol
1.  **Read Product Context:** Check if `product_context.json` exists. If not, create it with a clear Mission Statement.
2.  **Identify Stakeholders:** Ask "Who is paying?", "Who is using it?", "Who is maintaining it?". Create `STK-XXX` for each.
3.  **Define Business Rules:** Ask for non-negotiable constraints (GDPR, Budget, Timeline). Create `BR-XXX`.
4.  **Review:** Ensure all stakeholders have a `role` and `interests`.

## Validation
*   Run `loom validate` to ensure no syntax errors.
*   Do NOT proceed to Requirements until Scope is agreed upon.
