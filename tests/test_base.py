import pytest
import responses
from responses import matchers

from EmsiApiPy.base import Token
from EmsiApiPy.base import EmsiBaseConnection
from EmsiApiPy.base import JobPostingsConnection


def test_token():
    token = Token("super-secret-token")

    assert token.token == "super-secret-token"
    assert not token.is_expired()


class TestEmsiBaseConnection:
    conn = EmsiBaseConnection()
    conn.base_url = "https://example.com/"
    conn.token = Token("super-secret-token")

    @responses.activate
    def test_get_new_token(self):
        responses.add(
            responses.POST,
            "https://auth.emsicloud.com/connect/token",
            json={
                "access_token": "super-secret-token",
                "expires_in": 3600,
                "token_type": "Bearer",
            },
        )

        self.conn.token = None
        assert self.conn._username == "test-user"
        assert self.conn._password == "test-password"
        assert self.conn.scope == ""
        assert self.conn.name == ""

        self.conn.get_new_token()
        assert self.conn.token.token == "super-secret-token"

    @responses.activate
    def test_download_data_get(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}meta/metrics",
            json={"message": "GET was a success"},
        )
        assert self.conn.download_data("meta/metrics").json() == {
            "message": "GET was a success"
        }

    @responses.activate
    def test_download_data_post(self):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}meta/metrics",
            json={"message": "POST was a success"},
        )
        assert self.conn.download_data(
            "meta/metrics", payload={"filters": "some filtering"}
        ).json() == {"message": "POST was a success"}

    @responses.activate
    def test_get_data(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}meta/metrics",
            json={"message": "GET was a success"},
        )
        assert self.conn.get_data(f"{self.conn.base_url}meta/metrics").json() == {
            "message": "GET was a success"
        }

    @responses.activate
    def test_post_data(self):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}meta/metrics",
            json={"message": "POST was a success"},
        )
        assert self.conn.post_data(
            f"{self.conn.base_url}meta/metrics", payload={"filters": "some filtering"}
        ).json() == {"message": "POST was a success"}

    @responses.activate
    def test_get_status(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}status",
            json={"data": {"message": "Service is healthy", "healthy": True}},
        )
        assert self.conn.get_status() == "Service is healthy"

    @responses.activate
    def test_is_healthy(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}status",
            json={"data": {"message": "Service is healthy", "healthy": True}},
        )
        assert self.conn.is_healthy()

    @responses.activate
    def test_get_meta(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}meta",
            json={"data": "some meta info"},
        )
        assert self.conn.get_meta() == "some meta info"


class TestJobPostingsConnection(TestEmsiBaseConnection):
    conn = JobPostingsConnection()
    conn.base_url = "https://emsiservices.com/jpa/"
    conn.token = Token("super-secret-token")

    @responses.activate
    def test_post_totals(self, totals_data):
        # check the post_totals method
        responses.add(
            responses.POST,
            f"{self.conn.base_url}totals",
            json=totals_data,
        )
        totals_response = self.conn.post_totals(
            payload={
                "filter": {"when": {"start": "2020-01", "end": "2020-12"}},
                "metrics": ["median_salary", "unique_postings"],
            },
        )

        assert totals_response == totals_data["data"]["totals"]

    @responses.activate
    def test_post_timeseries(self, timeseries_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}timeseries",
            json=timeseries_data,
        )
        response = self.conn.post_timeseries(
            payload={
                "filter": {"when": {"start": "2020-01", "end": "2020-12"}},
                "metrics": ["median_salary", "unique_postings"],
            },
        )

        assert response == timeseries_data["data"]

    @responses.activate
    def test_get_rankings(self, rankings_get_data):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}rankings",
            json=rankings_get_data,
        )

        response = self.conn.get_rankings()
        assert response == rankings_get_data["data"]

    @responses.activate
    def test_post_rankings(self, rankings_post_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}rankings/company_name",
            json=rankings_post_data,
        )

        response = self.conn.post_rankings(
            facet="company_name",
            payload={
                "filter": {"when": {"start": "2020-01", "end": "2020-12"}},
                "rank": {"by": "unique_postings"},
            },
        )
        assert response == rankings_post_data

    @responses.activate
    def test_post_rankings_timeseries(self, rankings_timeseries_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}rankings/company_name/timeseries",
            json=rankings_timeseries_data,
        )

        response = self.conn.post_rankings_timeseries(
            facet="company_name",
            payload={
                "filter": {"when": {"start": "2020-01", "end": "2020-12"}},
                "rank": {"by": "unique_postings"},
                "timeseries": {"when": {"start": "2020-01-15", "end": "2020-01-20"}},
            },
        )
        assert response == rankings_timeseries_data["data"]

    @responses.activate
    def test_post_rankings_distributions(self, rankings_distributions_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}rankings/company_name/timeseries",
            json=rankings_distributions_data,
        )

        response = self.conn.post_rankings_timeseries(
            facet="company_name",
            payload={
                "filter": {"when": {"start": "2020-01", "end": "2023-12"}},
                "rank": {"by": "unique_postings", "limit": 2},
                "distribution": {
                    "type": "histogram",
                    "options": {"interval": 100000},
                    "metrics": ["duplicate_postings"],
                },
            },
        )
        assert response == rankings_distributions_data["data"]

    @responses.activate
    def test_post_nested_rankings(self, nested_rankings_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}rankings/company_name/rankings/title_name",
            json=nested_rankings_data,
        )

        response = self.conn.post_nested_rankings(
            facet="company_name",
            nested_facet="title_name",
            payload={
                "filter": {"when": {"start": "2020-01", "end": "2020-12"}},
                "rank": {"by": "unique_postings", "limit": 5},
                "nested_rank": {"by": "significance"},
            },
        )
        assert response == nested_rankings_data

    @responses.activate
    def test_post_postings(self, postings_post_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}postings",
            json=postings_post_data,
        )

        response = self.conn.post_postings(
            payload={"filter": {"when": {"start": "2020-01", "end": "2020-12"}}}
        )
        assert response == postings_post_data["data"]

    @responses.activate
    def test_get_postings(self, postings_get_data):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}postings/unique_id",
            json=postings_get_data,
        )

        response = self.conn.get_postings(posting_id="unique_id")
        assert response == postings_get_data["data"]

    @responses.activate
    def test_get_distributions(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}distributions",
            json={
                "data": [
                    "salary",
                    "posting_duration",
                    "min_years_experience",
                    "max_years_experience",
                ]
            },
        )

        distributions_response = self.conn.get_distributions()
        assert distributions_response == [
            "salary",
            "posting_duration",
            "min_years_experience",
            "max_years_experience",
        ]

    @responses.activate
    def test_post_distributions(self, distributions_data):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}distributions/salary",
            json=distributions_data,
        )

        response = self.conn.post_distributions(
            facet="salary",
            payload={
                "filter": {"when": "active"},
                "distribution": {
                    "type": "percentile",
                    "options": {"keys": [25, 50, 75]},
                    "metrics": ["unique_postings", "duplicate_postings"],
                },
            },
        )
        assert response == distributions_data["data"]

    @responses.activate
    def test_get_taxonomies(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}taxonomies",
            json={"data": ["cip2", "cip4", "cip6", "city"]},
        )

        response = self.conn.get_taxonomies()
        assert response == ["cip2", "cip4", "cip6", "city"]

    @responses.activate
    def test_get_taxonomies_facet(self):
        responses.add(
            responses.GET,
            f"{self.conn.base_url}taxonomies/title?q=data+sci",
            json={
                "data": [
                    {
                        "id": "ET3B93055220D592C8",
                        "name": "Data Scientists",
                        "properties": {
                            "singular_name": "Data Scientist",
                            "unique_postings": 2293,
                        },
                        "score": 8.407919,
                    },
                    {
                        "id": "ETFCE878A7B95881A6",
                        "name": "Data Specialists",
                        "properties": {
                            "singular_name": "Data Specialist",
                            "unique_postings": 1683,
                        },
                        "score": 5.7275753,
                    },
                ]
            },
        )

        response = self.conn.get_taxonomies(facet="title", q="data sci")
        assert response == [
            {
                "id": "ET3B93055220D592C8",
                "name": "Data Scientists",
                "properties": {
                    "singular_name": "Data Scientist",
                    "unique_postings": 2293,
                },
                "score": 8.407919,
            },
            {
                "id": "ETFCE878A7B95881A6",
                "name": "Data Specialists",
                "properties": {
                    "singular_name": "Data Specialist",
                    "unique_postings": 1683,
                },
                "score": 5.7275753,
            },
        ]

    @responses.activate
    def test_post_taxonomies(self):
        responses.add(
            responses.POST,
            f"{self.conn.base_url}taxonomies/title/lookup",
            json={
                "data": [
                    {
                        "id": "ET3B93055220D592C8",
                        "name": "Data Scientists",
                        "properties": {
                            "singular_name": "Data Scientist",
                            "unique_postings": 2293,
                        },
                    }
                ]
            },
        )

        response = self.conn.post_taxonomies(
            facet="title", payload={"ids": ["ETEB3BB8E555C79368"]}
        )
        assert response == [
            {
                "id": "ET3B93055220D592C8",
                "name": "Data Scientists",
                "properties": {
                    "singular_name": "Data Scientist",
                    "unique_postings": 2293,
                },
            },
        ]
