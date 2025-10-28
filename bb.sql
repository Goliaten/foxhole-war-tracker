CREATE TABLE `wars` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `war_number` integer UNIQUE NOT NULL,
  `start_time` datetime,
  `end_time` datetime,
  `winner` varchar(50),
  `shard` varchar(255)
);

CREATE TABLE `hex` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(100)
);

CREATE TABLE `regions` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(100),
  `map_name` varchar(100),
  `region_code` varchar(50) UNIQUE,
  `hex_id` integer
);

CREATE TABLE `war_regions_history` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `war_id` integer,
  `region_id` integer,
  `owner` varchar(50),
  `is_victory_town` boolean
);

CREATE TABLE `structure_history` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `region_id` integer,
  `war_id` integer,
  `name` varchar(100),
  `type` varchar(50),
  `coordinates` varchar(255),
  `controlling_faction` varchar(50),
  `is_victory_town` boolean,
  `is_scorched` boolean
);

CREATE TABLE `structure_type` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `town_id` integer,
  `name` varchar(100),
  `type` varchar(50),
  `created_at` datetime,
  `updated_at` datetime
);

CREATE TABLE `hex_statistic_history` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `created_at` datetime,
  `colonial_casualties` integer,
  `warden_casualties` integer,
  `total_enlistments` integer,
  `hex_id` integer,
  `war_id` integer
);

CREATE UNIQUE INDEX `wars_index_0` ON `wars` (`war_number`);

CREATE UNIQUE INDEX `regions_index_1` ON `regions` (`region_code`);

CREATE INDEX `regions_index_2` ON `regions` (`hex_id`);

CREATE INDEX `war_regions_history_index_3` ON `war_regions_history` (`war_id`);

CREATE INDEX `war_regions_history_index_4` ON `war_regions_history` (`region_id`);

CREATE INDEX `structure_history_index_5` ON `structure_history` (`region_id`);

CREATE INDEX `structure_history_index_6` ON `structure_history` (`war_id`);

CREATE INDEX `structure_type_index_7` ON `structure_type` (`town_id`);

CREATE INDEX `hex_statistic_history_index_8` ON `hex_statistic_history` (`war_id`);

CREATE INDEX `hex_statistic_history_index_9` ON `hex_statistic_history` (`hex_id`);

ALTER TABLE `war_regions_history` ADD FOREIGN KEY (`war_id`) REFERENCES `wars` (`id`);

ALTER TABLE `war_regions_history` ADD FOREIGN KEY (`region_id`) REFERENCES `regions` (`id`);

ALTER TABLE `structure_history` ADD FOREIGN KEY (`region_id`) REFERENCES `regions` (`id`);

ALTER TABLE `structure_type` ADD FOREIGN KEY (`town_id`) REFERENCES `structure_history` (`id`);

ALTER TABLE `regions` ADD FOREIGN KEY (`hex_id`) REFERENCES `hex` (`id`);

ALTER TABLE `structure_history` ADD FOREIGN KEY (`war_id`) REFERENCES `wars` (`id`);

ALTER TABLE `hex_statistic_history` ADD FOREIGN KEY (`war_id`) REFERENCES `wars` (`id`);

ALTER TABLE `hex_statistic_history` ADD FOREIGN KEY (`hex_id`) REFERENCES `hex` (`id`);
