#!/user/bin/python
# -*- coding: utf-8 -*-`

"""
This module contains all Messages that are used as the endpoints request/response skeleton type.
"""
from protorpc import messages


class CreateUser(messages.Message):
    """define fields need to create a new user"""
    user_name = messages.StringField(1, required=True)
    email = messages.StringField(2)


class Player(messages.Enum):
    """two player game side """
    LEFT = 0
    RIGHT = 1


class ShootResult(messages.Enum):
    """shoot response message"""
    HIT = 0
    MISS = 1
    SUNK = 2
    SUNK_ALL = 3


class Yrange(messages.Enum):
    """attribute names are used for denoting a point in y axis"""
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9


class ShipPoint(messages.Message):
    class Align(messages.Enum):
        H = 1
        V = 2

    y = messages.EnumField(Yrange, 1, required=True)
    # values [1-10] are allowed
    x = messages.IntegerField(2, required=True)
    align = messages.EnumField(Align, 3, default='H')


class Shoot(messages.Message):
    # side of the player who is making this shoot
    player = messages.EnumField(Player, 1, required=True)
    y = messages.EnumField(Yrange, 2, required=True)
    # values [1-10] are allowed
    x = messages.IntegerField(3, required=True)


class ShootResp(messages.Message):
    result = messages.StringField(1, required=True)
    # if the current move makes the game finish, that means current player side has won.
    game_over = messages.BooleanField(2, default=False)


class Grid(messages.Message):
    """used to create a single grid model"""
    user_name = messages.StringField(1, required=True)
    carrier = messages.MessageField(ShipPoint, 2, required=True)  # type: ShipPoint
    battleship = messages.MessageField(ShipPoint, 3, required=True)  # type: ShipPoint
    cruiser = messages.MessageField(ShipPoint, 4, required=True)  # type: ShipPoint
    destroyer1 = messages.MessageField(ShipPoint, 5, required=True)  # type: ShipPoint
    destroyer2 = messages.MessageField(ShipPoint, 6, required=True)  # type: ShipPoint
    submarine1 = messages.MessageField(ShipPoint, 7, required=True)  # type: ShipPoint
    submarine2 = messages.MessageField(ShipPoint, 8, required=True)  # type: ShipPoint


class CreateGame(messages.Message):
    """used to create a battleship game"""
    left = messages.MessageField(Grid, 1, required=True)  # type: Grid
    right = messages.MessageField(Grid, 2, required=True)  # type: Grid


class GameFormResp(messages.Message):
    """resultant message shown after creating a battleship game record"""
    urlsafe_key = messages.StringField(1, required=True)
    game_over = messages.BooleanField(2, required=True)
    # list of ships position like
    # B0B1B2B3B4|F0F1F2F3|I0I1I2|J0J1|J8J9|H4|C5 representing
    # (carrier, battleship, cruiser, destroyer, destroyers, submarine, submarine)
    left = messages.StringField(3, required=True)
    right = messages.StringField(4, required=True)
    # if the game is over return the winner name
    winner = messages.StringField(5)


class GameFormRespColl(messages.Message):
    games = messages.MessageField(GameFormResp, 1, repeated=True)


class StringMessage(messages.Message):
    """string message"""
    msg = messages.StringField(1, required=True)
