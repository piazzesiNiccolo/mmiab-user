import re
from flask.signals import message_flashed
from mock.mock import MagicMock, Mock
import pytest
import mock
import datetime
from mib import db
from mib.models.user import User
from mib.models.report import Report
from mib.dao.user_manager import UserManager
from mib.dao.user_reports import UserReport
class TestReportUsers:

    def test_report_same_id_forbidden(self):
        code, message = UserReport.add_report(1,1)
        assert code == 403
        assert message == "Users cannot report themselves"
    def test_report_reported_does_not_exists(self):
        code, message = UserReport.add_report(1,2)
        assert code == 404
        assert message == "Reported user not found"
    
    def test_report_reporter_does_not_exists(self):
        user = User(
        first_name='Niccolò',
        last_name='Piazzesi',
        email='email@email.com',
        phone='38217192937',
        birthdate=datetime.datetime.strptime("01/01/2000","%d/%m/%Y")
        )
        db.session.add(user)
        code, message = UserReport.add_report(1,2)
        assert code == 404
        assert message == "User not found"
        db.session.delete(user)
        db.session.commit()
    
    def test_report_user_already_reported(self):
        report = Report(
            id_reported=1,
            id_signaller=2
        )
        db.session.add(report)
      
        real = UserManager
        real.retrieve_by_id = MagicMock()
        real.retrieve_by_id.return_value = "ff"
        code, message = UserReport.add_report(1,2)
        assert code == 200
        assert message == "You have already reported this user"
        db.session.delete(report)
        db.session.commit()

    def test_report_user_ok(self):
        real = UserManager
        real.retrieve_by_id = MagicMock()
        real.retrieve_by_id.return_value = "ff"
        code, message = UserReport.add_report(1,2)
        assert code == 201
        assert message == "User succesfully reported"
    
    def test_report_trigger_ban(self):
        user = User(
        first_name='Niccolò',
        last_name='Piazzesi',
        email='email@email.com',
        phone='38217192937',
        birthdate=datetime.datetime.strptime("01/01/2000","%d/%m/%Y")
        )
        db.session.add(user)
        real = UserManager
        real.retrieve_by_id = MagicMock()
        real.retrieve_by_id.return_value = "ff"
        for i in range(2, 12):
            UserReport.add_report(1, i)
        assert user.is_banned
        db.session.delete(user)
        db.session.commit()