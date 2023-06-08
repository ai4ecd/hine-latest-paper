import re
import hashlib
import logging
import os
import requests
import urllib3
import pickle
import shutil
import time
from playwright.sync_api import sync_playwright
from time import sleep

# log config
logging.basicConfig()
logger = logging.getLogger('Sci-Hub')
logger.setLevel(logging.DEBUG)
urllib3.disable_warnings()

# constants
SCHOLARS_BASE_URL = 'https://scholar.google.com/scholar'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}


class SciHub(object):
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers = HEADERS
        self.available_base_url_list = self._get_available_scihub_urls()
        self.available_backbone_url_list = self._get_available_scihub_backbone_urls()
        self.cycle_iter = itertools.cycle(self.available_base_url_list)
        self.cycle_bb = itertools.cycle(self.available_backbone_url_list)
        self.base_url = self.available_base_url_list[0] + '/'
        self.sess.proxies = {
            "http": 'socks5://127.0.0.1:1080',
            "https": 'socks5://127.0.0.1:7890', }

        # init a playwright browser and page
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context()

            # Set the user agent
            context.set_user_agent(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )

            # Set the download options
            context.set_implicit_wait_timeout(5000)
            context._enable_default_browser_context()
            page = context.new_page()
            page.set_default_timeout(5000)
            self.page = page

    def _get_available_scihub_urls(self):
        return ['https://sci-hub.ee', 'https://sci-hub.shop', 'https://sci-hub.se', 'https://sci-hub.st',
                'http://sci-hub.is', 'https://sci.hubg.org', 'https://sci.hubbza.co.za', 'https://sci-hub.ru',
                'https://sci-hub.hkvisa.net', 'https://sci-hub.mksa.top', 'http://sci-hub.ren', 'https://sci-hub.wf']

    def _get_available_scihub_backbone_urls(self):
        return ['https://sci-hub.se', 'https://sci-hub.st', 'https://sci-hub.ru', 'https://sci.hubg.org/']

    def _change_base_url(self):
        self.base_url = next(self.cycle_iter)
        # logger.info("I'm changing to {}".format(self.base_url))

    def _change_backbone_url(self):
        self.base_url = next(self.cycle_bb)
        # logger.info("I'm changing to {}".format(self.base_url))

    def download(self, identifier, destination='', path=None):
        # load balancing.
        data = self.fetch(identifier)

        return data

    def fetch(self, identifier):
        """
        Original -> Scihub -> Scihub backbone
        """
        try:
            # Try download !
            shutil.rmtree("chrome_pdfs")
            os.makedirs("chrome_pdfs")
            self.page.goto(identifier)
            direct_succ = False
            sleep_time = 0
            sleep_limit = 5
            sleep_max = 10
            while sleep_time < sleep_limit:
                sleep(1)
                sleep_time += 1

                if len(os.listdir('chrome_pdfs')) == 1:
                    filename = os.listdir('chrome_pdfs')[0]
                    _, f_ext = os.path.splitext(filename)
                    if f_ext == '.pdf':  # we might found .crdownload
                        old_filename = filename
                        filename = str(time.time()) + '_' + filename
                        shutil.move(os.path.join('chrome_pdfs', old_filename), os.path.join('pdfs', filename))
                        direct_succ = True
                        break
                    else:  # still downloading!
                        sleep_limit += 1
                        sleep_limit = max(sleep_max, sleep_limit)
            if direct_succ:
                return {
                    'direct': True,
                    'pdf': None,
                    'url': identifier,
                    'name': filename,
                }
        except:
            pass

        try:
            print("Falling back to scihub.")
            self._change_base_url()
            self.page.goto(self.base_url + '/' + identifier)
            btn = self.page.query_selector(
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save') "
                "or contains(text(), '下载')]")
            btn.click()
            sci_succ = False
            sleep_time = 0
            sleep_limit = 5
            sleep_max = 10
            while sleep_time < sleep_limit:
                sleep(1)
                sleep_time += 1

                if len(os.listdir('chrome_pdfs')) == 1:
                    filename = os.listdir('chrome_pdfs')[0]
                    _, f_ext = os.path.splitext(filename)
                    if f_ext == '.pdf':  # we might found .crdownload
                        old_filename = filename
                        filename = str(time.time()) + '_' + filename
                        shutil.move(os.path.join('chrome_pdfs', old_filename), os.path.join('pdfs', filename))
                        sci_succ = True
                        break
                    else:  # still downloading!
                        sleep_limit += 1
                        sleep_limit = max(sleep_max, sleep_limit)

            if sci_succ:
                return {
                    'direct': True,
                    'pdf': None,
                    'url': identifier,
                    'name': filename,
                }
        except:
            pass

        try:
            print("Falling back to scihub backbone.")
            self._change_backbone_url()
            self.page.goto(self.base_url + '/' + identifier)
            btn = self.page.query_selector(
                "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'save') "
                "or contains(text(), '下载')]")
            btn.click()
            sci_succ = False
            sleep_time = 0
            sleep_limit = 5
            sleep_max = 10
            while sleep_time < sleep_limit:
                sleep(1)
                sleep_time += 1

                if len(os.listdir('chrome_pdfs')) == 1:
                    filename = os.listdir('chrome_pdfs')[0]
                    _, f_ext = os.path.splitext(filename)
                    if f_ext == '.pdf':  # we might found .crdownload
                        old_filename = filename
                        filename = str(time.time()) + '_' + filename
                        shutil.move(os.path.join('chrome_pdfs', old_filename), os.path.join('pdfs', filename))
                        sci_succ = True
                        break
                    else:  # still downloading!
                        sleep_limit += 1
                        sleep_limit = max(sleep_max, sleep_limit)

            if sci_succ:
                return {
                    'direct': True,
                    'pdf': None,
                    'url': identifier,
                    'name': filename,
                }
        except:
            pass

    def _generate_name(self, res):
        """
        Generate unique filename for paper. Returns a name by calculating 
        md5 hash of file contents, then appending the last 20 characters
        of the url which typically provides a good paper identifier.
        """
        name = res.url.split('/')[-1]
        name = re.sub('#view=(.+)', '', name)
        pdf_hash = hashlib.md5(res.content).hexdigest()
        return '%s-%s' % (pdf_hash, name[-20:])


class CaptchaNeedException(Exception):
    pass


if __name__ == '__main__':
    sh = SciHub()
    logger.setLevel(logging.DEBUG)

    file_idx = 0
    paper_idx = 0
    success_total_cnt = 0

    with open("download_log", 'r') as file:
        checkpoint = file.readlines()
        if len(checkpoint) != 0:
            file_idx = int(checkpoint[0])
            paper_idx = int(checkpoint[1]) + 1
            print("Checkpoint found, download from " + str(file_idx) + '.pickle ' + ' paper id : ' + str(paper_idx))

    while True:
        # find for *.pickle
        if os.path.exists(str(file_idx) + '.pickle'):
            success_cnt = 0

            print('unpickle file : ' + str(file_idx) + '.pickle')
            with open(str(file_idx) + '.pickle', 'rb') as file:
                try:
                    obj = pickle.load(file)
                    success_cnt = obj['total']
                    success_total_cnt += success_cnt
                except EOFError as e:
                    print(e)
                    break

            print('success total count: ' + str(success_total_cnt))

            for paper_id, paper_name in obj['id_name'][paper_idx:]:
                if paper_id.find('http') != -1:
                    continue

                if os.path.exists('pdfs/' + paper_name):
                    continue

                print('try paper ' + paper_name + ' ' + str(paper_idx) + '/' + str(len(obj['id_name'])))
                try:
                    sh.download(paper_id)
                except Exception as e:
                    print(e)
                    print('catch unknown error..')
                    break

                print('finished paper ' + paper_name + ' ' + str(paper_idx) + '/' + str(len(obj['id_name'])))
                paper_idx += 1

            paper_idx = 0
            file_idx += 1
            continue

        break

    print('job done. success total count : ' + str(success_total_cnt))
