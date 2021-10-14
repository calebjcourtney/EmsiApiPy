"""Summary
"""
import requests
import pandas as pd

try:
    from ..permissions import DEFAULT
except ValueError:  # need this for testing
    from permissions import DEFAULT


class EmsiBaseConnection(object):
    """docstring for EmsiBaseConnection

    Attributes:
        token (str): the authentication token for accessing the given API
        username (str): the client_id for accessing the API
        password (str): the client_secret for accessing the API
        scope (str): the scope for requesting an auth token from the API
    """

    def __init__(self) -> None:
        """
        Parses the username and password from the permissions
        """
        self.username, self.password = DEFAULT['username'], DEFAULT['password']

    def get_new_token(self) -> None:
        """Creates a new access token for connecting to the API

        Raises:
            ValueError: Raises an error if you don't have permission to access the given API
        """
        url = "https://auth.emsicloud.com/connect/token"

        payload = {
            "grant_type": "client_credentials",
            "scope": self.scope,
            "client_id": self.username,
            "client_secret": self.password
        }

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        # prints the error, if there is one
        if response.status_code != 200:
            print(response.text)
            print(response.status_code)

            raise ValueError("Looks like you don't have access to this dataset with those credentials")

        self.token = response.json()['access_token']

    def get_data(self, url: str, querystring: dict = None) -> requests.Response:
        """
        Makes a GET request to the API, given the URL and any querystring parameters.

        Args:
            url (str): the url for the query
            querystring (dict, optional): any additional url parameters to pass to the API

        Returns:
            requests.Response: the response from the API
        """
        headers = {'content-type': "application/json", 'authorization': "Bearer {}".format(self.token)}

        # added timeout = None - some meta requests from Core LMI are taking a long time to fulfill
        response = requests.get(url, headers = headers, params = querystring, timeout = None)

        if response.status_code == 401:
            self.get_new_token()
            return self.get_data(url, querystring)

        return response

    def post_data(self, url: str, payload: dict, querystring: dict = None) -> requests.Response:
        """
        Makes a POST request to the API, given the url and payload (querystring optional)

        Args:
            url (str): the url for the query
            payload (dict or str): a json object to be sent to the payload
            querystring (dict, optional): any additional url parameters to pass to the API

        Returns:
            requests.Response: the response from the API
        """
        headers = {'content-type': "application/json", 'authorization': "Bearer {}".format(self.token)}

        # allows for users to pass in a string as the payload (yes, even though it is documented as a dict)
        if isinstance(payload, str):
            response = requests.post(url, headers = headers, data = payload, params = querystring)
        else:
            response = requests.post(url, headers = headers, json = payload, params = querystring)

        if response.status_code == 401:
            self.get_new_token()
            return self.post_data(url, payload, querystring)

        return response

    def download_data(self, api_endpoint: str, payload: dict = None, querystring: dict = None) -> requests.Response:
        """
        Handles constructing the api_endpoint with the base url
        If the payload is None, we assume this should be a GET request (how Emsi's APIs function)
        If the payload is not None, we make a POST request instead.

        Args:
            api_endpoint (TYPE): the API url endpoint to query from
            payload (dict or str, optional): a json object to be sent to the payload
            querystring (dict, optional): any additional url parameters to pass to the API

        Returns:
            requests.Response: the response from the API
        """
        url = self.base_url + api_endpoint
        if payload is None:
            response = self.get_data(url, querystring)

        else:
            response = self.post_data(url, payload, querystring)

        if response.status_code != 200:
            print(response.text)

        return response

    def get_status(self) -> str:
        """
        Get the health of the service. Be sure to check the healthy attribute of the response, not just the status code. Caching not recommended.

        Returns:
            str: "Service is healthy"
        """
        response = self.download_data("status")

        return response.json()['data']['message']

    def is_healthy(self) -> bool:
        """
        Get the health of the service. Be sure to check the healthy attribute of the response, not just the status code. Caching not recommended.

        Returns:
            bool: True if service is health. False if not. Likely will throw an error instead, if it can't connect to the service.
        """
        response = self.download_data("status")

        return response.json()['data']['healthy']

    def get_meta(self) -> dict:
        """
        Get info on taxonomies, available months of data, available filters and facets, etc.

        Returns:
            dict: metadata, including taxonomies, available months of data, facets, metrics, and attribution text
        """
        response = self.download_data("meta")

        return response.json()['data']

    def get_docs(self) -> str:
        response = self.download_data("docs")
        return response.text


class JobPostingsConnection(EmsiBaseConnection):
    """Class for handling connections to APIs built on Emsi's postings data

    Deleted Attributes:
        base_url (str): the base url that is built off for each request
        scope (str): the scope used in the request for a token (in the Base class above)
        token (str): the token used in the request for data
    """

    def __init__(self) -> None:
        super().__init__()

    def post_totals(self, payload: dict, querystring: dict = None) -> dict:
        """
        Get summary metrics on all postings matching the filters.

        Args:
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'totals',
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']['totals']

    def post_timeseries(self, payload: dict, querystring: dict = None) -> dict:
        """
        Get summary metrics just like the /totals endpoint but broken out by month or day depending on the format of the requested time-frame.
        When requesting a daily timeseries only up to 90 days may be requested at a time.
        Months or days with 0 postings will be included in the response.
        Median posting duration is not available by timeseries to avoid biased results.

        Args:
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'timeseries',
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']

    def get_rankings(self) -> list:
        """Group and rank postings by available facets.

        Returns:
            list: list of facets available to rank by
        """
        response = self.download_data('rankings')

        return response.json()['data']

    def post_rankings_timeseries(self, facet: str, payload: dict, querystring: dict = None) -> dict:
        """Summary

        Args:
            facet (str): the data dimension to group and order on
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'rankings/{}/timeseries'.format(facet),
            payload = payload,
            querystring = querystring
        )

        try:
            return response.json()['data']
        except Exception:
            print(response.text)
            return response.json()['data']

    def post_rankings(self, facet: str, payload: dict, querystring: dict = None) -> dict:
        """
        Group and rank postings by {ranking_facet} with a monthly or daily timeseries for each ranked group.

        Args:
            facet (str): the data dimension to group and order on
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            "rankings/{}".format(facet),
            payload = payload,
            querystring = querystring
        )

        return response.json()

    def post_nested_rankings(self, facet: str, nested_facet: str, payload: dict, querystring: dict = None) -> dict:
        """
        Get a nested ranking (e.g. top companies, then top skills per company).

        Args:
            facet (str): the data dimension to group and order on
            nested_facet (str): one additional data dimension to group and order on
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            "rankings/{}/rankings/{}".format(facet, nested_facet),
            payload = payload,
            querystring = querystring
        )

        return response.json()

    def post_samples(self, payload: dict, querystring: dict = None) -> dict:
        """
        Get data for individual postings that match your requested filters.
        Note that not all fields are present for all postings, and some may be null or "Unknown".
        The url field is only available for currently active postings, and the destination website is not guaranteed to be secure or functional.

        Args:
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'samples',
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']

    def post_postings(self, payload: dict, querystring: dict = None) -> dict:
        """
        Get data for individual postings that match your requested filters.
        Note that not all fields are present for all postings, and some may be null or "Unknown".
        The url field is only available for currently active postings, and the destination website is not guaranteed to be secure or functional.

        Args:
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'postings',
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']

    def get_postings(self, posting_id: str, querystring: dict = None) -> dict:
        """
        Get a single posting by its id.

        Args:
            posting_id (str): The unique ID for a given job posting
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: Data for the specified job posting
        """
        response = self.download_data(f'postings/{posting_id}',)

        return response.json()['data']

    def get_taxonomies(self, facet: str = None, q: str = None, querystring: dict = None) -> dict:
        """
        Get a list of current available taxonomy facets.
        If `q` parameter is used, will search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete).

        Args:
            facet (str, optional): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            q (str, optional): A query string of whole or partial keywords to search for. Only when autocomplete is true is q is assumed to be a prefix. If q is omitted, the response will list results sorted by id of length limit.
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        if facet is None:
            response = self.download_data("taxonomies")
        else:
            api_endpoint = "taxonomies/{}".format(facet)
            if querystring is None:
                querystring = {"q": q}
            else:
                querystring["q"] = q

            response = self.download_data(api_endpoint, querystring = querystring)

        return response.json()['data']

    def post_taxonomies(self, facet: str, payload: dict, querystring: dict = None) -> dict:
        """
        Look up taxonomy items by ID.

        Args:
            facet (str, optional): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            "taxonomies/{}/lookup".format(facet),
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']

    def post_rankings_df(self, facet: str, payload: dict, querystring: dict = None) -> pd.DataFrame:
        """Summary

        Args:
            facet (str, optional): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            pd.DataFrame: A pandas dataframe of the rankings data
        """
        response = self.post_rankings(
            facet,
            payload = payload,
            querystring = querystring
        )

        df = pd.DataFrame(response['data']['ranking']['buckets'])
        df.rename(columns = {'name': facet}, inplace = True)

        return df

    def post_nested_rankings_df(self, facet: str, nested_facet: str, payload: dict, querystring: dict = None) -> pd.DataFrame:
        """Summary

        Args:
            facet (str): the data dimension to group and order on
            nested_facet (str): one additional data dimension to group and order on
            payload (dict or str): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            pd.DataFrame: A pandas dataframe of the nested rankings data
        """
        response = self.post_nested_rankings(
            facet,
            nested_facet,
            payload = payload,
            querystring = querystring
        )

        df = pd.DataFrame()
        for bucket in response['data']['ranking']['buckets']:
            temp_df = pd.DataFrame(bucket['ranking']['buckets'])
            temp_df['facet'] = bucket['name']

            df = df.append(temp_df, ignore_index = True)

        df.rename(columns = {'facet': facet, 'name': nested_facet}, inplace = True)

        return df


class ProfilesConnection(EmsiBaseConnection):
    """
    Use case
    This is an interface for retrieving aggregated Emsi profile data that is filtered, sorted and ranked by various properties of the profiles.

    About the data
    Profiles are collected from various sources and processed/enriched to provide information such as standardized company name, occupation, skills, and geography.

    Deleted Attributes:
        base_url (str): the beginning of the url for routing purposes (e.g. "https://emsiservices.com/profiles/")
        scope (str): the scope for requesting an auth token from the API
        token (str): the authentication token for accessing the given API
    """

    def __init__(self) -> None:
        super().__init__()

    def post_totals(self, payload: dict, querystring: dict = None) -> dict:
        """Get summary metrics on all profiles matching the filters.

        Args:
            payload (dict or str): json object for sending to the API as the body of the request

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'totals',
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']['totals']

    def post_recency(self, payload: dict, querystring: dict = None) -> dict:
        """Group filtered profile metrics by year, based on profile recency (when they were last updated).

        Args:
            payload (dict or str): json object for sending to the API as the body of the request

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            'recency',
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']['recency']

    def get_rankings(self) -> dict:
        """Get a list of current available ranking facets.

        Returns:
            dict: the data response from the API
        """
        response = self.download_data('rankings')

        return response.json()['data']

    def post_rankings(self, facet: str, payload: dict, querystring: dict = None) -> dict:
        """Rank profiles by a given facet

        Args:
            facet (str): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            payload (dict or str): json object for sending to the API as the body of the request

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            "rankings/{}".format(facet),
            payload = payload,
            querystring = querystring
        )

        return response.json()

    def get_taxonomies(self, facet: str = None, q: str = None, querystring: dict = None) -> dict:
        """
        Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete), or list taxonomy items.
        Get a list of current available taxonomy facets.
        Search taxonomies using either whole keywords (relevance search) or partial keywords (autocomplete).

        Args:
            facet (str, optional): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        if facet is None:
            response = self.download_data("taxonomies")
        else:
            api_endpoint = "taxonomies/{}".format(facet)
            if querystring is None:
                querystring = {"q": q}
            else:
                querystring["q"] = q

            response = self.download_data(api_endpoint, querystring = querystring)

        return response.json()['data']

    def post_taxonomies(self, facet: str, payload: dict, querystring: dict = None) -> dict:
        """Lookup taxonomy items by ID.

        Args:
            facet (str): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            dict: the data response from the API
        """
        response = self.download_data(
            "taxonomies/{}/lookup".format(facet),
            payload = payload,
            querystring = querystring
        )

        return response.json()['data']

    def post_rankings_df(self, facet: str, payload: dict, querystring: dict = None) -> pd.DataFrame:
        """Summary

        Args:
            facet (str): Which taxonomy to search for ID/name suggestions (Cities will always have a null ID, and cannot be listed without a q query parameter).
            payload (dict): json object for sending to the API as the body of the request
            querystring (dict, optional): additional url parameters to pass to the API (e.g. {"title_version": "emsi"})

        Returns:
            pd.DataFrame: Description
        """
        response = self.post_rankings(
            facet,
            payload = payload,
            querystring = querystring
        )
        df = pd.DataFrame(response['data']['ranking']['buckets'])
        df.rename(columns = {'name': facet}, inplace = True)

        return df
