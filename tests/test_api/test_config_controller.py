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
from flask import current_app as app
import pytest
from tests.util import override_config

admin_uid = '90001'
instructor_uid = '10001'


@pytest.fixture()
def admin_session(fake_auth):
    fake_auth.login('90001')


@pytest.fixture()
def instructor_session(fake_auth):
    fake_auth.login(instructor_uid)


class TestVersion:
    """Application version API."""

    def test_anonymous_version_request(self, client):
        """All users, even anonymous, can get version info."""
        response = client.get('/api/version')
        assert response.status_code == 200
        assert 'version' in response.json
        assert 'build' in response.json


class TestCacheClear:

    @staticmethod
    def _api_clear_cache(client, expected_status_code=200):
        response = client.get('/api/cache/clear')
        assert response.status_code == expected_status_code
        return response.json

    def test_anonymous(self, client):
        """Deny anonymous access."""
        self._api_clear_cache(client, expected_status_code=401)

    def test_unauthorized(self, client, instructor_session):
        """Deny access if user is not an admin."""
        self._api_clear_cache(client, expected_status_code=401)

    def test_authorized(self, client, admin_session):
        """Admin user has access."""
        assert self._api_clear_cache(client) is True


class TestConfigController:

    def test_anonymous(self, client):
        """All users, even anonymous, can get configs."""
        term_id = '2218'
        with override_config(app, 'CURRENT_TERM_ID', term_id):
            response = client.get('/api/config')
            assert response.status_code == 200
            assert 'diabloEnv' in response.json
            api_json = response.json
            assert api_json['devAuthEnabled'] is False
            assert api_json['ebEnvironment'] == 'diablo-test'
            assert 'berkeley.edu' in api_json['emailCourseCaptureSupport']
            assert api_json['timezone'] == 'America/Los_Angeles'
            assert api_json['currentTermId'] == term_id
            assert api_json['currentTermName'] == 'Fall 2021'
            assert len(api_json['emailTemplateTypes'])
            assert len(api_json['roomCapabilityOptions'])
            assert len(api_json['searchFilterOptions'])

            api_json_lower_string = str(api_json).lower()
            for keyword in ('password', 'secret'):
                assert keyword not in api_json_lower_string
