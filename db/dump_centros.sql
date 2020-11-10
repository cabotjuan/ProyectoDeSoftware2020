-- MySQL dump 10.16  Distrib 10.1.47-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: grupo5
-- ------------------------------------------------------
-- Server version	10.1.47-MariaDB-1~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appointments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(60) DEFAULT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `appointment_date` date NOT NULL,
  `center_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_appointments_email` (`email`),
  KEY `center_id` (`center_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`center_id`) REFERENCES `help_centers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `center_types`
--

DROP TABLE IF EXISTS `center_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `center_types` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_center_type` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `center_types`
--

LOCK TABLES `center_types` WRITE;
/*!40000 ALTER TABLE `center_types` DISABLE KEYS */;
INSERT INTO `center_types` VALUES (1,'Merendero'),(2,'Sociedad de Fomento'),(3,'Iglesia'),(4,'Sala'),(5,'Otros');
/*!40000 ALTER TABLE `center_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `help_centers`
--

DROP TABLE IF EXISTS `help_centers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `help_centers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_center` varchar(50) NOT NULL,
  `address` varchar(60) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `opening_time` time NOT NULL,
  `close_time` time NOT NULL,
  `town` varchar(20) NOT NULL,
  `web` varchar(80) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `visit_protocol` varchar(256) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `center_type_id` int(11) DEFAULT NULL,
  `latitude` varchar(20) NOT NULL,
  `longitude` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `center_type_id` (`center_type_id`),
  KEY `status_id` (`status_id`),
  CONSTRAINT `help_centers_ibfk_1` FOREIGN KEY (`center_type_id`) REFERENCES `center_types` (`id`),
  CONSTRAINT `help_centers_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `help_centers`
--

LOCK TABLES `help_centers` WRITE;
/*!40000 ALTER TABLE `help_centers` DISABLE KEYS */;
INSERT INTO `help_centers` VALUES (3,'Merendero todos por una sonrisa','Calle 88 nro 1912, Altos de San Lorenzo','221 - 5930941','09:00:00','16:00:00','La Plata','','','',1,1,'lat11111111111','lon1111111111'),(4,'Sociedad de fomento Las Margaritas','Santa Sofia 455, Bosques','11 - 8883421','09:00:00','16:00:00','Florencio Varela','','','',2,2,'lat1114223','lon55767687');
/*!40000 ALTER TABLE `help_centers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `statuses`
--

DROP TABLE IF EXISTS `statuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `statuses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `statuses`
--

LOCK TABLES `statuses` WRITE;
/*!40000 ALTER TABLE `statuses` DISABLE KEYS */;
INSERT INTO `statuses` VALUES (1,'Aceptado'),(2,'Pendiente'),(3,'Rechazado');
/*!40000 ALTER TABLE `statuses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-10 20:54:56
