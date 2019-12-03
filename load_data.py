"""
Data loading from csv files to Redis DB
"""
from models import Author, Tag, Rating, \
    User, Book, BooksAuthors, BooksTags


authors_path = '/Users/irinanazarchuk/Desktop/data/authors.csv'
books_path = '/Users/irinanazarchuk/Desktop/data/books.csv'
books_authors_path = '/Users/irinanazarchuk/Desktop/data/books_authors.csv'
ratings_path = '/Users/irinanazarchuk/Desktop/data/ratings.csv'
tags_path = '/Users/irinanazarchuk/Desktop/data/tags.csv'
books_tags_path = '/Users/irinanazarchuk/Desktop/data/books_tags.csv'
users_path = '/Users/irinanazarchuk/Desktop/data/users.csv'


def input_authors(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                author_id, full_name = line.split(',')
                author_id = author_id.strip()
                full_name = full_name.strip()
                Author(author_id=author_id, full_name=full_name)
    except Exception as e:
        print(e)


def input_tags(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                tag_id, name = line.split(',')
                tag_id = tag_id.strip()
                name = name.strip()
                Tag(tag_id=tag_id, name=name)
    except Exception as e:
        print(e)


def input_users(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                user_id, full_name, gender, language = line.split(',')
                user_id = user_id.strip()
                full_name = full_name.strip()
                gender = gender.strip()
                language = language.strip()
                User(user_id=user_id, full_name=full_name,
                     gender=gender, language=language)
    except Exception as e:
        print(e)


def input_books(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                sk_book_id, book_id, best_book_id, work_id, books_count, \
                    isbn, original_publication_year, original_title, title, \
                    language_code, average_rating, ratings_count, \
                    work_ratings_count, work_text_reviews_count = line.split(',')

                sk_book_id = sk_book_id.strip()
                book_id = book_id.strip()
                best_book_id = best_book_id.strip()
                work_id = work_id.strip()
                books_count = books_count.strip()
                isbn = isbn.strip()
                original_publication_year = original_publication_year.strip()
                original_title = original_title.strip()
                title = title.strip()
                language_code = language_code.strip()
                average_rating = average_rating.strip()
                ratings_count = ratings_count.strip()
                work_ratings_count = work_ratings_count.strip()
                work_text_reviews_count = work_text_reviews_count.strip()

                book = Book(
                    sk_book_id=sk_book_id, book_id=book_id, best_book_id=best_book_id, work_id=work_id, \
                    books_count=books_count, isbn=isbn, original_publication_year=original_publication_year, \
                    original_title=original_title, title=title, language_code=language_code, \
                    average_rating=average_rating, ratings_count=ratings_count, \
                    work_ratings_count=work_ratings_count, \
                    work_text_reviews_count=work_text_reviews_count
                )

                # print(book.hmget_dict('book_id', 'author_id', 'title'))
    except Exception as e:
        print(e)


def input_ratings(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                u_id, b_id, rating = line.split(',')
                u_id = u_id.strip()
                b_id = b_id.strip()
                rating = rating.strip()

                try:
                    user_id = User.get(user_id=u_id)
                except Exception:
                    user_id = 'None'

                try:
                    book_id = Book.get(book_id=b_id)
                except Exception:
                    book_id = 'None'

                Rating(user_id=user_id, book_id=book_id, rating=rating)
    except Exception as e:
        print(e)


def input_books_tags(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                t_id, b_id, count = line.split(',')
                t_id = t_id.strip()
                b_id = b_id.strip()
                count = count.strip()

                try:
                    sk_tag_id = Tag.get(tag_id=t_id)
                except Exception:
                    sk_tag_id = 'None'

                try:
                    sk_book_id = Book.get(sk_book_id=b_id)
                except Exception:
                    sk_book_id = 'None'

                BooksTags(sk_tag_id=sk_tag_id, sk_book_id=sk_book_id,
                          count=count)
    except Exception as e:
        print(e)


def input_books_authors(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                t_id, b_id = line.split(',')
                t_id = t_id.strip()
                b_id = b_id.strip()

                try:
                    sk_author_id = Author.get(author_id=t_id)
                except Exception:
                    sk_author_id = 'None'

                try:
                    sk_book_id = Book.get(sk_book_id=b_id)
                except Exception:
                    sk_book_id = 'None'

                BooksAuthors(sk_author_id=sk_author_id, sk_book_id=sk_book_id)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # input_authors(authors_path)
    # input_tags(tags_path)
    # input_users(users_path)
    input_books(books_path)
    # input_ratings(ratings_path)
    # input_books_tags(books_tags_path)
    # input_books_authors(books_authors_path)







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
