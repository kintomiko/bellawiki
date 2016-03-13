BEGIN;
CREATE TABLE `bellawiki_tag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `type` integer NOT NULL,
    `name` varchar(255) NOT NULL
)
;
CREATE TABLE `bellawiki_file_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `file_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`file_id`, `tag_id`)
)
;
CREATE TABLE `bellawiki_work_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `work_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`work_id`, `tag_id`)
)
;
ALTER TABLE `bellawiki_work_files` ADD CONSTRAINT `work_id_refs_id_2c7d457e` FOREIGN KEY (`work_id`) REFERENCES `bellawiki_work` (`id`);
ALTER TABLE `bellawiki_work_tags` ADD CONSTRAINT `work_id_refs_id_0677822e` FOREIGN KEY (`work_id`) REFERENCES `bellawiki_work` (`id`);

COMMIT;