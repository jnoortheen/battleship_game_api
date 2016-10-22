#!/user/bin/python
# -*- coding: utf-8 -*-`

"""
This module is used to define all API class methods
"""

import endpoints
from protorpc import remote
import models
import msgs
import containers
import logging


@endpoints.api("battle_ship_classic", version='v1')
class BattleShipApi(remote.Service):
    """
        set of classic battleship game backend APIs
    """

    @endpoints.method(request_message=containers.CreateUserReq,
                      response_message=msgs.StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, req):
        """
            Create a new user record if all requirements are satisfied
        Args:
            req (containers.CreateUserReq):
        Returns:
            msgs.StringMessage: user creation status
        Raises:
            endpoints.ConflictException: when duplicate user name is given
        """

        if models.User.query(models.User.name == req.user_name).get():
            raise endpoints.ConflictException('A User with that name already exists!')

        models.User.create(req.user_name, req.email)
        return msgs.StringMessage(msg="User {} created!".format(req.user_name))

    @endpoints.method(request_message=containers.CreateGameReq,
                      response_message=msgs.GameFormResp,
                      path='game',
                      name='create_game',
                      http_method='POST')
    def new_game(self, req):
        """
            create a new game and return the url for that
        Args:
            req (msgs.CreateGame): right and left grid params to creat a new game
        Returns:
            msgs.GameFormResp: Both side of fleet positions denoted as string
        Raises:
            endpoints.BadRequestException: when bad request is received
        """
        return models.BattleShip.create(req.left, req.right)

    @endpoints.method(request_message=containers.GetGameReq,
                      response_message=msgs.GameFormResp,
                      path='game/{url_key}',
                      name='get_game',
                      http_method='GET')
    def get_game(self, req):
        """
            get the game details by its url key
        Args:
            req (containers.GetGameReq):
        Returns:
            msgs.GameFormResp: Both side of fleet positions denoted as string
        """
        return models.BattleShip.getByUrlKey(req.url_key).toForm()

    @endpoints.method(request_message=containers.ShootReq,
                      response_message=msgs.ShootResp,
                      path='game/{url_key}',
                      name='shoot',
                      http_method='PUT')
    def play_a_shot(self, req):
        """
            shoot the opponents fleet. It must be called alternatively for each of the player
            until anyone of Players fleet is completely destroyed.
        Args:
            req (containers.ShootReq): Refer the class doc
        Returns:
            msgs.ShootResp: refer class doc of msgs.ShootResp
        """
        game = models.BattleShip.getByUrlKey(req.url_key)
        return game.shoot(str(req.player), (str(req.y) + str(req.x - 1)))

    @endpoints.method(request_message=containers.UserGamesReq,
                      response_message=msgs.,
                      path='user',
                      name='get_user_games',
                      http_method='GET')
    def get_user_games(self, req):
        """
            returns the list of game details that the user is being active participant of.
        Args:
            req (containers.UserGamesReq): contains the user name
        Returns:
            msgs.:
        """
        user = models.User.query(models.User.name == req.user_name).get()


api = endpoints.api_server([BattleShipApi])
