from mib import db 

class Report(db.Model):

    __tablename__ = "Report"

    # id_message is the primary key that identify a report
    id_report = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # id of reported and signaller
    id_reported = db.Column(db.Integer)
    id_signaller = db.Column(db.Integer)

    date_of_report = db.Column(db.DateTime)

    # constructor of the report object
    def __init__(self, *args, **kw):
        super(Report, self).__init__(*args, **kw)
