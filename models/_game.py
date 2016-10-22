from google.appengine.ext import ndb
from . import Grid
import msgs
import utils
import endpoints


class BattleShip(ndb.Model):
    """Battleship Game model"""

    # two grids
    leftGrid = ndb.KeyProperty(required=True, kind=Grid)  # type:Grid
    rightGrid = ndb.KeyProperty(required=True, kind=Grid)  # type:Grid
    # once the game is over, fill up the winner details
    winner = ndb.KeyProperty(kind='User')
    gameOver = ndb.BooleanProperty(default=False)
    cancelled = ndb.BooleanProperty(default=False)

    @classmethod
    def getByUrlKey(cls, urlKey):
        """
            returns the game form after querying
        Args:
            urlKey (str): url safe key of self

        Returns:
            BattleShip: resultant game record

        Raises:
            endpoints.NotFoundException: when no game found for the url key
            endpoints.BadRequestException: when key is not valid
        """

        try:
            game = ndb.Key(urlsafe=urlKey).get()
            if not game:
                raise endpoints.NotFoundException("Game for the given key is not found")
            return game
        except TypeError:
            raise endpoints.BadRequestException('Invalid Key')
        except Exception, e:
            if e.__class__.__name__ == 'ProtocolBufferDecodeError':
                raise endpoints.BadRequestException('Invalid Key')
            else:
                raise

    @classmethod
    def create(cls, leftGridArgs, rightGridArgs):
        """
            create a new battleship game object
        Args:
            leftGridArgs (msgs.Grid): container of arguments to be passed on to create a GRID
            rightGridArgs (msgs.Grid):
        Returns:
            GameFormResp: return newly inserted record's form
        """

        leftGrid = Grid.create(leftGridArgs.user_name,
                               utils.shipPtToNotation(leftGridArgs.carrier),
                               utils.shipPtToNotation(leftGridArgs.battleship),
                               utils.shipPtToNotation(leftGridArgs.cruiser),
                               utils.shipPtToNotation(leftGridArgs.destroyer1),
                               utils.shipPtToNotation(leftGridArgs.destroyer2),
                               utils.shipPtToNotation(leftGridArgs.submarine1),
                               utils.shipPtToNotation(leftGridArgs.submarine2))

        rightGrid = Grid.create(rightGridArgs.user_name,
                                utils.shipPtToNotation(rightGridArgs.carrier),
                                utils.shipPtToNotation(rightGridArgs.battleship),
                                utils.shipPtToNotation(rightGridArgs.cruiser),
                                utils.shipPtToNotation(rightGridArgs.destroyer1),
                                utils.shipPtToNotation(rightGridArgs.destroyer2),
                                utils.shipPtToNotation(rightGridArgs.submarine1),
                                utils.shipPtToNotation(rightGridArgs.submarine2))

        game = BattleShip(leftGrid=leftGrid.key, rightGrid=rightGrid.key)
        game.put()
        return game.toForm()

    def toForm(self):
        """
            return message format of self
        Returns:
           GameFormResp: string repr of both side of fleets
        """
        game = msgs.GameFormResp(left=self.leftGrid.get().fleets,
                                 right=self.rightGrid.get().fleets,
                                 urlsafe_key=self.key.urlsafe(),
                                 game_over=self.gameOver)
        if self.gameOver:
            game.winner = self.winner.get().name
        return game

    def shoot(self, side, shot):
        """
            record a shot by a player to the opponent's grid and notify the result. If all the ships sunk, then
            notify the current side as the winner and mark the game as ended.
        Args:
            side (str): one of 'LEFT', 'RIGHT'
            shot (str): new shot/guess as a square denotation [e.g. A0, C7 ...]
        Returns:
            msgs.ShootResp
        """

        if side == 'LEFT':
            grid = self.rightGrid.get()  # type: Grid
            playerGrid = self.leftGrid.get()  # type: Grid
        else:
            grid = self.leftGrid.get()
            playerGrid = self.rightGrid.get()

        # enacting the rule that the user must play consecutively
        if abs(len(playerGrid.shots) - len(grid.shots)) > 2:
            raise endpoints.ConflictException("Users must play consecutively, one after another.")

        # record the shot to the opponents grid
        rslt = grid.recordNewShot(shot)
        # no need to check any other values as they are passed from enum types
        resp = msgs.ShootResp()
        resp.result = rslt

        if rslt == 'SUNK_ALL':
            resp.game_over = True
            self.gameOver = True
            self.winner = grid.user.get().key
            self.put()

        # return the response
        return resp
