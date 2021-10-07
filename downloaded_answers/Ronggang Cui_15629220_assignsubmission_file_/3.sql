--Query 3 ronggang
SELECT COUNT(*)
FROM Customer
WHERE cid in 
(SELECT cid
FROM Deposit)
AND cid not in 
(SELECT cid
FROM loan)