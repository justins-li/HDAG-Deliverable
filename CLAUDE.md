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

## 2. Ownership and grading

Justin is the final say on everything that ships, and will be asked to walk through any of it
live — so every claim in the notebook and the deck has to hold up when questioned out loud.

Build freely and decide: framing, scoring, the route, charts, dashboard, deck. Commit to a
call rather than staging a menu of options, and surface the judgment calls that are genuinely
worth revisiting rather than every fork in the road.

Grading priority, per the brief: (1) problem framing, (2) soundness and honesty of reasoning,
(3) recommendation actually supported by the work, (4) clarity, (5) code quality.
**Code quality is last** — the graded substance is the thinking.

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

## 5. Findings established (do not re-derive, do not contradict)

**Framing.** Opportunity = *demand that already exists, on planes that are already full, on a
route nobody owns.* Scored as the **Thin Air Index**: D (demand) · G (growth) · S (strain,
= pax ÷ departures) · R (room, = 1 − HHI), each a percentile rank within the candidate pool.

**Funnel.** 4,398 pairs → 873 material → 785 niche → 605 growing → 307 contestable → 5 → 1.

**Recommendation: JFK ⇄ MAN (Manchester).** Verified numbers, Oct–Dec window:

| | value |
|---|---|
| 2018 Q4 passengers / departures | 82,512 / 240 → 343.8 per departure |
| 2019 Q4 passengers / departures | 56,277 / 176 → 319.8 per departure |
| Thomas Cook (`MT`) 2018 share | 38,749 pax = 47% of route; absent 2019 |
| Unserved Q4 demand | **26,235 passengers** |
| Equivalent capacity | 76 departures / 92 days = **0.83 per day ≈ one rotation** |

**TAI ranks LAX–HND first; JFK–MAN second.** LAX–HND is rejected *by hand* because Haneda's
US slots are allocated government-to-government — a barrier "Room" cannot see, since it
measures concentration only. **Never present JFK–MAN as the top-scoring route.** It ranks #1
only under Strain-led, Room-led or capturability-led weightings; #2 equal; **#24 size-led**.
That fragility is the sensitivity story, not something to hide.

Two further traps already found, worth keeping: five-year HHI says JFK–MAN has room = 0.70,
but its **2019 HHI is 1.00** (Virgin Atlantic monopoly); and `DY`/`DI` on LAX–LGW are both
Norwegian Group, so HHI scores one airline as two competitors.

## 6. Working agreements

- Branch: `claude/vigilant-feynman-o5i3eq`. PR: justins-li/HDAG-Deliverable#1.
- Keep the solution **short, sweet and creative** over sprawling. Budget for the case is 4–5 hours.
- Prefer one sharp idea executed well to five half-ideas.
- Flag uncertainty rather than smoothing over it — honesty is graded directly.
