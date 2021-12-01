-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Nov 29, 2021 at 07:56 AM
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
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Aliases`
--

INSERT INTO `Aliases` (`CurrentName`, `CurrentAlliance`, `CurrentLevel`, `PreviousName`, `PreviousAlliance`, `LastUpdatedBy`, `LastUpdated`) VALUES
('AdmiralAllanon', 'TTS', 38, NULL, NULL, current_user(), current_timestamp(6) ),
('CommodoreAl', 'TTS', 39, NULL, NULL, current_user(), current_timestamp(6) ),
('Derpina', 'DERP', 33, NULL, NULL, current_user(), current_timestamp(6) ),
('MrsWhatEver', 'DERP', 33, 'Derpina', 'DERP', current_user(), current_timestamp(6) ),
('TastyC', 'PYRT', 34, 'TastyCorpse', 'PYRT', current_user(), current_timestamp(6) ),
('TastyCorpse', 'PYRT', 33, NULL, NULL, current_user(), current_timestamp(6) ),
('VinnyBottoms', 'PYRT', 34, 'MrsWhatEver', 'DERP', current_user(), current_timestamp(6) );

-- --------------------------------------------------------

--
-- Table structure for table `Alliances`
--

CREATE TABLE `Alliances` (
  `CurrentName` varchar(4) NOT NULL,
  `CurrentAdmiral` varchar(40) NOT NULL,
  `PreviousName` varchar(4) DEFAULT NULL,
  `PreviousAdmiral` varchar(40) DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `Alliances`
--

INSERT INTO `Alliances` (`CurrentName`, `CurrentAdmiral`, `PreviousName`, `PreviousAdmiral`, `LastUpdatedBy`, `LastUpdated`) VALUES
('DERP', 'Derpina', NULL, NULL, current_user(), current_timestamp(6) ),
('PYRT', 'TastyCorpse', NULL, NULL, current_user(), current_timestamp(6) ),
('TTS', 'AdmiralAllanon', NULL, NULL, current_user(), current_timestamp(6) );

-- --------------------------------------------------------

--
-- Table structure for table `BaseSightings`
--

CREATE TABLE `BaseSightings` (
  `Name` varchar(40) NOT NULL,
  `Alliance` varchar(4) DEFAULT NULL,
  `SystemID` int(11) NOT NULL,
  `Location` varchar(25) NOT NULL,
  `ShipsPresent` int(11) DEFAULT NULL,
  `Shielded` tinyint(1) NOT NULL,
  `StillCurrent` tinyint(1) NOT NULL DEFAULT 1,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `BaseSightings`
--

INSERT INTO `BaseSightings` (`Name`, `Alliance`, `SystemID`, `Location`, `ShipsPresent`, `Shielded`, `StillCurrent`, `LastUpdatedBy`, `LastUpdated`) VALUES
('CommodoreAl', 'TTS', 1342058302, 'X:-23 Y:324', 4, 0, 1, current_user(), current_timestamp(6) );

COMMIT;

INSERT INTO `BaseSightings` (`Name`, `Alliance`, `SystemID`, `Location`, `ShipsPresent`, `Shielded`, `StillCurrent`, `LastUpdatedBy`, `LastUpdated`) VALUES
('CommodoreAl', 'TTS', 1342058302, 'X:-23 Y:324', 4, 1, 0, current_user(), current_timestamp(6) );

--
-- Triggers `BaseSightings`
--
-- DELIMITER $$
--  CREATE TRIGGER `BaseSightingCurrency` BEFORE INSERT ON `BaseSightings` FOR EACH ROW 
-- 	UPDATE `BaseSightings` SET `StillCurrent` = 0 
-- 	 WHERE `Alliance` = Alliance 
-- 	   AND `Name` = Name 
-- 	   AND `StillCurrent` = 1
-- $$
-- DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `FlagOfficers`
--

CREATE TABLE `FlagOfficers` (
  `Name` varchar(40) NOT NULL,
  `Alliance` varchar(4) NOT NULL,
  `SpotterID` varchar(20) NOT NULL,
  `AccessStarted` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `AccessEnded` timestamp(6) NULL DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `FlagOfficers`
--

INSERT INTO `FlagOfficers` (`Name`, `Alliance`, `SpotterID`, `AccessStarted`, `AccessEnded`, `LastUpdatedBy`, `LastUpdated`) VALUES
('AdmiralAllanon', 'TTS', 'ttsadmallanon', '2021-11-23 18:46:39', NULL, current_user(), current_timestamp(6) ),
('CommodoreAl', 'TTS', 'ttscmdral', '2021-11-23 18:45:42', NULL, current_user(), current_timestamp(6) );

-- --------------------------------------------------------

--
-- Table structure for table `ShipSightings`
--

CREATE TABLE `ShipSightings` (
  `Name` varchar(40) NOT NULL,
  `Alliance` varchar(4) NOT NULL,
  `SystemID` int(11) NOT NULL,
  `Location` varchar(25) NOT NULL,
  `ShipName` varchar(20) NOT NULL,
  `ShipStrength` int(11) NOT NULL,
  `SightingType` set('Grinding','Floating','Hunting','Mining') NOT NULL,
  `StillCurrent` tinyint(1) NOT NULL DEFAULT 1,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `StfcShips`
--

CREATE TABLE `StfcShips` (
  `ShipID` int(11) NOT NULL,
  `ShipName` varchar(20) NOT NULL,
  `ShipLevel` int(11) NOT NULL,
  `ShipType` set('Battleship','Explorer','Interceptor','Survey') NOT NULL,
  `ShipFaction` varchar(20) NULL DEFAULT NULL,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `StfcSystems`
--

CREATE TABLE `StfcSystems` (
  `SystemID` int(11) NOT NULL,
  `SystemName` varchar(20) NOT NULL,
  `SystemLevel` int(11) DEFAULT NULL,
  `SystemWarpDist` int(11) NOT NULL,
  `SystemType` set('Federation','Independent','Klingon','Romulan','Territory') NOT NULL,
  `DarkSpace` tinyint(1) NOT NULL DEFAULT 0,
  `LastUpdatedBy` varchar(20) NOT NULL DEFAULT CURRENT_USER,
  `LastUpdated` timestamp(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `StfcSystems`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Aliases`
--
ALTER TABLE `Aliases`
  ADD PRIMARY KEY (`CurrentName`,`CurrentAlliance`),
  ADD KEY `Alliances5` (`CurrentAlliance`);

--
-- Indexes for table `Alliances`
--
ALTER TABLE `Alliances`
  ADD PRIMARY KEY (`CurrentName`,`CurrentAdmiral`);

--
-- Indexes for table `BaseSightings`
--
ALTER TABLE `BaseSightings`
  ADD PRIMARY KEY (`Name`,`Alliance`,`LastUpdated`),
  ADD KEY `SystemID1` (`SystemID`),
  ADD KEY `Alliance1` (`Alliance`);

--
-- Indexes for table `FlagOfficers`
--
ALTER TABLE `FlagOfficers`
  ADD PRIMARY KEY (`SpotterID`,`Name`,`Alliance`);

--
-- Indexes for table `ShipSightings`
--
ALTER TABLE `ShipSightings`
  ADD PRIMARY KEY (`Name`,`Alliance`,`LastUpdated`),
  ADD KEY `SystemID3` (`SystemID`),
  ADD KEY `AllianceID3` (`Alliance`);

--
-- Indexes for table `StfcShips`
--
ALTER TABLE `StfcShips`
  ADD PRIMARY KEY (`ShipID`,`ShipName`);

--
-- Indexes for table `StfcSystems`
--
ALTER TABLE `StfcSystems`
  ADD PRIMARY KEY (`SystemID`,`SystemName`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Aliases`
--
ALTER TABLE `Aliases`
  ADD CONSTRAINT `Alliances5` FOREIGN KEY (`CurrentAlliance`) REFERENCES `Alliances` (`CurrentName`);

--
-- Constraints for table `BaseSightings`
--
ALTER TABLE `BaseSightings`
  ADD CONSTRAINT `Alias1` FOREIGN KEY (`Name`) REFERENCES `Aliases` (`CurrentName`),
  ADD CONSTRAINT `Alliance1` FOREIGN KEY (`Alliance`) REFERENCES `Alliances` (`CurrentName`),
  ADD CONSTRAINT `SystemID1` FOREIGN KEY (`SystemID`) REFERENCES `StfcSystems` (`SystemID`);

--
-- Constraints for table `ShipSightings`
--
ALTER TABLE `ShipSightings`
  ADD CONSTRAINT `Aliases3` FOREIGN KEY (`Name`) REFERENCES `Aliases` (`CurrentName`),
  ADD CONSTRAINT `AllianceID3` FOREIGN KEY (`Alliance`) REFERENCES `Alliances` (`CurrentName`),
  ADD CONSTRAINT `SystemID3` FOREIGN KEY (`SystemID`) REFERENCES `StfcSystems` (`SystemID`);

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
