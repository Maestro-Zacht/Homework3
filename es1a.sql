SELECT C1.Name,
    C1.Surname,
    T1.NameT,
    S1.SID,
    S1.Edition,
    I1.Location
FROM Cyclist C1,
    Team T1,
    Individual_ranking I1,
    Stage S1
WHERE T1.TID = C1.TID
    AND C1.CID = I1.CID
    AND S1.SID = I1.SID
    AND S1.Edition = I1.Edition
    AND C1.CID = 1
    AND S1.SID = 1
ORDER BY S1.Edition ASC;