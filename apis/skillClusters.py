"""Summary
"""
from .base import EmsiBaseConnection


class SkillClustersConnection(EmsiBaseConnection):
    """docstring for SkillClustersConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://sc.emsicloud.com/"
        self.scope = "skillscluster"

        self.token = self.get_new_token()

    def get_status(self) -> dict:
        """
        Summary

        Returns:
            TYPE: Description
        """
        return self.download_data("status").json()

    def is_healthy(self) -> bool:
        """
        Summary

        Returns:
            TYPE: Description
        """
        response = self.download_data("status")

        return response.json()['ok']

    def get_models(self, model_id: str = None) -> dict:
        if model_id is not None:
            response = self.download_data("models/{}".format(model_id))
        else:
            response = self.download_data("models")

        return response.json()

    def get_model_facets(self, model_id: str, facet_id: str = None) -> dict:
        if facet_id is not None:
            response = self.download_data("models/{}/facets/{}".format(model_id, facet_id))
        else:
            response = self.download_data("models/{}/facets".format(model_id))

        return response.json()

    def get_model_clusters(self, model_id: str, cluster_id: str = None) -> dict:
        if cluster_id is not None:
            response = self.download_data("models/{}/clusters/{}".format(model_id, cluster_id))
        else:
            response = self.download_data("models/{}/clusters".format(model_id))

        return response.json()

    def get_model_skills(self, model_id: str) -> dict:
        return self.download_data("models/{}/skills".format(model_id)).json()

    def post_model_match(self, model_id: str, payload: dict) -> dict:
        return self.download_data("models/{}/match".format(model_id), payload).json()

    def post_model_slice(self, model_id: str, payload: dict) -> dict:
        return self.download_data("models/{}/slice".format(model_id), payload).json()
