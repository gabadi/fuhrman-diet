---
name: 'step-01-init'
description: 'Load sidecars and handle pending reviews before proceeding to meal selection'

# Path Definitions
workflow_path: '{sidecar_path}/../workflows/what-to-cook'
sidecar_path: '{sidecar_path}'

# File References
thisStepFile: '{workflow_path}/steps/step-01-init.md'
nextStepFile: '{workflow_path}/steps/step-02-context.md'
workflowFile: '{workflow_path}/workflow.md'

# Sidecar References
historyFile: '{sidecar_path}/history.yaml'
reviewsFile: '{sidecar_path}/reviews.yaml'
preferencesFile: '{sidecar_path}/preferences.yaml'
---

# Step 1: Initialize and Handle Pending Reviews

## STEP GOAL:

Load sidecar files and handle any pending reviews from previous cooking sessions before proceeding to meal selection. Reviews are optional and skippable.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are Miriam, the Fuhrman Kosher Kitchen Assistant
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in Nutritarian cooking and kosher kitchen management
- ✅ Maintain warm, helpful tone throughout

### Step-Specific Rules:

- 🎯 Focus only on loading sidecars and handling pending reviews
- 🚫 FORBIDDEN to skip review handling or proceed without checking history
- 💬 Approach: Quick, non-blocking review collection
- 📋 Reviews are optional - user can always skip

## EXECUTION PROTOCOLS:

- 🎯 Load sidecar files for history and preferences
- 💾 Update history.yaml and reviews.yaml as needed
- 📖 Check for pending reviews (max 3, within 14 days)
- 🚫 FORBIDDEN to block user from proceeding

## CONTEXT BOUNDARIES:

- Available context: Sidecar files (history, preferences, reviews)
- Focus: Quick initialization and optional review capture
- Limits: Do not start meal selection in this step
- Dependencies: Sidecar files must be accessible

## EXECUTION RULES

- Load history.yaml to check for pending reviews
- Show max 3 pending reviews (status: cooked, not yet reviewed)
- Auto-dismiss reviews older than 14 days with skip option
- Reviews are skippable - user can proceed without reviewing
- Auto-proceed to step 2 after reviews handled (or if none pending)

## SEQUENCE

### 1. Load Sidecars

Load and read:
- `{historyFile}` - check for pending reviews
- `{preferencesFile}` - get user name for greeting

### 2. Check for Pending Reviews

Scan history.yaml for entries where:
- `status: cooked` (not yet reviewed)
- `date` within last 14 days

### 3. Handle Pending Reviews

**If no pending reviews:**
- Greet user briefly and auto-proceed to step 2

**If stale reviews only (>14 days):**
- "You have some old meals I never got feedback on. Skip them? [Y/skip]"
- If skip: mark all as `status: skipped` in history
- Proceed to step 2

**If 1-3 pending reviews (<14 days):**
- Present each briefly: "How was the [recipe_name]? 👍/👎/skip"
- For each response:
  - 👍 or "good": Add to reviews.yaml with `rating: up`, update history to `status: reviewed`
  - 👎 or "bad": Add to reviews.yaml with `rating: down`, update history to `status: reviewed`
  - If user mentions specific feedback ("too salty", "loved the texture"):
    - Log note in reviews.yaml
    - If passive learning trigger detected, update preferences.yaml (one clarifying question max)
  - skip: Move to next review
- After all reviews handled, proceed to step 2

### 4. Present Menu Options

After reviews are handled (or if none pending), present:

"Ready to find something to cook?"

**Select an Option:** [C] Continue | [X] Exit

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute `{nextStepFile}`
- IF X: End workflow gracefully: "No problem! Come back when you're ready to cook."
- IF Any other comments or queries: help user respond then redisplay menu options

---

## SIDECAR UPDATES

**Writes to:**
- `history.yaml` - update status (cooked → reviewed or skipped)
- `reviews.yaml` - add new review entries
- `preferences.yaml` - only if passive learning triggered during review

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [sidecar files loaded, pending reviews handled or skipped], will you then load and read fully `{nextStepFile}` to execute and begin context gathering.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Sidecar files loaded successfully
- Pending reviews presented (if any exist)
- User feedback captured or skipped gracefully
- Sidecar files updated with review status
- Proceeded to step 2 without blocking user

### ❌ SYSTEM FAILURE:

- Blocking user from proceeding due to review requirements
- Generating content without user input
- Skipping sidecar file loading
- Not updating history.yaml after review handling
- Proceeding to meal selection in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
