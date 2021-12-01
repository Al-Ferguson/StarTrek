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
