# Fuhrman Kosher Chef — Architecture Document

**Date:** 2025-12-28
**Status:** Approved
**Brainstorming Method:** Morphological Analysis + Targeted Elicitations

---

## Executive Summary

A single AI agent system ("Fuhrman Kosher Chef") that answers: **"What should I cook right now?"**

Tailored for:
- **Fuhrman Diet** (Nutritarian) compliance
- **Kosher** dietary laws
- **Argentine market** availability

---

## Core Design Principles

1. **Single agent** with sidecar knowledge folder
2. **Passive learning** — infers from choices, not Q&A
3. **Lazy verification** — imports freely, verifies through usage
4. **Minimal friction** — smart defaults, optional depth

---

## Folder Structure

```
_bmad/
└── fuhrman-chef/
    ├── agents/
    │   └── chef.md
    ├── workflows/
    │   ├── what-to-cook/
    │   │   └── workflow.md
    │   ├── add-product/
    │   │   └── workflow.md
    │   └── import-recipe/
    │       └── workflow.md
    └── sidecar/
        ├── preferences.yaml
        ├── products-ar.yaml
        ├── substitutions.yaml
        ├── history.yaml
        ├── reviews.yaml
        └── recipes/
            ├── index.yaml
            └── *.md
```

---

## Agent: chef.md

### Persona

Expert Fuhrman nutritionist + kosher kitchen manager + Argentine market specialist

### Interaction Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Quick** | "30 min, dinner" | Minimal questions, fast answer |
| **Planning** | "Shabbat menu" | Multi-dish, prep timeline |
| **Discovery** | "Something new" | Suggest unfamiliar recipes |
| **Use-up** | "I have X, Y" or photo | Ingredient-first search |
| **Low-spoon** | "Easy day" / "Low energy" | Ultra-simple, hands-off only |

### Compliance Levels

- **Strict:** 100% Fuhrman (no oil, no salt, no exceptions)
- **Relaxed:** 90/10 rule allowed

### Holiday Awareness

- Knows Hebrew calendar + Argentine dates
- Pesach → only pesach-friendly recipes
- Friday/Erev Chag → offers Shabbat planning mode
- Fast days → aware, plans for after

---

## Sidecar: preferences.yaml

```yaml
user_name: Gabadi
family_size: 1
location: argentina

kosher_standards:
  accepted_hechshers: [OU, OK, Star-K, local-AR]
  meat_dairy_wait_hours: 6
  chalav_yisrael: false
  pas_yisrael: false
  kitniyot_on_pesach: false

taste:
  loves: [mushrooms, kale, berries]
  dislikes: [eggplant, beets]
  allergies: []

limitations:
  equipment:
    missing: [food-processor]
    available: [blender, oven, stovetop]
  techniques:
    avoid: [deep-frying]
  ingredients:
    never_use: []
  time:
    max_weekday_cooking: 45
    max_shabbat_prep: 180
  budget:
    awareness: true
    level: moderate  # low / moderate / flexible
  energy:
    default_mode: normal  # normal / low-spoon

cooking:
  typical_weekday_time: 30
  shabbat_cooking: true
  complexity_preference: medium

fuhrman:
  compliance_level: strict  # strict / relaxed

jewish_calendar:
  aware: true
  location: argentina
```

---

## Sidecar: products-ar.yaml

```yaml
products:
  - name: Kale
    category: greens
    kosher_status: inherently_kosher
    status: verified  # verified / assumed / unavailable
    availability: high
    stores: [Jumbo, Carrefour, Feria]
    price_range: "$200-400/kg"
    season: year-round
    last_verified: 2025-01-15
    notes: "Check for insects"

  - name: Tahini
    category: seeds
    kosher_status: certified
    status: assumed  # Added from recipe import
    availability: unknown
    stores: []
    notes: "Needs verification"

  - name: Nutritional Yeast
    category: other
    status: unavailable
    notes: "Not available kosher in Argentina"
    alternatives: []
```

### Product Statuses

| Status | Meaning |
|--------|---------|
| `verified` | You've bought this, know where/price |
| `assumed` | From recipe import, not yet verified |
| `unavailable` | Confirmed can't find in AR |

---

## Sidecar: substitutions.yaml

```yaml
substitutions:
  - ingredient: kale
    alternatives: [spinach, collard-greens, swiss-chard]
    notes: "Any dark leafy green works"

  - ingredient: tahini
    alternatives: [sunflower-seed-butter, cashew-butter]
    notes: "Similar consistency, different flavor"

  - ingredient: nutritional-yeast
    alternatives: []
    notes: "No good substitute for cheesy flavor"
    unavailable_action: skip_or_omit
```

---

## Sidecar: history.yaml

```yaml
meals:
  - recipe_id: kale-bean-stew
    date: 2025-01-15
    status: reviewed  # suggested → cooked → reviewed
    cooking_notes: "Used spinach instead of kale"

  - recipe_id: mushroom-salad
    date: 2025-01-14
    status: cooked
    cooking_notes: null
```

### Meal Statuses

| Status | Meaning |
|--------|---------|
| `suggested` | User picked this recipe |
| `cooked` | User confirmed cooking done |
| `reviewed` | User gave taste feedback |
| `skipped` | User didn't make it |

---

## Sidecar: reviews.yaml

```yaml
reviews:
  - recipe_id: kale-bean-stew
    date: 2025-01-15
    rating: up  # up / down
    notes: "Family loved it"
    would_make_again: true

  - recipe_id: eggplant-thing
    date: 2025-01-10
    rating: down
    notes: "Texture bad with AR eggplants"
    would_make_again: false
    issues: [local-ingredient-problem]
```

---

## Sidecar: recipes/index.yaml

```yaml
recipes:
  - id: kale-bean-stew
    file: kale-bean-stew.md
    time_minutes: 35
    meal_type: [lunch, dinner]
    kosher_category: parve
    g_bombs: [greens, beans, onions]
    complexity: low
    servings: 4
    cuisine_style: comfort
    audience: [family, solo]
    shabbat_friendly: true
    pesach: false
    attention_level: low
    cognitive_load: simple
    ingredients: [kale, white-beans, onion, garlic, vegetable-broth]
    ingredients_verified: true
    source:
      type: book
      title: "Eat for Life"
      page: 234
    tags: [one-pot, quick]

  - id: frozen-berry-sorbet
    file: frozen-berry-sorbet.md
    time_minutes: 10
    meal_type: [dessert, snack]
    kosher_category: parve
    g_bombs: [berries]
    complexity: low
    servings: 2
    cuisine_style: refreshing
    audience: [kids, solo, guests]
    shabbat_friendly: true
    pesach: true
    attention_level: low
    cognitive_load: simple
    context: [sweet-craving, after-dinner]
    satisfies_craving: ice-cream
    ingredients: [frozen-berries, banana]
    ingredients_verified: true
    source:
      type: book
      title: "Eat to Live"
      page: 312
    tags: [no-cook, quick]
```

### Recipe Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `file` | string | Markdown filename |
| `time_minutes` | int | Total time |
| `meal_type` | array | breakfast, lunch, dinner, snack, dessert |
| `kosher_category` | string | meat, dairy, parve |
| `g_bombs` | array | Which G-BOMBS covered |
| `complexity` | string | low, medium, high |
| `servings` | int | Number of servings |
| `cuisine_style` | string | comfort, mediterranean, asian, etc. |
| `audience` | array | solo, family, kids, guests |
| `shabbat_friendly` | bool | Can be made ahead / eaten cold |
| `pesach` | bool | Kosher for Pesach |
| `attention_level` | string | low (hands-off), medium, high (active) |
| `cognitive_load` | string | simple, moderate, complex |
| `context` | array | sweet-craving, after-dinner, etc. |
| `satisfies_craving` | string | ice-cream, chocolate, etc. |
| `ingredients` | array | List of ingredients |
| `ingredients_verified` | bool | All ingredients verified in AR |
| `source` | object | Book/URL/user origin |
| `tags` | array | Searchable tags |

---

## Workflow: what-to-cook

### Flow

```
1. SESSION START
   - Check history for pending reviews
   - If meal with status='cooked' exists:
     → "How was [recipe]? thumbs up/down/skip"
     → Log to reviews.yaml, update status

2. PARSE INPUT
   - Extract: time, meal type, mode, energy level
   - Detect: "low energy" / "easy day" → low-spoon mode
   - Detect: "Shabbat" / "Friday" → Shabbat planning mode
   - Detect: ingredients mentioned or photo shared

3. PHOTO PROCESSING (if use-up mode + photo)
   - Extract visible ingredients via vision
   - Confirm with user: "I see kale, beans, onions. Correct?"

4. DETERMINE CONSTRAINTS
   - Kosher: meat/dairy/parve?
   - Holiday: Pesach? Shabbat?
   - Fuhrman: strict/relaxed?
   - Energy: normal/low-spoon?
   - Budget: consider if awareness=true

5. FILTER RECIPES
   - time <= available
   - kosher_category matches
   - holiday flags match
   - ingredients available in products-ar (or assumed)
   - not in recent history (7 days)
   - if low-spoon: attention_level=low, cognitive_load=simple
   - if use-up: prioritize matching ingredients

6. RANK BY PREFERENCES
   - Boost: loved ingredients
   - Penalize: disliked ingredients
   - Boost: missing G-BOMBS today
   - Boost: matches cuisine variety
   - Boost: matches audience

7. PRESENT TOP 3
   For each:
   - Name + brief description
   - Time + complexity + attention level
   - G-BOMBS covered
   - Warning if unverified ingredients: "Contains: tahini (not yet verified in AR)"
   - Shopping hint: "You may need to buy: X" (with store if known)

8. USER SELECTS
   - Log to history.yaml as 'suggested'
   - Show recipe
   - "Any issues while cooking? (or just say 'done' when ready)"

9. COOKING FEEDBACK (same session or later)
   - User reports issues → log cooking_notes
   - User says done → status='cooked'
   - "Did you find all ingredients?" → verify/mark unavailable

10. PASSIVE LEARNING
    - Rejected suggestions → note in preferences
    - Frequent choices → boost in ranking
```

---

## Workflow: add-product

### Flow

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

---

## Workflow: import-recipe

### Flow

```
1. INPUT
   - Source: book reference, URL, photo, pasted text

2. EXTRACT CONTENT
   - Parse recipe text/image
   - Identify: title, ingredients, instructions, time

3. ENRICH METADATA
   - Estimate: time_minutes, complexity, servings
   - Detect: meal_type, cuisine_style
   - Analyze: g_bombs coverage
   - Determine: attention_level, cognitive_load

4. KOSHER CLASSIFICATION
   - Determine: meat / dairy / parve
   - Flag if unclear → ask user

5. FUHRMAN COMPLIANCE CHECK
   - Scan for forbidden: oil, salt, sugar, processed foods
   - Flag violations → ask user to adapt or reject

6. INGREDIENT PROCESSING
   For each ingredient:
   - Search products-ar.yaml
   - If found → link, note status
   - If NOT found → auto-add as 'assumed'
   - Check substitutions.yaml for known swaps
   - Set ingredients_verified based on statuses

7. SOURCE TRACKING
   - Record: book/page, URL, or "user submitted"

8. GENERATE RECIPE FILE
   - Create recipes/[id].md
   - Update recipes/index.yaml

9. CONFIRM WITH USER
   - Show summary
   - "Recipe imported! Note: [tahini, nutritional-yeast] not yet verified in AR"
```

---

## Recipe File Template

```markdown
---
id: kale-bean-stew
title: Kale & White Bean Stew
---

# Kale & White Bean Stew

**Time:** 35 min | **Servings:** 4 | **Complexity:** Low

## G-BOMBS
Greens (kale) | Beans | Onions

## Ingredients
- 1 bunch kale, chopped
- 1 can white beans, rinsed
- 1 large onion, diced
- 4 cloves garlic, minced
- 4 cups vegetable broth (no salt added)
- 1 tsp cumin
- Black pepper to taste

## Instructions
1. Water-saute onion until soft (5 min)
2. Add garlic, cook 1 min
3. Add broth, bring to boil
4. Add beans and kale
5. Simmer 20 min until kale tender
6. Season with cumin and pepper

## Notes
- Fuhrman compliant: no oil, no salt
- Can substitute spinach for kale
- Shabbat: make ahead, reheat or serve room temp

## Source
Eat for Life, p.234
```

---

## Approved Decisions Summary

| # | Decision |
|---|----------|
| 1 | Single agent with sidecar folder |
| 2 | 5 interaction modes: Quick, Planning, Discovery, Use-up, Low-spoon |
| 3 | 6 sidecars: preferences, products-ar, substitutions, history, reviews, recipes |
| 4 | Passive learning from choices |
| 5 | MVP = recipe recommendation with shopping hints |
| 6 | Compliance levels (strict/relaxed) |
| 7 | 3 workflows: what-to-cook, add-product, import-recipe |
| 8 | Fridge photo → ingredient extraction (optional) |
| 9 | Jewish holiday awareness (simple flags) |
| 10 | Limitations: equipment, techniques, budget, energy, attention |
| 11 | Auto-add ingredients to products-ar when importing |
| 12 | Product statuses: verified, assumed, unavailable |
| 13 | Lazy verification through cooking feedback |
| 14 | Substitutions sidecar |
| 15 | Source tracking on recipes |
| 16 | Recipe tags: cuisine, audience, shabbat, pesach, attention, cognitive load |
| 17 | Review flow: cooking issues + taste review integrated in what-to-cook |

---

## Implementation Approach

**Decision:** Build as standalone folder in `_bmad/fuhrman-chef/` (Option B)

**Rationale:** Simpler, faster to iterate. Can convert to BMAD module later if sharing desired.

---

## Implementation Checklist

- [ ] Create folder structure
- [ ] Write chef.md agent
- [ ] Write what-to-cook workflow
- [ ] Write add-product workflow
- [ ] Write import-recipe workflow
- [ ] Create preferences.yaml with user data
- [ ] Create empty products-ar.yaml
- [ ] Create empty substitutions.yaml
- [ ] Create empty history.yaml
- [ ] Create empty reviews.yaml
- [ ] Create recipes/index.yaml
- [ ] Run batch import on Fuhrman books
- [ ] Seed initial products-ar with common AR items

---

*Document generated from brainstorming session using Morphological Analysis + Targeted Elicitations*
