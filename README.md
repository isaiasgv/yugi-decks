# yugi-decks

Canon Yu-Gi-Oh! decks for [Project Ignis (EDOPro)](https://github.com/edo9300/edopro), organized by anime/manga era.

Each `.ydk` file is a playable deck reflecting what the character actually used on screen. All passcodes are validated against [BabelCDB](https://github.com/ProjectIgnis/BabelCDB) (the same card database EDOPro ships with), so every card resolves correctly.

## Contents

52 character decks across seven eras:

| Era | Series | Decks |
|---|---|---|
| **DM** | Duel Monsters (1998-2004) | 19 |
| **GX** | Yu-Gi-Oh! GX (2004-2008) | 9 |
| **5Ds** | Yu-Gi-Oh! 5D's (2008-2011) | 8 |
| **Zexal** | Yu-Gi-Oh! Zexal (2011-2014) | 3 |
| **ArcV** | Yu-Gi-Oh! Arc-V (2014-2018) | 6 |
| **VRAINS** | Yu-Gi-Oh! VRAINS (2017-2019) | 4 |
| **Rush** | Sevens / Go Rush!! (2020+) | 3 |

### Deck list

#### DM (`decks/dm/`)
Atem (DSOD), Atem (Memory World), Bakura (Occult), Ishizu (Spirits), Joey (Battle City), Joey (Doma Hermos), Joey (Duelist Kingdom), Kaiba (Battle City), Kaiba (DSOD Modern), Kaiba (Doma), Kaiba (Duelist Kingdom), Mai (Harpies), Marik (Battle City), Pegasus (Toons), Yugi (Battle City), Yugi (Doma), Yugi (Duelist Kingdom), Yugi (Final Duel), Yugi (Manga Final)

#### GX (`decks/gx/`)
Aster (Destiny HERO), Atticus (Red-Eyes Darkness), Bastion (Element), Chazz (Ojama VWXYZ), Dark Jaden (Evil HERO), Jaden (HEROes), Jaden (Neos), Yubel, Zane (Cyber Dragon)

#### 5D's (`decks/5ds/`)
Akiza (Black Rose), Aporia (Meklord), Crow (Blackwing), Jack (Resonator), Leo (Morphtronic), Luna (Ancient Fairy), Yusei (Quasar), Yusei (Synchron)

#### Zexal (`decks/zexal/`)
Kaito (Galaxy-Eyes), Yuma (Numbers), Yuma (ZEXAL II)

#### Arc-V (`decks/arcv/`)
Yugo (Speedroid), Yuri (Predaplant), Yuto (Phantom Knights), Yuya (Magicians), Yuya (Performapal), Z-ARC (Supreme King)

#### VRAINS (`decks/vrains/`)
Aoi (Trickstar), Revolver (Rokket), Yusaku (Code Talker), Yusaku (Cyberse)

#### Rush Duel (`decks/rush/`)
Yuga (Sevens Road), Yudias (Galactica), Yuhi (Voidvelg)

## Install

Drop any `.ydk` file into your EDOPro `deck` folder:

```
C:\ProjectIgnis\deck\
```

Restart EDOPro (or just open the deck editor) and the deck appears in the dropdown.

To bulk-install everything, copy all `.ydk` files from this repo to the EDOPro deck folder:

```powershell
Copy-Item -Recurse decks\*\*.ydk C:\ProjectIgnis\deck\
```

## Playing canon decks

Most pre-VRAINS decks use cards that are forbidden under modern banlists (Pot of Greed, Card of Sanctity, Crush Card Virus, Future Fusion, etc.). To play them as the show portrayed:

1. **Banlist:** set to `No List` when you create a duel room.
2. **Allowed Cards:** set to `With anime cards` so cards like the Three Egyptian Gods are playable.
3. For Rush Duel decks, change **Mode** to `Rush Duel`.

For more historically-accurate format play, EDOPro ships with three frozen-in-time banlists:
- **GOAT** (April 2005) - end of original DM era
- **Edison** (March 2010) - GX era
- **HAT** (September 2014) - early Synchro era

## Notes on canon accuracy

A handful of anime-only cards do not exist in the TCG/OCG and were either substituted with their closest legal equivalent or omitted. Examples:

- Marik's torture-themed cards (Plasma Eel, Mechanical Spider) - omitted, no real-world print.
- Yusaku's *Storm Access* random draws - omitted.
- Wisel/Skiel/Granel parts (Aporia) - never released individually, deck uses the full Emperors and Armies only.
- Anime-only Phantom Knights / Predaplants that didn't get printed - omitted.

Egyptian Gods, ZEXAL Hopes, Z-ARC, etc. are present.

## Build scripts

The Python scripts in `scripts/` re-generate the `.ydk` files from card-name lists by looking up passcodes in `cards.cdb`.

To regenerate or modify a deck:

```bash
# Clone BabelCDB locally
git clone --depth 1 https://github.com/ProjectIgnis/BabelCDB.git /tmp/BabelCDB

# Edit the deck definitions in the script (top of file)
# Run the script to emit fresh .ydk files
python3 scripts/build_decks.py
```

The scripts:
- `build_decks.py` - the original 13 protagonist decks
- `build_more_decks.py` - 19 supporting characters (villains, rivals, etc.)
- `build_variant_decks.py` - 20 deck variants per protagonist (DK Yugi, DSOD Kaiba, Z-ARC, Quasar, etc.) plus Rush Duel decks

Each script outputs to `/sessions/.../mnt/outputs/decks/` by default - tweak `OUT_DIR` at the top to change destination.

## File format

`.ydk` files are plain text:

```
#created by author
#main
46986414         <- Dark Magician (passcode)
46986414
46986414
#extra
1136639          <- Dark Paladin
!side
```

Each line under `#main`, `#extra`, or `!side` is one card passcode. Duplicate the line to include multiple copies.

## License

The card data is (c) Konami. This repo only contains deck lists (passcode references). Card images, scripts, and the simulator itself come from Project Ignis.
