from limpyd import model, fields
from limpyd.contrib import related


class BaseModel(model.RedisModel):
    database = model.RedisDatabase(
        host="127.0.0.1",
        port=6379,
        db=0
    )
    abstract = True


class Author(BaseModel):
    author_id = fields.InstanceHashField(indexable=True)
    full_name = fields.InstanceHashField(indexable=True)


# class FakeBook(BaseModel):
#     database = model.RedisDatabase(
#         host="localhost",
#         port=6379,
#         db=0
#     )

#     book_id = fields.InstanceHashField(indexable=True)
#     author_id = related.FKInstanceHashField('Author', related_name='authors')
#     title = fields.InstanceHashField(indexable=True)

#     def hmget_dict(self, *args):
#         """
#         A call to hmget but which return a dict with field names as keys,
#         instead of only a list of values
#         """
#         values = self.hmget(*args)
#         keys = args or self._hashable_fields
#         return dict(zip(keys, values))


class Genre(BaseModel):
    genre_id = fields.InstanceHashField(indexable=True)
    name = fields.InstanceHashField(indexable=True)


class User(BaseModel):
    user_id = fields.InstanceHashField(indexable=True)
    full_name = fields.InstanceHashField(indexable=True)
    language = fields.InstanceHashField(indexable=True)


class Book(related.RelatedModel):
    database = model.RedisDatabase(
        host="localhost",
        port=6379,
        db=0
    )
    namespace = 'books'

    book_id = fields.InstanceHashField(indexable=True)
    best_book_id = fields.InstanceHashField(indexable=True)
    work_id = fields.InstanceHashField(indexable=True)
    genre_id = related.FKInstanceHashField('Genre', related_name='%(namespace)s_%(model)s_set')
    books_count = fields.InstanceHashField(indexable=True)
    original_title = fields.InstanceHashField(indexable=True)
    title = fields.InstanceHashField(indexable=True)
    author_id = related.FKInstanceHashField('Author', related_name='%(namespace)s_%(model)s_set')
    original_publication_year = fields.InstanceHashField(indexable=True)
    average_rating = fields.InstanceHashField(indexable=True)
    isbn = fields.InstanceHashField(indexable=True)
    isbn13 = fields.InstanceHashField(indexable=True)
    language_code = fields.InstanceHashField(indexable=True)
    num_pages = fields.InstanceHashField(indexable=True)
    ratings_count = fields.InstanceHashField(indexable=True)
    work_ratings_count = fields.InstanceHashField(indexable=True)
    work_text_reviews_count = fields.InstanceHashField(indexable=True)
    image_url = fields.InstanceHashField(indexable=True)

    def hmget_dict(self, *args):
        """
        A call to hmget but which return a dict with field names as keys,
        instead of only a list of values
        """
        values = self.hmget(*args)
        keys = args or self._hashable_fields
        return dict(zip(keys, values))


class Rating(related.RelatedModel):
    database = model.RedisDatabase(
        host="localhost",
        port=6379,
        db=0
    )
    namespace = 'ratings'

    rating_id = fields.InstanceHashField(indexable=True)
    user_id = related.FKInstanceHashField('User', related_name='%(namespace)s_%(model)s_set')
    book_id = related.FKInstanceHashField('Book', related_name='%(namespace)s_%(model)s_set')
