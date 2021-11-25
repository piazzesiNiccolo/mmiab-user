import mock
import pytest
from mib.dao.user_reports import UserReport
from mib.resources.users import *


class TestUserServices:

    def test_get_user_by_id_not_exists(self, test_client, mock_rbi):
        mock_rbi.return_value = None
        resp = test_client.get("/user/1")
        assert resp.json["status"] == "User not present"
        assert resp.status_code == 404
    
    def test_get_user_by_id_exists(self, test_client, mock_rbi,users):
        mock_rbi.return_value = users[0]
        resp = test_client.get("/user/1")
        assert resp.json["email"] == "email@email.com"
        assert resp.status_code == 200
    
    def test_get_user_by_email_not_exists(self, test_client, mock_rbe):
        mock_rbe.return_value = None
        resp = test_client.get("/user_email/email@email.com")
        assert resp.json["status"] == "User not present"
        assert resp.status_code == 404
    
    def test_get_user_by_email_exists(self, test_client, mock_rbe, users):
        mock_rbe.return_value = users[0]
        resp = test_client.get("/user_email/email@email.com")
        assert resp.json["email"] == "email@email.com"
        assert resp.status_code == 200
    
    def test_enable_filter_user_not_exists(self, test_client):
        with mock.patch('mib.dao.user_manager.UserManager.set_content_filter') as m:
            m.return_value = -1
            resp = test_client.get("/content_filter/1")
            assert resp.json["status"] == "failed"
            assert resp.status_code == 404
    
  
    @pytest.mark.parametrize("filter_val,code, status, value",[
        (True, 200, "Success", True),
        (False,200, "Success", False)]
        )
    def test_enable_filter_toggle_on(self, test_client, filter_val, code, status, value):
        with mock.patch('mib.dao.user_manager.UserManager.set_content_filter') as m:
            m.return_value = filter_val
            resp = test_client.get("/content_filter/1")
            assert resp.json["status"] == status
            assert resp.json["Value"] == value
            assert resp.status_code == code
    
    
    @pytest.mark.parametrize("add_ret_code,add_ret_mess, expected_mess,expected_code",[
        (403, "Users cannot block themselves", "failed", 403),
        (404, "Blocking user not found", "failed",404),
        (404,"Blocked user not found", "failed", 404),
        (201,"User added to blacklist", "success", 201)
    ] )
    def test_add_to_blacklist(self, test_client, add_ret_code,add_ret_mess,expected_mess,expected_code):
        with mock.patch("mib.dao.user_blacklist.UserBlacklist.add_user_to_blacklist") as m:
            m.return_value = add_ret_code, add_ret_mess
            resp = test_client.put("/blacklist/1/2")
            assert resp.json["status"] == expected_mess
            assert resp.status_code == expected_code
    
    @pytest.mark.parametrize("del_ret_code,del_ret_mess, expected_mess",[
        (404, "Blocking user not found", "failed"),
        (404,"Blocked user not found", "failed"),
        (200,"User removed from blacklist", "success")
    ] )
    def test_remove_from_blacklist(self, test_client, del_ret_code,del_ret_mess,expected_mess):
        with mock.patch("mib.dao.user_blacklist.UserBlacklist.remove_user_from_blacklist") as m:
            m.return_value = del_ret_code, del_ret_mess
            resp = test_client.delete("/blacklist/1/2")
            assert resp.json["status"] == expected_mess
            assert resp.status_code == del_ret_code
    
    @pytest.mark.parametrize("code_rep, mess_rep,status",[
        (404, "User not found", "failed"),
        (404,"Reported user not found", "failed"),
        (403, "Users cannot report themselves","failed"),
        (200, "You have already reported this user", "failed"),
        (201, "User succesfully reported", "success")
    ])
    def test_report(self, test_client, code_rep, mess_rep, status):
        with mock.patch("mib.dao.user_reports.UserReport.add_report") as m:
            m.return_value = code_rep, mess_rep
            resp = test_client.put("/report/1/1")
            assert resp.json['status'] == status
            assert resp.json['message'] == mess_rep
            assert resp.status_code == code_rep
    
    