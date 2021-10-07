--Query 2 Ntabassu
SELECT bid FROM Branch WHERE assets >=(SELECT avg (assets) FROM Branch WHERE city="Edmonton")