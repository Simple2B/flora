import requests
import urllib
from datetime import datetime

from flask import current_app


class ProcoreApi:
    def __init__(self):
        pass

    def get_me(self, access_token):
        """
        DESCRIPTION:
            Calls /vapid/me endpoint and returns user login/id.
        INPUTS:
            access_token =  access_token used as credentials to communicate with the API
        OUTPUTS:
            me_json['login'] = user's login name
            me_json['id']    = user's login ID
        """
        headers = {"Authorization": "Bearer " + access_token}
        response = requests.get(
            current_app.config["BASE_URL"] + "/vapid/me", headers=headers
        )
        me_json = response.json()
        return me_json["login"], me_json["id"]

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
            "client_id": current_app.config["CLIENT_ID"],
            "response_type": "code",
            "redirect_uri": current_app.config["REDIRECT_URI"],
        }
        url = (
            current_app.config["OAUTH_URL"]
            + "/oauth/authorize?"
            + urllib.parse.urlencode(params)
        )
        return url

    def update_date(self, created_at):
        '''
        DESCRIPTION:
            Turns unix time stamp into human readable time for the expire_date.Takes in unix created_at
                time value and adds 7200 (2 hours) to the created_at value before converting time.
        INPUTS:
            created_at = the unix date and time of the authorization token creation.
        OUTPUT:
            return     = returns the created_at unix date/time in a human-readable format
        '''
        return datetime.utcfromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S')

    def update_expire(self, created_at):
        '''
        DESCRIPTION:
            Turns unix time stamp into human readable time for the expire_date.Takes in unix created_at
                time value and adds 7200 (2 hours) to the created_at value before converting time.
        INPUTS:
            created_at = the unix date and time of the authorization token creation.
        OUTPUT:
            return     = returns the expires_at unix date/time in a human-readable format.
        '''
        return datetime.utcfromtimestamp(created_at+7200).strftime('%Y-%m-%d %H:%M:%S')

    def get_token(self, code):
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
        client_auth = requests.auth.HTTPBasicAuth(
            current_app.config["CLIENT_ID"], current_app.config["CLIENT_SECRET"]
        )
        post_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": current_app.config["REDIRECT_URI"],
        }
        response = requests.post(
            current_app.config["BASE_URL"] + "/oauth/token",
            auth=client_auth,
            data=post_data,
        )
        response_json = response.json()
        print(response_json)
        return (
            response_json["access_token"],
            response_json["refresh_token"],
            response_json["created_at"],
        )
