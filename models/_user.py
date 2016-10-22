import endpoints
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()

    @classmethod
    def create(cls, username, email=None):
        user = User(name=username, email=email)
        user.put()

    @classmethod
    def get_by_name(cls, user_name):
        user = User.query(User.name == user_name).get()
        if not user: raise endpoints.NotFoundException("No user found with name {}".format(user_name))
        return user
