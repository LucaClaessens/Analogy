SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `Analogy`
--

CREATE DATABASE `Analogy`;

-- --------------------------------------------------------

--
-- Use: `Analogy`
--

USE `Analogy`;

-- --------------------------------------------------------


--
-- Tabelstructuur voor tabel `selected_text`
--

CREATE TABLE `selected_text` (
  `selected_id` int(255) NOT NULL,
  `selected_length` int(255) NOT NULL,
  `selected_data` varchar(500) NOT NULL,
  `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `score` int(255) NOT NULL DEFAULT '1',
  `active` tinyint(1) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `source_material`
--

CREATE TABLE `source_material` (
  `sentence_id` int(11) NOT NULL,
  `sentence_data` varchar(600) COLLATE utf8_bin DEFAULT NULL,
  `score` float NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `images`
--

CREATE TABLE `images` (
  `image_id` int(255) NOT NULL,
  `image_url` varchar(255) COLLATE utf8_bin NOT NULL,
  `image_key` varchar(255) COLLATE utf8_bin NOT NULL,
  `key_score` int(255) NOT NULL DEFAULT '1',
  `active` tinyint(1) DEFAULT NULL,
  `inserted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `prints`
--

CREATE TABLE `prints` ( 
  `premium` BOOLEAN NOT NULL , 
  `printed_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
) ENGINE = InnoDB;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `selected_text`
--
ALTER TABLE `selected_text`
  ADD PRIMARY KEY (`selected_id`),
  ADD UNIQUE KEY `selected_data` (`selected_data`),
  ADD FULLTEXT KEY `selected_data` (`selected_data`);

--
-- Indexen voor tabel `source_material`
--
ALTER TABLE `source_material`
  ADD PRIMARY KEY (`sentence_id`),
  ADD FULLTEXT KEY `sentence_data` (`sentence_data`);

--
-- Indexen voor tabel `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_id`),
  ADD UNIQUE KEY `image_url` (`image_url`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `selected_text`
--
ALTER TABLE `selected_text`
  MODIFY `selected_id` int(255) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT voor een tabel `source_material`
--
ALTER TABLE `source_material`
  MODIFY `sentence_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT voor een tabel `images`
--
ALTER TABLE `images`
  MODIFY `image_id` int(255) NOT NULL AUTO_INCREMENT;