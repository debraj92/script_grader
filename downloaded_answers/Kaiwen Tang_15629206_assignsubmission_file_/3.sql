-- Query 3 kaiwen2
SELECT COUNT(cid)
FROM Customer
Where cid IN (
    SELECT cid 
        FROM Deposit
        EXCEPT
        SELECT cid
    FROM Loan
)