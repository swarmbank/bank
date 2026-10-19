---
name: Swarm Bank
description: A seat-governed pool for the IMD swarm, drawn as Isotype pictorial statistics on white paper.
colors:
  paper: "#ffffff"
  ink: "#111111"
  ink-2: "#5b5b5b"
  ink-3: "#8c8c8c"
  isotype-red: "#d12d1f"
  isotype-red-pressed: "#b1261a"
  isotype-blue: "#1f5fa8"
  isotype-green: "#2f8f4e"
  rule: "#111111"
typography:
  display:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "clamp(1.5rem, 2.6vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.015em"
  headline:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "clamp(1.35rem, 2.2vw, 2rem)"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "clamp(1.1rem, 1.6vw, 1.5rem)"
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: "-0.005em"
  body:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
    fontFeature: "tabular-nums"
  note:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Jost, system-ui, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 700
    lineHeight: 1.35
    letterSpacing: "0.08em"
rounded:
  none: "0px"
spacing:
  gap: "clamp(2px, 0.35vw, 5px)"
  caption-col: "24px"
  row-y: "9px 0 8px"
  pad: "clamp(16px, 4vw, 56px)"
  stage: "16px 24px 22px"
  fig: "clamp(12px, 1.32vw, 19px)"
  coin: "clamp(16px, 1.8vw, 26px)"
  maxw: "1440px"
components:
  action-bar:
    backgroundColor: "{colors.isotype-red}"
    textColor: "{colors.paper}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
    padding: "14px 20px"
  action-bar-hover:
    backgroundColor: "{colors.isotype-red-pressed}"
    textColor: "{colors.paper}"
  text-link:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.note}"
  text-link-hover:
    textColor: "{colors.isotype-red}"
  row-caption:
    textColor: "{colors.ink}"
    typography: "{typography.label}"
  row-note:
    textColor: "{colors.ink-2}"
    typography: "{typography.note}"
  stage-cell:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    padding: "{spacing.stage}"
---

# Design System: Swarm Bank

## Overview

**Creative North Star: "The Isotype Ledger"**

Swarm Bank is drawn the way Otto Neurath and Gerd Arntz drew social statistics: every quantity on the page is a countable row of pictograms on white paper, so a visitor sees who votes, what came in and what went out before reading a number. One figure is ten seats; one coin is one IMD. Figures stand in groups of ten with a wider gap after each group, rows flow inline like a line of text, and a small uppercase caption sits in a left column beside each row. Hairline black rules separate rows; a heavier rule marks the masthead, the action and the footer.

The material is print, not screen: black ink on white, three named colour inks each with one job, no cards, no shadows, no gradients, no icons beyond the authored pictogram set. Type is one geometric sans (Jost, self-hosted variable) in three weights with tabular numerals, because the page is a table that happens to be read like prose. The build refused the DAO-treasury landing (dark ground, hero metric, two buttons, feature cards); nothing here floats, glows or stacks.

Motion is one clock: when a row enters the viewport its figures appear one after another on a 9ms stagger with an exponential ease-out. That is the only animation on the site and it is skipped for reduced-motion users and for `?static=1`.

**Key Characteristics:**
- Every number is first drawn as a countable row (figures in tens, coins one-to-one), then stated in words in a note beneath.
- White ground, black figures; red, blue and green inks each mean one thing.
- Hairline black rules are the only structure: no boxes, borders-as-cards, shadows or fills.
- One sans (Jost 400 / 500 / 700), tabular figures, uppercase tracked captions set small at the left.
- Rows and lists share one two-column grid (caption column + content) that collapses to one column at 760px.
- One action: a full-width red bar with a plain text link at its right.

## Colors

Black ink on white paper, with the three Isotype inks (red, blue, green) each assigned a single meaning.

### Primary
- **Isotype Red** (`{colors.isotype-red}`): money leaving the pool (the OUT row's coins, the `.red` row) and the one action (the full-width bar, link hover, selection, focus ring, the "now" stage caption, the `.ink-red` emphasis in notes). **Pressed Red** (`{colors.isotype-red-pressed}`) is the action bar's hover fill only.

### Secondary
- **Isotype Blue** (`{colors.isotype-blue}`): money arriving in the pool (the IN row's coins; any `.blue` group).

### Tertiary
- **Isotype Green** (`{colors.isotype-green}`): reserved for the pool held. Defined on `:root`; no element draws it yet.

### Neutral
- **Paper** (`{colors.paper}`): the only ground. Forced white in both colour schemes (dark mode is explicitly disabled; there is no dark variant).
- **Ink** (`{colors.ink}`): body text, headings, black figures (wallets with one seat), outlined "open" figures in notes.
- **Ink 2** (`{colors.ink-2}`): dark-grey figures (wallets with 2 to 5 seats), subheads, row notes, the masthead line, footer.
- **Ink 3** (`{colors.ink-3}`): light-grey figures (wallets with 6 to 19 seats), open/greyed seats, dimmed figures in rule illustrations.
- **Rule** (`{colors.rule}`): every rule. Hairline (1px) between rows; 2px under the masthead, above the action bar, above the footer and under spec table heads.

### Named Rules
**The One-Job Ink Rule.** Each colour means one thing: black is seats and print, grey tiers are holder size, red is money out and the single action, blue is money in, green is the pool held. A colour is never used for decoration or a second meaning.

**The Grey-Is-Size Rule.** Seat figures are tiered by holder size, darkest for the smallest holder (ink → ink-2 → ink-3); wallets over the proposed cap are drawn as outlined figures (`#p-seat-open`), not another fill.

## Typography

**Display Font:** Jost (with system-ui, sans-serif)
**Body Font:** Jost (same family; self-hosted variable `fonts/jost.woff2`, 100–900, `font-display: swap`)
**Label/Mono Font:** none on the site; the Read page's code blocks use `ui-monospace, "SF Mono", Menlo, monospace`

**Character:** One geometric sans at three weights (400 body, 500 emphasis and links, 700 headings and captions). Numerals are tabular everywhere (`font-variant-numeric: tabular-nums` on `body`), so counts in notes line up with the figures above them. `em` renders as weight 500 upright, never italic; `code` inherits the body font at weight 500.

### Hierarchy
- **Display** (700, `clamp(1.5rem, 2.6vw, 2.5rem)`, 1.1, -0.015em): the one h1, held to one line at desktop; `max-width: 40ch`, balanced wrap.
- **Headline** (700, `clamp(1.35rem, 2.2vw, 2rem)`, 1.15, -0.01em): section heads (`.sec-h`, `.prose h2`, the close); 34px above, 8px below.
- **Title** (700, `clamp(1.1rem, 1.6vw, 1.5rem)`, -0.005em): the action bar's text; its sub-line is 0.85rem at weight 500.
- **Body** (400, 17px, 1.5; 19px at ≥1200px): prose in a 70ch measure; lead sub-line 96ch in ink-2.
- **Note** (400, 0.95rem, 1.5, ink-2): the sentence beneath a pictogram row (110ch max; inline notes 72ch); `strong` inside returns to ink.
- **Label** (700, 0.8rem, 1.35, 0.08em, UPPERCASE): row captions and stage captions in the left column. A caption's `small` sub-line is 0.82rem, weight 500, sentence case, ink-2.
- **Masthead** (700 wordmark at 0.95rem, 0.02em, uppercase; nav 0.95rem): the only other uppercase on the page.

### Named Rules
**The Tabular Rule.** Numerals are tabular everywhere. Counts are never typeset in a display size; the drawn row is the display, the number is a note.

**The Three-Weight Rule.** Jost at 400, 500 and 700 only. Emphasis is weight, never italic (`em` is upright 500).

## Layout

The page is a single column of ruled rows inside a 1440px container (`--maxw`) with side padding `clamp(16px, 4vw, 56px)` (`--pad`) on masthead, main and footer alike. The masthead is a three-column grid (wordmark, line, nav) aligned on the baseline under a 2px rule.

Every data row and every rule-list item uses the same two-column grid: a caption column `minmax(150px, 190px)` and a `1fr` content column with a 24px gutter, 9px/8px vertical padding, a 1px rule on top. Notes sit in the content column (`grid-column: 2`). Pictogram groups flow inline inside the content column: figures are `--fig` wide (`clamp(12px, 1.32vw, 19px)`) and twice as tall; coins are `--coin` square (`clamp(16px, 1.8vw, 26px)`; "small" coins 62% of that); the gap between figures is `--gap` (`clamp(2px, .35vw, 5px)`), and every tenth figure takes four gaps on its right. Figure rows reserve two figure heights so an empty row still holds its line.

Stages are three equal hairline columns (`repeat(3, 1fr)`, a 1px rule above, 1px rules between, `16px 24px 22px` padding, 40ch copy). The action row is a 2px rule with a flex bar: the red bar grows (`flex: 1 1 420px`) and the text link sits after it at the right. Prose runs at 70ch; the close heading at 28ch.

At ≤760px: the masthead stacks; every two-column row collapses to one column with an 8px row gap and the note returns to column 1; figures fix at 12px, coins at 16px (small coins 11px), gaps at 2px; the stages stack with rules between; the action bar stacks its two lines; hover labels may wrap to 70vw.

**The Read page** (`spec.html`, `spec.css` layered on the same stylesheet): the main column widens to 1240px so tables can breathe; text blocks stay at 80ch (paragraphs and list items 72ch); h2s carry a 2px rule above with 40px/10px margins; tables are full width with hairline row rules, a 2px rule under uppercase tracked heads (0.78rem, 0.08em), first column 16%, second 46%; code blocks sit on a 5% ink tint; blockquotes carry a 1px left rule in ink-2. Tables scroll horizontally on phones.

## Elevation & Depth

None. There are no shadows, no gradients, no tonal surfaces and no stacking: the only ground is white paper and the only structure is black rules (1px between rows, 2px at the masthead, action and footer). Hierarchy comes from rule weight, ink tier and figure size. The hover count label is paper on paper with a 2px top rule in the group's own ink; it reads as a printed annotation, not a tooltip.

### Named Rules
**The Flat Print Rule.** Nothing casts, floats or layers. If an element needs separating, it gets a rule, never a box.

## Shapes

Square corners everywhere (radius 0 on the bar, the hover label, the spec code block). Pictograms are the only curves: the seat figure (circle head, one-piece body on a 20×40 viewBox), the coin (concentric rings, 40×40, the middle ring filled with paper so it reads on any ink), the open seat (same figure outlined at 2px stroke). All symbols are authored inline `<svg><symbol>` definitions (`#p-seat`, `#p-seat-open`, `#p-coin`, `#p-coin-half`, `#p-coin-out`, `#p-grid100`) and fill `currentColor`, so ink is assigned by the group's class, never by the symbol. A fractional coin is the full coin clipped from the right with `clip-path: inset(0 calc(100% - var(--frac) * 100%) 0 0)`. Links underline at 1.5px with a 0.18em offset; the action bar is a hard rectangle.

## Components

### Buttons
- **Shape:** hard rectangle (0 radius), full width of the action row (`flex: 1 1 420px`).
- **Primary (the action bar):** Isotype red fill, white text, `14px 20px`, Title size at 700; text at the left and a 0.85rem/500 sub-line at the right (`justify-content: space-between`, baseline aligned). There is exactly one of these per view, repeated once at the close.
- **Hover / Focus:** fill shifts to pressed red (`{colors.isotype-red-pressed}`) and the bar lifts 1px (`translateY(-1px)`, 0.15s, `cubic-bezier(.2,.9,.3,1)`); active returns to 0. Focus is the global ring: 3px solid red, 3px offset.
- **Text link ("Read the spec"):** ink at weight 500, underlined, turns red on hover; it sits at the right end of the action row, never in a second bar.

### Links
- Inherit ink, 1.5px underline at 0.18em offset, red on hover. Masthead nav links have no underline until hover; the wordmark stays ink on hover.

### Browser surfaces
- Selection is red with white text (`--sel`); `:focus-visible` is a 3px red outline offset 3px (figure groups offset 6px). Smooth scrolling for in-page anchors.

### Navigation (masthead)
- A baseline-aligned three-column grid under a 2px rule: uppercase 700 wordmark with the seat figure at 11×22, an ink-2 masthead line whose `em` is red, and a plain 0.95rem nav with 20px gaps. Stacks to one column at ≤760px.

### Pictogram row (signature)
Caption at left (Label), figures at right, hairline rule above. `main.js` draws each `.grp` from its `data-n` count (`#p-seat` by default, `#p-seat-open` for `.g-open`/`.g-open-ink`, `#p-coin` for coin rows), stamps `--i` on every figure for the stagger, and makes the group a focusable `role="img"` with `aria-label` from `data-label`. Ink by class: `.g-1` ink, `.g-2` ink-2, `.g-3` ink-3, `.g-open` ink-3, `.g-whale` ink; a `.red` row or `.blue` group/row recolours its coins. Every tenth figure takes a four-gap right margin. On hover or focus-within the group's `data-label` count appears as a paper label with a 2px top rule in the group's ink, 0.78rem/500, fading in over 0.18s. An `.empty` row keeps its rule and caption with no minimum height.

### Rule illustrations
- `.rules` is a hairline-ruled list on the same two-column grid; the left cell holds a small figure drawing (`.rule-fig`, figures at 0.9 `--fig`, dimmed ones in ink-3, plus the `#p-grid100` hundred-grid, a lock and a square-root figure), the right cell a bold term and a 72ch sentence.

### Stages
- Three hairline columns, uppercase Label caption with a sentence-case sub-line, 40ch body; the current stage's caption and sub-line are red.

### Spec tables (Read page)
- Full width, hairline row rules, uppercase tracked heads over a 2px rule, 0.92rem body; no zebra, no borders on the sides.

### Reveal (motion)
- Under `prefers-reduced-motion: no-preference`, figures in a row not yet `.on` sit at opacity 0 and 4px down; when the IntersectionObserver (bottom margin -8%) marks the row `.on`, each figure transitions opacity and transform over 0.32s with `cubic-bezier(.16,1,.3,1)` and a delay of `var(--i) * 9ms`. Reduced motion, `?static=1`, a missing IntersectionObserver, and empty rows all render immediately.

## Do's and Don'ts

### Do:
- **Do** draw a quantity before stating it: a row of pictograms (one figure = ten seats, one coin = one IMD), then a note in ink-2 with the number in tabular figures.
- **Do** group figures in tens with a four-gap break after every tenth, and let rows wrap inline like text.
- **Do** put the caption in the left column, uppercase 0.8rem tracked 0.08em, and open each row with a 1px rule.
- **Do** keep the three inks to their jobs: red = money out and the one action, blue = money in, green = pool held, greys = holder size.
- **Do** use Jost at 400 / 500 / 700 only, with tabular numerals, and keep the h1 to one line at desktop.
- **Do** run every reveal on the shared clock (`--i` × 9ms, 0.32s, exponential ease-out) and honour reduced motion and `?static=1`.
- **Do** keep one red action bar per view with the secondary action as a plain text link at its right.

### Don't:
- **Don't** add cards, shadows, gradients, tinted panels or a dark ground; the only surface is white paper and the only structure is black rules.
- **Don't** introduce icons outside the authored pictogram set, or an icon font, or raster logos.
- **Don't** typeset a number as a hero metric or stat strip; the drawn row is the display.
- **Don't** use red, blue or green for emphasis or decoration, or give one ink a second meaning.
- **Don't** italicise; emphasis is weight 500 upright.
- **Don't** add a second button style; secondary actions are text links.
- **Don't** assign ink inside a symbol; pictograms fill `currentColor` and take their ink from the group's class.
