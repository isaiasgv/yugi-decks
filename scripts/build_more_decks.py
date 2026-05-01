"""
Round 2: more canon decks. Reuses lookup/write_ydk from build_decks.py.
"""
import os, sqlite3

CDB_PATH = "/tmp/BabelCDB/cards.cdb"
OUT_DIR = "/sessions/gallant-optimistic-sagan/mnt/outputs/decks"
con = sqlite3.connect(CDB_PATH)
cur = con.cursor()

def lookup(name):
    cur.execute("SELECT t.id FROM texts t JOIN datas d ON d.id=t.id WHERE LOWER(t.name)=LOWER(?) AND d.alias=0", (name,))
    r = cur.fetchone()
    if r: return r[0]
    cur.execute("SELECT id FROM texts WHERE LOWER(name)=LOWER(?)", (name,))
    r = cur.fetchone()
    return r[0] if r else None

def write_ydk(filename, author, main, extra, side=None):
    side = side or []
    missing = []
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)
    def resolve(cards):
        ids = []
        for e in cards:
            n, c = (e if isinstance(e, tuple) else (e, 1))
            cid = lookup(n)
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
# DM-era extras
# ============================================================

# Atem - DSOD movie deck (modern Dark Magician)
atem_dsod_main = [
    ("Dark Magician", 3),
    ("Dark Magician Girl", 1),
    ("Magician of Dark Illusion", 2),
    ("Magician's Rod", 3),
    ("Magicians' Souls", 3),
    ("Magician of Chaos", 1),
    ("Apprentice Illusion Magician", 2),
    ("Dark Magical Circle", 3),
    ("The Eye of Timaeus", 2),
    ("Soul Servant", 2),
    ("Magicians' Combination", 1),
    ("Illusion Magic", 1),
    ("Bond Between Teacher and Student", 1),
    ("Dark Magic Inheritance", 1),
    ("Dark Magic Attack", 1),
    ("Dark Magic Veil", 1),
    ("Thousand Knives", 1),
    ("Eternal Soul", 2),
    ("Magician Navigation", 2),
    ("Magic Cylinder", 1),
    ("Mirror Force", 1),
]
atem_dsod_extra = [
    ("Dark Cavalry", 1),
    ("The Dark Magicians", 1),
    ("Dark Paladin", 1),
    ("Quintet Magician", 1),
    ("Amulet Dragon", 1),
    ("Ebon Illusion Magician", 1),
    ("Ebon High Magician", 1),
]

# Pegasus - Toons
pegasus_main = [
    ("Toon Mermaid", 2),
    ("Manga Ryu-Ran", 1),
    ("Toon Summoned Skull", 2),
    ("Toon Gemini Elf", 1),
    ("Toon Goblin Attack Force", 1),
    ("Toon Cannon Soldier", 1),
    ("Toon Masked Sorcerer", 1),
    ("Toon Dark Magician Girl", 1),
    ("Toon Dark Magician", 1),
    ("Blue-Eyes Toon Dragon", 1),
    ("Red-Eyes Toon Dragon", 1),
    ("Toon Buster Blader", 1),
    ("Toon Cyber Dragon", 1),
    ("Toon Briefcase", 1),
    ("Toon Alligator", 1),
    ("Toon Mermaid", 1),
    ("Relinquished", 1),
    ("Thousand-Eyes Idol", 1),
    ("Parrot Dragon", 1),
    # Spells
    ("Toon World", 3),
    ("Toon Kingdom", 2),
    ("Toon Table of Contents", 3),
    ("Toon Page-Flip", 1),
    ("Comic Hand", 2),
    ("Mimicat", 1),
    ("Shine Palace", 1),
    ("Pot of Greed", 1),
    ("Mystical Space Typhoon", 1),
    ("Polymerization", 1),
    # Traps
    ("Toon Defense", 1),
    ("Toon Mask", 1),
    ("Toon Rollback", 1),
]
pegasus_extra = [
    ("Toon Black Luster Soldier", 1),
    ("Toon Ancient Gear Golem", 1),
    ("Thousand-Eyes Restrict", 1),
]

# Bakura - Occult / Dark Necrofear
bakura_main = [
    ("Dark Necrofear", 1),
    ("Earthbound Spirit", 2),
    ("Headless Knight", 2),
    ("The Earl of Demise", 2),
    ("Souls of the Forgotten", 2),
    ("Diabound Kernel", 1),
    ("Jowls of Dark Demise", 2),
    ("Puppet Master", 1),
    ("Ghost of a Grudge", 1),
    ("The Portrait's Secret", 1),
    ("Dark Spirit of the Silent", 1),
    ("Sangan", 1),
    ("Witch of the Black Forest", 1),
    ("Man-Eater Bug", 1),
    ("Doomcaliber Knight", 1),
    ("Dark Ruler Ha Des", 1),
    # Spells
    ("Dark Sanctuary", 2),
    ("The Dark Door", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    ("Multiplication of Ants", 1),
    ("Card Destruction", 1),
    # Traps
    ("Destiny Board", 1),
    ("Spirit Message \"I\"", 1),
    ("Spirit Message \"N\"", 1),
    ("Spirit Message \"A\"", 1),
    ("Spirit Message \"L\"", 1),
    ("Call of the Haunted", 1),
    ("Dark Spirit's Mastery", 1),
]
bakura_extra = []

# Mai Valentine - Harpies
mai_main = [
    ("Harpie Lady 1", 3),
    ("Harpie Lady 2", 1),
    ("Harpie Lady 3", 1),
    ("Harpie Queen", 3),
    ("Harpie Channeler", 3),
    ("Harpie Harpist", 2),
    ("Harpie Perfumer", 2),
    ("Harpie Oracle", 1),
    ("Harpie Dancer", 2),
    ("Cyber Harpie Lady", 1),
    ("Harpie's Pet Dragon", 1),
    ("Harpie's Pet Baby Dragon", 1),
    # Spells
    ("Elegant Egotist", 2),
    ("Hysteric Sign", 2),
    ("Hysteric Party", 2),
    ("Harpies' Hunting Ground", 3),
    ("Triangle Ecstasy Spark", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    ("Pot of Greed", 1),
    ("Cyber Shield", 1),
    # Traps
    ("Harpie's Feather Storm", 1),
    ("Icarus Attack", 1),
    ("Mirror Force", 1),
]
mai_extra = [
    ("Harpie Conductor", 1),
]

# Ishizu Ishtar - Fairy/Spirit (Agido/Keldo/Exchange of the Spirit)
ishizu_main = [
    ("Agido the Ancient Sentinel", 3),
    ("Keldo the Sacred Protector", 3),
    ("Mudora the Sword Oracle", 3),
    ("Kelbek the Ancient Vanguard", 3),
    ("Zolga the Prophet", 3),
    ("Dimension Shifter", 2),
    ("Effect Veiler", 2),
    ("Maxx \"C\"", 3),
    ("Pot of Prosperity", 3),
    ("Pot of Extravagance", 2),
    ("Foolish Burial", 1),
    ("Foolish Burial Goods", 1),
    ("Monster Reborn", 1),
    ("Forbidden Droplet", 2),
    ("Triple Tactics Talent", 1),
    # Traps
    ("Exchange of the Spirit", 1),
    ("Solemn Judgment", 1),
    ("Solemn Strike", 2),
    ("Infinite Impermanence", 3),
]
ishizu_extra = [
    ("Knightmare Phoenix", 1),
    ("S:P Little Knight", 1),
    ("I:P Masquerena", 1),
    ("Apollousa, Bow of the Goddess", 1),
]

# ============================================================
# GX-era extras
# ============================================================

# Aster Phoenix - Destiny HERO
aster_main = [
    ("Destiny HERO - Diamond Dude", 2),
    ("Destiny HERO - Doom Lord", 2),
    ("Destiny HERO - Dasher", 2),
    ("Destiny HERO - Dreadmaster", 1),
    ("Destiny HERO - Disk Commander", 1),
    ("Destiny HERO - Captain Tenacious", 2),
    ("Destiny HERO - Dogma", 2),
    ("Destiny HERO - Plasma", 1),
    ("Destiny HERO - Defender", 1),
    ("Destiny HERO - Decider", 1),
    ("Destiny HERO - Dystopia", 1),
    ("Destiny HERO - Drilldark", 2),
    ("Destiny HERO - Malicious", 3),
    ("Destiny HERO - Departed", 1),
    ("Destiny HERO - Dasher", 1),
    # Spells
    ("Destiny Draw", 3),
    ("D - Spirit", 1),
    ("D - Formation", 1),
    ("D - Time", 1),
    ("Misfortune", 2),
    ("Polymerization", 2),
    ("Reinforcement of the Army", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    # Traps
    ("D - Counter", 1),
    ("D - Chain", 1),
    ("Destiny Signal", 1),
    ("Mirror Force", 1),
]
aster_extra = [
    ("Destiny End Dragoon", 1),
    ("Destiny HERO - Dystopia", 1),
    ("Destiny HERO - Dangerous", 1),
    ("Destiny HERO - Dominance", 1),
    ("Destiny HERO - Dynatag", 1),
    ("Elemental HERO Shadow Mist", 0),
]

# Bastion Misawa - Element/Hydro
bastion_main = [
    ("Hydrogeddon", 3),
    ("Oxygeddon", 3),
    ("Carboneddon", 2),
    ("Water Dragon", 1),
    ("Aqua Spirit", 2),
    ("Element Saurus", 2),
    ("Helios - The Primordial Sun", 1),
    ("Helios Duo Megistus", 1),
    ("Helios Trice Megistus", 1),
    ("Volcanic Doomfire", 1),
    # Spells
    ("Bonding - H2O", 3),
    ("Bonding - DHO", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    ("Polymerization", 1),
    ("Mystical Space Typhoon", 1),
    # Traps
    ("Tornado Wall", 2),
    ("Umi", 1),
    ("Mirror Force", 1),
]
bastion_extra = []

# Atticus / Nightshroud - Red-Eyes Darkness
atticus_main = [
    ("Red-Eyes Black Dragon", 1),
    ("Red-Eyes Darkness Dragon", 1),
    ("Black Dragon's Chick", 2),
    ("Red-Eyes Wyvern", 2),
    ("Red-Eyes Retro Dragon", 2),
    ("Black Dragon's Chick", 2),
    ("Mavelus", 1),
    ("Spear Dragon", 2),
    ("Nightmare Penguin", 1),
    ("Skull Servant", 2),
    ("Wandering Mummy", 1),
    ("Mystic Tomato", 2),
    # Spells
    ("Inferno Fire Blast", 2),
    ("Red-Eyes Insight", 2),
    ("Red-Eyes Fusion", 2),
    ("Polymerization", 1),
    ("Pot of Greed", 1),
    ("Monster Reborn", 1),
    ("Cards of Consonance", 2),
    # Traps
    ("Mirror Force", 1),
    ("Call of the Haunted", 1),
    ("Red-Eyes Spirit", 2),
]
atticus_extra = [
    ("Red-Eyes Darkness Metal Dragon", 1),
    ("Red-Eyes Slash Dragon", 1),
    ("Archfiend Black Skull Dragon", 1),
    ("Red-Eyes Flare Metal Dragon", 1),
]

# Yubel
yubel_main = [
    ("Yubel", 1),
    ("Yubel - Terror Incarnate", 1),
    ("Yubel - The Ultimate Nightmare", 1),
    ("Spirit of Yubel", 3),
    ("Phantom of Yubel", 3),
    ("Eternal Favorite", 2),
    ("Sangan", 1),
    ("Mystic Tomato", 3),
    ("Samsara, Dragon of Rebirth", 1),
    ("Battle Fader", 1),
    ("Caius the Shadow Monarch", 1),
    ("Doomking Balerdroch", 1),
    # Spells
    ("Nightmare Pain", 3),
    ("Mature Chronicle", 2),
    ("Pot of Desires", 1),
    ("Fires of Doomsday", 2),
    ("Foolish Burial", 1),
    # Traps
    ("Limit Reverse", 1),
    ("Call of the Haunted", 1),
]
yubel_extra = [
    ("Knightmare Phoenix", 1),
    ("Knightmare Unicorn", 1),
    ("I:P Masquerena", 1),
    ("S:P Little Knight", 1),
]

# ============================================================
# 5D's-era extras
# ============================================================

# Akiza Izinski - Black Rose
akiza_main = [
    ("Twilight Rose Knight", 1),
    ("Witch of the Black Rose", 2),
    ("Phoenixian Cluster Amaryllis", 2),
    ("Phoenixian Seed", 1),
    ("Rose Tentacles", 1),
    ("Fragrance Storm", 1),
    ("Blue Rose Dragon", 1),
    ("Rose, Warrior of Revenge", 1),
    ("Lord Poison", 1),
    ("Wall of Ivy", 1),
    ("Copy Plant", 1),
    ("Lonefire Blossom", 2),
    ("Dark Verger", 2),
    ("Hedge Guard", 1),
    ("Tytannial, Princess of Camellias", 1),
    ("Spore", 1),
    ("Glow-Up Bulb", 1),
    # Spells
    ("Black Garden", 3),
    ("Mark of the Rose", 1),
    ("Pot of Avarice", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    ("Foolish Burial", 1),
    # Traps
    ("Wall of Thorns", 1),
    ("Mirror Force", 1),
]
akiza_extra = [
    ("Black Rose Dragon", 1),
    ("Black Rose Moonlight Dragon", 1),
    ("Splendid Rose", 1),
    ("Queen of Thorns", 1),
    ("Queen Angel of Roses", 1),
]

# Luna - Ancient Fairy
luna_main = [
    ("Sunlight Unicorn", 2),
    ("Kuribon", 2),
    ("Fairy Archer", 2),
    ("Spore", 1),
    ("Lonefire Blossom", 1),
    ("Glow-Up Bulb", 1),
    ("Copy Plant", 1),
    ("Regulus", 1),
    ("Goyo Predator", 1),
    ("Key Mace", 2),
    ("Key Mace #2", 1),
    ("Watthopper", 2),
    ("Dewloren, Tiger King of the Ice Barrier", 1),
    ("Beast of the Pharaoh", 1),
    # Spells
    ("Closed Forest", 1),
    ("Pot of Avarice", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    ("Polymerization", 1),
    ("Forest", 1),
    # Traps
    ("Mirror Force", 1),
    ("Call of the Haunted", 1),
]
luna_extra = [
    ("Ancient Fairy Dragon", 1),
    ("Regulus", 0),
    ("Power Tool Dragon", 0),
]

# Leo - Morphtronic
leo_main = [
    ("Morphtronic Celfon", 3),
    ("Morphtronic Magnen", 2),
    ("Morphtronic Magnen Bar", 1),
    ("Morphtronic Boomboxen", 2),
    ("Morphtronic Datatron", 2),
    ("Morphtronic Radion", 2),
    ("Morphtronic Cameran", 2),
    ("Morphtronic Remoten", 2),
    ("Morphtronic Smartfon", 1),
    ("Morphtronic Vacuumen", 1),
    ("Morphtronic Scopen", 1),
    ("Morphtronic Clocken", 1),
    # Spells
    ("Morphtronic Accelerator", 2),
    ("Morphtronic Forcefield", 1),
    ("Pot of Avarice", 1),
    ("Monster Reborn", 1),
    ("Mystical Space Typhoon", 1),
    # Traps
    ("Morphtronic Bind", 1),
    ("Morphtransition", 2),
    ("Mirror Force", 1),
    ("Call of the Haunted", 1),
]
leo_extra = [
    ("Power Tool Dragon", 1),
    ("Power Tool Mecha Dragon", 1),
    ("Life Stream Dragon", 1),
    ("Morphtronic Map", 0),
]

# Aporia - Meklord
aporia_main = [
    ("Meklord Emperor Wisel", 1),
    ("Meklord Emperor Granel", 1),
    ("Meklord Emperor Skiel", 1),
    ("Meklord Astro Mekanikle", 1),
    ("Meklord Army of Wisel", 3),
    ("Meklord Army of Granel", 3),
    ("Meklord Army of Skiel", 3),
    ("Meklord Emperor Wisel - Synchro Absorption", 1),
    # Spells
    ("Meklord Astro the Eradicator", 1),
    ("Meklord Fortress", 1),
    ("Meklord Factory", 1),
    ("Pot of Avarice", 1),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Boon of the Meklord Emperor", 1),
    ("Mirror Force", 1),
    ("Limit Reverse", 1),
]
aporia_extra = []

# ============================================================
# Zexal/ArcV/VRAINS extras
# ============================================================

# Kaito Tenjo - Galaxy-Eyes Photon
kaito_main = [
    ("Photon Thrasher", 3),
    ("Galaxy Knight", 2),
    ("Galaxy Wizard", 2),
    ("Photon Crusher", 2),
    ("Photon Sabre Tiger", 1),
    ("Galaxy-Eyes Photon Dragon", 3),
    ("Photon Lizard", 1),
    ("Daybreaker", 1),
    ("Cipher Wing", 2),
    ("Cipher Twin Raptor", 2),
    ("Cipher Etranger", 1),
    ("Galaxy-Eyes Cipher Dragon", 1),
    ("Galaxy Brave", 1),
    ("Galaxy Soldier", 3),
    ("Galaxy Worm", 2),
    # Spells
    ("Galaxy Expedition", 2),
    ("Galaxy Zero", 1),
    ("Galaxy Tyranno", 1),
    ("Trade-In", 2),
    ("Cipher Interference", 1),
    ("Photon Booster", 1),
    ("Polymerization", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Photon Sanctuary", 1),
    ("Mirror Force", 1),
]
kaito_extra = [
    ("Number 62: Galaxy-Eyes Prime Photon Dragon", 1),
    ("Number 95: Galaxy-Eyes Dark Matter Dragon", 1),
    ("Number 107: Galaxy-Eyes Tachyon Dragon", 1),
    ("Galaxy-Eyes Full Armor Photon Dragon", 1),
    ("Galaxy-Eyes Cipher Blade Dragon", 1),
    ("Galaxy-Eyes Cipher X Dragon", 1),
    ("Neo Galaxy-Eyes Cipher Dragon", 1),
    ("Neo Galaxy-Eyes Photon Dragon", 1),
    ("Number S0: Utopic ZEXAL", 1),
    ("Number S39: Utopia the Lightning", 1),
]

# Yuto - Phantom Knights
yuto_main = [
    ("The Phantom Knights of Ancient Cloak", 3),
    ("The Phantom Knights of Silent Boots", 3),
    ("The Phantom Knights of Ragged Gloves", 3),
    ("The Phantom Knights of Cloven Helm", 1),
    ("The Phantom Knights of Tomb Shield", 2),
    ("The Phantom Knights of Stained Greaves", 1),
    ("The Phantom Knights of Mist Claws", 1),
    ("The Phantom Knights of Torn Scales", 1),
    ("The Phantom Knights of Dark Gauntlets", 1),
    ("The Phantom Knights of Fragile Armor", 1),
    # Spells
    ("The Phantom Knights' Rank-Up-Magic Launch", 2),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Phantom Knights' Sword", 2),
    ("Phantom Knights' Spear", 1),
    ("Phantom Knights' Wing", 2),
    ("Phantom Knights' Fog Blade", 3),
    ("Phantom Knights' Rank-Up-Magic Force", 1),
]
yuto_extra = [
    ("Dark Rebellion Xyz Dragon", 1),
    ("Dark Anthelion Dragon", 1),
    ("Dark Requiem Xyz Dragon", 1),
    ("The Phantom Knights of Break Sword", 2),
    ("Number 39: Utopia", 1),
    ("The Phantom Knights of Cursed Javelin", 1),
    ("Number C39: Utopia Ray", 1),
]

# Yugo - Speedroid
yugo_main = [
    ("Speedroid Terrortop", 3),
    ("Speedroid Taketomborg", 3),
    ("Speedroid Red-Eyed Dice", 2),
    ("Speedroid Den-Den Daiko Duke", 2),
    ("Speedroid Tri-Eyed Dice", 1),
    ("Speedroid Double Yoyo", 2),
    ("Speedroid Skull Marbles", 1),
    ("Speedroid Marble Machine", 1),
    ("Speedroid Razorang", 2),
    ("Speedroid Ohajikid", 2),
    ("Speedroid Pachingo-Kart", 1),
    ("Speedroid Block-n-Roll", 1),
    ("Speedroid Wheel", 1),
    ("Speedroid Menko", 1),
    # Spells
    ("Cyclone Boomerang", 1),
    ("Pot of Desires", 2),
    ("Mystical Space Typhoon", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Mirror Force", 1),
]
yugo_extra = [
    ("Clear Wing Synchro Dragon", 1),
    ("Clear Wing Fast Dragon", 1),
    ("Crystal Wing Synchro Dragon", 1),
    ("Hi-Speedroid Clear Wing Rider", 1),
    ("Hi-Speedroid Chanbara", 2),
    ("Hi-Speedroid Kendama", 1),
    ("Hi-Speedroid Puzzle", 1),
    ("Formula Synchron", 1),
    ("Stardust Charge Warrior", 1),
    ("Hi-Speedroid Cork Shooter", 1),
    ("Hi-Speedroid Rubber Band Shooter", 1),
]

# Yuri - Predaplant
yuri_main = [
    ("Predaplant Ophrys Scorpio", 3),
    ("Predaplant Darlingtonia Cobra", 2),
    ("Predaplant Drosophyllum Hydra", 2),
    ("Predaplant Spinodionaea", 2),
    ("Predaplant Moray Nepenthes", 1),
    ("Predaplant Squid Drosera", 1),
    ("Predaplant Flytrap", 1),
    ("Predaplant Sarraceniant", 2),
    ("Predaplant Bufolicula", 1),
    ("Predaplant Heliamphorhynchus", 1),
    ("Predaplant Triantis", 1),
    ("Predaplant Pterapenthes", 1),
    # Spells
    ("Predapractice", 2),
    ("Predaplanet", 1),
    ("Predapruning", 1),
    ("Polymerization", 2),
    ("Predaponics", 1),
    ("Pot of Desires", 1),
    ("Foolish Burial", 1),
    ("Monster Reborn", 1),
    # Traps
    ("Predaprime Fusion", 1),
]
yuri_extra = [
    ("Starving Venom Fusion Dragon", 1),
    ("Starving Venom Predapower Fusion Dragon", 1),
    ("Greedy Venom Fusion Dragon", 1),
    ("Predaplant Dragostapelia", 2),
    ("Predaplant Chimerafflesia", 1),
    ("Predaplant Triphyoverutum", 1),
    ("Predaplant Verte Anaconda", 1),
]

# Revolver - Rokket / Borrel
revolver_main = [
    ("Rokket Tracer", 3),
    ("Autorokket Dragon", 2),
    ("Anesthrokket Dragon", 2),
    ("Magnarokket Dragon", 2),
    ("Silverrokket Dragon", 2),
    ("Metalrokket Dragon", 2),
    ("Shelrokket Dragon", 1),
    ("Rokket Synchron", 1),
    ("Rokket Recharger", 1),
    ("Rokket Caliber", 1),
    ("Striker Dragon", 1),
    ("Absorouter Dragon", 1),
    ("Exploderokket Dragon", 1),
    # Spells
    ("Quick Launch", 3),
    ("Boot Sector Launch", 2),
    ("Squib Draw", 2),
    ("Pot of Desires", 1),
    ("Monster Reborn", 1),
    ("Foolish Burial", 1),
    # Traps
    ("Red Reboot", 1),
    ("Mirror Force", 1),
]
revolver_extra = [
    ("Borreload Dragon", 1),
    ("Borreload Savage Dragon", 1),
    ("Borreload Furious Dragon", 1),
    ("Borreload Riot Dragon", 1),
    ("Borrelsword Dragon", 1),
    ("Borrelend Dragon", 1),
    ("Topologic Bomber Dragon", 1),
    ("Topologic Trisbaena", 1),
    ("Topologic Gumblar Dragon", 1),
    ("Topologic Zeroboros", 1),
    ("Striker Dragon", 1),
    ("Hieratic Seal of the Heavenly Spheres", 1),
    ("Knightmare Phoenix", 1),
    ("Knightmare Unicorn", 1),
    ("Crystron Halqifibrax", 0),
]

# Aoi Zaizen / Blue Angel - Trickstar
aoi_main = [
    ("Trickstar Lycoris", 3),
    ("Trickstar Lilybell", 3),
    ("Trickstar Candina", 3),
    ("Trickstar Mandrake", 2),
    ("Trickstar Narkissus", 1),
    ("Trickstar Corobane", 1),
    ("Trickstar Nightshade", 1),
    ("Trickstar Bouquet", 1),
    ("Trickstar Bloom", 1),
    ("Effect Veiler", 2),
    ("Maxx \"C\"", 3),
    ("Ash Blossom & Joyous Spring", 3),
    # Spells
    ("Trickstar Light Stage", 3),
    ("Trickstar Festival", 1),
    ("Trickstar Live Stage", 1),
    ("Pot of Desires", 1),
    ("Mystical Space Typhoon", 1),
    # Traps
    ("Trickstar Reincarnation", 2),
    ("Solemn Strike", 2),
    ("Infinite Impermanence", 3),
]
aoi_extra = [
    ("Trickstar Holly Angel", 1),
    ("Trickstar Crimson Heart", 1),
    ("Trickstar Foxglove Witch", 1),
    ("Trickstar Black Catbat", 1),
    ("Trickstar Bella Madonna", 1),
    ("Trickstar Delfiendium", 1),
    ("Knightmare Phoenix", 1),
    ("Knightmare Unicorn", 1),
    ("I:P Masquerena", 1),
    ("S:P Little Knight", 1),
    ("Apollousa, Bow of the Goddess", 1),
    ("Accesscode Talker", 1),
]

decks = [
    ("Atem - DSOD.ydk", "Atem - DSOD Dark Magician", atem_dsod_main, atem_dsod_extra),
    ("Pegasus - Toons.ydk", "Maximillion Pegasus", pegasus_main, pegasus_extra),
    ("Bakura - Occult.ydk", "Yami Bakura - Dark Necrofear", bakura_main, bakura_extra),
    ("Mai - Harpies.ydk", "Mai Valentine - Harpies", mai_main, mai_extra),
    ("Ishizu - Spirits.ydk", "Ishizu Ishtar - Fairy/Spirits", ishizu_main, ishizu_extra),
    ("Aster - Destiny HEROes.ydk", "Aster Phoenix", aster_main, aster_extra),
    ("Bastion - Element.ydk", "Bastion Misawa", bastion_main, bastion_extra),
    ("Atticus - Red-Eyes Darkness.ydk", "Atticus Rhodes / Nightshroud", atticus_main, atticus_extra),
    ("Yubel - GX.ydk", "Yubel", yubel_main, yubel_extra),
    ("Akiza - Black Rose.ydk", "Akiza Izinski", akiza_main, akiza_extra),
    ("Luna - Ancient Fairy.ydk", "Luna - 5Ds", luna_main, luna_extra),
    ("Leo - Morphtronic.ydk", "Leo - 5Ds", leo_main, leo_extra),
    ("Aporia - Meklord.ydk", "Aporia - 5Ds", aporia_main, aporia_extra),
    ("Kaito - Galaxy-Eyes.ydk", "Kaito Tenjo", kaito_main, kaito_extra),
    ("Yuto - Phantom Knights.ydk", "Yuto - Arc-V", yuto_main, yuto_extra),
    ("Yugo - Speedroid.ydk", "Yugo - Arc-V", yugo_main, yugo_extra),
    ("Yuri - Predaplant.ydk", "Yuri - Arc-V", yuri_main, yuri_extra),
    ("Revolver - Rokket Borrel.ydk", "Revolver - VRAINS", revolver_main, revolver_extra),
    ("Aoi - Trickstar.ydk", "Blue Angel - VRAINS", aoi_main, aoi_extra),
]

all_missing = {}
for f, a, m, x in decks:
    miss = write_ydk(f, a, m, x)
    if miss: all_missing[f] = miss

print("\n=== SUMMARY ===")
if all_missing:
    for f, miss in all_missing.items():
        print(f"  {f}: {miss}")
else:
    print("All cards resolved cleanly.")
