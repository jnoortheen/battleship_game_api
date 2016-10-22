#!/user/bin/python
# -*- coding: utf-8 -*-`

"""
This module contains all resource containers that are used for API requests.
"""
import endpoints
import msgs
from protorpc import messages

CreateUserReq = endpoints.ResourceContainer(msgs.CreateUser)
CreateGameReq = endpoints.ResourceContainer(msgs.CreateGame)
GetGameReq = endpoints.ResourceContainer(url_key=messages.StringField(1, required=True))
ShootReq = endpoints.ResourceContainer(msgs.Shoot, url_key=messages.StringField(1, required=True))
UserGamesReq = endpoints.ResourceContainer(user_name=messages.StringField(1, required=True))