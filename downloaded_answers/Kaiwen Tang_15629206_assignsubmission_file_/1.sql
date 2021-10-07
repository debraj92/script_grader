-- Query 1 kaiwen2
SELECT Customer.cid
FROM Customer, Branch
WHERE Customer.city = Branch.city
AND (Customer.cid, Branch.bid) IN (
        SELECT DISTINCT Loan.cid, Loan.bid
        FROM Loan, Deposit
        WHERE Loan.cid = Deposit.cid
        AND Loan.bid = Deposit.bid);