# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack
static HTML/CSS (owner, 2026-10-19): one self-contained folder under `site/`, no build step, no framework, so it pins to IPFS as-is under the IMD site label `bank` (bank.sites.imd.fun) and mirrors anywhere. Vote and claim UI live in the operator app (hoolibear/imd), not here.

## Users
- **Identity.md seat holders and the workers who run them** (about 2,000 seats, roughly 1,000 active agents). They meet this page from a link in the IMD community or the operator app. Job: understand what the swarm's shared pool is, why their seat is the vote, and go cast a signal vote in the operator app.
- **The IMD team and the wider crypto-literate public.** Job: judge whether the swarm should hold a seat-governed treasury, read the spec, and join the discussion. The page must persuade builders, not only members.

## Product Purpose
Swarm Bank is a seat-governed spending pool for the IMD swarm: fees flow in, registered agents spend within budgets, seat NFT holders decide anything larger, and a spend can be put to the swarm itself as an oracle question. The site presents that idea and asks for a first signal. Success at this stage = seat holders cast signal votes and the IMD team engages with the spec; no funds move.

## Positioning
The only treasury design where the voters are the swarm's own seats (one seat, one vote, with anti-whale rules) and where a spend can be approved by asking the swarm as an oracle question for 0.5 IMD. Agents spend; seats govern; no governance token.

## Operating Context
- Stage A (now): idea page, seat-verified signal votes in the operator app, a Safe as the pool, one founding oracle question. **No token at the start** (owner, 2026-10-19). The launch token and its 10% seat distribution are a later stage and must not be presented as live or promised.
- Stage B: contracts (Governor + Timelock + SeatVotes + AgentPool) replace the Safe. Stage C: oracle lane and per-agent budgets.
- Spec and decisions log: `docs/spec.md`, `docs/decisions.md` in this repo (github.com/swarmbank/bank, private as of 2026-10-19).
- IMD mechanics the page may state as fact: Intake payer = the address that called `request`; the payer earns 1% of launch-pool trades, delivered only when `claimFees` is called (permissionless, push payout 80/20); oracle questions cost 0.5 IMD and return an EIP-712 attestation from a panel.

## Capabilities and Constraints
- Static page: no wallet connection, no vote, no claim on this site. Actions link out to the operator app (vote) and to the spec (read).
- The site names and links no other project or token (owner, 2026-10-19): no SVO, no IMDO, no sovrn.one, no offsets.fun, no transaction links. Those facts stay in the internal spec only; the public spec rendering scrubs them (scripts/build-spec.py).
- Wording: "pool" or "treasury" for the mechanism; "Swarm Bank" is the project name only. Never "bank" as a claim of custody or deposits. No yield, APY, returns, or price language. No promise about a token.
- Facts that stay true: 0.5 IMD per oracle question / per job; one member per panel seat; seats are transferable NFTs; a 1% launch-pool share is small unless volume is real (SVO: about $22 since launch).
- Undecided: pair asset, caps, quorum, panel size (spec section 8). The page shows these as proposals, not settled numbers.

## Brand Commitments
- Name: **Swarm Bank**. Org: `swarmbank`. Future host: bank.sites.imd.fun. No logo, mark, imagery or colour exists yet (owner, 2026-10-19); the site establishes the identity.
- Voice: plain, factual, builder-to-builder. Numbers over adjectives.

## Evidence on Hand
- SVO launch 1205 fee claim, 2026-10-19, tx `0xb1e2a961688884b96738077a489c6bac8f436f17d96e1616019a6660f61b328e` on Robinhood (4663): 2.1289 IMD + 215,071 SVO pushed to the payer, 20% to IMD, by a permissionless call. Real, verifiable.
- IMD docs on the Intake/oracle mechanics (quoted in `docs/spec.md` section 2).
- No testimonials, no endorsements, no customers, no benchmarks. Do not fabricate any. The IMD team has not endorsed this.

## Product Principles
1. Seats govern; agents spend; nobody holds a key for anyone else.
2. Every number on the page is either on chain or labelled a proposal.
3. Make concentration slow and visible rather than claiming to make it impossible.
4. Ask for one small action now (a signal), never for funds.
5. The swarm builds and pays for its own bank, by vote.
