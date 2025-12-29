---
stepsCompleted: [1, 2, 3, 4, 6, 7, 8, 9]
---

# Workflow Creation Plan: add-product

## Initial Project Context

- **Module:** chef (bmb-creations/chef)
- **Target Location:** `_bmad-output/bmb-creations/chef/workflows/add-product/`
- **Created:** 2025-12-28
- **Source:** Architecture document at `_bmad-output/analysis/fuhrman-chef-architecture.md`

## Workflow Purpose

Add or verify products in the Argentine market database (`products-ar.yaml`).

## Flow from Architecture Document

```
1. USER INPUT
   - "I found kosher tahini at Jumbo"

2. GATHER DETAILS
   - Brand? Hechsher? Approximate price?

3. ADD TO products-ar.yaml
   - Set status: verified
   - Set last_verified: today

4. UPDATE RECIPES
   - Any recipes with this ingredient → ingredients_verified may become true

5. CONFIRM
   - "Added! I'll now recommend recipes using tahini."
```

## Data Structure (from products-ar.yaml)

```yaml
- name: Product Name
  category: greens | beans | seeds | berries | fruit | vegetables | other
  kosher_status: inherently_kosher | certified | unknown
  status: verified | assumed | unavailable
  availability: high | medium | low | unknown
  stores: [Store1, Store2]
  price_range: "$X-Y/unit"
  season: year-round | seasonal description
  last_verified: YYYY-MM-DD
  notes: "Any relevant notes"
  alternatives: []  # if unavailable
```

## Integration Points

- **Sidecar files:**
  - `products-ar.yaml` - Primary target for adding/updating products
  - `recipes/index.yaml` - Update `ingredients_verified` flag when products are verified
  - `substitutions.yaml` - May need to add alternatives for unavailable products

## Requirements (Step 2)

### Workflow Classification

| Aspect | Value |
|--------|-------|
| **Type** | Action Workflow (modifies sidecar YAML files) |
| **Flow Pattern** | Linear - may be simplified to fewer steps during design |
| **Interaction Style** | Conversational, minimal friction |
| **Instruction Style** | Intent-based (matches Miriam's persona) |

### Inputs

- User statement about a product (e.g., "I found kosher tahini at Jumbo")
- Optional details: Brand, hechsher, approximate price, store, availability

### Outputs

- Updated `products-ar.yaml` with new or verified product
- Updated `recipes/index.yaml` if recipes can now be marked `ingredients_verified: true`
- Confirmation message to user

### Success Criteria

- Product correctly added/updated in database
- Related recipes updated if applicable
- User receives clear confirmation

### Design Notes

- The 5 steps from architecture doc may consolidate into fewer workflow steps
- Should handle: adding new products, verifying assumed products, marking unavailable
- Keep interaction minimal - infer what's possible, ask only essentials

## Tools Configuration (Step 3)

### Core BMAD Tools

| Tool | Included | Reason |
|------|----------|--------|
| Party-Mode | No | Too simple for multi-agent discussion |
| Advanced Elicitation | No | Straightforward validation |
| Brainstorming | No | No creative ideation needed |

### LLM Features

| Feature | Included | Reason |
|---------|----------|--------|
| File I/O | Yes | Must read/write sidecar YAML files |
| Web-Browsing | No | Local data only |
| Sub-Agents | No | Single workflow path |
| Sub-Processes | No | Sequential operations |

### Memory Systems

| System | Included | Reason |
|--------|----------|--------|
| Sidecar File | Yes | Uses existing chef-sidecar structure |

### External Integrations

None required.

### Installation Requirements

None - all tools are built-in.

## Plan Review (Step 4)

### Recipe Update Logic (Clarified)

When a product is verified, the workflow should:
1. Find all recipes in `recipes/index.yaml` that have that ingredient in their `ingredients` array
2. For each recipe, check if ALL its ingredients now have `status: verified` in `products-ar.yaml`
3. If yes → set `ingredients_verified: true` on that recipe

This helps Miriam prioritize recipes where all ingredients are confirmed available in Argentina.

### Output Documents

This workflow does NOT produce output documents - it modifies existing sidecar YAML files.

### Plan Status: APPROVED

## Workflow Design (Step 6)

### Step Structure (2 steps)

| Step | File | Purpose |
|------|------|---------|
| 1 | step-01-init.md | Parse user input, check product exists, gather missing details |
| 2 | step-02-execute.md | Add/update product, update recipes, confirm to user |

### Continuation Support

Not needed - quick action workflow that completes in single interaction.

### Flow Diagram

```
WORKFLOW START
  User: "I found kosher tahini at Jumbo"
         │
         ▼
┌─────────────────────────────────────┐
│ STEP 1: Initialize & Gather         │
│ ─────────────────────────────       │
│ 1. Load products-ar.yaml            │
│ 2. Parse input (product, store)     │
│ 3. Check if product exists:         │
│    - assumed → verify mode          │
│    - verified → update mode         │
│    - not found → add new mode       │
│ 4. Infer category, kosher_status    │
│ 5. Ask only critical missing info   │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ STEP 2: Execute & Confirm           │
│ ─────────────────────────────       │
│ 1. Add/update in products-ar.yaml   │
│ 2. Load recipes/index.yaml          │
│ 3. Find recipes with ingredient     │
│ 4. Update ingredients_verified flag │
│ 5. Confirm with summary             │
└─────────────────────────────────────┘
         │
         ▼
WORKFLOW END
```

### Interaction Pattern

- Minimal friction - infer what's possible
- No menus - conversational flow
- Only ask critical questions (e.g., hechsher for certified products)

### File Structure

```
add-product/
├── workflow.md
├── steps/
│   ├── step-01-init.md
│   └── step-02-execute.md
└── workflow-plan-add-product.md
```

### Design Status: APPROVED

## Build Summary (Step 7)

### Files Created

| File | Path | Purpose |
|------|------|---------|
| workflow.md | `add-product/workflow.md` | Main workflow configuration |
| step-01-init.md | `add-product/steps/step-01-init.md` | Parse input, check existing, gather details |
| step-02-execute.md | `add-product/steps/step-02-execute.md` | Add/update product, update recipes, confirm |

### Full Paths

```
_bmad-output/bmb-creations/chef/workflows/add-product/
├── workflow.md
├── steps/
│   ├── step-01-init.md
│   └── step-02-execute.md
└── workflow-plan-add-product.md
```

### Key Features Implemented

1. **Four operation modes:** ADD NEW, VERIFY, UPDATE, REAVAILABLE
2. **Smart inference:** Category and kosher status inferred from product type
3. **Minimal questions:** Only asks for critical missing info (e.g., hechsher for certified products)
4. **Recipe verification:** Automatically updates `ingredients_verified` flag on recipes
5. **Warm confirmations:** Celebratory messages that match Miriam's persona

### Build Status: COMPLETE

## Review & Validation (Step 8)

### Validation Results

| Check | Status | Notes |
|-------|--------|-------|
| File Structure | PASSED | All 3 files present in correct locations |
| Configuration | PASSED | Frontmatter valid, paths use variables correctly |
| Step Compliance | PASSED | Both steps follow template structure |
| Cross-File Consistency | PASSED | Variable names match, paths consistent |
| Requirements Verification | PASSED | All requirements from architecture doc met |
| Best Practices | PASSED | Files focused, collaborative patterns used |

### Issues Found & Fixed

| Issue | Severity | Fix Applied |
|-------|----------|-------------|
| step-02-execute.md missing 🔄 CRITICAL rule | Warning | Added final step indicator rule |

### Test Scenarios

1. **Add new product:** "I found chia seeds at Jumbo"
2. **Verify assumed:** "Found tahini with OU at Carrefour" (tahini is assumed in DB)
3. **Update verified:** "Kale is also at Feria now" (kale is already verified)
4. **Reavailable:** "Nutritional yeast is back!" (currently unavailable)

### Deployment Notes

- Workflow integrates with existing chef agent via menu trigger `add-product`
- Uses same sidecar path as what-to-cook workflow
- No installation required - all files in place

## Completion (Step 9)

### Final Status: WORKFLOW CREATION COMPLETE

**Location:** `_bmad-output/bmb-creations/chef/workflows/add-product/`

**Files:**
- `workflow.md` - Main workflow entry point
- `steps/step-01-init.md` - Parse input, check existing, gather details
- `steps/step-02-execute.md` - Execute add/update, confirm to user

### Next Steps

1. **Test the workflow** by invoking Miriam and using the `add-product` trigger
2. **Verify recipe updates** work correctly when verifying products
3. **Consider adding** to chef.agent.yaml menu if not already present

### Integration Checklist

- [x] Workflow files created
- [x] Step files follow BMAD conventions
- [x] Sidecar paths match chef module
- [x] chef.agent.yaml has `add-product` menu trigger (line 48-50)
- [ ] Test with real product additions

### Workflow Creation: COMPLETE
