from limpyd import model, fields
from limpyd.contrib import related
from limpyd.indexes import TextRangeIndex


class BaseModel(model.RedisModel):
    database = model.RedisDatabase(
        host="127.0.0.1",
        port=6379,
        db=0
    )
    abstract = True


class BaseRelatedModel(related.RelatedModel):
    database = model.RedisDatabase(
        host="localhost",
        port=6379,
        db=0
    )
    namespace = 'base'
    abstract = True


class Author(BaseModel):
    author_id = fields.InstanceHashField(indexable=True)
    full_name = fields.InstanceHashField(indexable=True)


class Tag(BaseModel):
    tag_id = fields.InstanceHashField(indexable=True)
    name = fields.InstanceHashField(indexable=True, indexes=[TextRangeIndex])
    # name = fields.InstanceHashField(indexable=True)

    def hmget_dict(self, *args):
        """
        A call to hmget but which return a dict with field names as keys,
        instead of only a list of values
        """
        values = self.hmget(*args)
        keys = args or self._hashable_fields
        return dict(zip(keys, values))


class User(BaseModel):
    user_id = fields.InstanceHashField(indexable=True)
    full_name = fields.InstanceHashField(indexable=True)
    gender = fields.InstanceHashField(indexable=True)
    language = fields.InstanceHashField(indexable=True)

    def hmget_dict(self, *args):
        """
        A call to hmget but which return a dict with field names as keys,
        instead of only a list of values
        """
        values = self.hmget(*args)
        keys = args or self._hashable_fields
        return dict(zip(keys, values))


class Book(BaseModel):
    sk_book_id = fields.InstanceHashField(indexable=True)
    book_id = fields.InstanceHashField(indexable=True)
    best_book_id = fields.InstanceHashField(indexable=True)
    work_id = fields.InstanceHashField(indexable=True)
    books_count = fields.InstanceHashField(indexable=True)
    isbn = fields.InstanceHashField(indexable=True)
    original_publication_year = fields.InstanceHashField(indexable=True, indexes=[TextRangeIndex])
    # original_publication_year = fields.InstanceHashField(indexable=True)
    original_title = fields.InstanceHashField(indexable=True)
    title = fields.InstanceHashField(indexable=True)
    language_code = fields.InstanceHashField(indexable=True)
    average_rating = fields.InstanceHashField(indexable=True)
    ratings_count = fields.InstanceHashField(indexable=True)
    work_ratings_count = fields.InstanceHashField(indexable=True)
    work_text_reviews_count = fields.InstanceHashField(indexable=True)

    def hmget_dict(self, *args):
        """
        A call to hmget but which return a dict with field names as keys,
        instead of only a list of values
        """
        values = self.hmget(*args)
        keys = args or self._hashable_fields
        return dict(zip(keys, values))


class Rating(BaseRelatedModel):
    namespace = 'ratings'

    user_id = related.FKInstanceHashField('User', related_name='%(namespace)s_%(model)s_set')
    book_id = related.FKInstanceHashField('Book', related_name='%(namespace)s_%(model)s_set')
    rating = fields.InstanceHashField(indexable=True)

    def hmget_dict(self, *args):
        """
        A call to hmget but which return a dict with field names as keys,
        instead of only a list of values
        """
        values = self.hmget(*args)
        keys = args or self._hashable_fields
        return dict(zip(keys, values))


class BooksTags(BaseRelatedModel):
    namespace = 'books_tags'

    sk_tag_id = related.FKInstanceHashField('Tag', related_name='%(namespace)s_%(model)s_set')
    sk_book_id = related.FKInstanceHashField('Book', related_name='%(namespace)s_%(model)s_set')
    count = fields.InstanceHashField(indexable=True)

    def hmget_dict(self, *args):
        """
        A call to hmget but which return a dict with field names as keys,
        instead of only a list of values
        """
        values = self.hmget(*args)
        keys = args or self._hashable_fields
        return dict(zip(keys, values))


class BooksAuthors(BaseRelatedModel):
    namespace = 'books_authors'

    sk_author_id = related.FKInstanceHashField('Author', related_name='%(namespace)s_%(model)s_set')
    sk_book_id = related.FKInstanceHashField('Book', related_name='%(namespace)s_%(model)s_set')
















