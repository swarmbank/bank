# Swarm Bank — spec (was: TODO — Swarm spending pool)

Status: **spec only, nothing built, no owner go-ahead to build** (CLAUDE.md: no building without explicit consent). Written 2026-10-18
from a chat on 2026-10-15 (the owner's three questions and the answers given then; nothing was written at the time).
Every choice marked **OPEN** is a recommended default, not an owner decision. Sections 4b (oracle lane) and 10 (development flow) added 2026-10-18 after the owner asked for proposals as swarm questions. Settle section 8 before any build.

## 1. What and why

A "central bank" for the IMD swarm: one contract that fees flow INTO and that registered agents can spend FROM, with the
swarm's seat NFTs deciding anything large. The owner's framing, in order:

1. "A spending pool fees could flow into, and that agents could spend from."
2. "Make it require a quorum of votes by the swarm NFTs."
3. "There are over 1000 active agents. Prevent the wallets that hold 20–40 seats from having control."

IMD's docs (imd.fun/docs, read 2026-10-15, about 70% of the page; the oracle section and tail were cut off) have no native pool,
vault or seat-voting feature. All of this is a custom contract set, launched through IMD's own job flow.

## 2. Facts to build on (read 2026-10-15 / 2026-10-18)

| Fact | Where | Why it matters |
|---|---|---|
| The **payer** is whoever calls Intake `request`; a smart contract can be the payer. | imd.fun/docs | A contract can own a project and its fee stream. |
| The payer gets **1%** of every trade on a launched pool; the network gets 0.25%. (IMD's own sources disagree on hook launches: see `docs/offsets-swarm-brief.md` "Pool fee".) | imd.fun/docs | The pool contract as payer receives fees with no relay step. |
| Only the payer can **continue** a project (`job.continue`, 0.5 IMD per version). | imd.fun/docs | Upgrades of the pool's own project route through the pool, so through governance. |
| Quotes last 600 s, **no refunds**; a refused job body is a spent payment. | imd.fun/docs | Per-agent loss caps per epoch. |
| The HTTP x402 flow needs a wallet signature; a contract payer uses the on-chain Intake path. | imd.fun/docs | `buyJob()` in the pool must call Intake, not x402. |
| Seat NFT `0x0000eC93127BAA929E58E97dd0095A2BFb38ec1D`, ids 0..1999, `ownerOf` readable; **not known** to be ERC721Votes or enumerable. | `seat-owners.mjs`, `seat-claim.mjs` | Snapshot voting may need a wrapper (section 4). |
| This app already reads `ownerOf` for all 2,000 seats every 5 min (5 Multicall3 requests). | `seat-owners.mjs` `refreshSeatOwners` | The seat distribution (section 7, step 1) is one script over that map. |
| ~1,038 seats have metered runs on the ledger; the owner says over 1,000 active agents. | `regen-data.mjs`, owner | Quorum must assume many inactive seats. |
| An **ERC-8004 adapter** binds a seat to an agent id (docs mention). | imd.fun/docs | Possible source for "active agent" weighting. |
| `oracle.request` returns a signed EIP-712 attestation (panel + quorum), 0.5 IMD per answer. | imd.fun/docs | An optional second chamber; not for primary treasury control. |
| **Oracle request body** (`oracle.request`, "Ask the oracle"): `question` ≤ 2,000 chars, `answerType` bool/address/bytes32/uint256/address[]/bytes32[], `panelSize` 2..100 (`/requests/check` enforces ≥ 5), `quorum` 2..panelSize (refused `quorum_unreachable` if above the seats that took work in the last 24 h), `validForSeconds` 60..2,592,000, `evidence: "panel"` for judgment questions, `definitions`, `guards` (allow/deny/mustHaveCode/min/max), `consumer {chainId, verifyingContract}`, `allowAmbiguous` (the wording screen refuses questions with more than one reading). | imd.fun/docs, 2026-10-18 | A spend proposal fits: a `bool` question with `evidence: "panel"`. |
| **Oracle price:** 0.5 IMD buys "the question and its panel, not an answer"; a panel that disagrees ends without one. Answers arrive "minutes to days". | imd.fun/docs | Same price for a panel of 5 or 100. |
| **Attestation:** EIP-712 domain `{"IdentityMD Oracle", "2", chainId, verifyingContract = consumer}`; struct `OracleAttestation(requestId, chainId, questionHash, answerType, answer, figure, fromBlock, toBlock, blockHash, panelJobId, panelSize, quorum, agreed, issuedAt, expiresAt)`; `questionHash` = keccak-256 of the **canonical question document** (compact JSON, sorted keys: answerType, chainId, question, window, v, plus definitions/evidence/head when present), NOT of the question text; no nonce (`requestId` is the unique id). `GET /oracle/requests/:id/attestation` returns typed data + signature + `signer`. | imd.fun/docs | The contract must pin `questionHash` to the proposal and keep a `used[requestId]` set. |
| **Panel:** "one member per seat"; routing ranks machines by tools, load, recent failures and time since last such work; "nobody reviews their own work" (general rule). **Not stated:** random selection, whether one wallet's many seats can fill several panel seats, whether the requester's seat can sit on its own panel. | imd.fun/docs | Sybil resistance of the oracle lane is UNPROVEN; use large panels (section 4b). |
| **Precedent on chain:** `AdamSplitOracle` `0x15D8…df6b` (Sourcify-verified, Solidity 0.8.26): immutable `signer` + `relayer`, `used[requestId]`, `MAX_AGE` 26 h, `answerType` pinned, `panelSize ≥ 5`, `quorum ≥ 4`, `agreed ≥ quorum`, `agreed ≤ panelSize`, `chainId == block.chainid`, `toBlock < block.number`, monotonic `issuedAt`, value clamped. It does NOT pin `questionHash` (any uint question would pass; the relayer is the trust). Example attester in the docs: `0x5598…2982` (confirm the live signer from `GET /oracle/requests` before trusting it). | Sourcify, imd.fun/docs | Copy the checks, add the question pin, drop the relayer. |
| Existing Safes: Hook Owner, offsets, REGEN, etc. (owner, 2026-10-07). | `docs/todo-imdo-flywheel.md` | Candidate operator multisig for the second chamber / guardian. |

Unconfirmed: **whether a contract payer can claim the 1% fee share** (the docs say payer, but no contract payer has been tested).
Prove on Sepolia before anything else (section 7, step 2).

## 2b. Launch-pool fee claim: how the payer's 1% actually arrives (proven on chain 2026-10-19)

Checked against SVO, launch 1205 on Robinhood (4663), payer `0x28AA…C2DB`, LaunchFactory `0xa25b02a1e93903b790e6aaf7da1b8b8d50294645`
(Sourcify-verified; the mainnet LaunchFactory `0x12c6…a96f` and ProjectFactory `0xff03…7120` carry the same functions).

- **Nothing arrives by itself.** The 1.25% LP fee accrues inside the factory's single liquidity position. It moves only when someone
  calls `claimFees(uint64 launchNumber)` on the factory. There is no UI, no API route, no IMD schedule. SVO was claimed once by IMD's
  fee wallet (2026-10-14, by hand) and once by us (2026-10-19, tx `0xb1e2…b28e`); BLACKOUT (launch 1710) is claimed every 6–12 h by
  its own keeper `0x7a60…75b2`. The docs' example `OrdersALaunch` ("hand it on, or take it out") is the intended pattern for a contract.
- **Permissionless.** Any address may call it (simulated and sent from a wallet that is not the payer). The payout is a PUSH inside
  the same tx: 80% to the requester, 20% to IMD's fee wallet `0x3f25…1f22`, in BOTH pool currencies. `owed(account, currency)` only
  fills when a push fails (a contract that rejects the asset); `withdraw(account, currency)` then pays it out. `FeesClaimed`,
  `FeesPaid`, `FeesOwed`, `RequesterChanged` events.
- **The pool's currency0 is whatever the launch paired with.** SVO is IMD/SVO, so its fees are IMD + SVO, not ETH. A Swarm Bank launch
  paired with ETH pays ETH + token.
- **Recipient is movable:** the current requester calls `setRequester(launchNumber, next)` on the factory (fee rights only;
  continuation rights stay with the original Intake caller).
- **Scale:** SVO (liquidity $12k, volume ~$1.2k/day) has paid its requester about $22 since launch. A 1% share needs real volume.

**For the bank:** (1) the pool contract (or the forwarder that is the payer) needs a `claimFees` step in its keeper loop, or relies on
anyone calling it; (2) the pool must accept native ETH and ERC-20 pushes, or the share sits in `owed` until `withdraw`; (3) index
`FeesPaid` to show fee income on the dashboard; (4) the launch should be a hook launch with the pool as fee recipient (IMDO's model,
1.5% of all volume), with the 1% requester share as the second, smaller stream.

## 3. The pool contract (`AgentPool`)

1. **Deploy as the payer.** Launch with `launch.open` (`evm_project`, paired with IMD or ETH) or `workflow.open`; the pool contract
   itself calls Intake `request`, so it is `paidBy`. The 1% fee stream lands in the pool. The pool is also the only address that can
   continue the project.
2. **Intake.** Fees may arrive as IMD or the paired asset. `sweep(token)`: anyone can pull fee balances in. Per-token accounting.
   **OPEN:** split inbound by basis points, default 80% spendable / 20% reserve.
3. **Spender registry.** Each registered agent address has: a per-epoch budget (**OPEN:** 10 IMD per day), an allowlist of target
   contracts and selectors (Intake `request` for buying jobs, at minimum), a hard per-call cap.
4. **Spend path.** `spend(target, data, amount)`: caller registered, target + selector allowed, epoch budget has room, decrement,
   call. `buyJob(body)` helper pays 0.5 IMD per action through Intake so agents never hold keys. Every spend emits an event.
5. **Limits.** Total outflow cap per epoch (bounds a compromised agent). Guardian can pause (pause only, no spend power).
6. **Control.** The pool's owner is the governance Timelock (section 4), not an EOA. Budgets, allowlist and new agents change
   only through it.

## 4. Seat quorum (`Governor` + `Timelock` + `SeatVotes`)

Three ways were weighed; the first is the pick.

1. **Snapshot-based seat voting (pick).** If the seat NFT is ERC721Votes: OpenZeppelin `Governor` + `GovernorVotes` +
   `GovernorVotesQuorumFraction`, one seat = one vote at the proposal snapshot. If it is plain ERC721 (likely): no snapshot is
   possible and a seat can vote, move, vote again. Fix: `SeatVotes`, a lock wrapper (deposit a seat, get a checkpointed vote
   weight, withdraw later). Costs seat liquidity, but is sound.
2. **Pool-owned proposal flow.** Two tiers: small spends inside registered budgets need no vote; large spends, budget changes,
   allowlist changes and new agents need a seat vote with quorum, then the timelock. Pool owner = Timelock, proposer = Governor.
3. **Oracle-signed votes.** An IMD oracle panel answers "did seats approve X". Cheap, but trusts the oracle and costs 0.5 IMD per
   vote. Rejected for primary treasury control; kept as an optional second chamber (section 5, item 6).

**OPEN parameters:** quorum 10% of seats with simple majority (many seats are idle; a high quorum deadlocks the pool); voting 3 days;
delay 1 day; timelock 2 days; proposal threshold 1 seat (a few, if spam appears); guardian veto that expires or is removable by vote.

## 4b. Three tiers: the oracle lane in the middle (owner, 2026-10-18: "submit a spend proposal as a question to the swarm")

| Tier | Path | Who decides | Bound | Time |
|---|---|---|---|---|
| 1 | `spend()` inside a registered budget | nobody, the contract | per-agent epoch budget, per-call cap | seconds |
| 2 | **oracle question, 0.5 IMD** | a swarm panel (`evidence: "panel"`, `bool`) | per-proposal cap + per-epoch oracle-lane cap (**OPEN:** 5% of the pool), 24 h timelock, guardian veto | hours to a day |
| 3 | seat vote (section 4) | locked seats, quorum + distinct holders | everything else: rule changes, tier-2 caps, panel size/quorum, the oracle signer, upgrades | ~6 days |

Tier 3 owns every knob of tier 2, so the seats can shrink or switch off the oracle lane if IMD's key or its panels go bad. The
oracle may also serve as tier 3's second chamber (section 5, item 6).

**How a tier-2 proposal runs**

1. **Propose on chain.** `proposeSpend(target, data, amount, memo)` (memo bounded, say 280 chars). The contract stores the
   proposal and **builds the question text itself** from a fixed template, so the proposer cannot frame it:
   `"AgentPool <pool> on chain <id>, proposal <n>: pay <amount> <token> to <target>, calldata keccak <hash>. Memo: <memo>.
   Answer true if the swarm approves this spend."` It computes `questionHash = keccak256(canonicalDoc)` where `canonicalDoc`
   is the compact sorted-key JSON IMD hashes (`{"answerType":"bool","chainId":<id>,"evidence":"panel","question":"<text>",
   "v":1,"window":{"hours":24}}`, plus fixed `definitions`), stores it, and emits the full body so anyone can submit it verbatim.
   Must be proven byte-for-byte against IMD's canonicalisation on Sepolia (section 7, step 4); JSON string escaping of the memo
   is the risky part, so restrict the memo to `[A-Za-z0-9 .,:;()\-]`.
2. **Ask.** Anyone (usually the proposer) submits that exact body to `oracle.request` with `consumer = {chainId, pool}` and pays
   0.5 IMD (x402 from a wallet, or on chain through Intake from the pool's own tier-1 budget: a proposal then costs the pool
   0.5 IMD, bounded like any tier-1 spend). `panelSize` and `quorum` are read from the pool (**OPEN:** 25 and 17, two thirds;
   the price is the same for 5 or 100 members, and a large panel is the only sybil defence the docs give us). `validForSeconds`
   **OPEN:** 3 days.
3. **Submit the attestation.** Anyone calls `executeAttested(n, attestation, signature)`. Checks, copied from `AdamSplitOracle`
   and tightened: recovered signer == the pool's `oracleSigner`; `questionHash == proposals[n].questionHash` (the pin ADAM
   lacks); `answerType == bool` and `answer == true`; `chainId == block.chainid`; `panelSize ≥ pool.minPanel`, `quorum ≥
   pool.minQuorum`, `agreed ≥ quorum`, `agreed ≤ panelSize`; `issuedAt ≤ now`, `now − issuedAt ≤ MAX_AGE`, `expiresAt ≥ now`;
   `!used[requestId]`, then mark used; `amount ≤ perProposalCap` and the epoch's oracle-lane total + amount ≤ epochCap.
   A `false` answer, or no attestation before `expiresAt`, closes the proposal; it can be re-asked as a new proposal (new 0.5 IMD).
4. **Timelock.** 24 h. The guardian may cancel (pause-only role). Dissenting seats can start a tier-3 vote to cancel.
5. **Execute.** Anyone calls `execute(n)`; the pool makes the call and emits `Spent` like any tier-1 spend.

**What the lane trusts, plainly:** IMD's oracle signer (one key; bounded by the caps and replaceable by tier 3), IMD's panel
selection (undocumented; the large panel and the "nobody reviews their own work" rule are the only mitigations), and the
answer semantics (the panel judges the template text and memo; it never sees calldata, only its hash and the decoded
target/amount in the text, so the template must print the human-readable call: token, amount, recipient, and for Intake
`request` the job body hash).

**Why not oracle-only (no tier 3):** the signer key would be the pool. Keep the seats as the owner of record.

## 5. Anti-whale: wallets holding 20–40 seats

On chain this cannot be stopped outright: 40 seats split across 40 wallets are indistinguishable from 40 holders. The aim is to
make concentration **costly, slow and visible**. Tools, strongest first:

1. **Distinct-holder threshold.** A proposal needs the seat quorum AND a minimum number of distinct voting addresses (**OPEN:**
   100). A whale must split across 100 wallets to pass anything alone, which is visible and easy to veto. The most reliable tool:
   it targets the number of voters, not the weight.
2. **Per-wallet cap.** weight = `min(seats, CAP)`, **OPEN:** CAP 3 to 5. 20 to 40 seats count like 5.
3. **Square-root weight.** weight = `sqrt(seats)`: 4 seats = 2, 36 seats = 6. Shrinks the edge; pairs with the cap.
4. **Lock and age.** Only seats locked in `SeatVotes` for N days before the snapshot count (**OPEN:** 7). A fresh transfer costs
   time, which blocks buy-vote-sell and makes splitting slow.
5. **Active-agent filter.** Count only seats whose worker accepted work in the last N days, or has Merkle distributor claims
   (ERC-8004 adapter / explorer / distributor data). Idle whale seats count for nothing; a whale running 40 real workers still
   counts, but pays real compute. Adds an oracle dependency for "active".
6. **Two-chamber approval.** Treasury changes need the seat vote AND one of: a second vote with per-wallet cap 1, an operator
   multisig (an existing Safe), or an IMD oracle attestation.
7. **Delegation limit.** If delegation exists, cap any delegate at 3% of seats.
8. **Veto and rage-quit.** Time-boxed veto for small holders, or dissenters exit their share before a large spend executes.

**Pick (as answered 2026-10-15):** 1 + cap 3 and sqrt (2, 3) + 7-day lock (4) + active-agent filter (5) + timelock veto.

Trade-offs: caps and sqrt punish honest operators who run many seats (pick the cap from real holder data, section 7); the active
filter needs a trusted "active" source; cap, sqrt and lock are custom `SeatVotes` code, so adversarial review before anything else.

## 6. Wiring to IMD

- Governor, Timelock, `SeatVotes` and `AgentPool` go in ONE `evm_project` or `workflow.open` build; adversarial review runs before
  any frontend (the owner's checker rule).
- Sepolia first, with a mock seat NFT (the real one cannot be snapshotted yet) and a mock Intake.
- The pool pays its own continuations, so a contract upgrade is itself a governed spend.
- This app: nothing changes until the contracts exist. Later: a `/swarm-pool` card (balances, budgets, open proposals) reading the
  contracts, and a vote button through `window.directSignTx`. No server key: every vote and proposal is browser-signed.

## 7. Order of work (nothing started)

1. **Seat distribution (free, read-only, this repo).** One script over `refreshSeatOwners()`'s map: holders by seat count,
   how many wallets hold 20–40, their share of all seats and of metered seats. Simulate each scheme in section 5 against it
   (how many wallets pass quorum alone under cap / sqrt / distinct-holder). This decides CAP and the threshold.
2. **Seat NFT ABI.** Etherscan or `explorer.imd.fun`: ERC721Votes? enumerable? Decides whether `SeatVotes` is needed.
3. **Contract-payer fee claim.** A Sepolia launch paid by a throwaway contract; confirm the 1% reaches it.
4. **Oracle lane proof (Sepolia, 0.5 IMD per question; needs the owner's word to pay).** Read the live `signer` from
   `GET /oracle/requests`; ask one template question with `consumer` set to a throwaway verifier; confirm the on-chain
   `questionHash` matches IMD's byte for byte and the template passes the wording screen; recover the signer on chain. Also
   read the last 48 k chars of imd.fun/docs (schedules, pay-onchain callback) that no read has covered yet.
5. Draft the job body as `docs/swarm-requests/job-swarm-pool.draft.json`, run the free `check`. **No `quote`, `approve` or `pay`
   without the owner's word** (standing rule).
6. Build + adversarial review (swarm), then the app card.

## 8. Owner decisions needed before a build

| # | Decision | Recommended default |
|---|---|---|
| D1 | Paired asset for the pool's own project (IMD or ETH) | IMD |
| D2 | Spendable / reserve split of inbound fees | 80 / 20 |
| D3 | Per-agent epoch budget, per-call cap, total outflow cap | 10 IMD/day, 2 IMD, 5% of pool per epoch |
| D4 | Quorum, voting period, delay, timelock | 10%, 3d, 1d, 2d |
| D5 | Anti-whale set | section 5 pick; CAP from step 1 data |
| D6 | Second chamber: Safe, cap-1 vote, or oracle | an existing Safe, removable by vote later |
| D7 | Guardian (pause only): who, and expiry | Hook Owner Safe, expires after 180 days unless renewed |
| D8 | Who may register as an agent (any seat's worker? allowlist?) | vote-approved allowlist |
| D9 | Tier-2 caps: per proposal, per epoch | 1% of pool per proposal, 5% per epoch |
| D10 | Tier-2 panel size / quorum / validity | 25 / 17 / 3 days |
| D11 | Tier-2 timelock and who may cancel | 24 h; guardian, or a tier-3 vote |
| D12 | Who pays the 0.5 IMD: proposer's wallet, or the pool through Intake | proposer, until the pool's Intake path is proven |
| D13 | Stage A custody: A (people, 3-of-5 Safe) or B (no people, oracle-module Safe); hold-only as fallback | put to the first signal vote; my pick is B |

## 9. Out of scope / not this spec

- Changing IMD's fee policy or the seat NFT itself.
- Paying anyone from the app's own wallets; the pool holds its own funds, agents never hold keys.
- A snapshot of the real seat NFT before step 2 says it is possible.

## 10. Development flow (brainstorm with the owner, 2026-10-18; nothing started)

Constraint: one developer, one seat, enrolling the wider community. So the flow makes the community build and pay, and the owner's
job is specs, running votes and the glue. Progressive decentralisation in three stages.

**Stage A: signal, no contracts (weeks, cheap).** Goal is enrolment, not a treasury.
- Idea page + this spec, public (whitepaper pattern).
- **Seat-verified signal votes in THIS app**: login exists (SIWE), `seat-owners.mjs` already maps every seat to its owner. A `/pool`
  page: proposals as text, one vote per seat by signed message, live tally. Non-binding, no gas, no audit. Ships from this repo.
- **Who holds the pool is the FIRST signal vote (owner, 2026-10-19: IMD's mission is a zero-person company, a 3-of-5 of people may not fly;
  "present both and see what they say").** Two shapes, both on the site:
  - **A. People:** a Safe signed by five named seat holders, 3-of-5, spending only what a signal vote passed, every tx public. Stock, no audit.
  - **B. No people:** a Safe whose ONLY owner is an `OracleModule` (~150 lines): a spend is proposed by anyone, put to a panel of 25 agents as
    an oracle question (0.5 IMD), executed by the module when 17 agree, inside per-spend and per-epoch caps; the deploy key is renounced on
    day one. This is tier 2 from section 4b, built first; Stage B adds the seat Governor as a second module and hands it the knobs.
  - Both: fees arrive only on `claimFees`; the dashboard reads the Safe (balance, every outflow, matched proposal or attestation).
  - A third shape, hold-only (point every fee stream at a CREATE2 address that nothing controls until the pool contract is deployed there), is
    kept as the fallback if neither wins: zero keys, zero spending.
- **Founding oracle question** (0.5 IMD, panel 25+): "Should the IMD swarm hold a shared, seat-governed spending pool?" The signed
  attestation is the social-proof artefact for the pitch and dogfoods tier 2 before any contract.

**Stage B: contracts (months).** Governor + Timelock + SeatVotes + AgentPool replace the Safe's signers. Sepolia with a mock seat NFT
first. Signal votes become binding votes on the same page and login, only the submit path changes (`directSignTx` to the Governor).

**Stage C: oracle lane + agents spending.** Tier 1 budgets and tier 2 questions, once Stage B has run clean.

**Token design: the launch IS the token.** No governance token: seats govern (the anti-whale point). The pool's own IMD launch
(`launch.open`; in Stage A the Safe pays, in Stage B the pool contract) gives: 80% in the pool and 1% of every trade back to the
treasury (the fee source); **10% to the swarm via the Merkle distributor**, every connected seat gets a slice: the enrolment
mechanic, and the claim card already exists (`launch-claims.mjs`): "claim your share, then come vote". The token is liquidity plus
fee source, never a vote weight. No yield language (whitepaper rule).

**Who does what**

| Work | Who | Why |
|---|---|---|
| Idea site, visuals, copy, tokenomics page | swarm `build-website` job, 0.5 IMD | `docs/offsets-swarm-brief.md` rule: the site **reads our APIs, builds no wallet or vote flow** |
| Seat login, voting, spend/proposal dashboards, indexer | this app | SIWE, seat map, direct-sign, charts, ledger-crawler pattern exist; swarm-built wallet code would itself need an audit |
| Contracts | swarm `evm_project` job from this spec, then **adversarial review** jobs (regen-rail pattern, three rounds) | |
| Audit | swarm adversarial review + one human reviewer | publish both |
| Founding and later spend questions | oracle, 0.5 IMD each | |

Public JSON from this app (`GET /api/pool/state`: balance, outflows, proposals, votes, attestations) is the contract between the
two sides: the swarm site renders it, this app owns the truth.

**The flywheel that funds the work.** First proposals on the signal page: "pay 0.5 IMD for the contracts job", "pay for the audit",
"pay the developer X IMD a month" (**OPEN:** whether the owner's pay goes to a vote). The pool pays for its own construction by vote;
the owner becomes a contractor the swarm hired, not the sponsor.

**Order**
1. Spec public; `/pool` signal page in the operator app (plan: operator repo `docs/todo-pool-signal-votes.md`, written 2026-10-19); the custody question is proposal #1.
2. Founding oracle question; attestation shown on the page.
3. Launch the pool token from the Safe; distributor claim card; "claim then vote".
4. Site job to the swarm, API contract fixed first.
5. First votes: audit budget, dev budget. Contracts job. Reviews. Sepolia. Mainnet. Safe hands over to the Timelock.

Steps 2–5 each cost IMD and wait for the owner's word. Step 1 can start in this repo on the owner's word. Decisions owned now:
Safe signers, pair asset (IMD or ETH, D1), whether dev pay goes to a vote.
