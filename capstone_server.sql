
CREATE TABLE `users` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`email`	TEXT NOT NULL,
    `partner` INTEGER NOT NULL
);




CREATE TABLE `posts` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`problemDescription`	TEXT NOT NULL,
	`problem`	TEXT NOT NULL,
    `userId` INTEGER NOT NULL,
    FOREIGN KEY(`userId`) REFERENCES `users`(`id`)
);




INSERT INTO `users` VALUES (null, 'Collin', 'collin@email.com', TRUE);
INSERT INTO `users` VALUES (null, 'josh the GOACH', 'josh@goach.com', TRUE);
INSERT INTO `users` VALUES (null, 'Ivan Lerma', 'ivan@email.com', FALSE);


INSERT INTO `posts` VALUES (null, "function returns object object", "imagine this is some code", 1);
INSERT INTO `posts` VALUES (null, "terminal wont print", "print.print", 3);