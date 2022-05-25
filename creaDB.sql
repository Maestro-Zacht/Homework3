SET storage_engine = InnoDB;
SET FOREIGN_KEY_CHECKS = 1;
-- create database
CREATE DATABASE IF NOT EXISTS `Cycling`;
USE `Cycling`;
-- drop tables if exist
DROP TABLE IF EXISTS Cyclist;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Stage;
DROP TABLE IF EXISTS Individual_ranking;
-- create tables
SET autocommit = 0;
START TRANSACTION;
CREATE DOMAIN INCR AS INTEGER CHECK (INCR > 0);
CREATE DOMAIN CYEAR AS INTEGER CHECK (
    CYEAR >= 1900
    AND CYEAR <= 2000
);
CREATE DOMAIN CDIFFICULTY AS SMALLINT CHECK(
    CDIFFICULTY >= 1
    and CDIFFICULTY <= 10
);
CREATE TABLE Team(
    TID INCR PRIMARY KEY,
    NameT VARCHAR(50) NOT NULL,
    YearFoundation CYEAR NOT NULL,
    OfficeLocation VARCHAR(50)
);
CREATE TABLE Cyclist(
    CID INCR PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Surname VARCHAR(50) NOT NULL,
    Nationality VARCHAR(50) NOT NULL,
    TID INCR NOT NULL,
    BirthYear INTEGER NOT NULL CHECK(BirthYear > 1800),
    FOREIGN KEY (TID) REFERENCES Team(TID) ON DELETE NO ACTION ON UPDATE CASCADE
);
CREATE TABLE Stage(
    Edition INCR,
    SID INCR,
    DepartureCity VARCHAR(50) NOT NULL,
    ArrivalCity VARCHAR(50) NOT NULL,
    Length INTEGER NOT NULL CHECK (Lenght > 0),
    DeltaHeight INTEGER NOT NULL CHECK (DeltaHeight > 0),
    Difficulty CDIFFICULTY NOT NULL,
    PRIMARY KEY(Edition, SID)
);
CREATE TABLE Individual_ranking(
    Edition INCR,
    SID INCR,
    CID INCR,
    Location INTEGER NOT NULL CHECK(Location > 0),
    PRIMARY KEY(Edition, SID, CID),
    FOREIGN KEY (Edition, SID) REFERENCES Stage(Edition, SID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (CID) REFERENCES Cyclist(CID) ON DELETE CASCADE ON UPDATE CASCADE
);
COMMIT;
START TRANSACTION;
INSERT INTO Team(TID, NameT, YearFoundation, OfficeLocation)
VALUES (1, 'Team1', 1950, 'Turin'),
    (2, 'Team2', 1974);
INSERT INTO Cyclist(CID, Name, Surname, Nationality, TID, BirthYear)
VALUES (1, 'Name1', 'Surname1', 'Italy', 1, 2000),
    (2, 'Name2', 'Surname2', 'Germany', 1, 1999),
    (3, 'Name3', 'Surname3', 'Spain', 2, 2002);
INSERT INTO Stage(
        Edition,
        SID,
        DepartureCity,
        ArrivalCity,
        Length,
        DeltaHeight,
        Difficulty
    )
VALUES (1, 1, 'Turin', 'Milan', 141000, 500, 3),
    (1, 2, 'Turin', 'Susa', 80000, 1000, 6),
    (2, 2, 'Turin', 'Susa', 90000, 2000, 9);
INSERT INTO Individual_ranking(
        Edition,
        SID,
        CID,
        Location
    )
VALUES (1, 1, 1, 1),
    (1, 1, 2, 3),
    (1, 1, 3, 2),
    (1, 2, 1, 1),
    (2, 2, 1, 1);
COMMIT;