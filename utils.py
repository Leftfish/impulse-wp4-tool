from datetime import datetime
import json

# Import from modularized rights calculation modules
from utils_modules.additional_classification import (
    calculate_additional_object_classification_status,
)

from utils_modules.copyright import (
    calculate_intermediate_values_copyright,
    calculate_object_copyright_status,
    calculate_first_edition_protection_status,
)
from utils_modules.performance import (
    calculate_intermediate_values_performances,
    calculate_performance_rights_status,
)
from utils_modules.phonogram import (
    calculate_intermediate_values_phonograms,
    calculate_phonogram_rights_status,
)
from utils_modules.film_fixation import (
    calculate_intermediate_values_film_fixations,
    calculate_film_fixation_rights_status,
)
from utils_modules.broadcasting import (
    calculate_intermediate_values_broadcast,
    calculate_broadcast_rights_status,
)
from utils_modules.digital_representation import calculate_digital_representation_status

from utils_modules.other_legal_issues import (
    calculate_intermediate_values_other_legal_issues,
    calculate_other_legal_issues_status,
)

CURRENT_YEAR = datetime.now().year


def calculate_all_intermediate_values(data):
    """Calculate and return a unified dictionary of intermediate values
    for both copyright and performance calculations.
    """
    copyright_intermediate = calculate_intermediate_values_copyright(
        data["copyright_info"]
    )
    performance_intermediate = calculate_intermediate_values_performances(
        data["performance_info"]
    )
    phonogram_intermediate = calculate_intermediate_values_phonograms(
        data["phonogram_info"]
    )
    film_fixation_intermediate = calculate_intermediate_values_film_fixations(
        data["film_fixation_info"]
    )
    broadcasts_intermediate = calculate_intermediate_values_broadcast(
        data["broadcast_info"]
    )
    other_legal_issues_intermediate = calculate_intermediate_values_other_legal_issues(
        data["other_restrictions_info"]
    )

    # Merge with later functions taking precedence on overlapping keys (e.g., CURRENT_YEAR)
    merged = {}
    merged.update(copyright_intermediate)
    merged.update(performance_intermediate)
    merged.update(phonogram_intermediate)
    merged.update(film_fixation_intermediate)
    merged.update(broadcasts_intermediate)
    merged.update(other_legal_issues_intermediate)
    return merged


def calculate_results(data, intermediate):
    """Calculate final copyright status results based on intermediate values."""
    results = {
        "object_name": data.get("object_name"),
        "institution_name": data.get("institution_name"),
        "copyright_status": None,  # Will store object copyright status
        "performance_status": None,  # Will store performance rights status
        "phonogram_status": None,  # Will store phonogram rights status
        "film_fixation_status": None,  # Will store film fixation rights status
        "broadcast_status": None,  # Will store broadcasting organisation rights status
        "digital_repr_status": None,  # Will store digital representation status
        "debug_info": {},  # Add debug info tracking
    }

    # Track variable usage
    used_vars = set()

    # Expect callers to pass unified intermediate values
    merged_intermediate = intermediate or {}

    # Calculate object copyright status

    (
        object_copyright_results,
        object_copyright_used_vars,
    ) = calculate_object_copyright_status(data["copyright_info"], merged_intermediate)
    (
        object_first_edition_results,
        object_first_edition_used_vars,
    ) = calculate_first_edition_protection_status(
        data["copyright_info"],
        merged_intermediate,
    )
    used_vars.update(object_copyright_used_vars)
    used_vars.update(object_first_edition_used_vars)

    # Calculate performance rights status
    (
        object_performance_results,
        object_performance_used_vars,
    ) = calculate_performance_rights_status(
        data["performance_info"],
        merged_intermediate,
    )
    used_vars.update(object_performance_used_vars)

    # Calculate phonogram rights status
    (
        object_phonogram_results,
        object_phonogram_used_vars,
    ) = calculate_phonogram_rights_status(
        data["phonogram_info"],
        merged_intermediate,
    )
    used_vars.update(object_phonogram_used_vars)

    # Calculate film fixation rights status
    (
        object_film_fixation_results,
        object_film_fixation_used_vars,
    ) = calculate_film_fixation_rights_status(
        data["film_fixation_info"],
        merged_intermediate,
    )
    used_vars.update(object_film_fixation_used_vars)

    # Calculate broadcasting organisation rights status
    (
        object_broadcast_results,
        object_broadcast_used_vars,
    ) = calculate_broadcast_rights_status(
        data["broadcast_info"],
        merged_intermediate,
    )
    used_vars.update(object_broadcast_used_vars)

    # Calculate additional object classification status
    (
        object_additional_classification_results,
        object_additional_classification_used_vars,
    ) = calculate_additional_object_classification_status(
        data["other_intellectual_property_info"],
        merged_intermediate,
    )
    used_vars.update(object_additional_classification_used_vars)

    # Calculate other legal issues status (NEW)
    (
        other_legal_issues_results,
        other_legal_issues_used_vars,
    ) = calculate_other_legal_issues_status(
        data["other_restrictions_info"],
        merged_intermediate,
    )
    used_vars.update(other_legal_issues_used_vars)

    # Calculate digital representation status
    (
        digital_repr_results,
        digital_repr_used_vars,
    ) = calculate_digital_representation_status(
        data["digital_representation_info"],
        merged_intermediate,
    )
    used_vars.update(digital_repr_used_vars)

    # Store the results
    results["copyright_status"] = object_copyright_results
    results["first_edition_status"] = object_first_edition_results
    results["performance_status"] = object_performance_results
    results["phonogram_status"] = object_phonogram_results
    results["film_fixation_status"] = object_film_fixation_results
    results["broadcast_status"] = object_broadcast_results
    results["other_ip_rights_status"] = object_additional_classification_results
    results["other_legal_issues_status"] = other_legal_issues_results
    results["digital_repr_status"] = digital_repr_results

    # Prepare debug info
    basic_info_fields = [
        "object_name",
        "institution_name",
        "object_url",
        "object_collection_ownership",
        "digital_repr_nature",
        "general_notes",
    ]
    results["debug_info"] = {
        "basic_information": {k: data[k] for k in basic_info_fields if k in data},
        "input_data": {k: v for k, v in data.items() if k not in basic_info_fields},
        "intermediate_values": merged_intermediate,
        "used_variables": list(used_vars),
    }

    return results
