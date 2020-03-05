# Check if users have all the dependencies required
# If they installed from the requirements.txt file correctly, this should not raise an error
hard_dependencies = ("requests", "pandas")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies

# import all of the apis that we have connections defined for up to this point
from .apis.automationIndex import AutomationIndexConnection
from .apis.aggregateProfiles import AggregateProfilesConnection
from .apis.canadaPostings import CanadaPostingsConnection
from .apis.coreLmi import CoreLMIConnection
from .apis.usPostings import UnitedStatesPostingsConnection
from .apis.acsIndicators import ACSIndicatorsConnection
from .apis.emsiTitles import EmsiTitlesConnection
from .apis.skillClusters import SkillClustersConnection
