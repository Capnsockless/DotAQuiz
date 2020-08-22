import random
import discord
import asyncio
import json
import ast
import time
import os
from discord.ext import commands

os.chdir(r"D:\Discordbot\DotaQuizbot")

#The dictionary of questions: the keys are the questions and the values are answers, if the question has one answer the value is a string or a tuple if the same answer can be answered in multiple ways
#the answer is a list if the question has multiple right answers. Image questions are presented as tuples where the first item is the question and the second is the image location
#When the user has the wrong answer the correct answer is presented as 1)if string it is the string; 2)if it's a tuple the first answer gets displayed; 3)if it's a list a randomly selected answer that begins with a capital letter is displayed
questdict = {"What is Dark Seer's ultimate ability?":("Wall of Replica", "vacuum"), "What is Arteezy's real name?":("Artour Babaev", "Artour"), "What year was the 7.00 update released?":"2016",
"Who is Mogul Khan?":"Axe", "Which debuff can Orchid Malevolence cause to its target?":"Silence", "Except pudge, which other hero was needed to perform a fountain hook in DotA 2?":"Chen",
"Which team won TI4?":"Newbee", "Which hero has the lowest base movement speed?":("Broodmother", "brood"), "According to the lore, which hero took part in destroying Anti-mage's home village?":("Undying", "dirge"),
"Which hero can spawn treants?":("Nature's Prophet", "furion", "np"), "How much gold does an Aghanim's scepter cost?":("4200", "4.2k"), "Which item can be upgraded 4 times?":"Dagon",
"Name a hero that wears goggles.":["Sniper", "Tinker", "Snapfire", "gyro", "Gyrocopter", "Batrider"], "Which item burns mana on each hit?":("Diffusal Blade", "diffusal"),
'Which hero has the ability "Diabolic Edict"?':"leshrac", "Which hero has the highest base damage?":("Treant Protector", "treant"), "Which hero has the highest intelligence gain?":"Pugna",
"What's invokers name?":"Carl", "What does Dragon knight call his sword?":"Wyrmblade", "Which spell replaced Tusk's Frozen Sigil?":"Tag Team", "Which hero resembles a watermelon?":("Tidehunter", "watermelon", 'tide'),
"What's the name of the Goddess of the Moon?":"Selemene", "༼ つ ◕_◕ ༽つ GIVE":"DIRETIDE", "Which patch introduced neutral items?":"7.23", "What is Warlocks third ability called?":"Upheaval",
"Name a hero that has more than two eyes on one head.":["Broodmother", "Brood", "Sand King", "Venomancer", "veno", "banana"], "How many intelligence heroes are melee?":("3", "three"),
"Name a hero that rides a horse.":["Chaos Knight", "ck", "kotl", "Keeper of the Light", "Abaddon"], "How much gold does a Reaver cost?":("3000", "3k"), 'Which hero has an ability named "Essense Flux"?':("Outworld Devourer", "od", "obsidian destroyer"),
"Which God does Omniknight worship?":"Omniscience", "How many maximum units can Chen take control of with Holy Persuasion?(with talents)":("8", "eight"), "Which hero has the shortest average ability cooldown?":("Bristleback", "bb", "bristle"),
"Which ability allows you to steal gold?":"Jinada", "According to the lore, which hero patrols the Narrow Maze?":"Razor", "Name a hero voiced by Gary Schwartz.":["Lich", "Pugna", "Shadow Shaman", "shaman", "Sniper"],
"Name a hero voiced by John Patrick Lowrie.":["Dark Seer", "Earthshaker", "shaker", "Pudge", "Storm Spirit", "aa", "Ancient Apparition", "sf", "Shadow Fiend", "nevermore" "Doom"], "Which hero is also known as The Nightcrawler?":"Slark",
"What ability does Enchantress gain by acquiring an Aghanim's scepter?":"Sproink", "Name an ability that drains a PERCENTAGE of the targets' mana":["Sinister Gaze", "Fiend's grip"], "Name an active ability that requires no mana or health to cast":["puck out",
"Phase Shift", "Chakra Magic", "Tempest Double"], "What is Earth Spirit's name?":"Kaolin", "According to the lore, which hero was rewarded with the belt of Omexe?":("Centaur Warrunner", "centaur", "cent"),
"Name a hero that throws javelins or spears as their basic attack.":["Huskar", "Enchantress"], 'Which hero has the voiceline "Better to run than curse the road"?':"Clinkz", "Which professional player made the 6 Million dollar Echo slam?":"UNiVeRsE",
'How many heroes can be referred to as "ES"?':("3", "three"), 'Name one of the heroes released with the "Dueling fates"(7.07) update.':["Dark Willow", "mireska", "Pangolier", "pango"], "Which hero has been in the most amount of matches?":"Pudge",
"Name a hero with a hook.":["rizzrack", "timber", "Timbersaw", "rattletrap", "Clockwerk", "Pudge"], "Fill in the blank: ____ gonna have your mana.":"Lich", "Name an ability that takes effect when the target enemy moves":["Chakra Magic", "Rupture"],
"What was the prize pool for the victor at TI1?(in American dollars)":("One Million", "million", "1m", "1million", "1 000 000"), "Which professional team has the record for the longest losing streak?":("B8", "bait"),
"Which non-ultimate ability has the longest cooldown?":"Metamorphosis", "What is blink dagger's max blink range?":("1200", "1.2k"), "How many heroes are in DotA 2 currently?":("119", "onehundreadnineteen", "hungreadninteen"),
"Which neutral item can reset item cooldowns?":("Ex Machina"), "Name a hero that gains a new ability by acquiring Aghanim's Scepter.":["Grimstroke", "Tusk", "ymir", "Snapfire", "Enchantress", "Timbersaw", "timber", "rizzrack", "Arc Warden", "zet", "nyx",
"Nyx Assassin", "Juggernaut", "jugger", "yurnero", "Zeus", "Ogre Magi", "Lycan", "Clockwerk", "rattletrap"], "Which hero has 2 ultimate abilities?":("Dark Willow", "mireska"), "What's Gabe Newell's favorite hero?":("Sand King", "sk", "crixalis"),
"Name a hero that can speak Ozkavosh(The demon language).":["Shadow Demon", "sd", "sf", "Shadow Fiend", "nevermore" "Doom", "Terrorblade", "tb"], 'Who is the professional that player caused the "322 meme"?':"Solo",
"Who commands The Bronze legion?":("Legion Commander", "tresdin", "legion", "lc"), "Fill in the blank: ____ need no armor.":"Wolves", "What's the most expensive item?":("Dagon 5", "dagon five"),
"Name an item that drops when its holder dies.":["Divine Rapier", "rapira", "rapier", "gem", "Gem of True Sight"], "Name an item that can be assembled at the secret shop alone.":["Soul Booster", "rapira", "Divine Rapier",
"rapier", "Eye of Skadi", "skadi", "octarine", "Octarine Core", "Scythe of Vyse", "scythe", "sheepstick", "Lotus Orb", "lotus", "Perseverance", "Moon Shard"], "Name an item that amplifies healing(incoming or outgoing).":["Holy Locket",
"heart", "Heart of Tarrasque", "tarrasque"], 'What other nickname does the youtuber Trymike4instance use?':"mav", "Who's Pugna's pet?":("Viper", "netherdrake"), "Which hero's all 3 attributes are equal?":"Bane", "What's the fifth rank medal?":"Legend",
"How else is The Ancient often referred as?":"The Throne", "Which hero is a pope?":("Necrophos", "necro", "necrolyte"), "What's the name of the wisp Keeper of the Light summons with his ultimate ability?":"Ignis Fatuus",
"Which hero can bring a teammate to himself anywhere from the map?":"Chen", "Which spell does Wex-Wex-Exort invoke?":"Alacrity", "Name a hero with a flying mount.":"Batrider", "Which hero has the lowest agility gain?":"Tiny",
"Which passive skill heals the hero with a fixed amount of HP on each hit?":"Ransack", "Which Strength hero has the lowest strength?":("Io", "wisp"), "What did Naga Siren say at Tidehunter's grave?":"RIP Tide",
"Name a hero that uses its voice in battle.":["Beastmaster", "qop", "akasha", "Queen of Pain", "naga", "Naga Siren"], "Which hero works for the Flayed Twins?":"Bloodseeker", "Which hero's primary attribute is also its lowest?":("Arc Warden", "zet"),
"What nickname is the professional player Daryl Koh Pei Xiang known as?":("iceiceice", "ice3"), "Which hero is notorious for having a long head?":"Dark Seer", "How many DotA heroes are arthropods?":("4", "four"),
"Which color signifies mystery or The Unknown in the world of DotA?":"Purple", "How many ring items are there?(including neutral items)":("10", "ten"), ("Which unit has this ability?", "Poison_Sting.png"):("Spiderite", "spiderling"),
("What's the name of the shown spell?", "LVL_Death.png"):("LVL? Death", "level? death"), 'Which hero says "Come back and die again." after killing an enemy?':("Troll Warlord", "troll", "jah'rakal"),
"Which hero has the slowest basic attack projectile?":("Winter Wyvern", "ww", "wyvern"), "What's the longest duration channelling ability?":"tornado", 'Which neutral creeps are sometimes referred to as "Tomato" and "Potato"?':("Hellbears", "hellbear"),
"Which neutral Satyr can cast purge?":("Satyr Banisher", "banisher"), "Which unit has the Fireball ability?":("Ancient Black dragon", "black dragon"), "Which hero has the highest base attack range?":"Techies",
"Which item can assembled in mutliple different ways?":("Power Treads", "treads"), "Name a hero that has lower vision during the day.":("Night Stalker", "balanar"), "Which item grants True Strike?":("Divine Rapier", "rapira", "rapier"),
"Which hero has the lowest base attack time?":"Doom", "Which ability counters Shallow Grave?":"Culling Blade", "Which hero can steal its targets movement and attack speed?":"Visage",
"Name a hero with an odd number of natural horns.":["Magnus", "Tiny"], "Which hero is the son of a Vigil Knight?":"Sven", "Which hero has a 17% chance to bash on hit?(Without talents)":("Spirit breaker", "bara", "sb", "barathrum"),
"How many Reactive Armor stacks can Timbersaw have at max?(With talents)":("30", "thirty"), "Which hero can have a bonus while on the river?":"Slardar", "What's Underlords name?":"Vrogros",
"Except Pheonix and Tinker, which hero can reset its cooldowns without Refresher Orb?":["Clockwerk", "rattletrap", "Rubick"], "What is Snapfire to Timbersaw?(as a relative)":"Aunt", "Which hero is oldest by age?":"Void Spirit",
"Which hero says only 4 words on each voiceline?":("Ember Spirit", "ember", "xin"), "Which passive talent allows the hero to completely avoid any type of damage?":"Backtrack", "Name a hero with a passive ultimate ability.":["Ogre Magi",
"Phantom Lancer", "lancer", "pl", "Drow Ranger", "Drow", "Phantom Assassin", "pa", "Dazzle", "Riki", "rikimaru", "Wraith King", "wk", "Tiny", "bb", "BristleBack"], "What type of damage do Psi Blades deal?":"Pure", "Which hero can speak in reverse?":"Spectre",
"Which city hosted TI8?":"Vancouver", "Name a point-target ability that disarms.":("Fate's edict"), 'Which hero has the voiceline "Consider thyself purified"?':("Anti-Mage", "magina", "am"), "How many extra souls can Shadow Fiend keep by acquiring an Aghanim's Scepter?":("5", 'five'),
"Which hero leaves a very clear trail of footprints behind them?":("Terrorblade", "tb"), "Name a hero that has wings but doesn't use it for flight.":["Doom", "Terrorblade", "tb", "qop", "Queen of Pain", "akasha", "sf", "Shadow Fiend", "nevermore"],
"Name a hero based on ancient mythology.":["Zeus", "gorgon", "Medusa", "Mars", "Pheonix", "icarus", "Monkey King", "mk", "wukong"], "At max how many attacks does it take to destroy Pheonix' Supernova?(With talents and Aghanim's Scepter)":("16", "sixteen"),
"Which professional player's face is a Twitch emote?":("Dendi", "danylo ishutin", "danylo"), "Which hero has been to hell and back and back to hell and back?":"Lion", "Name a hero that can get a permanent buff.":["Clinkz", "Slark", "Legion Commander", "legion", "lc" "tresdin", "Pudge", "Silencer", "Underlord", "Lion"],
"Who does ODpixel usually cast competitive games with?":"Fogged", "Which hero does SirActionSlacks despise?":("Windranger", "wr", "windrunner"), "How many TI's have been hosted in the USA?":("6", "six"),
"Which professional team has been in the most amount of TI finals?":("Natus Vincere", "navi"), "Which year did the first Compendium/BattlePass come out?":"2013", 'Which hero has the response "Oh, look at it go!"?':("Witch Doctor", "wd", "Zharvakko"),
"Which tournament was the first to have a True Sight documentary?":"Kiev Major", "Which hero was the first to get an arcana?":"Lina", "Which professional player is notorious for playing Nature's Prophet and Lone Druid?":("AdmiralBulldog", "bulldog", "bulldong"),
'''Which hero has the voiceline "If killing you is wrong, I don't want to be right."?''':"Dazzle", "Which hero fears trees?":("Timbersaw", "timber", "rizzrack"), "Which player was the first to surpass 9000 mmr?":"Miracle-",
'Which hero has "Riki was here" carved onto them?':("Treant Protector", "treant"), "Which Tier of neutral items has the most amount of items?":("The fifth", "tier 5", "five", "5"),
"How much gold can Cheese be sold for?":("500", "five hundred", "0.5k"), "Which hero is known as the Arsenal Magus?":("Invoker", "injoker", "carl"), "In what year did Skeleton King become a wraith?":"2013",
"Name one of the Fundamentals.":["Keeper of the Light", "Enigma", "kotl", "ck", "Io", "Chaos Knight", "wisp"], "Name an ability that can turn day into night or night into day.":["Supernova", "Eclipse", "Dark Ascension"],
"Name a hero which has a talent that increases Night Vision.":["Spirit Breaker", "bara", "barahtrum", "Winter Wyvern", "ww", "auroth", "Slardar"], "Name an item that can grant bonus Night Vision.":["Moon Shard", "Vampire Fangs"], "How many heroes use a gun as a weapon?":("3", "three"),
"Name an item that the courier can't pick up from the ground.":["Aegis of the Immortal", "Divine Rapier", "rapier", "rapira", "aegis"], "Name an item that can incrase attack range?":["Broom Handle", "Enchanted Quiver", "Hurricane Pike", "Grove Bow", "Dragon Lance", "Ballista", "Telescope"],
"How many methods to hex exist?":("4", "four"), "Name an ability that can cause the hypnosis debuff on an enemy.":["Sinister Gaze", "Aether Remnant", "Will-O-Wisp", "ignis fatuus"], "Who's that handsome devil?":("Storm Spirit", "storm"),
"Name a NON-Ultimate ability that has global cast range.":["Living armor", "Rocket Flare", "Sunstrike", "Teleportation", "Nimbus", "Divine Favor", "charge", "Charge of Darkness"], "What year did DotA2 switch to the Source 2 engine?":"2015",
"What color is Kaya and Sange?":"Purple", "Name an item that reduces cooldowns.":["Octarine Core", "octarine", "Quickening Charm", "Spell Prism"], "Who's both accurate and precise?":("Clockwerk", "rattletrap", "clock"),
'Which hero has the voiceline "No room to swing a cat in this crowd."?':"Kunkka", "Which hero was the first to be released exclusively in DotA 2?":("Monkey King", "mk", "makaka"), "What is the name of Chaos Knight's horse?":"Armageddon",
"Which hero did Pudge barely win the arcana vote against in 2018?":"Rubick", "Name a hero of the Oglodi race.":["Warlock", "Axe", "Disruptor", "Lifestealer", "naix"], "Name a hero that has multiple charges of his/her ultimate ability.":["Ember Spirit", "Void Spirit", "xin", "inai", "ember", "Vengeful Spirit", "vengeful", "venge"],
"Who is Rubick's father?":"Aghanim", "Name one of the two heroes who were main characters of Wronchi's DotA animations.":["Rubick", "Enigma"], "What type of damage do proximity mines deal?":"Magical",
"Which hero has a cosmetic set dedicated to Ixmike88?":("Crystal Maiden", "cm"), "Name a mountless knight.":["Dragon Knight", "dk", "Omniknight", "Sven", "rogue knight"], "Who's was the youngest professional player to play in a TI?":"SumaiL",
"How many seconds does it take to teleport to an outpost for the first player?":("6", "six", "way too long", "too long"), "Name an item that has a Strong Dispel.":["Aeon Disk", "Magic Lamp"], "How many minutes is the buyback cooldown?":("8", "eight"),
"How much max health does Roshan gain every minute?":"115", "Which item decreases enemy attack speeds?":("Shiva's Guard", "shiva"), "What type of incoming damage does Vanguard decrease?":"Physical",
"Which type of debuff disables all use of items?":"Mute", "Name an ability increases Status Resistance.":["Bullldoze", "Enrage"], "According to the lore, which item was made for Thor?":"Mjollnir", "How else is Scythe of Vyse often referred as?":("Sheepstick", "hex"),
"How many ways exist to go in an ethereal form?":("4", "four"), "Which type of gold do last hits give?":"Unreliable", "How many charges do Drums of Endurance have?":("6", "six"), "How much damage per second does Armlet of Mordiggian deal to it's owner while active?":("54", "fifty four"),
"How much gold does Smoke of Deceit cost?":("50", "fifty"), "How much magic damage can an Infused Raindrop block?":"120", "Name an item that can be assembled using a Blight Stone.":["Medallion of Courage", "medallion", "Desolator", "deso"],
"What type of damage does a Javelin deal?":"Magical", "How much movement speed do units controlled with a Helm of the Dominator have?":"425", "Which item is made with two Perseverances?":("Refresher Orb", "refresher"), """Which item has an ability called "Combo Breaker"?""":"Aeon Disk",
"Which item has different cooldowns for ranged and melee heroes?":("Manta Style", "manta"), "Which item has a percentage based manacost?":"BloodStone", "Which item can be used on an ally for a Basic Dispel?":("Lotus Orb", "lotus"), "Which item can deal magical damage to buildings?":"Meteor Hammer",
"""Which item is an "upgrade" of Crystalys?""":"Daedalus", "What's the cast range of Abyssal Blade's active ability?":"550", "Name an item that gives evasion.":["Radiance", "Talisman of Evasion", "talisman", "Butterfly", "Heaven's Halberd", "halberd"],
"Which item can cause a Break debuff on the enemy?":"Silver Edge", "Which item grants the strongest passive Status Resistance?":"Satanic", "Vhich item's description is vritten in this manner?":"Orb of Venom",
"Which ability spawns trees?":"Sprout", "How many Power-Up runes are there?":("6", "six"), "What's the Movementspeed Cap for most units?":"550", "Which ability has the longest cast point?":"Teleportation", "Name an unit that deals bonus damage to buildings.":["Earth", "catapult", "Siege Creep", "Spirit Bear"],
"How many heroes can deny themselves?":("3", "three"), "Name an ability that allows players to deny allies.":["Venemous Gale", "gale", "Shadow Strike", "Doom"], "How many abilities can grant cleave?":("3", "three"), "What's the maximum movement speed a courier can have?":"580",
"Name a hero with a chance based bash.":["Faceless Void", "faceless", "Spirit Breaker", "bara", "sb", "barathrum"], """Which hero shouts "I SAID GOOD DAY SIR!"?""":("Axe", "Mogul Khan"), "Which actor voices Pangolier?":"Phil Lamarr"}
#Getting the dictionary length and it's keys and values as seperate lists.
questlen = len(questdict)-1
questkeys, questvalues = list(questdict.keys()), list(questdict.values())

#The dictionary of item images and each of their components, if an item is made by items from at least one of which can be named in two different ways the value of the image will be a list of lists, first list has the normal, official name item build and the others have alternate names,
#all lists of a list must contain the same amount of items so some items such as "Recipe" must be written in all lists within a list even though there is no alternate word for it.
shopkeepdict = {"Oblivion_Staff.png":["Quarterstaff", "Sage's Mask", "Robe of the magi"], "Orchid_Malevolence.png":["Oblivion Staff", "Oblivion Staff", "Recipe"],
"Bloodthorn.png":[["Orchid Malevolence", "Hyperstone", "Recipe"], ["orchid", "hyperstone", "Recipe"]], "Magic_Wand.png":[["Magic Stick", "Iron Branch", "Iron Branch", "Recipe"], ["Stick", "branch", "branch", "Recipe"]],
"Abyssal_Blade.png":[["Skull Basher", "Vanguard", "Recipe"],["basher", "vanguard", "Recipe"]], "Aeon_disk.png":["Vitality Booster", "Energy Booster", "Recipe"], "Aether_Lens.png":["Energy Booster", "Void Stone", "Recipe"],
"Aghanims_Scepter.png":["Point Booster", "Ogre Axe", "Blade of Alacrity", "Staff of Wizardry"], "Arcane_boots.png":[["Energy Booster", "Boots of Speed"], ["energy booster", "boots"]],
"Armlet_of_Mordiggian.png":[["Helm of Iron will", "Blades of Attack", "Gloves of Haste", "Recipe"], ["helm of ironwill", "claws of attack", "gloves", "Recipe"]], "Assault_Cuirass.png":["Platemail", "Hyperstone", "Buckler", "Recipe"],
"Battle_Fury.png":["Broadsword", "Claymore", "Perseverance", "Quelling blade"], "Black_King_Bar.png":["Ogre Axe", "Mithril Hammer", "Recipe"], "Blade_Mail.png":["Broadsword", "Chainmail", "Recipe"], "Bloodstone.png":["Kaya", "Soul Booster"],
"Boots_of_Travel.png":[["Boots of Speed", "Recipe"], ["boots", "Recipe"]], "Bracer.png":[["Circlet", "Gauntlets of Strength", "Recipe"], ["circlet", "gauntlets", "Recipe"]], "Buckler.png":["Ring of Protection", "Recipe"],
"Butterfly.png":[["Eaglesong", "Talisman of Evasion", "Quarterstaff"], ["eaglesong", "talisman", "quarterstaff"]], "Crimson_Guard.png":["Vanguard", "Helm of Iron will", "Recipe"], "Crystalys.png":["Broadsword", "Blades of Attack", "Recipe"],
"Daedalus.png":["Crystalys", "Demon Edge", "Recipe"], "Dagon.png":["Belt of Strength", "Band of Elvenskin", "Robe of the Magi", "Recipe"], "Desolator.png":["Mithril Hammer", "Mithril Hammer", "Blight Stone"], "Diffusal_Blade.png":["Blade of Alacrity", "Blade of Alacrity", "Robe of the Magi", "Recipe"],
"Divine_Rapier.png":["Sacred Relic", "Demon Edge"], "Dragon_lance.png":["Ogre Axe", "Band of Elvenskin", "Band of Elvenskin"], "Drum_of_Endurance.png":["Sage's Mask", "Crown", "Wind Lace", "Recipe"],
"Echo_Sabre.png":["Ogre Axe", "Oblivion Staff"], "Ethereal_Blade.png":["Eaglesong", "Ghost Scepter"], "Euls_Scepter_of_Divinity.png":["Staff of Wizardry", "Void Stone", "Wind Lace", "Recipe"], "Eye_of_Skadi.png":["Ultimate Orb", "Ultimate Orb", "Point Booster"],
"Force_Staff.png":["Staff of Wizardry", "Ring of Regen", "Recipe"], "Glimmer_Cape.png":[["Shadow Amulet", "Cloak", "Gloves of Haste"],["amulet", "cloak", "gloves"]], "Guardian_Greaves.png":[["Mekansm", "Arcane Boots", "Recipe"], ["mekansm", "manaboots", "Recipe"]],
"Hand_of_Midas.png":[["Gloves of Haste", "Recipe"],["gloves", "Recipe"]], "Headdress.png":["Ring of Regen", "Recipe"], "Heart_of_Tarrasque.png":["Ring of Tarrasque", "Vitality Booster", "Reaver", "Recipe"],
"Heavens_Halberd.png":[["Sange", "Talisman of Evasion"],["sange", "Talisman"]], "Helm_of_the_Dominator.png":["Helm of Iron Will", "Crown", "Recipe"], "Holy_Locket.png":[["Ring of Tarrasque", "Energy Booster", "Magic Wand", "Recipe"], ["ring of tarrasque", "energy booster", "wand", "Recipe"]],
"Hood_of_Defiance.png":["Ring of Health", "Cloak", "Ring of Regen", "Recipe"], "Hurricane_Pike.png":["Force Staff", "Dragon Lance", "Recipe"], "Kaya.png":["Staff of Wizardry", "Robe of the Magi", "Recipe"], "Linkens_Sphere.png":["Ultimate Orb", "Perseverance", "Recipe"],
"Lotus_Orb.png":["Perseverance", "Platemail", "Energy Booster"], "Maelstrom.png":["Mithril Hammer", "Javelin"], "Manta_Style.png":["Yasha", "Ultimate Orb", "Recipe"], "Mask_of_Madness.png":["Morbid Mask", "Quarterstaff"],
"Medallion_of_Courage.png":["Chainmail", "Sage's Mask", "Blight Stone"], "Mekansm.png":["Headdress", "Buckler", "Recipe"], "Meteor_Hammer.png":["Perseverance", "Crown", "Recipe"],
"Mjollnir.png":["Maelstrom", "Hyperstone", "Recipe"], "Monkey_King_Bar.png":["Demon Edge", "Javelin", "Blitz Knuckles"], "Moon_shard.png":["Hyperstone", "Hyperstone"], "Necronomicon.png":["Sage's Mask", "Sage's Mask", "Belt of Strength", "Recipe"],
"Null_Talisman.png":["Circlet", "Mantle of Intelligence", "Recipe"], "Nullifier.png":["Sacred Relic", "Helm of Iron Will"], "Octarine_Core.png":["Voodoo Mask", "Soul Booster", "Recipe"], "Perseverance.png":["Ring of Health", "Void Stone"],
"Phase_Boots.png":[["Boots of Speed", "Chainmail", "Blades of Attack"], ["boots", "chainmail", "blades of attack"]], "Pipe_of_Insight.png":[["Hood of Defiance", "Headdress", "Recipe"], ["hood", "headress", "recipe"]],
"Power_Treads.png":[["Boots of Speed", "Gloves of Haste", "Belt of Strength"],["boots", "gloves", "band of elvenskin"],["boots", "Gloves", "robe of the magi"]], "Radiance.png":["Sacred Relic", "Recipe"],
"Refresher_Orb.png":["Perseverance", "Perseverance", "Recipe"], "Ring_of_Basilius.png":["Sage's Mask", "Recipe"], "Rod_of_Atos.png":["Staff of Wizardry", "Crown", "Crown", "Recipe"],
"Sange.png":["Ogre Axe", "Belt of Strength", "Recipe"], "Satanic.png":["Morbid Mask", "Claymore", "Reaver", "Recipe"], "Scythe_of_Vyse.png":["Mystic Staff", "Ultimate Orb", "Void Stone"],
"Shadow_Blade.png":["Shadow Amulet", "Blitz Knuckles", "Broadsword"], "Shivas_Guard.png":["Platemail", "Mystic Staff", "Recipe"], "Silver_Edge.png":["Shadow Blade", "Echo Sabre", "Recipe"], "Skull_Basher.png":["Mithril Hammer", "Belt of Strength", "Recipe"],
"Solar_Crest.png":[["Medallion of Courage", "Ultimate Orb", "Wind Lace", "Recipe"], ["medallion", "ultimate orb", "wind lace", "Recipe"]], "Soul_Booster.png":["Vitality Booster", "Energy Booster", "Point Booster"],
"Soul_Ring.png":[["Ring of Protection", "Gauntlets of Strength", "Gauntlets of Strength", "Recipe"],["ring of protection", "gauntlets", "gauntlets", "Recipe"]], "Spirit_Vessel.png":[["Urn of Shadows", "Vitality Booster", "Recipe"],["urn", "vitality booster", "Recipe"]],
"Tranquil_Boots.png":[["Boots of Speed", "Wind Lace", "Ring of Regen"], ["boots", "wind lace", "ring of regen"]], "Urn_of_Shadows.png":["Sage's Mask", "Circlet", "Ring of Protection", "Recipe"],
"Vanguard.png":["Ring of Health", "Vitality Booster"], "Veil_of_Discord.png":["Ring of Basilius", "Crown", "Recipe"], "Vladmirs_Offering.png":["Ring of Basilius", "Blades of Attack", "Morbid Mask", "Recipe"],
"Wraith_Band.png":["Circlet", "Slippers of Agility", "Recipe"], "Yasha.png":["Blade of Alacrity", "Band of Elvenskin", "Recipe"]}

shopkeeplen = len(shopkeepdict)-1
shopkeepkeys, shopkeepvalues = list(shopkeepdict.keys()), list(shopkeepdict.values())

#lists of Replies in case of right, wrong or no/late answers
rightansw = ["That is correct!", "That's correct.", "Correct answer!", "You're right!", "Your answer is correct!", "Nice one.", "That answer is correct!"]
wrongansw = ["That's not quite right.", "That's not right...", "Your answer isn't correct.", "You're mistaken.", "Not correct...", "Not quite it...", "From the Ghastly Eyrie I can see to the ends of the world, and from this vantage point I declare with utter certainty that your answer is wrong." , "YOU GET NOTHING, GOOD DAY SIR!"]
lateansw = ["You ran out of time.", "Too late.", "You didn't answer in time.", "Be quicker next time...", "You're out of time.", "Out of time.", "Time grinds even questions to dust.", "You took too much time."]

#with open("users.json", "r") as fp:      #load the users.json file
#        users = json.load(fp)
#with open("rngfix.json", "r") as fp:     #load the rngfix.json file
#        rng = json.load(fp)

def open_json(jsonfile):
    with open(jsonfile, "r") as fp:      #load the users.json file
        return json.load(fp)       #openfunc for jsonfiles

def save_json(jsonfile, name):           #savefunc for jsonfiles
    with open(jsonfile, "w") as fp:
        json.dump(name, fp)

def add_gold(user: discord.User, newgold: int):           #add gold to users
    users = open_json("users.json")
    id = str(user.id)
    if id not in users.keys():                  #if user not already in users.json add user
        users[id] = {"gold":10, "items":"[]"}
        users[id]["gold"] = users[id]["gold"] + round(newgold)
        save_json("users.json", users)
        return round(newgold)
    else:
        if 2200 in ast.literal_eval(users[id]["items"]):
            users[id]["gold"] = users[id]["gold"] + round(newgold*1.25)
            save_json("users.json", users)
            return round(newgold*1.25)
        else:
            users[id]["gold"] = users[id]["gold"] + round(newgold)
            save_json("users.json", users)
            return round(newgold)

def pseudorandomizer(server, length, listkey: str):  #pseudorandomizer used in par with the rngfix.json file to avoid repeating numbers(questions)
    rng = open_json("rngfix.json")
    serv_id = str(server.id)
    if serv_id not in rng.keys():                #add channel to rngfix.json if not already in
        rng[serv_id] = {"questnumbers":"[]", "shopkeepnumbers":"[]", "vacuumcd":16}
        save_json("rngfix.json", rng)
    numlist = ast.literal_eval(rng[serv_id][listkey])        #convert list string to list
    if len(numlist) > round(length*3/4):         #if list of numbers in rngfix goes over 100 delete the first number
        del numlist[:round(length/5)]
        save_json("rngfix.json", rng)
    while True:
        n = random.randint(0, length)
        if n not in numlist:    #get a number that isn't already used and append it to the list of numbers in use
            numlist.append(n)
            rng[serv_id][listkey] = str(numlist)        #convert list back to string list
            save_json("rngfix.json", rng)
            return n

def strip_str(text):                 #function to remove punctuations, spaces and "the" from string and make it lowercase,
    punctuations = ''' !-;:`'"\,/_?'''  # in order to compare bot answers and user replies
    text2 = ""
    for char in text:
       if char not in punctuations:
           text2 = text2 + char
    return text2.lower().replace("the", "")

def calc_time(question, answer):           #Function to calculate time for each question according to its size(for blitz)
    queslen = len(question)
    if type(answer) == str:         #takes the length of the raw answer
        answlen = len(answer)
    else:                         #takes the average length of all answers
        answlen = sum(map(len, answer))/len(answer)
    seconds = queslen/7 + answlen/4
    if seconds > 12:          #balances it(I think)
        seconds -= 3
    return seconds

def set_time(author, duration):      #Set duration for quiz commands(30% more time if shiva is held)
    users = open_json("users.json")
    try:
        if 4850 in ast.literal_eval(users[str(author.id)]["items"]):
            duration += duration*0.3
            return duration
        else:
            return duration
    except KeyError:
        pass

def aegis(author, lives):              #Set amount of lives(+1 if the user has aegis)
    users = open_json("users.json")
    try:
        if 8000 in ast.literal_eval(users[str(author.id)]["items"]):
            return lives+1
        else:
            return lives
    except KeyError:
        pass

class Quizes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief = "Rapid questions that give more gold but with a risk.")
    @commands.cooldown(1, 52, commands.BucketType.channel)
    async def blitz(self, ctx):
        server, channel, author = ctx.guild, ctx.channel, ctx.author
        timeout = time.time() + set_time(author, 50)                    #full time for blitz round
        accumulated_g = 0
        ncorrectansws = 0
        await ctx.send(f"""You have ``{set_time(author, 48)}`` seconds for the blitz, don't forget to type in **skip** if you don't know the answer to minimize the gold and time you lose.""")
        time.sleep(3.7)
        while True:
            time.sleep(0.3)
            if time.time() > timeout:                    #stop the blitz, add accumulated gold to user.
                g = add_gold(author, (accumulated_g + (2*ncorrectansws*(ncorrectansws - 1)))) #((2a+d(n-1))/2)n a = 0 d = 4  n = ncorrectanswsers
                await ctx.send(f"**{author.display_name}** you got ``{ncorrectansws}`` correct answers and accumulated ``{g}`` gold during the blitz.")
                break
            questn = pseudorandomizer(server, questlen, "questnumbers") #Random number to give a random question
            correctansw = ""
            if type(questvalues[questn]) == str:
                correctansw = questvalues[questn]
            elif type(questvalues[questn]) == tuple:
                correctansw = questvalues[questn][0]
            else:
                correctansw = random.choice([z for z in questvalues[questn] if z[0].isupper()])
            if type(questkeys[questn]) == tuple:           #if the question comes with an image
                await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
                giventime = set_time(author, calc_time(questkeys[questn][0], questvalues[questn]))
            else:                                          #for normal string questions
                await ctx.send(f"**```{questkeys[questn]}```**")
                giventime = set_time(author, calc_time(questkeys[questn], questvalues[questn]))
            def check(m):
                return m.channel == channel and m.author == author      #checks if the reply came from the same person in the same channel
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=giventime)
            except asyncio.TimeoutError:                                #If too late
                await channel.send(f"**{random.choice(lateansw)}**, The correct answer was ``{correctansw}``.")
                accumulated_g -= 21
            else:
                if strip_str(msg.content) == "skip":        #if user wants to move onto the next question
                    accumulated_g -= 4
                    if type(questvalues[questn]) == str or type(questvalues[questn]) == tuple:
                        await channel.send(f"The correct answer was ``{correctansw}``.")
                    else:
                        await channel.send(f"One of the possible answers was ``{correctansw}``.")


                elif type(questvalues[questn]) == str or type(questvalues[questn]) == tuple and strip_str(msg.content) != "skip":     #If there is one correct answer
                    if strip_str(msg.content) == strip_str(questvalues[questn]) or strip_str(msg.content) in [strip_str(x) for x in questvalues[questn] if type(questvalues[questn]) == tuple]:
                        accumulated_g += 12
                        ncorrectansws += 1
                    else:
                        await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``.")
                        accumulated_g -= 12

                else:                                                   #If there are multiple answers
                    if strip_str(msg.content) in [strip_str(y) for y in questvalues[questn]]:
                        accumulated_g += 10
                        ncorrectansws += 1
                    else:
                        await channel.send(f"**{random.choice(wrongansw)}** One of the possible answers was ``{correctansw}``")
                        accumulated_g -= 8

    @commands.command(brief = "Endlessly sends DotA2 items to be assembled.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def shopquiz(self, ctx):
        server, channel, author = ctx.guild, ctx.channel, ctx.author     #get users server, channel and author
        accumulated_g = 0             #gold that will be given to the user at the end
        lives = aegis(author, 3)      #tries they have for the shopkeeperquiz
        correctitems = 0              #number of items they completed
        while True:                   #while lives are more than 0 it keeps sending new items to build once the previous item is completed/skipped
            if lives <= 0.4:            #ends the shopquiz
                g = add_gold(author, accumulated_g)
                await ctx.send(f"**{author.display_name}** You're out of lives, You built ``{correctitems}`` items and accumulated ``{g}`` gold during the Shopkeepers Quiz.")
                break
            elif lives == 322:          #if the quiz is stopped by command
                g = add_gold(author, accumulated_g)
                await ctx.send(f"**{author.display_name}** You built ``{correctitems}`` items and accumulated ``{g}`` gold during the Shopkeepers Quiz.")
                break
            elif correctitems == 88:
                g = add_gold(author, (accumulated_g+5000))
                await ctx.send(f"**{author.display_name}** You built every item and accumulated ``{g}`` gold during the Shopkeepers Quiz.")
                break
            shopkeepn = pseudorandomizer(server, shopkeeplen, "shopkeepnumbers")
            #create two lists of correct answers, itemanswers takes in stripped correct answers inside multiple lists while itemanswersmerged takes it all as one list
            itemanswers, itemanswersmerged = [], []
            if type(shopkeepvalues[shopkeepn][0]) == list:
                correctansw = "``, ``".join(shopkeepvalues[shopkeepn][0])  #creates a highlighted string of correct items
                for index, items in enumerate(shopkeepvalues[shopkeepn]):
                    itemanswers.append([])         #to create a list within a list which gets appended later
                    for answ in items:
                        itemanswers[index].append(strip_str(answ))
                        itemanswersmerged.append(strip_str(answ))
            else:
                correctansw = "``, ``".join(shopkeepvalues[shopkeepn])   #creates a highlighted string of correct items
                for k in shopkeepvalues[shopkeepn]:
                    itemanswers.append(strip_str(k))
                    itemanswersmerged.append(strip_str(k))

            await ctx.send("List the items that are required to assemble the shown item **One By One**.", file=discord.File(f"./shopkeepimages/{shopkeepkeys[shopkeepn]}"))

            while True:                    #while item is yet to be completed it takes in answers, checks them and uses them
                if len(itemanswersmerged) == 0:      #stops the single item answer collecting
                    correctitems += 1
                    accumulated_g += 20 + (correctitems * 8)
                    await ctx.send("*Item complete.*")
                    break
                elif lives == 322 or lives <= 0.4:
                    await ctx.send(f"You could've built this item with ``{correctansw}``.")
                    break

                def check(m):                #simple checker
                    return m.channel == channel and m.author == author
                try:
                    msg = await self.bot.wait_for("message", check=check, timeout=set_time(author, 20.322))
                except asyncio.TimeoutError:                                #If too late
                    lives -= 1
                    await channel.send(f"**{random.choice(lateansw)}**, you have ``{lives}`` lives remaining.")
                    accumulated_g -= 10
                else:
                    if strip_str(msg.content) == "stop":           #changes lives number to 322 and stops the quiz
                        lives = 322
                        break
                    elif strip_str(msg.content) == "skip":      #skip a single item and lose 0.5 life for it
                        lives -= 0.5
                        await ctx.send(f"This item could've been built with ``{correctansw}``, you have ``{lives}`` lives remaining.")
                        break
                    elif type(itemanswers[0]) == list:                         #if itemanswers has lists of correct answers it checks the correct answ in
                        if strip_str(msg.content) in itemanswersmerged:            #itemanswersmerged, gives reward
                            await ctx.send(f"**{random.choice(rightansw)}**")
                            accumulated_g += 6
                            itemstopop = []                                #create a new list of items that must be removed from itemanswersmerged
                            for itemlist in itemanswers:
                                if strip_str(msg.content) in itemlist:          #check index of correct answer to remove from all lists of itemanswers
                                    n = itemlist.index(strip_str(msg.content))
                            for index, itemlist in enumerate(itemanswers):
                                itemstopop.append(itemanswers[index][n])
                                itemanswers[index].pop(n)                     #pop answered item out of all lists of the itemanswers
                            for item in itemstopop:                      #loop through itemstopop and remove each item of it from itemanswersmerged
                                itemanswersmerged.remove(item)
                        else:
                            lives -= 1
                            await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")
                    else:
                        if strip_str(msg.content) in itemanswers:               #if itemanswers is just a list of strings, remove answered item from both lists.
                            await ctx.send(f"**{random.choice(rightansw)}**")
                            accumulated_g += 7
                            itemanswers.remove(strip_str(msg.content))
                            itemanswersmerged.remove(strip_str(msg.content))
                        else:
                            lives -= 1
                            await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")

    @commands.command(brief = "Sends quizes and items to assemble endlessly.")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def endless(self, ctx):
        server, channel, author = ctx.guild, ctx.channel, ctx.author  #the server, channel and author of the command activator
        accumulated_g = 0    #accumulated gold during the quiz
        ncorrectansws = 0    #number of correct answers
        lives = aegis(author, 5)
        while True:              #keeps asking questions till it breaks
            if lives == 0:               #break the whole command if lives are 0 or 322(which means the command was stopped by user)
                g = add_gold(author, (accumulated_g + (ncorrectansws*(ncorrectansws - 1)))) #((2a+d(n-1))/2)n a = 0 d = 2  n = ncorrectansws
                await ctx.send(f"You ran out of lives and you accumulated ``{g}`` gold by getting ``{ncorrectansws}`` correct answers.")
                break
            if lives == 322:
                g = add_gold(author, (accumulated_g + (ncorrectansws*(ncorrectansws - 1))))
                await ctx.send(f"You have stopped the endless quiz, you accumulated ``{g}`` gold by getting ``{ncorrectansws}`` correct answers.")
                break
            if random.randint(0, 1) == 0:          #if random number is 0 the question will be quiz
                    questn = pseudorandomizer(server, questlen, "questnumbers") #Random number to give a random question
                    correctansw = ""                      #obtaining the correct answer to display later
                    if type(questvalues[questn]) == str:
                        correctansw = questvalues[questn]
                    elif type(questvalues[questn]) == tuple:
                        correctansw = questvalues[questn][0]
                    else:
                        correctansw = random.choice([z for z in questvalues[questn] if z[0].isupper()])
                    if type(questkeys[questn]) == tuple:           #if the question comes with an image
                        await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
                    else:                                          #for normal string questions
                        await ctx.send(f"**```{questkeys[questn]}```**")
                    def check(m):
                        return m.channel == channel and m.author == author      #checks if the reply came from the same person in the same channel
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=set_time(author, 16.322))
                    except asyncio.TimeoutError:               #If too late
                        lives -= 1
                        await channel.send(f"**{random.choice(lateansw)}**, the correct answer was ``{correctansw}``, ``{lives}`` lives left.")
                        accumulated_g -= 15
                    else:
                        if strip_str(msg.content) == "skip":         #if user skips a question
                            lives -= 1
                            await ctx.send(f"The correct answer was ``{correctansw}``, you have ``{lives}`` remaining.")
                        elif strip_str(msg.content) == "stop":       #if user stops the "endless" quiz
                            lives = 322
                        elif type(questvalues[questn]) == str or type(questvalues[questn]) == tuple and strip_str(msg.content) != "skip" and strip_str(msg.content) != "stop":
                            if strip_str(msg.content) == strip_str(questvalues[questn]) or strip_str(msg.content) in [strip_str(x) for x in questvalues[questn] if type(questvalues[questn]) == tuple]:     #If there is only one correct answer
                                accumulated_g += 14
                                ncorrectansws += 1
                            else:
                                lives -= 1
                                await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``, ``{lives}`` lives remaining.")

                        else:           #If correct answer is in a list(there are multiple answers)
                            if strip_str(msg.content) in [strip_str(y) for y in questvalues[questn]]:
                                accumulated_g += 9
                                ncorrectansws += 1
                            else:
                                lives -= 1
                                await channel.send(f"**{random.choice(wrongansw)}** One of the possible answers was ``{correctansw}``, ``{lives}`` lives remaining")

            else:       #if random integer is 1 the question is a single shopquiz
                shopkeepn = pseudorandomizer(server, shopkeeplen, "shopkeepnumbers")
                #create two lists of correct answers, itemanswers takes in stripped correct answers inside multiple lists while itemanswersmerged takes it all as one list
                itemanswers, itemanswersmerged = [], []
                if type(shopkeepvalues[shopkeepn][0]) == list:
                    correctansw = "``, ``".join(shopkeepvalues[shopkeepn][0])   #creating string of highlighted correct answers
                    for index, items in enumerate(shopkeepvalues[shopkeepn]):
                        itemanswers.append([])         #to create a list within a list which gets appended later
                        for answ in items:
                            itemanswers[index].append(strip_str(answ))
                            itemanswersmerged.append(strip_str(answ))
                else:
                    correctansw = "``, ``".join(shopkeepvalues[shopkeepn])   #creating string of highlighted correct answers
                    for k in shopkeepvalues[shopkeepn]:
                        itemanswers.append(strip_str(k))
                        itemanswersmerged.append(strip_str(k))

                await ctx.send("List the items that are required to assemble the shown item **One By One**.", file=discord.File(f"./shopkeepimages/{shopkeepkeys[shopkeepn]}"))

                while True:                    #while item is yet to be completed it takes in answers, checks them and uses them
                    if len(itemanswersmerged) == 0:      #stops the individual item answer collecting
                        ncorrectansws += 1
                        accumulated_g += 24
                        await ctx.send("*Item complete.*")
                        break
                    elif lives == 0:
                        await ctx.send(f"You could've built this item with ``{correctansw}``.")
                        break

                    def check(m):                #simple checker
                        return m.channel == channel and m.author == author
                    try:
                        msg = await self.bot.wait_for("message", check=check, timeout=set_time(author, 15.322))
                    except asyncio.TimeoutError:
                        lives -= 1                                #If too late
                        await channel.send(f"**{random.choice(lateansw)}**, you have ``{lives}`` lives remaining.")
                        accumulated_g -= 18
                    else:
                        if strip_str(msg.content) == "skip":       #to skip an item
                            lives -= 1
                            await ctx.send(f"You have ``{lives}`` lives remaining, this item is built with ``{correctansw}``.")
                            break
                        elif strip_str(msg.content) == "stop":     #to stop the endless quiz
                            lives = 322
                            break
                        elif type(itemanswers[0]) == list:                         #if itemanswers has lists of correct answers it checks the correct answ in
                            if strip_str(msg.content) in itemanswersmerged:            #itemanswersmerged, gives reward
                                await ctx.send(f"**{random.choice(rightansw)}**")
                                accumulated_g += 6
                                itemstopop = []                                #create a new list of items that must be removed from itemanswersmerged
                                for itemlist in itemanswers:
                                    if strip_str(msg.content) in itemlist:          #check index of correct answer to remove from all lists of itemanswers
                                        n = itemlist.index(strip_str(msg.content))
                                for index, itemlist in enumerate(itemanswers):
                                    itemstopop.append(itemanswers[index][n])
                                    itemanswers[index].pop(n)                     #pop answered item out of all lists of the itemanswers
                                for item in itemstopop:                      #loop through itemstopop and remove each item of it from itemanswersmerged
                                    itemanswersmerged.remove(item)
                            else:
                                lives -= 1
                                await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")
                        else:
                            if strip_str(msg.content) in itemanswers:               #if itemanswers is just a list of strings, remove answered item from both lists.
                                await ctx.send(f"**{random.choice(rightansw)}**")
                                accumulated_g += 7
                                itemanswers.remove(strip_str(msg.content))
                                itemanswersmerged.remove(strip_str(msg.content))
                            else:
                                lives -= 1
                                await ctx.send(f"**{random.choice(wrongansw)}** you have ``{lives}`` lives remaining.")

    @commands.command(brief = "A single DotA related question for a bit of gold.")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def quiz(self, ctx):
        server, channel, author = ctx.guild, ctx.channel, ctx.author  #the server, channel and author of the command activator
        questn = pseudorandomizer(server, questlen, "questnumbers") #Random number to give a random question
        correctansw = ""                         #Find the correct answer to be displayed incase user gets it wrong
        if type(questvalues[questn]) == str:
            correctansw = questvalues[questn]
        elif type(questvalues[questn]) == tuple:
            correctansw = questvalues[questn][0]
        else:
            correctansw = random.choice([z for z in questvalues[questn] if z[0].isupper()])
        if type(questkeys[questn]) == tuple:           #if the question comes with an image
            await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
        else:                                          #for normal string questions
            await ctx.send(f"**```{questkeys[questn]}```**")
        def check(m):
            return m.channel == channel and m.author == author      #checks if the reply came from the same person in the same channel
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=set_time(author, 22.322))
        except asyncio.TimeoutError:                                #If too late
            await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
            add_gold(author, -4)
        else:
            if type(questvalues[questn]) == str or type(questvalues[questn]) == tuple:     #If there is one correct answer
                if strip_str(msg.content) == strip_str(questvalues[questn]) or strip_str(msg.content) in [strip_str(x) for x in questvalues[questn] if type(questvalues[questn]) == tuple]:
                    g = add_gold(author, 18)
                    await channel.send(f"**{random.choice(rightansw)}** you got ``{g}`` gold.")
                else:
                    await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")

            else:                         #If there are multiple correct answers
                if strip_str(msg.content) in [strip_str(y) for y in questvalues[questn]]:
                    g = add_gold(author, 14)
                    await channel.send(f"**{random.choice(rightansw)}** you got ``{g}`` gold.")
                else:
                    await channel.send(f"**{random.choice(wrongansw)}** One of the possible answers is ``{correctansw}``")

    @commands.command(brief = "Duel another user for 600 gold.")
    @commands.cooldown(1, 80, commands.BucketType.channel)
    async def duel(self, ctx, *, opponent: discord.Member):
        server, channel, author = ctx.guild, ctx.channel, ctx.author  #the server, channel and author of the command activator
        users = open_json("users.json")
        if str(author.id) not in users.keys():
            await ctx.send("You don't any have gold yet, use some quiz commands to earn money first")
            self.duel.reset_cooldown(ctx)
        elif str(opponent.id) not in users.keys():
            await ctx.send("That user doesn't have any gold to duel.")
            self.duel.reset_cooldown(ctx)
        elif author == opponent:
            await ctx.send("Why are you trying to duel yourself?")
            self.duel.reset_cooldown(ctx)
        elif users[str(ctx.author.id)]["gold"] < 600:
            await ctx.send("You don't have enough gold to start a duel.")
            self.duel.reset_cooldown(ctx)
        elif users[str(opponent.id)]["gold"] < 600:
            await ctx.send("Your chosen opponent doesn't have enough gold to start a duel.")
            self.duel.reset_cooldown(ctx)
        else:
            await ctx.send(f"{opponent.mention} Do you wish to duel {author.display_name}? Write **Accept** in chat if you wish to duel or **Decline** if otherwise.")
            def check(m):
                return m.channel == channel and m.author == opponent      #checks if the reply came from the same person in the same channel
            try:
                msg = await self.bot.wait_for("message", check=check, timeout=25)
            except asyncio.TimeoutError:                                #If too late
                await channel.send("The opponent didn't accept the duel.")
            else:
                if strip_str(msg.content) == "accept":
                    questionsasked = 0
                    questionsanswered1 = 0
                    questionsanswered2 = 0
                    await ctx.send("The opponent has accepted the duel, ``17`` questions will be asked and the one to get the most amount of correct answers wins!")
                    time.sleep(3.25)
                    while True:
                        time.sleep(0.75)
                        if questionsasked == 17:
                            if questionsanswered1 > questionsanswered2:
                                winner = author
                                loser = opponent
                            else:
                                winner = opponent
                                loser = author
                            g_win = add_gold(winner, 400)
                            g_lose = add_gold(loser, -600)
                            await ctx.send(f"The winner is {winner.display_name}, {winner.display_name} you won ``{g_win}`` gold and {loser.display_name} lost ``{g_lose}``...")
                            break

                        questn = pseudorandomizer(server, questlen, "questnumbers") #Random number to give a random question
                        correctansw = ""                         #Find the correct answer to be displayed incase user gets it wrong
                        if type(questvalues[questn]) == str:
                            correctansw = questvalues[questn]
                        elif type(questvalues[questn]) == tuple:
                            correctansw = questvalues[questn][0]
                        else:
                            correctansw = random.choice([z for z in questvalues[questn] if z[0].isupper()])

                        if type(questkeys[questn]) == tuple:           #if the question comes with an image
                            await ctx.send(f"**```{questkeys[questn][0]}```**", file=discord.File(f"./quizimages/{questkeys[questn][1]}"))
                            questionsasked += 1
                        else:                                          #for normal string questions
                            await ctx.send(f"**```{questkeys[questn]}```**")
                            questionsasked += 1
                        def check(m):
                            return m.channel == channel and (m.author == author or m.author == opponent)      #checks if the reply came from the same person in the same channel
                        try:
                            msg = await self.bot.wait_for("message", check=check, timeout=set_time(author, 20.322))
                        except asyncio.TimeoutError:                                #If too late
                            await channel.send(f"**{random.choice(lateansw)}** The correct answer was ``{correctansw}``")
                        else:
                            if type(questvalues[questn]) == str or type(questvalues[questn]) == tuple:     #If there is one correct answer
                                if strip_str(msg.content) == strip_str(questvalues[questn]) or strip_str(msg.content) in [strip_str(x) for x in questvalues[questn] if type(questvalues[questn]) == tuple]:
                                    await channel.send(f"**{random.choice(rightansw)}**.")
                                    if msg.author == author:
                                        questionsanswered1 += 1
                                    elif msg.author == opponent:
                                        questionsanswered2 += 1
                                else:
                                    await channel.send(f"**{random.choice(wrongansw)}** The correct answer was ``{correctansw}``")
                                    if msg.author == author:
                                        questionsanswered1 -= 1
                                    elif msg.author == opponent:
                                        questionsanswered2 -= 1

                            else:                         #If there are multiple correct answers
                                if strip_str(msg.content) in [strip_str(y) for y in questvalues[questn]]:
                                    await channel.send(f"**{random.choice(rightansw)}**.")
                                    if msg.author == author:
                                        questionsanswered1 += 1
                                    elif msg.author == opponent:
                                        questionsanswered2 += 1
                                else:
                                    await channel.send(f"**{random.choice(wrongansw)}** One of the possible answers is ``{correctansw}``")
                                    if msg.author == author:
                                        questionsanswered1 -= 1
                                    elif msg.author == opponent:
                                        questionsanswered2 -= 1

                elif strip_str(msg.content) == "decline":
                    await ctx.send("The opponent has declined the offer.")


    @quiz.error
    async def quizerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            users = open_json("users.json")
            if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
                if error.retry_after < 2:            #if user has octarine and the remaining time of the cooldown is Less
                    await ctx.reinvoke()             #than the time octarine saves the user just bypasses the cooldownerror
                    return
                else:
                    await ctx.send("**Quiz** is on **cooldown** at the moment. Try again in a few seconds")
            else:
                await ctx.send("**Quiz** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

    @blitz.error
    async def blitzerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("**Blitz** is on being used in this channel at the moment, wait a bit or play on a different channel.")

    @shopquiz.error
    async def shopquizerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            users = open_json("users.json")
            if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
                if error.retry_after < 7.5:
                    await ctx.reinvoke()
                    return
                else:
                    await ctx.send("**Shopkeepers quiz** is on **cooldown** at the moment.")
            else:
                await ctx.send("**Shopkeepers quiz** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

    @endless.error
    async def endlesserror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            users = open_json("users.json")
            if 5000 in ast.literal_eval(users[str(ctx.message.author.id)]["items"]):
                if error.retry_after < 75:
                    await ctx.reinvoke()
                    return
                else:
                    await ctx.send("**Endless** is on **cooldown** at the moment.")
            else:
                await ctx.send("**Endless** is on **cooldown** at the moment. You can buy an Octarine Core in the store to decrease command cooldowns.")

    @duel.error
    async def duelerror(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("**Duel** is currently on cooldown in this channel, try another channel or wait a bit.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify who you're duelling, like this: 322 duel @user")
            self.duel.reset_cooldown(ctx)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("That user doesn't exist or isn't in this server, try duelling someone else.")
            self.duel.reset_cooldown(ctx)

    async def cog_command_error(self, ctx, error):       #Errors to be ignored
        if isinstance(error, (commands.CommandOnCooldown, commands.MissingRequiredArgument, commands.BadArgument)):
            pass
        else:
            raise error

def setup(bot):
    bot.add_cog(Quizes(bot))