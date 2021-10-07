--Query 1 hayatsul
SELECT Customer.cid FROM Customer
JOIN Deposit ON Customer.cid = Deposit.cid
JOIN LOAN ON Customer.cid = Loan.cid 
JOIN branch ON Branch.bid = Deposit.bid
WHERE Deposit.bid = Loan.bid AND Branch.city = Customer.city;