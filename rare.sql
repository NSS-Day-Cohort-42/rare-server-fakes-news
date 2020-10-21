CREATE TABLE `Comment` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	INTEGER NOT NULL,
	`post_id`	INTEGER NOT NULL,
	`subject`	TEXT NOT NULL,
	`content`	TEXT NOT NULL,
	`date`	DATE NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `User`(`id`),
    FOREIGN KEY(`post_id`) REFERENCES `Post`(`id`)
);

CREATE TABLE `Post` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`title`	TEXT NOT NULL,
	`content`	TEXT NOT NULL,
	`category_id`	INTEGER NOT NULL,
	`date`	DATE NOT NULL,
	`user_id`	INTEGER NOT NULL,
    `approved` BOOLEAN,
    FOREIGN KEY(`category_id`) REFERENCES `Category`(`id`),
    FOREIGN KEY(`user_id`) REFERENCES `User`(`id`)
);

CREATE TABLE `Category` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`type`	TEXT NOT NULL
);

CREATE TABLE `TagPost` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`tag_id`	INTEGER NOT NULL,
    `post_id` INTEGER NOT NULL,
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`),
    FOREIGN KEY(`post_id`) REFERENCES `Post`(`id`)
);

CREATE TABLE `Tag` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`tag`	TEXT NOT NULL
);

CREATE TABLE `Subscription` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`user_id`	INTEGER NOT NULL,
	`subscribe_id`	INTEGER NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `User`(`id`),
    FOREIGN KEY(`subscribe_id`) REFERENCES `User`(`id`)
);

CREATE TABLE `User` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`avatar`	TEXT,
	`display_name`	TEXT NOT NULL,
	`password`	TEXT NOT NULL,
    `email` TEXT NOT NULL,
    `creation` DATE NOT NULL,
    `active` BOOLEAN NOT NULL
);

CREATE TABLE `ReactionPost` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`reaction_id`	INTEGER NOT NULL,
	`post_id`	INTEGER NOT NULL,
	`user_id`	INTEGER NOT NULL,
    FOREIGN KEY(`reaction_id`) REFERENCES `Reaction`(`id`), 
    FOREIGN KEY(`post_id`) REFERENCES `Post`(`id`) ,
    FOREIGN KEY(`user_id`) REFERENCES `User`(`id`)
);

CREATE TABLE `Reaction` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`reaction`	TEXT NOT NULL,
	`reaction_description`	TEXT NOT NULL
);

INSERT INTO `Comment` VALUES (null, 1, 1, "subject test data", "content test data", 1603311647523);
INSERT INTO `Post` VALUES (null, "title test", "content test", 1, 1603311647523, 1, TRUE);
INSERT INTO `Category` VALUES (null, "type test");
INSERT INTO `TagPost` VALUES (null, 1, 1);
INSERT INTO `Tag` VALUES (null, "Tag Test Data");
INSERT INTO `Subscription` VALUES (null, 1, 1);
INSERT INTO `User` VALUES (null, "Avatar String", "display name test", "password test", "email test data", 1603311647523, TRUE);
INSERT INTO `ReactionPost` VALUES (null, 1, 1, 1);
INSERT INTO `Reaction` VALUES (null, "reaction test data", "reaction description test data");

DELETE FROM `User`
