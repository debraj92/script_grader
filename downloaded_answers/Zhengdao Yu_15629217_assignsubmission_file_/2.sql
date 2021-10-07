-- Query 2 zhengdao
SELECT bid
FROM Branch
Where assets >(SELECT AVG(assets)
		FROM Branch
		WHERE city='Edmonton')
