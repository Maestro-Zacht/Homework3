-- create database
CREATE DATABASE IF NOT EXISTS `Cycling`;
USE `Cycling`;
-- drop tables if exist
SET autocommit = 0;
START TRANSACTION;
DROP TABLE IF EXISTS Individual_ranking;
DROP TABLE IF EXISTS Stage;
DROP TABLE IF EXISTS Cyclist;
DROP TABLE IF EXISTS Team;
COMMIT;
-- create tables
START TRANSACTION;
CREATE TABLE Team(
    TID INTEGER PRIMARY KEY CHECK (TID > 0),
    NameT VARCHAR(50) NOT NULL,
    YearFoundation INTEGER NOT NULL CHECK (
        YearFoundation >= 1900
        AND YearFoundation <= 2000
    ),
    OfficeLocation VARCHAR(50) DEFAULT NULL
);
CREATE TABLE Cyclist(
    CID INTEGER PRIMARY KEY CHECK (CID > 0),
    Name VARCHAR(50) NOT NULL,
    Surname VARCHAR(50) NOT NULL,
    Nationality VARCHAR(50) NOT NULL,
    TID INTEGER NOT NULL,
    BirthYear INTEGER NOT NULL CHECK(
        BirthYear >= 1900
        AND BirthYear <= 2000
    ),
    FOREIGN KEY (TID) REFERENCES Team(TID) ON DELETE NO ACTION ON UPDATE CASCADE
);
CREATE TABLE Stage(
    Edition INTEGER CHECK (Edition > 0),
    SID INTEGER CHECK (SID > 0),
    DepartureCity VARCHAR(50) NOT NULL,
    ArrivalCity VARCHAR(50) NOT NULL,
    Length INTEGER NOT NULL CHECK (Length > 0),
    DeltaHeight INTEGER NOT NULL CHECK (DeltaHeight > 0),
    Difficulty SMALLINT NOT NULL CHECK(
        Difficulty >= 1
        and Difficulty <= 10
    ),
    PRIMARY KEY(Edition, SID)
);
CREATE TABLE Individual_ranking(
    Edition INTEGER,
    SID INTEGER,
    CID INTEGER,
    Location INTEGER NOT NULL CHECK(Location > 0),
    PRIMARY KEY(Edition, SID, CID),
    FOREIGN KEY (Edition, SID) REFERENCES Stage(Edition, SID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (CID) REFERENCES Cyclist(CID) ON DELETE CASCADE ON UPDATE CASCADE
);
COMMIT;
START TRANSACTION;
INSERT INTO Team(TID, NameT, YearFoundation, OfficeLocation)
VALUES (1, 'Team1', 1950, 'Turin'),
    (2, 'Team2', 1974, NULL);
INSERT INTO Cyclist(CID, Name, Surname, Nationality, TID, BirthYear)
VALUES (1, 'Name1', 'Surname1', 'Italy', 1, 2000),
    (2, 'Name2', 'Surname2', 'Germany', 1, 1999),
    (3, 'Name3', 'Surname3', 'Spain', 2, 1988);
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
    (2, 1, 'Turin', 'Milan', 141000, 500, 3),
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
    (2, 1, 1, 2),
    (2, 1, 2, 1),
    (1, 2, 1, 1),
    (2, 2, 1, 1);
COMMIT;