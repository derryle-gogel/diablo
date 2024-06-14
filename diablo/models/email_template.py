"""
Copyright ©2024. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""
from diablo import db, std_commit
from diablo.lib.util import to_isoformat
from diablo.models.base import Base
from sqlalchemy.dialects.postgresql import ENUM


email_template_type = ENUM(
    'admin_operator_requested',
    'changes_confirmed',
    'instructors_added',
    'instructors_removed',
    'new_class_scheduled',
    'no_longer_scheduled',
    'notify_instructor_of_changes',
    'opted_out',
    'remind_scheduled',
    'room_change_no_longer_eligible',
    'schedule_change',
    'semester_start',
    name='email_template_types',
    create_type=False,
)


class EmailTemplate(Base):
    __tablename__ = 'email_templates'

    id = db.Column(db.Integer, nullable=False, primary_key=True)  # noqa: A003
    template_type = db.Column(email_template_type, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)
    subject_line = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __init__(
            self,
            template_type,
            name,
            subject_line,
            message,
    ):
        self.template_type = template_type
        self.name = name
        self.subject_line = subject_line
        self.message = message

    def __repr__(self):
        return f"""<EmailTemplate
                    id={self.id},
                    template_type={self.template_type},
                    name={self.name},
                    subject_line={self.subject_line}
                    message={self.message}>
                """

    @classmethod
    def create(cls, template_type, name, subject_line, message):
        email_template = cls(
            template_type=template_type,
            name=name,
            subject_line=subject_line,
            message=message,
        )
        db.session.add(email_template)
        std_commit()
        return email_template

    @classmethod
    def delete_template(cls, template_id):
        db.session.delete(cls.query.filter_by(id=template_id).first())
        std_commit()

    @classmethod
    def get_template(cls, template_id):
        return cls.query.filter_by(id=template_id).first()

    @classmethod
    def get_template_by_type(cls, template_type):
        return cls.query.filter_by(template_type=template_type).first()

    @classmethod
    def get_all_templates_names(cls):
        return cls.query.with_entities(cls.id, cls.name).order_by(cls.name).all()

    @classmethod
    def all_templates(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def update(cls, template_id, template_type, name, subject_line, message):
        email_template = cls.query.filter_by(id=template_id).first()
        email_template.template_type = template_type
        email_template.name = name
        email_template.subject_line = subject_line
        email_template.message = message
        db.session.add(email_template)
        std_commit()
        return email_template

    @classmethod
    def get_template_type_options(cls):
        return {
            'admin_operator_requested': 'Admin alert: operator requested',
            'changes_confirmed': 'Changes confirmed',
            'instructors_added': 'Instructor(s) added to class',
            'instructors_removed': 'Instructor(s) removed from class',
            'new_class_scheduled': 'New class scheduled',
            'no_longer_scheduled': 'Class no longer scheduled',
            'notify_instructor_of_changes': 'Notify instructor of changes',
            'opted_out': 'Opted out',
            'remind_scheduled': 'Remind scheduled instructors',
            'room_change_no_longer_eligible': 'Room change: no longer eligible',
            'schedule_change': 'Schedule change',
            'semester_start': 'Semester start',
        }

    def to_api_json(self):
        return {
            'id': self.id,
            'templateType': self.template_type,
            'typeName': self.get_template_type_options()[self.template_type],
            'name': self.name,
            'subjectLine': self.subject_line,
            'message': self.message,
            'createdAt': to_isoformat(self.created_at),
            'updatedAt': to_isoformat(self.updated_at),
        }
