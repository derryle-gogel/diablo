"""
Copyright ©2020. The Regents of the University of California (Regents). All Rights Reserved.

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

from datetime import datetime

from diablo import db, std_commit
from diablo.lib.util import to_isoformat


class Scheduled(db.Model):
    __tablename__ = 'scheduled'

    section_id = db.Column(db.Integer, nullable=False, primary_key=True)
    term_id = db.Column(db.Integer, nullable=False, primary_key=True)
    location = db.Column(db.String(255), db.ForeignKey('rooms.location'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, section_id, term_id, location):
        self.section_id = section_id
        self.term_id = term_id
        self.location = location

    def __repr__(self):
        return f"""<Approval
                    section_id={self.section_id},
                    term_id={self.term_id},
                    location={self.location}
                    created_at={self.created_at}>
                """

    @classmethod
    def create(cls, section_id, term_id, location):
        db.session.add(cls(section_id=section_id, term_id=term_id, location=location))
        std_commit()

    @classmethod
    def get_all_scheduled(cls, term_id):
        return cls.query.filter_by(term_id=term_id).all()

    @classmethod
    def was_scheduled(cls, section_id, term_id):
        return cls.query.filter_by(section_id=section_id, term_id=term_id).first() is not None

    def to_api_json(self):
        return {
            'sectionId': self.section_id,
            'termId': self.term_id,
            'location': self.location,
            'createdAt': to_isoformat(self.created_at),
        }
