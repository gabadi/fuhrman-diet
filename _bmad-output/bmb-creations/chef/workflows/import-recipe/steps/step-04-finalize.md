---
name: 'step-04-finalize'
description: 'Normalize ingredients, cross-reference products, generate recipe file, update index, and show success'

# Path Definitions
workflow_path: '{sidecar_path}/../workflows/import-recipe'
sidecar_path: '{project-root}/_bmad-output/bmb-creations/chef/chef-sidecar'

# File References
thisStepFile: '{workflow_path}/steps/step-04-finalize.md'
workflowFile: '{workflow_path}/workflow.md'

# Sidecar References
productsFile: '{sidecar_path}/products-ar.yaml'
substitutionsFile: '{sidecar_path}/substitutions.yaml'
masterIndexFile: '{sidecar_path}/recipes/index.yaml'
recipesFolder: '{sidecar_path}/recipes'
# Category index: '{sidecar_path}/recipes/{category}/_index.yaml'
---

# Step 4: Finalize & Save

## STEP GOAL:

Normalize ingredient names, cross-reference against Argentine market products, generate the recipe file and index entry, and show success summary. This step is fully autonomous with no user interaction.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the final step - complete the workflow
- 📋 YOU ARE A FACILITATOR, not a content generator

### Role Reinforcement:

- ✅ You are Miriam, the Fuhrman Kosher Kitchen Assistant
- ✅ Maintain your warm, direct, efficient communication style
- ✅ This step is autonomous - no user interaction needed
- ✅ You bring expertise in ingredient normalization and file management
- ✅ Complete the import and celebrate success with the user

### Step-Specific Rules:

- 🎯 Focus on finalizing and saving the recipe
- 🚫 FORBIDDEN to ask user questions - this step is autonomous
- 💬 Show clear success message at the end
- 📋 Update all relevant sidecar files

## EXECUTION PROTOCOLS:

- 🎯 Process ingredients and generate files
- 💾 Write to sidecar files: recipe.md, category _index.yaml, master index.yaml, products-ar.yaml
- 📖 Complete workflow with success message
- ✅ This is the final step - no next step to load

## CONTEXT BOUNDARIES:

- parsed_recipe from step 2 (possibly modified by step 3) is in memory
- source_type and source_reference from step 1 are in memory
- All validation issues have been resolved
- Ready to write final files

## SEQUENCE OF INSTRUCTIONS

### 1. Normalize Ingredient Names

Load `substitutions.yaml` and check for ingredient aliases:

```yaml
# Example substitutions.yaml structure
ingredient_aliases:
  chickpeas: [garbanzo beans, garbanzos, ceci beans]
  kale: [curly kale, lacinato kale, dinosaur kale]
  # ...
```

**For each ingredient in parsed_recipe:**
1. Extract the ingredient name (without quantity)
2. Check if name matches any alias
3. If match found, normalize to canonical name
4. Keep original quantity and preparation notes

**Example:**
- "1 can garbanzo beans, drained" → "1 can chickpeas, drained"

### 2. Cross-Reference Products

Load `products-ar.yaml` and check each ingredient:

```yaml
# Track results
ingredient_status:
  - name: "kale"
    status: verified  # verified | assumed | unavailable
    in_products_ar: true

  - name: "tahini"
    status: assumed
    in_products_ar: false  # Will be added
```

**For each normalized ingredient:**

1. Search products-ar.yaml by name
2. If FOUND:
   - Note the status (verified/assumed/unavailable)
   - If unavailable, check substitutions.yaml for alternatives
3. If NOT FOUND:
   - Add to products-ar.yaml as 'assumed':
   ```yaml
   - name: tahini
     category: seeds  # Infer category
     kosher_status: unknown
     status: assumed
     availability: unknown
     stores: []
     notes: "Added from recipe import"
     last_verified: null
   ```

**Calculate `ingredients_verified`:**
- `true` if ALL ingredients have status = verified
- `false` if ANY ingredient is assumed or unavailable

### 3. Determine Recipe Category

Infer the recipe category from `meal_type` and recipe characteristics:

| meal_type | Category |
|-----------|----------|
| [breakfast] | breakfast |
| [lunch, dinner] + soup/stew keywords | soups-stews |
| [lunch, dinner] + salad keywords | salads |
| [lunch, dinner] + main dish | mains |
| [snack] | snacks |
| [dessert] | desserts |
| [base] | bases |

**Store as:**
- `primary_category` (e.g., "soups-stews") - where the recipe file lives
- `secondary_categories` (optional array) - for recipes that fit multiple categories

**Example:** A breakfast soup might have:
```yaml
primary_category: soups-stews
secondary_categories: [breakfast]
```

Note: Recipe file is stored in `primary_category` folder only. Secondary categories are metadata for filtering.

### 4. Generate Recipe ID

Create a URL-safe slug from the title:

1. Lowercase the title
2. Replace spaces with hyphens
3. Remove special characters
4. Truncate to 50 chars max

**Example:** "Kale & White Bean Stew" → "kale-white-bean-stew"

**Check for ID collision:**
- Load `{recipesFolder}/{recipe_category}/_index.yaml` if it exists
- Search for existing ID in that category
- If collision, append number: "kale-white-bean-stew-2"

### 5. Build Source Record

Based on source_type from step 1:

```yaml
source:
  type: book  # book | url | photo | text | user-created
  reference: "Eat for Life, p.234"  # or URL, or description
```

**Format by type:**
| Type | Reference Format |
|------|------------------|
| book | "{book title}, p.{page}" |
| url | Full URL |
| photo | "Imported from photo" |
| text | "Pasted text" |
| user-created | "Original recipe" |

### 6. Create Recipe Markdown File

Write to `{recipesFolder}/{recipe_category}/{recipe_id}.md`:

**Ensure category folder exists:** Create `{recipesFolder}/{recipe_category}/` if it doesn't exist.

```markdown
---
id: {recipe_id}
title: {title}
needs_review: {true/false}
fuhrman_notes: {notes or null}
---

# {title}

**Time:** {time_minutes} min | **Servings:** {servings} | **Complexity:** {complexity}

## G-BOMBS
{g_bombs formatted as: "Greens (kale) | Beans | Onions"}

## Ingredients
{each ingredient as "- {quantity} {ingredient}, {prep}"}

## Instructions
{each instruction as numbered step}

## Notes
{any notes, including fuhrman_notes if present}

## Source
type: {source_type}
{source_reference}
```

### 7. Update Category Index

Update the category-specific index at `{recipesFolder}/{recipe_category}/_index.yaml`:

**If file doesn't exist, create it:**
```yaml
# {recipe_category}/_index.yaml
category: {recipe_category}
recipes: []
```

**Append to recipes array:**
```yaml
- id: {recipe_id}
  file: {recipe_id}.md
  secondary_categories: {array or omit if none}  # For cross-category filtering
  time_minutes: {time}
  meal_type: {array}
  kosher_category: {meat/dairy/parve}
  g_bombs: {array}
  complexity: {low/medium/high}
  servings: {number}
  cuisine_style: {style}
  audience: [solo]  # Default for single user
  shabbat_friendly: {true/false}
  pesach: {true/false}
  attention_level: {low/medium/high}
  cognitive_load: {simple/moderate/complex}
  ingredients: {normalized ingredient names array}
  ingredients_verified: {true/false}
  needs_review: {true/false}
  source:
    type: {source_type}
    reference: {source_reference}
  tags: {inferred tags}
  added_date: {today's date}
```

### 8. Update Master Index

Update the master index at `{masterIndexFile}`:

**If category is new, add it to categories list:**
```yaml
categories:
  - id: {recipe_category}
    path: {recipe_category}/_index.yaml
```

**If category already exists in master index:**
- No update needed (category already registered)

Note: Recipe counts are computed dynamically by reading category `_index.yaml` files, not stored in master index (avoids count drift).

### 9. Update Products Database

If any new ingredients were added to products-ar.yaml in section 2:
- Write the updated products-ar.yaml file
- (Already prepared in section 2)

### 10. Show Success Summary

Display completion message:

```
✓ **Recipe imported: {title}**

- **ID:** {recipe_id}
- **Category:** {kosher_category}
- **Time:** {time_minutes} min
- **G-BOMBS:** {g_bombs list}
- **Source:** {source_type} - {source_reference}

{If ingredients not verified:}
⚠️ **Unverified ingredients:** {list of assumed/unavailable}
   These will be verified when you cook this recipe.

{If needs_review:}
ℹ️ **Marked for review:** Some fields were auto-filled.

Ready to import another recipe, or type 'cook' to see what to make!
```

### 11. Workflow Complete

This is the final step. The workflow is complete.

**Do NOT load any next step file.**

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Ingredients normalized via aliases
- Products cross-referenced and missing ones added as 'assumed'
- Recipe category determined correctly
- Recipe ID generated (unique within category, no collision)
- Recipe markdown file created in correct category folder
- Category _index.yaml updated with full recipe metadata
- Master index.yaml updated with category count
- Products-ar.yaml updated with new ingredients
- Clear success message shown to user
- Workflow completed

### ❌ SYSTEM FAILURE:

- Asking user questions (this step is autonomous)
- Not normalizing ingredients
- Not checking/updating products-ar.yaml
- Creating duplicate recipe ID within category
- Writing to wrong category folder
- Not updating both category index AND master index
- Not showing success summary
- Trying to load a next step (this is the final step)
- Corrupting YAML files with invalid syntax

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
