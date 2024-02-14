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
import os
import sys
import time

abspath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(abspath)

import click  # noqa
from diablo.factory import create_app  # noqa

application = create_app(standalone=True)


@application.cli.command('delete_scheduled_events_from_kaltura')
@click.argument('rehearsal', default=False)
def delete_kaltura_events(rehearsal):
    """Delete Kaltura events created by Diablo."""
    with application.app_context():
        from diablo.externals.kaltura import CREATED_BY_DIABLO_TAG, Kaltura

        def _print(message):
            print(f"""
                {'[REHEARSAL MODE]: ' if rehearsal else ''}{message}
            """)
        _print('Time for some Kaltura housekeeping...')

        kaltura = Kaltura()
        kaltura_events = kaltura.get_events_by_tag(tags_like=CREATED_BY_DIABLO_TAG)
        if kaltura_events:
            _print(f'In two seconds we will delete {len(kaltura_events)} event(s) in Kaltura. Use control-C to abort.')
            time.sleep(2)

            for event in kaltura_events:
                if not rehearsal:
                    kaltura.delete(event_id=event['id'])
                _print(f'Deleted --> {event["description"] or event["summary"]}')
        else:
            _print(f'No events found with tag {CREATED_BY_DIABLO_TAG}')
        _print('Have a nice day!')


@application.cli.command('update_lti')
def update_lti():
    """Update Kaltura LTI configurations in Canvas to match local Diablo configs."""
    with application.app_context():
        from diablo.externals.canvas import update_lti_configurations

        print('Starting LTI configuration update...')

        successes, errors = update_lti_configurations()
        if successes:
            print('The following tools were updated:')
            for tool_name in successes:
                print(f'  * {tool_name}')
        if errors:
            print('The following tools could not be updated:')
            for tool_name in errors:
                print(f'  * {tool_name}')
            print('Check app logs for details.')
