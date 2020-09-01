"""
This API provides metadata about educational institutions reporting via IPEDS, US News rankings, and a translation layer between CIP and SOC codes.
Information and search functionality for institutions are exposed via the institution family of endpoints.
A SOC-CIP mapping is provided via the `soccip` endpoints.
"""
import pandas as pd

from .base import EmsiBaseConnection


class IpedsConnection(EmsiBaseConnection):
    """
    This API provides metadata about educational institutions reporting via IPEDS, US News rankings, and a translation layer between CIP and SOC codes.
    Information and search functionality for institutions are exposed via the institution family of endpoints.
    A SOC-CIP mapping is provided via the `soccip` endpoints.

    Attributes:
        base_url (str): The url for connecting to the API and that every other url for this class is built off
        scope (str): The scope for accessing the API
        token (str): The current access token for connecting to the API
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://ipeds.emsicloud.com/"
        self.scope = "emsiauth"

        self.get_new_token()

    def get_status(self):
        """
        This endpoint checks the health of the service.
        If the service is healthy, returns an empty `200 OK` response.

        Returns:
            TYPE: Description
        """
        return self.download_data("health/status").json()

    def post_institutions(self, institutions: list) -> dict:
        """
        Fetch information for one or more institutions. The institution IDs are IPEDS Unit IDs.

        Args:
            institutions (list): list of institutions by id for accessing the API

        Returns:
            dict: The JSON response from the API
        """
        payload = {"institutionIds": institutions}
        return self.download_data(
            "institutions",
            payload = payload
        ).json()

    def get_institutions_geo(self, geo_level: str, geo_code: str) -> dict:
        """
        Return a list of institutions operating in the specified FIPS/ZIP code.

        Args:
            geo_level (str): Description
            geo_code (str): Description

        Returns:
            TYPE: Description

        Raises:
            ValueError: Raises this error if the geo level is not one of [`zip`, `fips`]
        """
        if geo_level not in ['zip', 'fips']:
            raise ValueError(f"`geo_level` must be one of ['zip', 'fips'], found `{geo_level}`")

        return self.download_data(f"institutions/{geo_level}/{geo_code}").json()

    def get_institutions_search(self, search: str) -> dict:
        """
        Return a list of institutions matching the supplied name.

        Args:
            search (str): Description

        Returns:
            TYPE: Description
        """
        return self.download_data(f"institutions/{search}").json()

    def post_institutions_search(self, payload: dict) -> dict:
        """
        Search institutions using multiple values. Valid search types are `zip`, `fips`, `city`, `id`, and `name`.

        Args:
            payload (dict): Description

        Returns:
            TYPE: Description
        """
        return self.download_data(
            f"institutions/search",
            payload = payload
        ).json()

    def get_institutions_all(self, offset: int = 0, limit: int = 0) -> dict:
        """
        Lists all institutions with pagination.

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        return self.download_data(f"institutions/all/{offset}/{limit}").json()

    # please note that the post_rankings endpoint is not included,
    # since it has been removed from Emsi's software and the data is not updated

    def post_cip_soc(self, cips: list) -> dict:
        """
        This endpoint maps a CIP (Classification of Instructional Programs) code to the SOC (Standard Occupation Classification) codes it most likely trains for.
        For more information on CIP codes, see the (NCES site)[https://nces.ed.gov/ipeds/cipcode/Default.aspx].

        Args:
            cips (list): Description

        Returns:
            TYPE: Description
        """
        payload = {"cipCodes": cips}
        return self.download_data(
            "soccip/cip2soc",
            payload = payload
        ).json()

    def post_soc_cip(self, socs: list) -> dict:
        """
        This endpoint maps from one or more SOC codes to the CIP codes of the programs which most likely train for them.

        Args:
            socs (list): Description

        Returns:
            TYPE: Description
        """
        payload = {"socCodes": socs}
        return self.download_data(
            "soccip/soc2cip",
            payload = payload
        )

    def post_institutions_df(self, institutions: list) -> pd.DataFrame:
        """
        Fetch information for one or more institutions. The institution IDs are IPEDS Unit IDs.

        Args:
            institutions (list): Description

        Returns:
            TYPE: Description
        """
        data = self.post_institutions(institutions)
        df = pd.DataFrame(data["rows"])

        return df

    def get_institutions_geo_df(self, geo_level: str, geo_code: str) -> pd.DataFrame:
        """
        Return a list of institutions operating in the specified FIPS/ZIP code.

        Args:
            geo_level (str): Description
            geo_code (str): Description

        Returns:
            TYPE: Description
        """
        data = self.get_institutions_geo(geo_level, geo_code)
        df = pd.DataFrame(data["rows"])

        return df

    def get_institutions_search_df(self, search: str) -> pd.DataFrame:
        """
        Return a list of institutions matching the supplied name.

        Args:
            search (str): Description

        Returns:
            TYPE: Description
        """
        data = self.get_institutions_search(search)
        df = pd.DataFrame(data["rows"])

        return df

    def post_institutions_search_df(self, payload: dict) -> pd.DataFrame:
        """
        Search institutions using multiple values. Valid search types are `zip`, `fips`, `city`, `id`, and `name`.

        Args:
            payload (dict): Description

        Returns:
            TYPE: Description
        """
        data = self.get_institutions_search(payload)
        df = pd.DataFrame(data["rows"])

        return df

    def get_institutions_all_df(self, offset: int = 0, limit: int = 0) -> pd.DataFrame:
        """
        Lists all institutions with pagination.

        Args:
            payload (dict): Description

        Returns:
            dict: Description
        """
        data = self.download_data(f"institutions/all/{offset}/{limit}").json()
        df = pd.DataFrame(data)

        return df

    def post_cip_soc_df(self, cips: list) -> pd.DataFrame:
        """
        This endpoint maps a CIP (Classification of Instructional Programs) code to the SOC (Standard Occupation Classification) codes it most likely trains for.
        For more information on CIP codes, see the (NCES site)[https://nces.ed.gov/ipeds/cipcode/Default.aspx].

        Args:
            cips (list): Description

        Returns:
            TYPE: Description
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

    def post_soc_cip_df(self, socs: list) -> pd.DataFrame:
        """
        This endpoint maps from one or more SOC codes to the CIP codes of the programs which most likely train for them.

        Args:
            socs (list): Description

        Returns:
            TYPE: Description
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
