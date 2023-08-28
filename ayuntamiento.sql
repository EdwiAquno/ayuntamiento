-- MariaDB dump 10.19  Distrib 10.6.8-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ayuntamiento
-- ------------------------------------------------------
-- Server version	10.6.8-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Area`
--

DROP TABLE IF EXISTS `Area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Area` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `correo` varchar(255) DEFAULT NULL,
  `clave` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Area`
--

LOCK TABLES `Area` WRITE;
/*!40000 ALTER TABLE `Area` DISABLE KEYS */;
INSERT INTO `Area` VALUES (1,'sistemas','sdfghjklñ',NULL,NULL),(2,'rh','sdfghjk',NULL,NULL),(3,'rh','qwertyuik',NULL,NULL),(4,'oficina de partes','dfvghjkjhgfvdcfvgybjk',NULL,NULL),(5,'oficina de partes','dfvghjkjhgfvdcfvgybjk',NULL,NULL),(6,'oficina de partes','dfvghjkjhgfvdcfvgybjk',NULL,NULL),(7,'oficina de partes','dfvghjkjhgfvdcfvgybjk',NULL,NULL),(8,'oficina de partes','dfvghjkjhgfvdcfvgybjk',NULL,NULL),(9,'oficina de partes','dfvghjkjhgfvdcfvgybjk',NULL,NULL),(10,'oficina de partes','dfghjk',NULL,NULL),(11,'COORDINACION DE SERVICIOS PUBLICOS MUNICIPALES','COORDINACION DE SERVICIOS PUBLICOS MUNICIPALES','c82156978@gmail.com','sjnsjrhrirmllkbj');
/*!40000 ALTER TABLE `Area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DetalleSolicitud`
--

DROP TABLE IF EXISTS `DetalleSolicitud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `DetalleSolicitud` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `solicitud_id` int(11) DEFAULT NULL,
  `material_id` int(11) DEFAULT NULL,
  `cantidad_solicitada` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `solicitud_id` (`solicitud_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `DetalleSolicitud_ibfk_1` FOREIGN KEY (`solicitud_id`) REFERENCES `Solicitud` (`ID`),
  CONSTRAINT `DetalleSolicitud_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `Material` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DetalleSolicitud`
--

LOCK TABLES `DetalleSolicitud` WRITE;
/*!40000 ALTER TABLE `DetalleSolicitud` DISABLE KEYS */;
/*!40000 ALTER TABLE `DetalleSolicitud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Entrega`
--

DROP TABLE IF EXISTS `Entrega`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Entrega` (
  `solicitud_id` int(11) NOT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `responsable_entrega` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`solicitud_id`),
  CONSTRAINT `Entrega_ibfk_1` FOREIGN KEY (`solicitud_id`) REFERENCES `Solicitud` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Entrega`
--

LOCK TABLES `Entrega` WRITE;
/*!40000 ALTER TABLE `Entrega` DISABLE KEYS */;
/*!40000 ALTER TABLE `Entrega` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Material`
--

DROP TABLE IF EXISTS `Material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Material` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `cantidad_disponible` int(11) DEFAULT NULL,
  `lote` varchar(50) DEFAULT NULL,
  `proveedor_id` int(11) DEFAULT NULL,
  `fecha_registro` date DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `proveedor_id` (`proveedor_id`),
  CONSTRAINT `Material_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `Proveedores` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Material`
--

LOCK TABLES `Material` WRITE;
/*!40000 ALTER TABLE `Material` DISABLE KEYS */;
INSERT INTO `Material` VALUES (9,'curitas','material medico',3,'123456',1,'2023-07-23'),(10,'silla','lugar donde sentarse',0,'|1234ty',1,'2023-08-03');
/*!40000 ALTER TABLE `Material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Proveedores`
--

DROP TABLE IF EXISTS `Proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Proveedores` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `ciudad` varchar(255) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo_electronico` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Proveedores`
--

LOCK TABLES `Proveedores` WRITE;
/*!40000 ALTER TABLE `Proveedores` DISABLE KEYS */;
INSERT INTO `Proveedores` VALUES (1,'Carmen Monserrat','calle santa viva ','huamantla','2471223544','qwerty@example.com');
/*!40000 ALTER TABLE `Proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Solicitud`
--

DROP TABLE IF EXISTS `Solicitud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Solicitud` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_solicitud` date DEFAULT NULL,
  `area_solicitante` int(11) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `usuario_solicitante` int(11) DEFAULT NULL,
  `material` varchar(255) DEFAULT NULL,
  `numero_requisicion` varchar(50) DEFAULT NULL,
  `unidad_de_medida` varchar(50) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `area_solicitante` (`area_solicitante`),
  KEY `fk_usuario_solicitante` (`usuario_solicitante`),
  CONSTRAINT `Solicitud_ibfk_1` FOREIGN KEY (`area_solicitante`) REFERENCES `Area` (`ID`),
  CONSTRAINT `fk_usuario_solicitante` FOREIGN KEY (`usuario_solicitante`) REFERENCES `Usuario` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=186 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Solicitud`
--

LOCK TABLES `Solicitud` WRITE;
/*!40000 ALTER TABLE `Solicitud` DISABLE KEYS */;
INSERT INTO `Solicitud` VALUES (84,'2023-07-22',NULL,'fghjk',2,'curitas ','vbnm,','caja',4),(85,'2023-07-22',NULL,'dxfghjk',2,'toallas ','AG-DE-S-4','caja',1),(86,'2023-07-22',NULL,'ftghjkl',2,'toallas ','AG-DE-S-4','caja',2),(87,'2023-07-22',NULL,'ftghjkl',2,'toallas ','AG-DE-S-4','caja',2),(88,'2023-07-22',NULL,'sdfghjk',2,'curitas ','AG-DE-S-8','caja',3),(89,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(90,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(91,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(92,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(93,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(94,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(95,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(96,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(97,'2023-07-22',NULL,'ertyuiop',2,'toallas ','AG-DE-S-4','caja',3),(98,'2023-07-22',NULL,'yghjiop',2,'toallas ','AG-DE-S-4','caja',4),(99,'2023-07-22',NULL,'fghjkl',2,'curitas ','AG-DE-S-4','caja',3),(100,'2023-07-22',NULL,'sdfghj',2,'toallas ','AG-DE-S-4','caja',3),(101,'2023-07-22',NULL,'rtfghjklñ',2,'toallas ','AG-DE-S-4','caja',2),(102,'2023-07-22',NULL,'dfgjkl',2,'toallas ','AG-DE-S-4','caja',2),(103,'2023-07-22',NULL,'sdfghjk',2,'curitas ','AG-DE-S-4','caja',1),(104,'2023-07-22',NULL,'vbnjmkmjnhbvcx',2,'toallas ','AG-DE-S-4','caja',3),(105,'2023-07-22',NULL,'fghjk',2,'toallas ','AG-DE-S-4','caja',2),(106,'2023-07-22',NULL,'fghjkml',2,'toallas ','AG-DE-S-4','caja',1),(107,'2023-07-22',NULL,'fghjkml',2,'toallas ','AG-DE-S-4','caja',1),(108,'2023-07-22',NULL,'fghjk',2,'curitas ','AG-DE-S-4','caja',2),(109,'2023-07-22',NULL,'sdfghj',2,'curitas ','AG-DE-S-4','caja',2),(110,'2023-07-22',NULL,'fghj',2,'toallas ','AG-DE-S-4','caja',3),(111,'2023-07-22',NULL,'dfvgbh',2,'toallas ','AG-DE-S-4','caja',2),(112,'2023-07-22',NULL,'drftghbnjhg',2,'toallas ','AG-DE-S-6-i8','caja',2),(113,'2023-07-22',NULL,'dfghjkl',2,'toallas ','AG-DE-S-6-i8','caja',2),(114,'2023-07-22',NULL,'dcfgjklñ',2,'toallas ','AG-DE-S-6-i8-l','caja',3),(115,'2023-07-22',NULL,'sdxcfgvbhjmk',2,'curitas ','AG-DE-S-4','caja',1),(116,'2023-07-23',NULL,'sfdhjkl',2,'toallas ','AG-DE-S-4','caja',2),(117,'2023-07-24',NULL,'fcghj',2,'toallas ','AG-DE-S-6','caja',3),(118,'2023-07-24',NULL,'t6y7u8',2,'toallas ','AG-DE-S-6','caja',2),(119,'2023-07-24',NULL,'gtfrd',2,'toallas ','AG-DE-S-6','caja',2),(120,'2023-07-24',NULL,'dfgh',2,'toallas ','AG-DE-S-6','caja',2),(121,'2023-07-24',NULL,'sdrtyui',2,'toallas ','AG-DE-S-4','caja',2),(122,'2023-07-24',NULL,'tyguhjikl',2,'toallas ','AG-DE-S-6','caja',3),(123,'2023-07-24',NULL,'tyguhjikl',2,'toallas ','AG-DE-S-6','caja',3),(124,'2023-07-24',NULL,'tyguhjikl',2,'toallas ','AG-DE-S-6','caja',3),(125,'2023-07-24',NULL,'ubi',2,'toallas ','AG-DE-S-6','caja',1),(126,'2023-07-24',NULL,'fgh',2,'toallas ','AG-DE-S-8','caja',3),(127,'2023-07-24',NULL,'vybhjnk',2,'curitas ','gbhnj','caja',1),(128,'2023-07-26',11,'dfghj',3,'sillas','AG-DE-S-8','pieza',1),(129,'2023-07-26',11,'sdrtgyhuj',3,'sillas','AG-DE-S-6-i8','pieza',1),(130,'2023-07-26',11,'ejemplo',3,'toallas ','AG-DE-S-8','caja',2),(131,'2023-07-26',11,'ejemplo',3,'curitas ','AG-DE-S-8','caja',1),(132,'2023-07-26',11,'ejemplo',3,'sillas','AG-DE-S-8','pieza',2),(133,'2023-07-26',11,'ejemplo',3,'sillas','AG-DE-S-8','pieza',2),(134,'2023-07-26',11,'ejemplo',3,'sillas','AG-DE-S-8','pieza',2),(135,'2023-07-26',11,'ejemplo',3,'sillas','AG-DE-S-8','pieza',2),(136,'2023-07-26',11,'ejemplo',3,'lapiz','AG-DE-S-8','caja',2),(137,'2023-07-26',11,'ejemplo',3,'lapiz','AG-DE-S-8','pieza',2),(138,'2023-07-26',11,'ejemplo',3,'curitas ','AG-DE-S-8','caja',1),(139,'2023-07-26',11,'ejemplo',3,'curitas','AG-DE-S-8','pieza',2),(140,'2023-07-26',11,'ejemplo',3,'toallas ','AG-DE-S-8','caja',2),(141,'2023-07-26',11,'ejemplo',3,'curitas ','AG-DE-S-8','caja',1),(142,'2023-07-26',11,'ejemplo',3,'curitas ','AG-DE-S-8','caja',2),(143,'2023-07-26',11,'ejemplo',3,'curitas ','AG-DE-S-8','caja',1),(144,'2023-07-26',11,'ejemplo',3,'curitas','AG-DE-S-8','pieza',2),(145,'2023-07-26',11,'ejemplo',3,'toallas ','AG-DE-S-8','pieza',5),(146,'2023-07-30',11,'nuevo',3,'lapicero','as-er-12','caja',1),(147,'2023-08-09',11,'nuevo',3,'toallas ','AG-DE-S-8-uj','caja',1),(148,'2023-08-09',11,'nuevo',3,'lapiz','AG-DE-S-8-uj','caja',2),(149,'2023-08-09',11,'nuevo',3,'toallas ','AG-DE-S-6-l','caja',1),(150,'2023-08-09',11,'nuevo',3,'sillas','AG-DE-S-6-l','caja',1),(151,'2023-08-09',11,'otro',3,'toallas ','AG-DE-S-6-i8','caja',1),(152,'2023-08-09',11,'otro',3,'lapiz','AG-DE-S-6-i8','caja',1),(153,'2023-08-09',11,'otraves',3,'toallas ','AG-DE-S-6','caja',1),(154,'2023-08-09',11,'otraves',3,'lapiz','AG-DE-S-6','caja',1),(155,'2023-08-10',11,'qwertyuiop',3,'toallas ','AG-DE-S-8','caja',3),(156,'2023-08-10',11,'qwertyuiop',3,'curitas ','AG-DE-S-8','caja',3),(157,'2023-08-16',NULL,'fghjm,',2,'xcvbnm,','fdghjm,','pieza',1),(158,'2023-08-16',11,'fghmj,',3,'toallas ','cvbnm,','caja',1),(159,'2023-08-16',11,'hjbkm',3,'cvbnm,','vbnm','cm,',1),(160,'2023-08-16',11,'gvbjk.',3,'toallas ','cgh,','caja',1),(161,'2023-08-16',11,'dfghjk.',3,'toallas ','AG-DE-S-8','caja',1),(162,'2023-08-16',11,'fgvhbm,',3,'curitas ','vbnm,','caja',1),(163,'2023-08-16',11,'gfhjk,',3,'toallas ','AG-DE-S-8','caja',1),(164,'2023-08-16',11,'dfghjm',3,'toallas ','AG-DE-S-8','caja',1),(165,'2023-08-16',11,'xcgvbm,',3,'curitas ','AG-DE-S-8','caja',1),(166,'2023-08-16',11,'ghbjnk',3,'toallas ','AG-DE-S','caja',1),(167,'2023-08-16',11,'hyjk',3,'curitas','AG-DE-S-8','caja',1),(168,'2023-08-16',11,'gfhjk',3,'curitas ','AG-DE-S-8','pieza',1),(169,'2023-08-16',11,'sdfghj',3,'toallas ','AG-DE-S-8','caja',1),(170,'2023-08-16',11,'ghj,',3,'sillas','AG-DE-S-8','caja',1),(171,'2023-08-16',11,'yhgtfrd',3,'toallas ','tgvfd','caja',1),(172,'2023-08-21',NULL,'wertyu',16,'toallas ','AG-DE-S-6','caja',1),(173,'2023-08-21',NULL,'wertyu',16,'toallas ','AG-DE-S-6','caja',1),(174,'2023-08-21',11,'fghjk',3,'toallas ','AG-DE-S-8','caja',1),(175,'2023-08-21',11,'fghjk',3,'curitas ','AG-DE-S-8','caja',1),(176,'2023-08-21',11,'fghjk',3,'toallas ','AG-DE-S-8','pieza',3),(177,'2023-08-21',11,'fghjk',3,'xcvbn','AG-DE-S-8','pieza',3),(178,'2023-08-21',11,'fghjk',3,'xcvbn','AG-DE-S-8','pieza',3),(179,'2023-08-21',11,'fghjk',3,'xcvbn','AG-DE-S-8','pieza',3),(180,'2023-08-21',11,'fghjk',3,'xcvbn','AG-DE-S-8','pieza',3),(181,'2023-08-21',11,'fghjk',3,'xcvbn','AG-DE-S-8','pieza',3),(182,'2023-08-21',11,'fghjk',3,'xcvbn','AG-DE-S-8','pieza',3),(183,'2023-08-21',11,'fghjk',3,'xcvbnm,','AG-DE-S-8k','cm,',1),(184,'2023-08-21',11,'fghjk',3,'toallas ','AG-DE-S-8k','caja',1),(185,'2023-08-22',11,'fghjk',3,'toallas ','AG-DE-S-8k','ghb',1);
/*!40000 ALTER TABLE `Solicitud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Solicitud_Material`
--

DROP TABLE IF EXISTS `Solicitud_Material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Solicitud_Material` (
  `solicitud_id` int(11) DEFAULT NULL,
  `material_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  KEY `solicitud_id` (`solicitud_id`),
  KEY `material_id` (`material_id`),
  CONSTRAINT `Solicitud_Material_ibfk_1` FOREIGN KEY (`solicitud_id`) REFERENCES `Solicitud` (`ID`),
  CONSTRAINT `Solicitud_Material_ibfk_2` FOREIGN KEY (`material_id`) REFERENCES `Material` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Solicitud_Material`
--

LOCK TABLES `Solicitud_Material` WRITE;
/*!40000 ALTER TABLE `Solicitud_Material` DISABLE KEYS */;
/*!40000 ALTER TABLE `Solicitud_Material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `apellido_paterno` varchar(50) DEFAULT NULL,
  `apellido_materno` varchar(50) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `tipo` varchar(50) NOT NULL,
  `area` int(11) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_area` (`area`),
  CONSTRAINT `fk_area` FOREIGN KEY (`area`) REFERENCES `Area` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (1,'edwin','Aquino','Mendieta','pbkdf2:sha256:600000$nOWar1AMhtIXCgWP$c4ab1ccd8fa4a03411da05e0c5376513524620b0cb83da82a10c675ab0c05eec','Administrador',NULL,'edwin123',NULL),(2,'diana','cuevas','sanches','pbkdf2:sha256:600000$62zhr0BYfhyYqLDE$8f875f0248e83cdb17e58a46ad50d0dbb7ac396e68ab7fd8408cf9a269bb59f9','Area',NULL,'diana2',NULL),(3,'pablo','marmol','picapiedra','pbkdf2:sha256:600000$j7A8R1rViEv7Jwgb$28c726eb05116fb508447e3f7b9c97965b8839b4e8a26a0086215a9dbc28d2b9','Area',11,'pablo123',NULL),(4,'gabriel','aquino','mendieta','pbkdf2:sha256:600000$whHqd6sXcrmEfqkt$9c25be7c36904f92657283b91cb0a2af03d0fc30158408cb187d4cc5e11e1982','Area',NULL,'tiaquel',NULL),(15,'alguien','cuevas','briones','pbkdf2:sha256:600000$wKmbgWCrlLF8kAQt$14f9e061407243eb3f72885f534e348372c44c35d2f532a8dcb3f6e5591a00f1','Area',NULL,'edwin2435','edwin.nol2.123@gmail.com'),(16,'diana','cuevas','diana1','pbkdf2:sha256:600000$gsQ89b7JJWuqL9SN$44236fd1eb9d1ad92ab3b5c4d2a4dbc4e61986498a0f0ad8792142f9d4f7a018','Area',NULL,'diana1','vitofa1592@sparkroi.com'),(17,'alguien','marmol','qwejh567','pbkdf2:sha256:600000$2QNcQYCimMnx3NJ2$5cff85539ed55223d5915e847cf98942f40f04d4326fb06c5ac3149d20b17b12','Direccion',NULL,'qwejh567','ayuntamiento.prueva@outlook.com'),(18,'alguien','marmol','montaño','pbkdf2:sha256:600000$3MHY8SklzQBgrdYa$6af43f149a779f5c171de8699acfdacaf08e6e6226b768dce5930dd7985a51ed','Area',2,'edwin123','ritet84964@miqlab.com');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aceptadas`
--

DROP TABLE IF EXISTS `aceptadas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aceptadas` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_solicitud` date DEFAULT NULL,
  `area_solicitante` varchar(50) DEFAULT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `usuario_solicitante` varchar(50) DEFAULT NULL,
  `material` varchar(255) DEFAULT NULL,
  `numero_requisicion` varchar(50) DEFAULT NULL,
  `unidad_de_medida` varchar(50) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `numero_peticion` varchar(50) DEFAULT NULL,
  `concepto` varchar(255) DEFAULT NULL,
  `responsable_aprobacion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aceptadas`
--

LOCK TABLES `aceptadas` WRITE;
/*!40000 ALTER TABLE `aceptadas` DISABLE KEYS */;
INSERT INTO `aceptadas` VALUES (1,'2023-08-03','gfhnm','fdgchm','diana cuevas sanches','9','gfhnm,','metro',1,'vcbnm,','cvbnm, ','cvbnm,'),(2,'2023-08-03','Ayuntamiento','ejemplo','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','qwerty'),(3,'2023-08-03','Ayuntamiento','ejemplo','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','qwerty'),(4,'2023-08-03','Ayuntamiento','ejemplo','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','qwerty'),(5,'2023-08-03','Ayuntamiento','ejemplo','diana cuevas sanches','10','1234','pieza',1,'1234','ejemplo','qwerty'),(6,'2023-08-03','Ayuntamiento','ejemplo','diana cuevas sanches','10','1234','pieza',1,'1234','ejemplo','qwerty'),(7,'2023-08-08','Ayuntamiento','nuevo','diana cuevas sanches','10','1234','metro',1,'1234','ejemplo','qwerty'),(8,'2023-08-08','Ayuntamiento','nuevo','diana cuevas sanches','10','1234','metro',1,'1234','ejemplo','qwerty'),(9,'2023-08-08','Ayuntamiento','nuevo','diana cuevas sanches','10','1234','metro',1,'1234','ejemplo','qwerty'),(10,'2023-08-08','Ayuntamiento','nuevo','diana cuevas sanches','10','1234','caja',1,'1234','ejemplo','cvbnm,'),(11,'2023-08-08','Ayuntamiento','nuevo','diana cuevas sanches','10','1234','caja',1,'1234','ejemplo','cvbnm,'),(12,'2023-08-08','Ayuntamiento','prueva','diana cuevas sanches','10','1234','pieza',1,'1234','ejemplo','qwerty'),(13,'2023-08-08','jestion','prueba','uno','10','1223','pieza',2,'146465','prueba','qwertyui'),(14,'2023-08-08','jestion','prueba','uno','10','1223','pieza',2,'146465','prueba','qwertyui'),(15,'2023-08-08','prueva','dfghj','wert','10','asd','caja',1,'asd','asdf','sdfgh'),(16,'2023-08-08','Ayuntamiento','otraves','diana cuevas sanches','10','1234','litros',3,'1234','ejemplo','cvbnm,'),(17,'2023-08-08','sdf','sdfg','sdfg','10','asdfg','asdf',1,'sdf','zxc','asd'),(18,'2023-08-09','Ayuntamiento','sdfgh','diana cuevas sanches','9','gfhnm,','caja',1,'1234','ejemplo','cvbnm,'),(19,'2023-08-09','Ayuntamiento','asdf','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','cvbnm,'),(20,'2023-08-09','gfhnm','qwer','diana cuevas sanches','9','1234','caja',1,'asd','ejemplo','cvbnm,'),(21,'2023-08-09','Ayuntamiento','qwert','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','cvbnm,'),(22,'2023-08-09','wert','gfhj','sdfgh','10','sdfgh','wedrgh',1,'qwert','wert','sdf'),(23,'2023-08-09','Ayuntamiento','qwert','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','cvbnm,'),(24,'2023-08-09','cgh','sdfghj','fdg','9','fdgh','refgh',1,'1234','ejemplo','cvbnm,'),(25,'2023-08-09','cgh','sdfghj','fdg','9','fdgh','refgh',1,'1234','ejemplo','cvbnm,'),(26,'2023-08-09','Ayuntamiento','asd','sd','9','1234','metro',1,'1234','ejemplo','cvbnm,'),(27,'2023-08-09','Ayuntamiento','asdfg','dfgh','10','1234','caja',1,'1234','ejemplo','cvbnm,'),(28,'2023-08-09','wert','gfhj','fghj','10','dfghj','dfghj',1,'sdfg','dsfgh','asdfg'),(29,'2023-08-09','wert','gfhj','fghj','10','dfghj','dfghj',1,'sdfg','dsfgh','asdfg'),(30,'2023-08-09','wert','gfhj','fghj','10','dfghj','dfghj',1,'sdfg','dsfgh','asdfg'),(31,'2023-08-09','wert','gfhj','fghj','10','dfghj','dfghj',1,'sdfg','dsfgh','asdfg'),(32,'2023-08-09','Ayuntamiento','esrdty','fgh','10','1234','caja',1,'1234','ejemplo','cvbnm,'),(33,'2023-08-10','Ayuntamiento','sdfghj','diana cuevas sanches','9','gfhnm,','caja',2,'vcbnm,','ejemplo','cvbnm,'),(34,'2023-08-10','Ayuntamiento','sdfghj','diana cuevas sanches','9','gfhnm,','caja',2,'vcbnm,','ejemplo','cvbnm,'),(35,'2023-08-10','Ayuntamiento','sdfghj','diana cuevas sanches','9','gfhnm,','caja',2,'vcbnm,','ejemplo','cvbnm,'),(36,'2023-08-10','Ayuntamiento','sdfg','diana cuevas sanches','9','1234','caja',1,'1234','cvbnm, ','cvbnm,'),(37,'2023-08-13','Ayuntamiento','sadfg','dsf','9','1234','metro',1,'1234','ejemplo','qwerty'),(38,'2023-08-13','Ayuntamiento','fdghj','diana cuevas sanches','9','1234','caja',1,'1234','ejemplo','cvbnm,'),(39,'2023-08-27','Ayuntamiento','vcbnm,','diana cuevas sanches','9','1234','metro',1,'1234','ejemplo','cvbnm,');
/*!40000 ALTER TABLE `aceptadas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-27 22:05:31
