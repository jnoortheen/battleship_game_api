import endpoints
from google.appengine.ext import ndb
import msgs


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

    def getRank(self):
        """return the number of matches and winning details"""
        from . import BattleShip
        # search only the completed games
        q = BattleShip.query(BattleShip.gameOver == True, BattleShip.cancelled == False)
        matches = q.filter(ndb.OR(BattleShip.leftPlayer == self.key, BattleShip.rightPlayer == self.key)).count()
        wins = q.filter(ndb.OR(BattleShip.winner == self.key)).count()
        return msgs.UserRank(name=self.name, matches=matches, wins=wins)
