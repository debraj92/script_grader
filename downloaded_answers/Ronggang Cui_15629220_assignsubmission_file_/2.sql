--Query 2 ronggang
SELECT DISTINCT b1.bid
FROM Branch b1
WHERE b1.assets > 
(SELECT AVG(b2.assets)
FROM Branch b2
WHERE b2.city = 'Edmonton')