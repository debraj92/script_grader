--Query 2 hayatsul
SELECT bid FROM branch WHERE assets >= 
(SELECT AVG(assets) FROM branch WHERE city = "Edmonton");