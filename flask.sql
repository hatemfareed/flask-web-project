#MYSQL
db_name = flask

CREATE TABLE `config` (
  `id` int(11) NOT NULL,
  `capacity` float NOT NULL,
  `policty` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `replacement` (
  `id` int(11) NOT NULL,
  `policty` varchar(20) DEFAULT NULL,
  `description` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `statistic` (
  `id` int(11) NOT NULL,
  `miss_rate` float NOT NULL,
  `hit_rate` float NOT NULL,
  `number_of_requests` int(11) NOT NULL,
  `DATETIME` datetime NOT NULL,
  `number_of_item` int(11) NOT NULL,
  `total_size` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `todo` (
  `id` int(200) NOT NULL,
  `key_img` varchar(200) NOT NULL,
  `path` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `config`
  ADD PRIMARY KEY (`id`),
  ADD KEY `policty` (`policty`);

ALTER TABLE `replacement`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `statistic`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `todo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `key_img` (`key_img`),
  ADD KEY `id` (`id`);

ALTER TABLE `config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=273;

ALTER TABLE `statistic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6752;

ALTER TABLE `todo`
  MODIFY `id` int(200) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2875;

ALTER TABLE `config`
  ADD CONSTRAINT `config_ibfk_1` FOREIGN KEY (`policty`) REFERENCES `replacement` (`id`);




