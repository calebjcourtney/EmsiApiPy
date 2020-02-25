class EmsiConnection(object):
    def __init__(self) -> None:
        """Summary
        """

        super().__init__()
        self.base_url = "https://agnitio.emsicloud.com/"
        self.scope = "emsiauth"

        self.token = self.get_new_token()
