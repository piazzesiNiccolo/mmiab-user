from mib import db 
from mib.dao.user_manager import UserManager
from mib.models.user import User 
from mib.models.report import Report
import datetime
class UserReport:
    """
    Wrapper class  for all db operations involving report
    """

    # add a report and return a number of report of the reported user
    def add_report(id_reported, id_signaller):
        if UserManager.retrieve_by_id(id_reported) is None:
            return 404, "Reported user not found"
        elif UserManager.retrieve_by_id(id_signaller) is None:
            return 404, "User not found"
        # check if the signaller has already report the user
        elif (
            UserReport.is_user_reported(id_signaller,id_reported)
        ):
            return 200, "You have already reported this user"
        else:
            # add into the database the new Report
            db.session.add(
                Report(
                    id_reported=id_reported,
                    id_signaller=id_signaller,
                    date_of_report=datetime.datetime.now(),
                )
            )
            db.session.commit()

            count = (
                db.session.query(Report)
                .filter(Report.id_reported == id_reported)
                .count()
            )

            if count == 10:
                db.session.query(User).filter(User.id == id_reported).update(
                    {User.is_banned: True}
                )
            return 201, "User succesfully reported"

    def is_user_reported(current_id, other_id):
        return (
            db.session.query(Report)
            .filter(Report.id_reported == other_id, Report.id_signaller == current_id)
            .count()
        ) == 1