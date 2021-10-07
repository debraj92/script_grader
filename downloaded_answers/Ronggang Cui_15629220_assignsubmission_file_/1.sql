--Query 1 ronggang
SELECT DISTINCT c.cid
FROM Customer c, Deposit d, Loan l, Branch b
WHERE c.cid = d.cid AND c.cid = l.cid AND d.bid = b.bid AND l.bid = b.bid AND b.city = 'Edmonton'