import requests
import urllib
from datetime import datetime, timedelta

from flask import current_app

from app.logger import log


class ProcoreApi:

    TOKEN_EXPIRED_PERIOD = timedelta(hours=2)

    def __init__(self):
        self.token_updated = None
        self.__access_token = None
        self.__drawings = {}
        self.__drawing_uploads = {}

    def get_me(self):
        """
        DESCRIPTION:
            Calls /vapid/me endpoint and returns user login/id.
        INPUTS:
            access_token =  access_token used as credentials to communicate with the API
        OUTPUTS:
            me_json['login'] = user's login name
            me_json['id']    = user's login ID
        """
        headers = {"Authorization": "Bearer " + self.access_token}
        response = requests.get(
            current_app.config["PROCORE_API_BASE_URL"] + "/vapid/me", headers=headers
        )
        me_json = response.json()

        return me_json["login"], me_json["id"]

    def bids(self, ignore_testing=False):
        """
        DESCRIPTION:
            List Bids Within A Company.
        """
        if current_app.config["TESTING"] and not ignore_testing:
            from tests.utils import TEST_BIDS
            return TEST_BIDS

        access_token = self.access_token
        if not access_token:
            log(log.ERROR, "ProcoreApi.bids: need access_token!")
            return []
        headers = {"Authorization": "Bearer " + access_token}
        PROCORE_API_BASE_URL = current_app.config["PROCORE_API_BASE_URL"]
        PROCORE_API_COMPANY_ID = current_app.config["PROCORE_API_COMPANY_ID"]

        url = f"{PROCORE_API_BASE_URL}vapid/companies/{PROCORE_API_COMPANY_ID}/bids"

        log(log.DEBUG, 'Make request to get bids')
        response = requests.get(url, headers=headers)
        log(log.DEBUG, 'Get response with bids')
        if response.status_code >= 400:
            res = response.json()
            log(log.ERROR, res['errors'])
            return []
        bids_json = response.json()

        return bids_json

    def make_authorization_url(self):
        """
        DESCRIPTION:
            Creates the authorization URL to obtain the authorization code from Procore.
        INPUTS:
            N/A
        OUTPUTS:
            url: the url used to obtain the authorization code from the application.
        """
        # Generate a random string for the state parameter
        # Save it for use later to prevent xsrf attacks

        params = {
            "client_id": current_app.config["PROCORE_API_CLIENT_ID"],
            "response_type": "code",
            "redirect_uri": current_app.config["PROCORE_API_REDIRECT_URI"],
        }
        url = (
            current_app.config["PROCORE_API_OAUTH_URL"]
            + "/oauth/authorize?"
            + urllib.parse.urlencode(params)
        )

        return url

    def update_date(self, created_at):
        """
        DESCRIPTION:
            Turns unix time stamp into human readable time for the expire_date.Takes in unix created_at
                time value and adds 7200 (2 hours) to the created_at value before converting time.
        INPUTS:
            created_at = the unix date and time of the authorization token creation.
        OUTPUT:
            return     = returns the created_at unix date/time in a human-readable format
        """
        return datetime.utcfromtimestamp(created_at).strftime("%Y-%m-%d %H:%M:%S")

    def update_expire(self, created_at):
        """
        DESCRIPTION:
            Turns unix time stamp into human readable time for the expire_date.Takes in unix created_at
                time value and adds 7200 (2 hours) to the created_at value before converting time.
        INPUTS:
            created_at = the unix date and time of the authorization token creation.
        OUTPUT:
            return     = returns the expires_at unix date/time in a human-readable format.
        """
        return datetime.utcfromtimestamp(created_at + 7200).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    @property
    def access_token(self):
        """
        DESCRIPTION:
            Gets the access token by utilizating the authorization code that was
            previously obtained from the authorization_url call.
        INPUTS:
            code = authorization code
        OUTPUTS:
            response_json["access_token"]  = user's current access token
            response_json["refresh_token"] = user's current refresh token
            response_json['created_at']    = the date and time the user's access
            token was generated
        """
        now = datetime.now()
        log(log.DEBUG, 'Make response to get access token')
        if self.token_updated and (now - self.token_updated) < self.TOKEN_EXPIRED_PERIOD:
            return self.__access_token

        post_data = {
            "grant_type": "client_credentials",
            "client_id": current_app.config["PROCORE_API_CLIENT_ID"],
            "client_secret": current_app.config["PROCORE_API_CLIENT_SECRET"],
        }

        response = requests.post(
            current_app.config["PROCORE_API_BASE_URL"] + "/oauth/token",
            data=post_data,
        )
        response_json = response.json()
        self.token_updated = datetime.now()
        log(log.DEBUG, f'Get response with access token after "{(self.token_updated - now).seconds}"')
        log(log.DEBUG, "%s", response_json)
        self.__access_token = response_json["access_token"]
        return self.__access_token

    @property
    def projects(self):
        """
        DESCRIPTION:
            List Projects Within A Company.
        """
        access_token = self.access_token
        if not access_token:
            log(log.ERROR, "ProcoreApi.bids: need access_token!")
            return []
        headers = {"Authorization": "Bearer " + access_token}
        PROCORE_API_BASE_URL = current_app.config["PROCORE_API_BASE_URL"]
        PROCORE_API_COMPANY_ID = current_app.config["PROCORE_API_COMPANY_ID"]

        url = f"{PROCORE_API_BASE_URL}vapid/projects?company_id={PROCORE_API_COMPANY_ID}"

        log(log.DEBUG, 'Make request to get projects')
        response = requests.get(url, headers=headers)
        log(log.DEBUG, 'Get response with projects')
        if response.status_code >= 400:
            res = response.json()
            log(log.ERROR, res['errors'])
            return []
        return response.json()

    def drawing_uploads(self, project_id):
        """
        DESCRIPTION:
            List Projects Within A Company.
        """
        log(log.DEBUG, "drawing_uploads for project_id:%d", project_id)
        if project_id in self.__drawing_uploads:
            return self.__drawing_uploads[project_id]
        access_token = self.access_token
        if not access_token:
            log(log.ERROR, "ProcoreApi.bids: need access_token!")
            return []
        headers = {"Authorization": "Bearer " + access_token}
        PROCORE_API_BASE_URL = current_app.config["PROCORE_API_BASE_URL"]
        url = f"{PROCORE_API_BASE_URL}rest/v1.0/projects/{project_id}/drawing_uploads"
        response = requests.get(url, headers=headers)
        if response.status_code >= 400:
            res = response.json()
            log(log.ERROR, res['errors'])
            return []
        result = response.json()
        self.__drawing_uploads[project_id] = result
        return result

    def drawings(self, drawing_area_id):
        """
        DESCRIPTION:
            List Drawings by drawing_area_id
        """
        log(log.DEBUG, "drawings for drawing_area_id:%d", drawing_area_id)
        if drawing_area_id in self.__drawings:
            return self.__drawings[drawing_area_id]
        access_token = self.access_token
        if not access_token:
            log(log.ERROR, "ProcoreApi.bids: need access_token!")
            return []
        headers = {"Authorization": "Bearer " + access_token}
        PROCORE_API_BASE_URL = current_app.config["PROCORE_API_BASE_URL"]
        url = f"{PROCORE_API_BASE_URL}vapid/drawing_areas/{drawing_area_id}/drawings"
        response = requests.get(url, headers=headers)
        if response.status_code >= 400:
            res = response.json()
            log(log.ERROR, res['errors'])
            return []
        result = response.json()
        self.__drawings[drawing_area_id] = result
        return result
