import pytest
import os
import mock
import io
import base64
from werkzeug.datastructures import FileStorage
from mib.dao.utils import Utils
from mib.models.user import User
from uuid import uuid4

class TestUtils:

    def test_load_propic_not_found(self):
        filename = str(uuid4()) + '.png'
        user = User(pfp_path=filename)
        propic = Utils.load_profile_picture(user)
        assert propic['name'] == filename
        assert propic['data'] == ''
        assert propic['type'] == 'png'

    def test_load_propic_ok(self):
        filename = 'default.png'
        user = User(pfp_path=filename)
        with mock.patch('os.path.join') as m:
            m.return_value = 'mib/static/assets/' + filename
            propic = Utils.load_profile_picture(user)
            assert propic['name'] == filename
            assert propic['type'] == 'png'

    def test_save_propic_empty(self):
        assert Utils.save_profile_picture('') == ''

    def test_save_propic_ok(self):
        filename = 'test.png'
        with mock.patch('os.path.join') as m:
            fake_path = 'mib/static/assets/' + filename
            m.return_value = fake_path
            name = Utils.save_profile_picture({'data': base64.b64encode(b'propic data').decode('utf-8'), 'name': filename})
            assert name.endswith(filename)
            with open(fake_path, 'rb') as file:
                assert file.read() == b'propic data'
            os.remove(fake_path)



