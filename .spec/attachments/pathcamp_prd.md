# PRD: Pathcamp – Sandbox Campaign Engine

## 1. Executive Summary
**Pathcamp** is a metadata-driven "Campaign Simulation Engine" for Pathfinder 2e. It automates the mechanical "traces" of a living world—tracking time (Ticks), evolving world events, and scaling encounters—allowing the Game Master (GM) to focus exclusively on narrative impact. The system prioritizes deterministic rule-keeping over AI generation for all gameplay mechanics.

## 2. Core Concepts
* **The World Tick:** The fundamental unit of time. One "Tick" represents a meaningful passage of time (a day, a week, or a journey) that triggers world logic.
* **The Scene:** A metadata-rich container for a location. Scenes have "Traits" (e.g., `[Jungle]`, `[High-Magic]`, `[War-torn]`) that act as filters for all internal calculations.
* **World Events:** * *Background (Static):* Events that occur on specific Ticks regardless of player action (geopolitics).
    * *Fronts (Dynamic):* Threat-based events that players can avert or modify.
* **Trace vs. Impact:** The tool calculates the "Trace" (what monsters appear, what DC is required, how the environment changed); the GM decides the "Impact" (how NPCs react, the emotional weight of the scene).

## 3. Key Features

### 3.1. Metadata-Driven Encounter Engine (Deterministic)
* **Trait-Based Filtering:** Monsters and hazards are proposed based strictly on Scene metadata (e.g., a `[Swamp]` scene only pulls monsters with the `Amphibious` or `Swamp` trait).
* **Level-Scaled Scaling:** Automatic application of Elite/Weak templates based on the Party Level stored in the current session state.
* **Zero-AI Rules:** No LLM is used to determine monster stats, traits, or encounter difficulty.

### 3.2. Chronos Timeline (The Tick System)
* **Tick Management:** GM-controlled "Advance Tick" button.
* **Event Triggers:** On a Tick advance, the system checks the Global Timeline. 
    * *Example:* On Tick 15, "The Plague" event triggers, adding the `[Plagued]` tag to all `[Urban]` scenes.
* **Travel Logic:** Calculation of Ticks required for travel between locations, automatically checking for event triggers during transit.

### 3.3. Scene & Environment Manager
* **Characteristic Inheritance:** Scenes inherit tags from the Global World State (e.g., if a "War" event is active, the scene inherits `[Civilian Unrest]`).
* **Contextual Loot:** Rewards are filtered by scene metadata (e.g., `[Underwater]` scenes favor items with the `Water` trait).

### 3.4. AI Narrator (The "Flavor Layer")
* **Role:** The LLM (Gemini API) is used *only* to describe the metadata. 
* **Input:** "Describe a `[Swamp]` scene with `[Refugee]` and `[War-torn]` tags where a `[Giant Toad]` appears."
* **Output:** Narrative prose that contextualizes the mechanical data provided by the engine.

## 4. Technology Stack
* **Data Layer:** PostgreSQL (for relational World Events) and MongoDB (for the "loose" JSON monster data from Foundry VTT).
* **Backend:** FastAPI (Python) to handle the complex "Elite/Weak" math and trait-filtering logic.
* **Frontend:** React/Tailwind for a dashboard-style GM interface.
* **Intelligence:** Gemini 1.5 Flash for narrative flavor-text only.

## 5. Constraints & Compliance
* **Legal:** Open Gaming License (OGL) or Open RPG Creative License (ORC) compliance. No proprietary IP.
* **Resources:** Use generic fantasy assets for UI branding.
* **Determinism:** The system must never use AI to "guess" a monster's level or a check's DC. All must be derived from the metadata.

## 6. User Workflow Example
1.  **GM Action:** Moves players from *City A* to *City B*. The journey takes **2 Ticks**.
2.  **Tool Trace:** * Advances world clock by 2. 
    * Detects "Background Event: Siege" has started. 
    * Applies `[Siege]` tag to the region.
    * Calculates a `Moderate` encounter for the `[Swamp]` pass.
3.  **Tool Proposal:** "Encounter: 2x Bog Mummies (Elite). Scene Modifier: Visibility reduced by smoke from the Siege."
4.  **GM Impact:** Decides the mummies are actually fallen soldiers from the Siege, adding a narrative hook.