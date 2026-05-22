-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: oryx_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `po_file`
--

DROP TABLE IF EXISTS `po_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `po_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `po_id` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `po_id` (`po_id`),
  CONSTRAINT `po_file_ibfk_1` FOREIGN KEY (`po_id`) REFERENCES `po_monitoring` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `po_file`
--

LOCK TABLES `po_file` WRITE;
/*!40000 ALTER TABLE `po_file` DISABLE KEYS */;
INSERT INTO `po_file` VALUES (4,8,'PO_8_New_Text_Document.txt'),(5,9,'PO_9_Book1.xlsx'),(6,9,'PO_9_File_for_S._JO_ok_na.docx');
/*!40000 ALTER TABLE `po_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `po_item`
--

DROP TABLE IF EXISTS `po_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `po_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `po_id` int NOT NULL,
  `pr_checked` tinyint(1) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  `qty` int DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `po_id` (`po_id`),
  CONSTRAINT `po_item_ibfk_1` FOREIGN KEY (`po_id`) REFERENCES `po_monitoring` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `po_item`
--

LOCK TABLES `po_item` WRITE;
/*!40000 ALTER TABLE `po_item` DISABLE KEYS */;
INSERT INTO `po_item` VALUES (24,8,0,'',1,'',''),(30,9,0,'',1,'',''),(36,10,0,'cpu with ms office',1,'Endorsed to Technical','sir ceddie'),(37,10,0,'vbvb',1,'Waiting for Suppliers Delivery','v bv bvb'),(39,11,0,'',1,'',''),(40,12,0,'',1,'',''),(41,13,0,'',1,'','');
/*!40000 ALTER TABLE `po_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `po_monitoring`
--

DROP TABLE IF EXISTS `po_monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `po_monitoring` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_received` varchar(100) NOT NULL,
  `po_no` varchar(100) NOT NULL,
  `dept` varchar(100) NOT NULL,
  `received_by` varchar(100) NOT NULL,
  `dr_no` varchar(100) DEFAULT NULL,
  `si_no` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `status_note` varchar(255) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `po_monitoring`
--

LOCK TABLES `po_monitoring` WRITE;
/*!40000 ALTER TABLE `po_monitoring` DISABLE KEYS */;
INSERT INTO `po_monitoring` VALUES (8,'2026-03-07','3434','eng management division','asda','2323234234234234234','2323','Pending','','julius rotoni cabasal'),(9,'2026-03-07','po-supytmi-26-10000192','eng management division','marjorie peralta','','','','','julius rotoni cabasal'),(10,'2026-03-17','po-supytmi-26-10001736','cmo','oba','1212','1212','Others','endoresed','julius rotoni cabasal'),(11,'','','','','5246','','','','julius kamaho'),(12,'2026-04-18','QWEQWE','QQWE','QEQE','QWEQE','QWEWQE','','','julius kamaho'),(13,'2026-04-28','WEQE','QQWE','QWEQE','QWEQE','WEQEQ','','','julius kamaho');
/*!40000 ALTER TABLE `po_monitoring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pr_file`
--

DROP TABLE IF EXISTS `pr_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pr_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pr_id` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pr_id` (`pr_id`),
  CONSTRAINT `pr_file_ibfk_1` FOREIGN KEY (`pr_id`) REFERENCES `pr_monitoring` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pr_file`
--

LOCK TABLES `pr_file` WRITE;
/*!40000 ALTER TABLE `pr_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `pr_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pr_item`
--

DROP TABLE IF EXISTS `pr_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pr_item` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pr_id` int NOT NULL,
  `description` varchar(500) NOT NULL,
  `qty` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pr_id` (`pr_id`),
  CONSTRAINT `pr_item_ibfk_1` FOREIGN KEY (`pr_id`) REFERENCES `pr_monitoring` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pr_item`
--

LOCK TABLES `pr_item` WRITE;
/*!40000 ALTER TABLE `pr_item` DISABLE KEYS */;
INSERT INTO `pr_item` VALUES (24,4,'HJBJ',1),(25,5,'FCGGFG',1),(26,6,'SDFSDF',1),(27,7,'SDFSF',1),(28,8,'SDFSDF',1),(29,9,'QWEQEWQE',1),(30,10,'WQEQWEW',1),(31,11,'SFDSFD',1),(32,12,'SDFSFSDF',1),(33,13,'SDFSDFSDF',1);
/*!40000 ALTER TABLE `pr_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pr_monitoring`
--

DROP TABLE IF EXISTS `pr_monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pr_monitoring` (
  `id` int NOT NULL AUTO_INCREMENT,
  `purchase_no` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `urgent_reason` varchar(500) DEFAULT NULL,
  `po_no` varchar(100) DEFAULT NULL,
  `doc_date` varchar(100) NOT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pr_monitoring`
--

LOCK TABLES `pr_monitoring` WRITE;
/*!40000 ALTER TABLE `pr_monitoring` DISABLE KEYS */;
INSERT INTO `pr_monitoring` VALUES (4,'1212','DS','','Pending','','','2026-04-28','julius kamaho'),(5,'dfgfdg','RD','','Pending','','','2026-04-28','julius kamaho'),(6,'DFSDF','RD','','Open','','','2026-04-28','julius kamaho'),(7,'SDFS','DS','','Closed','','','2026-04-25','julius kamaho'),(8,'SDFSFD','RD','SDFSF','Open','','','2026-04-30','julius kamaho'),(9,'EWQEWQ','DS','WQEWQE','Approved','','','2026-04-21','julius kamaho'),(10,'QWEWQE','RD','','Pending','','','2026-04-21','julius kamaho'),(11,'FFF','DS','SDFSDDF','Approved','','SDFSDF','2026-04-10','julius kamaho'),(12,'SDFSDF','DS','SDFSFSDFSDF','Others','SFDSDFF','','2026-04-11','julius kamaho'),(13,'SDFSDF','RD','FSDFSF','Approved','','FSDSD','2026-04-11','julius kamaho');
/*!40000 ALTER TABLE `pr_monitoring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reminder`
--

DROP TABLE IF EXISTS `reminder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reminder` (
  `id` int NOT NULL AUTO_INCREMENT,
  `note` varchar(500) NOT NULL,
  `author_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reminder`
--

LOCK TABLES `reminder` WRITE;
/*!40000 ALTER TABLE `reminder` DISABLE KEYS */;
INSERT INTO `reminder` VALUES (6,'sdads','julius rotoni cabasal'),(7,'12345\n25\n525','Alecza Bienne'),(8,'for deployment naba\\','julius rotoni cabasal');
/*!40000 ALTER TABLE `reminder` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uat_file`
--

DROP TABLE IF EXISTS `uat_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uat_file` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uat_id` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uat_id` (`uat_id`),
  CONSTRAINT `uat_file_ibfk_1` FOREIGN KEY (`uat_id`) REFERENCES `uat_monitoring` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uat_file`
--

LOCK TABLES `uat_file` WRITE;
/*!40000 ALTER TABLE `uat_file` DISABLE KEYS */;
INSERT INTO `uat_file` VALUES (2,2,'UAT_2_File_for_S._JO_ok_na.docx'),(3,5,'UAT_5_PO_9_Book1.xlsx'),(4,6,'UAT_6_converted.docx'),(5,6,'UAT_6_Torres_tech_OJT_allowance_form_fill_up.pdf'),(6,7,'UAT_7_File_for_S._JO.pdf'),(7,8,'UAT_8_File_for_S._JO.pdf'),(8,10,'UAT_10_New_Text_Document.txt');
/*!40000 ALTER TABLE `uat_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uat_monitoring`
--

DROP TABLE IF EXISTS `uat_monitoring`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uat_monitoring` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uat_no` varchar(100) NOT NULL,
  `ccr` varchar(100) NOT NULL,
  `dept` varchar(100) NOT NULL,
  `accepting_personnel` varchar(100) NOT NULL,
  `it_incharge` varchar(100) NOT NULL,
  `date_start` varchar(50) DEFAULT NULL,
  `date_end` varchar(50) DEFAULT NULL,
  `hr_per_day` varchar(50) DEFAULT NULL,
  `total_cost` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uat_monitoring`
--

LOCK TABLES `uat_monitoring` WRITE;
/*!40000 ALTER TABLE `uat_monitoring` DISABLE KEYS */;
INSERT INTO `uat_monitoring` VALUES (2,'uat-45','Q','ASAS','ASAS','ASA','2026-03-27','2026-03-04','343','2509870.00','For Billing','julius rotoni cabasal'),(5,'uat-syssup-2026-0026','uat-syssup-2026-0026','eng management division','don HUAN LACZAMANA/ JONATHAN JUAN','don arthuro makamaho/ alfamaro kalamaho editrial men','2026-03-31','2026-03-31','2.75','2648.25','Billed','julius rotoni cabasal'),(6,'uat-syssup-2026-0009','qqqqqqqqqqq rwerffwer','crew','don HUAN LACZAMANA/ JONATHAN JUAN','alfarita','2026-04-03','2026-04-08','2.75','7427.00','For Signature','julius rotoni cabasal'),(7,'uat-syssup-2026-00056','qqqqqqqqqqq rwerffwer','ASAS','don HUAN LACZAMANA','don arthuro makamaho/ alfamaro kalamaho editrial men','2026-04-08','2026-04-11','2.75','7427.00','','julius rotoni cabasal'),(8,'uat-syssup-2026-0089','qqqqqqqqqqq rwerffwer','crew','don HUAN LACZAMANA/ JONATHAN JUAN','ASA','2026-04-04','2026-04-14','2.888','99.00','','julius rotoni cabasal'),(9,'','','','','','','','','0.00','','Alecza Bienne'),(10,'vbn','vbnvb','vbn','vbn','vbnvb','2026-04-24','2026-04-28','vbnvbn','3000','For Signature','julius rotoni cabasal'),(11,'DFGG','GDFGDG','FDGDFG','DFGFDG','DFGDFG','2026-04-23','2026-04-28','DFGDG','','','julius kamaho'),(12,'DFGDFG','DGDFG','DGFDG','FGDG','GDFG','','','','','','julius kamaho'),(13,'DGDFG','','GG','GDFG','GDF','','','','','','julius kamaho');
/*!40000 ALTER TABLE `uat_monitoring` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'juls','scrypt:32768:8:1$94jk87sOmqNypuWv$630b345c045eff423a0fa7e9b7a7696bc81f52660d8fcccef44bc0fb6ed2b0ca3f8a1221e66e034568b1ae693a3dd4d3740f135f3fb0f735871d93630b85188a','julius rotoni cabasal'),(2,'kamaho','scrypt:32768:8:1$YW7oD92GuU0UEMBI$368c4bb3fca83305231aa207cc4339ba1ef8d2249086535a1e1d0c2855e16058d452d3612bf5ae893f3777f3eb4bfbe9ce7e6b29fcdc0e0087723263cfc5888d','julius kamaho'),(3,'jilie','scrypt:32768:8:1$SOGGCs61slAzyX5V$570df50a79cea66c54cff9e780fdcc99edc5b1ce329a7a1890100ed3ee63a544453b42d6dca61e7421d8df0ab83b7850a7184e3be38241dc5aed5164dc16e053','jlie'),(4,'alecza','scrypt:32768:8:1$XvyYxAMga5XjhUgm$211eccfcd01755001083372c55d03271cced2156c8a5db4684a30ad6c5116ebd74fb165acca47431b36fab504003a4d9b28f7f2cf2fa083f4e899619929af18f','Alecza Bienne');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-29  9:25:20
