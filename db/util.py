import MySQLdb as sql
import hashlib

import db



tabels = {}

tabels['Users'] = '''CREATE TABLE `Users` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` tinytext NOT NULL,
  `lastName` tinytext NOT NULL,
  `email` text NOT NULL,
  `phone` int(10) DEFAULT NULL,
  `password` text NOT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['Roles'] = '''CREATE TABLE `Roles` (
  `roleId` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` text NOT NULL,
  PRIMARY KEY (`roleId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

tabels['UserRoles'] = '''CREATE TABLE `UserRoles` (
  `roleId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`roleId`,`userId`),
  KEY `roleId` (`roleId`),
  KEY `userId` (`userId`),
  CONSTRAINT `roleId` FOREIGN KEY (`roleId`) REFERENCES `Roles` (`roleId`),
  CONSTRAINT `userId` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''



def check():
    conn = db.conn()
    cursor = conn.cursor(db.DictCursor)

    cursor.execute('select * from Users;')

    return cursor.fetchall()