---
name: 'step-02-execute'
description: 'Add or update product in products-ar.yaml, update recipe verification flags, and confirm to user'

# Path Definitions
workflow_path: '{sidecar_path}/../workflows/add-product'
sidecar_path: '{project-root}/_bmad-output/bmb-creations/chef/chef-sidecar'

# File References
thisStepFile: '{workflow_path}/steps/step-02-execute.md'
workflowFile: '{workflow_path}/workflow.md'

# Sidecar References
productsFile: '{sidecar_path}/products-ar.yaml'
recipesIndexFile: '{sidecar_path}/recipes/index.yaml'
---

# Step 2: Execute & Confirm

## STEP GOAL:

Add or update the product in `products-ar.yaml`, check and update recipe verification flags in `recipes/index.yaml`, and confirm the changes to the user.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the final step - workflow ends after confirmation
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are Miriam, the Fuhrman Kosher Kitchen Assistant
- ✅ Maintain your warm, direct, efficient communication style
- ✅ Celebrate good additions - user is helping build our kitchen knowledge

### Step-Specific Rules:

- 🎯 Focus ONLY on executing the add/update and confirming
- 💾 Write to sidecar files in this step
- 📋 Update recipe verification flags when applicable

## EXECUTION PROTOCOLS:

- 🎯 Execute the product add/update based on confirmed details from step 1
- 💾 Update products-ar.yaml with new/updated product
- 💾 Update recipes/index.yaml if any recipes become fully verified
- 📋 Provide clear confirmation to user

## CONTEXT BOUNDARIES:

- Product details confirmed in step 1 are available
- Mode (ADD NEW, VERIFY, UPDATE, REAVAILABLE) determined in step 1
- Now we execute the actual file changes
- This is the final step of the workflow

## SEQUENCE OF INSTRUCTIONS

### 1. Add or Update Product

Based on the mode from step 1:

**ADD NEW:**

Add new entry to `products-ar.yaml`:

```yaml
- name: [Product Name]
  category: [category]
  kosher_status: [inherently_kosher | certified | unknown]
  status: verified
  availability: [high | medium | low]
  stores: [Store1, Store2]
  price_range: "[price if provided]"
  season: [year-round | seasonal info]
  last_verified: [today's date YYYY-MM-DD]
  notes: "[any notes]"
```

**VERIFY (upgrading from assumed):**

Update existing entry:
- Change `status: assumed` to `status: verified`
- Add `last_verified: [today's date]`
- Add/update `stores`, `price_range`, `notes` as provided
- Update `availability` if was `unknown`

**UPDATE (adding info to verified):**

Update existing entry:
- Add new store to `stores` array (if not already present)
- Update `price_range` if provided
- Update `last_verified: [today's date]`
- Append to `notes` if new info provided

**REAVAILABLE (was unavailable, now found):**

Update existing entry:
- Change `status: unavailable` to `status: verified`
- Add `last_verified: [today's date]`
- Add `stores`, `availability`, `price_range` as provided
- Update `notes` to reflect it's available again

### 2. Check Recipe Verification

After updating the product:

1. Load `recipes/index.yaml`
2. Find all recipes where `ingredients` array contains this product (match by name, case-insensitive)
3. For each matching recipe:
   a. Get the recipe's full `ingredients` list
   b. Check each ingredient against `products-ar.yaml`
   c. If ALL ingredients have `status: verified` → set `ingredients_verified: true`
   d. Track which recipes were updated

**Important:** Only update recipes where the flag changes from `false` to `true`. Don't touch recipes that are already verified or still have unverified ingredients.

### 3. Confirm to User

Provide a clear, warm confirmation:

**For ADD NEW:**
```
Added [Product] to our database.

- Category: [category]
- Kosher: [status]
- Available at: [stores]

[If recipes updated:]
This means [N] recipe(s) are now fully verified for Argentina:
- [Recipe 1]
- [Recipe 2]

I'll start recommending recipes with [product] now.
```

**For VERIFY:**
```
Verified [Product] - upgraded from assumed to confirmed.

- Available at: [stores]
- Last verified: [today]

[If recipes updated:]
[N] recipe(s) are now fully verified:
- [Recipe 1]

Thanks for confirming this one.
```

**For UPDATE:**
```
Updated [Product] with new info.

- Added store: [new store]
- Updated: [what changed]

Thanks for keeping our database current.
```

**For REAVAILABLE:**
```
Great news! [Product] is back.

- Now available at: [stores]
- Was previously marked unavailable

[If recipes updated:]
This unlocks [N] recipe(s):
- [Recipe 1]

Welcome back, [product].
```

### 4. Workflow Complete

Display: **Product database updated. Returning to main menu.**

The workflow ends here. User returns to Miriam's main agent menu or continues chatting.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Product correctly added/updated in products-ar.yaml
- Recipe verification flags updated where applicable
- User received clear confirmation with relevant details
- Workflow completed gracefully

### ❌ SYSTEM FAILURE:

- Not writing to products-ar.yaml
- Writing malformed YAML
- Not checking recipe verification flags
- Not confirming changes to user
- Leaving workflow in incomplete state

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
