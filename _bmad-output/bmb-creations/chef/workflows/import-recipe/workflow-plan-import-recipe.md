---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9]
status: COMPLETE
completionDate: 2025-12-28
---

# Workflow Creation Plan: import-recipe

## Initial Project Context

- **Module:** chef (Fuhrman Kosher Chef - Miriam)
- **Target Location:** _bmad-output/bmb-creations/chef/workflows/import-recipe/
- **Created:** 2025-12-28
- **Source:** Brainstorming document at `_bmad-output/analysis/fuhrman-chef-architecture.md`

## Workflow Purpose

Import recipes from multiple sources (book references, URLs, photos, pasted text) into Miriam's recipe library with:
- Fuhrman compliance checking
- Kosher classification
- Argentine market ingredient verification
- Automatic metadata enrichment

## Requirements Gathered

### Workflow Type
**Action Workflow** - performs actions (recipe parsing, file creation, database updates)

### Workflow Flow
**Linear with branching** - main linear path with decision points at compliance checks

### User Interaction Style
**Collaborative but efficient** - confirmations at key decision points, not every field

### Instruction Style
**Intent-Based** - matching other chef workflows, flexible conversation

### Input Requirements
- Recipe source: book reference, URL, photo, or pasted text
- Sidecar files: products-ar.yaml, substitutions.yaml, recipes/index.yaml, preferences.yaml

### Output Specifications
- Primary: Recipe markdown file in `recipes/[id].md`
- Secondary: Updated `recipes/index.yaml`
- Side effect: Auto-add missing ingredients to `products-ar.yaml` as 'assumed'

### Success Criteria
- Recipe properly parsed from source
- Metadata enriched (time, complexity, g_bombs, etc.)
- Kosher category determined correctly
- Fuhrman compliance checked per user's compliance_level
- Ingredients cross-referenced with products-ar
- Recipe file and index created/updated

## Elicitation Decisions (Approved)

### P1: Store Original Recipe ✅ ACCEPTED
Store `original_text` in recipe file - allows user to reference/compare/revert after adaptations.

### P2: Duplicate Detection ✅ ACCEPTED
Before creating, check for existing recipe with same title OR same source (book+page, URL). Warn user if found.

### P3: Quick Capture Mode ✅ PARTIAL ACCEPTED
Instead of two full modes, allow skipping confirmation step. Mark recipe as `needs_review: true` for later refinement.

### P4: Batch Import ❌ DEFERRED
Keep single import fast. Revisit if actual usage shows need.

### P5: Ingredient Normalization ✅ ACCEPTED
Use `ingredient_aliases` in substitutions.yaml. Normalize "garbanzo beans" → "chickpeas" during import.

### P6: Compliance Levels on Import ✅ ACCEPTED
Honor `compliance_level` from preferences.yaml:
- **strict:** Flag all violations, require user decision
- **relaxed:** Import with `fuhrman_notes` warning but don't block

### P7: User Confirmation Summary ✅ ACCEPTED
Before saving, show summary of all auto-detected fields (kosher category, time, g-bombs, etc.) for user verification.

### P8: Kosher Ambiguity Detection ✅ ACCEPTED
Scan ingredient list for known meat/dairy indicators (chicken, beef, butter, cream, cheese, milk). If found, force user confirmation of kosher category.

### P9: Language/Translation ❌ DEFERRED
Handle on-the-fly if needed. Don't add workflow complexity.

## Elicitation Decisions - Round 2 (Approved)

### P10: Batch Warnings Together ✅ ACCEPTED
Collect ALL warnings (kosher ambiguity, Fuhrman violations, missing fields) during analysis. Present them together in one "Issues Found" summary. User addresses all at once instead of sequential interrupts.

### P11: Auto-Proceed When Clean ✅ ACCEPTED
If no warnings, no ambiguity, no compliance issues → auto-save and show success. Only stop for user input when actually needed. Aligns with "minimal friction" design principle.

### P12: Graceful URL Parsing Failure ✅ ACCEPTED
If URL parsing produces incomplete/invalid result (no title, no ingredients), show what was extracted and ask: "I couldn't fully parse this. Here's what I got: [preview]. Edit manually / Try different URL / Cancel?"

### P13: Handle Missing Recipe Fields ✅ ACCEPTED
Define defaults/fallbacks:
- No title → Generate from first 3 ingredients or ask user
- No time → Mark as `time_minutes: null` with `needs_review: true`
- No servings → Default to 4, mark `needs_review: true`

### P14: "User-Created" Source Type ✅ ACCEPTED
Add source type `user-created` for original recipes. Covers user inventions and verbally shared recipes.

### P15: Simplify to 5 Phases ✅ ACCEPTED
Consolidate 10 granular steps into 5 logical phases (5 step files). Each file handles a complete phase instead of micro-actions.

### P16: Seed Ingredient Aliases ✅ ACCEPTED
Implementation note: Seed substitutions.yaml with 20-30 common ingredient aliases. Expand organically as user imports recipes.

## Elicitation Decisions - Round 3 (Structure Design)

### P17: Merge PROCESS + SAVE ✅ ACCEPTED
Merge step-04-process and step-05-save into single `step-04-finalize.md`. Both are autonomous work with no user interaction. Result: 4 step files instead of 5.

### P18: Keep ANALYZE + VALIDATE separate ✅ KEPT
Different concerns (extraction vs compliance). Clearer error handling - know exactly which phase failed.

### P19: Quick Import escape hatch ❌ DEFERRED
Make normal flow fast enough. User can always say "save anyway" when issues found.

### P20: Issues Resolution UI ✅ ACCEPTED
When issues found in step-03, present actionable resolution:
```
**Issues Found (3):**
1. ⚠️ Kosher: Contains "butter" - detected as dairy but recipe has meat. [Mark as DAIRY / Mark as MEAT / Ask me]
2. ⚠️ Fuhrman: Contains "1 tbsp olive oil" [Remove / Keep with note / Ask me]
3. ℹ️ Missing: No time estimate [Enter time / Skip (needs_review)]

Resolve all and continue? [Y / Edit individually]
```

### P21: Move duplicate check after validation ❌ REJECTED
Current order (duplicate first) is more intuitive: "Do you even want this?" → "Is it valid?" → "Save it."

## Final Flow (4 Phases)

```
PHASE 1: RECEIVE (step-01-receive.md)
   - Detect source type: book, URL, photo, text, user-created (P14)
   - If URL: fetch content, handle 404/failures gracefully (P12)
   - If photo: extract via vision, handle blur/unreadable (P12)
   - Check for duplicates by title similarity + source match (P2)
   - If duplicate found → ask: "Similar recipe exists. Import anyway / Skip / View existing?"
   - Store raw input for processing
   - User interaction: Only if source fails OR duplicate found

PHASE 2: ANALYZE (step-02-analyze.md)
   - Parse recipe: title, ingredients, instructions
   - Handle missing fields with defaults (P13):
     - No title → generate from ingredients or ask
     - No time → null + needs_review
     - No servings → default 4 + needs_review
   - Enrich metadata:
     - Estimate: time_minutes, complexity, servings
     - Detect: meal_type, cuisine_style
     - Analyze: g_bombs coverage
     - Determine: attention_level, cognitive_load
   - User interaction: Only if parsing fails completely (P12)

PHASE 3: VALIDATE (step-03-validate.md)
   - Kosher classification:
     - Determine: meat / dairy / parve
     - Scan for meat/dairy keywords (P8)
     - Flag ambiguity if detected
   - Fuhrman compliance check:
     - Load compliance_level from preferences.yaml (P6)
     - Scan for forbidden: oil, salt, sugar, processed foods
     - If strict: flag violations
     - If relaxed: note warnings but don't block
   - BATCH all warnings together (P10):
     - Kosher ambiguity
     - Fuhrman violations
     - Missing/defaulted fields
   - If ANY issues → present Issues Resolution UI (P20):
     - Show all issues with default resolutions
     - User can accept defaults [Y] or edit individually
   - If CLEAN → proceed silently (P11)
   - User interaction: Only if issues found

PHASE 4: FINALIZE (step-04-finalize.md) [MERGED P17]
   - Normalize ingredient names via aliases (P5, P16)
   - For each ingredient:
     - Search products-ar.yaml
     - If found → link, note status
     - If NOT found → auto-add as 'assumed'
     - Check substitutions.yaml for known swaps
   - Set ingredients_verified based on statuses
   - Record source tracking:
     - book: title + page
     - URL: full URL
     - photo: "imported from photo"
     - text: "pasted text"
     - user-created: "original recipe" (P14)
   - Generate recipe ID (slug from title)
   - Create recipes/[id].md:
     - Frontmatter with all metadata
     - Fuhrman notes if any
   - Update recipes/index.yaml
   - Update products-ar.yaml with new 'assumed' ingredients
   - Show success summary:
     - "Recipe imported: [name]"
     - Note unverified ingredients if any
     - Note if needs_review flag set
   - User interaction: None (autonomous)
```

## Workflow Structure Design

### File Structure
```
import-recipe/
├── workflow.md
└── steps/
    ├── step-01-receive.md
    ├── step-02-analyze.md
    ├── step-03-validate.md
    └── step-04-finalize.md
```

### Continuation Support
Not needed - single recipe import is fast, no multi-session work.

### Interaction Pattern
Minimal friction (P11): Steps auto-proceed when clean. Only stop for:
- Source failures (step-01)
- Duplicates found (step-01)
- Parse failures (step-02)
- Compliance issues (step-03)

No A/P/C menus - simple Y/n confirmations where needed.

### Data Flow
```
User Input → RECEIVE → raw_content, source_type
                ↓
            ANALYZE → parsed_recipe, metadata, warnings[]
                ↓
            VALIDATE → kosher_category, compliance_status, resolved_issues
                ↓
            FINALIZE → recipe.md + index.yaml + products-ar.yaml updated
```

### Role & Persona
Miriam - Fuhrman Kosher Kitchen Assistant. Warm, direct, efficient. Minimal questions, maximum inference.

### Error Handling
| Error | Step | Handling |
|-------|------|----------|
| URL 404/failure | step-01 | Ask for different source |
| Photo unreadable | step-01 | Ask for retry or manual entry |
| Parse garbage | step-02 | Show preview, offer manual edit (P12) |
| No title | step-02 | Generate from ingredients or ask (P13) |
| Duplicate found | step-01 | Ask: Import anyway / Skip / View |
| Kosher ambiguity | step-03 | Force resolution via Issues UI (P20) |
| Fuhrman violation (strict) | step-03 | Force resolution via Issues UI (P20) |
| ID collision | step-04 | Auto-generate unique suffix |

## Tools Configuration

### Core BMAD Tools
- **Party-Mode**: excluded - Not needed for focused action workflow
- **Advanced Elicitation**: excluded - Used during planning, not runtime
- **Brainstorming**: excluded - Structured extraction, not ideation

### LLM Features
- **Web-Browsing**: included - Essential for importing recipes from URLs
- **File I/O**: included - Core to workflow (recipe files, sidecar updates)
- **Sub-Agents**: excluded - Single workflow, no delegation needed
- **Sub-Processes**: excluded - No parallel processing needed

### Memory Systems
- **Sidecar Files**: included - Essential for products-ar.yaml, substitutions.yaml, recipes/index.yaml, preferences.yaml

### External Integrations
- None required - all selected tools are built-in LLM features

### Installation Requirements
- None - no external dependencies required

## Output Format Design

**Format Type**: Semi-structured

**Output Requirements**:
- Document type: Recipe markdown file + index entry
- File format: .md (recipe) + .yaml (index)
- Frequency: Single recipe per import

**Recipe File Structure** (enhanced from architecture):

```markdown
---
id: kale-bean-stew
title: Kale & White Bean Stew
needs_review: false          # P3/P13: flags incomplete imports
fuhrman_notes: null          # P6: compliance warnings if any
---

# Kale & White Bean Stew

**Time:** 35 min | **Servings:** 4 | **Complexity:** Low

## G-BOMBS
Greens (kale) | Beans | Onions

## Ingredients
- 1 bunch kale, chopped
- ...

## Instructions
1. Water-saute onion until soft (5 min)
2. ...

## Notes
- Fuhrman compliant: no oil, no salt
- ...

## Source
type: book
Eat for Life, p.234
```

**Additions to existing template**:
- `needs_review`: bool - flags imports needing refinement
- `fuhrman_notes`: string|null - compliance warnings
- `source.type`: enum (book|url|photo|text|user-created) - P14

**Removed** (token efficiency):
- `original_text` - can re-fetch from source if needed

**Index Entry**: No changes to architecture-defined format in recipes/index.yaml

## Build Summary

### Files Created

| File | Path | Purpose |
|------|------|---------|
| workflow.md | `_bmad-output/bmb-creations/chef/workflows/import-recipe/workflow.md` | Main workflow configuration |
| step-01-receive.md | `.../steps/step-01-receive.md` | Input detection, URL/photo fetch, duplicate check |
| step-02-analyze.md | `.../steps/step-02-analyze.md` | Parse recipe, extract fields, enrich metadata |
| step-03-validate.md | `.../steps/step-03-validate.md` | Kosher + Fuhrman compliance, batch issues UI |
| step-04-finalize.md | `.../steps/step-04-finalize.md` | Normalize ingredients, save files, success message |

### Implementation Notes

- **4 step files** (consolidated from original 5 per P17)
- **No continuation support** - single recipe import is fast
- **No templates** - recipe format is inline in step-04
- **Auto-proceed pattern** - only stops for issues (P11)
- **Batch issues UI** - implemented in step-03 per P20

### Integration Points

- Reads: `preferences.yaml`, `products-ar.yaml`, `substitutions.yaml`, `recipes/index.yaml`
- Writes: `recipes/{id}.md`, `recipes/index.yaml`, `products-ar.yaml`

### Next Steps for Testing

1. Register workflow in chef.agent.yaml menu
2. Test with URL import
3. Test with book reference
4. Test with pasted text
5. Test duplicate detection
6. Test Fuhrman violation handling (strict mode)
7. Test kosher ambiguity detection
