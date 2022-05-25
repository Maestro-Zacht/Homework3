START TRANSACTION;
INSERT INTO Cyclist(CID, Name, Surname, Nationality, TID, BirthYear)
VALUES (4, 'Name4', 'Surname4', 'UK', 1, 1996);
INSERT INTO Individual_ranking(
        Edition,
        SID,
        CID,
        Location
    )
VALUES (2, 1, 4, 3);
COMMIT;