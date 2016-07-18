import requests
import time


class SSLLabsApi(object):
    ''' Api for the ssl lab checks

        Do not wonder about the `time.sleep` statements, i know that code should
        never wait unless it is highly needed.

        ssllabs.com will grade a client down and reduce its maxAssessments limit
        if there are plenty of new assessment requests in a short amount of
        time. So see this time of waiting as benefit of parallel processing.
    '''

    BASE_URL = 'https://api.ssllabs.com/api/v2/'

    pending_queue = []
    in_progress_queue = []
    result_storage = {}

    def __init__(self):
        ''' Fetch info initial to check limits '''

        self.check_info()

    def call(self, endpoint='', params={}):
        ''' Wrapper for api calls

            Because this script will probably run as as cronjob, we want to
            avoid never ending loops of failures. So we will count failures for
            every single call, repeat the call 10 times on failure and raise an
            exception if the call fails 10 times in a row.
        '''

        failures = 0
        while failures < 10:
            res = requests.get(
                '{}{}'.format(self.BASE_URL, endpoint),
                params=params
            )
            if res.status_code == 200:
                return res.json()
            else:
                failures += 1
                time.sleep(10)

        raise Exception('Too many failed calls! Please inspect this! ([{}] {})'.format(res.status_code, res.text))

    def check_info(self):
        ''' Get all information about the current api status '''

        info = self.call(endpoint='info')

        self.max_assessments = int(info.get('maxAssessments', 0))
        self.current_assessments = int(info.get('currentAssessments', 0))
        time.sleep(0.2)

    def check_domains(self, domain_list):
        ''' Check a list of domains

            Returns a dictionary like this:
            {
                'example.com': {
                    'messages': [],
                    'grades': []
                }
            }
        '''

        self.pending_queue = domain_list

        while self.pending_queue or self.in_progress_queue:

            # add new assessment if limit is not reached
            # print('\nADDING new domains')
            self.check_info()
            while self.pending_queue and self.current_assessments < self.max_assessments:
                next_domain = self.pending_queue.pop()

                if not self.check_assessment_status(next_domain, cached=False):
                    self.in_progress_queue.append(next_domain)

                time.sleep(2)
                self.check_info()

            time.sleep(30)

            # check if some assessments already finished
            # print('\nCHECKING submitted domains')
            for domain in list(self.in_progress_queue):

                if self.check_assessment_status(domain):
                    self.in_progress_queue.remove(domain)

                time.sleep(2)

        return self.result_storage

    def check_assessment_status(self, domain, cached=True):
        ''' Check the status of an domain assessment

            Will return True if the assessment for the given domain has
            finished regardless if the assessment was successful or raised an
            error.
            It returns False if the is still in progress.

            Additional it will update the result_storage with the results of the
            assessment.
        '''

        # print('  ({:<2}/{:<2}) {:<45}: '.format(self.current_assessments, self.max_assessments, domain), end='', flush=True)
        res = self.call(endpoint='analyze', params={'host': domain, 'startNew': 'off' if cached else 'on'})

        if res.get('status', '') == 'READY':
            self.update_result_storage(domain, res)
            # print('\033[32mSuccess\033[0m')

        elif res.get('status', '') == 'ERROR':
            self.result_storage.update({domain: {'grades': [], 'messages': [res.get('statusMessage')]}})
            # print('\033[31mAborted\033[0m ({})'.format(res.get('statusMessage')))

        else:
            # print('\033[33mContinues\033[0m')
            return False
        return True

    def update_result_storage(self, domain, result):
        ''' Update the result_storage with the results of an finished assessment '''
        try:
            grades = list(set([e['grade'] for e in result.get('endpoints', [])]))
        except KeyError:
            grades = list()
        messages = list(set([e['statusMessage'] for e in result.get('endpoints', [])]))

        self.result_storage.update({domain: {'grades': grades, 'messages': messages}})
