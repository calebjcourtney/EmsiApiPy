# Check if users have all the dependencies required
# If they installed from the requirements.txt file correctly, this should not raise an error
from __future__ import annotations

from .apis.acsIndicators import ACSIndicatorsConnection
from .apis.aggregateProfiles import AggregateProfilesConnection
from .apis.automationIndex import AutomationIndexConnection
from .apis.base import EmsiBaseConnection
from .apis.canadaPostings import CanadaPostingsConnection
from .apis.companies import CompaniesConnection
from .apis.coreLmi import CoreLMIConnection
from .apis.emsiTitles import TitlesConnection
from .apis.geography import GeographyConnection
from .apis.globalPostings import GlobalPostingsConnection
from .apis.globalProfiles import GlobalProfilesConnection
from .apis.ipeds import IpedsConnection
from .apis.openSkills import SkillsClassificationConnection
from .apis.talentBenchmark import TalentBenchmarkConnection
from .apis.unitedKingdomPostings import UKPostingsConnection
from .apis.unitedKingdomProfiles import UKProfiles
from .apis.usCompensation import UsCompensationConnection
from .apis.usInputOutput import USInputOutputConncetion
from .apis.usOccEarnings import UsOccupationEarningsConnection
from .apis.usPostings import UnitedStatesPostingsConnection

hard_dependencies = ("requests", "pandas")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n"
        + "\n".join(missing_dependencies),
    )
del hard_dependencies, dependency, missing_dependencies

# import all of the apis that we have connections defined for up to this point

__all__ = [
    "ACSIndicatorsConnection",
    "AggregateProfilesConnection",
    "AutomationIndexConnection",
    "EmsiBaseConnection",
    "CanadaPostingsConnection",
    "CompaniesConnection",
    "CoreLMIConnection",
    "TitlesConnection",
    "GeographyConnection",
    "GlobalPostingsConnection",
    "GlobalProfilesConnection",
    "IpedsConnection",
    "SkillsClassificationConnection",
    "TalentBenchmarkConnection",
    "UKPostingsConnection",
    "UKProfiles",
    "UsCompensationConnection",
    "USInputOutputConncetion",
    "UsOccupationEarningsConnection",
    "UnitedStatesPostingsConnection",
]
