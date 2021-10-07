-- Query 3 zhengdao
SELECT COUNT(DISTINCT cid)
FROM Customer
WHERE cid in
(SELECT cid
FROM Deposit
EXCEPT
SELECT cid
FROM Loan)
