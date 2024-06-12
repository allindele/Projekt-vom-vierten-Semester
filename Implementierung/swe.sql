-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 12. Jun 2024 um 15:09
-- Server-Version: 10.4.32-MariaDB
-- PHP-Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `swe`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `krankmeldung`
--

CREATE TABLE `krankmeldung` (
  `Knr` int(18) NOT NULL,
  `userID` int(16) NOT NULL,
  `Grund` varchar(50) NOT NULL,
  `Von` date NOT NULL,
  `Bis` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `krankmeldung`
--

INSERT INTO `krankmeldung` (`Knr`, `userID`, `Grund`, `Von`, `Bis`) VALUES
(5, 1, 'lkfmbl', '1991-03-19', '1999-12-31'),
(6, 2, 'Keine lust', '2024-06-12', '2024-06-12'),
(7, 2, 'Schlafen', '2024-06-13', '2024-06-15');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user`
--

CREATE TABLE `user` (
  `Unr` int(10) NOT NULL,
  `Vorname` varchar(50) NOT NULL,
  `Nachname` varchar(50) NOT NULL,
  `Rolle` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `user`
--

INSERT INTO `user` (`Unr`, `Vorname`, `Nachname`, `Rolle`) VALUES
(1, 'M', 'A', 'Arbeiter'),
(2, 'Baum', 'Mustermann', 'Arbeiter');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `veranstaltung`
--

CREATE TABLE `veranstaltung` (
  `Vnr` int(16) NOT NULL,
  `userID` int(50) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Type` varchar(50) NOT NULL,
  `Von` datetime NOT NULL,
  `Bis` datetime NOT NULL,
  `Ort` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `veranstaltung`
--

INSERT INTO `veranstaltung` (`Vnr`, `userID`, `Name`, `Type`, `Von`, `Bis`, `Ort`) VALUES
(2, 1, '', 'dsfad', '2024-06-10 08:09:00', '2024-06-10 10:09:00', 'fads2'),
(3, 1, '', 'Vorlesung', '2024-06-11 08:41:12', '2024-06-11 12:41:12', 'Hier'),
(4, 1, '', 'Vorlesung', '2024-06-11 12:41:12', '2024-06-11 13:41:12', 'Hier'),
(5, 1, '', 'Vorlesung', '9999-09-19 09:09:00', '9999-09-09 09:09:00', 'sdas'),
(6, 1, '', 'Test', '9999-07-12 12:00:00', '9999-07-12 14:00:00', 'hier'),
(7, 1, '', 'Test', '2024-07-12 12:00:00', '2024-07-12 14:00:00', 'hier'),
(8, 1, '', 'Vorlesung', '2024-06-15 12:00:00', '2024-06-15 14:00:00', 'Haus'),
(9, 2, '', 'Vorlesung', '2024-06-13 12:00:00', '2024-06-13 14:00:00', 'Haus'),
(10, 0, '', 'Vorlesung', '2024-06-16 08:00:00', '2021-06-16 12:00:00', 'hies');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `krankmeldung`
--
ALTER TABLE `krankmeldung`
  ADD PRIMARY KEY (`Knr`);

--
-- Indizes für die Tabelle `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`Unr`);

--
-- Indizes für die Tabelle `veranstaltung`
--
ALTER TABLE `veranstaltung`
  ADD PRIMARY KEY (`Vnr`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `krankmeldung`
--
ALTER TABLE `krankmeldung`
  MODIFY `Knr` int(18) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT für Tabelle `user`
--
ALTER TABLE `user`
  MODIFY `Unr` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT für Tabelle `veranstaltung`
--
ALTER TABLE `veranstaltung`
  MODIFY `Vnr` int(16) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
