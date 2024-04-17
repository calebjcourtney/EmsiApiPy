import pytest
import responses
import pandas as pd

from permissions import DEFAULT

DEFAULT["username"] = "test-user"
DEFAULT["password"] = "test-password"


@pytest.fixture
def token():
    from EmsiApiPy.base import Token

    return Token("super-secret-token")


@pytest.fixture
def totals_data():
    return {"data": {"totals": {"median_salary": 57024, "unique_postings": 46990}}}


@pytest.fixture
def timeseries_data():
    return {
        "data": {
            "timeseries": {
                "duplicate_postings": [
                    1189,
                    1032,
                    889,
                    741,
                    1160,
                    1696,
                    2082,
                    2409,
                    1991,
                    1292,
                    995,
                    930,
                ],
                "month": [
                    "2020-01",
                    "2020-02",
                    "2020-03",
                    "2020-04",
                    "2020-05",
                    "2020-06",
                    "2020-07",
                    "2020-08",
                    "2020-09",
                    "2020-10",
                    "2020-11",
                    "2020-12",
                ],
                "unique_postings": [
                    300,
                    207,
                    171,
                    127,
                    167,
                    186,
                    225,
                    279,
                    259,
                    202,
                    162,
                    179,
                ],
            },
            "totals": {"duplicate_postings": 4911, "unique_postings": 965},
        }
    }


@pytest.fixture
def rankings_get_data():
    return {
        "data": [
            "certifications",
            "certifications_name",
            "city",
            "city_name",
            "cip2",
            "cip2_name",
            "cip4",
            "cip4_name",
            "cip6",
            "cip6_name",
            "company",
            "company_name",
            "county",
            "county_name",
            "edulevels",
            "edulevels_name",
            "employment_type",
            "employment_type_name",
            "fips",
            "fips_name",
            "specialized_skills",
            "specialized_skills_name",
            "common_skills",
            "common_skills_name",
            "max_years_experience",
            "min_years_experience",
            "msa",
            "msa_name",
            "msa_skill_cluster",
        ]
    }


@pytest.fixture
def rankings_post_data():
    return {
        "data": {
            "ranking": {
                "buckets": [
                    {
                        "duplicate_postings": 6559,
                        "name": "Geisinger Inc",
                        "unique_postings": 722,
                    },
                    {
                        "duplicate_postings": 2938,
                        "name": "Community Health Systems, Inc.",
                        "unique_postings": 590,
                    },
                    {
                        "duplicate_postings": 4381,
                        "name": "Army National Guard",
                        "unique_postings": 320,
                    },
                    {
                        "duplicate_postings": 217,
                        "name": "Soliant Health, Inc",
                        "unique_postings": 263,
                    },
                    {
                        "duplicate_postings": 442,
                        "name": "Allied Services, L.L.C.",
                        "unique_postings": 202,
                    },
                ],
                "facet": "company_name",
                "limit": 5,
                "rank_by": "unique_postings",
            },
            "totals": {"duplicate_postings": 85990, "unique_postings": 20023},
        }
    }


@pytest.fixture
def rankings_timeseries_data():
    return {
        "data": {
            "ranking": {
                "buckets": [
                    {
                        "duplicate_postings": 6559,
                        "name": "Geisinger Inc",
                        "timeseries": {
                            "day": [
                                "2020-01-15",
                                "2020-01-16",
                                "2020-01-17",
                                "2020-01-18",
                                "2020-01-19",
                                "2020-01-20",
                            ],
                            "unique_postings": [189, 190, 196, 196, 201, 200],
                        },
                        "unique_postings": 722,
                    },
                    {
                        "duplicate_postings": 2938,
                        "name": "Community Health Systems, Inc.",
                        "timeseries": {
                            "day": [
                                "2020-01-15",
                                "2020-01-16",
                                "2020-01-17",
                                "2020-01-18",
                                "2020-01-19",
                                "2020-01-20",
                            ],
                            "unique_postings": [139, 137, 138, 142, 143, 143],
                        },
                        "unique_postings": 590,
                    },
                    {
                        "duplicate_postings": 4381,
                        "name": "Army National Guard",
                        "timeseries": {
                            "day": [
                                "2020-01-15",
                                "2020-01-16",
                                "2020-01-17",
                                "2020-01-18",
                                "2020-01-19",
                                "2020-01-20",
                            ],
                            "unique_postings": [84, 85, 85, 85, 86, 85],
                        },
                        "unique_postings": 320,
                    },
                    {
                        "duplicate_postings": 217,
                        "name": "Soliant Health, Inc",
                        "timeseries": {
                            "day": [
                                "2020-01-15",
                                "2020-01-16",
                                "2020-01-17",
                                "2020-01-18",
                                "2020-01-19",
                                "2020-01-20",
                            ],
                            "unique_postings": [46, 44, 44, 46, 46, 46],
                        },
                        "unique_postings": 263,
                    },
                    {
                        "duplicate_postings": 442,
                        "name": "Allied Services, L.L.C.",
                        "timeseries": {
                            "day": [
                                "2020-01-15",
                                "2020-01-16",
                                "2020-01-17",
                                "2020-01-18",
                                "2020-01-19",
                                "2020-01-20",
                            ],
                            "unique_postings": [76, 77, 78, 78, 78, 78],
                        },
                        "unique_postings": 202,
                    },
                ],
                "facet": "company_name",
                "limit": 5,
                "rank_by": "unique_postings",
            },
            "totals": {"duplicate_postings": 85990, "unique_postings": 20023},
        }
    }


@pytest.fixture
def rankings_distributions_data():
    return {
        "data": {
            "ranking": {
                "buckets": [
                    {
                        "distribution": {
                            "buckets": [
                                {"duplicate_postings": 13156784, "key": 1, "value": 0},
                                {
                                    "duplicate_postings": 2464553,
                                    "key": 2,
                                    "value": 100000,
                                },
                                {
                                    "duplicate_postings": 187126,
                                    "key": 3,
                                    "value": 200000,
                                },
                                {
                                    "duplicate_postings": 41355,
                                    "key": 4,
                                    "value": 300000,
                                },
                                {"duplicate_postings": 8025, "key": 5, "value": 400000},
                                {"duplicate_postings": 2780, "key": 6, "value": 500000},
                            ],
                            "domain": {"max": 500000, "min": 15100},
                            "facet": "salary",
                            "interval": 100000,
                            "type": "histogram",
                        },
                        "name": "Unclassified",
                        "unique_postings": 18621508,
                    },
                    {
                        "distribution": {
                            "buckets": [
                                {"duplicate_postings": 5650866, "key": 1, "value": 0},
                                {
                                    "duplicate_postings": 17838,
                                    "key": 2,
                                    "value": 100000,
                                },
                                {"duplicate_postings": 1490, "key": 3, "value": 200000},
                                {"duplicate_postings": 183, "key": 4, "value": 300000},
                                {"duplicate_postings": 8, "key": 5, "value": 400000},
                                {"duplicate_postings": 69, "key": 6, "value": 500000},
                            ],
                            "domain": {"max": 500000, "min": 17680},
                            "facet": "salary",
                            "interval": 100000,
                            "type": "histogram",
                        },
                        "name": "Amazon",
                        "unique_postings": 1257477,
                    },
                ],
                "facet": "company_name",
                "limit": 2,
                "rank_by": "unique_postings",
            },
            "totals": {"unique_postings": 163400492},
        }
    }


@pytest.fixture
def nested_rankings_data():
    return {
        "data": {
            "ranking": {
                "buckets": [
                    {
                        "duplicate_postings": 6559,
                        "name": "Geisinger Inc",
                        "ranking": {
                            "buckets": [
                                {
                                    "name": "Specialty Clinic Licensed Practical Nurses",
                                    "significance": 151.9881157958914,
                                    "unique_postings": 5,
                                },
                                {
                                    "name": "Evaluation Assistants",
                                    "significance": 125.88211732387495,
                                    "unique_postings": 4,
                                },
                                {
                                    "name": "Licensed Registered Nurses",
                                    "significance": 98.38387034949157,
                                    "unique_postings": 8,
                                },
                                {
                                    "name": "Medical Surgical Oncology Registered Nurses",
                                    "significance": 94.84830283499103,
                                    "unique_postings": 10,
                                },
                                {
                                    "name": "Operating Room Aides",
                                    "significance": 94.40743286825246,
                                    "unique_postings": 6,
                                },
                            ],
                            "facet": "title_name",
                            "limit": 5,
                            "rank_by": "significance",
                        },
                        "unique_postings": 722,
                    },
                    {
                        "duplicate_postings": 2938,
                        "name": "Community Health Systems, Inc.",
                        "ranking": {
                            "buckets": [
                                {
                                    "name": "Nurse Extenders",
                                    "significance": 233.672283347697,
                                    "unique_postings": 7,
                                },
                                {
                                    "name": "Courtesy Drivers",
                                    "significance": 133.5236292253184,
                                    "unique_postings": 6,
                                },
                                {
                                    "name": "Behavioral Health Workers",
                                    "significance": 115.87300679197276,
                                    "unique_postings": 9,
                                },
                                {
                                    "name": "Medical Services Representatives",
                                    "significance": 114.45415192678624,
                                    "unique_postings": 2,
                                },
                                {
                                    "name": "Event Sales Planners",
                                    "significance": 66.76520444316768,
                                    "unique_postings": 1,
                                },
                            ],
                            "facet": "title_name",
                            "limit": 5,
                            "rank_by": "significance",
                        },
                        "unique_postings": 590,
                    },
                    {
                        "duplicate_postings": 4381,
                        "name": "Army National Guard",
                        "ranking": {
                            "buckets": [
                                {
                                    "name": "Geospatial Engineers",
                                    "significance": 236.71707954494437,
                                    "unique_postings": 11,
                                },
                                {
                                    "name": "Track Vehicle Repairers",
                                    "significance": 215.64496055403308,
                                    "unique_postings": 11,
                                },
                                {
                                    "name": "Multi-Channel Transmission Systems Operators/Maintainers",
                                    "significance": 151.28722439236114,
                                    "unique_postings": 8,
                                },
                                {
                                    "name": "Fire Support Specialists",
                                    "significance": 148.92609588623046,
                                    "unique_postings": 7,
                                },
                                {
                                    "name": "Air Defense Battle Management System Operators",
                                    "significance": 94.2697801983173,
                                    "unique_postings": 3,
                                },
                            ],
                            "facet": "title_name",
                            "limit": 5,
                            "rank_by": "significance",
                        },
                        "unique_postings": 320,
                    },
                    {
                        "duplicate_postings": 217,
                        "name": "Soliant Health, Inc",
                        "ranking": {
                            "buckets": [
                                {
                                    "name": "Gifted Education Teachers",
                                    "significance": 697.8579777290183,
                                    "unique_postings": 3,
                                },
                                {
                                    "name": "Preschool Speech Language Pathologists",
                                    "significance": 226.79614314215908,
                                    "unique_postings": 3,
                                },
                                {
                                    "name": "Coverage Specialists",
                                    "significance": 201.6029088175339,
                                    "unique_postings": 1,
                                },
                                {
                                    "name": "Special Education Specialists",
                                    "significance": 174.45593929917473,
                                    "unique_postings": 3,
                                },
                                {
                                    "name": "Paraprofessionals/Teaching Assistants",
                                    "significance": 168.0017903010501,
                                    "unique_postings": 1,
                                },
                            ],
                            "facet": "title_name",
                            "limit": 5,
                            "rank_by": "significance",
                        },
                        "unique_postings": 263,
                    },
                    {
                        "duplicate_postings": 442,
                        "name": "Allied Services, L.L.C.",
                        "ranking": {
                            "buckets": [
                                {
                                    "name": "Transitional Interns",
                                    "significance": 3417.5311734143716,
                                    "unique_postings": 2,
                                },
                                {
                                    "name": "Assistant Directors of Health Information Management",
                                    "significance": 1708.7655867071858,
                                    "unique_postings": 1,
                                },
                                {
                                    "name": "Residence Assistants",
                                    "significance": 1708.7655867071858,
                                    "unique_postings": 1,
                                },
                                {
                                    "name": "Skilled Nursing Registered Nurses",
                                    "significance": 798.1785612831718,
                                    "unique_postings": 16,
                                },
                                {
                                    "name": "Allied Physical Therapists",
                                    "significance": 759.4436710997832,
                                    "unique_postings": 2,
                                },
                            ],
                            "facet": "title_name",
                            "limit": 5,
                            "rank_by": "significance",
                        },
                        "unique_postings": 202,
                    },
                ],
                "facet": "company_name",
                "limit": 5,
                "rank_by": "unique_postings",
            },
            "totals": {"duplicate_postings": 85990, "unique_postings": 20023},
        }
    }


@pytest.fixture
def postings_post_data():
    return {
        "data": {
            "limit": 5,
            "page": 1,
            "pages_available": 2,
            "postings": [
                {
                    "body": "<!--id: bc143b36b07b49c9b6e02895ba1e489e--> Data Analyst 2020-01-22T08:03:51Z Harvard University Credit Union Responsibilities include: <ul><li> Write, maintain and support a variety of lists and reports utilizing appropriate reporting tools. </li><li> Acquire data from primary or secondary data sources and maintain databases/data systems. </li><li> Assist in the creation of member segmentation tools and targeted marketing lists. </li><li> Assist in ongoing market research efforts and development of new research tools. </li><li> Enhance and maintain data collection processes to optimize statistical efficiency and data quality. </li><li> Work with Retail and Operational staff to ensure consistency and accuracy of data collection. </li><li> Audit data from various systems to ensure data is collected appropriately and maintain data integrity. </li><li> Identify and analyze trends or patterns in complex data sets. </li><li> Provide ongoing tracking of key metrics. </li><li> Share findings through effective reporting of data output to various stakeholders throughout the organization. </li><li> Other duties as assigned.</li></ul> <h5>Please note:</h5> Harvard University requires a pre-employment reference and background screening, which includes OFAC (Office of Foreign Assets Control) check . <ul><li> Harvard University is unable to provide work authorization and/or visa sponsorship. </li><li> This position has a 90-day orientation and review period.</li></ul> Harvard University Employees Credit Union website : https://www.huecu.org/ The Harvard University Employees Credit Union (HUECU) is one of the fastest growing Credit Unions in the country and a leader in our industry. As a not-for-profit cooperative, we put our members' best interests first in all that we do. We are passionate about service and fanatical about solving problems. Integrity and transparency are the foundation of HUECU's philosophy. Our mission is to enhance our members' lives by developing and offering trustworthy products that are easy to understand, easy to use and best suited to meet their financial needs. HUECU has a dynamic small-business atmosphere where every member of the team has a significant impact on our success. Our headquarters and flagship branch are located in the heart of Harvard Square, surrounded by shops, restaurants, and the vibrant University community. HUECU staff are employed by Harvard University and enjoy competitive salaries and a robust benefits package. We're looking for talented, member-centric stars to join our growing team. If you have energy, enthusiasm, and thrive in a fast-paced environment, you should check out the career opportunities with HUECU. Harvard University offers an outstanding benefits package including, but not limited to: <h5>Time Off:</h5> 3 - 4 weeks paid vacation, a paid winter recess break, 12 paid sick days, 11.5 paid holidays, and 3 paid personal days per year. <h5>Medical/Dental/Vision plans:</h5> We offer a variety of excellent medical plans, dental &amp; vision plans, all coverage begins as of your start date. <h5>Retirement:</h5> University-funded retirement plan with full vesting after 3 years of service. <h5>Tuition Assistance Programs:</h5> Competitive tuition assistance program, $40 per class at the Harvard Extension School and discounted options through participating Harvard grad schools. <h5>Transportation:</h5> Harvard offers a 50% subsidized MBTA pass as well as additional options to assist employees in their daily commute. Wellness options : Harvard offers programs and classes at little or no cost, including stress management, massages, nutrition, meditation and complimentary health services. Harvard access to athletic facilities, libraries, campus events and many discounts throughout the metro Boston area. For more information on Total Rewards at Harvard visit: https://hr.harvard.edu/totalrewards <h5>Salary Grade:</h5> 053 <h5>Union:</h5> 55 - Hvd Union Cler &amp; Tech Workers <ul><li> High School Diploma </li><li> A minimum of one year of professional related experience, preferably within a financial services industry. </li><li> Bachelor's Degree preferred. Major in Mathematics, Statistics or related field strongly preferred. </li><li> Strong ability to work with numbers </li><li> Analytical mind, able to process information logically </li><li> Advanced computer software knowledge, particularly MS Excel, and high level of comfort learning new software </li><li> Highly organized with a meticulous attention to detail </li><li> Ability to work independently with minimal supervision. </li><li> Ability to work collaboratively with cross-functional teams </li></ul><h5>EQUAL OPPORTUNITY EMPLOYER</h5> We are an equal opportunity employer and all qualified applicants will receive consideration for employment without regard to race, color, religion, sex, national origin, disability status, protected veteran status, or any other characteristic protected by law.",
                    "city_name": "Boston, MA",
                    "company_name": "Harvard University",
                    "expired": "2020-01-26",
                    "id": "bc143b36b07b49c9b6e02895ba1e489e",
                    "posted": "2020-01-22",
                    "score": 0,
                    "title_raw": "Data Analyst",
                    "url": [],
                },
                {
                    "body": "<!--id: a89e44c28b0944569954c3b6a0f429b7--> Strategic Partnerships Manager, Venture Capital/Private Equity Boston, MA 4.0 1 hour ago Full-time Quick Apply Skills Private Equity Business Development Investment Banking Negotiation InsightSquared is the leading sales and marketing analytics provider for growing companies that want to run their business by the numbers. We help our customers make better decisions by equipping them with actionable, real-time intelligence that drives predictable growth. We're funded by a great team of investors including Accomplice, Tola Capital, DFJ, Bessemer, and Salesforce.com. We were named a leader in the G2 Crowd's Business Intelligence Platform GridSM, ranking #1 in customer satisfaction for the fourth year in a row. We are a four-time winner of both The Boston Business Journal's \"Best Places to Work\" and The Boston Globe's \"Top Places to Work.\" As Strategic Partnerships Manager, Venture Capital/Private Equity you will be a key member of our go-to-market organization tasked with maintaining and expanding our base of Private Equity and Venture Capital partnerships. You will report into the Head of BD, Alliances &amp; Investor Partnerships and assist in targeting new partnership opportunities and maintain existing ones by managing relationships with Investors and Operating Partners at PE/VC firms with the aim of expanding InsightSquared's footprint within their portfolios. <h5>Responsibilities:</h5> Assist in the targeting of new PE/VC partner prospects, the negotiation of new partnerships, and the development of commercial agreements Work with new partners to develop launch strategy for new partnerships Assist in overseeing the health of existing PE/VC partner channel and manage partner performance by leading QBRs with delivery of quarterly reporting highlighting key metrics such as progress toward goals, portfolio penetration &amp; pipeline reviews Maintain active relationships with PE/VC firms to ensure continued engagement and maximization of new business lead flow for InsightSquared's sales team Work with PE/VC Partners to develop a best practices framework aligned with PE/VC Partner's value creation initiatives for portfolio company customers Collaborate internally with the Services team to oversee the development of new partner offerings (i.e. use-case expansion to support due-diligence, cross-portfolio dashboards, standardized board reports, etc.) Identify areas of success and opportunity for each partner, develop strategies to fuel future growth and optimize results of each partnership Sales enablement - develop presentations and other selling tools in partnership with Marketing (white papers, case studies, ROI calculators, etc.) which articulate the value of InsightSquared to PE/VC Partners and portfolio companies Lead the development of sales strategy and process to leverage master agreements and coach sales reps through full-cycle channel sales engagements. Collaborate with Customer Success, Support, &amp; Services teams to drive adoption and ensure success of portfolio company customers Advocate for partner demand and needs internally. Develop and effectively manage internal relationships necessary to reach mutually beneficial objectives and the cross-functional commitments to achieve them <h5>Qualifications:</h5> 2-5 years experience in partner management, sales, marketing or business development Prior experience with a strategy consulting firm, investment banking, private equity, or venture capital is a plus Demonstrated presentation, negotiation and persuasion skills Ability to lead and influence cross-functional teams InsightSquared is the leading sales and marketing analytics provider for growing companies that want to run their business by the numbers. We help our customers make better decisions by equipping them with actionable, real-time intelligence that drives predictable growth. We're funded by a great team of investors including Accomplice, Tola Capital, DFJ, Bessemer, and Salesforce.com. We were named a leader in the G2 Crowd's Business Intelligence Platform GridSM, ranking #1 in customer satisfaction for the fourth year in a row. We are a four-time winner of both The Boston Business Journal's \"Best Places to Work\" and The Boston Globe's \"Top Places to Work.\" As Strategic Partnerships Manager, Venture Capital/Private Equity you will be a key member of our go-to-market organization tasked with maintaining and expanding our base of Private Equity and Venture Capital partnerships. You will report into the Head of BD, Alliances &amp; Investor Partnerships and assist in targeting new partnership opportunities and maintain existing ones by managing relationships with Investors and Operating Partners at PE/VC firms with the aim of expanding InsightSquared's footprint within their portfolios. <h5>Responsibilities:</h5> Assist in the targeting of new PE/VC partner prospects, the negotiation of new partnerships, and the development of commercial agreements Work with new partners to develop launch strategy for new partnerships Assist in overseeing the health of existing PE/VC partner channel and manage partner performance by leading QBRs with delivery of quarterly reporting highlighting key metrics such as progress toward goals, portfolio penetration &amp; pipeline reviews Maintain active relationships with PE/VC firms to ensure continued engagement and maximization of new business lead flow for InsightSquared's sales team Work with PE/VC Partners to develop a best practices framework aligned with PE/VC Partner's value creation initiatives for portfolio company customers Collaborate internally with the Services team to oversee the development of new partner offerings (i.e. use-case expansion to support due-diligence, cross-portfolio dashboards, standardized board reports, etc.) Identify areas of success and opportunity for each partner, develop strategies to fuel future growth and optimize results of each partnership Sales enablement - develop presentations and other selling tools in partnership with Marketing (white papers, case studies, ROI calculators, etc.) which articulate the value of InsightSquared to PE/VC Partners and portfolio companies Lead the development of sales strategy and process to leverage master agreements and coach sales reps through full-cycle channel sales engagements. Collaborate with Customer Success, Support, &amp; Services teams to drive adoption and ensure success of portfolio company customers Advocate for partner demand and needs internally. Develop and effectively manage internal relationships necessary to reach mutually beneficial objectives and the cross-functional commitments to achieve them <h5>Qualifications:</h5> 2-5 years experience in partner management, sales, marketing or business development Prior experience with a strategy consulting firm, investment banking, private equity, or venture capital is a plus Demonstrated presentation, negotiation and persuasion skills Ability to lead and influence cross-functional teams Quick Apply • ID#: 768266835 • <h5>Location:</h5> Boston, MA • <h5>Type:</h5> Other • <h5>Company:</h5> InsightSquared",
                    "city_name": "Boston, MA",
                    "company_name": "Insightsquared, Inc",
                    "expired": "2020-03-18",
                    "id": "a89e44c28b0944569954c3b6a0f429b7",
                    "posted": "2020-01-28",
                    "score": 0,
                    "title_raw": "Strategic Partnerships Manager, Venture Capital/Private Equity",
                    "url": [],
                },
                {
                    "body": "<!--id: cda7a43ccdee44ada42704bf3b07f154--> Register Job Search Login FAQs Register Employer FAQs Login Apply for Jobs Apply for Jobs Post a Job Post a Job Local Jobs Home Register Here to Apply for Jobs or Post Jobs. X General Manager Job in Boston - MA Massachusetts - <h5>USA Apply Here Company:</h5> Related Full Time position Listed on 2020-08-26 Job specializations: <ul><li> Management Property Management </li><li> Real Estate/Property Property Management Job Description &amp; How to Apply Below Learn more about Related's innovated culture /434468879 </li></ul><h5>Role Summary:</h5> The Multi Property General Manager is responsible for leading all phases of operation of a three (3) residential buildings including, but not limited to, direct supervision and development of the onsite management team, financial performance to budget and accountability for the sales, resident relations and maintenance functions. This position ensures that Company standards are maintained across Related Rentals. The position provides inspirational leadership, successfully promotes Company values, and creates an environment of exceptional customer service for residents, prospects, and vendors. <ul><li> Understands and manages capital and expense budgets, including reporting to senior staff and stakeholder representatives. </li><li> Maintains verbal and written communication with stakeholders, vendors and residents (as needed) on issues relating to our management responsibilities, including but not limited to: quality control; vendor contract management; maintenance personnel responsibilities; access control for mechanical equipment rooms and utilities management. </li><li> Oversees all construction activities during initial development/lease up of the property </li><li> During construction and fit-outs, makes recommendations to eliminate potential problems and/or improve building operations. </li><li> Develops policies, procedures, and regulations to effectively manage the property, pertaining but not limited to, construction work, tenant alteration process and certificate of insurance requirements. </li><li> Develops, implements and assures continued implementation of preventive maintenance programs. </li><li> Assures that all outside vendors are in compliance with the tenets of their contractual agreements for all work performed. </li><li> Ensures that each staff member reviews and complies with the procedures outlined in the Emergency Preparedness Manual. </li><li> Develops and manages all contracts, i.e. Waste Removal, Janitorial and Electrical. </li><li> Supervises and coordinates loading dock access and deliveries. </li><li> Comprehensive understanding of all facets of accounts payable and account receivable in order to effectively supervise staff responsible for this function. </li><li> Confirm that the appropriate allocation methodology is established and ensure that all invoices are coded to and paid from the appropriate entity. </li><li> Ensures that all invoices are processed for timely payment in order to maintain good vendor relations and accounts. </li><li> Reviews and approves purchase orders that exceed amounts over site staff level up to designated approval limit of $1000. </li><li> Ensures that proper insurance documentation for all outside vendors is collect and available for supervisory review. </li><li> Participates in preparation of initial draft of the annual and capital operating budgets for the rental and overall condo entities.</li></ul>Prepares the monthly variance reports for the rental, co-op and overallcondentities. <ul><li> Ensures that budgetary guidelines approved for controllable expenses are met. </li><li> Ensures that staff is fully aware of budgetary goals and constraints. </li><li> Responsible for overseeing all maintenance operations and repairs at the property. </li><li> Responsible for the successful coordination of all move-in/move-outs. </li><li> Service Request System - Facilities </li><li> Confirms timely, efficient completion of all service requests. </li><li> As a general rule, resident-requested service requests should be completed within twenty-four (24) hours. Emergency repairs are addressed promptly, in particular when those situations may cause increasing damage to the property or may endanger the residents' health and safety. </li><li> All completed service requests are signed and placed in the respective resident files to provide documentation of requested services. </li><li> If appropriate, confirms that damage charges are applied to the resident's account for repairs attributable to cause beyond normal wear and tear. </li><li> Ensures that proper key control systems and procedures are in place at all times </li><li> Product Presentation </li><li> Apartment turnovers must produce units that are impeccably clean, painted, and mechanically in good working order prior to the pending move-in. </li><li> A resident survey that queries the conditions of the apartments and the residents' perceptions of the servicesRMCprovides is administered and distributed from the main office annually. Responsible to confirm that any deficiencies noted on the responses have been addressed and assures residents' satisfaction with the service. </li><li> Maintenance of Common Areas </li><li> Common areas, such as laundry rooms, hallways, offices, shops, storage areas, refuse areas, and grounds must be clean at all times. </li><li> Confirms that the routine janitorial schedule is maintained to ensure that the noted expectations are consistently met. </li><li> External Maintenance Services Under the supervision of the Vice President, solicits, reviews </li></ul><h5>Benefits:</h5> <ul><li> Incentive bonus program </li><li> Training and development programs </li><li> Benefits including: Medical, Dental, Life &amp; Disability, Paid Time Off, 401(K), Flexible Spending Accounts </li><li> Employee Recognition &amp; Wellness Programs Qualifications </li><li> Five (5) years of knowledge of property management compliance practice and procedures related to Class A and Affordable property preferred. </li><li> Experience in an affordable housing processing or demonstrate transferable skills </li><li> Demonstrate ability to learn recertification policies, procedures and principles </li><li> Experience in budget preparation and financial reporting, with a strong understanding of building operational systems, leasing and marketing, documentation and administration </li><li> Minimum of five (5) years' experience managing a team of people </li><li> Ability to manage a property as demonstrated by work experience including financial performance, customer service, communications, marketing, negotiation, crisis management, and staffing. </li><li> Ability to analyze data/reports to develop solutions to sustain high standards of customer service, optimal revenue generation and effective expense management as demonstrated by business results in previous position. </li><li> Ability to successfully resolve resident issues as demonstrated by work experience. </li><li> Ability to negotiate and manage contracts with 3rd party service providers as demonstrated by previous work experience. </li><li> Ability to supervise and develop employees and provide feedback and coaching to subordinates resulting in improved performance as demonstrated by experience in previous position. </li><li> Ability to work a flexible schedule; any day of the week, including being \"on-call\". </li><li> Ability to write and communicate professionally in English. </li><li> Ability to apply critical thinking and sound decision-making. </li><li> Ability to resolve residents' concerns while maintaining a friendly and professional demeanor. </li><li> Ability to demonstrate project management skills to ensure tasks are completed on schedule. </li><li> Ability to communicate professionally and adapt interpersonal skills to a variety of audiences. </li><li> Ability to demonstrate teamwork by assisting co-workers and direct reports. </li><li> Ability to provide coaching to direct reports to develop their knowledge and skill-set. </li><li> Ability to effectively convey ideas and influence the opinions of others. </li><li> Ability to demonstrate computer literacy using Microsoft Office software.</li></ul> Overview Related Management Company is the owner and operator of a premier portfolio of assets valued at over $60 billion. Our operating portfolio consists of a diversified mix of properties including luxury rental buildings, retail and commercial space, luxury condominium residences, affordable, and workforce housing located throughout the United States. As the owner and developer for the majority of the RMC portfolio, we have ensured that our buildings are the best assets in their respective submarkets. We provide a diligently maintained property management platform with dedicated professionals who consistently exceeds our residents' and commercial tenants' expectations. Our dedication to providing the highest and most personalized level of service is one of the hallmarks of the company and a key differentiator in the market. For more please visit (Please contact us using the \"Apply for this Job Posting\" box below) Related is an Equal Opportunity Employer For information about how we use your personal information, including information submitted for career opportunities, please review our Privacy Policy at https:// . Related is an Equal Employment Opportunity Employer and participates in E-Verify Position Requirements 1 to 2 Years work experience Go to Application Site Search for further <h5>Jobs Here:</h5> × [<h5>INS:</h5> :<br><br>INS] <h5>LANGUAGE ES DE</h5> Terms &amp; Privacy Policy Refund Policy Site Map Contact us © 2020 Learn4Good Job Posting Web Site - listing US Job Opportunities, Staffing Agencies, International / Overseas Employment. Find &amp; apply for expat jobs/ English teaching jobs abroad for Americans, Canadians, EU/British citizens, recent college graduates...",
                    "city_name": "Boston, MA",
                    "company_name": "Related Management Corporation",
                    "expired": "2020-09-03",
                    "id": "cda7a43ccdee44ada42704bf3b07f154",
                    "posted": "2020-08-26",
                    "score": 0,
                    "title_raw": "General Manager",
                    "url": [],
                },
                {
                    "body": "<!--id: f0df162d10d64c1ab835e270fe28ad2b--> try the craigslist app » Android iOS CL <ul><li> boston </li><li> boston/camb/brook </li><li> skilled trades/artisan boston/camb/brook &gt; skilled trades/artisan favorite favorite hide unhide flag flagged Posted 2020-07-28 10:38 ELECTRICAL /APPRENTICES (BOSTON/FITCHBURG/NORTHSHORE) </li></ul><h5>WASHINGTON</h5> near LIBERTY compensation: <h5>PAY DETERMINED BY EXPERIENCE HOLIDAYS VACATIONS</h5> employment type: full-time <h5>SYLVIA ELECTRICAL CONTRACTING 3</h5> year minimum field electrical experience Own transportation basic hand tools Good work ethic Pay depends on experience. Payed vacation and holidays Friendly working atmosphere Please call 9784798723 <ul><li> Principals only. Recruiters, please don't contact this job poster. </li><li> do NOT contact us with unsolicited services or offers </li><li> OK to highlight this job opening for persons with disabilities post id: 7167361636 posted: 2020-07-28 10:38 updated: 2020-07-28 10:38</li></ul>",
                    "city_name": "Boston, MA",
                    "company_name": None,
                    "expired": "2020-09-14",
                    "id": "f0df162d10d64c1ab835e270fe28ad2b",
                    "posted": "2020-07-28",
                    "score": 0,
                    "title_raw": "ELECTRICAL /APPRENTICES",
                    "url": [],
                },
                {
                    "body": "<!--id: 2ac6df82e1634084907a7739baacb150--> Biology Lab Technician Co-op • <h5>Share This:</h5> Share on TwitterShare on LinkedinShare on Facebook • Copy Link Posted on: November 24, 2020 Apply Now Boston, MA Co-op Expires January 22, 2021 The Department of Sciences seeks a co-op employee to provide technical assistance to students and support to faculty and staff in the biology laboratories for the Spring 2021 semester. The co-op technician will be responsible for learning and understanding all instructional experiments for the Cell &amp; Molecular Biology and Anatomy &amp; Physiology courses. The co-op technician will also be responsible for supporting both the in-person and online labs for all biology courses. Primary responsibilities include setting up, organizing and testing instructional experiments as well as assisting with instruction. The co-op technician will be responsible for participating in all aspects of laboratory maintenance including safety inspections, organism care, equipment maintenance, dish washing, and the proper disposal of chemical and bio-hazardous waste. The co-op technician must follow all guidelines outlined in the biosafety manual, chemical hygiene plan, and laboratory safety plans. The co-op technician must attend all course meetings and training sessions. In addition to the daily lab responsibilities, the co-op technician will be expected to participate in an independent project that supports the work being done in the laboratory. This project can be but is not limited to a larger ongoing research project, redesign or innovation of labs being taught in any of the biology courses, an approved independent project of the co-op technician's choice. For training purposes, the start date may be earlier than the first day of the semester. This opportunity may also extend beyond the last day of the semester to ensure that all milestones and lab responsibilities are completed.",
                    "city_name": "Boston, MA",
                    "company_name": "Wentworth Institute of Technology, Inc.",
                    "expired": "2021-04-30",
                    "id": "2ac6df82e1634084907a7739baacb150",
                    "posted": "2020-12-02",
                    "score": 0,
                    "title_raw": "co-op technician",
                    "url": [],
                },
            ],
            "unique_postings": 322643,
            "viewable_postings": 322643,
        }
    }


@pytest.fixture
def postings_get_data():
    return {
        "data": {
            "body": "<!--id: 68078da7705941108426e4930941d323--> Keywords (e.g. nurse, sales) Category State City Radius Robotics Software Engineer Slide Brook Partners Email Job to a <h5>Friend Job Location:</h5> Boston, MA Robotics Software Engineer<ul><li>Boston Area (start-up) This Boston area start-up is seeking a lead software engineer with experience in robotics or computer vision-based software.</li></ul> ? The right candidate will be an adventurous and hard-working engineer who has worked in the fast paced world of robotics or vision based software. <h5>Qualifications:</h5><ul><li>Have at 2-4years of relevant job experience</li><li>Have been a part of a start-up or fast-paced environment</li><li>Have experience programming inC++ or Python, and ROS</li><li>Have a drive to solve complex robotics problems</li><li>Have experience working with a small team ?</li></ul> <h5>Responsibilities:</h5><ul><li>Generate software architecture</li><li>Design and build full-stack robot software</li><li>Oversee software engineers and contractors</li><li>Manage software builds and releases</li><li>Direct a QA and DVT program</li></ul>",
            "city_name": "Boston, MA",
            "company_name": "Brook Partners, Inc.",
            "employment_type_name": "Full-time (> 32 hours)",
            "expired": "2018-06-28",
            "id": "68078da7705941108426e4930941d323",
            "max_years_experience": None,
            "min_years_experience": None,
            "onet": "15-1132.00",
            "posted": "2018-03-31",
            "score": 12.145,
            "skills": [
                "KS440446CLVJYFGF0X6D",
                "KS440QS66YCBN23Y8K25",
                "KS125LS6N7WP4S6SFTCK",
                "KS1283R6BBX34S61XLQS",
                "KS7G4D96T7C2L619L5TH",
                "KS123X777H5WFNXQ6BPM",
                "KS120NP6J9YGDMN22JGF",
            ],
            "skills_name": [
                "Robot Operating Systems",
                "Software Engineering",
                "Python (Programming Language)",
                "Software Architecture",
                "Design Verification Test",
                "Sales",
                "Computer Vision",
            ],
            "title": "ET6850661D6AE5FA86",
            "title_name": "Software Engineers",
            "url": [],
            "active_urls": [],
        }
    }


@pytest.fixture
def distributions_data():
    return {
        "data": {
            "distribution": {
                "buckets": [
                    {
                        "duplicate_postings": 422706,
                        "key": 25,
                        "unique_postings": 126445,
                        "value": 38178,
                    },
                    {
                        "duplicate_postings": 868120,
                        "key": 50,
                        "unique_postings": 257335,
                        "value": 52000,
                    },
                    {
                        "duplicate_postings": 1231723,
                        "key": 75,
                        "unique_postings": 381181,
                        "value": 90000,
                    },
                ],
                "domain": {"max": 500000, "min": 24980},
                "facet": "salary",
                "interval": None,
                "type": "percentile",
            },
            "totals": {"duplicate_postings": 3874932, "unique_postings": 1445428},
        }
    }
