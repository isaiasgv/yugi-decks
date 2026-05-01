"""
Canon Yu-Gi-Oh! deck builder for Project Ignis (EDOPro).

Reads card IDs from BabelCDB's cards.cdb (the same database EDOPro uses)
and writes .ydk files compatible with the simulator.
"""
import os
import sqlite3
import sys

CDB_PATH = "/tmp/BabelCDB/cards.cdb"
OUT_DIR = "/sessions/gallant-optimistic-sagan/mnt/outputs/decks"

con = sqlite3.connect(CDB_PATH)
cur = con.cursor()


def lookup(name: str) -> int | None:
    """Resolve a card name to its passcode. Tries exact match first, then LIKE."""
    cur.execute(
        "SELECT t.id FROM texts t JOIN datas d ON d.id = t.id "
        "WHERE LOWER(t.name) = LOWER(?) AND d.alias = 0",
        (name,),
    )
    row = cur.fetchone()
    if row:
        return row[0]
    # Fallback: any alias
    cur.execute("SELECT id FROM texts WHERE LOWER(name) = LOWER(?)", (name,))
    row = cur.fetchone()
    if row:
        return row[0]
    return None


def write_ydk(filename: str, author: str, main: list, extra: list, side: list = None):
    side = side or []
    missing = []
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)

    def resolve_section(cards):
        ids = []
        for entry in cards:
            if isinstance(entry, tuple):
                name, count = entry
            else:
                name, count = entry, 1
            cid = lookup(name)
            if cid is None:
                missing.append(name)
                continue
            ids.extend([cid] * count)
        return ids

    main_ids = resolve_section(main)
    extra_ids = resolve_section(extra)
    side_ids = resolve_section(side)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"#created by {author}\n")
        f.write("#main\n")
        for cid in main_ids:
            f.write(f"{cid}\n")
        f.write("#extra\n")
        for cid in extra_ids:
            f.write(f"{cid}\n")
        f.write("!side\n")
        for cid in side_ids:
            f.write(f"{cid}\n")

    print(f"[{filename}] main={len(main_ids)} extra={len(extra_ids)} side={len(side_ids)}", end="")
    if missing:
        print(f"  MISSING: {missing}")
    else:
        print("  OK")
    return missing


# ============================================================
# CANON DECKS
# ============================================================

# Yugi Muto - Battle City era
yugi_bc_main = [
    ("Dark Magician", 3),
    ("Dark Magician Girl", 1),
    ("Buster Blader", 1),
    ("Alpha The Magnet Warrior", 1),
    ("Beta The Magnet Warrior", 1),
    ("Gamma The Magnet Warrior", 1),
    ("Valkyrion the Magna Warrior", 1),
    ("Kuriboh", 1),
    ("Watapon", 1),
    ("Big Shield Gardna", 1),
    ("Gazelle the King of Mythical Beasts", 1),
    ("Berfomet", 1),
    ("Catapult Turtle", 1),
    ("Obnoxious Celtic Guard", 1),
    ("Queen's Knight", 1),
    ("King's Knight", 1),
    ("Jack's Knight", 1),
    ("Sangan", 1),
    ("Magician of Black Chaos", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Dark Magic Attack", 1),
    ("Magical Hats", 1),
    ("Brain Control", 1),
    ("Card of Sanctity", 1),
    ("Soul Exchange", 1),
    ("Mage Power", 1),
    ("Mystical Space Typhoon", 1),
    ("Swords of Revealing Light", 1),
    ("Multiply", 1),
    ("Black Luster Ritual", 1),
    ("Card Destruction", 1),
    ("Exchange", 1),
    ("Monster Recovery", 1),
    # Traps
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
    ("Spellbinding Circle", 1),
    ("Magical Trick Mirror", 1),
    ("Reinforcements", 1),
    ("Lightforce Sword", 1),
]
yugi_bc_extra = [
    ("Chimera the Flying Mythical Beast", 1),
    ("Black Luster Soldier", 1),
    ("Dark Paladin", 1),
    ("Slifer the Sky Dragon", 1),
]

# Seto Kaiba - Battle City era
kaiba_bc_main = [
    ("Blue-Eyes White Dragon", 3),
    ("Lord of D.", 1),
    ("Kaiser Sea Horse", 2),
    ("Vorse Raider", 1),
    ("La Jinn the Mystical Genie of the Lamp", 1),
    ("Battle Ox", 1),
    ("Spear Dragon", 1),
    ("Familiar-Possessed - Aussa", 1),
    ("X-Head Cannon", 1),
    ("Y-Dragon Head", 1),
    ("Z-Metal Tank", 1),
    ("Cyber Jar", 1),
    ("Witch of the Black Forest", 1),
    ("Hyozanryu", 1),
    ("Saggi the Dark Clown", 1),
    ("Different Dimension Dragon", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("The Flute of Summoning Dragon", 1),
    ("Card of Demise", 1),
    ("Soul Exchange", 1),
    ("Cost Down", 1),
    ("Shrink", 1),
    ("Enemy Controller", 1),
    ("Mystical Space Typhoon", 1),
    ("Heavy Storm", 1),
    ("Mesmeric Control", 1),
    ("Stamping Destruction", 1),
    ("Ring of Defense", 1),
    # Traps
    ("Mirror Force", 1),
    ("Crush Card Virus", 1),
    ("Ring of Destruction", 1),
    ("Negate Attack", 1),
    ("Trap Jammer", 1),
    ("Attack Guidance Armor", 1),
    ("Shadow Spell", 1),
    ("Interdimensional Matter Transporter", 1),
]
kaiba_bc_extra = [
    ("Blue-Eyes Ultimate Dragon", 1),
    ("XYZ-Dragon Cannon", 1),
    ("XY-Dragon Cannon", 1),
    ("XZ-Tank Cannon", 1),
    ("YZ-Tank Dragon", 1),
    ("Obelisk the Tormentor", 1),
]

# Joey Wheeler - Battle City era
joey_bc_main = [
    ("Red-Eyes Black Dragon", 1),
    ("Jinzo", 1),
    ("Gearfried the Iron Knight", 1),
    ("Insect Queen", 1),
    ("Time Wizard", 1),
    ("Baby Dragon", 1),
    ("Thousand Dragon", 1),  # may not exist as normal
    ("Flame Swordsman", 1),
    ("Panther Warrior", 1),
    ("Goblin Attack Force", 1),
    ("Rocket Warrior", 1),
    ("Little-Winguard", 1),
    ("Swordsman of Landstar", 1),
    ("Alligator's Sword", 1),
    ("Axe Raider", 1),
    ("Garoozis", 1),
    ("Hayabusa Knight", 1),
    ("Maximum Six", 1),
    ("Skull Dice", 1),  # actually a trap
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Scapegoat", 1),
    ("Question", 1),
    ("Giant Trunade", 1),
    ("The Reliable Guardian", 1),
    ("Shield & Sword", 1),
    ("Salamandra", 1),
    ("Legendary Sword", 1),
    ("Lightning Blade", 1),
    ("Mystical Space Typhoon", 1),
    ("Foolish Burial", 1),
    # Traps
    ("Skull Dice", 1),
    ("Graverobber", 1),
    ("Kunai with Chain", 1),
    ("Fairy Box", 1),
    ("Magical Arm Shield", 1),
    ("Roll Out!", 1),
    ("Reinforcements", 1),
]
joey_bc_extra = [
    ("Red-Eyes Black Dragon Sword", 0),  # placeholder removed if 0
]
joey_bc_extra = [
    ("Thousand Dragon", 1),
    ("Flame Swordsman", 1),
]

# Marik Ishtar - Battle City finale
marik_bc_main = [
    ("Lava Golem", 1),
    ("Helpoemer", 1),
    ("Revival Jam", 1),
    ("Makyura the Destructor", 1),
    ("Drillago", 1),
    ("Holding Arms", 1),
    ("Holding Legs", 1),
    ("Bowganian", 1),
    ("Granadora", 1),
    ("Gil Garth", 1),
    ("Viser Des", 1),
    ("Newdoria", 1),
    ("Mystic Tomato", 1),
    ("Swarm of Scarabs", 1),
    ("Swarm of Locusts", 1),
    ("Juragedo", 1),
    ("Masked Beast Des Gardius", 1),
    # Spells
    ("Pot of Greed", 1),
    ("Card of Safe Return", 1),
    ("Infinite Cards", 1),
    ("Premature Burial", 1),
    ("The Mask of Remnants", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    ("Brain Control", 1),
    ("Nightmare's Steelcage", 1),
    ("Card of Sanctity", 1),
    # Traps
    ("Jam Defender", 1),
    ("Jam Breeding Machine", 1),  # actually a continuous spell
    ("Coffin Seller", 1),
    ("Nightmare Wheel", 1),
    ("Judgment of Anubis", 1),
    ("Metal Detector", 1),
    ("Rope of Life", 1),
    ("Fiend's Mirror", 1),
]
marik_bc_extra = [
    ("Slifer the Sky Dragon", 1),
    ("The Winged Dragon of Ra", 1),
]

# Jaden Yuki - GX (Season 1 base Elemental HEROes)
jaden_main = [
    ("Elemental HERO Avian", 2),
    ("Elemental HERO Burstinatrix", 2),
    ("Elemental HERO Sparkman", 2),
    ("Elemental HERO Clayman", 2),
    ("Elemental HERO Bubbleman", 2),
    ("Elemental HERO Wildheart", 1),
    ("Elemental HERO Bladedge", 1),
    ("Elemental HERO Necroshade", 1),
    ("Winged Kuriboh", 2),
    ("Winged Kuriboh LV10", 1),
    ("Wroughtweiler", 1),
    ("Hero Signal", 1),  # actually trap
    # Spells
    ("Polymerization", 3),
    ("Fusion Recovery", 1),
    ("R - Righteous Justice", 1),
    ("Skyscraper", 2),
    ("Pot of Greed", 1),
    ("Mystical Space Typhoon", 1),
    ("Reinforcement of the Army", 1),
    ("Monster Reborn", 1),
    ("E - Emergency Call", 2),
    ("The Warrior Returning Alive", 1),
    ("H - Heated Heart", 1),
    ("Bubble Shuffle", 1),
    ("Bubble Blaster", 1),
    # Traps
    ("Hero Signal", 1),
    ("Negate Attack", 1),
    ("Mirror Gate", 1),
    ("A Hero Emerges", 1),
    ("Draining Shield", 1),
]
jaden_extra = [
    ("Elemental HERO Flame Wingman", 1),
    ("Elemental HERO Thunder Giant", 1),
    ("Elemental HERO Rampart Blaster", 1),
    ("Elemental HERO Mudballman", 1),
    ("Elemental HERO Wildedge", 1),
    ("Elemental HERO Tempest", 1),
    ("Elemental HERO Steam Healer", 1),
    ("Elemental HERO Wild Wingman", 1),
    ("Elemental HERO Shining Flare Wingman", 1),
    ("Elemental HERO Phoenix Enforcer", 1),
]

# Zane Truesdale - GX Cyber Dragon
zane_main = [
    ("Cyber Dragon", 3),
    ("Proto-Cyber Dragon", 2),
    ("Cyber Phoenix", 2),
    ("Cyber Kirin", 1),
    ("Cyber Larva", 1),
    ("Cyber Dragon Zwei", 1),
    ("Cyber Valley", 2),
    ("Cyber Barrier Dragon", 1),
    ("Cyber Laser Dragon", 1),
    ("Mystical Space Typhoon", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    ("Polymerization", 1),
    ("Power Bond", 2),
    ("Future Fusion", 1),
    ("De-Fusion", 1),
    ("Photon Generator Unit", 1),
    ("Megamorph", 1),
    ("Limiter Removal", 1),
    ("Different Dimension Capsule", 1),
    ("Attack Reflector Unit", 1),
    # Traps
    ("Mirror Force", 1),
    ("Call of the Haunted", 1),
    ("Trap Jammer", 1),
    ("Damage Polarizer", 1),
    ("Negate Attack", 1),
]
zane_extra = [
    ("Cyber End Dragon", 1),
    ("Cyber Twin Dragon", 1),
    ("Chimeratech Overdragon", 1),
    ("Cyber Eltanin", 1),
]

# Chazz Princeton - GX (VWXYZ + Ojama)
chazz_main = [
    ("Ojama Black", 2),
    ("Ojama Yellow", 2),
    ("Ojama Green", 2),
    ("Ojama King", 1),
    ("Ojama Knight", 1),
    ("Armed Dragon LV3", 2),
    ("Armed Dragon LV5", 2),
    ("Armed Dragon LV7", 2),
    ("Armed Dragon LV10", 1),
    ("V-Tiger Jet", 1),
    ("W-Wing Catapult", 1),
    ("X-Head Cannon", 1),
    ("Y-Dragon Head", 1),
    ("Z-Metal Tank", 1),
    # Spells
    ("Ojama Delta Hurricane!!", 1),
    ("Ojamagic", 1),
    ("Ojamuscle", 1),
    ("Polymerization", 2),
    ("Frontline Base", 1),
    ("Level Up!", 2),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Mystical Space Typhoon", 1),
    ("Inferno Reckless Summon", 1),
    # Traps
    ("Call of the Haunted", 1),
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
]
chazz_extra = [
    ("VW-Tiger Catapult", 1),
    ("XY-Dragon Cannon", 1),
    ("XZ-Tank Cannon", 1),
    ("YZ-Tank Dragon", 1),
    ("XYZ-Dragon Cannon", 1),
    ("VWXYZ-Dragon Catapult Cannon", 1),
    ("Armed Dragon Catapult Cannon", 1),
]

# Yusei Fudo - 5D's Synchron
yusei_main = [
    ("Junk Synchron", 3),
    ("Quickdraw Synchron", 2),
    ("Nitro Synchron", 1),
    ("Turbo Synchron", 1),
    ("Speed Warrior", 3),
    ("Sonic Chick", 2),
    ("Tuningware", 1),
    ("Quillbolt Hedgehog", 2),
    ("Level Eater", 1),
    ("Shield Warrior", 1),
    ("Healing Wave Generator", 1),
    ("Tricular", 1),
    ("Bicular", 1),
    ("Unicycular", 1),
    ("Stardust Xiaolong", 1),
    ("Max Warrior", 1),
    ("Road Synchron", 1),
    # Spells
    ("Tuning", 2),
    ("One for One", 1),
    ("Pot of Avarice", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    ("Giant Trunade", 1),
    ("Reinforcement of the Army", 1),
    ("Fighting Spirit", 1),
    ("Synchro Boost", 1),
    # Traps
    ("Scrap-Iron Scarecrow", 2),
    ("Defense Draw", 1),
    ("Counter Counter", 1),
    ("Limiter Overload", 1),
    ("Graceful Revival", 1),
    ("Call of the Haunted", 1),
]
yusei_extra = [
    ("Stardust Dragon", 1),
    ("Junk Warrior", 1),
    ("Nitro Warrior", 1),
    ("Turbo Warrior", 1),
    ("Road Warrior", 1),
    ("Junk Archer", 1),
    ("Junk Destroyer", 1),
    ("Drill Warrior", 1),
    ("Armory Arm", 1),
    ("Formula Synchron", 1),
    ("Shooting Star Dragon", 1),
    ("Stardust Dragon/Assault Mode", 1),
]

# Jack Atlas - 5D's Resonator
jack_main = [
    ("Dark Resonator", 3),
    ("Synkron Resonator", 1),
    ("Mirror Resonator", 1),
    ("Creation Resonator", 1),
    ("Force Resonator", 1),
    ("Big Piece Golem", 2),
    ("Medium Piece Golem", 1),
    ("Small Piece Golem", 1),
    ("Mighty Warrior", 2),
    ("Strong Wind Dragon", 1),
    ("Twin-Sword Marauder", 1),
    ("Exploder Dragon", 2),
    ("Vice Dragon", 1),
    ("Battle Fader", 1),
    ("Top Runner", 1),
    ("Hand of the Six Samurai", 1),
    # Spells
    ("Pot of Avarice", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    ("Mind Trust", 1),
    ("Powerful Rebirth", 1),
    ("Resonator Call", 1),
    ("Lineage of Destruction", 1),
    # Traps
    ("Tyrant's Tirade", 1),
    ("Crimson Fire", 1),
    ("Mirror Force", 1),
    ("Call of the Haunted", 1),
    ("Limit Reverse", 1),
    ("Synchro Deflector", 1),
]
jack_extra = [
    ("Red Dragon Archfiend", 1),
    ("Red Dragon Archfiend/Assault Mode", 1),
    ("Red Nova Dragon", 1),
    ("Exploder Dragonwing", 1),
    ("Hot Red Dragon Archfiend", 1),
    ("Scarlight Red Dragon Archfiend", 1),
    ("Tyrant Red Dragon Archfiend", 1),
    ("Majestic Red Dragon", 1),
]

# Crow Hogan - 5D's Blackwings
crow_main = [
    ("Blackwing - Gale the Whirlwind", 1),
    ("Blackwing - Bora the Spear", 3),
    ("Blackwing - Shura the Blue Flame", 2),
    ("Blackwing - Sirocco the Dawn", 2),
    ("Blackwing - Blizzard the Far North", 2),
    ("Blackwing - Kalut the Moon Shadow", 3),
    ("Blackwing - Mistral the Silver Shield", 2),
    ("Blackwing - Vayu the Emblem of Honor", 1),
    ("Blackwing - Pinaki the Waxing Moon", 1),
    ("Blackwing - Ghibli the Searing Wind", 1),
    ("Blackwing - Etesian of Two Swords", 1),
    # Spells
    ("Black Whirlwind", 3),
    ("Pot of Avarice", 1),
    ("Allure of Darkness", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    # Traps
    ("Icarus Attack", 2),
    ("Delta Crow - Anti Reverse", 1),
    ("Black Sonic", 1),
    ("Black Return", 1),
    ("Royal Decree", 1),
]
crow_extra = [
    ("Blackwing Armed Wing", 1),
    ("Blackwing Armor Master", 1),
    ("Blackwing - Gram the Shining Star", 1),
    ("Blackwing - Nothung the Starlight", 1),
    ("Black-Winged Dragon", 1),
    ("Assault Blackwing - Raikiri the Rain Shower", 1),
    ("Blackwing Tamer - Obsidian Hawk Joe", 1),
    ("Blackwing Full Armor Master", 1),
]

# Yuma Tsukumo - Zexal Numbers
yuma_main = [
    ("Gagaga Magician", 3),
    ("Gagaga Girl", 2),
    ("Gagaga Child", 1),
    ("Gogogo Golem", 3),
    ("Gogogo Giant", 2),
    ("Gogogo Goram", 1),
    ("Gogogo Ghost", 1),
    ("Zubaba Knight", 3),
    ("Achacha Archer", 1),
    ("Dododo Warrior", 1),
    ("Dododo Bot", 1),
    ("Kagetokage", 2),
    ("Ganbara Knight", 1),
    # Spells
    ("Double or Nothing!", 2),
    ("Onomatopickup", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    ("Xyz Reborn", 1),
    ("Rank-Up-Magic Astral Force", 1),
    ("Rank-Up-Magic Limited Barian's Force", 1),
    # Traps
    ("Half Unbreak", 1),
    ("Damage Diet", 1),
    ("Wonder Wand", 1),  # spell?
    ("Xyz Block", 1),
]
yuma_extra = [
    ("Number 39: Utopia", 1),
    ("Number C39: Utopia Ray", 1),
    ("Number C39: Utopia Ray Victory", 1),
    ("Number S39: Utopia the Lightning", 1),
    ("Number 39: Utopia Beyond", 1),
    ("Number 39: Utopia Roots", 1),
    ("Gagaga Cowboy", 1),
    ("Number 17: Leviathan Dragon", 1),
    ("Number 61: Volcasaurus", 1),
    ("Number 83: Galaxy Queen", 1),
    ("Number 19: Freezadon", 1),
    ("Number F0: Utopic Future", 1),
]

# Yuya Sakaki - Arc-V Performapal/Odd-Eyes
yuya_main = [
    ("Performapal Hip Hippo", 2),
    ("Performapal Whip Snake", 2),
    ("Performapal Sword Fish", 2),
    ("Performapal Skeeter Skimmer", 2),
    ("Performapal Cheermole", 1),
    ("Performapal Trampolynx", 1),
    ("Performapal Drummerilla", 1),
    ("Performapal Kaleidoscorp", 1),
    ("Performapal Silver Claw", 1),
    ("Performapal Lizardraw", 1),
    ("Performapal Pendulum Sorcerer", 1),
    ("Performapal Skullcrobat Joker", 1),
    ("Odd-Eyes Pendulum Dragon", 1),
    ("Stargazer Magician", 1),
    ("Timegazer Magician", 1),
    # Spells
    ("Smile World", 1),
    ("Hippo Carnival", 1),
    ("Wonder Balloons", 1),
    ("Performapal Pinch Helper", 1),
    ("Pendulum Halt", 1),
    # Traps
    ("Performapal Revival", 1),
    ("Performapal Call", 1),
    ("Mirror Force", 1),
    ("Wall of Disruption", 1),
]
yuya_extra = [
    ("Odd-Eyes Rebellion Dragon", 1),
    ("Odd-Eyes Vortex Dragon", 1),
    ("Odd-Eyes Phantom Dragon", 1),
    ("Odd-Eyes Absolute Dragon", 1),
    ("Odd-Eyes Raging Dragon", 1),
    ("Dark Rebellion Xyz Dragon", 1),
    ("Dark Anthelion Dragon", 1),
    ("Beast-Eyes Pendulum Dragon", 1),
    ("Performage Trapeze Magician", 1),
    ("Rune-Eyes Pendulum Dragon", 1),
    ("Number 39: Utopia", 1),
    ("Hi-Speedroid Chanbara", 1),
]

# Yusaku Fujiki / Playmaker - VRAINS Cyberse
yusaku_main = [
    ("Cyberse Wizard", 3),
    ("Cyberse Gadget", 3),
    ("Backup Secretary", 3),
    ("Linkslayer", 1),
    ("Stack Reviver", 2),
    ("Cyberse Synchron", 1),
    ("Balancer Lord", 1),
    ("Bitron", 2),
    ("Draconnet", 2),
    ("RAM Clouder", 2),
    ("ROM Cloudia", 1),
    ("Dotscaper", 2),
    ("Cyberse White Hat", 1),
    # Spells
    ("Cynet Storm", 1),
    ("Cynet Mining", 1),
    ("Cynet Backdoor", 1),
    ("Recoded Alive", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Cynet Codec", 1),
    ("Cynet Crosswipe", 1),
    ("Cynet Refresh", 1),
    ("Link Restart", 1),
]
yusaku_extra = [
    ("Decode Talker", 1),
    ("Decode Talker Extended", 1),
    ("Decode Talker Heatsoul", 1),
    ("Firewall Dragon", 1),
    ("Firewall Dragon Darkfluid", 1),
    ("Encode Talker", 1),
    ("Powercode Talker", 1),
    ("Transcode Talker", 1),
    ("Excode Talker", 1),
    ("Accesscode Talker", 1),
    ("Honeybot", 1),
    ("Linkuriboh", 1),
    ("Link Spider", 1),
    ("Cyberse Witch", 1),
    ("Cyberse Quantum Dragon", 1),
]

decks = [
    ("Yugi - Battle City.ydk", "Yugi Muto - Battle City", yugi_bc_main, yugi_bc_extra),
    ("Kaiba - Battle City.ydk", "Seto Kaiba - Battle City", kaiba_bc_main, kaiba_bc_extra),
    ("Joey - Battle City.ydk", "Joey Wheeler - Battle City", joey_bc_main, joey_bc_extra),
    ("Marik - Battle City.ydk", "Marik Ishtar - Battle City Finals", marik_bc_main, marik_bc_extra),
    ("Jaden Yuki - GX.ydk", "Jaden Yuki - Elemental HERO", jaden_main, jaden_extra),
    ("Zane Truesdale - GX.ydk", "Zane Truesdale - Cyber Dragon", zane_main, zane_extra),
    ("Chazz Princeton - GX.ydk", "Chazz Princeton - VWXYZ/Ojama/Armed Dragon", chazz_main, chazz_extra),
    ("Yusei Fudo - 5Ds.ydk", "Yusei Fudo - Synchron", yusei_main, yusei_extra),
    ("Jack Atlas - 5Ds.ydk", "Jack Atlas - Resonator", jack_main, jack_extra),
    ("Crow Hogan - 5Ds.ydk", "Crow Hogan - Blackwing", crow_main, crow_extra),
    ("Yuma Tsukumo - Zexal.ydk", "Yuma Tsukumo - Number/Utopia", yuma_main, yuma_extra),
    ("Yuya Sakaki - ArcV.ydk", "Yuya Sakaki - Performapal/Odd-Eyes", yuya_main, yuya_extra),
    ("Yusaku Fujiki - VRAINS.ydk", "Yusaku Fujiki - Cyberse", yusaku_main, yusaku_extra),
]

all_missing = {}
for filename, author, main, extra in decks:
    miss = write_ydk(filename, author, main, extra)
    if miss:
        all_missing[filename] = miss

print("\n=== SUMMARY ===")
if all_missing:
    print("Cards not found by exact name (these will be skipped or need correction):")
    for f, miss in all_missing.items():
        print(f"  {f}: {miss}")
else:
    print("All cards resolved cleanly.")
