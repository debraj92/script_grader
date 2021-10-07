-- Query 2 kaiwen2
SELECT bid
FROM Branch
Where Branch.assets >= (
    SELECT AVG(assets)
    FROM Branch
)