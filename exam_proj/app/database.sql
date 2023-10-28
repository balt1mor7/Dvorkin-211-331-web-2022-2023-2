-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_1861_exam_proj
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('7baa03583ee2');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_collection`
--

DROP TABLE IF EXISTS `book_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_collection` (
  `book.id` int(11) DEFAULT NULL,
  `collection.id` int(11) DEFAULT NULL,
  KEY `fk_book_collection_book.id_books` (`book.id`),
  KEY `fk_book_collection_collection.id_collections` (`collection.id`),
  CONSTRAINT `fk_book_collection_book.id_books` FOREIGN KEY (`book.id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_collection_collection.id_collections` FOREIGN KEY (`collection.id`) REFERENCES `collections` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_collection`
--

LOCK TABLES `book_collection` WRITE;
/*!40000 ALTER TABLE `book_collection` DISABLE KEYS */;
INSERT INTO `book_collection` VALUES (9,3);
/*!40000 ALTER TABLE `book_collection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `book.id` int(11) DEFAULT NULL,
  `genre.id` int(11) DEFAULT NULL,
  KEY `fk_book_genre_book.id_books` (`book.id`),
  KEY `fk_book_genre_genre.id_genres` (`genre.id`),
  CONSTRAINT `fk_book_genre_book.id_books` FOREIGN KEY (`book.id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_book_genre_genre.id_genres` FOREIGN KEY (`genre.id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (1,1),(2,2),(2,3),(3,5),(3,4),(7,2),(7,7),(9,2),(9,3),(17,2),(17,4),(17,3),(18,2),(19,2),(21,1),(21,3),(22,1),(22,5),(22,4);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `short_desc` text NOT NULL,
  `created_at` varchar(4) NOT NULL,
  `publishing_house` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `volume` int(11) NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rating_num` int(11) NOT NULL,
  `background_image_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_books_background_image_id_images` (`background_image_id`),
  CONSTRAINT `fk_books_background_image_id_images` FOREIGN KEY (`background_image_id`) REFERENCES `images` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'1984. Скотный двор','\"1984\".\r\nСвоеобразный антипод второй великой антиутопии XX века - \"О дивный новый мир\" Олдоса Хаксли. Что, в сущности, страшнее: доведенное до абсурда \"общество потребления\" - или доведенное до абсолюта \"общество идеи\"? По Оруэллу, нет и не может быть ничего ужаснее тотальной несвободы...\r\n\"Скотный двор\".\r\nПритча, полная юмора и сарказма. Может ли скромная ферма стать символом тоталитарного общества? Конечно, да. Но... каким увидят это общество его \"граждане\" - животные, обреченные на бойню?','2017','АСТ','Оруэлл Джордж',384,0,0,'2fff0808-94a5-4d68-9bb3-88882f5e5ba9'),(2,'Королевство','В норвежском городке, затерянном в горах, течет сонная, мирная жизнь. И она вполне устраивает Роя, который тут родился и вырос, но на его пороге появляется возмутитель спокойствия - младший брат Карл, успешный, предприимчивый, дерзкий. Он приехал со своей новой женой, довольно странной особой, - и с грандиозными планами строительства отеля в целях возрождения города. Но, во-первых, на поверку планы Карла оказались далеко не так благородны, во-вторых, Рой понимает, что его неудержимо тянет к жене брата, в-третьих, темные тайны прошлого, казалось похороненные навсегда, начинают всплывать на поверхность... Тихий мирок Роя рушится, и скоро ему придется выбирать между своей верностью семье и будущим, в которое он никогда не смел поверить.','2021','Азбука','Ю Несбё',576,0,0,'561aa283-773b-4ac4-a10e-f01eb6e07e0f'),(3,'Евгений Онегин (Борис Годунов. Маленькие трагедии)','\"Евгений Онегин\" (1823-1831) – одно из самых значительных произведений русской литературы.\r\nПронзительная любовная история, драматические повороты сюжета, тонкий психологизм персонажей, детальное описание быта и нравов той эпохи (не случайно Белинский назвал роман \"энциклопедией русской жизни\") – в этом произведении, как в зеркале, отразилась вся русская жизнь. \"Евгений Онегин\" никогда не утратит своей актуальности, и даже спустя два века мы поражаемся точности и верности \"ума холодных наблюдений и сердца горестных замет\" великого русского поэта.\r\nВ сборник включены также драма \"Борис Годунов\" и цикл коротких пьес \"Маленькие трагедии\".','2021','АСТ','Александр Пушкин',352,0,0,'b2bf729e-32d7-49ef-aa60-4b625bdc9a12'),(7,'Человек-Паук. История жизни. Золотая коллекция Marvel','Человек-Паук творит историю!\r\nВ 1962 году в \"Удивительном фэнтези\" #15 пятнадцатилетний Питер Паркер был укушен радиоактивным пауком и стал удивительным Человеком-Пауком! Пятьдесят семь лет прошло в нашем мире с того момента… Так что бы стало с Питером, если бы для него прошло столько же? В честь 80-летней годовщины Marvel Чип Здарски и легенда паучьих комиксов Марк Багли объединились, чтобы сплести уникальную историю про Паучка - пересказать всю его жизнь от начала и до конца, поставив его перед значимыми событиями десятилетий, которые мы пережили! От войны во Вьетнаме, Секретных войн и Гражданской войны до миссии, которая может стать последней для 72-летнего Человека-Паука. Приготовьтесь увидеть историю жизни Питера Паркера, растянувшуюся на 57 лет поразительных сюжетов… и узнайте, что случится с ним и его родными!\r\nНевероятная история от мастеров жанра: Чипа Здарски (\"Говард Утка\", \"Секс-преступники\", \"Джагхед\") и невероятного Марка Багли (\"Современный Человек-Паук\"). Альтернативная ветка развития событий, в которой нет места вечно юным героям, время - ещё один беспощадный враг, с которым придётся столкнуться Паучку и его товарищам. Авторы мастерскими играют чувствами читателя, заставляя его то смеяться, то плакать, то задумываться о своей жизни, судьбах мира и о том, в чьих руках они находятся.','2020','Комильфо','Здарски Чип',208,0,0,'b49997ea-2d77-4f87-9c3d-39a5120253fc'),(9,'Мир смерти. Планета проклятых','Люди давным-давно покорили космос, вот только непохоже, чтобы сам космос считал себя покоренным. Он вновь и вновь предстает перед человеком грозным и непостижимым Сфинксом, вновь и вновь загадывает головоломные загадки и жестоко карает за неверный ответ.\r\nТри планеты, на которых довелось побывать искателю приключений Язону динАльту, это три загадки космоса, три смертельные логические ловушки. На Пирре всё ополчилось против людей - животные, растения, стихии, и гибель героической колонии - лишь вопрос времени. На планете дикарей можно стать или рабовладельцем, или рабом, третьего не дано. А кочевники планеты Счастье не ведают иной цели существования, кроме бесконечной войны.\r\nРоман \"Планета проклятых\" дополняет сборник. На сей раз автор посылает своих героев на планету Дит, прозванную планетой проклятых и угрожающую жизни самой Вселенной.','2022','Азбука','Гарри Гаррисон',640,0,0,'6a7dc0fd-7b87-4dcd-bbb3-12b7173c1968'),(17,'Девушка с татуировкой дракона','<p>Сорок лет загадка исчезновения юной родственницы не дает покоя стареющему промышленному магнату, и вот он предпринимает последнюю в своей жизни попытку - поручает розыск журналисту Микаэлю Блумквисту. Тот берется за безнадежное дело больше для того, чтобы отвлечься от собственных неприятностей, но вскоре понимает: проблема даже сложнее, чем кажется на первый взгляд...</p>\n<p><em>Девушка с татуировкой дракона</em> - начало культовой трилогии \"Миллениум\", проданной тиражом более 100 миллионов экземпляров. Абсолютный мировой бестселлер. Дважды экранизирован. Награды и премии, которых была удостоена книга, не поддаются подсчету. Этот роман навсегда изменил законы остросюжетной литературы.</p>\n<p><em>Уникально и завораживающе. Удовольствие как от глотка свежего воздуха. - Chicago Tribune</em></p>\n<p><em>Вы даже не подозреваете, на что способна остросюжетная литература, пока не прочитали этот затягивающий роман. - Glamour</em></p>','2015','Эксмо-Пресс','Стиг Ларссон',576,0,0,'71ba18d1-61b5-4047-b6ae-f443de35be38'),(18,'Когда меркнет свет','<p>Успешный автор детективов Мэг Броган отправляется в родной город, чтобы написать книгу о нераскрытом убийстве сестры, которое произошло два десятка лет назад. Мэг тогда нашли без сознания неподалеку от места преступления. Очнувшись, она так и не вспомнила, что с ней случилось. Ныне она пытается хотя бы частично восстановить события, но цель ее приезда не встречает понимания в городе. <strong>*Кто-то расписывает ее дом кровью и стреляет по окнам…</strong></p>','2020','Эксмо-Пресс','Лорет Уайт',480,0,0,'e1779529-194d-4008-a59e-b2aa024e7b1d'),(19,'Самые темные дороги','<p>Ребекка Норд не первый год занимается расследованием убийств, и мало что может выбить ее из колеи. <strong>Но последнее дело…</strong> Ее собственный отец погиб при очень странных обстоятельствах. Все это выглядит как самоубийство, но на деле оказывается жуткой, изощренной инсценировкой. Чтобы собрать улики, Ребекка отправляется в глухой городок за тысячи километров от столицы. Там ее ждут снежные пещеры, неожиданная встреча с давним возлюбленным и связанные с ним кровавые, запутанные детали их общего прошлого.</p>','2021','Эксмо-Пресс','Лорет Уайт',480,0,0,'afbf2f5f-83cd-447a-9504-8a9152fcd55d'),(21,'Дети Времени всемогущего','<p>Девять текстов по трем мирам: от архаично-мифологических \"эллинских\" времен до поздней римской античности; условная \"Европа\" XVI и XVIII вв., \"Африка\" второй половины XV в., газовые фонари, карабины, телеграф, мистика, сражения и доблесть.\n&gt; От автора цикла фэнтези-романов \"Отблески Этерны\", который называют \"лучшим образчиком исторического фэнтези на всем постсоветском пространстве\"</p>','2023','Эксмо','Вера Камша',752,0,0,'6d2431d8-21e5-4847-b5ad-150f60f2114f'),(22,'Тропою Пушкина','<p>«Пушкин против Пушкина», «Дивный казус», «Третий Пушкин?», «Загадка Х главы»... Названия глав новой книги Г. Павленко звучат как заголовки детективных романов. Может ли так случиться, что литературоведы и пушкинисты за почти 200 лет изысканий нашли не все ответы на вопросы о жизни и творчестве А.С. Пушкина? Казалось бы, биографии поэта, его друзей и родственников изучены учёными вдоль и поперёк и белых пятен уже не осталось. Или всё-таки остались? Почему Пушкин был так привязан к С.А. Соболевскому? Какие отношения связывали Александра Сергеевича и А.О. Смирнову-Россет? Кто из друзей мог бы остановить поэта в день роковой дуэли?\nВ данной книге автор тонко переплетает факты и гипотезыв историях жизни людей из ближнего круга А.С. Пушкина. Здесь читатели встретят дядю поэта В.Л. Пушкина, поэта-министра И.И. Дмитриева, государственных деятелей графа П.Д. Киселёва и князя Д.В. Голицына, писателей В.Ф. Одоевского и В.А. Соллогуба и других современников Пушкина.</p>','2023','Наше Завтра','Георгий Павленко',288,0,0,'397e1fde-e450-491f-a48b-9815d680ff5b');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` text,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_collections_name` (`name`),
  KEY `fk_collections_user_id_users` (`user_id`),
  CONSTRAINT `fk_collections_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES (3,'Подборка №1','',5),(4,'Подборка №2','Подборка №2',5),(5,'ПодборОчка 3','',5),(6,'ПоДбОрКа 4','',5),(7,'пОДБОРКА 5 ','Для демонстрации пагинации\r\n',5);
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (6,'Биография'),(2,'Детектив'),(1,'Классическая и современная проза'),(7,'Комиксы'),(5,'Поэзия'),(4,'Романтика'),(3,'Фэнтези');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_images_md5_hash` (`md5_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES ('2fff0808-94a5-4d68-9bb3-88882f5e5ba9','1984.png','image/png','de2193f062bd0803c76ee4ae624e98d5','2023-06-15 20:21:37'),('397e1fde-e450-491f-a48b-9815d680ff5b','pushkin.jpg','image/jpeg','0726975b414f72fe77aea046f508b44d','2023-06-19 14:40:57'),('561aa283-773b-4ac4-a10e-f01eb6e07e0f','detective.png','image/png','90ea5416396c4cec9e7c3201a3883c76','2023-06-15 21:07:31'),('6a7dc0fd-7b87-4dcd-bbb3-12b7173c1968','Worldofdeath.jpg','image/jpeg','a91f082fdf70c4e4148bece456c76746','2023-06-16 18:42:52'),('6d2431d8-21e5-4847-b5ad-150f60f2114f','b2aebe6e-ca62-4721-a9f8-60c2d4c5c3ee.jpg','image/jpeg','8162e11c5fb9abe6efb30200bfece647','2023-06-19 14:39:54'),('71ba18d1-61b5-4047-b6ae-f443de35be38','girl_with_tatu.jpg','image/jpeg','8a1059b594fe81317e7f65fbab643087','2023-06-17 18:35:03'),('afbf2f5f-83cd-447a-9504-8a9152fcd55d','dark_ways.jpg','image/jpeg','f8b5d060892f13dbd5be18c2e6b6693b','2023-06-17 18:40:53'),('b2bf729e-32d7-49ef-aa60-4b625bdc9a12','poet.jpg','image/jpeg','4b0b36b45150c22a19535c698376a7a9','2023-06-15 21:11:28'),('b49997ea-2d77-4f87-9c3d-39a5120253fc','spiderman.jpg','image/jpeg','0c52432b9456c24449d1f5339570183a','2023-06-16 18:09:25'),('e1779529-194d-4008-a59e-b2aa024e7b1d','when_ligth.jpg','image/jpeg','a40052aa0fc327360c99f3d86395dcc6','2023-06-17 18:38:40');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book_id_books` (`book_id`),
  KEY `fk_reviews_user_id_users` (`user_id`),
  CONSTRAINT `fk_reviews_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`),
  CONSTRAINT `fk_reviews_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Модератор','может редактировать данные книг и производить модерацию рецензий'),(3,'Пользователь','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'user','pbkdf2:sha256:260000$jdY7F8IT5ZNssYLp$90bcadc82d5751498573b4f93d109476e99b13cf58e37d4358f7741198c5f32c','Иванов','Иван',NULL,'2023-06-15 16:08:33',1),(3,'user1','pbkdf2:sha256:260000$8OYIKagHRXEkEt3Z$fe42bc86b342a6a3642f35e385152246d20c0f115cf4c02c1966cd04c073b7b4','Петренко','Екатерина',NULL,'2023-06-15 16:08:44',2),(4,'user2','pbkdf2:sha256:260000$H5v17ssLpatJWwZP$5a8b5d1759dc40193c99c3dac9b58744084a587b9d34bc2cae15da83c3bd5d82','Алексеев','Павел','Павлович','2023-06-15 16:08:52',3),(5,'user3','pbkdf2:sha256:260000$3vJXQamHzfxPWgp0$ab0b3376c5e087a8973e2d0e3d6e2d9e2fc9551d4645d80bab4a19a82fa5d02b','Медведев','Андрей',NULL,'2023-06-15 16:09:02',3),(6,'user4','pbkdf2:sha256:260000$Y2XMfJOI0pwQxMme$2ed2cce27619585afc4a5801624ffc66c05a6c392245abaed3728deab1c8b3ff','Шабалина','Светлана','Алексеевна','2023-06-15 16:09:08',3),(7,'user5','pbkdf2:sha256:260000$MCWgDoYnv0KWbpYH$11098a5f0ccfa8a68a77cffd4679d4cbbe9c9cfe4f12f5678fcda8d4210bdb36','Меладзе','Валерий','Алексеевич','2023-06-15 16:09:16',3),(8,'user6','pbkdf2:sha256:260000$5Ldgc29CGwj10TDw$4813fc844175ede95464d11985ee506b078dd9844604eafb43858f13b557f9cc','Билан','Дмитрий',NULL,'2023-06-15 16:09:24',3),(9,'user7','pbkdf2:sha256:260000$Nqa1VtadEXQNzxx8$27aed21f9bf1357bcf68c5affc097d8721d86f1d85b9ba9dc4e73c0a4461a448','Бабкина','Надежда',NULL,'2023-06-15 16:09:30',3),(10,'user8','pbkdf2:sha256:260000$EoJvvVOia0yZpQjr$1fc9a3415ec6e93bf657168b58f05567c3c31008039a1b28f6299d09d66073cf','Пугачёва','Алла',NULL,'2023-06-15 16:09:37',3),(11,'user9','pbkdf2:sha256:260000$tHIh7dXZyqUdSPXO$ad8cf01bc68f57ab856832ed149be4bd091e590d78590da8dee2731705ec653a','Киркоров','Филлип',NULL,'2023-06-15 16:09:45',3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-19 15:04:51