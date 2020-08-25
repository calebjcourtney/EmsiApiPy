# thanks to Paolo Rovelli for this: https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/27876800#27876800
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from apis.openSkills import SkillsClassificationConnection

skills_conn = SkillsClassificationConnection()


def test_get_status():
    response = skills_conn.get_status()

    assert response.json()['data']['message'] == 'Service is healthy'


def test_get_is_healthy():
    response = skills_conn.is_healthy()

    assert response is True


def test_get_versions():
    response = skills_conn.get_versions()

    assert len(response['data']) >= 38


def test_get_version_metadata():
    response = skills_conn.get_version_metadata()

    assert float(response['data']['version']) >= 7.2


def test_get_list_all_skills():
    response = skills_conn.get_list_all_skills()

    assert len(response['data']) > 29000


def test_post_list_requested_skills():
    skills = "{ \"ids\": [ \"KS1200364C9C1LK3V5Q1\", \"KS1275N74XZ574T7N47D\", \"KS125QD6K0QLLKCTPJQ0\" ] }"
    response = skills_conn.post_list_requested_skills(payload = skills)

    assert len(response['data']) == 3


def test_get_skill_by_id():
    skill_id = 'KS125LS6N7WP4S6SFTCK'
    response = skills_conn.get_skill_by_id(skill_id = skill_id)

    assert response['data']['name'] == 'Python (Programming Language)'


def test_post_find_related_skills():
    skills = ["KS1200364C9C1LK3V5Q1", "KS1275N74XZ574T7N47D", "KS125QD6K0QLLKCTPJQ0"]
    response = skills_conn.post_find_related_skills(skill_ids = skills)

    assert len(response['data']) > 1


def test_post_extract():
    job_description = "{ \"text\": \"... Great candidates also have\\n\\n Experience with a particular JS MV* framework (we happen to use React)\\n Experience working with databases\\n Experience with AWS\\n Familiarity with microservice architecture\\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...\"}"

    response = skills_conn.post_extract(description = job_description)
    for skill in ['JavaScript (Programming Language)', 'React.js', 'Amazon Web Services', 'Cascading Style Sheets (CSS)']:
        assert skill in [d['name'] for d in [e['skill'] for e in response['data']]]


def test_post_extract_with_source():
    job_description = "{ \"text\": \"... Great candidates also have\\n\\n Experience with a particular JS MV* framework (we happen to use React)\\n Experience working with databases\\n Experience with AWS\\n Familiarity with microservice architecture\\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...\"}"

    response = skills_conn.post_extract_with_source(description = job_description)

    assert len(response['data']) > 0
