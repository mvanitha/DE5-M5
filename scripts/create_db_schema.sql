Use QAETLStagingDB;

drop table if exists dbo.Customer;
create table if not exists dbo.Customer
(
  	 CustomerID integer
	, CustomerName varchar(100)
)
;

drop table if exists dbo.Book;
create table if not exists dbo.Book
(
  	  Id integer
	, Books varchar(Max)
	, Book_checkout datetime
	, Book_Returned datetime
	, Days_allowed_to_borrow varchar(50)
	, Customer_ID integer
	, Days_Borrowed integer
)
;

drop table if exists dbo.AuditLog;
create table if not exists dbo.AuditLog
(
  	    LoadName varchar(100)
	  , LoadCount integer
	  , InsertDateTime datetime default getdate()	
)
;

select * from dbo.Customer
select * from dbo.Book
select * from dbo.AuditLog