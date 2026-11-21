-- GTA 6 tables for the Gemini tools (get_character, get_region, compare_editions, get_game_facts).
-- Seeded from backend/GTA 6 Data.md. Runs on first start of the Docker MySQL volume;
-- for a local MySQL, run it against your DB_NAME database. Safe to re-run (INSERT IGNORE).

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS gta6_characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    aliases VARCHAR(255),
    playable BOOLEAN NOT NULL DEFAULT FALSE,
    role VARCHAR(255),
    background TEXT,
    relationships TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS gta6_regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    aliases VARCHAR(255),
    real_world_basis VARCHAR(100),
    location VARCHAR(255),
    description TEXT,
    landmarks TEXT,
    activities TEXT
);

CREATE TABLE IF NOT EXISTS gta6_editions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    us_price VARCHAR(20),
    eur_price VARCHAR(20),
    format VARCHAR(255),
    contents TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS gta6_facts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(30) NOT NULL,
    fact_key VARCHAR(80) NOT NULL,
    fact_value TEXT NOT NULL,
    UNIQUE KEY uq_gta6_facts (topic, fact_key)
);

INSERT IGNORE INTO gta6_characters (name, aliases, playable, role, background, relationships, notes) VALUES
('Jason Duval', 'jason,duval', TRUE, 'Playable protagonist and Lucia''s partner', 'Grew up around grifters and crooks. Joined the army to change course, but it did not work out. Back in the Leonida Keys working for local drug runners.', 'Partner of Lucia Caminos; friend of Cal Hampton; lives rent-free at one of Brian Heder''s properties in exchange for helping with his shakedowns.', 'Meeting Lucia changes his life, for better or worse.'),
('Lucia Caminos', 'lucia,caminos', TRUE, 'Playable protagonist and Jason''s partner', 'Grew up in Liberty City. Wants the good life her mother always dreamed of. Was imprisoned at Leonida Penitentiary after fighting for her family; Trailer 2 opens with her leaving prison.', 'Partner of Jason Duval.', 'A trained fighter. First playable female protagonist in the modern 3D-era GTA series.'),
('Cal Hampton', 'cal,hampton', FALSE, 'Jason''s friend and an associate of Brian Heder', 'Reclusive and paranoid, with a conspiracy-theorist streak.', 'Friend of Jason Duval; associate of Brian Heder.', 'Snoops on Coast Guard radio communications; drinks beer and browses in incognito tabs.'),
('Boobie Ike', 'boobie,ike', FALSE, 'Vice City local legend and businessman', 'One of the few who rose above the streets. Runs an empire spanning real estate, a strip club and a recording studio, funded by the drug trade.', 'Runs the record label Only Raw Records with Dre''Quan Priest.', 'The Extended Look opens with Jason and Lucia collecting a shipment linked to him.'),
('Dre''Quan Priest', 'dre''quan,drequan,dre quan,priest', FALSE, 'Music mogul running Only Raw Records with Boobie Ike', 'Once dealt on the streets but was always more hustler than gangster; music was the goal. Booked acts into Boobie''s strip club early on.', 'Business partner of Boobie Ike; has signed the rap duo Real Dimez.', 'Wants to break into the wider Vice City music scene.'),
('Real Dimez', 'real dimez,dimez,bae-luxe,bae luxe,roxy', FALSE, 'Rap duo and social media sensations', 'Members are Bae-Luxe and Roxy. Broke through with an early hit single with local rapper DWNPLY.', 'Signed to Only Raw Records (Dre''Quan Priest and Boobie Ike).', NULL),
('Raul Bautista', 'raul,bautista', FALSE, 'Seasoned bank robber', 'Takes big risks for big rewards. Reckless; often raises the stakes in ways that endanger his crew.', 'Works with Jason and Lucia; in the Extended Look he shoots at police alongside Jason while Lucia drives.', NULL),
('Brian Heder', 'brian,heder', FALSE, 'Landlord and veteran drug runner', 'A drug runner from the golden age of Keys smuggling.', 'Lets Jason live rent-free at one of his properties in exchange for help with shakedowns; married to Lori, his third wife; Cal Hampton is an associate.', NULL),
('Lori', 'lori,lori heder', FALSE, 'Brian Heder''s wife', 'Brian Heder''s third wife.', 'Married to Brian Heder.', 'Appears in the Extended Look.');

INSERT IGNORE INTO gta6_regions (name, aliases, real_world_basis, location, description, landmarks, activities) VALUES
('Vice City', 'vice city,vc', 'Miami', 'Southeast coast of Leonida, in Vice-Dale County', 'Art Deco beachfronts, neon nightlife, a glass-tower downtown, canals and a busy cruise port. Rockstar calls it the sun and fun capital of America. Returns from 2002''s GTA: Vice City in a modern setting.', 'Districts: Ocean Beach, South Beach, Washington Beach, Vice Beach, Downtown, Little Cuba, La Perle, Stockyard, Bayside, Rialto Islands. Hubs: Vice City Port, Vice City International Airport. Venues: Victory Arms, Megamundo Tower, Effluvia, Jack of Hearts, Hank''s Waffles, Hotel Dixon, Zeke''s Gadgets.', 'Nightlife, beaches, shopping, robberies'),
('Leonida Keys', 'keys,leonida keys,the keys', 'The Florida Keys', 'A chain of bridge-linked tropical islands south of Vice City', 'Where Jason and Lucia live at the start of the game.', NULL, 'Boating and island travel'),
('Grassrivers', 'grassrivers,grass rivers', 'The Everglades', 'Southwest Leonida', 'Mangroves, flooded grassland and swamp, home to alligators.', NULL, 'Airboat and fanboat travel, wildlife'),
('Port Gellhorn', 'port gellhorn,gellhorn', 'Panama City Beach, Florida', 'West coast of Leonida', 'Rockstar calls it Leonida''s forgotten coast: run-down motels, empty strip malls and dead attractions around a working port.', NULL, 'Dirt bikes and ATVs'),
('Ambrosia', 'ambrosia', 'Central Florida''s industrial heartland', 'Central Leonida, beside Lake Leonida', 'A local biker gang controls the area. Rockstar says it is where the battle for health and wealth begins.', 'Allied Crystal sugar refinery dominates the skyline', NULL),
('Mount Kalaga National Park', 'mount kalaga,kalaga,mt kalaga,mt. kalaga', NULL, 'Along Leonida''s northern border', 'Forests, canyons, rivers and backcountry trails.', NULL, 'Hunting, fishing, kayaking, dirt biking and off-roading');

INSERT IGNORE INTO gta6_editions (name, us_price, eur_price, format, contents, notes) VALUES
('Standard Edition', '$79.99', '€79.99', 'Digital, or a physical box containing a download code (no disc)', 'The base game.', 'Boxed copies available from 12 November 2026 to support pre-loading. Can be upgraded to Ultimate later.'),
('Ultimate Edition', '$99.99', '€99.99', 'Digital only', 'Base game plus: ''95 Grotti Cheetah; ''67 Vapid Dominator Buggy (Paradise Garage); Jason''s Dinka Enduro motorcycle and Crest Kayak; retro Vapid Ganado pickup; Shitzu Squalo watercraft; Classic Car Collection from Wyman; Hawk & Little Morgan Revolvers; engravings for the Girardi ES9 and Klose K17; Vice City Style outfits and tattoos; Goodtime Gear and Stock 305 clothing.', 'Ultimate-only shops: Rideout Customs, Sara''s Unisex Salon, Stock 305, Electric Fang Tattoo (50+ FAILE tattoos), One-Eyed Willie''s, and the PTT Youngin$ Compound raid location.');

INSERT IGNORE INTO gta6_facts (topic, fact_key, fact_value) VALUES
('release', 'Release date', 'Thursday, 19 November 2026'),
('release', 'Developer', 'Rockstar Games (owned by Take-Two Interactive)'),
('release', 'Rollout', 'Staggered by time zone; New Zealand first at midnight local time on 19 November (6 a.m. ET on 18 November)'),
('release', 'Pre-load', 'Digital pre-loading from local midnight on 12 November 2026'),
('platforms', 'Platforms', 'PlayStation 5 and Xbox Series X|S only'),
('platforms', 'PC version', 'Not announced at launch; no date or window'),
('platforms', 'Previous generation', 'No PS4 or Xbox One version'),
('delays', 'Original target', 'Autumn 2025'),
('delays', 'First delay', 'Announced May 2025; moved to 26 May 2026'),
('delays', 'Second delay', 'Announced 6 November 2025; moved six months to 19 November 2026 for extra polish'),
('performance', 'Frame rate', '30 fps on PS5, PS5 Pro, Xbox Series X and Series S; no performance mode'),
('performance', 'Resolution', 'About 1440p internal on PS5 and PS5 Pro (Digital Foundry)'),
('performance', 'PS5 Pro', 'Holds 30 fps almost flawlessly; PSSR brings the image close to 4K; adds ray-traced shadows'),
('performance', 'Base PS5', 'Drops below 30 fps more often than expected, down to about 23 fps in demanding scenes'),
('performance', 'Ray tracing', 'Ray-traced reflections and global illumination on all consoles'),
('reviews', 'Metacritic', '99 from 114 critic reviews at launch, none mixed or negative'),
('reviews', 'IGN', '10/10 (Luke Reilly)'),
('reviews', 'GameSpot', '10/10 (Tamoor Hussain); criticised progression requirements disrupting pacing'),
('reviews', 'Forbes', '10/10 (Paul Tassi)'),
('reviews', 'Giant Bomb', '5 stars (Dan Ryckert)'),
('sales', 'Pre-orders', 'About 16 million (Sensor Tower estimate, 17 November 2026)'),
('sales', 'Pre-launch revenue', 'About $1.54 billion (Sensor Tower estimate)'),
('sales', 'Launch-week forecast', '$3.25 billion to $5.2 billion (Newzoo estimate)'),
('sales', 'Take-Two shares', 'Up 6.16% to $216.49 on 18 November 2026'),
('online', 'At launch', 'Single-player only; no online mode'),
('online', 'Announcement', 'No new online mode named, dated or priced by launch'),
('online', 'Existing GTA Online', 'The GTA 5-based GTA Online continues separately'),
('preorder_bonus', 'Name', 'Vintage Vice City Pack, included with both editions for purchases before 20 November 2026'),
('preorder_bonus', 'Vehicle', '''55 Vapid Stanier sedan, with the Shore Court garage (weapon locker and fencing drop-off)'),
('preorder_bonus', 'Weapon pattern', 'Palm-tree pattern for most guns, inspired by Tommy Vercetti''s shirt'),
('preorder_bonus', 'Outfits', 'Jason''s pastel linen suit and Lucia''s red sequin mini dress, with matching hairstyles'),
('preorder_bonus', 'Digital extra', 'One free month of GTA+'),
('marketing', 'Trailer 1', '4 December 2023 (released a day early after a leak); ''Love Is a Long Road'' by Tom Petty'),
('marketing', 'Trailer 2', '6 May 2025; ''Hot Together'' by the Pointer Sisters; 475M+ views in 24 hours'),
('marketing', 'Extended Look', '27 August 2026 on Netflix; about 26 minutes of PS5 gameplay'),
('marketing', 'Pre-orders', 'Opened 25 June 2026, after cover art was revealed on 18 June 2026');
