-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Dec 01, 2021 at 02:15 AM
-- Server version: 10.6.5-MariaDB-1:10.6.5+maria~focal
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stfcpirate`
--

-- --------------------------------------------------------

--
-- Table structure for table `Aliases`
--

CREATE TABLE `Aliases` (
  `CurrentName` varchar(40) NOT NULL,
  `CurrentAlliance` varchar(4) NOT NULL,
  `CurrentLevel` int(11) DEFAULT NULL,
  `PreviousName` varchar(40) DEFAULT NULL,
  `PreviousAlliance` varchar(4) DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Aliases`
--

INSERT INTO `Aliases` (`CurrentName`, `CurrentAlliance`, `CurrentLevel`, `PreviousName`, `PreviousAlliance`, `LastUpdatedBy`, `LastUpdated`) VALUES
('AdmiralAllanon', 'TTS', 38, NULL, NULL, 'root@%', '2021-12-01 02:13:50.293428'),
('CommodoreAl', 'TTS', 39, NULL, NULL, 'root@%', '2021-12-01 02:13:50.293428'),
('Derpina', 'DERP', 33, NULL, NULL, 'root@%', '2021-12-01 02:13:50.293428'),
('MrsWhatEver', 'DERP', 33, 'Derpina', 'DERP', 'root@%', '2021-12-01 02:13:50.293428'),
('TastyC', 'PYRT', 34, 'TastyCorpse', 'PYRT', 'root@%', '2021-12-01 02:13:50.293428'),
('TastyCorpse', 'PYRT', 33, NULL, NULL, 'root@%', '2021-12-01 02:13:50.293428'),
('VinnyBottoms', 'PYRT', 34, 'MrsWhatEver', 'DERP', 'root@%', '2021-12-01 02:13:50.293428');

-- --------------------------------------------------------

--
-- Table structure for table `Alliances`
--

CREATE TABLE `Alliances` (
  `CurrentName` varchar(4) NOT NULL,
  `CurrentAdmiral` varchar(40) NOT NULL,
  `PreviousName` varchar(4) DEFAULT NULL,
  `PreviousAdmiral` varchar(40) DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Alliances`
--

INSERT INTO `Alliances` (`CurrentName`, `CurrentAdmiral`, `PreviousName`, `PreviousAdmiral`, `LastUpdatedBy`, `LastUpdated`) VALUES
('DERP', 'Derpina', NULL, NULL, 'root@%', '2021-12-01 02:13:50.349641'),
('PYRT', 'TastyCorpse', NULL, NULL, 'root@%', '2021-12-01 02:13:50.349641'),
('TTS', 'AdmiralAllanon', NULL, NULL, 'root@%', '2021-12-01 02:13:50.349641');

-- --------------------------------------------------------

--
-- Table structure for table `BaseSightings`
--

CREATE TABLE `BaseSightings` (
  `Name` varchar(40) NOT NULL,
  `Alliance` varchar(4) NOT NULL,
  `SystemID` bigint(11) NOT NULL,
  `Location` varchar(25) NOT NULL,
  `ShipsPresent` int(11) DEFAULT NULL,
  `Shielded` tinyint(1) NOT NULL,
  `StillCurrent` tinyint(1) NOT NULL DEFAULT 1,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `BaseSightings`
--

INSERT INTO `BaseSightings` (`Name`, `Alliance`, `SystemID`, `Location`, `ShipsPresent`, `Shielded`, `StillCurrent`, `LastUpdatedBy`, `LastUpdated`) VALUES
('CommodoreAl', 'TTS', 1342058302, 'X:-23 Y:324', 4, 0, 1, 'root@%', '2021-12-01 02:13:50.403350'),
('CommodoreAl', 'TTS', 1342058302, 'X:-23 Y:324', 4, 1, 0, 'root@%', '2021-12-01 02:13:50.424275');

-- --------------------------------------------------------

--
-- Table structure for table `FlagOfficers`
--

CREATE TABLE `FlagOfficers` (
  `Name` varchar(40) NOT NULL,
  `Alliance` varchar(4) NOT NULL,
  `SpotterID` varchar(20) NOT NULL,
  `AccessStarted` timestamp(6) NOT NULL DEFAULT current_timestamp(6),
  `AccessEnded` timestamp(6) NULL DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `FlagOfficers`
--

INSERT INTO `FlagOfficers` (`Name`, `Alliance`, `SpotterID`, `AccessStarted`, `AccessEnded`, `LastUpdatedBy`, `LastUpdated`) VALUES
('AdmiralAllanon', 'TTS', 'ttsadmallanon', '2021-11-23 18:46:39.000000', NULL, 'root@%', '2021-12-01 02:13:50.470643'),
('CommodoreAl', 'TTS', 'ttscmdral', '2021-11-23 18:45:42.000000', NULL, 'root@%', '2021-12-01 02:13:50.470643');

-- --------------------------------------------------------

--
-- Table structure for table `ShipSightings`
--

CREATE TABLE `ShipSightings` (
  `Name` varchar(40) NOT NULL,
  `Alliance` varchar(4) NOT NULL,
  `SystemID` bigint(11) NOT NULL,
  `Location` varchar(25) NOT NULL,
  `ShipName` varchar(20) NOT NULL,
  `ShipStrength` int(11) NOT NULL,
  `SightingType` set('Grinding','Floating','Hunting','Mining') NOT NULL,
  `StillCurrent` tinyint(1) NOT NULL DEFAULT 1,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `StfcShips`
--

CREATE TABLE `StfcShips` (
  `ShipID` bigint(11) NOT NULL,
  `ShipName` varchar(20) NOT NULL,
  `ShipLevel` int(11) NOT NULL,
  `ShipType` set('Battleship','Explorer','Interceptor','Survey') NOT NULL,
  `ShipFaction` varchar(20) DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `StfcShips`
--


-- --------------------------------------------------------

--
-- Table structure for table `StfcSystems`
--

CREATE TABLE `StfcSystems` (
  `SystemID` bigint(11) NOT NULL,
  `SystemName` varchar(20) NOT NULL,
  `SystemLevel` int(11) DEFAULT NULL,
  `SystemWarpDist` int(11) NOT NULL,
  `SystemType` set('Federation','Independent','Klingon','Romulan','Territory') NOT NULL,
  `DarkSpace` tinyint(1) NOT NULL DEFAULT 0,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT current_user(),
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `StfcSystems`
--
