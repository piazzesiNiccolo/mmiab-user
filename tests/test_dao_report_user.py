from mib import db
from mib.dao.user_reports import UserReport
from mib.models.report import Report


class TestReportUsers:
    def test_report_same_id_forbidden(self):
        code, message = UserReport.add_report(1, 1)
        assert code == 403
        assert message == "Users cannot report themselves"

    def test_report_reported_does_not_exists(self):
        code, message = UserReport.add_report(1, 2)
        assert code == 404
        assert message == "Reported user not found"

    def test_report_reporter_does_not_exists(self, users):
        code, message = UserReport.add_report(1, 3)
        assert code == 404
        assert message == "User not found"

    def test_report_user_already_reported(self, mock_rbi):
        report = Report(id_reported=1, id_signaller=2)
        db.session.add(report)

        mock_rbi.return_value = "ff"
        code, message = UserReport.add_report(1, 2)
        assert code == 200
        assert message == "You have already reported this user"

        db.session.delete(report)
        db.session.commit()

    def test_report_user_ok(self, mock_rbi):
        mock_rbi.return_value = "ff"
        code, message = UserReport.add_report(1, 2)
        assert code == 201
        assert message == "User succesfully reported"

    def test_report_trigger_ban(self, users, mock_rbi):
        mock_rbi.return_value = "ff"
        for i in range(2, 12):
            UserReport.add_report(1, i)
        assert users[0].is_banned
