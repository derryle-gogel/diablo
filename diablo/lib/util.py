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
from datetime import datetime

from dateutil.tz import tzutc
from flask import current_app as app
import pytz


"""Generic utilities."""


def basic_attributes_to_api_json(attributes):
    return {
        'csid': attributes['csid'],
        'email': attributes['email'],
        'firstName': attributes['first_name'],
        'lastName': attributes['last_name'],
        'uid': attributes['uid'],
    }


def default_timezone():
    return pytz.timezone(app.config['TIMEZONE'])


def epoch_time_to_isoformat(epoch_time):
    return epoch_time and datetime.fromtimestamp(epoch_time, tz=default_timezone()).isoformat()


def format_days(days):
    n = 2
    return [(days[i:i + n]) for i in range(0, len(days), n)] if days else []


def format_time(military_time):
    return datetime.strptime(military_time, '%H:%M').strftime('%I:%M %p').lower().lstrip('0') if military_time else None


def get_eb_environment():
    return app.config['EB_ENVIRONMENT'] if 'EB_ENVIRONMENT' in app.config else None


def get_names_of_days(day_codes):
    names_by_code = {
        'mo': 'Monday',
        'tu': 'Tuesday',
        'we': 'Wednesday',
        'th': 'Thursday',
        'fr': 'Friday',
        'sa': 'Saturday',
        'su': 'Sunday',
    }
    return [names_by_code.get(day_code[:2].lower()) for day_code in day_codes or ()]


def json_objects_to_dict(json_objects, field_name_of_key):
    items_per_key = {}
    for json_object in json_objects:
        key = json_object[field_name_of_key]
        if key not in items_per_key:
            items_per_key[key] = []
        items_per_key[key].append(json_object)
    return items_per_key


def local_now():
    return utc_now().astimezone(pytz.timezone(app.config['TIMEZONE']))


def localize_datetime(dt):
    return dt.astimezone(pytz.timezone(app.config['TIMEZONE']))


def localized_timestamp_to_utc(_str, date_format='%Y-%m-%dT%H:%M:%S'):
    naive_datetime = datetime.strptime(_str, date_format)
    localized_datetime = pytz.timezone(app.config['TIMEZONE']).localize(naive_datetime)
    return localized_datetime.astimezone(pytz.utc)


def readable_join(items):
    return (f"{', '.join(items[:-1])} and {items[-1]}" if len(items) > 1 else items[0]) if len(items or []) else ''


def resolve_xml_template(xml_filename):
    with open(app.config['BASE_DIR'] + f'/diablo/xml_templates/{xml_filename}', encoding='utf-8') as file:
        template_string = file.read()
    return resolve_xml_template_string(template_string)


def resolve_xml_template_string(template_string):
    return template_string.format(
        **{
            'kmc_id': app.config['CANVAS_LTI_KEY'],
        },
    )


def safe_strftime(date, date_format):
    return datetime.strftime(date, date_format) if date else None


def to_isoformat(value):
    return value and value.astimezone(tzutc()).isoformat()


def utc_now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)
