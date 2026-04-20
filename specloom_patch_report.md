# SpecLoom Engine Patch Report (MBSE/Arcadia Support)

The following modifications were necessary in the core `specloom` package to fully support the new Architecture/MBSE schemas (Logical Components, Physical Components, Functional Chains, UI Navigation, and Architecture Views) and fix validation errors.

## 1. `dist/core/domain/SpecNode.js`

**Reasoning:** The `NodeType` enum lacked the new types introduced by the UI and View schemas. Additionally, the standard artifact ID regex (`/^[A-Z]{2,6}-[0-9]{3}$/`) was too restrictive for some custom IDs, though in our case it was mainly an issue with `REF-PRD` which we renamed to `REF-001`. The Regex patch ensures maximum compatibility if alphabetic characters are ever used after the hyphen, though not strictly required if IDs stick to digits.

**Old String:**
```javascript
    NodeType["TEST_SCENARIO"] = "test_scenario";
    NodeType["REFERENCE_SOURCE"] = "reference_source";
})(NodeType || (NodeType = {}));
// ...
    static ID_REGEX = /^[A-Z]{2,6}-[0-9]{3}$/;
// ...
        if (type !== NodeType.IMPLEMENTATION &&
            type !== NodeType.VERIFICATION &&
            type !== NodeType.SYSTEM_REQUIREMENT &&
            !SpecNode.ID_REGEX.test(id)) {
            throw new Error(`Invalid ID format: ${id}. Expected /^[A-Z]{2,6}-[0-9]{3}$/`);
        }
```

**New String:**
```javascript
    NodeType["TEST_SCENARIO"] = "test_scenario";
    NodeType["REFERENCE_SOURCE"] = "reference_source";
    NodeType["UI_NAVIGATION_MAP"] = "ui_navigation_map";
    NodeType["UI_COMPONENT_SPEC"] = "ui_component_spec";
    NodeType["ARCHITECTURE_VIEW"] = "architecture_view";
})(NodeType || (NodeType = {}));
// ...
    static ID_REGEX = /^[A-Z]{2,6}-[A-Z0-9]{3,4}$/;
// ...
        if (type !== NodeType.IMPLEMENTATION &&
            type !== NodeType.VERIFICATION &&
            type !== NodeType.SYSTEM_REQUIREMENT &&
            !SpecNode.ID_REGEX.test(id)) {
            throw new Error(`Invalid ID format: ${id}. Expected /^[A-Z]{2,6}-[A-Z0-9]{3,4}$/`);
        }
```

---

## 2. `dist/core/engine/SpecEngine.js`

**Reasoning:** 
1. **Type Inference:** The `inferTypeFromId` method was silently skipping `NAV-`, `UIC-`, and `VIEW-` artifacts during `loom sync` because it couldn't infer their type. 
2. **Deep Trace Parsing:** The sync engine only looked for traces in a top-level `trace_to` object. The MBSE schemas use nested arrays (e.g., `allocated_functions[].traces_to` in `LCOMP`) and custom fields (e.g., `realizes_logical_components` in `PCOMP`, and a flat `traces_to` in `FCHAIN`). This patch injects custom logic right before the standard `trace_to` extraction to ensure these relationships are written to the database, preventing "Orphan" errors during validation.

**Old String (inferTypeFromId):**
```javascript
        if (id.startsWith('SCN-'))
            return NodeType.TEST_SCENARIO;
        if (id.startsWith('REF-'))
            return NodeType.REFERENCE_SOURCE;
        return null;
```

**New String (inferTypeFromId):**
```javascript
        if (id.startsWith('SCN-'))
            return NodeType.TEST_SCENARIO;
        if (id.startsWith('REF-'))
            return NodeType.REFERENCE_SOURCE;
        if (id.startsWith('NAV-'))
            return NodeType.UI_NAVIGATION_MAP;
        if (id.startsWith('UIC-'))
            return NodeType.UI_COMPONENT_SPEC;
        if (id.startsWith('VIEW-'))
            return NodeType.ARCHITECTURE_VIEW;
        return null;
```

**Old String (Sync Extraction):**
```javascript
                // Extract links from trace_to
                if (content.trace_to) {
```

**New String (Sync Extraction):**
```javascript
                // Custom Arcadia extraction
                if (content.allocated_functions) {
                    for (const func of content.allocated_functions) {
                        if (func.traces_to) {
                            for (const targetId of func.traces_to) {
                                this.db.addLink(content.id, targetId, 'functional_requirements');
                            }
                        }
                    }
                }
                if (content.realizes_logical_components) {
                    for (const targetId of content.realizes_logical_components) {
                        this.db.addLink(content.id, targetId, 'logical_components');
                    }
                }
                if (Array.isArray(content.traces_to)) {
                    for (const targetId of content.traces_to) {
                        this.db.addLink(content.id, targetId, 'user_requirements');
                    }
                }

                // Extract links from trace_to
                if (content.trace_to) {
```

---

## 3. `dist/core/engine/SemanticValidator.js`

**Reasoning:** Reference Source artifacts (`REF-XXX`) were being flagged as Orphans because the validator did not recognize `reference_source` as a valid "root" type (a node that does not require parent nodes). 

**Old String:**
```javascript
            // Root types don't need parents
            const rootTypes = [
                'context',
                'stakeholder',
                'user_char',
                'business_rule',
                'non_functional_requirement',
                'constraint',
                'assumption',
                'system_requirement'
            ];
```

**New String:**
```javascript
            // Root types don't need parents
            const rootTypes = [
                'context',
                'stakeholder',
                'user_char',
                'business_rule',
                'non_functional_requirement',
                'constraint',
                'assumption',
                'system_requirement',
                'reference_source'
            ];
```