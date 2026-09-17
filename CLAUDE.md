# CLAUDE.md: working notes ("soul document")

**Read this before touching the deliverable.**

This file is for me. It is the standing context for this project: what is being built, what the
data will and won't support, and what has already been settled so it doesn't get re-derived or
quietly contradicted two sessions from now.

---

## 1. The project

Route network strategy for **Meridian Air**, a mid-sized international airline. After two
profitable years the board has funded **exactly one** new US↔international route, one aircraft
rotation's worth of capacity. The question is which route, and what the case for it is.

The client has been explicit: **do not recommend the biggest markets.** They already know the
large US↔international routes exist, and they know those are held by incumbents with cost and
slot advantages Meridian cannot match. What they want is a route where the historical record
shows real, *capturable* opportunity, together with an honest account of the risks of being
wrong.

**What ships:** the notebook (the single `.ipynb` at the repo root), running clean top to
bottom, plus a **five-slide** PDF deck. The dashboard and the deck both hang off the notebook,
so the notebook is the entry point to everything else.

## 2. How the work gets decided

Justin is the last mirror: the final reader of what the data says and the one who carries the
conclusions forward and answers for them.

So: build and decide. Pick the framing, choose the weights, commit to a route, write the
narrative. Where a call is genuinely contestable, make it anyway and say plainly what would
overturn it. That is more useful to him than an unresolved option set, and it is the part he
can actually push back on.

What makes this work good, roughly in order:

1. **The framing.** There is no given target variable. Deciding what "opportunity" means, and
   defending it, is the substance. Everything downstream is mechanics.
2. **Honest reasoning.** Be specific about what the data cannot say. A limitation that names a
   real consequence beats a vague one.
3. **Support.** The recommendation has to follow from what was actually computed, not from what
   sounds good. If the index ranks something else first, say so and explain the override.
4. **Clarity**, then **code quality**. In that order. The thinking is the product.

## 3. Absolute rules

1. **Never invent a number.** Every figure in the notebook, dashboard or deck must trace to a
   computation over the provided CSVs, or to a cited external source with a URL.
2. **No placeholder or illustrative data.** If a number isn't computed yet, leave it blank and
   say so.
3. **Leave the notebook's original prompt cells intact:** the title, the problem statement, the
   data description, the Part 1/2/3 headers, the assumptions heading and the closing section.
   Don't delete or reword them; add cells around them freely.
4. **The notebook must run top to bottom** from a clean kernel.
5. Cite any external dataset inline with its source and retrieval date.

## 4. Data facts established (do not re-derive, do not contradict)

Source: USDOT T-100 International Report, via `https://github.com/AnmayG/f24-hdag-data`
(that repo also holds unrelated course datasets, so ignore all but the two `International_Report_*`
files).

- Both files: **250,000 rows**, 16 columns, **1990–2019**.
- `Scheduled + Charter == Total` holds exactly in both files.
- `carriergroup` ∈ {0, 1}. 0 is foreign carriers, 1 is US carriers.
- `type` is constant per file ("Departures" / "Passengers").
- `carrier` has nulls: 708 (departures), 947 (passengers).
- Grain is confirmed: zero duplicate keys on Year · Month · `usg_apt` · `fg_apt` · `carrier`.

### ⚠ The critical finding: these are NOT full years

Each year holds only the final months of that year, and **the window shifts mid-series**:

| File | 1990–2002 | 2003–2010 | 2011–2019 |
|---|---|---|---|
| **Passengers** | Sep–Dec (4 mo) | Aug–Dec (5 mo) | Aug–Dec (5 mo) |
| **Departures** | Oct–Dec (3 mo) | Oct–Dec (3 mo) | Sep–Dec (4 mo) |

Consequences that have to be handled explicitly:

1. **Q4 seasonal bias.** The summer peak is entirely absent. Summer-peaking routes
   (Mediterranean leisure, Alaska) are structurally undercounted; winter-peaking routes
   (Caribbean, Southern Hemisphere) are over-represented relative to true annual demand.
2. **Step artifacts in any year-over-year series.** Passengers gain a month at 2003; departures
   gain a month at 2011. Naive YoY growth shows a spurious jump at those breakpoints. Fix by
   normalising per month or restricting to a constant window.
3. **The two files do not share a month window.** Any load-factor style metric
   (passengers ÷ departures) computed by a naive join is wrong. The intersection is **Oct–Dec
   for 1990–2010, Sep–Dec for 2011–2019**.
4. Totals are therefore **not annual totals.** 2019 "total passengers" here is 99.5M against a
   true US international figure several times that. Never present these as annual volumes
   without the caveat.

**The working choice:** everything runs on a forced constant **Oct–Dec** window, the one window
present in both files in every year, which removes the step artifacts and makes the two files
joinable. It costs the summer peak, which is a real and stated limitation.

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
| Thomas Cook (`MT`) 2018 share | 38,749 pax = 47% of route; absent in 2019 |
| Unserved Q4 demand | **26,235 passengers** |
| Equivalent capacity | 76 departures / 92 days = **0.83 per day ≈ one rotation** |

**TAI ranks LAX–HND first; JFK–MAN second.** LAX–HND is rejected *by hand* because Haneda's US
slots are allocated government-to-government, a barrier "Room" cannot see, since it measures
concentration only. **Never present JFK–MAN as the top-scoring route.** It ranks #1 only under
Strain-led, Room-led or capturability-led weightings; #2 on equal weights; **#24 size-led.**
That fragility is the sensitivity story, not something to hide.

Two further traps worth keeping: five-year HHI says JFK–MAN has room = 0.70, but its **2019 HHI
is 1.00** (Virgin Atlantic monopoly), so the route being entered is a monopoly today; and
`DY`/`DI` on LAX–LGW are both Norwegian Group, so HHI scores one airline as two competitors.

## 6. Working agreements

- Branch `claude/vigilant-feynman-o5i3eq`, PR #1.
- **Short, sweet and creative** over sprawling. One sharp idea executed well beats five
  half-ideas.
- Flag uncertainty rather than smoothing it over.
- Notebook cells merge badly. Git matches them by position, so a stale output can land on a
  cell whose source has since changed. Check outputs after any merge.
