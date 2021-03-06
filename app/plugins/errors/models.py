"""Errors plugin models.py is the error table database handler."""
#  coding=utf-8
from app import db
from datetime import datetime
from app import YamlInfo


class Errors(db.Model):
    """HTTP Error Code Database Table."""

    __tablename__ = "errors"
    id = db.Column(db.Integer, primary_key=True)
    error_name = db.Column(db.String(128), index=True)
    error_message = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        """AUCR HTTP Error return self."""
        return '<Error {}>'.format(self.error_name)


def insert_initial_error_values(*args, **kwargs):
    """Insert HTTP error code default database values from a yaml template file."""
    run = YamlInfo("app/plugins/errors/errors.yml", "none", "none")
    error_data = run.get()
    for items in error_data:
        new_error_table_row = Errors(error_name=items, error_message=error_data[items]["message"])
        db.session.add(new_error_table_row)
        db.session.commit()


db.event.listen(Errors.__table__, 'after_create', insert_initial_error_values)
