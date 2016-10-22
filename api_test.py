"""
a set of methods to test endpoints APIs.
"""

import api
import containers
import msgs
import unittest
import models
from google.appengine.ext import testbed
from google.appengine.ext import ndb


class TestBattleShipApi(unittest.TestCase):
    def setUp(self):
        self.tb = testbed.Testbed()
        self.tb.activate()
        self.tb.init_datastore_v3_stub()
        self.tb.init_memcache_stub()
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.tb.deactivate()

    def testDbCreateUser(self):
        models.User.create("user_1", "email@domain.com")
        models.User.create("user_2", "email2@domain.com")
        models.User.create("user_3", "email3@domain.com")
        models.User.create("user_nm")
        self.assertEqual(4, len(models.User.query().fetch()))

    def testApiCreateUser(self):
        btApi = api.BattleShipApi()
        req = api.BattleShipApi.create_user.remote.request_type(user_name="user_1")
        resp = btApi.create_user(req)
        assert resp.msg == "User user_1 created!"

        req = api.BattleShipApi.create_user.remote.request_type(user_name="user_2", email="user2@domain.com")
        resp = btApi.create_user(req)
        assert resp.msg == "User user_2 created!"

    def testApiCreateGame(self):
        self.testDbCreateUser()
        btApi = api.BattleShipApi()
        carrier = msgs.ShipPoint(x=1, y=msgs.Yrange.A)
        battleship = msgs.ShipPoint(x=1, y=msgs.Yrange.B)
        cruiser = msgs.ShipPoint(x=1, y=msgs.Yrange.C)
        destroyer1 = msgs.ShipPoint(x=1, y=msgs.Yrange.D)
        destroyer2 = msgs.ShipPoint(x=1, y=msgs.Yrange.E)
        submarine1 = msgs.ShipPoint(x=1, y=msgs.Yrange.F)
        submarine2 = msgs.ShipPoint(x=1, y=msgs.Yrange.G)

        leftGrid = msgs.Grid(user_name="user_1",
                             carrier=carrier,
                             battleship=battleship,
                             cruiser=cruiser,
                             destroyer1=destroyer1,
                             destroyer2=destroyer2,
                             submarine1=submarine1,
                             submarine2=submarine2)
        rightGrid = msgs.Grid(user_name="user_2",
                              carrier=carrier,
                              battleship=battleship,
                              cruiser=cruiser,
                              destroyer1=destroyer1,
                              destroyer2=destroyer2,
                              submarine1=submarine1,
                              submarine2=submarine2)
        req = api.BattleShipApi.new_game.remote.request_type(right=rightGrid, left=leftGrid)
        resp = btApi.new_game(req)
        assert resp.left == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'
        assert resp.right == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'
        return resp

    def testApiGetGame(self):
        aGame = self.testApiCreateGame()
        btApi = api.BattleShipApi()
        req = api.BattleShipApi.get_game.remote.request_type(url_key=aGame.urlsafe_key)
        resp = btApi.get_game(req)
        assert resp.left == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'
        assert resp.right == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'

    def testApiShoot(self):
        aGame = self.testApiCreateGame()
        btApi = api.BattleShipApi()

        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=1, y=msgs.Yrange.A,
                                                                player=msgs.Player.LEFT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=2, y=msgs.Yrange.A,
                                                                player=msgs.Player.RIGHT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=3, y=msgs.Yrange.A,
                                                                player=msgs.Player.LEFT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=4, y=msgs.Yrange.A,
                                                                player=msgs.Player.RIGHT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=5, y=msgs.Yrange.A,
                                                                player=msgs.Player.LEFT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')

        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=1, y=msgs.Yrange.A,
                                                                player=msgs.Player.RIGHT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=2, y=msgs.Yrange.A,
                                                                player=msgs.Player.LEFT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=3, y=msgs.Yrange.A,
                                                                player=msgs.Player.RIGHT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'HIT')
        # shot
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=4, y=msgs.Yrange.A,
                                                                player=msgs.Player.LEFT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'SUNK')
        # shot will sink a ship
        req = api.BattleShipApi.play_a_shot.remote.request_type(url_key=aGame.urlsafe_key, x=5, y=msgs.Yrange.A,
                                                                player=msgs.Player.RIGHT)
        resp = btApi.play_a_shot(req)
        self.assertEqual(resp.result, 'SUNK')
