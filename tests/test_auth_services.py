

class TestAuthServices:

    def test_authenticate_user_not_exists(self, test_client, mock_rbe):
        json = {
            "email": "email@email.com",
            "password" : "pass"
        }
        mock_rbe.return_value = None
        resp = test_client.post("/authenticate", json=json)
        assert resp.json["user"] is None
        assert resp.status_code == 401
    
    def test_authenticate_user_exists(self, test_client, mock_rbe,users):
        json = {
            "email": "email@email.com",
            "password" : "pass"
        }
        mock_rbe.return_value = users[0]
        resp = test_client.post("/authenticate", json=json)
        assert resp.json["authentication"] == "success"
        assert resp.json["user"]["email"] == "email@email.com"
        assert resp.status_code == 200