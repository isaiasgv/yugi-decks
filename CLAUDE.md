# CLAUDE.md

Context for AI assistants working in this repo.

## What this is

A collection of canon Yu-Gi-Oh! anime/manga decks as `.ydk` files for the [Project Ignis EDOPro](https://github.com/edo9300/edopro) simulator. Each deck reflects what a specific character used on screen during a specific story arc.

The user (Isaias) plays Yu-Gi-Oh! casually using EDOPro. He installs to `C:\ProjectIgnis\` on Windows. He's a .NET / C# / Blazor / SQL developer, so technical explanations and code examples are welcome.

## Repo layout

```
yugi-decks/
├── README.md              ← User-facing readme
├── CLAUDE.md              ← This file
├── decks/
│   ├── dm/                ← Duel Monsters era (Yugi, Kaiba, Joey, Marik, Pegasus, ...)
│   ├── gx/                ← GX (Jaden, Zane, Chazz, Aster, ...)
│   ├── 5ds/               ← 5D's (Yusei, Jack, Crow, Akiza, ...)
│   ├── zexal/             ← Zexal (Yuma, Kaito)
│   ├── arcv/              ← Arc-V (Yuya, Yuto, Yugo, Yuri, Z-ARC)
│   ├── vrains/            ← VRAINS (Yusaku, Revolver, Aoi)
│   └── rush/              ← Rush Duel (Sevens / Go Rush!!)
└── scripts/
    ├── build_decks.py           ← Original 13 protagonist decks
    ├── build_more_decks.py      ← 19 supporting characters
    └── build_variant_decks.py   ← 20 protagonist deck variants + Rush Duel decks
```

Filename convention: `Character (Theme or Arc).ydk`. Examples:
- `Yugi (Battle City).ydk`
- `Kaiba (DSOD Modern).ydk`
- `Yuya (Performapal).ydk`
- `Z-ARC (Supreme King).ydk`

## .ydk file format

Plain text. Three sections:

```
#created by Author Name
#main
[8-digit passcode]
[8-digit passcode]
...
#extra
[8-digit passcode]
...
!side
[8-digit passcode]
...
```

- Repeat the same passcode line to include multiple copies (max 3 of any card by default).
- Lines starting with `#` after the headers are ignored as comments.
- A passcode is a card's unique 8-digit ID. EDOPro looks it up in `cards.cdb`.

## Card database

Passcodes are validated against ProjectIgnis's [BabelCDB](https://github.com/ProjectIgnis/BabelCDB), specifically:

- `cards.cdb` - main TCG/OCG card database (SQLite)
- `cards-rush.cdb` - Rush Duel card database (separate)
- `cards-unofficial.cdb` - anime-only / unreleased cards

Schema:

```
texts(id, name, desc, str1..str16)
datas(id, ot, alias, setcode, type, atk, def, level, race, attribute, category)
```

`alias != 0` indicates a reprint variant (different art, same gameplay). When looking up by name, prefer rows where `alias = 0`.

To regenerate decks, the build scripts assume BabelCDB is cloned to `/tmp/BabelCDB/`:

```bash
git clone --depth 1 https://github.com/ProjectIgnis/BabelCDB.git /tmp/BabelCDB
```

## Adding a new deck

1. Choose the era folder (e.g., `decks/gx/`).
2. Easiest path: open the relevant `scripts/build_*.py`, add a new entry following the existing pattern (a list of `(card_name, count)` tuples for main and extra), and rerun the script.
3. Or write the `.ydk` file by hand if you already know the passcodes.

When the script runs, missing card names are listed at the end. Common reasons a name doesn't resolve:
- Anime-only card never released → omit it.
- Misspelling → look it up with `python3 -c "import sqlite3; ..."` queries against `texts` table.
- Card has prefix like `The`, `Number 39:`, or punctuation → match exactly as it appears in `cards.cdb`.

## Conventions

- **Strict canon by default.** Decks reflect what the character actually used on screen, not what's competitively strong. If the user wants a meta version, build it as a separate file (e.g., `Kaiba (DSOD Modern).ydk` is the modern competitive Blue-Eyes deck, distinct from `Kaiba (Battle City).ydk`).
- **Anime/manga-only cards:** if BabelCDB has them, include them. If not, drop the card (don't substitute silently — note it in the script comment).
- **Pot of Greed and friends:** include them in older era decks. The user is expected to play with `No List` banlist.
- **Egyptian Gods:** put in the Extra Deck slot of the relevant DM-era deck. They aren't summonable normally; user toggles "Allowed Cards: With anime cards" to use them.
- **Rush Duel decks:** prefix filename with `[Rush]` (or just live in `decks/rush/`). Use `cards-rush.cdb` for lookups, not `cards.cdb`. Different format - no Extra Deck.

## Common questions

**Why isn't a deck loading in EDOPro?**
A passcode referenced in the `.ydk` doesn't exist in the user's `cards.cdb`. They likely need to run the BabelCDB updater. Or a typo in the script - rerun the build script and look at the missing-card output.

**Banlist tells me a card is forbidden:**
Casual / anime banlist is `No List`. Modern competitive bans cards like Pot of Greed, Crush Card Virus, Maxx "C" (in TCG), etc.

**The user wants only one era's decks visible at a time:**
EDOPro reads everything in `C:\ProjectIgnis\deck\` flat. To filter by era, either:
1. Move unwanted era folders aside (manual)
2. Build a launcher script that swaps deck folders (we tried this and the user preferred all decks visible at once)
3. Use EDOPro's deck-editor search bar to type the character name

**The user is on .NET / Blazor:**
For tools/scripts, prefer PowerShell or .NET (C# console app, dotnet script) over Python where it makes sense. He'd appreciate idiomatic C# / Blazor solutions when building UI tooling around EDOPro.
