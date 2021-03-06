#!/user/bin/python
# -*- coding: utf-8 -*-`

from google.appengine.ext import ndb
import utils
from . import User
import endpoints
import msgs


class Grid(ndb.Model):
    """10x10 grid representational model"""

    # user to which this grid belongs to
    user = ndb.KeyProperty(required=True, kind='User')

    # Note:
    # a single square on the grid is denoted as a cap letter and a number(size two). e.g. A0, J9, C3
    # Letters range - [A-J] and numbers range - [0-9]

    # a string property to store the position of fleet efficiently(instead of using array)
    # a ships is encoded as a list of square denotion and separated by a pipe symbol
    # e.g. a destroyer of length two can be marked as A0B0;
    # thus a series of seven ships(total strength of fleet) can be denoted as (from larger to smaller)
    # B0B1B2B3B4|F0F1F2F3|I0I1I2|J0J1|J8J9|H4|C5
    # -->
    # (carrier, battleship, cruiser, two of destroyers, two of submarines)
    fleets = ndb.StringProperty(required=True, indexed=False)  # type:str

    # to hold a list of shots made by the opponent
    shots = ndb.StringProperty(indexed=False, default="")  # type:str
    shotResps = ndb.TextProperty(indexed=False, default="")  # type:str

    @classmethod
    def create(cls, user_name, carrier, battleship, cruiser, destroyer1, destroyer2, submarine1, submarine2):
        """
            create a new grid and refer to the given user
        Args:
            user_name (str): user

            All of the following specifies start point and alignment of ships. e.g. A9V, B7H.
            For more details see utils.getShipDenotation method
                carrier (str):
                battleship (str):
                cruiser (str):
                destroyer1 (str):
                destroyer2 (str):
                submarine1 (str):
                submarine2 (str):

        Returns:
            Grid: return the new grid

        Raises:
            endpoints.NotFoundException: when the given user name not found in the database
            ValueError: when the given arguments fail to meet requirements
            endpoints.ConflictException: when any of the ships position overlaps
        """

        user = User.get_by_name(user_name)

        fleet = [utils.getAShip(carrier, 5),
                 utils.getAShip(battleship, 4),
                 utils.getAShip(cruiser, 3),
                 utils.getAShip(destroyer1, 2), utils.getAShip(destroyer2, 2),
                 utils.getAShip(submarine1, 1), utils.getAShip(submarine2, 1)]
        # check for any overlap in the ship positions
        if len(utils.getShipsFromNotation("".join(fleet))[0]) != 18:
            raise endpoints.ConflictException("Ships position on the grid must not overlap")
        grid = Grid(user=user.key, fleets="|".join(fleet))
        grid.put()
        return grid

    def recordNewShot(self, shot):
        """
            update the shots field with the point and notify the result
        Args:
            shot (str): new shot/guess as a square denotation [e.g. A0, C7 ...]

        Returns:
            str: one of 'HIT' or 'MISS' or 'SUNK' or 'SUNK_ALL'
        """

        resp = utils.reflectAShot(self.fleets, self.shots, shot)
        # record the new shot
        self.shots += shot
        self.shotResps += resp + "|"
        self.put()
        return resp

    def toForm(self):
        return msgs.GridInfo(user=self.user.get().name, grid=self.fleets)

    def getHistory(self):
        shots = [self.shots[i:i + 2] for i in range(0, len(self.shots), 2)]
        resps = self.shotResps.split("|")
        return msgs.GridHistory(user=self.user.get().name,
                                shots=[msgs.GridShot(shot=shot[0], msg=shot[1]) for shot in zip(shots, resps)])
