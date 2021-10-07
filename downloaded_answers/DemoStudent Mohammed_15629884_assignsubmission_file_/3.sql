--Query 3 hayatsul
SELECT COUNT(cid) AS TotalCustomers FROM 
(SELECT cid FROM customer NATURAL JOIN deposit EXCEPT SELECT cid FROM customer NATURAL JOIN loan);
