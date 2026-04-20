# Software Requirements Specification (SRS)

## 1. Product Context
**Product:** A metadata-driven Campaign Simulation Engine to create, manage, and share dynamic campaigns and world events.
**Perspective:** Independent web-based application (frontend and backend) for Pathfinder 2e Game Masters.

### Definitions


---

## 2. Stakeholders

### STK-001: Primary User and Campaign Creator
*   **Concern:** 

### STK-002: Regulatory Stakeholder
*   **Concern:** 

### STK-003: Secondary User
*   **Concern:** 


---

## 3. Requirements

### 3.1 Use Cases (User Requirements)

#### UR-001: Create a Campaign
*   **Primary Actor:** UCH-001
*   **Trigger:** GM clicks the 'New Campaign' button
*   **Preconditions:**
    
    - GM is locally registered and logged in
    
    - GM is on the main dashboard
    
*   **Postconditions:**
    
    - A new campaign is created in the database at Tick 1
    
    - GM is viewing the new Campaign Dashboard
    
*   **Main Scenario:**
    
    1. GM submits the New Campaign form with Name, Description, Party Size, and Party Starting Level
    
    2. System creates the campaign in the database and initializes its timeline at Tick 1
    
    3. System automatically navigates the GM to the newly created Campaign Dashboard (Timeline View)
    
*   **Exceptions:**
    
    - **1a (Campaign Name already exists for this GM):** System displays an error message 'Campaign Name already exists' and prevents creation
    
    - **1a (Required fields are missing):** System displays an error message and highlights the missing fields
    
*   **Acceptance Criteria:**
    
    - A campaign with the provided details is successfully saved.
    
    - The GM is immediately redirected to the Campaign Dashboard.
    
    - The new campaign starts exactly at Tick 1.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}

#### UR-002: Manage Timeline (Ticks)
*   **Primary Actor:** UCH-001
*   **Trigger:** GM creates a new Tick or selects an existing Tick to modify
*   **Preconditions:**
    
    - GM is logged in
    
    - A campaign exists
    
*   **Postconditions:**
    
    - Timeline is updated with a new Tick or a modified historical Tick
    
    - Subsequent Ticks inherit state changes
    
*   **Main Scenario:**
    
    1. GM creates a new Tick (milestone) or selects a historical Tick on the timeline
    
    2. GM defines or updates the narrative context for that Tick
    
    3. System cascades the state of all global assets (Scenes, NPCs) from the previous Tick into the current one
    
    4. If modifying a historical Tick, System warns GM that changes will overwrite state in subsequent Ticks and requests confirmation
    
    5. System updates the active state for the selected Tick and recalculates inheritance for any future Ticks
    
*   **Exceptions:**
    
    - **4a (GM cancels the historical edit warning):** System reverts changes to the historical Tick and aborts the cascade
    
*   **Acceptance Criteria:**
    
    - A new Tick inherits the exact state of the previous Tick.
    
    - Modifying a past Tick automatically cascades those changes forward to all subsequent Ticks, overwriting conflicting states.
    
    - A warning is displayed before cascading historical changes.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}

#### UR-003: Manage Global Assets (Scenes & NPCs)
*   **Primary Actor:** UCH-001
*   **Trigger:** GM creates or modifies a Scene or NPC within a specific Tick
*   **Preconditions:**
    
    - GM is logged in
    
    - A campaign exists
    
*   **Postconditions:**
    
    - Asset is available globally across the campaign
    
    - Asset state is applied to the active Tick
    
*   **Main Scenario:**
    
    1. GM creates a new Global Asset (Scene or NPC) or selects an existing one within the current Tick
    
    2. GM assigns or modifies Metadata/Traits for that asset in the context of the current Tick
    
    3. GM optionally uploads external files (images, notes) to attach to the Scene
    
    4. System saves the asset's new state to the current Tick
    
    5. System cascades this new state forward to all subsequent Ticks
    
*   **Exceptions:**
    
    - **3a (File upload exceeds size limits or is invalid format):** System displays an error and rejects the file
    
*   **Acceptance Criteria:**
    
    - Scenes and NPCs exist as global entities that can be referenced in any Tick.
    
    - Changes made to a Scene/NPC in Tick X persist in Tick X+1 unless changed again.
    
    - GMs can attach files to Scenes without the system attempting to parse their contents.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}

#### UR-004: Manage World Events and Fronts
*   **Primary Actor:** UCH-001
*   **Trigger:** GM creates a new Event or Front
*   **Preconditions:**
    
    - GM is logged in
    
    - A campaign exists
    
*   **Postconditions:**
    
    - Event or Front is created and assigned to a specific Tick
    
    - Event traits cascade to relevant assets from that Tick onward
    
*   **Main Scenario:**
    
    1. GM defines a new Event or Front (Name, Type, Metadata/Traits)
    
    2. GM assigns the Event to begin at a specific Tick (past, present, or future)
    
    3. System saves the Event to the designated Tick
    
    4. If the Event is assigned to a past or present Tick, System recalculates state inheritance for all subsequent Ticks to include the new Event's traits
    
    5. System warns the GM if recalculation overwrites conflicting states in future Ticks
    
*   **Exceptions:**
    
    - **4a (GM cancels the recalculation warning):** System aborts the event creation and reverts state
    
*   **Acceptance Criteria:**
    
    - Events can be scheduled on any Tick, regardless of the 'current' chronological position.
    
    - Events placed in past Ticks automatically ripple their effects forward.
    
    - The GM is warned about downstream overwrites before they are finalized.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}

#### UR-005: Generate Encounter within a Scene
*   **Primary Actor:** UCH-001
*   **Trigger:** GM clicks 'Generate Encounter' inside a Scene view
*   **Preconditions:**
    
    - GM is logged in
    
    - A Scene exists within a Tick
    
*   **Postconditions:**
    
    - An encounter is generated and attached to the Scene for that Tick
    
*   **Main Scenario:**
    
    1. GM triggers encounter generation within a specific Scene in the current Tick
    
    2. System reads the Scene's explicit traits and any traits inherited from active World Events in that Tick
    
    3. System reads the Campaign's current Party Level and Size
    
    4. System deterministically queries the monster/hazard database using the Traits
    
    5. System calculates the appropriate Elite/Weak templates based on Party Level
    
    6. System outputs the mechanical Trace and allows the GM to input narrative flavor, saving both to the Scene for that Tick
    
*   **Exceptions:**
    
    - **4a (No monsters found matching the exact trait combination):** System proposes closest match or broadens search, notifying the GM
    
*   **Acceptance Criteria:**
    
    - Encounters are generated based strictly on the Scene's traits for that specific Tick.
    
    - The generation process is deterministic.
    
    - The encounter is saved as part of the Scene's state for that Tick along with optional GM narrative.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}

#### UR-006: Share Campaign
*   **Primary Actor:** UCH-001
*   **Trigger:** GM clicks 'Share Campaign'
*   **Preconditions:**
    
    - GM is logged in
    
    - A campaign exists
    
*   **Postconditions:**
    
    - A read-only access link is generated
    
*   **Main Scenario:**
    
    1. GM selects the sharing option for an active campaign
    
    2. System generates a unique, read-only URL
    
    3. GM provides this URL to Campaign Viewers (UCH-002)
    
    4. Viewers access the URL to see the timeline, public events, and current scenes
    
*   **Exceptions:**
    
    - **2a (System fails to generate link):** System displays an error message
    
*   **Acceptance Criteria:**
    
    - The generated link provides read-only access.
    
    - Viewers cannot modify Ticks, Scenes, Events, or trigger Encounters.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}

#### UR-007: Manage Users
*   **Primary Actor:** UCH-003
*   **Trigger:** Admin accesses the user management dashboard
*   **Preconditions:**
    
    - Admin is logged in
    
*   **Postconditions:**
    
    - User account status is modified (blocked/unblocked)
    
*   **Main Scenario:**
    
    1. Admin logs into the system
    
    2. Admin views a list of all registered GM users
    
    3. Admin selects a user and changes their status to Blocked or Active
    
    4. System updates the user's access permissions immediately
    
*   **Exceptions:**
    
    - **3a (Admin attempts to block themselves or the primary super-admin):** System prevents the action and displays an error
    
*   **Acceptance Criteria:**
    
    - All registered users are treated as GMs.
    
    - Admins can block or unblock users to control platform access.
    
    - A blocked user cannot log in or access their campaigns.
    
*   **Trace:** {
  "stakeholders": [
    "STK-001"
  ]
}


### 3.2 Functional Requirements

#### FR-001: Campaign Creation Fields
The system shall allow the Game Master to create a new campaign by capturing the following fields: Name, Description, Party Size, and Party Starting Level.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Database schema correctly stores Name, Description, Party Size, and Starting Level for a Campaign.
    
*   **Trace:** {
  "user_requirements": [
    "UR-001"
  ]
}

#### FR-002: Campaign Data Validation
The system shall require all Campaign Creation fields to be filled and ensure the Campaign Name is unique per Game Master.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - An error is thrown if required fields are blank.
    
    - An error is thrown if a duplicate name is used by the same GM.
    
*   **Trace:** {
  "user_requirements": [
    "UR-001"
  ]
}

#### FR-003: Campaign Timeline Initialization
The system shall initialize every new campaign with an empty timeline starting at exactly Tick 1.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - A newly created campaign has a 'current_tick' value of 1.
    
    - The campaign's global timeline is initialized without any active events.
    
*   **Trace:** {
  "user_requirements": [
    "UR-001"
  ]
}

#### FR-004: Campaign Dashboard Navigation
The system shall automatically navigate the Game Master to the Campaign Dashboard immediately upon successful creation of a new campaign.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Upon successful creation, the frontend router changes view to the specific Campaign Dashboard.
    
*   **Trace:** {
  "user_requirements": [
    "UR-001"
  ]
}

#### FR-005: Create and Update Tick Narrative Context
The system shall allow the Game Master to create a new Tick on the timeline or select an existing Tick to define or update its narrative context.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - GM can create a new sequential Tick.
    
    - GM can select any existing Tick and modify its narrative description field.
    
*   **Trace:** {
  "user_requirements": [
    "UR-002"
  ]
}

#### FR-006: Tick State Inheritance Cascade
Upon creation of a new Tick, the system shall automatically cascade the state of all global assets (Scenes, NPCs) from the immediately preceding Tick into the new Tick.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - A newly created Tick inherits the exact metadata and traits of all assets from the previous Tick.
    
*   **Trace:** {
  "user_requirements": [
    "UR-002"
  ]
}

#### FR-007: Historical Tick Modification Warning
When the Game Master attempts to modify the state of a historical Tick, the system shall display a warning that changes will overwrite state in subsequent Ticks and require explicit confirmation. If cancelled, the system shall abort the operation.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Modifying a non-latest Tick triggers a confirmation prompt.
    
    - Cancelling the prompt reverts any unsaved changes and prevents cascade.
    
*   **Trace:** {
  "user_requirements": [
    "UR-002"
  ]
}

#### FR-008: Future Tick Recalculation
Upon confirmation of changes to a historical Tick, the system shall recalculate the inheritance cascade for all subsequent Ticks, overwriting any conflicting future states with the newly applied changes.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Changes made to Tick N automatically update the inherited state in Tick N+1, N+2, etc.
    
    - Conflicting state changes in later Ticks are overwritten by the cascading update.
    
*   **Trace:** {
  "user_requirements": [
    "UR-002"
  ]
}

#### FR-009: Asset Creation and Trait Assignment
The system shall allow the Game Master to create new Global Assets (Scenes or NPCs) or select existing ones within a specific Tick, and assign or modify their Metadata and Traits.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - GM can create a new Scene or NPC.
    
    - GM can edit traits of an existing Scene or NPC for the currently selected Tick.
    
*   **Trace:** {
  "user_requirements": [
    "UR-003"
  ]
}

#### FR-010: Asset File Attachments and Validation
The system shall allow the GM to upload external files (such as images or notes) to attach to a Scene, enforcing predefined size limits and allowed file formats. It shall display an error and reject invalid files.
*   **Priority:** Should-have
*   **Acceptance Criteria:**
    
    - Valid files are successfully attached to the Scene.
    
    - Files exceeding the size limit trigger an error message and are rejected.
    
    - Unsupported file formats trigger an error message and are rejected.
    
*   **Trace:** {
  "user_requirements": [
    "UR-003"
  ]
}

#### FR-011: Asset State Persistence and Cascade
The system shall save any modifications to an asset's state within the currently active Tick and automatically cascade these changes forward to all subsequent Ticks.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Modifications are saved and immediately reflected in the current Tick.
    
    - The new state is automatically applied to the asset in all chronologically later Ticks.
    
*   **Trace:** {
  "user_requirements": [
    "UR-003"
  ]
}

#### FR-012: Event and Front Creation
The system shall allow the GM to define a new Event or Front with Name, Type, and Metadata/Traits, and assign it to begin at any specific Tick (past, present, or future).
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - GM can successfully create and save an Event or Front with all required fields.
    
    - The Event can be assigned to any existing chronological Tick.
    
*   **Trace:** {
  "user_requirements": [
    "UR-004"
  ]
}

#### FR-013: Event Inheritance Recalculation
When an Event or Front is assigned to a past or present Tick, the system shall recalculate the state inheritance for all subsequent Ticks to include the new Event's traits.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Assigning an event to Tick N correctly applies its traits to assets in Tick N, N+1, N+2, etc.
    
*   **Trace:** {
  "user_requirements": [
    "UR-004"
  ]
}

#### FR-014: Event Overwrite Warning and Cancellation
The system shall warn the GM if the recalculation of an Event's inheritance will overwrite conflicting states in future Ticks. If the GM cancels the warning, the system shall abort the event creation and revert any state changes.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - A warning is shown before overwriting conflicting future states due to an Event.
    
    - Cancelling the warning discards the new Event and preserves the existing timeline state.
    
*   **Trace:** {
  "user_requirements": [
    "UR-004"
  ]
}

#### FR-015: Deterministic Encounter Query by Traits
Upon triggering Encounter Generation, the system shall read the Scene's traits and inherited World Event traits, and deterministically query the monster/hazard database. If no exact match is found, the system shall broaden the search to find the closest match and notify the GM.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - System successfully queries the database using combined traits.
    
    - If an exact match is missing, the system falls back to a broader search and notifies the user.
    
*   **Trace:** {
  "user_requirements": [
    "UR-005"
  ],
  "business_rules": [
    "BR-001",
    "BR-004"
  ]
}

#### FR-016: Encounter Template Calculation
After selecting monsters for an encounter, the system shall mathematically calculate and apply the appropriate Elite or Weak templates based on the Campaign's Party Level and Size.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Elite/Weak templates are correctly applied based on Party Level and Size rules.
    
    - Calculations do not rely on AI/LLM components.
    
*   **Trace:** {
  "user_requirements": [
    "UR-005"
  ],
  "business_rules": [
    "BR-001",
    "BR-004"
  ]
}

#### FR-017: Encounter Narrative Flavor and Persistence
The system shall take the deterministically generated mechanical encounter data and provide a text interface for the GM to add narrative flavor text. Both the mechanical trace and narrative flavor shall be saved to the Scene for the current Tick.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Mechanical trace and user-provided narrative text are both saved successfully.
    
    - The complete encounter is saved and persisted in the Scene's state for the current Tick.
    
*   **Trace:** {
  "user_requirements": [
    "UR-005"
  ],
  "business_rules": [
    "BR-002"
  ]
}

#### FR-018: Campaign Read-Only Link Generation
The system shall generate a unique, read-only URL when the GM selects the sharing option for an active campaign. It shall display an error message if link generation fails.
*   **Priority:** Should-have
*   **Acceptance Criteria:**
    
    - A unique URL is successfully generated upon request.
    
    - If an internal error prevents link generation, a clear error message is shown to the GM.
    
*   **Trace:** {
  "user_requirements": [
    "UR-006"
  ],
  "business_rules": [
    "BR-005"
  ]
}

#### FR-019: Campaign Read-Only Access View
The system shall allow users with a valid read-only link to view the campaign's timeline, public events, and current scenes, while strictly preventing any modifications or encounter generations.
*   **Priority:** Should-have
*   **Acceptance Criteria:**
    
    - Viewers can see the timeline, public events, and current scenes.
    
    - Viewers cannot edit assets, create ticks, or generate encounters.
    
*   **Trace:** {
  "user_requirements": [
    "UR-006"
  ],
  "business_rules": [
    "BR-005"
  ]
}

#### FR-020: Admin User List View
The system shall provide an administrative dashboard where authenticated Admin users can view a list of all registered GM users on the platform.
*   **Priority:** Should-have
*   **Acceptance Criteria:**
    
    - Admin can view all registered users.
    
    - Non-admin users cannot access this view.
    
*   **Trace:** {
  "user_requirements": [
    "UR-007"
  ]
}

#### FR-021: Admin User Status Management
The system shall allow Admins to change the status of any GM user to 'Blocked' or 'Active', immediately updating their access permissions. The system must prevent an Admin from blocking their own account or the primary super-admin account.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Setting a user to 'Blocked' immediately revokes their login and platform access.
    
    - Setting a user to 'Active' restores their access.
    
    - An Admin attempting to block themselves receives an error and the action is blocked.
    
    - An Admin attempting to block the primary super-admin receives an error and the action is blocked.
    
*   **Trace:** {
  "user_requirements": [
    "UR-007"
  ]
}

#### FR-022: User Registration
The system shall allow new Game Masters to register an account with a username, email, and password.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - New users can create accounts.
    
    - User credentials are securely hashed and stored.
    
*   **Trace:** {
  "user_requirements": [
    "UR-001"
  ],
  "stakeholders": [
    "STK-001"
  ]
}

#### FR-023: User Authentication
The system shall provide a login and logout interface for registered users to manage their session.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Users can log in with valid credentials.
    
    - Users can log out to end their session.
    
*   **Trace:** {
  "user_requirements": [
    "UR-001",
    "UR-007"
  ],
  "stakeholders": [
    "STK-001"
  ]
}

#### FR-024: Session Authorization
The system shall enforce authentication for all campaign-modifying API endpoints.
*   **Priority:** Must-have
*   **Acceptance Criteria:**
    
    - Unauthenticated users cannot modify campaign data.
    
    - Campaign viewers (UCH-002) have read-only access via shared links.
    
*   **Trace:** {
  "business_rules": [
    "BR-006"
  ],
  "stakeholders": [
    "STK-001"
  ]
}


### 3.3 Non-Functional Requirements


### 3.4 Constraints

*   **CON-001:** The user interface must follow a Pathfinder 2e aesthetic (fantasy, colorful, clean, simple) and be primarily desktop-focused but fully responsive for mobile devices. (Technical)


### 3.5 Assumptions

