"""
Loops through the APIs and generates the raw documentation files for each API.
"""

from EmsiApiPy import (
    AutomationIndexConnection,
    AggregateProfilesConnection,
    CanadaPostingsConnection,
    UnitedStatesPostingsConnection,
    ACSIndicatorsConnection,
    SkillsClassificationConnection,
    EmsiTitlesConnection,
    # UsCompensationConnection,
    UsOccupationEarningsConnection,
    GeographyConnection,
    IpedsConnection,
    UKPostingsConnection,
    TalentBenchmarkConnection,
    GlobalPostingsConnection,
    GlobalProfilesConnection,
    CompaniesConnection
)

for connection in [
        AutomationIndexConnection,
        AggregateProfilesConnection,
        CanadaPostingsConnection,
        UnitedStatesPostingsConnection,
        ACSIndicatorsConnection,
        SkillsClassificationConnection,
        EmsiTitlesConnection,
        # UsCompensationConnection,
        UsOccupationEarningsConnection,
        GeographyConnection,
        IpedsConnection,
        UKPostingsConnection,
        TalentBenchmarkConnection,
        GlobalProfilesConnection,
        GlobalPostingsConnection,
        CompaniesConnection
]:
    conn = connection()
    print(conn.name)
    doc_string = conn.get_docs()

    with open(f"docs/raw_doc_pages/{conn.name}.md", "w+") as out_file:
        out_file.write(doc_string)
