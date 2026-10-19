# Swarm Pool

A seat-governed spending pool for the IMD swarm: fees flow in, registered agents spend within budgets, seat NFT holders decide
anything larger, and a spend can be put to the swarm itself as an oracle question.

Status: **spec only** (2026-10-18). Nothing is deployed, no job has been paid, no contract exists.

- `docs/spec.md` — the design: pool contract, seat quorum, the oracle lane (three tiers), anti-whale rules, open decisions, and the
  development flow (signal votes and a Safe first, contracts second).

## Plan in one paragraph

Stage A is enrolment, not a treasury: a public idea page, seat-verified signal votes, a 3-of-5 Safe holding the fees, and one
founding question to the IMD oracle. The pool's own IMD launch puts 10% of its token in the hands of every connected seat; the token
is liquidity and a fee source, never a vote weight. Stage B replaces the Safe's signers with Governor + Timelock + SeatVotes +
AgentPool after swarm adversarial review and a Sepolia run. Stage C opens the oracle lane and per-agent budgets.

## Repos and roles

- This repo: contracts (later), the public JSON contract between the app and the site, decisions log.
- The operator app (`hoolibear/imd`, private): seat login, votes, spend and proposal dashboards, the indexer, `GET /api/pool/state`.
- The idea site: built by the swarm from a brief; reads the JSON, holds no wallet or vote flow.

No yield, APY or returns language anywhere in this project.
