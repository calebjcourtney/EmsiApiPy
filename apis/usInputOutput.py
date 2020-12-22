"""
This documentation describes Emsi's Input-Output API for regions in the U.S., Canada, and the U.K.
"""
from .base import EmsiBaseConnection

import requests


class USInputOutputConncetion(EmsiBaseConnection):
    """
    Attributes:
        base_url (str): the base url for making requests to the API
        scope (str): the scope for handling authentication to the Oauth 2.0 server
        token (str): the Oauth 2.0 token
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://io.emsicloud.com/"
        self.scope = "us-io"  # todo: add more scopes for other nations

        self.get_new_token()

    def download_data(self, api_endpoint: str, payload: dict = None, querystring: dict = None) -> requests.Response:
        """Summary

        Args:
            api_endpoint (TYPE): Description
            payload (None, optional): Description

        Returns:
            requests.Response: Description
        """
        url = self.base_url + api_endpoint
        if payload is None:
            response = self.get_data(url, querystring)

        else:
            response = self.post_data(url, payload, querystring)

        if response.status_code != 200:
            if response.text == "Token expired":
                self.get_new_token()
                return self.download_data(api_endpoint, payload, querystring)

            else:
                print(response.text)

        return response

    def get_dataruns(self, country = "us") -> list:
        """All possible dataruns available for a country may be accessed by doing a GET request to https://io.emsicloud.com/v1/<country>/.

        Args:
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            list: Description
        """
        return self.download_data("v1/{}".format(country)).json()

    def get_years(self, datarun: str = None, country: str = "us") -> list:
        """All possible years available for a country and datarun may be accessed by doing a GET or POST request to https://io.emsicloud.com/v1/<country>/<datarun>/.

        Args:
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            list: years available
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        return self.download_data(f"v1/{country}/{datarun}").json()

    def get_codes(self, datarun: str = None, country: str = "us") -> list:
        """A listing of all codes and their definitions can be obtained by doing a GET or POST request to https://io.emsicloud.com/v1/<country>/<datarun>/codes/.

        Args:
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            list: list of the codes and definitions
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        return self.download_data(f"v1/{country}/{datarun}/codes").json()

    def get_functions(self, datarun: str = None, year: str = None, country: str = "us"):
        """A listing of each data function, their respective descriptions, and whether the function has a multi-regional counterpart can be obtained by doing a GET or POST request to https://io.emsicloud.com/v1/<country>/<datarun>/<year>/.

        Args:
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            year (str, optional): the year to use. If none is provided, will use the latest year available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            list: a list of the services available
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        if year is None:
            year = max(self.get_years(datarun, country))

        return self.download_data(f"v1/{country}/{datarun}/{year}/").json()

    def post_basics(self, payload: dict, datarun: str = None, year: str = None, country: str = "us") -> dict:
        """A series of services that just return data and don't require any inputs. They can be requested individually as services by using https://io.emsicloud.com/v1/<country>/<datarun>/<year>/<service>. Alternatively, when requesting the basics service using https://io.emsicloud.com/v1/<country>/<datarun>/<year>/<basics>, they can be bundled in the metrics array.

            - Multipliers: type-to-type multipliers
            - ConsultantMultipliers: sales-to-type multipliers
            - GRP: Earnings, Taxes, Subsidies, Profits
            - TPI: Tax component vectors
            - Sales
            - Exports
            - Ratios: sales to jobs/earnings/value added ratios
            - RPCs: Regional Purchasing Coefficients
            - RID: Residents' Income Data
            - A: A matrix (technical coefficients) Warning: very large amount of data!
            - B: B matrix (sales multipliers) Warning: very large amount of data!
            - BJobs: Jobs B matrix (jobs-to-jobs multipliers) Warning: very large amount of data!
            - Z: Z matrix (transactions) Warning: very large amount of data!

        The metrics object is an array of objects with the properties altName and name. The altName is an arbitrary string that will be returned from the API in conjunction with the output of its respective dataset.

        Args:
            payload (dict): the json being passed to the server
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            year (str, optional): the year to use. If none is provided, will use the latest year available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            dict: the json portion of the response from the API
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        if year is None:
            year = max(self.get_years(datarun, country))

        response = self.download_data(
            url = f"v1/{country}/{datarun}/{year}/basics",
            payload = payload
        )

        return response.json()

    def post_scenario(self, payload: dict, datarun: str = None, year: str = None, country: str = "us") -> dict:
        """Run a scenario on the I-O API

        Args:
            payload (dict): the json being passed to the server
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            year (str, optional): the year to use. If none is provided, will use the latest year available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            dict: the json portion of the response from the API
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        if year is None:
            year = max(self.get_years(datarun, country))

        return self.download_data(
            url = f"v1/{country}/{datarun}/{year}/scenario",
            payload = payload
        ).json()

    def post_requirements(self, payload: dict, datarun: str = None, year: str = None, country: str = "us") -> dict:
        """
        This service requires inputs of sectors for the service to process.
        If no input is specified, the service acts like a basic service and returns the requirements for all sectors.

        Args:
            payload (dict): the json being passed to the server
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            year (str, optional): the year to use. If none is provided, will use the latest year available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            dict: the json portion of the response from the API
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        if year is None:
            year = max(self.get_years(datarun, country))

        return self.download_data(
            f"v1/{country}/{datarun}/{year}/requirements",
            payload = payload
        ).json()

    def post_spending(self, payload: dict, datarun: str = None, year: str = None, country: str = "us") -> dict:
        """This service requires inputs of sectors for the service to process.
        If no input is specified, the service acts like a basic service and returns the spending for all sectors.

        Args:
            payload (dict): the json being passed to the server
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            year (str, optional): the year to use. If none is provided, will use the latest year available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            dict: the json portion of the response from the API
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        if year is None:
            year = max(self.get_years(datarun, country))

        return self.download_data(
            url = f"v1/{country}/{datarun}/{year}/spending",
            payload = payload
        ).json()

    def post_econbase(self, payload: dict, datarun: str = None, year: str = None, country: str = "us") -> dict:
        """This service requires inputs of all sectors that will be broken out into groups.

        Args:
            payload (dict): the json being passed to the server
            datarun (str, optional): the datarun to use. If none is provided, will use the latest datarun available
            year (str, optional): the year to use. If none is provided, will use the latest year available
            country (str, optional): the country to request data for (currently only US supported). If none is provided, will default to the US

        Returns:
            dict: the json portion of the response from the API
        """
        if datarun is None:
            datarun = max(self.get_dataruns(country))

        if year is None:
            year = max(self.get_years(datarun, country))

        return self.download_data(
            url = f"v1/{country}/{datarun}/{year}/econbase",
            payload = payload
        ).json()
