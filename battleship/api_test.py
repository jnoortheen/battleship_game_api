"""
a set of methods to test endpoints APIs.
"""

import api
import msgs
import unittest
import models
from google.appengine.ext import testbed, ndb
from google.appengine.api import mail


class TestBattleShipApi(unittest.TestCase):
    def setUp(self):
        self.tb = testbed.Testbed()
        self.tb.activate()
        self.tb.init_datastore_v3_stub()
        self.tb.init_memcache_stub()
        self.tb.init_mail_stub()
        ndb.get_context().clear_cache()
        self.mailStub = self.tb.get_stub(testbed.MAIL_SERVICE_NAME)

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

    def testApiCreateGame(self, createUser=True):
        if createUser: self.testDbCreateUser()
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
        assert resp.left.grid == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'
        assert resp.right.grid == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'
        return resp

    def testApiGetGame(self):
        aGame = self.testApiCreateGame()
        btApi = api.BattleShipApi()
        req = api.BattleShipApi.get_game.remote.request_type(url_key=aGame.urlsafe_key)
        resp = btApi.get_game(req)
        assert resp.left.grid == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'
        assert resp.right.grid == 'A0A1A2A3A4|B0B1B2B3|C0C1C2|D0D1|E0E1|F0|G0'

    def testApiGetUserGames(self):
        self.testApiCreateGame()
        self.testApiCreateGame(False)
        self.testApiCreateGame(False)
        btApi = api.BattleShipApi()
        req = api.BattleShipApi.get_user_games.remote.request_type(user_name='user_3')
        resp = btApi.get_user_games(req)
        assert len(resp.games) == 0
        req = api.BattleShipApi.get_user_games.remote.request_type(user_name='user_1')
        resp = btApi.get_user_games(req)
        assert len(resp.games) == 3
        req = api.BattleShipApi.get_user_games.remote.request_type(user_name='user_2')
        resp = btApi.get_user_games(req)
        assert len(resp.games) == 3

    def testApiGetUserRanks(self):
        self.testApiCreateGame()
        self.testApiCreateGame(False)
        self.testApiCreateGame(False)
        btApi = api.BattleShipApi()
        req = api.BattleShipApi.get_user_rankings.remote.request_type()
        resp = btApi.get_user_rankings(req)
        print resp

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

        req = api.BattleShipApi.get_game_history.remote.request_type(url_key=aGame.urlsafe_key)
        resp = btApi.get_game_history(req)
        print resp

    def testEmail(self):
        mail.send_mail(to="jnoortheen@gmail.com", subject="test", body="testbody", sender="jnoortheen@gmail.com")
        messages = self.mailStub.get_sent_messages(to='jnoortheen@gmail.com')
        print messages
