import time
from collections import defaultdict, Counter
from models import Author, Tag, Rating, User, Book


def first_query():
    """
    give 5 best books with tag '100-books'
    """
    tag = Tag.get(name='100-books')._pk

    books_1 = Book.collection(tag1=tag).sort(by='average_rating').instances(lazy=True)
    books_2 = Book.collection(tag2=tag).sort(by='average_rating').instances(lazy=True)
    books_3 = Book.collection(tag3=tag).sort(by='average_rating').instances(lazy=True)
    books_4 = Book.collection(tag4=tag).sort(by='average_rating').instances(lazy=True)

    books = list(set(books_1) | set(books_2) | set(books_3) | set(books_4))

    if len(books) >= 5:
        return books[-5:]
    else:
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
    the worst 5 books written by author 'J.K.Rowling'
    """
    author = Author.get(full_name='J.K. Rowling')._pk

    books_1 = Book.collection(author1=author).sort(by='average_rating').instances(lazy=True)
    books_2 = Book.collection(author2=author).sort(by='average_rating').instances(lazy=True)
    books_3 = Book.collection(author3=author).sort(by='average_rating').instances(lazy=True)

    books = list(set(books_1) | set(books_2) | set(books_3))

    if len(books) >= 5:
        return books[:5]
    else:
        return books


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


if __name__ == '__main__':
    start_time = time.time()
    result = ninth_query()
    print("--- %s seconds ---\n\n" % (time.time() - start_time))

    import itertools
    new_dict = dict(itertools.islice(result.items(),15))

    for key, value in new_dict.items():
        print(key, value)

    # print(result.hmget_dict('title', 'average_rating', 'original_publication_year', 'language_code'))


