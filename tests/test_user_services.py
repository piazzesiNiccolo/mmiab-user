import mock
import pytest


class TestUserServices:
    def test_create_user_already_exists(self, users, test_client, mock_rbe):
        mock_rbe.return_value = users[0]
        data = {
            "email": "email@email.com",
            "first_name": "Niccolò",
            "last_name": "Piazzesi",
            "phone": "1234567890",
            "birthdate": "01/01/2000",
            "location": "Faella",
            "nickname": "npiazzesi",
            "password": "password12",
        }
        resp = test_client.post("/user", json=data)
        assert resp.json["status"] == "Already present"
        assert resp.status_code == 200

    def test_create_user_ok(self, test_client, users, mock_rbe):

        mock_rbe.return_value = None
        data = {
            "email": "email@email.com",
            "first_name": "Niccolò",
            "last_name": "Piazzesi",
            "phone": "1234567890",
            "birthdate": "01/01/2000",
            "location": "Faella",
            "nickname": "npiazzesi",
            "password": "password12",
            "profile_picture": {
                "name": "test.png",
                "data": "",
            },
        }
        with mock.patch("mib.dao.user_manager.UserManager.create_user") as create_m:
            with mock.patch("mib.dao.utils.Utils.load_profile_picture") as load_m:
                with mock.patch("mib.dao.utils.Utils.save_profile_picture") as save_m:
                    create_m.return_value == users[0]
                    save_m.return_value = "default.png"
                    load_m.return_value = ""
                    resp = test_client.post("/user", json=data)
                    assert resp.json["status"] == "success"
                    assert resp.json["message"] == "User successfully registered"
                    assert resp.json["user"]["email"] == data["email"]
                    assert resp.status_code == 201

    def test_delete_user_not_exists(self, test_client, mock_rbi):
        mock_rbi.return_value = None
        resp = test_client.delete("/user/1")
        assert resp.json["status"] == "failed"
        assert resp.status_code == 404

    def test_delete_user_exists(self, test_client, mock_rbi):
        mock_rbi.return_value = 1
        with mock.patch("mib.dao.user_manager.UserManager.delete_user") as m:
            m.return_value = None
            resp = test_client.delete("/user/1")
            assert resp.json["status"] == "success"
            assert resp.json["message"] == "Successfully deleted"
            assert resp.status_code == 202

    def test_get_user_by_id_not_exists(self, test_client, mock_rbi):
        mock_rbi.return_value = None
        resp = test_client.get("/user/1")
        assert resp.json["status"] == "User not present"
        assert resp.status_code == 404

    def test_get_user_by_id_exists(self, test_client, mock_rbi, users):
        mock_rbi.return_value = users[0]
        resp = test_client.get("/user/1")
        assert resp.json["user"]["email"] == "email@email.com"
        assert resp.status_code == 200

    def test_get_user_by_email_not_exists(self, test_client, mock_rbe):
        mock_rbe.return_value = None
        resp = test_client.get("/user_email/email@email.com")
        assert resp.json["status"] == "User not present"
        assert resp.status_code == 404

    def test_get_user_by_email_exists(self, test_client, mock_rbe, users):
        mock_rbe.return_value = users[0]
        resp = test_client.get("/user_email/email@email.com")
        assert resp.json["user"]["email"] == "email@email.com"
        assert resp.status_code == 200

    def test_users_list_id_not_exists(self, test_client, mock_rbi):
        mock_rbi.return_value = None
        resp = test_client.get("/users_list/1")
        assert resp.json["status"] == "failed"
        assert resp.status_code == 404

    def test_users_list(self, test_client, users):
        resp = test_client.get("users_list/1")
        assert resp.json["status"] == "success"
        assert resp.json["users"][0]["email"] == "email@email.com"
        assert resp.status_code == 200

    def test_get_blacklist_id_not_exists(self, test_client, mock_rbi):
        mock_rbi.return_value = None
        resp = test_client.get("/blacklist/1")
        assert resp.json["status"] == "failed"
        assert resp.status_code == 404

    def test_get_blacklist(self, test_client, users):
        with mock.patch("mib.dao.user_blacklist.UserBlacklist.get_blocked_users") as m:
            m.return_value = users[1:]
            resp = test_client.get("blacklist/1")
            assert resp.json["status"] == "success"
            assert resp.json["users"][0]["email"] == "email1@email1.com"
            assert resp.status_code == 200

    def test_get_blacklist(self, test_client, users):
        with mock.patch("mib.dao.user_blacklist.UserBlacklist.get_blocked_users") as m:
            m.return_value = users[1:]
            resp = test_client.get("blacklist/1")
            assert resp.json["status"] == "success"
            assert resp.json["users"][0]["email"] == "email1@email1.com"
            assert resp.status_code == 200

    def test_enable_filter_user_not_exists(self, test_client):
        with mock.patch("mib.dao.user_manager.UserManager.set_content_filter") as m:
            m.return_value = -1
            resp = test_client.get("/content_filter/1")
            assert resp.json["status"] == "failed"
            assert resp.status_code == 404

    @pytest.mark.parametrize(
        "filter_val,code, status, value",
        [(True, 200, "success", True), (False, 200, "success", False)],
    )
    def test_enable_filter_toggle_on(
        self, test_client, filter_val, code, status, value, users
    ):
        with mock.patch("mib.dao.user_manager.UserManager.set_content_filter") as m:
            m.return_value = filter_val
            resp = test_client.get("/content_filter/1")
            assert resp.json["status"] == status
            assert resp.json["value"] == value
            assert resp.status_code == code

    @pytest.mark.parametrize(
        "filter,code, mess",
        [(None, 404, "failed"), (True, 200, "success"), (False, 200, "success")],
    )
    def test_get_content_filter(self, test_client, filter, code, mess):
        with mock.patch(
            "mib.dao.user_manager.UserManager.get_toggle_content_filter"
        ) as m:
            m.return_value = filter
            resp = test_client.get("/user/filter_value/1")
            assert resp.status_code == code
            assert resp.json["status"] == mess

    @pytest.mark.parametrize(
        "user, code, status", [(1, 200, "success"), (10, 404, "failed")]
    )
    def test_get_recipients(self, test_client, users, user, code, status):
        resp = test_client.get(f"/recipients/{user}")
        assert resp.status_code == code
        assert resp.json["status"] == status

    def test_get_display_info(self, test_client, users):
        resp = test_client.get("/users/display_info?ids=1,2")
        assert resp.status_code == 200
        assert len(resp.json["users"]) == 2

    @pytest.mark.parametrize(
        "add_ret_code,add_ret_mess, expected_mess,expected_code",
        [
            (403, "Users cannot block themselves", "failed", 403),
            (404, "Blocking user not found", "failed", 404),
            (404, "Blocked user not found", "failed", 404),
            (201, "User added to blacklist", "success", 201),
        ],
    )
    def test_add_to_blacklist(
        self, test_client, add_ret_code, add_ret_mess, expected_mess, expected_code
    ):
        with mock.patch(
            "mib.dao.user_blacklist.UserBlacklist.add_user_to_blacklist"
        ) as m:
            m.return_value = add_ret_code, add_ret_mess
            resp = test_client.put("/blacklist/1/2")
            assert resp.json["status"] == expected_mess
            assert resp.status_code == expected_code

    @pytest.mark.parametrize(
        "del_ret_code,del_ret_mess, expected_mess",
        [
            (404, "Blocking user not found", "failed"),
            (404, "Blocked user not found", "failed"),
            (200, "User removed from blacklist", "success"),
        ],
    )
    def test_remove_from_blacklist(
        self, test_client, del_ret_code, del_ret_mess, expected_mess
    ):
        with mock.patch(
            "mib.dao.user_blacklist.UserBlacklist.remove_user_from_blacklist"
        ) as m:
            m.return_value = del_ret_code, del_ret_mess
            resp = test_client.delete("/blacklist/1/2")
            assert resp.json["status"] == expected_mess
            assert resp.status_code == del_ret_code

    @pytest.mark.parametrize(
        "code_rep, mess_rep,status",
        [
            (404, "User not found", "failed"),
            (404, "Reported user not found", "failed"),
            (403, "Users cannot report themselves", "failed"),
            (200, "You have already reported this user", "failed"),
            (201, "User succesfully reported", "success"),
        ],
    )
    def test_report(self, test_client, code_rep, mess_rep, status):
        with mock.patch("mib.dao.user_reports.UserReport.add_report") as m:
            m.return_value = code_rep, mess_rep
            resp = test_client.put("/report/1/1")
            assert resp.json["status"] == status
            assert resp.json["message"] == mess_rep
            assert resp.status_code == code_rep

    @pytest.mark.parametrize(
        "report_status, blocked_status",
        [(True, True), (True, False), (False, True), (False, False)],
    )
    def test_user_status(self, test_client, report_status, blocked_status):
        with mock.patch("mib.dao.user_blacklist.UserBlacklist.is_user_blocked") as m:
            with mock.patch("mib.dao.user_reports.UserReport.is_user_reported") as m2:
                m.return_value = blocked_status
                m2.return_value = report_status
                resp = test_client.get("/user_status/1/2")
                assert resp.json["status"] == "success"
                assert resp.json["blocked"] == blocked_status
                assert resp.json["reported"] == report_status
                assert resp.status_code == 200

    def test_update_user_not_exists(self, test_client):
        resp = test_client.put("/user/1")
        assert resp.status_code == 404

    def test_update_not_unique_phone(self, test_client, users, mock_rbp):
        data = {"phone": "1234567890", "nickname": "npiazzesi"}
        mock_rbp.return_value = 1
        resp = test_client.put("/user/1", json=data)
        assert resp.json["message"] == "Phone already used"
        assert resp.status_code == 400

    def test_update_not_unique_email(self, test_client, users, mock_rbe):
        data = {
            "email": "email1@email1.com",
            "first_name": "Niccolò",
            "last_name": "Piazzesi",
            "phone": "12302847890",
            "birthdate": "01/01/2000",
            "location": "Faella",
            "nickname": "npiazzesi",
            "password": "password12",
        }
        mock_rbe.return_value = 1
        resp = test_client.put("/user/1", json=data)
        assert resp.json["message"] == "Email already used"
        assert resp.status_code == 400

    def test_update_incorrect_old_password(self, test_client, users):
        data = {"old_password": "password1232"}
        with mock.patch("mib.models.user.User.check_password") as m:
            m.return_value = False
            resp = test_client.put("/user/1", json=data)
            assert resp.json["message"] == "Password incorrect"
            assert resp.status_code == 200

    def test_update_no_old_password(self, test_client, users):
        data = {"first_name": "Marco", "birthdate": "01/01/1992"}
        with mock.patch("mib.dao.user_manager.UserManager.update_user") as m:
            m.return_value == None
            resp = test_client.put("/user/1", json=data)
            assert resp.json["status"] == "failed"
            assert resp.status_code == 200

    def test_update_user_ok(self, test_client, users):

        data = {
            "first_name": "Giovanni",
            "old_password": "pass",
            "new_password": "password34",
            "birthdate": "01/01/1993",
            "profile_picture": {
                "name": "new_propic.png",
                "data": "",
            },
        }
        with mock.patch("mib.dao.user_manager.UserManager.update_user") as update_m:
            with mock.patch("mib.dao.utils.Utils.save_profile_picture") as save_m:
                with mock.patch("mib.dao.utils.Utils.load_profile_picture") as load_m:
                    update_m.return_value == None
                    save_m.return_value = "new_propic.png"
                    load_m.return_value = ""
                    resp = test_client.put("/user/1", json=data)
                    assert resp.json["status"] == "success"
                    assert resp.status_code == 201

    def test_update_user_no_birthdate(self, test_client, users):

        data = {"first_name": "Luca", "old_password": "pass"}
        with mock.patch("mib.dao.user_manager.UserManager.update_user") as m:
            m.return_value == None
            resp = test_client.put("/user/1", json=data)
            assert resp.json["status"] == "success"
            assert resp.status_code == 201

    def test_update_user_no_propic(self, test_client, users):

        data = {
            "first_name": "Giovanni",
            "old_password": "pass",
            "new_password": "password34",
            "birthdate": "01/01/1993",
        }
        with mock.patch("mib.dao.user_manager.UserManager.update_user") as m:
            m.return_value == None
            resp = test_client.put("/user/1", json=data)
            assert resp.json["status"] == "success"
            assert resp.status_code == 201
