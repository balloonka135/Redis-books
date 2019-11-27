from collections import defaultdict, Counter
from models import Author, Genre, Rating, User, Book


def first_query():
    """
    give 5 best books of genre 'drama'
    """

    genre_instance = Genre.get(name='drama')
    # sort in asc order, retrieve last 5 books
    books = Book.collection(
        genre_id=genre_instance).sort(by='average_rating')[-5:]
    return books


def third_query():
    """
    user that ranked the most books
    """

    users_in_ratings = Rating.collection().values_list('user_id', flat=True)
    # counts the number of each user occurence in a list
    num_user_occurs = Counter(users_in_ratings)
    most_common_user = num_user_occurs.most_common(1)
    user_id = most_common_user[0][0]
    user = User.get(user_id=user_id)
    return user


def fifth_query():
    """
    the worst books written by author 'J.K.Rowling'
    """

    author = Author.get(full_name='J.K.Rowling')
    books = Book.collection(author_id=author).sort(by='average_rating')[:5]
    return books


def seventh_query():
    """
    update book 'Harry Potter'
    """

    book = Book.get(title='Harry Potter')
    print(book)
    book.hmset(
        average_rating='5',
        original_publication_year=1990,
        language_code='ru'
    )
    return book


def ninth_query():
    """
    for each user select books with same language
    and that aren't older then 20 years
    """

    books = Book.collection(original_publication_year__gte=1999).instances()
    # generate list of book dictionaries
    books_list = [book.hmget_dict('title', 'language_code') for book in books]

    users = User.collection().instances()
    # generate list of user dictionaries
    users_list = [user.hmget_dict('full_name', 'language') for user in users]

    result = defaultdict(list)
    for user in users_list:
        user_language = user['language']
        for book in books_list:
            if book['language_code'] == user_language:
                result[user['full_name']].append(book['title'])

    return result




