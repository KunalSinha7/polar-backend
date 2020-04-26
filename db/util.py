from flask import abort, jsonify
import db
import MySQLdb as sql

from time import sleep


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
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  `location` text,
  `description` text,
  `reminder` int(11) DEFAULT '0',
  `reminderTime` int(11) DEFAULT NULL,
  `closed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`eventId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
'''

tables['CheckIn'] = '''CREATE TABLE IF NOT EXISTS `CheckIn` (
  `userId` int(11) NOT NULL,
  `eventId` int(11) NOT NULL,
  `checkedIn` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`userId`,`eventId`),
  CONSTRAINT `UserToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tables['Permissions'] = '''CREATE TABLE IF NOT EXISTS `Permissions` (
  `permissionId` int(11) NOT NULL AUTO_INCREMENT,
  `permissionName` varchar(99) NOT NULL DEFAULT '',
  PRIMARY KEY (`permissionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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

add_data = {}

add_data['admin'] =''' INSERT INTO Users (firstName, lastName, email, password)
  VALUES ('admin', 'user', 'admin@polarapp.xyz',
          '4c0a0c2f206cd7744eef9aa2a8c4a11d9d25e683e3cca1f2030d78228f5b7f894e55456f93c639f084a6c54d1a7fc02e40a7737f598ec69c251c08b6c9d5333d');
'''

add_data['role'] = '''INSERT INTO Roles (roleName) values ('admin');'''
add_data['userrole'] = '''insert into UserRoles values (1,1);'''

add_data['permsStatic'] = '''
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

add_data['perms'] = '''
  INSERT INTO PermissionRoles VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (1, 8),
    (1, 9),
    (1, 10),
    (1, 11);'''





def setupTestDB():
    conn = db.test_conn()
    cursor = conn.cursor()

    cursor.execute('select MAX(tableId) from Tables;')
    max = cursor.fetchone()

    # Drops all tables
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    for name, cmd in tables.items():
        cursor.execute('TRUNCATE table {};'.format(name))

    if max[0] is not None:
      for i in range(0, max[0] + 1):
        cursor.execute('DROP TABLE if exists table_' + str(i) + ';')

    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    for name, cmd in add_data.items():
        cursor.execute(cmd)

    conn.commit()

    return 

    
def resetDB():
    conn = db.conn()
    cursor = conn.cursor()

    # Drops all tables
    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    for name, cmd in tables.items():
        cursor.execute('TRUNCATE table {};'.format(name))

    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    for name, cmd in add_data.items():
        cursor.execute(cmd)

    conn.commit()
