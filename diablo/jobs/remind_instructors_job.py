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
from diablo.jobs.base_job import BaseJob
from diablo.jobs.util import get_eligible_courses
from diablo.models.queued_email import remind_instructors_scheduled
from diablo.models.sis_section import AUTHORIZED_INSTRUCTOR_ROLE_CODES
from flask import current_app as app


class RemindInstructorsJob(BaseJob):

    def _run(self):
        term_id = app.config['CURRENT_TERM_ID']
        courses_by_instructor_uid = {}

        # Schedule recordings
        for course in get_eligible_courses(term_id):
            for instructor in list(filter(lambda i: i['roleCode'] in AUTHORIZED_INSTRUCTOR_ROLE_CODES, course['instructors'])):
                if instructor['uid'] not in courses_by_instructor_uid:
                    courses_by_instructor_uid[instructor['uid']] = {'instructor': instructor, 'courses': []}
                courses_by_instructor_uid[instructor['uid']]['courses'].append(course)

        # Queue semester start emails
        for uid, instructor_courses in courses_by_instructor_uid.items():
            remind_instructors_scheduled(instructor_courses['instructor'], instructor_courses['courses'])

    @classmethod
    def description(cls):
        return 'This job is intended for manual run. It queues up reminder emails to instructors with scheduled courses.'

    @classmethod
    def key(cls):
        return 'remind_instructors'
