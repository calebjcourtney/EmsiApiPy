# thanks to Paolo Rovelli for this: https://stackoverflow.com/questions/11536764/how-to-fix-attempted-relative-import-in-non-package-even-with-init-py/27876800#27876800
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from apis.openSkills import SkillsClassificationConnection

skills_conn = SkillsClassificationConnection()


def test_get_status():
    response = skills_conn.get_status()

    assert response.text == 'OK'


def test_get_documentation():
    response = skills_conn.get_documentation()

    assert len(response) > 0

def test_get_changelog():
    response = skills_conn.get_changelog()

    assert len(response) > 0


def test_get_versions():
    response = skills_conn.get_versions()

    assert len(response) >= 38


def test_get_list_all_skills():
    response = skills_conn.get_list_all_skills()

    assert len(response['skills']) > 29000

def test_post_list_requested_skills():
    skills = "{\"skills\" : [{\"id\":\"KS1200364C9C1LK3V5Q1\"},{\"id\":\"KS1275N74XZ574T7N47D\"}, {\"id\":\"KS125QD6K0QLLKCTPJQ0\"}]}"
    response = skills_conn.post_list_requested_skills(payload = skills)

    assert len(response['skills']) == 3


def test_get_search_skills():
    response = skills_conn.get_search_skills(skill_name = 'python')

    assert len(response['skills']) > 1


def test_get_skills_fields():
    fields = {"fields":"id,tags"}
    skills = "{\"skills\" : [{\"id\":\"KS1200364C9C1LK3V5Q1\"}, {\"id\":\"KS1275N74XZ574T7N47D\"}, {\"id\":\"KS125QD6K0QLLKCTPJQ0\"}]}"
    response = skills_conn.post_list_requested_skills(payload = skills, querystring = fields)

    assert len(response['skills']) == 3


def test_get_skill_by_id():
    skill_id = 'KS125LS6N7WP4S6SFTCK'
    response = skills_conn.get_skill_by_id(skill_id = skill_id)

    assert response['name'] == 'Python (Programming Language)'

def test_get_fields():
    response = skills_conn.get_fields()

    for field in ['id', 'name', 'tags', 'type', 'default']:
        assert field in [d['key'] for d in response['fields']]

def test_get_skill_types():
    response = skills_conn.get_skill_types()

    for skill_type in ['Hard Skill', 'Certification', 'Soft Skill']:
        assert skill_type in [d['name'] for d in response['types']]

def test_post_extract():
    job_description = "{\"full_text\" : \"... Great candidates also have\n\n Experience with a particular JS MV* framework (we happen to use React)\n Experience working with databases\n Experience with AWS\n Familiarity with microservice architecture\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...\"}"

    response = skills_conn.post_extract(description = job_description)
    for skill in ['JavaScript (Programming Language)', 'React.js', 'Amazon Web Services', 'Cascading Style Sheets (CSS)']:
        assert skill in [d['name'] for d in [e['skill'] for e in response['skills']]]

def test_post_extract_with_source():
    job_description = "{\"full_text\" : \"... Great candidates also have\n\n Experience with a particular JS MV* framework (we happen to use React)\n Experience working with databases\n Experience with AWS\n Familiarity with microservice architecture\n Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS ...\"}"

    response = skills_conn.post_extract_with_source(description = job_description)

    assert len(response['trace']) > 0
