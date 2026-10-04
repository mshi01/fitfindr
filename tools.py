"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────
_STOPWORDS = {
    # articles, conjunctions, prepositions
    "a", "an", "the", "and", "or", "but", "for", "with", "without", "in", "on",
    "of", "to", "from", "at", "by", "as", "into", "under", "over", "around",
    # pronouns and light verbs
    "i", "im", "me", "my", "you", "your", "it", "its", "is", "are", "be",
    "am", "have", "has", "want", "need", "looking", "find", "get", "show",
    # filler and shopping chatter
    "some", "any", "something", "anything", "that", "this", "like", "just",
    "please", "cute", "nice", "good", "great", "size", "price", "budget",
}


def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    query_words = _keywords(description)
    if not query_words:
        return []

    scored = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size is not None and not _size_matches(size, listing["size"]):
            continue

        # Title and tag hits count more than a mention buried in the description.
        title_words = _keywords(listing["title"])
        tag_words = _keywords(
            " ".join(
                [listing["category"], listing.get("brand") or ""]
                + listing["style_tags"]
                + listing["colors"]
            )
        )
        body_words = _keywords(listing["description"])

        score = sum(
            3 * (w in title_words) + 2 * (w in tag_words) + (w in body_words)
            for w in query_words
        )
        if score > 0:
            scored.append((score, listing))

    scored.sort(key=lambda pair: pair[0], reverse=True)  # stable: ties keep data order
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


def _keywords(text: str) -> set[str]:
    """Lowercase alphanumeric words, minus stopwords, with a trailing plural 's' folded."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {
        w[:-1] if len(w) > 3 and w.endswith("s") else w
        for w in words
        if w not in _STOPWORDS
    }


def _size_matches(wanted: str, listed: str) -> bool:
    """
    True when every token of `wanted` is a whole token of `listed`.

    Sizes are split on anything non-alphanumeric, so "M" matches "S/M" and
    "M/L" but not "XL" or "US 9", and "W30" matches "W30 L30".
    """
    wanted_tokens = re.findall(r"[a-z0-9.]+", wanted.lower())
    listed_tokens = set(re.findall(r"[a-z0-9.]+", listed.lower()))
    return bool(wanted_tokens) and all(t in listed_tokens for t in wanted_tokens)


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    brand = new_item.get("brand") or "unbranded"
    item_text = (
        f"{new_item.get('title', 'Untitled item')} "
        f"(category: {new_item.get('category', 'unknown')}; "
        f"colors: {', '.join(new_item.get('colors') or []) or 'unspecified'}; "
        f"style: {', '.join(new_item.get('style_tags') or []) or 'unspecified'}; "
        f"brand: {brand}; size: {new_item.get('size', 'unknown')}; "
        f"condition: {new_item.get('condition', 'unknown')})\n"
        f"Description: {new_item.get('description', '')}"
    )

    items = (wardrobe or {}).get("items") or []

    if not items:
        system = (
            "You are a friendly thrift-fashion stylist. Be specific and concise."
        )
        prompt = (
            f"A shopper is considering this secondhand item:\n{item_text}\n\n"
            "They haven't told me what's in their wardrobe. Give general styling "
            "advice: one or two outfit ideas built around this item, describing "
            "the kinds of pieces, colors and shoes that would go with it."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {i.get('name', 'Unnamed')} "
            f"(category: {i.get('category', 'unknown')}; "
            f"colors: {', '.join(i.get('colors') or []) or 'unspecified'}; "
            f"style: {', '.join(i.get('style_tags') or []) or 'unspecified'}"
            + (f"; notes: {i['notes']}" if i.get("notes") else "")
            + ")"
            for i in items
        )
        system = (
            "You are a friendly thrift-fashion stylist. Be specific and concise. "
            "Only reference wardrobe pieces from the list you are given, by name."
        )
        prompt = (
            f"A shopper is considering this secondhand item:\n{item_text}\n\n"
            f"Their current wardrobe:\n{wardrobe_lines}\n\n"
            "Suggest one or two outfits that combine the new item with specific "
            "pieces they already own, naming those pieces exactly as listed. "
            "Add one line on why each outfit works."
        )

    response = generate(prompt, system=system)
    if not response or not response.strip():
        return (
            f"Couldn't generate outfit suggestions for "
            f"{new_item.get('title', 'this item')} right now. Try again."
        )
    return response


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    title = new_item.get("title", "this item")
    if not outfit or not outfit.strip():
        return (
            f"Can't write a fit card for {title} without an outfit suggestion. "
            "Generate an outfit first, then try again."
        )

    price = new_item.get("price")
    price_text = f"${price:g}" if isinstance(price, (int, float)) else "unlisted price"
    platform = new_item.get("platform") or "a resale app"
    tags = ", ".join(new_item.get("style_tags") or []) or "unspecified"

    system = (
        "You write captions for thrift-fit posts. Sound like a real person "
        "posting to friends, not a product description. No hashtag spam; at "
        "most one emoji."
    )
    prompt = (
        f"Item: {title}\n"
        f"Price: {price_text}\n"
        f"Platform: {platform}\n"
        f"Style tags: {tags}\n"
        f"Outfit idea:\n{outfit}\n\n"
        "Write a two-to-four sentence caption for a post about this find. "
        "Mention the item, its price and the platform exactly once each, and "
        "be specific about the vibe. Return only the caption."
    )

    # cache=False so repeated runs on the same inputs produce fresh captions.
    response = generate(prompt, system=system, cache=False)
    if not response or not response.strip():
        return f"Couldn't generate a fit card for {title} right now. Try again."
    return response.strip()
