from flask import abort, jsonify
import db
import MySQLdb as sql


tabels = {}


tabels['Roles'] = '''CREATE TABLE `Roles` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` text NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Users'] = '''CREATE TABLE `Users` (
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

tabels['UserRoles'] = '''CREATE TABLE `UserRoles` (
  `roleId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`userId`),
  KEY `roleId` (`roleId`),
  KEY `userId` (`userId`),
  CONSTRAINT `Role` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `User` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Event'] = '''CREATE TABLE `Event` (
  `eventId` int(11) NOT NULL AUTO_INCREMENT,
  `eventName` varchar(256) NOT NULL DEFAULT '',
  `time` datetime DEFAULT NULL,
  `location` text,
  `description` text,
  PRIMARY KEY (`eventId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
'''

tabels['CheckIn'] = '''CREATE TABLE `CheckIn` (
  `userId` int(11) NOT NULL,
  `eventId` int(11) NOT NULL,
  `checkedIn` tinyint(1) NOT NULL,
  PRIMARY KEY (`userId`,`eventId`),
  CONSTRAINT `UserToUser` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Permissions'] = '''CREATE TABLE `Permissions` (
  `permissionId` int(11) NOT NULL AUTO_INCREMENT,
  `permissionName` varchar(99) NOT NULL DEFAULT '',
  PRIMARY KEY (`permissionId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['PermissionRoles'] = '''CREATE TABLE `PermissionRoles` (
  `roleId` int(11) NOT NULL,
  `permissionId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`permissionId`),
  CONSTRAINT `RoleToRole` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''


def setupTestDB():
    conn = db.test_conn()
    cursor = conn.cursor()

    # Drops all tabels
    drop = 'SET FOREIGN_KEY_CHECKS = 0;'
    for name, cmd in tabels.items():
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
