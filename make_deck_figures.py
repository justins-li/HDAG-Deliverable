"""Render dark-theme figures for the slide deck.

The notebook renders light figures, which is right for a notebook. The deck runs
on a dark ground, so the same charts are re-rendered here from the same source
data with a dark palette. Run after the notebook, before re-rendering the deck:

    python make_deck_figures.py
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

WINDOW = [10, 11, 12]
KEY = ['usg_apt', 'fg_apt']
REC = ('JFK', 'MAN')

# palette: validated for a dark surface (lightness band, chroma, contrast all pass;
# the amber/green CVD pair sits in the warn band and is covered by direct labels)
CYAN, VIOLET, GREEN, AMBER = '#2e9ed4', '#8257e3', '#1f9e72', '#bd8a34'
INK, MUTED, GRID, DOT = '#e6edfb', '#93a9cf', '#1e3766', '#3d5c96'

departures = pd.read_csv('f24-hdag-data/International_Report_Departures.csv')
passengers = pd.read_csv('f24-hdag-data/International_Report_Passengers.csv')
d = departures[departures.Month.isin(WINDOW)]
p = passengers[passengers.Month.isin(WINDOW)]
rec = p[p.Year.between(2015, 2019)]
pri = p[p.Year.between(2010, 2014)]

routes = pd.DataFrame(index=rec.groupby(KEY).Total.sum().index)
routes['pax'] = rec.groupby(KEY).Total.sum()
routes['pax_sched'] = rec.groupby(KEY).Scheduled.sum()
routes['prior'] = pri.groupby(KEY).Total.sum()
routes['years'] = rec.groupby(KEY).Year.nunique()
routes['carriers'] = rec.groupby(KEY).carrier.nunique()
routes['deps'] = d[d.Year.between(2015, 2019)].groupby(KEY).Total.sum()
routes = routes.fillna({'prior': 0, 'deps': 0})
share = rec.groupby(KEY + ['carrier']).Total.sum()
routes['hhi'] = ((share / share.groupby(KEY).transform('sum')) ** 2).groupby(KEY).sum()
routes['sched_share'] = routes.pax_sched / routes.pax.replace(0, np.nan)
routes['growth'] = (routes.pax - routes.prior) / routes.prior.replace(0, np.nan)
routes['strain'] = routes.pax / routes.deps.replace(0, np.nan)
routes['room'] = 1 - routes.hhi

stage = routes[(routes.pax >= 50_000) & (routes.years == 5) &
               (routes.sched_share >= .80) & (routes.deps > 0)]
stage = stage[stage.pax < stage.pax.quantile(.90)]
stage = stage[stage.growth > 0]
cand = stage[(stage.carriers >= 2) & (stage.hhi <= .90)].copy()
for dial, col in [('D', 'pax'), ('G', 'growth'), ('S', 'strain'), ('R', 'room')]:
    cand[dial] = cand[col].rank(pct=True) * 100
cand['TAI'] = cand[['D', 'G', 'S', 'R']].mean(axis=1)
shortlist = cand.nlargest(5, 'TAI')


def style(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUTED, length=0, labelsize=9)
    ax.set_facecolor('none')


# Figure A. the capacity gap
hist = p[(p.usg_apt == REC[0]) & (p.fg_apt == REC[1])]
hdep = d[(d.usg_apt == REC[0]) & (d.fg_apt == REC[1])]
by_carrier = (hist[hist.Year >= 2014]
              .pivot_table(index='Year', columns='carrier', values='Total', aggfunc='sum')
              .fillna(0).astype(int))
pax18 = hist[hist.Year == 2018].Total.sum()
pax19 = hist[hist.Year == 2019].Total.sum()
GAP = pax18 - pax19

fig, ax = plt.subplots(figsize=(7.6, 4.0))
fig.patch.set_alpha(0)
cols = [c for c in ['VS', 'MT', 'AA', 'DL'] if c in by_carrier.columns]
colmap = {'VS': CYAN, 'MT': VIOLET, 'AA': GREEN, 'DL': AMBER}
bottom = np.zeros(len(by_carrier))
for c in cols:
    v = by_carrier[c].values
    ax.bar(by_carrier.index, v, .64, bottom=bottom, label=c, color=colmap[c],
           zorder=3, linewidth=1.4, edgecolor='#0a1f4d')
    for x, (b, h) in enumerate(zip(bottom, v)):
        if h > 12000:
            ax.text(by_carrier.index[x], b + h / 2, f'{c}\n{h/1000:,.0f}k', ha='center',
                    va='center', fontsize=8, color='white', weight='bold', zorder=4)
    bottom += v
ax.set_ylim(0, pax18 * 1.42)
ax.axhline(pax18, color=MUTED, ls=(0, (4, 3)), lw=1, zorder=2)
ax.text(by_carrier.index.max() + .45, pax18 * 1.012, '2018 peak', va='bottom', ha='right',
        fontsize=8.5, color=MUTED)
ax.annotate(f'Thomas Cook exits\n{GAP:,} Q4 passengers unserved',
            xy=(2019, pax19 * 1.03), xytext=(2015.6, pax18 * 1.30),
            fontsize=9.5, color=INK,
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2,
                            connectionstyle='arc3,rad=-.15'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v/1000:,.0f}k' if v else '0'))
ax.set_ylabel('Q4 passengers', fontsize=9.5, color=MUTED)
ax.legend(frameon=False, fontsize=9, ncol=4, loc='upper left',
          bbox_to_anchor=(0, -0.06), labelcolor=MUTED)
ax.grid(axis='y', color=GRID, lw=.8, zorder=0)
ax.set_axisbelow(True)
style(ax)
plt.tight_layout()
plt.savefig('deck_fig_gap.png', dpi=200, transparent=True)
plt.close()

# Figure B. strain against room
fig, ax = plt.subplots(figsize=(7.0, 4.0))
fig.patch.set_alpha(0)
ax.scatter(cand.room, cand.strain, s=17, color=DOT, zorder=2,
           label=f'{len(cand)} contestable routes')
OFFSET = {('JFK', 'MAN'): (11, 6, 'left'), ('LAX', 'HND'): (-11, 7, 'right'),
          ('SEA', 'ICN'): (-11, -3, 'right'), ('DEN', 'CUN'): (-11, -3, 'right'),
          ('GUM', 'PUS'): (11, -3, 'left')}
for idx, r in shortlist.iterrows():
    is_rec = idx == REC
    ax.scatter(r.room, r.strain, s=150 if is_rec else 70,
               color=VIOLET if is_rec else CYAN, zorder=4,
               edgecolor='#0a1f4d', linewidth=1.6)
    dx, dy, ha = OFFSET.get(idx, (10, 4, 'left'))
    ax.annotate(f'{idx[0]}–{idx[1]}', (r.room, r.strain), textcoords='offset points',
                xytext=(dx, dy), ha=ha, fontsize=9, zorder=5,
                color=INK if is_rec else MUTED,
                weight='bold' if is_rec else 'normal')
ax.set_xlim(right=cand.room.max() + .06)
ax.set_xlabel('Room to enter   (1 − HHI)  →', fontsize=9.5, color=MUTED)
ax.set_ylabel('Strain  (pax per departure)  →', fontsize=9.5, color=MUTED)
ax.legend(frameon=False, fontsize=9, labelcolor=MUTED, loc='lower left')
ax.grid(color=GRID, lw=.8, zorder=0)
ax.set_axisbelow(True)
style(ax)
plt.tight_layout()
plt.savefig('deck_fig_scatter.png', dpi=200, transparent=True)
plt.close()

print('wrote deck_fig_gap.png and deck_fig_scatter.png')
print(f'  gap {GAP:,} | 2018 {pax18:,} | 2019 {pax19:,}')
print(f'  shortlist: {[f"{a}-{b}" for a, b in shortlist.index]}')
