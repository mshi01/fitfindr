# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
Search the listings data for items matching a description, and optionally a size and a price ceiling. 
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
     - description (str): keywords describing what the user wants
          
     - size (str) || None (None): a size string to filter by, or None to skip size filtering.

     - max_price (float) || None (None): maximum price, inclusive, or None to skip price filtering.
- **Returns:**
A list of matching listing dicts, best match first. Each listing dict has these fields:
id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform.
- **When it has nothing:**
Returns an empty list.

### `suggest_outfit`

- **What it does:**
Given a thrifted item and the user's wardrobe, suggest one or two outfits.

- **Inputs:**

     - new_item: a listing dict, the item the user is considering. Each listing dict has these fields:
id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform.

     - wardrobe: a wardrobe dict with an 'items' key holding a list of items. Each item has the fields of id, name, category, colors, style_tags and notes. It may be empty.

- **Returns:**
A non-empty string with outfit suggestions. 

- **When it has nothing:**
With an empty wardrobe, return general styling advice.

### `create_fit_card`

- **What it does:**
Write a short caption someone would actually post about the find.

- **Inputs:**
outfit:   the outfit suggestion string from suggest_outfit().
new_item: the listing dict for the item.

- **Returns:**
A two-to-four sentence caption.
- **When it has nothing:**

Return a descriptive message.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

If search_listings returns an empty list, run_agent puts a message in session["error"] and returns the session immediately. The message names the query that was tried and suggests what to change: raise the price limit, change or drop the size, or use more general keywords. suggest_outfit and create_fit_card are never called, so fit_card stays None. Otherwise, it stores the first result in session["selected_item"], calls suggest_outfit with that item and the wardrobe, then passes the outfit and the item to create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
The query is parsed with regular expressions, not the model. The parsing lives in _parse_query in agent.py. It handles the three fields in this order:
1. Price (max_price): It matches a limit word followed by a number: under, below, less than, up to, max, maximum, at most, within, or <. It also accepts a bare dollar amount like "$50". It takes the first match as a float, so "under $30" gives 30.0. The matched text is removed from the query.
2. Size (size): It first looks for the word "size" followed by a value: "size M", "size XXS", "size M/L" or "size US 9". The us, uk and eu prefixes are allowed.
If that fails, it looks for a lone size token (xxs, xs, s, m, l, xl, xxl) written in capitals, like "denim jacket M". The capitals rule stops ordinary words like "a" or "m" from being read as sizes.
The matched text is removed from the query.
3. Description: Whatever is left has commas and semicolons stripped and whitespace collapsed. For "looking for a vintage graphic tee under $30, size M" it keeps "looking for a vintage graphic tee". Filler words like "looking for" are left in. search_listings already drops them as stopwords, so there was no need to strip them here.



**What moves through the session:** <!-- which fields, in what order -->
query → parsed (description, size, max_price) → search_results → selected_item → outfit_suggestion → fit_card. The error field is set only when the run stops early.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None,'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layeringunder a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt —Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics,clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}]

```
$ python -c "from tools import suggest_outfit; ..."

```
Hey there! Those vintage Levi's 501 Jeans are an incredible find. Here are two ways to style them using pieces right out of your closet:

**Outfit 1**
* **Wear:** Vintage Levi's 501 Jeans — Medium Wash + White ribbed tank top + Vintage black denim jacket + Chunky white sneakers
* **Why it works:** Pairing the fitted white tank with the classic medium wash denim creates an effortless base, while the slightly cropped black jacket and chunky sneakers lean right into a cool streetwear vibe.

**Outfit 2**
* **Wear:** Vintage Levi's 501 Jeans — Medium Wash + Oversized grey crewneck sweatshirt + Brown leather belt + Black combat boots
* **Why it works:** Tucking the cozy, oversized grey crewneck into the 501s balances the volume, and accessorizing with the brown belt and combat boots adds a great grunge-meets-classic contrast.

```
$ python -c "from tools import create_fit_card; ..."

```
Found these vintage Levi's 501 jeans and they have the exact broken-in 90s slouch you always look for. Snagged them on depop for $38, which feels like a steal for denim that actually fits right. Just pair them with some beat-up white sneakers and you're done.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
I asked Claude how the query is parsed in agent.py::_parse_query.
- *What came back:*
The AI only said the query is parsed with regular expressions and showed example inputs and outputs for max_price, size and description. It did not spell out the rules behind those results.
- *What I changed:*
When I asked specifically how the query is parsed, the AI gave the regex rules it uses to extract max_price, size and description.

**Moment 2**

- *What I asked for:*
I asked Claude to give suggestions on the fifth criteria that testing working for the agent.

- *What came back:*
It suggest me about the max price ceiling cap.

- *What I changed:*
I would like to write one for the empty wardrobe path, so I rewrote the fifth criteria to be about the empty wardrobe path. 
<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  | A matching query completes all three tools | 4 out of 5 | PASS | PASS | PASS | PASS | PASS | MET (5 out of 5) |
| 2.  | An impossible query stops before the second tool | 5 out of 5 | PASS | PASS | PASS | PASS | PASS | MET (5 out of 5) |
| 3.  | With an empty wardrobe and a query that matches a listing, the agent completes all three tools and the fit card is non-empty | 5 out of 5 | PASS | PASS | PASS | PASS | PASS | MET (5 out of 5) |
| 4.  | The item passed to suggest_outfit and create_fit_card is identical | 5 out of 5 | PASS | PASS | PASS | PASS | PASS | MET (5 out of 5)|
| 5.  | Each fit card mentions the item's exact price, and shares no identical opening sentence | 5 out of 5 | PASS | PASS | PASS | PASS | PASS | MET (5 out of 5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
run python run_eval.py --label before

Criterion 1:
matching query completes  (example wardrobe)
  query: vintage graphic tee under $30
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Vintage Graphic Hoodie — Faded Black … +7 more
[2] suggest_outfit
      in:  dict with keys: item, wardrobe
      out: Hey there! Here are two easy, effortless ways to style your new Graphic Tee — 2003 Tour Bootleg Style using pi…
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Found this sick 2003 tour bootleg tee on depop for $24 and it's giving major grungy streetwear energy. Throw i…
  try 1: completed — fit card 212 chars

Criterion 2:
impossible query stops early  (example wardrobe)
  query: designer ballgown size XXS under $5
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit
  try 1: stopped early — No listings matched "designer ballgown" in size XXS under $5

Criterion 3:
empty wardrobe  (empty wardrobe)
  query: denim jacket under $50
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Denim Jacket — Light Wash, Cropped, High-Waisted Denim Shorts — Cutoff, Denim Vest — Medium Wash, Studded … +4 more
[2] suggest_outfit
      in:  dict with keys: item, wardrobe
      out: Hey there! That Wrangler jacket is an absolute gem—structured shoulders make all the difference! Here are two …
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Scored this cropped Wrangler denim jacket on Poshmark for $42 and the structured shoulders give it the ultimat…
  try 1: completed — fit card 208 chars

Criterion 4:
states matching  (example wardrobe)
  query: denim jacket under $50
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 7 items: Denim Jacket — Light Wash, Cropped, High-Waisted Denim Shorts — Cutoff, Denim Vest — Medium Wash, Studded … +4 more
[2] suggest_outfit
      in:  dict with keys: item, wardrobe
      out: **Outfit 1** * **Denim Jacket — Light Wash, Cropped** + **White ribbed tank top** + **Baggy straight-leg jeans…
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Found this cropped light wash denim jacket on Poshmark for $42 and it instantly gave me that 90s off-duty mode…
  try 1: completed — fit card 199 chars

Criterion 5:
each fit card mentions the item's price and shares no identical opening sentence (example wardrobe)
  query: white t-shirt size M
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 6 items: 90s Track Jacket — Navy/White Stripe, Vintage Polo Shirt — Forest Green, Y2K Baby Tee — Butterfly Print … +3 more
  [rate limit] 15 requests used this minute. Waiting 43s. This is normal.
[2] suggest_outfit
      in:  dict with keys: item, wardrobe
      out: Here are two fresh ways to style your new 90s Track Jacket:  **Outfit 1** * **Pair with:** White ribbed tank t…
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Found this navy and white 90s track jacket on Poshmark for $45 and it’s giving major retro athletic energy. To…
  try 1: completed — fit card 188 chars




```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools  | 5 of 5 | MET (5 of 5) | A matching query completes all three tools for all tries. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5 of 5) | For impossible query, the agent stops before the second tool. |
| 3 | With an empty wardrobe and a query that matches a listing, the agent completes all three tools and the fit card is non-empty | 5 of 5 | MET (5 of 5) | All tries with empty wardrobe. The agent completes all three tools and the fit card is not empty. |
| 4 |  The item passed to suggest_outfit and create_fit_card is identical | 5 of 5 | MET (5 of 5) | For all tries the item passed to suggest_outfit and create_fit_card is the same. |
| 5 | Each fit card mentions the item's exact price, and shares no identical opening sentence | 5 of 5 | MET (5 of 5) | For all tries, the fit card shared no identical opening sentence and mentionsed the item price.|

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
python app.py ask 'purple dress' --trace

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 3 items: Vintage Windbreaker — Color Block Purple/Teal, 90s Silk Slip Dress — Floral, Midi Length, Y2K Baby Tee — Butterfly Print
[2] suggest_outfit
      in:  dict with keys: item, wardrobe
      out: Hey friend! That color block windbreaker is such a fun 90s score. Here are two quick ways to style it using pi…
[3] create_fit_card
      in:  dict with keys: outfit, item
      out: Scored this wild 90s color block windbreaker on thredUp for only $40 and honestly I'm obsessed. It’s giving ma…

  Found:    Vintage Windbreaker — Color Block Purple/Teal — $40.0 on thredUp

  Outfit:   Hey friend! That color block windbreaker is such a fun 90s score. Here are two quick ways to style it using pieces from your closet:

**Outfit 1**
*   **Wear with:** Baggy straight-leg jeans, dark wash, White ribbed tank top, and Chunky white sneakers.
*   **Why it works:** The fitted white tank balances the volume of the jacket, and the sneakers lean right into that retro streetwear vibe.

**Outfit 2**
*   **Wear with:** Wide-leg khaki trousers and Chunky white sneakers.
*   **Why it works:** Pairing the sporty windbreaker with tailored trousers creates an effortless, high-low streetwear look.

  Fit card: Scored this wild 90s color block windbreaker on thredUp for only $40 and honestly I'm obsessed. It’s giving major retro athletic energy, especially thrown over some baggy denim and chunky sneakers. 🧥
```

**Empty search**

```
python app.py ask 'black jacket under $0' --trace

[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit

  No listings matched "black jacket" under $0. You could raise your price limit; use fewer or more general keywords (e.g. "jacket" instead of a specific style).
```

**On the MCP move:**

I moved one tool, `search_listings`, behind an MCP server. Two files changed:

- `mcp_server.py`: I registered `search_listings` with `@mcp.tool()` on a FastMCP server. The typed inputs match my Tool Inventory: `description: str`, `size: str | None`, `max_price: float | None`. The function just calls the real implementation in `tools.py`, imported under the alias `_search_listings_impl` so the registered tool doesn't call itself. I wrote the docstring for a reader who can't see the code. It names the units (US dollars, inclusive ceiling), explains how size matching works ("M" matches "S/M" but not "XL"), lists every field of the returned listings, and states the empty case: an empty list, never null and never an error.
- `agent.py::run_agent`: in the search stage, the direct `search_listings(...)` call became `call_tool("search_listings", {...})` from `mcp_client.py`. The other two tools are still called directly.



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
