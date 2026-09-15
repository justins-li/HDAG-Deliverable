# CLAUDE.md — Project Guardrails ("soul document")

**Read this at the start of every prompt before touching the deliverable.**

---

## 1. What this project is

HDAG (Harvard Data Analytics Group) Case Team Analyst take-home. Client: **Meridian Air**,
a mid-sized international airline with budget for **exactly one** new US↔international route.

Deliverable = (a) `HDAG_Case_Team_Deliverable.ipynb` run top to bottom, (b) a **5-slide-max** PDF deck.
Due 9/15 9:00 AM. Submitted via the Google Form linked in the notebook's final cell.

The client has explicitly said: **do not recommend the biggest markets.** They want a niche route
where the historical record shows real, capturable opportunity, plus an honest account of the risks.

## 2. The AI policy — the hard constraint on this repo

Quoted verbatim from the case instructions (notebook cell 1):

> You **may** use generative AI to help write code. You **may not** use it to fabricate data,
> invent results, or generate an analysis you don't understand. You are responsible for every
> line you submit and **will be asked to explain any of it**, including why you made each choice.
> A polished answer you can't defend scores worse than a modest one you can.

### What this means operationally

| Claude does | Justin owns |
|---|---|
| Data loading, cleaning, validation, exploration code | The definition of "opportunity" and why |
| Scoring machinery once the criteria are chosen | Which criteria enter the score, and their weights |
| Charts, dashboard, deck scaffolding and rendering | The SWOT judgments |
| Surfacing evidence, options and trade-offs | The final route choice and the narrative |
| Sanity checks, reproducibility, refactors | Every sentence submitted as reasoning |

Rule of thumb: **Claude builds the instrument; Justin reads the dial and makes the call.**
If a prompt asks Claude to decide the framing or pick the route, Claude should push back and
surface options with trade-offs instead.

Grading priority, per the brief: (1) problem framing, (2) soundness and honesty of reasoning,
(3) recommendation actually supported by the work, (4) clarity, (5) code quality.
Note that **code quality is last** — the graded substance is the thinking.

## 3. Absolute rules

1. **Never invent a number.** Every figure in the notebook, dashboard or deck must trace to a
   computation over the provided CSVs, or to a cited external source with a URL.
2. **No placeholder/illustrative data.** If a number isn't computed yet, leave it blank and say so.
3. **Do not delete or reword the original instruction cells** (0–4, 7, 9, 11, 13, 15, 16).
   Add new cells around them freely.
4. **Notebook must run top to bottom** from a clean kernel.
5. Cite any external dataset inline with its source and retrieval date.

## 4. Data facts established (do not re-derive, do not contradict)

Source: USDOT T-100 International Report, via `https://github.com/AnmayG/f24-hdag-data`
(the repo also contains unrelated course datasets — ignore all but the two `International_Report_*` files).

- Both files: **250,000 rows**, 16 columns, **1990–2019**.
- `Scheduled + Charter == Total` holds exactly in both files.
- `carriergroup` ∈ {0, 1}. `type` is constant per file ("Departures" / "Passengers").
- `carrier` has nulls: 708 (departures), 947 (passengers).

### ⚠ The critical finding: these are NOT full years

Each year contains only the final months of the year, and **the window changes mid-series**:

| File | 1990–2002 | 2003–2010 | 2011–2019 |
|---|---|---|---|
| **Passengers** | Sep–Dec (4 mo) | Aug–Dec (5 mo) | Aug–Dec (5 mo) |
| **Departures** | Oct–Dec (3 mo) | Oct–Dec (3 mo) | Sep–Dec (4 mo) |

Consequences that must be handled explicitly:

1. **Q4 seasonal bias.** Summer peak is entirely absent. Summer-peaking routes (Mediterranean
   leisure, Alaska) are structurally undercounted; winter-peaking routes (Caribbean, Southern
   Hemisphere) are over-represented relative to true annual demand.
2. **Step artifacts in any year-over-year series.** Passengers gain a month at 2003;
   departures gain a month at 2011. Naive YoY growth shows a spurious jump at those breakpoints.
   Fix by normalizing per-month or restricting to a constant month window.
3. **The two files do not share a month window.** Any load-factor style metric
   (passengers ÷ departures) computed by a naive join is wrong. Restrict to the month
   intersection first: **Oct–Dec for 1990–2010, Sep–Dec for 2011–2019.**
4. Totals are therefore **not** annual totals. 2019 "total passengers" in this file is
   99.5M against a true US international figure several times that. Never present these as
   annual volumes without the caveat.

These are real, specific limitations — exactly what the brief asks for
("the data could be cleaner" is explicitly called out as not good enough).

## 5. Working agreements

- Branch: `claude/vigilant-feynman-o5i3eq`. PR: justins-li/HDAG-Deliverable#1.
- Keep the solution **short, sweet and creative** over sprawling. Budget for the case is 4–5 hours.
- Prefer one sharp idea executed well to five half-ideas.
- Flag uncertainty rather than smoothing over it — honesty is graded directly.
