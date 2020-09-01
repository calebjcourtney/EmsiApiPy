"""
Summary
"""
import pandas as pd

from .base import EmsiBaseConnection


class SkillsClassificationConnection(EmsiBaseConnection):
    """docstring for SkillsClassificationConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://ipeds.emsicloud.com/"
        self.scope = "emsiauth"

        self.token = self.get_new_token()

    def get_status(self):
        """
        url = "https://ipeds.emsicloud.com/health/status"

        response = requests.request("GET", url)

        print(response.text)
        """
        return self.download_data("health/status").json()

    def post_institutions(self, institutions: list):
        """
        import requests

        url = "https://ipeds.emsicloud.com/institutions"

        payload = "{\"institutionIds\": [247940, 166027]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        payload = {"institutionIds": institutions}
        return self.download_data(
            "institutions",
            payload = payload
        ).json()

    def get_institutions_geo(self, geo_level, geo_code):
        """
        url = "https://ipeds.emsicloud.com/institutions/zip/42303"

        headers = {'authorization': 'Bearer <access_token>'}

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        """
        if geo_level not in ['zip', 'fips']:
            raise ValueError(f"`geo_level` must be one of ['zip', 'fips'], found `{geo_level}`")

        return self.download_data(f"institutions/{geo_level}/{geo_code}").json()

    def get_institutions_search(self, search):
        """
        url = "https://ipeds.emsicloud.com/institutions/Harvard"

        headers = {'authorization': 'Bearer <access_token>'}

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        """
        return self.download_data(f"institutions/{search}").json()

    def post_institutions_search(self, payload):
        """
        url = "https://ipeds.emsicloud.com/institutions/search"

        payload = "{\"searchType\": \"zip\", \"values\":[\"83843\", \"42303\"]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        return self.download_data(
            f"institutions/search",
            payload = payload
        ).json()

    # please note that the post_rankings endpoint is not included,
    # since it has been removed from Emsi's software and the data is not updated

    def post_cip_soc(self, cips: list):
        """
        url = "https://ipeds.emsicloud.com/soccip/cip2soc"

        payload = "{\"cipCodes\": [\"45.0902\", \"45.0401\"]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        payload = {"cipCodes": cips}
        return self.download_data(
            "soccip/cip2soc",
            payload = payload
        ).json()

    def post_soc_cip(self, socs: list):
        """
        url = "https://ipeds.emsicloud.com/soccip/soc2cip"

        payload = "{\"socCodes\": [\"19-3094\"]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        payload = {"socCodes": socs}
        return self.download_data(
            "soccip/soc2cip",
            payload = payload
        )

    def post_institutions_df(self, institutions: list):
        """
        import requests

        url = "https://ipeds.emsicloud.com/institutions"

        payload = "{\"institutionIds\": [247940, 166027]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        data = self.post_institutions(institutions)
        df = pd.DataFrame(data["rows"])

        return df

    def get_institutions_geo_df(self, geo_level, geo_code):
        """
        url = "https://ipeds.emsicloud.com/institutions/zip/42303"

        headers = {'authorization': 'Bearer <access_token>'}

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        """
        data = self.get_institutions_geo(geo_level, geo_code)
        df = pd.DataFrame(data["rows"])

        return df

    def get_institutions_search_df(self, search):
        """
        url = "https://ipeds.emsicloud.com/institutions/Harvard"

        headers = {'authorization': 'Bearer <access_token>'}

        response = requests.request("GET", url, headers=headers)

        print(response.text)
        """
        data = self.get_institutions_search(search)
        df = pd.DataFrame(data["rows"])

        return df

    def post_institutions_search_df(self, payload):
        """
        url = "https://ipeds.emsicloud.com/institutions/search"

        payload = "{\"searchType\": \"zip\", \"values\":[\"83843\", \"42303\"]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        data = self.get_institutions_search(payload)
        df = pd.DataFrame(data["rows"])

        return df

    def post_cip_soc_df(self, cips):
        """
        url = "https://ipeds.emsicloud.com/soccip/cip2soc"

        payload = "{\"cipCodes\": [\"45.0902\", \"45.0401\"]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """
        data = self.post_cip_soc(cips)
        df = pd.DataFrame()
        for record in data["mapping"]:
            temp_df = pd.DataFrame(
                {
                    "cip": [record["code"] for _ in record["corresponding"]],
                    "soc": [x for x in record["corresponding"]]
                }
            )
            df = df.append(temp_df, ignore_index = True)

        return df

    def post_soc_cip_df(self, socs):
        """
        url = "https://ipeds.emsicloud.com/soccip/soc2cip"

        payload = "{\"socCodes\": [\"19-3094\"]}"
        headers = {
            'authorization': "Bearer <access_token>",
            'content-type': "application/json"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
        """

        data = self.post_soc_cip(socs)
        df = pd.DataFrame()
        for record in data["mapping"]:
            temp_df = pd.DataFrame(
                {
                    "soc": [record["code"] for _ in record["corresponding"]],
                    "cip": [x for x in record["corresponding"]]
                }
            )
            df = df.append(temp_df, ignore_index = True)

        return df
