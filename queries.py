from collections import defaultdict, Counter
from models import Author, Tag, Rating, User, Book


def first_query():
    """
    give 5 best books with tag '100-books'
    """
    tag = Tag.get(name='100-books')._pk

    books_1 = Book.collection(tag1=tag).instances(lazy=True)
    books_2 = Book.collection(tag2=tag).instances(lazy=True)
    books_3 = Book.collection(tag3=tag).instances(lazy=True)
    books_4 = Book.collection(tag4=tag).instances(lazy=True)

    books = list(set(books_1) | set(books_2) | set(books_3) | set(books_4))

    rated_books = books.sort(by='average_rating')

    if len(rated_books) >= 5:
        return rated_books[-5:]
    else:
        return rated_books


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
    author = Author.get(full_name='J.K. Rowling')._pk

    books_1 = Book.collection(author1=author).instances(lazy=True)
    books_2 = Book.collection(author2=author).instances(lazy=True)
    books_3 = Book.collection(author3=author).instances(lazy=True)

    books = list(set(books_1) | set(books_2) | set(books_3))

    rated_books = books.sort(by='average_rating')

    if len(rated_books) >= 5:
        return rated_books[:5]
    else:
        return rated_books


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


def ninth_query():
    # TODO: modify to rating > 4
    """
    for each user select books with same language
    and that aren't older than 10 years
    """

    books = Book.collection(original_publication_year__gte=2009).instances()
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
                username = user['full_name'].encode('utf8')
                book_title = book['title'].encode('utf8')
                result[username].append(book_title)

    print(result)
    return result


if __name__ == '__main__':
    first_query()

