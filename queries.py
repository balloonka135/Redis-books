from collections import defaultdict, Counter
from models import Author, Tag, Rating, User, Book, BooksTags, BooksAuthors


def first_query():
    """
    give 5 best books with tag 'dystopia'
    """

    tags = Tag.collection(name__startswith='dystopia').instances()
    book_tags = BooksTags.collection().instances()
    result_books_tags = []
    for book_tag in book_tags:
        if book_tag.hmget('sk_tag_id') in tags:
            result_books_tags.append(book_tag.hmget('sk_book_id'))

    result = []
    books = Book.collection().sort(by='average_rating')
    for book in books:
        if book.hmget('sk_book_id') in result_books_tags:
            result.append(book)

    return result[-5:]


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
    the worst 5 books written by author 'J.K.Rowling'
    """

    author = Author.get(full_name='J.K. Rowling')
    author_books = BooksAuthors.collection(sk_author_id=author).values_list('sk_book_id', flat=True)
    books = Book.collection().sort(by='average_rating')

    result = []
    for book in books:
        if book.hmget('sk_book_id') in author_books:
            result.append(book)

    return result[:5]


def seventh_query():
    """
    update book 'Gone Girl'
    """

    book = Book.get(title='Gone Girl')
    print(book)
    book.hmset(
        average_rating='4.5',
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




