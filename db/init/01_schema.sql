-- Schema and seed data for the MySQL container (copied from summa.txt).
-- MySQL runs this once, on first start with an empty volume, inside MYSQL_DATABASE (DB_NAME).
-- No CREATE DATABASE/USE here: names are case-sensitive on Linux, so 'LLM' would not match DB_NAME=llm.
-- To re-run it: docker compose down -v (deletes the DB volume), then docker compose up.

CREATE TABLE users(
id int auto_increment not null primary key unique,
name varchar(100),
email varchar(100),
password varchar(80)
);

CREATE TABLE chat(
id int,
chat_id int auto_increment unique not null,
chat_title text,
chat_history json,
UNIQUE KEY unique_chat (id, chat_id),
foreign key(id) references users(id)
);

CREATE TABLE weapon_info (
name varchar(30),
type varchar(50),
condition_rating float,
damage float,
`range` float,
accuracy float,
rate_of_fire float,
penetration float,
stopping_power float,
magazine_size float,
source varchar(20)
);

INSERT INTO weapon_info (name, type, condition_rating, damage, `range`, accuracy, rate_of_fire, penetration, stopping_power, magazine_size, source) VALUES
('SAF', 'Assault Rifle', 1, 1.7, 3.6, 8.0, 9.4, 6.5, 1.5, 25, 'Pick Up'),
('MWS', 'Assault Rifle', 3, 2.5, 2.4, 8.1, 9.6, 3.5, 1.8, 35, 'Hot Springs'),
('US556', 'Assault Rifle', 5, 2.9, 2.7, 8.7, 9.8, 3.5, 1.8, 30, 'Hot Springs'),
('Rock Chuck', 'Assault Rifle', 5, 2.6, 3.7, 8.1, 10.0, 3.5, 1.8, 35, 'Unlock'),
('IDF Pup', 'Assault Rifle', 5, 3.8, 2.7, 8.7, 9.8, 3.5, 1.8, 45, 'Unlock'),
('M7', 'Rifle', 1, 2.5, 4.1, 9.1, 1.0, 3.5, 1.8, 6, 'Pick Up'),
('.22 Repeater', 'Rifle', 2, 2.7, 4.1, 9.1, 3.2, 3.5, 1.8, 5, 'Hot Springs'),
('M14', 'Rifle', 3, 3.9, 5.0, 8.6, 3.1, 3.5, 4.4, 10, 'Iron Mike''s'),
('The Cowboy', 'Rifle', 4, 4.6, 4.8, 9.4, 3.1, 3.5, 5.6, 6, 'Wizard Island'),
('Badlands Big Game', 'Rifle', 5, 6.0, 4.7, 9.4, 2.3, 3.5, 4.4, 10, 'Wizard Island'),
('Sawed Off', 'Shotgun', 1, 4.5, 1.4, 0.5, 2.3, 3.5, 1.8, 3, 'Pick Up'),
('RSF60', 'Shotgun', 3, 5.1, 1.6, 0.5, 1.4, 3.5, 1.8, 5, 'Hot Springs'),
('Boozer''s Shotgun', 'Shotgun', 3, 5.5, 1.4, 0.5, 1.4, 3.5, 1.8, 5, 'Unlock'),
('Combat Shotgun', 'Shotgun', 4, 6.1, 1.8, 1.6, 1.4, 3.5, 3.1, 9, 'Hot Springs'),
('Crowd Breaker', 'Shotgun', 4, 6.5, 1.9, 0.5, 1.0, 3.5, 3.1, 16, 'Iron Mike''s'),
('Nock Valley', 'Shotgun', 4, 8.5, 1.9, 3.9, 1.0, 3.5, 8.2, 1, 'Wizard Island'),
('Liberator', 'Shotgun', 5, 9.0, 1.8, 2.8, 7.3, 3.5, 4.4, 6, 'Iron Mike''s'),
('Auto Shotgun', 'Shotgun', 5, 7.2, 1.9, 0.5, 7.0, 3.5, 6.3, 16, 'Unlock'),
('Stinger', 'SMG', 2, 2.0, 2.6, 7.9, 9.9, 3.5, 1.8, 30, 'Hot Springs'),
('Swat 10', 'SMG', 3, 2.4, 2.4, 7.2, 10.0, 3.5, 1.8, 30, 'Iron Mike''s'),
('M50 Reising', 'SMG', 4, 2.8, 1.7, 8.8, 9.4, 3.5, 1.8, 15, 'Iron Mike''s'),
('PPSH-41', 'SMG', 4, 3.4, 2.3, 8.3, 9.8, 3.5, 1.8, 30, 'Wizard Island'),
('Chicago Chopper', 'SMG', 4, 3.9, 2.8, 7.8, 10.0, 3.5, 1.8, 55, 'Wizard Island');

CREATE TABLE zombie_details (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY UNIQUE,
    name VARCHAR(20),
    type VARCHAR(30),
    about TEXT,
    how_to_kill TEXT
);

INSERT INTO zombie_details (name, type, about, how_to_kill) VALUES
(
    'Swarmers',
    'Freakers',
    'Swarmers are one of the most common types of Freakers. They don''t have any special combat characteristics. Like all Freakers, they will stumble about until they spot you. Once they see you they will charge towards you.',
    'These Freakers don''t have any special characteristics so feel free to sneak up on them with stealth, shoot them, or take them on directly with a melee weapon or your boot knife.'
),
(
    'Newts',
    'Freakers',
    'Newts are skittish and usually stick to out-of-reach places like rooftops. They will attack if they sense you are low on Health or if you invade on their turf.',
    'Newts won''t attack if you keep to yourself but sometimes avoiding combat is impossible. Here''s how you can take them on:\n- Toss a molotov cocktail or pipe bomb to take out a few at once, they often crowd together.\n- Newts are weak and go down easily. Don''t be afraid to get in close and stab them with your boot knife or beat them to death with a melee weapon. This works well when there are only a few Newts.\n- When facing a large group of Newts keep your distance and pick them off one by one from afar (shoot and use throwables).'
),
(
    'Bleachers',
    'Freakers',
    'Similar to Swarmers, this type of Freaker is also very common. They don''t have any special combat characteristics but their skin is completely white as a result of the virus. Like all Freakers, they will stumble about until they spot you. Once they see you they will charge towards you.',
    'These Freakers don''t have any special characteristics so feel free to sneak up on them with stealth, shoot them, or take them on directly with a melee weapon or your boot knife.'
),
(
    'Screamers',
    'Freakers',
    'Screamers are mutated female Swarmers. Their cries can attract Freakers from the surrounding area. If you''re too close, a Screamer cry will physically hurt you.',
    'Keep your distance.\nKill them quickly because their screams will attract more enemies.\nIf you can''t get a kill off, focus on getting some distance because several more Freakers will be charging towards you soon.'
),
(
    'Breakers',
    'Freakers',
    'These extremely powerful Freakers are much larger than your garden variety Swarmers and Bleachers. Breakers take a lot of hits to kill. You will encounter your first one during the mandatory story mission Playing All Night. After that, Breakers will appear in the wild, or during missions, like any other enemy.\nBreakers are solitary. You will find them alone, or sometimes in pairs. They will attack anything, including other Freakers.',
    'Lay traps.\nComb area for items before engaging with the Breaker.\nUse Molotov Cocktails to weaken the enemy.\nUse powerful weapons during combat.\nA perfect headshot with a powerful Special Weapon, such as the SSR, can kill the Breaker in one hit. Be sure to use focus shot (one of the Best Skills to Get First) when attempting this.\nUnlock the Executioner skill so you can use a stealth takedown on Breakers.'
),
(
    'Reachers',
    'Freakers',
    'Reachers can be recognized by the white main that grows down their neck and across their shoulders. They are strong and very fast. They will dart from side to side, making it hard to track them with a gun, even with Focus active. They will move in quickly for a slashing attack, then retreat, circle around, and attack again. Reachers are solitary, always traveling alone. They will attack anything and everything they encounter, including other Freakers.',
    'A Reacher can withstand a lot, so lay down a steady barrage of bullets when you see one. Be ready to dodge when it gets close. A powerful melee weapon, like the Superior Mace or the Superior Metal Axe, will stagger it, allowing you to strike multiple times. The IPCA Stun Gun is very effective against Reachers.'
),
(
    'Runners',
    'Freakers',
    'Runners are infected wolves in that are incredibly vicious and fast, and can even keep pace with Deacon while he is on his bike.',
    'While on your bike: shoot them. Remember the smaller the icon, the more accurate the shot is. The most accurate shot will show the target as a green square.\nWhile on foot: sawed-off shotgun, lil'' stubby, or any other equally powerful primary weapon or sidearm.'
),
(
    'Ragers',
    'Freakers',
    'The Ragers are infected Bears in Days Gone that are very strong and extremely dangerous to fight - and appear to be best avoided when possible.',
    'Use Molotov Cocktails because its fur is highly flammable.\nUse a shotgun or powerful Special Weapon such as the C8 Rifle to do heavier damage.'
),
(
    'Criers',
    'Freakers',
    'Criers are infected crows. They are only encountered in the Crater Lake and Highway 97 regions, and during the mission We Couldn''t Take the Risk in Iron Butte. Criers are only found a short distance from their nests. They will circle overhead, then swoop down and attack. They will skreech when they attack. When you hear the screech, roll out of the way to avoid the strike.',
    'You can shoot Criers and knock them down with melee weapons. Dead Criers will yield a Crier beak, which can be traded for trust and credits at any camp.\nBurn Crier nests, which can be found in dead trees and on telephone poles. When the nests are gone, the Criers will fly away.'
),
(
    'Marauders',
    'Marauders',
    'These people are found in enemy camps which will attack you on sight. Enemy camps can be found throughout the Farewell Wilderness. Made up of Marauders, Rippers or Anarchists, they are filled with murderers and thieves who prey on the weak.\nMarauders will shoot you from a distance but will also toss Molotov Cocktails. Expect their camps to have plenty of traps from tripwire to bear traps on the ground.',
    'Use stealth of as long as possible.\nMark enemies with your binoculars for a better sense of where everyone is.\nTake out snipers ASAP using a special weapon which are great for long distances.\nShoot them right before they toss a Molotov. This will cause the Molotov Cocktail to explode on their side taking down one or more enemies.\nHeavily armored Marauders (fully suited) are harder to kill. Try using throwables and focus on headshots. Keep your distance because they have a flamethrower.'
),
(
    'Rippers',
    'Rippers',
    'Rippers are a cult that worships Freakers. They are known for their merciless attacks, kidnappings, and their distinct look of having self-inflicted cuts all over their body.\nRippers cut themselves, shave their heads, and allow their skin to go pale in order to resemble the Freakers they worship.',
    'Gun them down and beware of the Pipe Bombs they often throw.\nBeware of close combat because the Rippers have powerful melee weapons. On the plus side, you can loot them from their bodies once you kill them.'
),
(
    'Anarchists',
    'Anarchists',
    'Anarchists operate basically the same as marauders. These people are found in enemy camps and will attack you on sight. Enemy camps can be found throughout the Oregon wilderness. You can also encounter some roaming the roads and trails on motorcycles. Anarchists can be recognized by the white symbol painted on their faces. Anarchists tend to have better firearms than marauders, so look around after clearing a camp. You might be able to pick up a new and powerful weapon.',
    'Camps may be occupied by a dozen or more enemies. Use stealth to thin out their numbers.\nMark enemies with your binoculars for a better sense of where everyone is.\nTake out snipers ASAP. Use a sniper rifle of your own, equipped with a suppressor.\nShoot them right before they toss a Molotov. This will cause the Molotov Cocktail to explode on their side taking down one or more enemies.'
),
(
    'Wolves',
    'Animals',
    'Healthy wolves are roaming around Oregon and will attack you if you get too close. Killing a wolf allows you to walk up and skin it. You can sell this wolf meat at Camps to build Trust and earn Credits which is How to Upgrade Guns, Bike, and Gear in the game.',
    'Gunfire or melee combat are acceptable because these Wolves are far left vicious than their infected counterpart aka Runners.'
),
(
    'Bears',
    'Animals',
    'This large animal will take a lot of hits to bring down. Bears will charge towards you and swipe their claws. If they catch you, they''ll bite into you until you break free.',
    'Bears are weaker than their infected counterparts, Ragers, but the process to defeat them is the same.\nUse Molotov Cocktails because its fur is highly flammable.\nUse a shotgun or powerful Special Weapon such as the C8 Rifle to do heavier damage.'
),
(
    'Cougars',
    'Animals',
    'This animal can be found roaming in the wild but will attack if you get too close. Stronger than a wolf but less powerful than a bear, its meat can be turned into a camp to earn trust and Credits which is How to Upgrade Guns, Bike, and Gear in Days Gone.\nBe sure to consult our Best Camps to Invest In page before parting with your cougar meat.',
    'Due to this enemy''s size, be sure to keep your distance by shooting or using throwables to attack.'
);
