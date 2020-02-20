from flask import abort, jsonify
import db
import MySQLdb as sql


tables = {}

tables['Roles'] = '''CREATE TABLE IF NOT EXISTS `Roles` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` text NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Users'] = '''CREATE TABLE `Users` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` tinytext,
  `lastName` tinytext,
  `email` varchar(256) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `password` text,
  PRIMARY KEY (`userId`),
  UNIQUE KEY `Unique User` (`userId`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO `Users` (`firstName`, `lastName`, `email`, `phone`, `password`)
VALUES
	('Bill','Gates','bill@polarapp.xyz',NULL,'e729b97be60ecf3071f77f25d17025cf9e07fa6195df40143fdde42a2d4713e4e86cff7dc82c108cbc1e1ae0cd96da83cff36886b56a7dbff4271c088884dda7');
'''

tables['UserRoles'] = '''CREATE TABLE IF NOT EXISTS `UserRoles` (
  `roleId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`userId`),
  KEY `roleId` (`roleId`),
  KEY `userId` (`userId`),
  CONSTRAINT `Role` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `User` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Event'] = '''CREATE TABLE IF NOT EXISTS `Event` (
  `eventId` int(11) NOT NULL AUTO_INCREMENT,
  `eventName` varchar(256) NOT NULL DEFAULT '',
  `time` datetime DEFAULT NULL,
  `location` text,
  `description` text,
  PRIMARY KEY (`eventId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
'''

tables['CheckIn'] = '''CREATE TABLE IF NOT EXISTS `CheckIn` (
  `userId` int(11) NOT NULL,
  `eventId` int(11) NOT NULL,
  `checkedIn` tinyint(1) NOT NULL,
  PRIMARY KEY (`userId`,`eventId`),
  CONSTRAINT `UserToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Permissions'] = '''CREATE TABLE IF NOT EXISTS `Permissions` (
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

tables['PermissionRoles'] = '''CREATE TABLE IF NOT EXISTS `PermissionRoles` (
  `roleId` int(11) NOT NULL,
  `permissionId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`permissionId`),
  CONSTRAINT `RoleToRole` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Links'] = '''CREATE TABLE IF NOT EXISTS `Links` (
  `linkId` int(11) NOT NULL AUTO_INCREMENT,
  `used` tinyint(1) NOT NULL DEFAULT '0',
  `link` varchar(40) NOT NULL DEFAULT '',
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`linkId`),
  KEY `LInkToUser` (`userId`),
  CONSTRAINT `LInkToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Files'] = '''CREATE TABLE `Files` (
  `fileId` int(11) NOT NULL AUTO_INCREMENT,
  `storageName` varchar(256) NOT NULL DEFAULT '',
  `displayName` varchar(256) NOT NULL DEFAULT '',
  `description` text,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`fileId`),
  KEY `FileToUser` (`userId`),
  CONSTRAINT `FileToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['FileRoles'] = '''CREATE TABLE `FileRoles` (
  `fileId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  KEY `FileRole` (`roleId`,`fileId`),
  KEY `FileToFile` (`fileId`),
  CONSTRAINT `FileToFile` FOREIGN KEY (`fileId`) REFERENCES `Files` (`fileId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Tables'] = '''CREATE TABLE `Tables` (
  `tableId` int(11) NOT NULL AUTO_INCREMENT,
  `tableName` varchar(256) NOT NULL DEFAULT '',
  `trackHistory` tinyint(1) NOT NULL,
  PRIMARY KEY (`tableId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['TableHistory'] = '''CREATE TABLE `TableHistory` (
  `changeId` int(11) NOT NULL AUTO_INCREMENT,
  `tableId` int(11) NOT NULL,
  `rowId` int(11) NOT NULL,
  `beforeVal` text NOT NULL,
  `afterVal` text NOT NULL,
  `userChangeId` int(11) NOT NULL,
  `time` datetime NOT NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`changeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''


def setupTestDB():
    conn = db.test_conn()
    cursor = conn.cursor()

    # Drops all tables
    drop = 'SET FOREIGN_KEY_CHECKS = 0;'
    for name, cmd in tables.items():
        drop = drop + 'TRUNCATE table {};'.format(name)
        #drop = drop + 'drop table if exists {};'.format(name)

    drop = drop + 'SET FOREIGN_KEY_CHECKS = 1;'

    try:
        cursor.execute(drop)
    except sql.Error as e:
        print(e)


def resetDB():
    conn = db.conn()
    cursor = conn.cursor()

    # Drops all tables
    drop = 'SET FOREIGN_KEY_CHECKS = 0;'
    for name, cmd in tables.items():
        # drop = drop + 'TRUNCATE table {};'.format(name)
        drop = drop + 'drop table if exists {};'.format(name)

    drop = drop + 'SET FOREIGN_KEY_CHECKS = 1;'

    try:
        cursor.execute(drop)
    except sql.Error as e:
        print(e)

    # Creates all tables
    create = ''

    for name, cmd in tables.items():
        create = create + cmd

    # print(create)

    try:
        cursor.execute(create)
    except sql.Error as e:
        print(e)
