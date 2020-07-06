# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.30)
# Database: rimornesia_mountain
# Generation Time: 2020-07-06 05:57:23 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table stories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `stories`;

CREATE TABLE `stories` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(100) DEFAULT NULL,
  `climbing_post_id` int(100) DEFAULT NULL,
  `content` text,
  `is_published` int(5) DEFAULT '0',
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table stories_content
# ------------------------------------------------------------

DROP TABLE IF EXISTS `stories_content`;

CREATE TABLE `stories_content` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `types` int(50) DEFAULT NULL,
  `text` text,
  `attachment_id` int(100) DEFAULT NULL,
  `attachment_layout` int(15) DEFAULT NULL,
  `markup` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table stories_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `stories_content_type`;

CREATE TABLE `stories_content_type` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `stories_content_type` WRITE;
/*!40000 ALTER TABLE `stories_content_type` DISABLE KEYS */;

INSERT INTO `stories_content_type` (`id`, `name`)
VALUES
	(1,'title'),
	(2,'subtitle'),
	(3,'attachment_image'),
	(4,'attachment_video'),
	(5,'paragraph'),
	(6,'attachment_link');

/*!40000 ALTER TABLE `stories_content_type` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table stories_markup_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `stories_markup_type`;

CREATE TABLE `stories_markup_type` (
  `id` int(100) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `stories_markup_type` WRITE;
/*!40000 ALTER TABLE `stories_markup_type` DISABLE KEYS */;

INSERT INTO `stories_markup_type` (`id`, `name`)
VALUES
	(1,'bold'),
	(2,'italic');

/*!40000 ALTER TABLE `stories_markup_type` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
