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
import time

from flask import current_app as app
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as Coptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as Foptions
from xena.test_utils import util


class WebDriverManager(object):

    @classmethod
    def launch_browser(cls, browser=None, headless=None):
        _browser = browser or util.get_xena_browser()
        if headless:
            _headless = True if headless == 'true' else False
        else:
            _headless = util.get_xena_browser_headless()
        app.logger.warning(f'Launching {_browser.capitalize()}')
        app.logger.info(f'Headless is {_headless}')

        if _browser == 'firefox':
            p = FirefoxProfile()
            p.set_preference(key='devtools.jsonview.enabled', value=False)
            options = Foptions()
            options.profile = p
            options.headless = _headless
            return webdriver.Firefox(options=options)
        else:
            options = Coptions()
            options.binary_location = util.get_xena_browser_chrome_binary_path()
            if _headless:
                options.add_argument('--headless=new')
            prefs = {
                'profile.default_content_settings.popups': 0,
                'download.default_directory': util.default_download_dir(),
                'directory_upgrade': True,
            }
            options.add_experimental_option('prefs', prefs)
            driver = webdriver.Chrome(options=options)
            WebDriverManager.allow_canvas_iframe_in_chrome(driver)
            return driver

    @classmethod
    def allow_canvas_iframe_in_chrome(cls, driver):
        driver.get('chrome://settings/trackingProtection')
        time.sleep(util.get_click_sleep())
        site_list_root = (driver.find_element(By.CSS_SELECTOR, 'settings-ui').shadow_root
                          .find_element(By.CSS_SELECTOR, 'settings-main').shadow_root
                          .find_element(By.CSS_SELECTOR, 'settings-basic-page').shadow_root
                          .find_element(By.CSS_SELECTOR, 'settings-privacy-page').shadow_root
                          .find_element(By.CSS_SELECTOR, 'settings-cookies-page').shadow_root
                          .find_element(By.CSS_SELECTOR, 'site-list').shadow_root)
        driver.execute_script('arguments[0].click();', site_list_root.find_element(By.CSS_SELECTOR, 'cr-button[id=addSite]'))
        time.sleep(util.get_click_sleep())
        add_site_dialog_root = site_list_root.find_element(By.CSS_SELECTOR, 'add-site-dialog').shadow_root
        add_site_input_root = add_site_dialog_root.find_element(By.CSS_SELECTOR, 'cr-input[id=site]').shadow_root
        add_site_input_root.find_element(By.CSS_SELECTOR, 'input[id=input]').click()
        add_site_input_root.find_element(By.CSS_SELECTOR, 'input[id=input]').send_keys('[*.]instructure.com')
        add_site_dialog_root.find_element(By.CSS_SELECTOR, 'cr-button[id=add]').click()
        time.sleep(util.get_click_sleep())

    @classmethod
    def quit_browser(cls, driver):
        app.logger.warning(f'Quitting {util.get_xena_browser().capitalize()}')
        driver.quit()
