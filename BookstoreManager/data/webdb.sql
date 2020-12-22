-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: webstoredb
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `book_import`
--

DROP TABLE IF EXISTS `book_import`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_import` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `total_cost` float NOT NULL,
  `employee_incharge` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_incharge` (`employee_incharge`),
  CONSTRAINT `book_import_ibfk_1` FOREIGN KEY (`employee_incharge`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_import`
--

LOCK TABLES `book_import` WRITE;
/*!40000 ALTER TABLE `book_import` DISABLE KEYS */;
INSERT INTO `book_import` VALUES (2,'2020-12-22',8627500,2);
/*!40000 ALTER TABLE `book_import` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_storage`
--

DROP TABLE IF EXISTS `book_storage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_storage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `avatar` varchar(50) DEFAULT NULL,
  `instock` int NOT NULL,
  `author` varchar(30) NOT NULL,
  `category` varchar(20) NOT NULL,
  `selling_price` int NOT NULL,
  `path` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_storage`
--

LOCK TABLES `book_storage` WRITE;
/*!40000 ALTER TABLE `book_storage` DISABLE KEYS */;
INSERT INTO `book_storage` VALUES (1,'Con Chim Xanh Biếc',NULL,309,'Nguyễn Nhật Ánh','Tiểu Thuyết',79900,'images/conchimxanh.jpg'),(2,'Đi Trốn',NULL,598,'Bình Ca','Tiểu Thuyết',89000,'images/ditron.jpg'),(3,'Your Name',NULL,446,' Shinkai Makoto','Light novel',56000,'images/yourname.jpg'),(4,'Vòm Rừng',NULL,172,' Richard Powers','Tiểu Thuyết',55000,'images/vomrung.jpg'),(5,'Bữa Cơm Ta Cùng Chờ Đợi',NULL,217,' Maiko Seo','Tiểu Thuyết',16500,'images/buacom.jpg'),(6,'Hiệu Sách Nhỏ Ở Paris',NULL,387,' Nina George','Tiểu Thuyết',20350,'images/hieusach.jpg'),(7,'Thanh Gươm Diệt Quỷ',NULL,381,'Koyoharu Gotouge','Tiểu Thuyết',17270,'images/thanhguom.jpg'),(8,'Anh Hai Rất Nhớ Em',NULL,160,'Cửu Bả Đao','Tiểu Thuyết',16500,'images/nhungnam.jpg'),(9,'Bí Mật Mùa Hè Năm Ấy',NULL,18,'Sarah Dessen','Tiểu Thuyết',142800,'images/bimat.jpg'),(10,'Chùm Nho Phẫn Nộ',NULL,8,'John Steinbeck','Tiểu Thuyết',157500,'images/chumnho.jpg'),(11,'Kiếp Nào Cũng Thấy Nhau',NULL,-5,'Brian L. Weiss','Tiểu Thuyết',55400,'images/kiepnao.jpg'),(12,'Những Giấc Mơ Ở Morisaki',NULL,19,'Yagisawa Satoshi','Tiểu Thuyết',41700,'images/sachMorisaki.jpg'),(13,'Người Đua Diều',NULL,27,'Khaled Hosseini','Tiểu Thuyết',54500,'images/nguoiduadieu.jpg'),(14,'5 Centimet Trên Giây',NULL,9,'Shinkai Makoto, Kanoh Arata','Light novel',58500,'images/5cm.jpg'),(15,'Kỷ Niệm Xanh',NULL,10,'Yoichi Ogami','Tiểu Thuyết',53000,'images/kyniemxanh.jpg'),(16,'Đẹp Và Buồn',NULL,25,'Kawabata Yasunari','Tiểu Thuyết',77100,'images/depvabuon.jpg'),(17,'Chiến Binh Cầu Vồng',NULL,14,'Andrea Hirata','Tiểu Thuyết',81600,'images/cauvong.jpg'),(18,'Trường Ca Achilles',NULL,23,'Madeline Miller','Tiểu Thuyết',101300,'images/truongca.jpg'),(19,'Bí Mật Của Naoko',NULL,29,'Higashino Keigo','Tiểu Thuyết',54000,'images/naoko.jpg'),(20,'Nắm Nhầm Một Bàn Tay',NULL,20,'Cốc Hựu Tử','Tiểu Thuyết',49500,'images/namtay.jpg'),(21,'Bố Con Cá Gai',NULL,28,'Cho Chang - In','Tiểu Thuyết',63600,'images/bocon.jpg'),(22,'Colorful',NULL,15,'Mori Eto','Light novel',47900,'images/Colorful.jpg'),(23,'Bên Kia Mây Trời',NULL,22,'Shinkai Makoto','Light novel',101900,'images/benkia.jpg'),(24,'Ở Một Góc Nhân Gian',NULL,24,'Fumiyo Kono, Maita Yohei','Light novel',38900,'images/omotgoc.jpg'),(25,'Sự Im Lặng Của Bầy Cừu',NULL,25,'Thomas Harris','Trinh Thám',95450,'images/baycuuimlang.jpg'),(26,'Khúc Ca Tú Cầu Của Ác Quỷ',NULL,14,'Yokomizo Seishi','Trinh Thám',88000,'images/khucca.jpg'),(27,'Biến Thân',NULL,11,'Keigo Higashino','Trinh Thám',76300,'images/bienthan.jpg'),(28,'Dù Được Ban Đôi Cánh',NULL,20,'Yonezawa Honobu','Tiểu Thuyết',118150,'images/doicanh.jpg'),(29,'Tớ Thích Cậu Hơn Cả Harvard',NULL,27,'Lan Rùa','Ngôn Tình',77420,'images/tothichcau.jpg'),(30,'Thời Niên Thiếu',NULL,23,'Cửu Nguyệt Hi','Ngôn Tình',93600,'images/nienthieu.jpg'),(31,'Tan Vỡ Và Trưởng Thành',NULL,25,'Yến Nhi','Truyện Ngắn',62400,'images/truongthanh.jpg'),(32,'Lòng Người Chật Hẹp',NULL,21,'Dưa Hấu Hạt Tím','Truyện Ngắn',73600,'images/longnguoi.jpg'),(33,'999 Lá Thư',NULL,17,'Miêu Công Tử','Truyện Ngắn',79200,'images/chinhminh.jpg'),(34,'Tự Thương Mình',NULL,11,'Trí','Truyện Ngắn',62400,'images/thuongminh.jpg'),(35,'Một Mảnh Trăng',NULL,20,'Ha Hyun','Truyện Ngắn',79200,'images/manhtrang.jpg'),(36,'Quên Một Người',NULL,29,'a Tòn','Truyện Ngắn',71200,'images/quennguoi.jpg');
/*!40000 ALTER TABLE `book_storage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `avatar` varchar(50) DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(40) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone` int DEFAULT NULL,
  `role` varchar(10) NOT NULL,
  `debt` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `customer_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Quốc Tấn','images/upload/s1.png','khachhang','c4ca4238a0b923820dcc509a6f75849b',1,'tqthost@gmail.com','123 Nguyễn Kiệm',706638940,'guest',0),(2,'Thanh Vũ','images/upload/s1.png','khachhang2','c4ca4238a0b923820dcc509a6f75849b',1,'alo@host.com','12 Nguyễn Trãi',123456789,'guest',20000),(3,'Quốc Vin','images/upload/s1.png','khachhang3','c4ca4238a0b923820dcc509a6f75849b',1,'alo2@gmail.com','10 Lê Lai',987654321,'guest',100000);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `debt_collection`
--

DROP TABLE IF EXISTS `debt_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `debt_collection` (
  `debt_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int NOT NULL,
  `employee_id` int NOT NULL,
  `date` date NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`debt_id`),
  KEY `customer_id` (`customer_id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `debt_collection_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `debt_collection_ibfk_2` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `debt_collection`
--

LOCK TABLES `debt_collection` WRITE;
/*!40000 ALTER TABLE `debt_collection` DISABLE KEYS */;
/*!40000 ALTER TABLE `debt_collection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `avatar` varchar(50) DEFAULT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(40) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `employee_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Nhân viên','images/admin/su.png','nhanvien','202cb962ac59075b964b07152d234b70',1,'Employee'),(2,'Quản lý','images/admin/su.png','quanly','202cb962ac59075b964b07152d234b70',1,'Admin');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `import_detail`
--

DROP TABLE IF EXISTS `import_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `import_detail` (
  `book_id` int NOT NULL,
  `import_id` int NOT NULL,
  `quantity` int NOT NULL,
  `cost` float NOT NULL,
  PRIMARY KEY (`book_id`,`import_id`),
  KEY `import_id` (`import_id`),
  CONSTRAINT `import_detail_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book_storage` (`id`),
  CONSTRAINT `import_detail_ibfk_2` FOREIGN KEY (`import_id`) REFERENCES `book_import` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `import_detail`
--

LOCK TABLES `import_detail` WRITE;
/*!40000 ALTER TABLE `import_detail` DISABLE KEYS */;
INSERT INTO `import_detail` VALUES (6,2,175,18500),(7,2,200,15700),(8,2,150,15000);
/*!40000 ALTER TABLE `import_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `invoice_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int DEFAULT NULL,
  `customer_id` int NOT NULL,
  `date` date NOT NULL,
  `total_price` float NOT NULL,
  PRIMARY KEY (`invoice_id`),
  KEY `employee_id` (`employee_id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (1,2,1,'2020-12-22',319600),(2,2,1,'2020-12-22',319600);
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice_detail`
--

DROP TABLE IF EXISTS `invoice_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice_detail` (
  `invoice_id` int NOT NULL,
  `book_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`invoice_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `invoice_detail_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`),
  CONSTRAINT `invoice_detail_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book_storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice_detail`
--

LOCK TABLES `invoice_detail` WRITE;
/*!40000 ALTER TABLE `invoice_detail` DISABLE KEYS */;
INSERT INTO `invoice_detail` VALUES (1,1,2,159800),(2,1,2,159800);
/*!40000 ALTER TABLE `invoice_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping_detail`
--

DROP TABLE IF EXISTS `shipping_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shipping_detail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `invoice_id` int NOT NULL,
  `address` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `phone` int DEFAULT NULL,
  `status` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `invoice_id` (`invoice_id`),
  CONSTRAINT `shipping_detail_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `invoice` (`invoice_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping_detail`
--

LOCK TABLES `shipping_detail` WRITE;
/*!40000 ALTER TABLE `shipping_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `shipping_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_rule`
--

DROP TABLE IF EXISTS `system_rule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_rule` (
  `rule_id` int NOT NULL AUTO_INCREMENT,
  `rule` varchar(20) NOT NULL,
  `value` int NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`rule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_rule`
--

LOCK TABLES `system_rule` WRITE;
/*!40000 ALTER TABLE `system_rule` DISABLE KEYS */;
INSERT INTO `system_rule` VALUES (1,'max_debt',20000,'Số tiền tối đa KH nợ'),(2,'min_import',150,'SL tối thiểu một lần nhập sách'),(3,'valid_import',300,'Chỉ nhập sách có số lượng tồn ít hơn giá trị này');
/*!40000 ALTER TABLE `system_rule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wish_detail`
--

DROP TABLE IF EXISTS `wish_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wish_detail` (
  `wish_id` int NOT NULL,
  `book_id` int NOT NULL,
  PRIMARY KEY (`wish_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `wish_detail_ibfk_1` FOREIGN KEY (`wish_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `wish_detail_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book_storage` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wish_detail`
--

LOCK TABLES `wish_detail` WRITE;
/*!40000 ALTER TABLE `wish_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `wish_detail` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-22 16:46:08
