import pytest
import mock
from mib.dao.user_reports import UserReport
from mib.resources.users import *
import requests
class TestUserServices:


    def test_report_404(self, test_client):
        rep = UserReport
        rep.add_report = mock.MagicMock()
        rep.add_report.return_value = 404, "User not found"
        resp = test_client.put("/report/1/1")
        assert resp.json['status'] == 'failed'
        assert resp.json['message'] == "User not found"
        assert resp.status_code == 404
    
    def test_report_403(self,test_client):
        rep = UserReport
        rep.add_report = mock.MagicMock()
        rep.add_report.return_value = 403, "Users cannot report themselves"
        resp = test_client.put("/report/1/1")
        assert resp.json['status'] == 'failed'
        assert resp.json['message'] == "Users cannot report themselves"
        assert resp.status_code == 403
    def test_report_200(self, test_client):
        rep = UserReport
        rep.add_report = mock.MagicMock()
        rep.add_report.return_value = 200, "You have already reported this user"
        resp = test_client.put("/report/1/1")
        assert resp.json['status'] == 'failed'
        assert resp.json['message'] == "You have already reported this user"
        assert resp.status_code == 200
    
    def test_report_201(self,test_client):
        rep = UserReport
        rep.add_report = mock.MagicMock()
        rep.add_report.return_value = 201, "User succesfully reported"
        resp = test_client.put("/report/1/1")
        assert resp.json['status'] == 'success'
        assert resp.json['message'] == "User succesfully reported"
        assert resp.status_code == 201