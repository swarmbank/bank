---
version: 1
slug: "site-index-html"
primary_target: "site/index.html"
related_targets: ["site/spec.html"]
---

# Surface brief: site/index.html (bank.sites.imd.fun)

Scope: the one-page presentation site for Swarm Bank, plus `site/spec.html` (the spec rendered for reading). Visitor mode: Persuade.
Audience: identity.md seat holders and the workers who run them; the IMD team and crypto-literate builders.
Job: understand what a seat-governed pool is and why their seat is the vote. Action: cast a signal vote (operator app, `/pool`, Stage A) or read the spec. No funds, no token, no wallet on this site.
Proof: the SVO fee claim of 2026-10-19 (real tx), the live seat distribution read from the NFT (real), IMD's documented mechanics (0.5 IMD per question, permissionless fee claim). Everything undecided is labelled "proposed".
Constraints: static HTML/CSS, self-hosted fonts, no framework; "pool"/"treasury" for the mechanism, "Swarm Bank" as the name only; no yield/APY/returns/price language; no token promise; no endorsements.
Unresolved: the exact signal-vote URL (assumed https://offsets.fun/pool, opens with Stage A); pair asset, caps, quorum, panel size (spec §8).

## Direction contract

THESIS: The pool read as Isotype pictorial statistics: every quantity on the page is a countable row of pictograms (one figure = ten seats, one coin = one IMD), so a visitor sees who votes, what came in and what went out before reading a number. It refuses the DAO-treasury landing (dark ground, headline, two buttons, stats strip, feature cards) and the hero-metric template.

OWN-WORLD: White ground, black figures, and three named inks: Isotype red for money leaving and for the one action, Isotype blue for money arriving, Isotype green for the pool held. Authored SVG pictograms in the Gerd Arntz manner (seat figure, coin, crossed coin, question mark panel), one stroke weight, aligned on a strict row grid with hairline black rules. One geometric sans (Jost) in two weights, tabular figures, uppercase row captions set small to the left of each row. No cards, no shadows, no gradients, no icons but the pictogram set.

STORY: The visitor understands that the swarm's money would be governed by its seats, not a token; believes it because the seat distribution is drawn from the chain and the only fee ever claimed is printed with its hash; and does one thing: cast a signal vote, or read the spec.

FIRST VIEWPORT: Full-width chart at desktop: a small masthead line ("Swarm Bank — a seat-governed pool for the IMD swarm", proposal, not live) above three stacked pictogram rows filling the viewport: SEATS (2,000 as 200 figures, grouped in tens, wallets over the proposed cap greyed), IN (the SVO claim as coins, blue), OUT (nothing yet: an empty row with its rule and the caption "no spend has been proposed"). The primary action is a red full-width bar directly under the chart, "Cast a signal vote", with "Read the spec" as a text link at its right end. Signature interaction: rows fill figure by figure on one shared clock as they enter the viewport; hovering a figure group shows its count in the margin.

FORM: Isotype pictorial statistics (Otto Neurath, Gerd Arntz), position 1 on my ordered list; the roll assigned position 5 (the passbook) and the user chose the pick card. Seed key 09c9531a (direction, persuade). Code-led: `.impeccable/config.json` buildPath = code.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
