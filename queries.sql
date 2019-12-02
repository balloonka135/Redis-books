/*
    1) give 5 best books with tag 'dystopia'
*/
SELECT TOP 5 BOOKS.TITLE FROM BOOKS
WHERE TAGS.NAMETAG = 'dystopia%'
INNER JOIN BOOKS_TAGS ON BOOKS_TAGS.SK_IDBOOK = BOOKS.SK_IDBOOK
INNER JOIN TAGS ON TAGS.SK_IDTAG = BOOKS_TAGS.SK_IDTAG
ORDER BY BOOKS.AVERAGERATING DESC


/*
    3) user that ranked the most books
*/
SELECT TOP 1 USERS.NAMEUSER
FROM USERS INNER JOIN RATINGS ON RATINGS.SK_IDUSER = USERS.SK_IDUSER
GROUP BY USERS.NAMEUSER
ORDER BY COUNT(RATINGS.SK_IDUSER) DESC

/*
    5) the worst 5 books written by author 'J.K.Rowling'
*/
SELECT TOP 5 BOOKS.TITLE FROM BOOKS
WHERE AUTHORS.NAMEAUTHOR = 'J.K. Rowling'
INNER JOIN BOOKS_AUTHORS ON BOOKS_AUTHORS.SK_IDBOOK = BOOKS.SK_IDBOOK
INNER JOIN AUTHORS ON AUTHORS.SK_IDAUTHOR = BOOKS_AUTHORS.SK_IDAUTHOR
ORDER BY BOOKS.AVERAGERATING ASC

/*
    7) update book 'Harry Potter'
*/
UPDATE BOOKS
SET AVERAGERATING = 5, YEAROFPUBLICATION = 1990, LANGUAGE = 'ru'
WHERE TITLE = 'Gone Girl'


/*
    9) for each user select books with same language
       and that aren't older then 20 years
*/
SELECT USERS.NAMEUSER FROM USERS
GROUP BY USERS.NAMEUSER
WHERE USERS.NATIVELANGUAGE = (
    SELECT BOOKS.LANGUAGE FROM BOOKS
    WHERE BOOKS.YEAROFPUBLICATION >= 1999
)