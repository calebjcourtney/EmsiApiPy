# Emsi Skills
```python
import EmsiApiPy

conn = EmsiApiPy.SkillsClassificationConnection()

# make sure we have a good connection
assert conn.is_healthy()

# get a list of all the skills
print(conn.get_list_all_skills()["data"][:])
"""
[
  {
    "id": "KS120P86XDXZJT3B7KVJ",
    "infoUrl": "https://skills.emsidata.com/skills/KS120P86XDXZJT3B7KVJ",
    "name": "(American Society For Quality) ASQ Certified",
    "type": {
      "id": "ST3",
      "name": "Certification"
    }
  },
  {
    "id": "KS126XS6CQCFGC3NG79X",
    "infoUrl": "https://skills.emsidata.com/skills/KS126XS6CQCFGC3NG79X",
    "name": ".NET Assemblies",
    "type": {
      "id": "ST1",
      "name": "Hard Skill"
    }
  },
  ...
]
"""

# search the library for any skills with the name of "python" in them
print(conn.get_list_all_skills(q="python"))
"""
{
  "data": [
    {
      "id": "KS125LS6N7WP4S6SFTCK",
      "infoUrl": "https://skills.emsidata.com/skills/KS125LS6N7WP4S6SFTCK",
      "name": "Python (Programming Language)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      }
    },
    {
      "id": "KSGWPO6DSN70GRY20JFT",
      "infoUrl": "https://skills.emsidata.com/skills/KSGWPO6DSN70GRY20JFT",
      "name": "Pandas (Python Package)",
      "type": {
        "id": "ST1",
        "name": "Hard Skill"
      }
    },
    ...
  ]
}
"""

# extract skills from text
text = """
Full Stack Web Developer

If you're ready to join a high-functioning team of full stack devs working closely with product managers, data engineers, and designers to create interfaces and visualizations that make nuanced data intelligible, we'd love to hear from you.

Candidates must have

    Experience with the front-end basics: HTML5, CSS3, and JS
    Experience using a version control system
    Familiarity with MV* frameworks, e.g. React, Ember, Angular, Vue
    Familiarity with server-side languages like PHP, Python, or Node

Great candidates also have

    Experience with a particular JS MV* framework (we happen to use React)
    Experience working with databases
    Experience with AWS
    Familiarity with microservice architecture
    Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS

People who succeed in this position are

    Team oriented and ready to work closely with other developers
    Determined to produce clean, well-tested code
    Comfortable with working in rapid development cycles
    Skilled oral and written communicators
    Enthusiastic for learning and pushing the envelope
""".encode("utf-8").decode("utf-8", "strict")

print(conn.post_extract(text))
"""
{
  "data": [
    {
      "confidence": 1.0,
      "skill": {
        "id": "KS440H66BML35BBRFCTK",
        "infoUrl": "https://skills.emsidata.com/skills/KS440H66BML35BBRFCTK",
        "name": "Server-Side",
        "tags": [
          {
            "key": "wikipediaExtract",
            "value": "Server-side refers to operations that are performed by the server in a client–server relationship in a computer network."
          },
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/Server-Side"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    {
      "confidence": 1.0,
      "skill": {
        "id": "KSMNXY6MPS1EDWJ8P6B0",
        "infoUrl": "https://skills.emsidata.com/skills/KSMNXY6MPS1EDWJ8P6B0",
        "name": "Enthusiasm",
        "tags": [],
        "type": {
          "id": "ST2",
          "name": "Soft Skill"
        }
      }
    },
    {
      "confidence": 1.0,
      "skill": {
        "id": "KSDJCA4E89LB98JAZ7LZ",
        "infoUrl": "https://skills.emsidata.com/skills/KSDJCA4E89LB98JAZ7LZ",
        "name": "React.js",
        "tags": [
          {
            "key": "wikipediaExtract",
            "value": "React is an open-source JavaScript library for building user interfaces or UI components. It is maintained by Facebook and a community of individual developers and companies.\nReact can be used as a base in the development of single-page or mobile applications. However, React is only concerned with rendering data to the DOM, and so creating React applications usually requires the use of additional libraries for state management and routing. Redux and React Router are respective examples of such libraries."
          },
          {
            "key": "wikipediaUrl",
            "value": "https://en.wikipedia.org/wiki/React.js"
          }
        ],
        "type": {
          "id": "ST1",
          "name": "Hard Skill"
        }
      }
    },
    ...
  ]
}
"""

```
