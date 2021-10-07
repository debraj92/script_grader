-- Query 1 zhengdao
SELECT DISTINCT c.cid
FROM Branch b, Customer c, Deposit d, Loan l
WHERE c.cid = d.cid
	and d.cid = l.cid
	and d.bid = l.bid
	and b.city = c.city
	and b.bid = d.bid
	and b.bid = l.bid
