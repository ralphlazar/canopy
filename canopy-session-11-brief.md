# Canopy Build Brief - Sessions 1-11

## Platform Context
Canopy is a conservation intelligence and finance platform covering Africa. Stack: HTML + JSON data files, no framework. Hosted on Cloudflare Pages (canopy-acx.pages.dev), auto-deploys on git push. Local repo: /Users/lisaswerling/RALPH/AI/canopy. Eight sections with colour identities.

## Session Rules
- Files always download to ~/Downloads/. Bash copy commands use `"$(ls -t ~/Downloads/filename*.ext | head -1)"` with quotes around the subshell to handle Mac space-in-filename convention.
- Always show a plan before building. Never start without it. Always ask for confirmation after showing the plan. Wait for go-ahead.
- All text must not look AI-written. No em-dashes - use regular hyphens. No apostrophes in JSON summary fields.
- Add to brief when asked. Never present as download unless asked. Always give brief as .MD file for download.
- When asked for bash code, respond with just the code block. No preamble.
- Do not push to git during development. Push only when session work is complete and confirmed.
- When needing a file from local repo, give bash code to copy it to Downloads, then wait for upload.
- Always give URLs as clickable hyperlinks.
- When asked to add a rule, add it to the brief. Do not present the revised brief unless asked.

---

## Session 11 Work

### Task 1 - CAIRN Password Removal [COMPLETED]

Removed password gate from both surfaces:

**cairn.html:**
- Removed gate CSS (`.gate-wrap`, `.gate-box`, `.gate-input`, `.gate-btn`, `.gate-clue`, `.gate-error`)
- Removed gate HTML block entirely (padlock, "Members only", password input, clue text)
- Changed `.tool-wrap` from `display: none` to `display: block`
- Removed `checkPassword()` function
- Added `loadAndScore()` call directly on page load

**index.html:**
- Removed the `cairn-lock` div from card 6 (padlock icon + "Members only" label + sub text)

### Task 2 - Who's Who Additions [COMPLETED]

Added 14 new profiles across multiple batches. Total now 174 profiles.

**Verra Board (3 profiles):**
- El Hadji Mbaye Diagne - Director General, AEE Senegal; Chair CDM Executive Board; Article 6.4 Supervisory Body; IPCC AR6 lead author
- Jennifer Park - Partner, ALTERRA Management Limited (UAE $30bn climate fund); former UN Secretary-General adviser; Paris Agreement/JETPs
- Derek Walker - Principal, Summit Strategy Group; former VP Global Energy Transition at EDF; Verra board member

**Verra Staff (5 profiles):**
- Mandy Rambharos - CEO Verra; South African; former GM Just Energy Transition at Eskom; co-chaired Article 6 at COP26
- Katie Goslee - Director Forest Carbon, Verra; leads REDD+/IFM/ARR/Blue Carbon methodologies
- Manish Neupane - Director Natural Climate Solutions, Verra; oversees SD VISta and CCB programs
- Marie Calmel - Director NCS Program Quality, Verra; Congo Basin field experience; JNR/REDD+ integrity
- Sinclair Vincent - Senior Director Program Development, Verra; built SD VISta Nature Framework

**Savo (3 profiles):**
- Gail Klintworth - Chairman/Co-Founder Savo; former Unilever CSO/CEO South Africa; Chair Shell Foundation; Rabobank supervisory board
- Robbie Marwick - CEO/Co-Founder Savo; interim CEO Africa Carbon Partners; SYSTEMIQ founding employee; McKinsey; Gashaka Gumti and Okomu National Park projects
- Ade Okuwoga - Co-Founder Savo; now Associate at General Atlantic BeyondNetZero; SYSTEMIQ; McKinsey; Harvard MBA

**Tony Hansen and Duko Hopman network (6 profiles):**
- Adam Falk - President and CEO, WCS; founding partner of Keystone Partnership alongside Rob Walton Foundation
- Frederick Kumah - VP Global Leadership, AWF; Nairobi-based; leads APAD network and AWF Keystone work; 26 years across AWF/WWF/Oxfam
- Joshua Katz - Partner Natural Capital and Nature, McKinsey; current leader of team Tony Hansen and Duko Hopman built; co-authored Nature in the Balance with both
- Kartik Jayaram - Senior Partner, McKinsey Nairobi; leads Sustainability Practice EEMA; voluntary carbon market development; Green Africa series; co-authored with Duko Hopman
- Kristine Tompkins - President/Co-Founder Tompkins Conservation; former CEO Patagonia; Carnegie Medal of Philanthropy; UN Global Patron for Protected Areas 2018-2022; Tony Hansen advisory board
- Ashley Robson - Founder, Keystone Conservation; financial and resource modelling for African protected areas; developed the Keystone Standard; co-authored the 2025 Keystone Protected Areas paper with WCS/African Parks/FZS/Rob Walton Foundation

### Task 3 - Box 8: Carbon Market Pulse [COMPLETED]

Added card 8 to homepage and built carbonsnaps.html.

**index.html changes:**
- Card 7 (Funding Instruments) no longer spans full width - now takes one column
- Card 8 (Carbon Market Pulse) added as second column alongside card 7
- Slate navy colour identity (`#1a3552`) - distinct from all existing cards
- Card shows: VCM spot ($6.40, -2.1% this week, Bearish), CORSIA (Mixed, Phase 1 ends Dec 2026), two upcoming regulatory events
- Quiet `carbonsnaps.com ->` attribution bottom right
- Card links to `carbonsnaps.html`

**carbonsnaps.html (new file):**
- Standalone Canopy page - native Canopy content, not a redirect
- Intro: explains why carbon market signals matter for funders evaluating African projects
- Signal bar: overall read for African conservation projects (Bearish near-term)
- Two instrument cards: VCM (price/changes/signal/story) and CORSIA (phase/signal/story)
- "What this means for African projects" editorial box - connects market signals to the project database and Keystone financing gap
- Three regulatory events: EU ETS surrender deadline (30 Apr 2026), COP31 Belem (Nov 2026), CORSIA Phase 2 transition (31 Dec 2026)
- External link box to carbonsnaps.com for full eight-instrument picture
- Framing: first framing (native Canopy content, carbonsnaps.com is context not the point)

### Task 4 - Bug Fixes [COMPLETED]

**Bug 1 - Logo map not showing on carbonsnaps.html:**
nav.js calls `renderLogoMap()` if the function exists. carbonsnaps.html had no such function. Fixed by adding D3, topojson, `africaISO` set, `loadWorld()`, and `renderLogoMap()` to carbonsnaps.html.

**Bug 2 - Who's Who animation race condition on hard refresh:**
Root cause: `load()` was called in the first `<script>` block, but D3 and topojson were loaded in `<script>` tags that followed it. On localhost, JSON files resolve faster than CDN scripts. When `load()` resolved, `renderMiniProjMap` was not yet defined, so the entire render block (including `initWWNetwork()`) silently skipped. Fixed by moving D3 and topojson script tags to before the first `<script>` block.

---

## Carbon Market Pulse - Data Plan [AGREED - NOT YET BUILT]

### Route B - Replicate live data in Canopy repo

A script extracts the relevant subset from CarbonSnaps `CB_data.json` and writes to `canopy/data/carbonsnaps.json`. The carbonsnaps.html page reads that file at runtime. No cross-repo dependency, no API call to carbonsnaps.com.

**What to extract:**
- VCM: price, change_1w, change_1m, change_3m, spark, signal, story
- CORSIA: signal, phase, story
- Regulatory events tagged VCM or CORSIA only

**Script:** ~30 lines, added to CarbonSnaps weekly ritual alongside existing scripts.

**Build sequence:** Extract script runs after `CB_update_stories.py`, before `git push`. Canopy data file is committed with the weekly CarbonSnaps push.

---

## Who's Who - Strategic Notes

**Stickiness strategy:** Who's Who is Canopy's primary traffic driver and outreach tool. Adding profiles of people who will see themselves in the directory - and share it - is the highest-leverage growth activity.

**Key sources identified:**
- Carbon Markets Africa Summit speaker list (highest yield - curated, verifiable, Africa-focused)
- Verra board and staff (done - good coverage now)
- ACMI leadership and country leads
- FSD Africa carbon markets team
- DFI Africa conservation leads (BII, Proparco, DEG, FMO, US DFC)
- African Development Bank climate team
- Conservation org finance arms (WCS, AWF, WWF Africa, Flora & Fauna, Space for Giants)
- CAFI executive board

**Who's Who stays on Canopy only** - do not replicate on CarbonSnaps. Use it as the entry point that brings users to both tools.

---

## CarbonSnaps Relationship

CarbonSnaps (carbonsnaps.com) is a sibling tool covering global carbon market intelligence across 8 instruments. Canopy covers the projects; CarbonSnaps covers the markets those projects sell into.

**Overlap:** VCM (primary) and CORSIA (secondary). All other instruments (EUA, UKA, CCA, LCFS, RGGI, RIN, 45Z) are compliance markets with no direct Canopy relevance.

**Integration built (Session 11):**
- Box 8 on Canopy homepage
- carbonsnaps.html as a curated market context page

**Integration planned (Route B):** Live data sync script from CarbonSnaps repo to Canopy data folder, run as part of CarbonSnaps weekly ritual.

**No Who's Who on CarbonSnaps** - keep directory whole on Canopy.

---

## Content and Distribution Plan [AGREED - NOT YET BUILT]

### Core principle
The site is the source of truth. The email is a curated digest of what moved. The pipeline serves both.

### Update cadence

| Cadence | Task | Est. time |
|---|---|---|
| Weekly | Intelligence pipeline - fetch, draft, review, approve, push | 15 min |
| Weekly | Carbon Market Pulse update (once Route B script built) | 2 min |
| Monthly | Projects registry sweep - flag status changes, review, update JSON, push | 30-45 min |
| Monthly | Policy sweep - read the month's news, update any countries that moved, push | 20 min |
| Monthly | Email written and sent (last Thursday of month) | 90 min |
| Quarterly | Who's Who refresh - LinkedIn checks, role change flags | 60-120 min |

Total monthly commitment once pipeline is built: approximately 4-5 hours.

### Email
- Cadence: monthly (bi-weekly is too frequent for the content cadence)
- Platform: Substack
- Send day: last Thursday of the month
- Target length: 400-500 words, readable in 3 minutes
- Structure: lead item, intelligence highlights (4-5 items), policy watch, projects, from the site
- Tone: same voice as the site - informed, direct, no padding

### Intelligence pipeline (to build - highest priority)
Script hits curated RSS feeds (Carbon Pulse, Ecosystem Marketplace, IUCN, Verra registry notices, relevant government portals, key NGO publications). Drafts candidate items to a review file. Editorial review approves/edits/rejects. Approved items write to `data/intelligence.json` and push.

### Projects registry checker (to build - second priority)
Script queries Verra and Gold Standard registries for status changes on tracked projects.

### Email digest generator (to build - third priority)
Draws from approved intelligence items accumulated over the month.

### Build sequence
1. Intelligence pipeline (RSS fetch, draft, approve, push)
2. Projects registry checker (Verra/Gold Standard)
3. Carbon Market Pulse data sync script (CarbonSnaps to Canopy)
4. Email digest generator
5. Policy update tooling (lighter - structured review checklist)

---

## Files Modified Session 11
- `index.html` - card 7 de-spanned, card 8 added, D3/topojson moved before first script block
- `cairn.html` - password gate removed
- `carbonsnaps.html` - new standalone page
- `data/whos_who.json` - 160 -> 174 profiles

Standard deploy pattern (updated for session 11 file structure):
```bash
cp "$(ls -t ~/Downloads/index*.html | head -1)" /Users/lisaswerling/RALPH/AI/canopy/index.html
cp "$(ls -t ~/Downloads/cairn*.html | head -1)" /Users/lisaswerling/RALPH/AI/canopy/cairn.html
cp "$(ls -t ~/Downloads/carbonsnaps*.html | head -1)" /Users/lisaswerling/RALPH/AI/canopy/carbonsnaps.html
cp "$(ls -t ~/Downloads/whos_who*.json | head -1)" /Users/lisaswerling/RALPH/AI/canopy/data/whos_who.json
cd /Users/lisaswerling/RALPH/AI/canopy && git add -A && git commit -m '...' && git push
```

---

## Sessions 1-10 Work (Summary)

### Session 10 - Architecture Split: SPA to 7 Standalone Pages
index.html was 2,719 lines - split into 7 standalone HTML files. Each page fetches only its own data. nav.html updated with correct hrefs. Who's Who modal suggest form added; disclaimer repositioned to bottom.

### Session 9 - Who's Who Verification Pass 2
Systematic fact-check of all 157 profiles. 128 clean verified. 29 entries flagged. Major corrections made. All 83 source URLs verified live.

### Session 8 - Who's Who Verification Pass 1
First systematic pass through all 157 entries. Major corrections across 20+ profiles.

### Sessions 1-7 - Platform Build
- Sessions 1-3: Core platform - projects map, policy tracker, Article 6 readiness, CAIRN scoring
- Session 4: Intelligence feed, weekly brief architecture
- Session 5: Keystones section (162 protected areas), Who's Who directory v1
- Session 6: Map performance improvements, data enrichment
- Session 7: CAIRN scoring improvements, mobile fixes, data completions

---

## Map Architecture

All maps use `world-atlas@2/countries-50m.json`.

**index.html maps (share `loadWorldData()` cache):**
1. `renderMiniProjMap()` - card 2, mini choropleth
2. `renderMiniPolicyMap()` - card 1, mini choropleth
3. `renderMiniKSMap()` - card 3, mini choropleth with north-to-south reveal
4. `renderLogoMap()` - nav logo, uses allPolicy data for colouring

**Standalone pages (each defines own `renderLogoMap()`):**
- All 6 section pages + keystones.html + carbonsnaps.html define a standalone renderLogoMap that draws a neutral green Africa silhouette with no data dependency

**D3/topojson loading rule (important):**
D3 and topojson script tags must appear BEFORE the first `<script>` block on any page that calls async data loading. Race condition exists on localhost where JSON resolves faster than CDN scripts.

**Somaliland handling (all files):**
```js
f.properties && f.properties.name === 'Somaliland'
```

---

## Section Colour Identities

| # | Section | Colour |
|---|---|---|
| 1 | Policy Tracker | Red `#8b1a1a` |
| 2 | Projects Tracker | Dark green `#1a4a2e` |
| 3 | Keystones | Brown `#5c3317` |
| 4 | Intelligence | Blue `#4a6fa3` |
| 5 | Who's Who | Teal `#1a5c5c` |
| 6 | CAIRN | Purple `#4a2a6b` |
| 7 | Funding Instruments | Gold `#c17f00` |
| 8 | Carbon Market Pulse | Slate navy `#1a3552` |

---

## Naming / Branding Notes

Platform name under consideration: **NKOSI** - from Nkosi Sikelel' iAfrika (God bless Africa), written by Enoch Sontonga in 1897 and woven into five African national anthems.

Domain recommendation: **nkosi.africa** - pairs name and continent, endorsed by the African Union. Check availability at [registry.africa](https://registry.africa).

Acronym if needed: Natural capital - Knowledge - Open - Source - Intelligence

---

## Who's Who - Entry Quality Standard

**Goal:** Make every entry good enough that the subject would share it unprompted.

**Format per entry:**
- Opening paragraph: what they have built, what they are known for, why it matters. No superlatives, no "passionate about", no "leading expert". Facts assembled with care.
- Structured fields: current role, organisation, past roles, education, boards/advisory roles
- `notable_work` array: specific named deals, reports, frameworks, initiatives with source URLs

**Tone:** Closer to an FT person profile than a conference bio.

**Process:**
- Research each entry individually - do not template from LinkedIn
- Use web search to verify education, roles, awards, and publications
- Where information is uncertain, omit rather than guess
- Mark `verified: true` only when role and organisation confirmed from primary source

**Priority outstanding:** Resolve flagged entries from sessions 8-9. Update stale entries (Eve Bazaiba, Daniela Raik). Carbon Markets Africa Summit speaker list is the highest-yield next source.
