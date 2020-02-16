from flask import abort, jsonify
import db
import MySQLdb as sql


tabels = {}

tabels['Roles'] = '''CREATE TABLE IF NOT EXISTS `Roles` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` text NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Users'] = '''CREATE TABLE IF NOT EXISTS `Users` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` tinytext NOT NULL,
  `lastName` tinytext NOT NULL,
  `email` varchar(256) NOT NULL DEFAULT '',
  `phone` int(10) DEFAULT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `Unique User` (`userId`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['UserRoles'] = '''CREATE TABLE IF NOT EXISTS `UserRoles` (
  `roleId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`userId`),
  KEY `roleId` (`roleId`),
  KEY `userId` (`userId`),
  CONSTRAINT `Role` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `User` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Event'] = '''CREATE TABLE IF NOT EXISTS `Event` (
  `eventId` int(11) NOT NULL AUTO_INCREMENT,
  `eventName` varchar(256) NOT NULL DEFAULT '',
  `time` datetime DEFAULT NULL,
  `location` text,
  `description` text,
  PRIMARY KEY (`eventId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
'''

tabels['CheckIn'] = '''CREATE TABLE IF NOT EXISTS `CheckIn` (
  `userId` int(11) NOT NULL,
  `eventId` int(11) NOT NULL,
  `checkedIn` tinyint(1) NOT NULL,
  PRIMARY KEY (`userId`,`eventId`),
  CONSTRAINT `UserToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Permissions'] = '''CREATE TABLE IF NOT EXISTS `Permissions` (
  `permissionId` int(11) NOT NULL AUTO_INCREMENT,
  `permissionName` varchar(99) NOT NULL DEFAULT '',
  PRIMARY KEY (`permissionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Permissions` (`permissionId`, `permissionName`)
VALUES
	(1,'fileView'),
	(2,'fileUpload'),
	(3,'eventCreate'),
	(4,'eventCheckIn'),
	(5,'eventDelete'),
	(6,'eventMessage'),
	(7,'message'),
	(8,'inventoryView'),
	(9,'inventoryTable'),
	(10,'inventoryEdit'),
	(11,'iam');
'''

tabels['PermissionRoles'] = '''CREATE TABLE IF NOT EXISTS `PermissionRoles` (
  `roleId` int(11) NOT NULL,
  `permissiondId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`permissiondId`),
  CONSTRAINT `RoleToRole` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Links'] = '''CREATE TABLE IF NOT EXISTS `Links` (
  `linkId` int(11) NOT NULL AUTO_INCREMENT,
  `used` tinyint(1) NOT NULL DEFAULT '0',
  `link` varchar(40) NOT NULL DEFAULT '',
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`linkId`),
  KEY `LInkToUser` (`userId`),
  CONSTRAINT `LInkToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''


def setupTestDB():
    conn = db.test_conn()
    cursor = conn.cursor()

    # Drops all tabels
    drop = 'SET FOREIGN_KEY_CHECKS = 0;'
    for name, cmd in tabels.items():
        #drop = drop + 'TRUNCATE table {};'.format(name)
        drop = drop + 'drop table if exists {};'.format(name)

    drop = drop + 'SET FOREIGN_KEY_CHECKS = 1;'

    try:
        cursor.execute(drop)
    except sql.Error as e:
        print(e)

    # Creates all tabels
    create = ''

    for name, cmd in tabels.items():
        create = create + cmd

    # print(create)

    try:
        cursor.execute(create)
    except sql.Error as e:
        print(e)
