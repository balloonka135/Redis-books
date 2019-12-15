USE "AdvDB Project"

/*
2) Insert a book which author doesn't exists in the database
*/

begin transaction;
declare @max_author int;
declare @max_book int;
declare @author_exists int;

set @max_author = (SELECT MAX(SK_IDAUTHOR) +1 FROM AUTHORS);
set @max_book = (SELECT MAX(SK_IDBOOK) +1 FROM BOOKS);
set @author_exists = (SELECT count(*) FROM AUTHORS WHERE NAMEAUTHOR = 'John Grisham');

IF @author_exists>0 
	INSERT INTO AUTHORS VALUES(@max_author, 'John Grisham');

INSERT INTO BOOKS VALUES (@max_book, 93892839,93892839,93892839,1,'211293892839',2019,'The Guardians','The Guardians','eng',0,0,0,0);
INSERT INTO BOOKS_AUTHORS VALUES (@max_author, @max_book);
commit transaction;

/*
4) Best Book Recommendation by Similar Users
*/
SELECT TOP 10
B.TITLE 
FROM USERS U,
RATINGS R_USER,
RATINGS R_REC,
USERS U_SIM,
RATINGS R_REC2,
BOOKS B
WHERE U.SK_IDUSER = 14
AND U.SK_IDUSER = R_USER.SK_IDUSER
AND R_USER.RATING >= 4 /*Both of them likes this book*/
AND R_REC.SK_IDBOOK = R_USER.SK_IDBOOK
AND R_REC.SK_IDUSER = U_SIM.SK_IDUSER
AND R_REC.RATING >= 4 /*Both of them likes this book*/
AND U_SIM.SK_IDUSER!= U.SK_IDUSER
AND U_SIM.SK_IDUSER= R_REC2.SK_IDUSER
and R_REC2.RATING >=4 /*Best books*/
AND R_REC2.SK_IDBOOK = B.SK_IDBOOK
AND R_USER.SK_IDBOOK != B.SK_IDBOOK
GROUP BY B.TITLE
ORDER BY COUNT(*) DESC
/*
6) Most rated Books that were published in 2015 (Number of Rates)
*/

SELECT TOP 10
B.TITLE, COUNT(*) NUM_RATES
FROM BOOKS B,
RATINGS R
WHERE
B.SK_IDBOOK = R.SK_IDBOOK
GROUP BY B.TITLE
ORDER BY NUM_RATES DESC 

/*
8) Delete the user the rated the least amount of books
*/

begin transaction;

   declare @deletedIds table ( id int );

   delete from RATINGS
   output deleted.SK_IDUSER into @deletedIds
   WHERE SK_IDUSER IN (SELECT
					   U.SK_IDUSER
					   FROM  USERS U
					   LEFT JOIN RATINGS R
					   ON U.SK_IDUSER = R.SK_IDUSER
					   GROUP BY U.SK_IDUSER
					   HAVING COUNT(*) = 
					   (
					   SELECT TOP 1
					   COUNT(*) CANTIDAD
					   FROM USERS U
					   LEFT JOIN RATINGS R
					   ON U.SK_IDUSER = R.SK_IDUSER
					   GROUP BY U.SK_IDUSER
					   ORDER BY CANTIDAD ASC));

   delete from USERS
   WHERE SK_IDUSER IN (SELECT ID FROM @deletedIds);
   
commit transaction;

/*
10) Users that rated Esteban's books with the highest rating per book.
*/

SELECT
A.NAMEAUTHOR
, B.TITLE
, U.NAMEUSER
, R.RATING
FROM 
BOOKS B,
BOOKS_AUTHORS AB,
AUTHORS A,
RATINGS R,
USERS U
WHERE
B.SK_IDBOOK = AB.SK_IDBOOK
AND A.SK_IDAUTHOR = AB.SK_IDAUTHOR
AND R.SK_IDBOOK = B.SK_IDBOOK
AND R.SK_IDUSER = U.SK_IDUSER
AND UPPER(A.NAMEAUTHOR) LIKE '%ESTEBAN%' 
AND R.RATING = (SELECT MAX(RATING) FROM RATINGS R2 WHERE R2.SK_IDBOOK = B.SK_IDBOOK)
ORDER BY B.ORIGINALTITLE ASC
