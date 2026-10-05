# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
I picked 4 of 5 rather than 5 of 5 because search_listings is a plain keyword match. A query phrased differently from the listing title (for example "vintage denim jacket" against "Levi's trucker jacket") can return nothing even when a good listing exists. Allowing one miss in five covers that, and a miss here points to a search-matching problem rather than a loop problem.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
5 of 5 is the right target here because this path has no variance. When search_listings returns nothing, the if not session["search_results"] check in the agent loop is plain code with no model call. It sets session["error"] and returns before suggest_outfit runs, so the same query should stop at the same point every time. Any miss would mean a bug in the guard, not an unlucky run.
---

## 3. Something about state

In 5 of 5 matching runs, the item passed to suggest_outfit and create_fit_card is identical (same listing id and price) to session["selected_item"], and selected_item is search_results[0].
<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->



**Why this target:**

5 of 5 is the right target because passing state between tools involves no model call. The agent sets session["selected_item"] to the first search result and hands that same dict to suggest_outfit and create_fit_card. Nothing in that path can vary between runs, so any mismatch would mean something mutated or re-fetched the item. That would be a bug in how the session is used.

---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->
For 5 different items, each fit card mentions the item's exact price, and shares no identical opening sentence.


**Why this target:**

For 5 different items, each fit card mentions that item's exact price, and no two of the 5 cards share the same opening sentence. All 5 must meet both conditions.


---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
With an empty wardrobe and a query that matches a listing, the agent completes all three tools in 5 of 5 runs. session["error"] stays None, suggest_outfit returns a non-empty outfit built around the found item, and the fit card is non-empty. 


**Why this target:**

With an empty wardrobe and a query that matches a listing, suggest_outfit returns general styling advice for the found item. The agent doesn't raise an error and still calls create_fit_card, in 5 of 5 runs. The empty-wardrobe branch is a fixed code path.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
