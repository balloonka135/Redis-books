import time
from collections import defaultdict, Counter
from models import Author, Tag, Rating, User, Book


def first_query():
    """
    give 5 best books with tag '100-books'
    """
    tag = Tag.get(name='100-books')._pk

    books = Book.collection(tag1=tag).sort(by='average_rating').instances(lazy=True)

    if len(books) >= 5:
        return books[-5:]
    else:
        return books


def second_query():
    """
    2) Insert a book which author doesn't exists in the database
    """

    authors = Author.collection()
    max_author = max([int(author) for author in authors]) + 1
    books = Book.collection()
    max_books = max([int(book) for book in books]) + 1

    book = Book(sk_book_id=max_books, book_id=93892839, best_book_id=93892839, work_id=93892839, \
                        books_count=1, isbn='211293892839', original_publication_year=2019, \
                        original_title='The Guardians', title='The Guardians', language_code='eng', \
                        average_rating=0, ratings_count=0, \
                        work_ratings_count=0, \
                        work_text_reviews_count=0, \
                        author1=max_author, author2='None', author3='None', \
                        tag1='None', tag2='None', tag3='None', tag4='None', tag5='None'
                    )

    author = Author(author_id=max_author, full_name='John Grisham')

    return author


def third_query():
    """
    user that ranked the most books
    """

    users_in_ratings = Rating.collection().values_list('user_id', flat=True)
    num_user_occurs = Counter(list(users_in_ratings))
    most_common_user = num_user_occurs.most_common(10)
    user_id = most_common_user[0][0]
    user = User.get(user_id=user_id)

    return user


def fourth_query():
    """
    4) Best Book Recommendation by Similar Users
    """
    user = User.get(user_id = 20)
    books_user = [r.hmget_dict('book_id') for r in Rating.collection(user_id = user, rating = 5).instances(lazy = True) if r.hmget_dict('book_id')['book_id'] != 'None']
    users_similar = [r.hmget_dict('user_id') for u in books_user for r in Rating.collection(book_id = u['book_id'], rating = 5).instances(lazy = True)]
    books_similar = [r.hmget_dict('book_id')['book_id'] for u in users_similar for r in Rating.collection(user_id = u['user_id'], rating = 5).instances(lazy = True) if r.hmget_dict('book_id')['book_id'] != 'None']
    best_10_books = Counter(books_similar).most_common(10)

    for b in best_10_books:
        print(Book.get(pk=b[0]).hmget_dict('title'))

    print('\n\n')



def fifth_query():
    """
    the worst 5 books written by author 'J.K.Rowling'
    """
    author = Author.get(full_name='J.K. Rowling')._pk

    books_1 = Book.collection(author1=author).sort(by='average_rating').instances(lazy=True)
    books_2 = Book.collection(author2=author).sort(by='average_rating').instances(lazy=True)
    books_3 = Book.collection(author3=author).sort(by='average_rating').instances(lazy=True)

    books_list = list(set(books_1) | set(books_2) | set(books_3))
    books = sorted(list([b.hmget('title')[0], b.hmget('average_rating')[0]] for b in books_list), key=lambda x: x[1])
    if len(books) >= 5:
        return books[:5]
    else:
        return books


def sixth_query():
    """
    6) Most rated Books that were published in 2015 (Number of Rates)
    """
    books = Book.collection(original_publication_year='2015', language_code='en-US').instances()
    ratings = []
    ratings = [r.hmget_dict('book_id')['book_id'] for b in books for r in Rating.collection(book_id=b).instances(lazy = True)]
    num_rating_books = Counter(ratings).most_common(10)

    for b in num_rating_books:
        print(Book.get(pk=b[0]).hmget_dict('title'))

    print('\n\n')


def seventh_query():
    """
    update book 'Gone Girl'
    """

    book = Book.get(title='Gone Girl')
    book.hmset(
        average_rating='4.5',
        original_publication_year=1990,
        language_code='ru'
    )
    return book


def eigth_query():
    """
    8) Delete the user the rated the least amount of books
    """

    user_ratings = Rating.collection().values_list('user_id', flat=True)
    num_rating_users = Counter(user_ratings)
    m = min(num_rating_users, key=num_rating_users.get)
    [r.delete() for r in Rating.collection(user_id=m).instances()]
    User.get(user_id=m).delete()

    return User.get(user_id=m)


def ninth_query():
    """
    for each female user select books from 2009 with same language
    """

    books = Book.collection(original_publication_year='2009').instances()
    # generate list of book dictionaries
    books_list = [book.hmget_dict('title', 'language_code') for book in books]

    users = User.collection(gender='female').instances()
    # generate list of user dictionaries
    users_list = [user.hmget_dict('full_name', 'language') for user in users]

    result = defaultdict(list)
    for user in users_list:
        user_language = user['language']
        for book in books_list:
            if book['language_code'] == user_language:
                username = user['full_name'].encode('utf8')
                book_title = book['title'].encode('utf8')
                result[username].append(book_title)

    return result


def tenth_query():
    """
        10) Users that rated Esteban's books with the highest rating per book.
    """
    author = Author.get(full_name = 'Esteban Zimanyi')
    book = Book.get(author1 = author._pk)
    ratings = [r.hmget_dict('user_id') for r in Rating.collection(book_id = book, rating = 5).instances()]
    best_users = [u.hmget_dict('full_name') for r in ratings for u in User.collection(user_id = r['user_id']).instances()]
    print(best_users)


if __name__ == '__main__':
    start_time = time.time()
    result = sixth_query()
    print("\n\n--- %s seconds ---\n\n" % (time.time() - start_time))
