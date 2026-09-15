# ROADMAP — Meridian Air Route Recommendation

General guide, not a spec. Phases are ordered but overlap.
**Before each work session, re-read `CLAUDE.md`.**

Ownership legend: 🔧 **Build** (Claude may do) · 🧠 **Judgment** (Justin must own — see CLAUDE.md §2)

---

## Phase 0 — Foundation & data trust  ✅ done
🔧 Load both CSVs, verify grain, validate `Scheduled+Charter=Total`, map month coverage.

**Outcome:** the month-window discovery (CLAUDE.md §4). Every later phase depends on it.
Any analysis written before this was known is suspect and should be redone.

---

## Phase 1 — Planning: frame the problem
The most heavily weighted part of the case. Notebook Part 1.

🧠 **Define "opportunity."** There is no target variable. Decide what makes a route attractive
to a *small* carrier that gets exactly one rotation, and defend it. Write it in your own words.
🧠 **SWOT** of Meridian's position — strengths/weaknesses internal, opportunities/threats
environmental. Feeds directly into what the metric should reward.
🔧 Compute whatever candidate signals the chosen definition implies, so the framing can be
pressure-tested against real numbers before it's locked.

**Design constraint from the client:** niche over mainstream. A metric that just ranks by
volume will surface JFK–LHR and fail the brief on its face. The metric has to encode
*capturability*, not just size.

**Exit:** a written definition of opportunity + a SWOT, both defensible out loud.

---

## Phase 2 — Candidates → shortlist → one route
Notebook Part 2. The brief wants **the funnel, not just the endpoint**.

🔧 Build the funnel mechanically: full route universe → filters → scored shortlist → finalists.
Each narrowing step logged with how many routes survived and why.
🧠 Choose the filters and thresholds, and justify each cut.
🧠 Pick the single recommended route from the finalists.

**Exit:** a reproducible funnel table and one named route.

---

## Phase 3 — Execution: the interactive dashboard
The creative centerpiece. A simple local website (single HTML file, no server needed).

🔧 Let the user move the weights/parameters of the opportunity score and watch the ranking
re-order live. This does double duty:
- it *shows* the framework rather than asserting it, and
- it directly answers deliverable #6 — **"what single finding would have changed your
  recommendation?"** becomes a thing the viewer can discover by dragging a slider until the
  top-ranked route flips.

🔧 Keep it visually simple; the insight is the interactivity, not the chrome.
🧠 Decide which parameters are worth exposing.

**Exit:** one self-contained `.html` that opens by double-click, plus the sensitivity finding
it reveals.

---

## Phase 4 — Assumptions, limitations, risks
Notebook Part 3 / final markdown cell. Graded as "honesty of reasoning."

Required minimums: **≥3 assumptions, ≥2 limitations**, plus failure modes.
🔧 Quantify sensitivity — how far can an input move before the answer changes?
🧠 Write the assumptions and the honest account of how this could be wrong.

Already banked (CLAUDE.md §4): Q4-only coverage, the mid-series month step, the
passengers/departures window mismatch. These are strong, specific limitations —
good enough to satisfy the requirement on their own, but they need *your* framing of
why each one matters to *this* recommendation.

---

## Phase 5 — The deck (5 slides max)
🔧 Render to PDF once the content is settled.
🧠 All narrative and claims.

Working shape (adjust freely):
1. The question + the framing — what "opportunity" means, in one line
2. The funnel — many → few → one
3. The recommendation + quantified opportunity
4. Sensitivity & risk — what would change the answer *(dashboard link here)*
5. SWOT + limitations, deliberately airy with generous white space

Deliverable requires **≥2 visualizations that genuinely support** the recommendation —
not decoration.

---

## Phase 6 — Ship
🔧 Clean-kernel top-to-bottom run, export `.ipynb` + deck `.pdf`, verify the dashboard opens
standalone. Upload both to the Google Form in the notebook's final cell.

---

### Sequencing note
Phases 2–5 are all downstream of the Phase 1 framing. Locking the definition of opportunity
first prevents rework — and it's the part that carries the most grading weight, so it deserves
the most of the 4–5 hour budget.
