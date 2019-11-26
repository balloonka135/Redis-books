"""
Data loading from csv files to Redis DB
"""
from models import Author, Genre, Rating, User, Book


authors_path = '/Users/irinanazarchuk/Desktop/authors.csv'
books_path = '/Users/irinanazarchuk/Desktop/books.csv'
ratings_path = 'filepath'
genres_path = 'filepath'
users_path = 'filepath'


def input_authors(filepath):
    try:
        with open(filepath) as f:
            for line in f:
                author_id, full_name = line.split(',')
                author_id = author_id.strip()
                full_name = full_name.strip()
                Author(author_id=author_id, full_name=full_name)
    except Exception as e:
        print(e)


# def input_fake_books(filepath):
#     try:
#         with open(filepath) as f:
#             for line in f:
#                 book_id, title, a_id = line.split(',')
#                 book_id = book_id.strip()
#                 title = title.strip()
#                 a_id = a_id.strip()

#                 try:
#                     author_id = Author.get(author_id=a_id)
#                 except ValueError:
#                     author_id = 'None'
#                     # author_id = Author.collection(author_id=a_id).instances() # list of authors
#                     # TODO: create several instances of the book
#                 except Exception:
#                     author_id = 'None'

#                 book = FakeBook(book_id=book_id, title=title, author_id=author_id)
#                 # book.author_id.set(author_id)
#                 print(book.hmget_dict('book_id', 'author_id', 'title'))
#     except Exception as e:
#         print(e)


def input_genres(filepath):
    try:
        with open(filepath) as f:
            for line in f:
                genre_id, name = line.split(',')
                genre_id = genre_id.strip()
                name = name.strip()
                Genre(genre_id=genre_id, name=name)
    except Exception as e:
        print(e)


def input_users(filepath):
    try:
        with open(filepath) as f:
            for line in f:
                user_id, full_name, language = line.split(',')
                user_id = user_id.strip()
                full_name = full_name.strip()
                language = language.strip()
                User(user_id=user_id, full_name=full_name, language=language)
    except Exception as e:
        print(e)


def input_books(filepath):
    try:
        with open(filepath) as f:
            for line in f:
                book_id, best_book_id, work_id, books_count, \
                    original_title, title, a_id, original_publication_year, \
                    average_rating, isbn, isbn13, language_code, num_pages, \
                    ratings_count, work_ratings_count, \
                    work_text_reviews_count, image_url = line.split(',')

                book_id = book_id.strip()
                best_book_id = best_book_id.strip()
                work_id = work_id.strip()
                books_count = books_count.strip()
                original_title = original_title.strip()
                title = title.strip()
                a_id = a_id.strip()
                original_publication_year = original_publication_year.strip()
                average_rating = average_rating.strip()
                isbn = isbn.strip()
                isbn13 = isbn13.strip()
                language_code = language_code.strip()
                num_pages = num_pages.strip()
                ratings_count = ratings_count.strip()
                work_ratings_count = work_ratings_count.strip()
                work_text_reviews_count = work_text_reviews_count.strip()
                image_url = image_url.strip()

                try:
                    author_id = Author.get(author_id=a_id)
                except ValueError:
                    author_id = 'None'
                    # author_id = Author.collection(author_id=a_id).instances() # list of authors
                    # TODO: create several instances of the book
                except Exception:
                    author_id = 'None'

                book = Book(
                    book_id=book_id, best_book_id=best_book_id, work_id=work_id, \
                    books_count=books_count, original_title=original_title, title=title, \
                    author_id=author_id, original_publication_year=original_publication_year, \
                    average_rating=average_rating, isbn=isbn, isbn13=isbn13, \
                    language_code=language_code, num_pages=num_pages, ratings_count=ratings_count, \
                    work_ratings_count=work_ratings_count, \
                    work_text_reviews_count=work_text_reviews_count, image_url=image_url
                )
                # print(book.hmget_dict('book_id', 'author_id', 'title'))
    except Exception as e:
        print(e)


def input_ratings(filepath):
    try:
        with open(filepath) as f:
            for line in f:
                rating_id, u_id, b_id = line.split(',')
                rating_id = rating_id.strip()
                u_id = u_id.strip()
                b_id = b_id.strip()

                try:
                    user_id = User.get(user_id=u_id)
                except Exception:
                    user_id = 'None'

                try:
                    book_id = Book.get(book_id=b_id)
                except Exception:
                    book_id = 'None'

                Rating(rating_id=rating_id, user_id=user_id, book_id=book_id)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    input_authors(authors_path)
    input_genres(genres_path)
    input_users(users_path)
    input_books(books_path)
    input_ratings(ratings_path)







# create instance

# book = Book(title='Lolita')

# to set FK
# books.genre.hset(genre._pk)
# M2M
# books.authors.sadd(author1._pk, author2._pk)

# add several FK
# book.authors.sadd(author1, author2)

# filter instances and get [0] index
# list(Person.collection(firstname='john', lastname='Smith')) 
