import endpoints
from google.appengine.ext import ndb
import msgs
import datetime


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

    def hasInactiveGames(self):
        """
            return  inactive games that the user is being part of
        Returns:
            bool: true or false
        """
        from . import BattleShip
        q = BattleShip.query(BattleShip.gameOver == False,
                             BattleShip.cancelled == False,
                             ndb.OR(BattleShip.leftPlayer == self.key, BattleShip.rightPlayer == self.key))

        for aGame in q:
            # if any of the user's game is not active for more than 1 hour
            if (datetime.datetime.now() - aGame.time_updated) > datetime.timedelta(hours=1):
                return True

        return False
