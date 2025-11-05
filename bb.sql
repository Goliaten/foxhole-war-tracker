DROP TABLE IF EXISTS StaticMapDataItem;
DROP TABLE IF EXISTS DynamicMapDataItem;
DROP TABLE IF EXISTS WarState;
DROP TABLE IF EXISTS MapWarReport;
DROP TABLE IF EXISTS StaticMapData;
DROP TABLE IF EXISTS DynamicMapData;
DROP TABLE IF EXISTS StructureTypes;
DROP TABLE IF EXISTS hex;
DROP TABLE IF EXISTS shard;
DROP TABLE IF EXISTS REV;

CREATE TABLE IF NOT EXISTS `REV` (
  `REV` INT UNSIGNED AUTO_INCREMENT,
  tmstmp TIMESTAMP,
  PRIMARY KEY (REV)
);

CREATE TABLE IF NOT EXISTS `hex` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `name` VARCHAR(150),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `StructureTypes` (
  `id` INT UNSIGNED,
  `REV` INT UNSIGNED,
  `name` VARCHAR(50),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `shard` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `url` VARCHAR(200),
  `name` VARCHAR(20),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `WarState` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `shard_id` INT UNSIGNED,
  `warId` VARCHAR(40),
  `warNumber` INT,
  `winner` VARCHAR(20),
  `conquestStartTime` TIMESTAMP,
  `conquestEndTime` TIMESTAMP,
  `resistanceStartTime` TIMESTAMP,
  `scheduledConquestEndTime` TIMESTAMP,
  `requiredVictoryTowns` INT,
  `shortRequiredVictoryTowns` INT,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `MapWarReport` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `hex_id` INT UNSIGNED,
  `shard_id` INT UNSIGNED,
  `totalEnlistments` INT,
  `colonialCasualties` INT,
  `wardenCasualties` INT,
  `dayOfWar` INT,
  `version` INT,
  PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS `StaticMapData` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `hex_id` INT UNSIGNED,
  `shard_id` INT UNSIGNED,
  `regionId` INT,
  `scorchedVictoryTowns` INT,
  `version` INT,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `StaticMapDataItem` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `StaticMapData_id` INT UNSIGNED,
  `text` VARCHAR(150),
  `x` decimal(10,9),
  `y` decimal(10,9),
  `mapMarkerType` VARCHAR(6),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `DynamicMapData` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `hex_id` INT UNSIGNED,
  `shard_id` INT UNSIGNED,
  `regionId` INT,
  `scorchedVictoryTowns` INT,
  `version` INT,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS `DynamicMapDataItem` (
  `id` INT UNSIGNED AUTO_INCREMENT,
  `REV` INT UNSIGNED,
  `DynamicMapData_id` INT UNSIGNED,
  `teamId` VARCHAR(20),
  `iconType` INT UNSIGNED,
  `x` DECIMAL(10,9),
  `y` DECIMAL(10,9),
  `flags` INT,
  `viewDirection` INT,
  PRIMARY KEY (id)
);


ALTER TABLE `WarState` ADD FOREIGN KEY (`shard_id`) REFERENCES `shard` (`id`);
ALTER TABLE `MapWarReport` ADD FOREIGN KEY (`shard_id`) REFERENCES `shard` (`id`);
ALTER TABLE `MapWarReport` ADD FOREIGN KEY (`hex_id`) REFERENCES `hex` (`id`);
ALTER TABLE `StaticMapData` ADD FOREIGN KEY (`shard_id`) REFERENCES `shard` (`id`);
ALTER TABLE `StaticMapData` ADD FOREIGN KEY (`hex_id`) REFERENCES `hex` (`id`);
ALTER TABLE `DynamicMapData` ADD FOREIGN KEY (`shard_id`) REFERENCES `shard` (`id`);
ALTER TABLE `DynamicMapData` ADD FOREIGN KEY (`hex_id`) REFERENCES `hex` (`id`);
ALTER TABLE `StaticMapDataItem` ADD FOREIGN KEY (`StaticMapData_id`) REFERENCES `StaticMapData` (`id`);
ALTER TABLE `DynamicMapDataItem` ADD FOREIGN KEY (`DynamicMapData_id`) REFERENCES `DynamicMapData` (`id`);
ALTER TABLE `DynamicMapDataItem` ADD FOREIGN KEY (`iconType`) REFERENCES `StructureTypes` (`id`);
ALTER TABLE `hex` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);
ALTER TABLE `WarState` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);
ALTER TABLE `MapWarReport` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);
ALTER TABLE `StaticMapData` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);
ALTER TABLE `DynamicMapData` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);
ALTER TABLE `StaticMapDataItem` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);
ALTER TABLE `DynamicMapDataItem` ADD FOREIGN KEY (`REV`) REFERENCES `REV` (`REV`);

INSERT INTO REV (tmstmp) VALUES
  (CURRENT_TIMESTAMP());

INSERT INTO StructureTypes (id, REV, name) VALUES
  (5, 1, 'Static Base 1'),
  (6, 1, 'Static Base 2'),
  (7, 1, 'Static Base 3'),
  (8, 1, 'Forward Base 1'),
  (9, 1, 'Forward Base 2'),
  (10, 1, 'Forward Base 3'),
  (11, 1, 'Hospital'),
  (12, 1, 'Vehicle Factory'),
  (13, 1, 'Armory'),
  (14, 1, 'Supply Station'),
  (15, 1, 'Workshop'),
  (16, 1, 'Manufacturing Plant'),
  (17, 1, 'Refinery'),
  (18, 1, 'Shipyard'),
  (19, 1, 'Tech Center'),
  (20, 1, 'Salvage Field'),
  (21, 1, 'Component Field'),
  (22, 1, 'Fuel Field'),
  (23, 1, 'Sulfur Field'),
  (24, 1, 'World Map Tent'),
  (25, 1, 'Travel Tent'),
  (26, 1, 'Training Area'),
  (27, 1, 'Special Base (Keep)'),
  (28, 1, 'Observation Tower'),
  (29, 1, 'Fort'),
  (30, 1, 'Troop Ship'),
  (32, 1, 'Sulfur Mine'),
  (33, 1, 'Storage Facility'),
  (34, 1, 'Factory'),
  (35, 1, 'Garrison Station'),
  (36, 1, 'Ammo Factory'),
  (37, 1, 'Rocket Site'),
  (38, 1, 'Salvage Mine'),
  (39, 1, 'Construction Yard'),
  (40, 1, 'Component Mine'),
  (41, 1, 'Oil Well'),
  (45, 1, 'Relic Base 1'),
  (46, 1, 'Relic Base 2'),
  (47, 1, 'Relic Base 3'),
  (51, 1, 'Mass Production Factory'),
  (52, 1, 'Seaport'),
  (53, 1, 'Coastal Gun'),
  (54, 1, 'Soul Factory'),
  (56, 1, 'Town Base 1'),
  (57, 1, 'Town Base 2'),
  (58, 1, 'Town Base 3'),
  (59, 1, 'Storm Cannon'),
  (60, 1, 'Intel Center'),
  (61, 1, 'Coal Field'),
  (62, 1, 'Oil Field'),
  (70, 1, 'Rocket Target'),
  (71, 1, 'Rocket Ground Zero'),
  (72, 1, 'Rocket Site With Rocket'),
  (75, 1, 'Facility Mine Oil Rig'),
  (83, 1, 'Weather Station'),
  (84, 1, 'Mortar House');

INSERT INTO shard VALUES
  (1, 1, 'https://war-service-live.foxholeservices.com/api', 'able'),
  (2, 1, 'https://war-service-live-2.foxholeservices.com/api', 'bravo'),
  (3, 1, 'https://war-service-live-3.foxholeservices.com/api', 'charlie');
