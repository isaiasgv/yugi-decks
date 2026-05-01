"""
Round 3: variant decks for main protagonists across each character's deck phases.
Includes Rush Duel decks (Sevens / Go Rush) using cards-rush.cdb.
"""
import os, sqlite3

CDB_NORMAL = "/tmp/BabelCDB/cards.cdb"
CDB_RUSH   = "/tmp/BabelCDB/cards-rush.cdb"
OUT_DIR    = "/sessions/gallant-optimistic-sagan/mnt/outputs/decks"

con_n = sqlite3.connect(CDB_NORMAL); cur_n = con_n.cursor()
con_r = sqlite3.connect(CDB_RUSH);   cur_r = con_r.cursor()

def lookup(name, rush=False):
    cur = cur_r if rush else cur_n
    cur.execute("SELECT t.id FROM texts t JOIN datas d ON d.id=t.id WHERE LOWER(t.name)=LOWER(?) AND d.alias=0", (name,))
    r = cur.fetchone()
    if r: return r[0]
    cur.execute("SELECT id FROM texts WHERE LOWER(name)=LOWER(?)", (name,))
    r = cur.fetchone()
    return r[0] if r else None

def write_ydk(filename, author, main, extra, side=None, rush=False):
    side = side or []
    missing = []
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)
    def resolve(cards):
        ids = []
        for e in cards:
            n, c = (e if isinstance(e, tuple) else (e, 1))
            cid = lookup(n, rush=rush)
            if cid is None: missing.append(n); continue
            ids.extend([cid]*c)
        return ids
    m, x, s = resolve(main), resolve(extra), resolve(side)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"#created by {author}\n#main\n")
        for cid in m: f.write(f"{cid}\n")
        f.write("#extra\n")
        for cid in x: f.write(f"{cid}\n")
        f.write("!side\n")
        for cid in s: f.write(f"{cid}\n")
    print(f"[{filename}] main={len(m)} extra={len(x)}", "OK" if not missing else f"MISSING:{missing}")
    return missing

# ============================================================
# YUGI / ATEM VARIANTS
# ============================================================

# 1. Duelist Kingdom era (early Yugi)
yugi_dk_main = [
    ("Dark Magician", 2),
    ("Gaia The Fierce Knight", 1),
    ("Curse of Dragon", 1),
    ("Mystical Elf", 1),
    ("Beaver Warrior", 1),
    ("Celtic Guardian", 1),
    ("Feral Imp", 1),
    ("Silver Fang", 1),
    ("Winged Dragon, Guardian of the Fortress #1", 1),
    ("Summoned Skull", 1),
    ("Kuriboh", 1),
    ("Big Shield Gardna", 1),
    ("Giant Soldier of Stone", 1),
    ("Mammoth Graveyard", 1),
    ("Dark Magician Girl", 1),
    ("Magician of Faith", 1),
    ("Sangan", 1),
    ("Witch of the Black Forest", 1),
    ("Catapult Turtle", 1),
    ("Exodia the Forbidden One", 1),
    ("Right Arm of the Forbidden One", 1),
    ("Left Arm of the Forbidden One", 1),
    ("Right Leg of the Forbidden One", 1),
    ("Left Leg of the Forbidden One", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Multiply", 1),
    ("Dark Hole", 1),
    ("Swords of Revealing Light", 1),
    ("Mystic Box", 1),
    ("Fissure", 1),
    ("Brain Control", 1),
    # Traps
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
    ("Spellbinding Circle", 1),
    ("Trap Hole", 1),
    ("Reinforcements", 1),
]
yugi_dk_extra = [
    ("Gaia the Dragon Champion", 1),
    ("Black Skull Dragon", 1),
]

# 2. Doma / Waking the Dragons arc
yugi_doma_main = [
    ("Dark Magician", 3),
    ("Dark Magician Girl", 1),
    ("Buster Blader", 1),
    ("Watapon", 1),
    ("Big Shield Gardna", 1),
    ("Kuriboh", 1),
    ("Beta The Magnet Warrior", 1),
    ("Alpha The Magnet Warrior", 1),
    ("Gamma The Magnet Warrior", 1),
    ("Queen's Knight", 1),
    ("King's Knight", 1),
    ("Jack's Knight", 1),
    ("Gazelle the King of Mythical Beasts", 1),
    ("Berfomet", 1),
    ("Sangan", 1),
    ("Catapult Turtle", 1),
    # Doma-specific cards
    ("Legendary Knight Timaeus", 1),
    ("Legendary Knight Hermos", 1),
    ("Legendary Knight Critias", 1),
    # Spells
    ("The Eye of Timaeus", 1),
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Card of Sanctity", 1),
    ("Mystical Space Typhoon", 1),
    ("Brain Control", 1),
    ("Magical Hats", 1),
    # Traps
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
    ("Spellbinding Circle", 1),
]
yugi_doma_extra = [
    ("Dark Paladin", 1),
    ("Amulet Dragon", 1),
    ("Mirror Force Dragon", 1),
    ("Timaeus the Knight of Destiny", 1),
]

# 3. Pharaoh Memory World - Atem's pharaonic deck (late Yugi w/ all 3 Gods)
atem_memory_main = [
    ("Dark Magician", 3),
    ("Dark Magician Girl", 1),
    ("Buster Blader", 1),
    ("Magician of Black Chaos", 1),
    ("Black Luster Soldier - Envoy of the Beginning", 1),
    ("Chaos Sorcerer", 1),
    ("Chaos Emperor Dragon - Envoy of the End", 1),
    ("Sky Dragoons of Draconia", 1),
    ("Spirit Ryu", 1),
    ("Mystical Beast of Serket", 1),
    ("Vorse Raider", 1),
    ("Marshmallon", 1),
    ("Watapon", 1),
    ("Kuriboh", 1),
    ("Sangan", 1),
    # Spells
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    ("Polymerization", 1),
    ("Card Destruction", 1),
    ("Card of Sanctity", 1),
    ("Soul Release", 1),
    ("Mystical Space Typhoon", 1),
    ("Black Luster Ritual", 1),
    ("Premature Burial", 1),
    # Traps
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
    ("Spellbinding Circle", 1),
    ("Magical Trick Mirror", 1),
]
atem_memory_extra = [
    ("Dark Paladin", 1),
    ("Black Luster Soldier", 1),
    ("Slifer the Sky Dragon", 1),
    ("Obelisk the Tormentor", 1),
    ("The Winged Dragon of Ra", 1),
    ("Ra's Disciple", 0),
]

# 4. Yugi's Final Deck (the deck Yugi uses against Atem in Ceremonial Duel)
yugi_final_main = [
    ("Dark Magician", 1),
    ("Dark Magician Girl", 1),
    ("Silent Magician LV4", 2),
    ("Silent Magician LV8", 1),
    ("Silent Swordsman LV3", 2),
    ("Silent Swordsman LV5", 1),
    ("Silent Swordsman LV7", 1),
    ("Big Shield Gardna", 1),
    ("Marshmallon", 1),
    ("Kuriboh", 1),
    ("Watapon", 1),
    ("Magician's Valkyria", 1),
    ("Sangan", 1),
    ("Gandora the Dragon of Destruction", 1),
    ("Skilled Dark Magician", 2),
    # Spells
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Polymerization", 1),
    ("Mystical Space Typhoon", 1),
    ("Brain Control", 1),
    ("Card of Sanctity", 1),
    ("Level Up!", 2),
    ("Magic Formula", 1),
    ("Dedication through Light and Darkness", 1),
    ("Diffusion Wave-Motion", 1),
    # Traps
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
    ("Magical Hats", 1),
    ("Last Will", 1),
    ("Magic Drain", 1),
]
yugi_final_extra = [
    ("Dark Paladin", 1),
    ("Dark Magician Knight", 1),
]

# 5. Dawn of the Duel manga — Yugi's manga ending deck (Black Luster era)
yugi_manga_main = [
    ("Dark Magician", 3),
    ("Dark Magician Girl", 1),
    ("Buster Blader", 1),
    ("Black Luster Soldier - Envoy of the Beginning", 1),
    ("Chaos Sorcerer", 1),
    ("Chaos Emperor Dragon - Envoy of the End", 1),
    ("Magician of Black Chaos", 1),
    ("Dark Magician of Chaos", 1),
    ("Magician of Faith", 1),
    ("Witch of the Black Forest", 1),
    ("Sangan", 1),
    ("Beta The Magnet Warrior", 1),
    ("Alpha The Magnet Warrior", 1),
    ("Gamma The Magnet Warrior", 1),
    ("Queen's Knight", 1),
    ("King's Knight", 1),
    ("Jack's Knight", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Card of Sanctity", 1),
    ("Black Luster Ritual", 1),
    ("Mystical Space Typhoon", 1),
    ("Brain Control", 1),
    # Traps
    ("Mirror Force", 1),
    ("Magic Cylinder", 1),
    ("Spellbinding Circle", 1),
]
yugi_manga_extra = [
    ("Black Luster Soldier", 1),
    ("Dark Paladin", 1),
    ("The Dark Magicians", 1),
]

# ============================================================
# KAIBA VARIANTS
# ============================================================

# 1. Duelist Kingdom Kaiba
kaiba_dk_main = [
    ("Blue-Eyes White Dragon", 3),
    ("Battle Ox", 1),
    ("La Jinn the Mystical Genie of the Lamp", 1),
    ("Mystic Horseman", 1),
    ("Saggi the Dark Clown", 1),
    ("Hitotsu-Me Giant", 1),
    ("Rude Kaiser", 1),
    ("Vorse Raider", 1),
    ("Judge Man", 1),
    ("Ancient Lamp", 1),
    ("Witch of the Black Forest", 1),
    ("Ryu-Kishin", 1),
    ("Krokodilus", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Dark Hole", 1),
    ("Mystical Space Typhoon", 1),
    ("Mountain", 1),
    ("Stop Defense", 1),
    # Traps
    ("Crush Card Virus", 1),
    ("Trap Master", 1),
    ("Reinforcements", 1),
]
kaiba_dk_extra = [
    ("Blue-Eyes Ultimate Dragon", 1),
]

# 2. Doma Kaiba
kaiba_doma_main = [
    ("Blue-Eyes White Dragon", 3),
    ("Lord of D.", 1),
    ("Kaiser Sea Horse", 2),
    ("Vorse Raider", 1),
    ("Different Dimension Dragon", 1),
    ("Pitch-Dark Dragon", 1),
    ("Spear Dragon", 1),
    ("Hyozanryu", 1),
    ("Cyber Jar", 1),
    ("Witch of the Black Forest", 1),
    ("Saggi the Dark Clown", 1),
    ("X-Head Cannon", 1),
    ("Y-Dragon Head", 1),
    ("Z-Metal Tank", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("The Flute of Summoning Dragon", 1),
    ("Soul Exchange", 1),
    ("Cost Down", 1),
    ("Shrink", 1),
    ("Enemy Controller", 1),
    ("Mystical Space Typhoon", 1),
    # Traps
    ("Mirror Force", 1),
    ("Crush Card Virus", 1),
    ("Ring of Destruction", 1),
    ("Negate Attack", 1),
]
kaiba_doma_extra = [
    ("Blue-Eyes Ultimate Dragon", 1),
    ("XYZ-Dragon Cannon", 1),
    ("XY-Dragon Cannon", 1),
    ("XZ-Tank Cannon", 1),
    ("YZ-Tank Dragon", 1),
]

# 3. Kaiba DSOD modern (the goldstandard Blue-Eyes deck)
kaiba_dsod_main = [
    ("Blue-Eyes White Dragon", 3),
    ("Blue-Eyes Alternative White Dragon", 3),
    ("Dragon Spirit of White", 1),
    ("Master with Eyes of Blue", 3),
    ("Maiden with Eyes of Blue", 1),
    ("Sage with Eyes of Blue", 1),
    ("Effect Veiler", 2),
    ("Kaibaman", 2),
    ("The White Stone of Ancients", 2),
    ("The White Stone of Legend", 2),
    ("Dragon Shrine", 2),
    ("The Melody of Awakening Dragon", 3),
    ("Trade-In", 2),
    ("Cards of Consonance", 2),
    ("Bingo Machine, Go!!!", 2),
    ("Return of the Dragon Lords", 2),
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
]
kaiba_dsod_extra = [
    ("Blue-Eyes Ultimate Dragon", 1),
    ("Blue-Eyes Twin Burst Dragon", 2),
    ("Neo Blue-Eyes Ultimate Dragon", 1),
    ("Blue-Eyes Spirit Dragon", 2),
    ("Azure-Eyes Silver Dragon", 1),
    ("Stardust Spark Dragon", 1),
    ("Crystal Wing Synchro Dragon", 1),
    ("Number 38: Hope Harbinger Dragon Titanic Galaxy", 1),
    ("Galaxy-Eyes Cipher Dragon", 1),
    ("Number 95: Galaxy-Eyes Dark Matter Dragon", 1),
    ("Daigusto Phoenix", 1),
    ("Number S0: Utopic ZEXAL", 1),
]

# ============================================================
# JOEY VARIANTS
# ============================================================

# 1. Duelist Kingdom Joey (no Red-Eyes yet)
joey_dk_main = [
    ("Time Wizard", 1),
    ("Baby Dragon", 1),
    ("Flame Swordsman", 1),
    ("Garoozis", 1),
    ("Battle Warrior", 1),
    ("Swordsman of Landstar", 1),
    ("Tiger Axe", 1),
    ("Axe Raider", 1),
    ("Alligator's Sword", 1),
    ("Panther Warrior", 1),
    ("Little-Winguard", 1),
    ("Masaki the Legendary Swordsman", 1),
    ("Rocket Warrior", 1),
    ("Goblin Attack Force", 1),
    ("Red-Eyes Black Dragon", 1),
    ("Kojikocy", 1),
    # Spells
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Scapegoat", 1),
    ("Salamandra", 1),
    ("Legendary Sword", 1),
    ("Lightning Blade", 1),
    ("Shield & Sword", 1),
    ("Giant Trunade", 1),
    ("The Reliable Guardian", 1),
    # Traps
    ("Skull Dice", 1),
    ("Graverobber", 1),
    ("Kunai with Chain", 1),
    ("Magical Arm Shield", 1),
    ("Time Machine", 1),
]
joey_dk_extra = [
    ("Thousand Dragon", 1),
]

# 2. Doma Joey (Hermos)
joey_doma_main = [
    ("Red-Eyes Black Dragon", 1),
    ("Time Wizard", 1),
    ("Baby Dragon", 1),
    ("Flame Swordsman", 1),
    ("Panther Warrior", 1),
    ("Gearfried the Iron Knight", 1),
    ("Insect Queen", 1),
    ("Jinzo", 1),
    ("Goblin Attack Force", 1),
    ("Rocket Warrior", 1),
    ("Little-Winguard", 1),
    ("Hayabusa Knight", 1),
    ("Alligator's Sword", 1),
    ("Axe Raider", 1),
    ("Legendary Knight Hermos", 1),
    # Hermos-equipped cards become equip spells in real game
    # Spells
    ("The Claw of Hermos", 1),
    ("Time Magic Hammer", 1),
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Scapegoat", 1),
    ("Mystical Space Typhoon", 1),
    ("Salamandra", 1),
    ("Legendary Sword", 1),
    ("Question", 1),
    # Traps
    ("Skull Dice", 1),
    ("Graverobber", 1),
    ("Magical Arm Shield", 1),
    ("Roll Out!", 1),
]
joey_doma_extra = [
    ("Thousand Dragon", 1),
]

# ============================================================
# JADEN VARIANTS
# ============================================================

# 1. Neos era Jaden (GX season 2)
jaden_neos_main = [
    ("Elemental HERO Neos", 3),
    ("Elemental HERO Neos Alius", 1),
    ("Neo-Spacian Air Hummingbird", 2),
    ("Neo-Spacian Aqua Dolphin", 2),
    ("Neo-Spacian Dark Panther", 2),
    ("Neo-Spacian Flare Scarab", 2),
    ("Neo-Spacian Glow Moss", 1),
    ("Neo-Spacian Grand Mole", 2),
    ("Elemental HERO Avian", 1),
    ("Elemental HERO Burstinatrix", 1),
    ("Elemental HERO Sparkman", 1),
    ("Elemental HERO Bubbleman", 1),
    ("Winged Kuriboh", 2),
    ("Winged Kuriboh LV10", 1),
    ("Wroughtweiler", 1),
    # Spells
    ("Polymerization", 2),
    ("Convert Contact", 2),
    ("Instant Contact", 1),
    ("Neo Space", 2),
    ("Neos Force", 1),
    ("Cocoon Party", 1),
    ("Skyscraper", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Hero Signal", 1),
    ("A Hero Emerges", 1),
    ("Mirror Gate", 1),
]
jaden_neos_extra = [
    ("Elemental HERO Air Neos", 1),
    ("Elemental HERO Aqua Neos", 1),
    ("Elemental HERO Dark Neos", 1),
    ("Elemental HERO Flare Neos", 1),
    ("Elemental HERO Glow Neos", 1),
    ("Elemental HERO Grand Neos", 1),
    ("Elemental HERO Storm Neos", 1),
    ("Elemental HERO Magma Neos", 1),
    ("Elemental HERO Chaos Neos", 1),
    ("Elemental HERO Divine Neos", 1),
    ("Elemental HERO Flame Wingman", 1),
    ("Elemental HERO Shining Flare Wingman", 1),
]

# 2. Dark Jaden / Evil HERO (GX season 3 villain Jaden)
jaden_evil_main = [
    ("Evil HERO Infernal Gainer", 2),
    ("Evil HERO Infernal Prodigy", 2),
    ("Evil HERO Adusted Gold", 1),
    ("Elemental HERO Avian", 1),
    ("Elemental HERO Burstinatrix", 1),
    ("Elemental HERO Sparkman", 1),
    ("Elemental HERO Clayman", 1),
    ("Elemental HERO Bubbleman", 1),
    ("Elemental HERO Wildheart", 1),
    ("Elemental HERO Necroshade", 1),
    ("Elemental HERO Neos", 1),
    ("Winged Kuriboh", 1),
    ("Winged Kuriboh LV10", 1),
    # Spells
    ("Dark Fusion", 3),
    ("Dark Calling", 2),
    ("Polymerization", 1),
    ("Fusion Recovery", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    ("Reinforcement of the Army", 1),
    ("E - Emergency Call", 2),
    # Traps
    ("Hero Signal", 1),
    ("Eternal Dread", 1),
    ("Mirror Gate", 1),
]
jaden_evil_extra = [
    ("Evil HERO Inferno Wing", 1),
    ("Evil HERO Lightning Golem", 1),
    ("Evil HERO Malicious Fiend", 1),
    ("Evil HERO Dark Gaia", 2),
    ("Evil HERO Malicious Bane", 1),
    ("Elemental HERO Flame Wingman", 1),
    ("Elemental HERO Thunder Giant", 1),
    ("Elemental HERO Shining Flare Wingman", 1),
]

# ============================================================
# YUSEI VARIANT - Quasar Ark Cradle
# ============================================================
yusei_quasar_main = [
    ("Junk Synchron", 3),
    ("Quickdraw Synchron", 2),
    ("Road Synchron", 2),
    ("Synchron Explorer", 2),
    ("Speed Warrior", 2),
    ("Sonic Chick", 2),
    ("Tuningware", 2),
    ("Quillbolt Hedgehog", 2),
    ("Effect Veiler", 1),
    ("Hyper Synchron", 1),
    ("Level Eater", 1),
    ("Tricular", 1),
    ("Bicular", 1),
    ("Unicycular", 1),
    ("Stardust Xiaolong", 1),
    ("Doppelwarrior", 1),
    ("Junk Servant", 1),
    # Spells
    ("Tuning", 3),
    ("One for One", 1),
    ("Pot of Avarice", 1),
    ("Foolish Burial", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    ("Synchro Boost", 1),
    # Traps
    ("Scrap-Iron Scarecrow", 2),
    ("Starlight Road", 1),
    ("Limit Reverse", 1),
    ("Call of the Haunted", 1),
]
yusei_quasar_extra = [
    ("Stardust Dragon", 1),
    ("Junk Warrior", 1),
    ("Junk Berserker", 1),
    ("Junk Destroyer", 1),
    ("Junk Archer", 1),
    ("Nitro Warrior", 1),
    ("Turbo Warrior", 1),
    ("Road Warrior", 1),
    ("Drill Warrior", 1),
    ("Formula Synchron", 2),
    ("T.G. Hyper Librarian", 1),
    ("Shooting Star Dragon", 1),
    ("Shooting Quasar Dragon", 1),
    ("Stardust Dragon/Assault Mode", 1),
]

# ============================================================
# YUMA - ZEXAL II
# ============================================================
yuma_zexal2_main = [
    ("Gagaga Magician", 3),
    ("Gagaga Girl", 1),
    ("Gagaga Caesar", 2),
    ("Gagaga Sister", 2),
    ("Gogogo Golem", 2),
    ("Gogogo Giant", 1),
    ("Zubaba Knight", 2),
    ("Achacha Archer", 1),
    ("Dododo Warrior", 1),
    ("Dododo Driver", 1),
    ("Kagetokage", 2),
    ("Photon Pirate", 1),
    ("Goblindbergh", 1),
    ("Tin Goldfish", 1),
    # Spells
    ("Onomatopickup", 2),
    ("Double or Nothing!", 2),
    ("Onomatopaira", 1),
    ("Rank-Up-Magic Astral Force", 1),
    ("Rank-Up-Magic Limited Barian's Force", 1),
    ("Rank-Up-Magic Numeron Force", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Half Unbreak", 1),
    ("Damage Diet", 1),
    ("Xyz Block", 1),
]
yuma_zexal2_extra = [
    ("Number 39: Utopia", 1),
    ("Number 39: Utopia Beyond", 1),
    ("Number S39: Utopia the Lightning", 1),
    ("Number C39: Utopia Ray", 1),
    ("Number C39: Utopia Ray V", 1),
    ("Number C39: Utopia Ray Victory", 1),
    ("Number 39: Utopia Roots", 1),
    ("Number 99: Utopic Dragon", 1),
    ("Number S0: Utopic ZEXAL", 1),
    ("Number F0: Utopic Future", 1),
    ("Number F0: Utopic Draco Future", 1),
    ("Number 99: Utopia Dragonar", 1),
]

# ============================================================
# YUYA VARIANTS
# ============================================================

# 1. Magicians / Synchro Dimension
yuya_magicians_main = [
    ("Performapal Skullcrobat Joker", 3),
    ("Performapal Pendulum Sorcerer", 2),
    ("Performapal Lizardraw", 2),
    ("Performapal Trump Witch", 1),
    ("Stargazer Magician", 1),
    ("Timegazer Magician", 1),
    ("Astrograph Sorcerer", 2),
    ("Chronograph Sorcerer", 2),
    ("Wisdom-Eye Magician", 2),
    ("Black Fang Magician", 1),
    ("White Wing Magician", 1),
    ("Xiangsheng Magician", 1),
    ("Xiangke Magician", 1),
    ("Harmonizing Magician", 1),
    ("Odd-Eyes Pendulum Dragon", 1),
    ("Odd-Eyes Persona Dragon", 1),
    # Spells
    ("Sky Iris", 1),
    ("Pendulum Storm", 1),
    ("Performapal Pinch Helper", 1),
    ("Smile World", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Performapal Revival", 1),
    ("Performapal Call", 1),
    ("Mirror Force", 1),
]
yuya_magicians_extra = [
    ("Odd-Eyes Rebellion Dragon", 1),
    ("Odd-Eyes Vortex Dragon", 1),
    ("Odd-Eyes Phantom Dragon", 1),
    ("Odd-Eyes Absolute Dragon", 1),
    ("Odd-Eyes Raging Dragon", 1),
    ("Dark Anthelion Dragon", 1),
    ("Beast-Eyes Pendulum Dragon", 1),
    ("Rune-Eyes Pendulum Dragon", 1),
    ("Performage Trapeze Magician", 1),
    ("Enlightenment Paladin", 1),
    ("Hi-Speedroid Chanbara", 1),
    ("Number 39: Utopia", 1),
]

# 2. Z-ARC / Supreme King
zarc_main = [
    ("Supreme King Dragon Darkwurm", 3),
    ("Supreme King Dragon Starving Venom", 1),
    ("Supreme King Dragon Clear Wing", 1),
    ("Supreme King Dragon Dark Rebellion", 1),
    ("Supreme King Dragon Odd-Eyes", 1),
    ("Performapal Skullcrobat Joker", 2),
    ("Performapal Pendulum Sorcerer", 2),
    ("Astrograph Sorcerer", 1),
    ("Wisdom-Eye Magician", 1),
    ("Stargazer Magician", 1),
    ("Timegazer Magician", 1),
    ("Performapal Lizardraw", 1),
    ("Odd-Eyes Pendulum Dragon", 1),
    ("Odd-Eyes Wing Dragon", 1),
    ("Odd-Eyes Saber Dragon", 1),
    # Spells
    ("Supreme King Gate Zero", 2),
    ("Supreme King Gate Infinity", 2),
    ("Sky Iris", 1),
    ("Pendulum Fusion", 1),
    ("Polymerization", 1),
    ("Pendulum Storm", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Mirror Force", 1),
]
zarc_extra = [
    ("Supreme King Z-ARC", 1),
    ("Odd-Eyes Rebellion Dragon", 1),
    ("Odd-Eyes Raging Dragon", 1),
    ("Dark Rebellion Xyz Dragon", 1),
    ("Clear Wing Synchro Dragon", 1),
    ("Starving Venom Fusion Dragon", 1),
    ("Beast-Eyes Pendulum Dragon", 1),
    ("Rune-Eyes Pendulum Dragon", 1),
    ("Dark Anthelion Dragon", 1),
    ("Crystal Wing Synchro Dragon", 1),
    ("Greedy Venom Fusion Dragon", 1),
    ("Odd-Eyes Vortex Dragon", 1),
    ("Odd-Eyes Absolute Dragon", 1),
]

# ============================================================
# YUSAKU - Code Talker (mid-late VRAINS)
# ============================================================
yusaku_codetalker_main = [
    ("Cyberse Wizard", 1),
    ("Cyberse Gadget", 3),
    ("Backup Secretary", 3),
    ("Linkslayer", 1),
    ("Stack Reviver", 2),
    ("Cyberse Synchron", 1),
    ("Bitron", 2),
    ("Draconnet", 2),
    ("RAM Clouder", 2),
    ("ROM Cloudia", 1),
    ("Dotscaper", 2),
    ("Cyberse White Hat", 1),
    ("Latency", 1),
    ("Lady Debug", 2),
    ("Micro Coder", 2),
    # Spells
    ("Cynet Mining", 3),
    ("Cynet Backdoor", 1),
    ("One for One", 1),
    ("Cynet Fusion", 1),
    ("Recoded Alive", 2),
    ("Monster Reborn", 1),
    # Traps
    ("Cynet Crosswipe", 2),
    ("Cynet Refresh", 1),
]
yusaku_codetalker_extra = [
    ("Decode Talker", 1),
    ("Decode Talker Extended", 1),
    ("Decode Talker Heatsoul", 1),
    ("Encode Talker", 1),
    ("Powercode Talker", 1),
    ("Transcode Talker", 1),
    ("Excode Talker", 1),
    ("Shootingcode Talker", 1),
    ("Tri-Gate Wizard", 1),
    ("Update Jammer", 1),
    ("Honeybot", 1),
    ("Linkuriboh", 1),
    ("Link Spider", 1),
    ("Cyberse Witch", 1),
    ("Firewall Dragon", 1),
]

# ============================================================
# RUSH DUEL — Sevens / Go Rush!! (rush=True)
# ============================================================

# Yuga Ohdo - Sevens Road / Magnum Overlord (Rush Duel)
yuga_main = [
    ("Sevens Road Magician", 3),
    ("Sevens Road Witch", 3),
    ("Sevens Road Mage", 3),
    ("Sevens Road Wiz", 2),
    ("Sevens Road Sorcerer", 2),
    ("Sevens Road Warlock", 2),
    ("Sevens Road Enchanter", 1),
    ("Sevens Road Charmy Witch", 1),
    ("Sevens Fear Magician", 1),
    ("Sevens Paladin", 2),
    ("Magician of Dark Sevens", 2),
    ("Strong Boy Sevens Road", 2),
    ("Master of the Sevens Road", 1),
    ("Sevens Road Ultima Witch", 1),
    ("Majesty of the Sevens Road", 1),
    ("Sevens Chariot the Magical Knight", 1),
    ("Sevens Knight the Multistrike Dragon Knight", 1),
    ("Sevensgias the Magical Dragon Knight", 1),
    # Spells
    ("Sevens Wonder Fusion", 2),
    ("Magical Sevens Fusion", 2),
    ("Magical Stone Excavation (Rush)", 2),
    # Traps
    ("Sevens Road Protection", 2),
    ("Road Arms - Sevens Lance", 2),
]
yuga_extra = []

# Yudias - Galactica (Go Rush!!)
yudias_main = [
    ("Galactica Oblivion", 3),
    ("Galactica Tabula Rasa", 3),
    ("Galactica Xiphos", 3),
    ("Galactica Dejavu", 3),
    ("Galactica Adargatling", 3),
    ("Recombination Galactica", 2),
    ("Galactica Lost Oblivion", 1),
    ("Darkness Galactica Oblivion", 1),
    ("Galactica Chaos Oblivion", 1),
    ("Galactica God Oblivion", 1),
    ("Eternal Galactica Oblivion", 1),
    ("Galactica Oblivion Ark", 1),
    # Spells
    ("Galactica Force", 2),
    ("Galactica Lattice", 2),
    ("Galactica Repulsion", 1),
    ("Galactica Reminiscence", 1),
    # Traps
    ("Galactica Amnesia", 2),
    ("Galactica Jamaisvu", 1),
    # Maximum (Yudias has Super Galaxy King)
    ("Super Galaxy King Lord of Galactica [L]", 1),
    ("Super Galaxy King Lord of Galactica", 1),
    ("Super Galaxy King Lord of Galactica [R]", 1),
]
yudias_extra = []

# Yuhi Ohdo - Voidvelg (Go Rush!!)
yuhi_main = [
    ("Voidvelg Requiem", 3),
    ("Voidvelg Tyrfing", 3),
    ("Voidvelg Cataphract", 3),
    ("Voidvelg Black Dwarf", 2),
    ("Voidvelg Protostar", 2),
    ("Voidvelg Phalanx", 2),
    ("Voidvelg Kyrie", 2),
    ("Voidvelg Logisticos", 2),
    ("Voidvelg Chrysaor", 1),
    ("Voidvelg Theogonia", 1),
    ("Voidvelg Gigantomachia", 1),
    ("Voidvelg Hetairoi", 1),
    ("Voidvelg Universtella", 1),
    ("Voidvelg Stork", 1),
    ("Voidvelg Beyond Probe", 1),
    ("Eternum Voidvelg Requiem", 1),
    ("Voidvelg Forbidden Requiem", 1),
    ("Voidvelg God Requiem", 1),
    ("Voidvelg Apocalypse", 1),
    ("Voidvelg Chaosmachia", 1),
]
yuhi_extra = []

# ============================================================
# Run them all
# ============================================================
master_decks = [
    # Yugi/Atem
    ("Yugi - Duelist Kingdom.ydk", "Yugi - Duelist Kingdom era", yugi_dk_main, yugi_dk_extra, False),
    ("Yugi - Doma Arc.ydk", "Yugi - Waking the Dragons", yugi_doma_main, yugi_doma_extra, False),
    ("Atem - Memory World.ydk", "Atem - Memory World/Pharaoh", atem_memory_main, atem_memory_extra, False),
    ("Yugi - Final Duel (vs Atem).ydk", "Yugi's Final Deck - Silent Magician/Swordsman", yugi_final_main, yugi_final_extra, False),
    ("Yugi - Manga Final.ydk", "Yugi - Dawn of the Duel manga", yugi_manga_main, yugi_manga_extra, False),
    # Kaiba
    ("Kaiba - Duelist Kingdom.ydk", "Kaiba - Duelist Kingdom era", kaiba_dk_main, kaiba_dk_extra, False),
    ("Kaiba - Doma Arc.ydk", "Kaiba - Waking the Dragons", kaiba_doma_main, kaiba_doma_extra, False),
    ("Kaiba - DSOD Modern.ydk", "Kaiba DSOD - Blue-Eyes Alternative", kaiba_dsod_main, kaiba_dsod_extra, False),
    # Joey
    ("Joey - Duelist Kingdom.ydk", "Joey - Duelist Kingdom era", joey_dk_main, joey_dk_extra, False),
    ("Joey - Doma (Hermos).ydk", "Joey - Waking the Dragons", joey_doma_main, joey_doma_extra, False),
    # Jaden
    ("Jaden - Neos era.ydk", "Jaden - Neos & Neo-Spacians", jaden_neos_main, jaden_neos_extra, False),
    ("Jaden - Dark Evil HERO.ydk", "Dark Jaden - Evil HERO", jaden_evil_main, jaden_evil_extra, False),
    # Yusei
    ("Yusei - Quasar (Ark Cradle).ydk", "Yusei - Shooting Quasar Dragon", yusei_quasar_main, yusei_quasar_extra, False),
    # Yuma
    ("Yuma - ZEXAL II.ydk", "Yuma - ZEXAL II Hope/Chaos Numbers", yuma_zexal2_main, yuma_zexal2_extra, False),
    # Yuya
    ("Yuya - Magicians (Synchro Dim).ydk", "Yuya - Magicians/Synchro Dimension", yuya_magicians_main, yuya_magicians_extra, False),
    ("Yuya - Z-ARC Supreme King.ydk", "Z-ARC - Supreme King", zarc_main, zarc_extra, False),
    # Yusaku
    ("Yusaku - Code Talker.ydk", "Yusaku - Code Talker (S2)", yusaku_codetalker_main, yusaku_codetalker_extra, False),
    # Rush Duel - Sevens / Go Rush
    ("[Rush] Yuga - Sevens Road.ydk", "Yuga Ohdo - Sevens Road (Rush Duel)", yuga_main, yuga_extra, True),
    ("[Rush] Yudias - Galactica.ydk", "Yudias - Galactica (Rush Duel)", yudias_main, yudias_extra, True),
    ("[Rush] Yuhi - Voidvelg.ydk", "Yuhi Ohdo - Voidvelg (Rush Duel)", yuhi_main, yuhi_extra, True),
]

all_missing = {}
for f, a, m, x, rush in master_decks:
    miss = write_ydk(f, a, m, x, rush=rush)
    if miss: all_missing[f] = miss

print("=== SUMMARY ===")
if all_missing:
    for f, miss in all_missing.items():
        print(f"  {f}: {miss}")
else:
    print("All cards resolved cleanly.")
