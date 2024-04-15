"""
Loops through the APIs and generates the raw documentation files for each API.
"""
from __future__ import annotations

from EmsiApiPy import ACSIndicatorsConnection
from EmsiApiPy import AggregateProfilesConnection
from EmsiApiPy import AutomationIndexConnection
from EmsiApiPy import CanadaPostingsConnection
from EmsiApiPy import CompaniesConnection
from EmsiApiPy import GeographyConnection
from EmsiApiPy import GlobalPostingsConnection
from EmsiApiPy import GlobalProfilesConnection
from EmsiApiPy import IpedsConnection
from EmsiApiPy import SkillsClassificationConnection
from EmsiApiPy import TalentBenchmarkConnection
from EmsiApiPy import TitlesConnection
from EmsiApiPy import UKPostingsConnection
from EmsiApiPy import UnitedStatesPostingsConnection
from EmsiApiPy import UsOccupationEarningsConnection

for connection in [
    AutomationIndexConnection,
    AggregateProfilesConnection,
    CanadaPostingsConnection,
    UnitedStatesPostingsConnection,
    ACSIndicatorsConnection,
    SkillsClassificationConnection,
    TitlesConnection,
    UsOccupationEarningsConnection,
    GeographyConnection,
    IpedsConnection,
    UKPostingsConnection,
    TalentBenchmarkConnection,
    GlobalProfilesConnection,
    GlobalPostingsConnection,
    CompaniesConnection,
    # these apis don't have a "docs" endpoint
    # UsCompensationConnection,
    # USInputOutputConncetion,
    # CoreLMIConnection,
]:
    conn = connection()
    doc_string = conn.get_docs()

    with open(f"docs/raw_doc_pages/{conn.name}.md", "w+") as out_file:
        out_file.write(doc_string)
