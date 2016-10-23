#!/usr/bin/env python

"""main.py - This file contains handlers that are called by cronjobs."""

import webapp2
from google.appengine.api import mail, app_identity
import models


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about their inactive and incomplete games.
        Called every hour using a cron job"""

        app_id = app_identity.get_application_id()
        users = models.User.query(models.User.email != None)
        for user in users:
            if user.hasInactiveGames():
                subject = 'Battleship Game reminder!'
                body = 'Hello {}, It seems like some of your games seems to be inactive for a while.'.format(user.name)
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email,
                               subject,
                               body)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail)
], debug=True)
