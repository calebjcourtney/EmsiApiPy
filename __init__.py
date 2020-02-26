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

from .apis.automationIndex import AutomationIndexConnection
from .apis.aggregateProfiles import AggregateProfilesConnection
from .apis.canadaPostings import CanadaPostingsConnection
from .apis.coreLmi import CoreLMIConnection
