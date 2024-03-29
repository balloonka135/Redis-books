"""
Data loading from csv files to Redis DB
"""

from models import Author, Tag, Rating, \
    User, Book


authors_path = '/Users/irinanazarchuk/Desktop/data/authors.csv'
books_path = '/Users/irinanazarchuk/Desktop/data/books.tsv'
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
                work_ratings_count, work_text_reviews_count, \
                aid1, aid2, aid3, \
                tid1, tid2, tid3, tid4, tid5 = line.split('\t')

                tid5 = tid5.strip()

                # chinese code style...
                if aid1.isspace():
                    author1 = 'None'
                else:
                    try:
                        # author1 = Author.get(author_id=aid1)
                        aid1 = str(int(float(aid1)))
                        author1 = Author.get(author_id=aid1)._pk
                    except Exception:
                        author1 = 'None'

                if aid2.isspace():
                    author2 = 'None'
                else:
                    try:
                        aid2 = str(int(float(aid2)))
                        author2 = Author.get(author_id=aid2)._pk
                    except Exception:
                        author2 = 'None'

                if aid3.isspace():
                    author3 = 'None'
                else:
                    try:
                        aid3 = str(int(float(aid3)))
                        author3 = Author.get(author_id=aid3)._pk
                    except Exception:
                        author3 = 'None'

                if tid1.isspace():
                    tag1 = 'None'
                else:
                    try:
                        tid1 = str(int(float(tid1)))
                        tag1 = Tag.get(tag_id=tid1)._pk
                    except Exception:
                        tag1 = 'None'

                if tid2.isspace():
                    tag2 = 'None'
                else:
                    try:
                        tid2 = str(int(float(tid2)))
                        tag2 = Tag.get(tag_id=tid2)._pk
                    except Exception:
                        tag2 = 'None'

                if tid3.isspace():
                    tag3 = 'None'
                else:
                    try:
                        tid3 = str(int(float(tid3)))
                        tag3 = Tag.get(tag_id=tid3)._pk
                    except Exception:
                        tag3 = 'None'

                if tid4.isspace():
                    tag4 = 'None'
                else:
                    try:
                        tid4 = str(int(float(tid4)))
                        tag4 = Tag.get(tag_id=tid4)._pk
                    except Exception:
                        tag4 = 'None'

                if tid5.isspace():
                    tag5 = 'None'
                else:
                    try:
                        tid5 = str(int(float(tid5)))
                        tag5 = Tag.get(tag_id=tid5)._pk
                    except Exception:
                        tag5 = 'None'

                book = Book(
                    sk_book_id=sk_book_id, book_id=book_id, best_book_id=best_book_id, work_id=work_id, \
                    books_count=books_count, isbn=isbn, original_publication_year=original_publication_year, \
                    original_title=original_title, title=title, language_code=language_code, \
                    average_rating=average_rating, ratings_count=ratings_count, \
                    work_ratings_count=work_ratings_count, \
                    work_text_reviews_count=work_text_reviews_count, \
                    author1=author1, author2=author2, author3=author3, \
                    tag1=tag1, tag2=tag2, tag3=tag3, tag4=tag4, tag5=tag5
                )

                # print(book.hmget_dict('book_id', 'author_id', 'title'))
    except Exception as e:
        print(e)


def input_ratings(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                b_id, u_id, rating = line.split(',')
                u_id = u_id.strip()
                b_id = b_id.strip()
                rating = rating.strip()

                try:
                    user_id = User.get(user_id=u_id)
                except Exception:
                    user_id = 'None'

                try:
                    book_id = Book.get(sk_book_id=b_id)
                except Exception:
                    book_id = 'None'

                Rating(user_id=user_id, book_id=book_id, rating=rating)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    input_authors(authors_path)
    input_tags(tags_path)
    input_users(users_path)
    input_books(books_path)
    input_ratings(ratings_path)



# to run in terminal, use:
# export PYTHONIOENCODING=utf-8
