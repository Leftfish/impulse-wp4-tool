# pylint: disable=unsubscriptable-object, missing-function-docstring, missing-module-docstring, missing-class-docstring, line-too-long

import unittest
from utils import calculate_all_intermediate_values, calculate_results


STATUS_CATEGORIES = [
    "green",
    "yellow",
    "red",
    "info",
    "rights_green",
    "rights_yellow",
]


def extract_input_data(json_data):
    """Extracts input data from JSON structure"""
    return json_data["debug_info"]["input_data"]


def extract_expected_statuses(json_data):
    """Extracts expected statuses from JSON structure, excluding debug_info"""
    expected = {}
    status_keys = [
        "broadcast_status",
        "copyright_status",
        "digital_repr_status",
        "film_fixation_status",
        "first_edition_status",
        "other_ip_rights_status",
        "other_legal_issues_status",
        "performance_status",
        "phonogram_status",
    ]
    for key in status_keys:
        if key in json_data:
            expected[key] = json_data[key]
    return expected


def run_comprehensive_test(data):
    """Runs the calculations and returns all results"""
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results


def _normalize_status_entries(entries):
    """Normalizes status entries for comparison regardless of order.
    Only compares condition names, not explanations."""
    return sorted([entry.get("condition") for entry in entries])


def _get_test_case_by_name(name):
    """Helper to get a test case JSON by name"""
    for test_case in TEST_CASE_JSONS:
        if test_case["name"] == name:
            return test_case
    raise ValueError(f"Test case '{name}' not found")


# Test case JSONs - add new test cases here
TEST_CASE_JSONS = [
    {
        "name": "diverse_object_scenario",
        "json": {
            "broadcast_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotABroadcast",
                        "explanation": "It is not protected as a broadcast.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "copyright_status": {
                "green": [],
                "info": [
                    {
                        "condition": "CopyrightDerivativeWork",
                        "explanation": "This is a derivative work. This means that you also need to verify the status of the original work.",
                    },
                    {
                        "condition": "CopyrightCompoundWork",
                        "explanation": "This is a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.",
                    },
                ],
                "red": [
                    {
                        "condition": "CopyrightPublicDomainRightsLapsedArticle1Sec3",
                        "explanation": "The object is still under copyright because fewer than 70 years passed since it was first made available.",
                    }
                ],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "debug_info": {
                "input_data": {
                    "broadcast_info": {
                        "broadcast_before_1970": "broadcast_not_made_before_1970",
                        "broadcast_cc_license": "not_applicable",
                        "broadcast_current_rightholder": "rightholder_unknown",
                        "broadcast_rights_acquired_to_make_available": "not_applicable",
                        "broadcast_year": None,
                        "broadcasters": [{"country_of_origin": "EU"}],
                        "is_broadcast": "not_broadcast",
                        "is_compound_broadcast": "not_compound",
                    },
                    "copyright_info": {
                        "architecture_country": "XX",
                        "author_alive": "author_alive",
                        "author_death_year": None,
                        "authors": [{"country_of_origin": "AT", "identity_known": False}],
                        "cinematographic_country": "XX",
                        "country_first_publication": "AT",
                        "created_before_1850": "not_made_before_1850",
                        "creation_year": 1930,
                        "current_rightholder": "rightholder_unknown",
                        "first_available_year": 1980,
                        "first_publication_year": 1960,
                        "internet_first_available": "not_made_available_internet",
                        "is_compound": "compound",
                        "is_copyright_work": "work",
                        "is_derivative": "derivative",
                        "is_photography": "not_photography",
                        "is_collective": "not_collective_work",
                        "object_cc_license": "not_applicable",
                        "object_copyright_rights_acquired_to_make_available": "not_applicable",
                        "original_rightholder": "human_author",
                        "otherwise_available": "made_available_no_medium",
                        "physically_published": "published_on_physical_medium",
                        "simultaneous_publication_countries": ["XX"],
                        "territory_status_changed": False,
                    },
                    "digital_representation_info": {
                        "digital_repr_copyright_cc_license": "not_applicable",
                        "digital_repr_copyright_current_rightholder": "rightholder_unknown",
                        "digital_repr_copyright_rights_acquired": "not_applicable",
                        "digital_repr_film_fixation_cc_license": "not_applicable",
                        "digital_repr_film_fixation_current_rightholder": "rightholder_unknown",
                        "digital_repr_film_fixation_rights_acquired": "not_applicable",
                        "digital_repr_ip_rights": {
                            "copyright": "no",
                            "film_fixation_rights": "no",
                            "other_ip_rights": "no",
                            "phonogram_rights": "no",
                        },
                        "digital_repr_nature": "obj_audio",
                        "digital_repr_other_cc_license": "not_applicable",
                        "digital_repr_other_current_rightholder": "rightholder_unknown",
                        "digital_repr_other_rights_acquired": "not_applicable",
                        "digital_repr_phonogram_cc_license": "not_applicable",
                        "digital_repr_phonogram_current_rightholder": "rightholder_unknown",
                        "digital_repr_phonogram_rights_acquired": "not_applicable",
                        "visual_art_work": "no",
                    },
                    "film_fixation_info": {
                        "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                        "film_fixation_available_no_medium_year": None,
                        "film_fixation_before_1920": "film_fixation_not_made_before_1920",
                        "film_fixation_cc_license": "not_applicable",
                        "film_fixation_current_rightholder": "rightholder_unknown",
                        "film_fixation_producers": [{"country_of_origin": "EU"}],
                        "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                        "film_fixation_published_fixed_medium_year": None,
                        "film_fixation_rights_acquired_to_make_available": "not_applicable",
                        "film_fixation_year": None,
                        "is_compound_film_fixation": "not_compound",
                        "is_film_fixation": "not_film_fixation",
                    },
                    "other_intellectual_property_info": {
                        "critical_edition": "not_critical_edition",
                        "design": "uncertain",
                        "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                        "press_publication": "not_press_publication",
                        "press_publication_year": None,
                        "trademark": "uncertain",
                    },
                    "other_restrictions_info": {
                        "object_administrative_restrictions": "no_administrative_restrictions",
                        "object_contractual_restrictions": "contractual_restrictions",
                        "object_discriminatory_content": "does_not_contain_discriminatory",
                        "object_legal_consultation": "no_self_answer",
                        "object_living_identifiable_info": "does_not_contain_identifiable_living",
                        "object_other_problems": "no_other_problems",
                        "object_other_sensitive_content": "does_not_contain_other_sensitive",
                        "object_ownership_status": "own_object",
                        "object_provenance_issues": "provenance_not_troublesome",
                        "object_provenance_traced": "provenance_traced",
                        "object_restrictions_notes": "",
                        "object_sensitive_historical_info": "does_not_contain_sensitive_historical",
                        "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
                    },
                    "performance_info": {
                        "is_compound_performance": "not_compound",
                        "is_performance": "performance",
                        "performance_before_1900": "performance_not_made_before_1900",
                        "performance_cc_license": "cc_by_sa",
                        "performance_current_rightholder": "rightholder_not_us",
                        "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_available",
                        "performance_fixed_not_phonogram_available_year": 1980,
                        "performance_phonogram_available": "performance_phonogram_available",
                        "performance_phonogram_available_year": 1950,
                        "performance_rights_acquired_to_make_available": "not_applicable",
                        "performance_year": 1960,
                        "performers": [{"country_of_origin": "AT", "identity_known": True}],
                    },
                    "phonogram_info": {
                        "is_compound_phonogram": "compound",
                        "is_phonogram": "phonogram",
                        "phonogram_available_no_medium": "uncertain",
                        "phonogram_available_no_medium_year": None,
                        "phonogram_before_1900": "phonogram_not_made_before_1900",
                        "phonogram_cc_license": "cc_by_nd",
                        "phonogram_current_rightholder": "rightholder_not_us",
                        "phonogram_producers": [{"country_of_origin": "AT"}],
                        "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                        "phonogram_published_fixed_medium_year": 1960,
                        "phonogram_rights_acquired_to_make_available": "not_applicable",
                        "phonogram_year": 1960,
                    },
                },
            },
            "digital_repr_status": {
                "green": [
                    {
                        "condition": "DigitalRepresentationCopyrightStatus",
                        "explanation": "The digital representation is not protected by copyright protection.",
                    },
                    {
                        "condition": "DigitalRepresentationPhonogramStatus",
                        "explanation": "The digital representation is not protected by phonogram rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationFilmFixationStatus",
                        "explanation": "The digital representation is not protected by film fixation rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationOtherIPStatus",
                        "explanation": "The digital representation is not protected by other IP rights protection.",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "film_fixation_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAFilmFixation",
                        "explanation": "It is not protected as a film fixation.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "first_edition_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_ip_rights_status": {
                "green": [
                    {
                        "condition": "NotPressPublication",
                        "explanation": "The object is not a press publication.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [
                    {
                        "condition": "Trademark",
                        "explanation": "There may be obstacles stemming from trademark law.",
                    },
                    {
                        "condition": "Design",
                        "explanation": "There may be obstacles stemming from design law. In some cases, an unauthorized depiction of a design in an online environment is an infringement.",
                    },
                ],
            },
            "other_legal_issues_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [
                    {
                        "condition": "HasContractualRestrictions",
                        "explanation": "It is necessary to review the agreements pertaining to the use of the work to determine the scope of possible obstacles.",
                    }
                ],
            },
            "performance_status": {
                "green": [
                    {
                        "condition": "PerformanceProtectionLapsedArticle3Publication",
                        "explanation": "The performance was protected but the protection has lapsed.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "phonogram_status": {
                "green": [],
                "info": [
                    {
                        "condition": "CompoundPhonogram",
                        "explanation": "This recording is, in fact, a collection of multiple recording or it is made from various recording. The analysis must be performed for each separately.",
                    }
                ],
                "red": [],
                "rights_green": [],
                "rights_yellow": [
                    {
                        "condition": "PhonogramAvailableCCLicense",
                        "explanation": "While the recording is protected, it is available under an open content license. Additional verification of the license terms may be needed.",
                    }
                ],
                "yellow": [
                    {
                        "condition": "PhonogramUnknownPublicationExceptions",
                        "explanation": "It is impossible to determine if the recording is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.",
                    }
                ],
            },
        },
    },
    {
        "name": "territory_status_changed_scenario",
        "json": {
            "broadcast_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotABroadcast",
                        "explanation": "It is not protected as a broadcast.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "copyright_status": {
                "green": [],
                "info": [
                    {
                        "condition": "CopyrightCompoundWork",
                        "explanation": "This is a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.",
                    },
                    {
                        "condition": "CopyrightTerritoryStatusChanged",
                        "explanation": "Problems with international succession were encountered.",
                    },
                ],
                "red": [
                    {
                        "condition": "CopyrightPublicDomainRightsLapsedArticle1Sec1-2",
                        "explanation": "The object is still under copyright because fewer than 70 years passed since the author's death.",
                    }
                ],
                "rights_green": [],
                "rights_yellow": [
                    {
                        "condition": "CopyrightObjectOnlineAvailable",
                        "explanation": "While the work is protected by copyright, you can make it available online based on the right to quote, but additional verification may be needed.",
                    }
                ],
                "yellow": [],
            },
            "debug_info": {
                "input_data": {
                    "broadcast_info": {
                        "broadcast_before_1970": "broadcast_not_made_before_1970",
                        "broadcast_cc_license": "not_applicable",
                        "broadcast_current_rightholder": "rightholder_unknown",
                        "broadcast_rights_acquired_to_make_available": "not_applicable",
                        "broadcast_year": None,
                        "broadcasters": [{"country_of_origin": "EU"}],
                        "is_broadcast": "not_broadcast",
                        "is_compound_broadcast": "not_compound",
                    },
                    "copyright_info": {
                        "architecture_country": "XX",
                        "author_alive": "author_dead",
                        "author_death_year": 1980,
                        "authors": [{"country_of_origin": "CZ", "identity_known": True}],
                        "cinematographic_country": "XX",
                        "country_first_publication": "CZ",
                        "created_before_1850": "not_made_before_1850",
                        "creation_year": 1945,
                        "current_rightholder": "rightholder_not_us",
                        "first_available_year": None,
                        "first_publication_year": 1990,
                        "internet_first_available": "not_made_available_internet",
                        "is_compound": "compound",
                        "is_copyright_work": "work",
                        "is_derivative": "not_derivative",
                        "is_photography": "not_photography",
                        "is_collective": "not_collective_work",
                        "object_cc_license": "not_applicable",
                        "object_copyright_rights_acquired_to_make_available": "quote_right",
                        "original_rightholder": "human_author",
                        "otherwise_available": "uncertain",
                        "physically_published": "published_on_physical_medium",
                        "simultaneous_publication_countries": ["XX"],
                        "territory_status_changed": True,
                    },
                    "digital_representation_info": {
                        "digital_repr_copyright_cc_license": "not_applicable",
                        "digital_repr_copyright_current_rightholder": "rightholder_unknown",
                        "digital_repr_copyright_rights_acquired": "not_applicable",
                        "digital_repr_film_fixation_cc_license": "not_applicable",
                        "digital_repr_film_fixation_current_rightholder": "rightholder_unknown",
                        "digital_repr_film_fixation_rights_acquired": "not_applicable",
                        "digital_repr_ip_rights": {
                            "copyright": "no",
                            "film_fixation_rights": "no",
                            "other_ip_rights": "yes",
                            "phonogram_rights": "no",
                        },
                        "digital_repr_nature": "obj_2d_to_2d",
                        "digital_repr_other_cc_license": "not_applicable",
                        "digital_repr_other_current_rightholder": "rightholder_us",
                        "digital_repr_other_rights_acquired": "not_applicable",
                        "digital_repr_phonogram_cc_license": "not_applicable",
                        "digital_repr_phonogram_current_rightholder": "rightholder_unknown",
                        "digital_repr_phonogram_rights_acquired": "not_applicable",
                        "visual_art_work": "no",
                    },
                    "film_fixation_info": {
                        "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                        "film_fixation_available_no_medium_year": None,
                        "film_fixation_before_1920": "film_fixation_not_made_before_1920",
                        "film_fixation_cc_license": "not_applicable",
                        "film_fixation_current_rightholder": "rightholder_unknown",
                        "film_fixation_producers": [{"country_of_origin": "EU"}],
                        "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                        "film_fixation_published_fixed_medium_year": None,
                        "film_fixation_rights_acquired_to_make_available": "not_applicable",
                        "film_fixation_year": None,
                        "is_compound_film_fixation": "not_compound",
                        "is_film_fixation": "not_film_fixation",
                    },
                    "other_intellectual_property_info": {
                        "critical_edition": "not_critical_edition",
                        "design": "not_design",
                        "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                        "press_publication": "not_press_publication",
                        "press_publication_year": None,
                        "trademark": "not_trademark",
                    },
                    "other_restrictions_info": {
                        "object_administrative_restrictions": "administrative_restrictions",
                        "object_contractual_restrictions": "no_contractual_restrictions",
                        "object_discriminatory_content": "does_not_contain_discriminatory",
                        "object_legal_consultation": "no_self_answer",
                        "object_living_identifiable_info": "does_not_contain_identifiable_living",
                        "object_other_problems": "no_other_problems",
                        "object_other_sensitive_content": "does_not_contain_other_sensitive",
                        "object_ownership_status": "own_object",
                        "object_provenance_issues": "provenance_troublesome",
                        "object_provenance_traced": "provenance_traced",
                        "object_restrictions_notes": "",
                        "object_sensitive_historical_info": "does_not_contain_sensitive_historical",
                        "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
                    },
                    "performance_info": {
                        "is_compound_performance": "not_compound",
                        "is_performance": "performance",
                        "performance_before_1900": "performance_not_made_before_1900",
                        "performance_cc_license": "not_applicable",
                        "performance_current_rightholder": "rightholder_unknown",
                        "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_available",
                        "performance_fixed_not_phonogram_available_year": 1998,
                        "performance_phonogram_available": "performance_phonogram_available",
                        "performance_phonogram_available_year": 1998,
                        "performance_rights_acquired_to_make_available": "not_applicable",
                        "performance_year": 1946,
                        "performers": [{"country_of_origin": "EU", "identity_known": True}],
                    },
                    "phonogram_info": {
                        "is_compound_phonogram": "not_compound",
                        "is_phonogram": "phonogram",
                        "phonogram_available_no_medium": "uncertain",
                        "phonogram_available_no_medium_year": None,
                        "phonogram_before_1900": "phonogram_not_made_before_1900",
                        "phonogram_cc_license": "no",
                        "phonogram_current_rightholder": "rightholder_not_us",
                        "phonogram_producers": [{"country_of_origin": "CZ"}],
                        "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                        "phonogram_published_fixed_medium_year": 1998,
                        "phonogram_rights_acquired_to_make_available": "quote_right",
                        "phonogram_year": 1998,
                    },
                },
            },
            "digital_repr_status": {
                "green": [
                    {
                        "condition": "DigitalRepresentationCopyrightStatus",
                        "explanation": "The digital representation is not protected by copyright protection.",
                    },
                    {
                        "condition": "DigitalRepresentationPhonogramStatus",
                        "explanation": "The digital representation is not protected by phonogram rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationFilmFixationStatus",
                        "explanation": "The digital representation is not protected by film fixation rights protection.",
                    },
                ],
                "info": [],
                "red": [
                    {
                        "condition": "DigitalRepresentationOtherIPStatus",
                        "explanation": "The digital representation is protected by other IP rights protection.",
                    }
                ],
                "rights_green": [
                    {
                        "condition": "DigitalRepresentationOtherIPCurrentRightHolderKnown",
                        "explanation": "Even if the digital representation is protected by other IP rights, you are the rightholder.",
                    }
                ],
                "rights_yellow": [],
                "yellow": [],
            },
            "film_fixation_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAFilmFixation",
                        "explanation": "It is not protected as a film fixation.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "first_edition_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_ip_rights_status": {
                "green": [
                    {
                        "condition": "NotPressPublication",
                        "explanation": "The object is not a press publication.",
                    },
                    {
                        "condition": "NoOtherIPRights",
                        "explanation": "No other IP rights to consider",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_legal_issues_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [
                    {
                        "condition": "HasAdministrativeRestrictions",
                        "explanation": "There may be restrictions stemming from administrative legal regulations.",
                    },
                    {
                        "condition": "HasProvenanceIssues",
                        "explanation": "Although troublesome provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution",
                    },
                ],
            },
            "performance_status": {
                "green": [
                    {
                        "condition": "PerformanceProtectionLapsedArticle3Publication",
                        "explanation": "The performance was protected but the protection has lapsed.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "phonogram_status": {
                "green": [],
                "info": [],
                "red": [
                    {
                        "condition": "PhonogramStillProtectedArticle3S1",
                        "explanation": "The recording is still under protection.",
                    }
                ],
                "rights_green": [],
                "rights_yellow": [
                    {
                        "condition": "PhonogramOnlineAvailable",
                        "explanation": "While the recording is protected, you may make it available online under a limited license or specific legal provisions. Additional verification may be needed.",
                    }
                ],
                "yellow": [],
            },
        },
    },
    {
        "name": "broadcast_pre_1970_territory_changed_scenario",
        "json": {
            "broadcast_status": {
                "green": [
                    {
                        "condition": "PublicDomainRuleOfThumbBroadcasts",
                        "explanation": "Given the time the broadcast was made, it has passed to the public domain.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "copyright_status": {
                "green": [],
                "info": [
                    {
                        "condition": "CopyrightTerritoryStatusChanged",
                        "explanation": "Problems with international succession were encountered.",
                    }
                ],
                "red": [
                    {
                        "condition": "CopyrightPublicDomainRightsLapsedArticle1Sec1-2",
                        "explanation": "The object is still under copyright because fewer than 70 years passed since the author's death.",
                    }
                ],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "debug_info": {
                "input_data": {
                    "broadcast_info": {
                        "broadcast_before_1970": "broadcast_made_before_1970",
                        "broadcast_cc_license": "not_applicable",
                        "broadcast_current_rightholder": "rightholder_unknown",
                        "broadcast_rights_acquired_to_make_available": "not_applicable",
                        "broadcast_year": None,
                        "broadcasters": [{"country_of_origin": "EU"}],
                        "is_broadcast": "broadcast",
                        "is_compound_broadcast": "not_compound",
                    },
                    "copyright_info": {
                        "architecture_country": "XX",
                        "author_alive": "author_dead",
                        "author_death_year": 1962,
                        "authors": [{"country_of_origin": "CA", "identity_known": True}],
                        "cinematographic_country": "XX",
                        "country_first_publication": "CA",
                        "created_before_1850": "not_made_before_1850",
                        "creation_year": 1950,
                        "current_rightholder": "rightholder_unknown",
                        "first_available_year": 1960,
                        "first_publication_year": 1960,
                        "internet_first_available": "not_made_available_internet",
                        "is_compound": "not_compound",
                        "is_copyright_work": "work",
                        "is_derivative": "not_derivative",
                        "is_photography": "not_photography",
                        "is_collective": "not_collective_work",
                        "object_cc_license": "not_applicable",
                        "object_copyright_rights_acquired_to_make_available": "not_applicable",
                        "original_rightholder": "human_author",
                        "otherwise_available": "made_available_no_medium",
                        "physically_published": "published_on_physical_medium",
                        "simultaneous_publication_countries": ["FR"],
                        "territory_status_changed": True,
                    },
                    "digital_representation_info": {
                        "digital_repr_copyright_cc_license": "not_applicable",
                        "digital_repr_copyright_current_rightholder": "rightholder_unknown",
                        "digital_repr_copyright_rights_acquired": "not_applicable",
                        "digital_repr_film_fixation_cc_license": "not_applicable",
                        "digital_repr_film_fixation_current_rightholder": "rightholder_unknown",
                        "digital_repr_film_fixation_rights_acquired": "not_applicable",
                        "digital_repr_ip_rights": {
                            "copyright": "no",
                            "film_fixation_rights": "no",
                            "other_ip_rights": "no",
                            "phonogram_rights": "no",
                        },
                        "digital_repr_nature": "obj_2d_to_2d",
                        "digital_repr_other_cc_license": "not_applicable",
                        "digital_repr_other_current_rightholder": "rightholder_unknown",
                        "digital_repr_other_rights_acquired": "not_applicable",
                        "digital_repr_phonogram_cc_license": "not_applicable",
                        "digital_repr_phonogram_current_rightholder": "rightholder_unknown",
                        "digital_repr_phonogram_rights_acquired": "not_applicable",
                        "visual_art_work": "no",
                    },
                    "film_fixation_info": {
                        "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                        "film_fixation_available_no_medium_year": None,
                        "film_fixation_before_1920": "film_fixation_not_made_before_1920",
                        "film_fixation_cc_license": "not_applicable",
                        "film_fixation_current_rightholder": "rightholder_unknown",
                        "film_fixation_producers": [{"country_of_origin": "EU"}],
                        "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                        "film_fixation_published_fixed_medium_year": None,
                        "film_fixation_rights_acquired_to_make_available": "not_applicable",
                        "film_fixation_year": None,
                        "is_compound_film_fixation": "not_compound",
                        "is_film_fixation": "not_film_fixation",
                    },
                    "other_intellectual_property_info": {
                        "critical_edition": "not_critical_edition",
                        "design": "not_design",
                        "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                        "press_publication": "not_press_publication",
                        "press_publication_year": None,
                        "trademark": "not_trademark",
                    },
                    "other_restrictions_info": {
                        "object_administrative_restrictions": "no_administrative_restrictions",
                        "object_contractual_restrictions": "no_contractual_restrictions",
                        "object_discriminatory_content": "does_not_contain_discriminatory",
                        "object_legal_consultation": "no_self_answer",
                        "object_living_identifiable_info": "does_not_contain_identifiable_living",
                        "object_other_problems": "no_other_problems",
                        "object_other_sensitive_content": "does_not_contain_other_sensitive",
                        "object_ownership_status": "own_object",
                        "object_provenance_issues": "provenance_not_troublesome",
                        "object_provenance_traced": "provenance_traced",
                        "object_restrictions_notes": "",
                        "object_sensitive_historical_info": "does_not_contain_sensitive_historical",
                        "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
                    },
                    "performance_info": {
                        "is_compound_performance": "not_compound",
                        "is_performance": "performance",
                        "performance_before_1900": "performance_not_made_before_1900",
                        "performance_cc_license": "not_applicable",
                        "performance_current_rightholder": "uncertain",
                        "performance_fixed_not_phonogram_available": "uncertain",
                        "performance_fixed_not_phonogram_available_year": None,
                        "performance_phonogram_available": "uncertain",
                        "performance_phonogram_available_year": None,
                        "performance_rights_acquired_to_make_available": "quote_right",
                        "performance_year": 1950,
                        "performers": [{"country_of_origin": "CA", "identity_known": True}],
                    },
                    "phonogram_info": {
                        "is_compound_phonogram": "not_compound",
                        "is_phonogram": "not_phonogram",
                        "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                        "phonogram_available_no_medium_year": None,
                        "phonogram_before_1900": "phonogram_not_made_before_1900",
                        "phonogram_cc_license": "not_applicable",
                        "phonogram_current_rightholder": "rightholder_unknown",
                        "phonogram_producers": [{"country_of_origin": "EU"}],
                        "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                        "phonogram_published_fixed_medium_year": None,
                        "phonogram_rights_acquired_to_make_available": "not_applicable",
                        "phonogram_year": None,
                    },
                },
            },
            "digital_repr_status": {
                "green": [
                    {
                        "condition": "DigitalRepresentationCopyrightStatus",
                        "explanation": "The digital representation is not protected by copyright protection.",
                    },
                    {
                        "condition": "DigitalRepresentationPhonogramStatus",
                        "explanation": "The digital representation is not protected by phonogram rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationFilmFixationStatus",
                        "explanation": "The digital representation is not protected by film fixation rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationOtherIPStatus",
                        "explanation": "The digital representation is not protected by other IP rights protection.",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "film_fixation_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAFilmFixation",
                        "explanation": "It is not protected as a film fixation.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "first_edition_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_ip_rights_status": {
                "green": [
                    {
                        "condition": "NotPressPublication",
                        "explanation": "The object is not a press publication.",
                    },
                    {
                        "condition": "NoOtherIPRights",
                        "explanation": "No other IP rights to consider",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_legal_issues_status": {
                "green": [
                    {
                        "condition": "NoLegalIssues",
                        "explanation": "No legal issues unrelated to intellectual property found.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "performance_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [
                    {
                        "condition": "PerformanceOnlineAvailable",
                        "explanation": "While the performance is protected, you may make it available online under a limited license orspecific legal provisions. Additional verification may be needed.",
                    }
                ],
                "yellow": [
                    {
                        "condition": "PerformanceNonEEAUncertain",
                        "explanation": "Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.",
                    }
                ],
            },
            "phonogram_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAPhonogram",
                        "explanation": "It is not protected as a phonogram.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
        },
    },
    {
        "name": "non_eea_rule_of_shorter_term_scenario",
        "json": {
            "broadcast_status": {
                "green": [
                    {
                        "condition": "BroadcastLapsedEvenIfEEA",
                        "explanation": "Country of origin appears to be outside the EEA, but the broadcast would have lost protection even if the country of origin were in the EEA.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "copyright_status": {
                "green": [],
                "info": [
                    {
                        "condition": "CopyrightTerritoryStatusChanged",
                        "explanation": "Problems with international succession were encountered.",
                    }
                ],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [
                    {
                        "condition": "CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm",
                        "explanation": "According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world's copyright systems.",
                    }
                ],
            },
            "debug_info": {
                "input_data": {
                    "broadcast_info": {
                        "broadcast_before_1970": "broadcast_not_made_before_1970",
                        "broadcast_cc_license": "not_applicable",
                        "broadcast_current_rightholder": "rightholder_unknown",
                        "broadcast_rights_acquired_to_make_available": "not_applicable",
                        "broadcast_year": 1972,
                        "broadcasters": [{"country_of_origin": "UA"}],
                        "is_broadcast": "broadcast",
                        "is_compound_broadcast": "not_compound",
                    },
                    "copyright_info": {
                        "architecture_country": "XX",
                        "author_alive": "author_dead",
                        "author_death_year": 1962,
                        "authors": [{"country_of_origin": "CA", "identity_known": True}],
                        "cinematographic_country": "XX",
                        "country_first_publication": "CA",
                        "created_before_1850": "not_made_before_1850",
                        "creation_year": 1950,
                        "current_rightholder": "rightholder_unknown",
                        "first_available_year": 1960,
                        "first_publication_year": 1960,
                        "internet_first_available": "not_made_available_internet",
                        "is_compound": "not_compound",
                        "is_copyright_work": "work",
                        "is_derivative": "not_derivative",
                        "is_photography": "not_photography",
                        "is_collective": "not_collective_work",
                        "object_cc_license": "not_applicable",
                        "object_copyright_rights_acquired_to_make_available": "not_applicable",
                        "original_rightholder": "human_author",
                        "otherwise_available": "made_available_no_medium",
                        "physically_published": "published_on_physical_medium",
                        "simultaneous_publication_countries": ["XX"],
                        "territory_status_changed": True,
                    },
                    "digital_representation_info": {
                        "digital_repr_copyright_cc_license": "not_applicable",
                        "digital_repr_copyright_current_rightholder": "rightholder_unknown",
                        "digital_repr_copyright_rights_acquired": "not_applicable",
                        "digital_repr_film_fixation_cc_license": "not_applicable",
                        "digital_repr_film_fixation_current_rightholder": "rightholder_unknown",
                        "digital_repr_film_fixation_rights_acquired": "not_applicable",
                        "digital_repr_ip_rights": {
                            "copyright": "no",
                            "film_fixation_rights": "no",
                            "other_ip_rights": "no",
                            "phonogram_rights": "no",
                        },
                        "digital_repr_nature": "obj_2d_to_2d",
                        "digital_repr_other_cc_license": "not_applicable",
                        "digital_repr_other_current_rightholder": "rightholder_unknown",
                        "digital_repr_other_rights_acquired": "not_applicable",
                        "digital_repr_phonogram_cc_license": "not_applicable",
                        "digital_repr_phonogram_current_rightholder": "rightholder_unknown",
                        "digital_repr_phonogram_rights_acquired": "not_applicable",
                        "visual_art_work": "no",
                    },
                    "film_fixation_info": {
                        "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                        "film_fixation_available_no_medium_year": None,
                        "film_fixation_before_1920": "film_fixation_not_made_before_1920",
                        "film_fixation_cc_license": "not_applicable",
                        "film_fixation_current_rightholder": "rightholder_unknown",
                        "film_fixation_producers": [{"country_of_origin": "EU"}],
                        "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                        "film_fixation_published_fixed_medium_year": None,
                        "film_fixation_rights_acquired_to_make_available": "not_applicable",
                        "film_fixation_year": None,
                        "is_compound_film_fixation": "not_compound",
                        "is_film_fixation": "not_film_fixation",
                    },
                    "other_intellectual_property_info": {
                        "critical_edition": "not_critical_edition",
                        "design": "not_design",
                        "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                        "press_publication": "not_press_publication",
                        "press_publication_year": None,
                        "trademark": "not_trademark",
                    },
                    "other_restrictions_info": {
                        "object_administrative_restrictions": "no_administrative_restrictions",
                        "object_contractual_restrictions": "no_contractual_restrictions",
                        "object_discriminatory_content": "does_not_contain_discriminatory",
                        "object_legal_consultation": "no_self_answer",
                        "object_living_identifiable_info": "contains_identifiable_living",
                        "object_other_problems": "no_other_problems",
                        "object_other_sensitive_content": "does_not_contain_other_sensitive",
                        "object_ownership_status": "own_object",
                        "object_provenance_issues": "provenance_not_troublesome",
                        "object_provenance_traced": "provenance_traced",
                        "object_restrictions_notes": "",
                        "object_sensitive_historical_info": "contains_sensitive_historical",
                        "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
                    },
                    "performance_info": {
                        "is_compound_performance": "not_compound",
                        "is_performance": "performance",
                        "performance_before_1900": "performance_not_made_before_1900",
                        "performance_cc_license": "cc_by",
                        "performance_current_rightholder": "uncertain",
                        "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_available",
                        "performance_fixed_not_phonogram_available_year": 1960,
                        "performance_phonogram_available": "performance_phonogram_available",
                        "performance_phonogram_available_year": 1960,
                        "performance_rights_acquired_to_make_available": "quote_right",
                        "performance_year": 1950,
                        "performers": [{"country_of_origin": "CA", "identity_known": True}],
                    },
                    "phonogram_info": {
                        "is_compound_phonogram": "not_compound",
                        "is_phonogram": "phonogram",
                        "phonogram_available_no_medium": "uncertain",
                        "phonogram_available_no_medium_year": None,
                        "phonogram_before_1900": "phonogram_not_made_before_1900",
                        "phonogram_cc_license": "not_applicable",
                        "phonogram_current_rightholder": "rightholder_not_us",
                        "phonogram_producers": [{"country_of_origin": "CA"}],
                        "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                        "phonogram_published_fixed_medium_year": 1962,
                        "phonogram_rights_acquired_to_make_available": "limited_license_agreement",
                        "phonogram_year": 1960,
                    },
                },
            },
            "digital_repr_status": {
                "green": [
                    {
                        "condition": "DigitalRepresentationCopyrightStatus",
                        "explanation": "The digital representation is not protected by copyright protection.",
                    },
                    {
                        "condition": "DigitalRepresentationPhonogramStatus",
                        "explanation": "The digital representation is not protected by phonogram rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationFilmFixationStatus",
                        "explanation": "The digital representation is not protected by film fixation rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationOtherIPStatus",
                        "explanation": "The digital representation is not protected by other IP rights protection.",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "film_fixation_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAFilmFixation",
                        "explanation": "It is not protected as a film fixation.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "first_edition_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_ip_rights_status": {
                "green": [
                    {
                        "condition": "NotPressPublication",
                        "explanation": "The object is not a press publication.",
                    },
                    {
                        "condition": "NoOtherIPRights",
                        "explanation": "No other IP rights to consider",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_legal_issues_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [
                    {
                        "condition": "ContainsLivingIdentifiableInfo",
                        "explanation": "The use of the object may lead to personal data processing, and depending on the exact context, require a legal basis under the General Data Protection Regulation",
                    },
                    {
                        "condition": "ContainsSensitiveHistoricalInfo",
                        "explanation": "The use of the object may expose the institution to defamation claims or similar liability",
                    },
                ],
            },
            "performance_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [
                    {
                        "condition": "PerformanceAvailableCCLicense",
                        "explanation": "While the performance is protected, it is available under an open content license (e.g., CC0 or CC-BY).",
                    }
                ],
                "rights_yellow": [
                    {
                        "condition": "PerformanceOnlineAvailable",
                        "explanation": "While the performance is protected, you may make it available online under a limited license orspecific legal provisions. Additional verification may be needed.",
                    }
                ],
                "yellow": [
                    {
                        "condition": "PerformanceNonEEAUncertain",
                        "explanation": "Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the performance would not have lapsed even under EEA rules, the status is uncertain.",
                    }
                ],
            },
            "phonogram_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [
                    {
                        "condition": "PhonogramOnlineAvailable",
                        "explanation": "While the recording is protected, you may make it available online under a limited license or specific legal provisions. Additional verification may be needed.",
                    }
                ],
                "yellow": [
                    {
                        "condition": "PhonogramNonEEAUncertain",
                        "explanation": "Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.",
                    }
                ],
            },
        },
    },
    {
        "name": "anonymous_anthology_scenario",
        "json": {
            "broadcast_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotABroadcast",
                        "explanation": "It is not protected as a broadcast.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "copyright_status": {
                "green": [],
                "info": [
                    {
                        "condition": "CopyrightDerivativeWork",
                        "explanation": "This is a derivative work. This means that you also need to verify the status of the original work.",
                    },
                    {
                        "condition": "CopyrightCompoundWork",
                        "explanation": "This is a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.",
                    },
                    {
                        "condition": "CopyrightCollectiveWork", 
                        "explanation": "This is a collective work. It means that even if copyright protection of the collective work (e.g. a given magazine issue) has lapsed, it may still apply with regard to the individual works that are elements of the collective work."
                    }
                ],
                "red": [
                    {
                        "condition": "CopyrightPublicDomainRightsLapsedArticle1Sec3",
                        "explanation": "The object is still under copyright because fewer than 70 years passed since it was first made available.",
                    }
                ],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "debug_info": {
                "input_data": {
                    "broadcast_info": {
                        "broadcast_before_1970": "broadcast_not_made_before_1970",
                        "broadcast_cc_license": "not_applicable",
                        "broadcast_current_rightholder": "rightholder_unknown",
                        "broadcast_rights_acquired_to_make_available": "not_applicable",
                        "broadcast_year": None,
                        "broadcasters": [{"country_of_origin": "EU"}],
                        "is_broadcast": "not_broadcast",
                        "is_compound_broadcast": "not_compound",
                    },
                    "copyright_info": {
                        "architecture_country": "XX",
                        "author_alive": "uncertain",
                        "author_death_year": None,
                        "authors": [
                            {"country_of_origin": "EU", "identity_known": False},
                            {"country_of_origin": "EU", "identity_known": False},
                            {"country_of_origin": "EU", "identity_known": False},
                        ],
                        "cinematographic_country": "XX",
                        "country_first_publication": "EU",
                        "created_before_1850": "not_made_before_1850",
                        "creation_year": 1930,
                        "current_rightholder": "rightholder_unknown",
                        "first_available_year": None,
                        "first_publication_year": 1960,
                        "internet_first_available": "not_made_available_internet",
                        "is_compound": "compound",
                        "is_copyright_work": "work",
                        "is_derivative": "derivative",
                        "is_photography": "not_photography",
                        "is_collective": "collective_work_authors_not_identified_on_copies",
                        "object_cc_license": "not_applicable",
                        "object_copyright_rights_acquired_to_make_available": "not_applicable",
                        "original_rightholder": "human_author",
                        "otherwise_available": "not_made_available_no_medium",
                        "physically_published": "published_on_physical_medium",
                        "simultaneous_publication_countries": ["XX"],
                        "territory_status_changed": False,
                    },
                    "digital_representation_info": {
                        "digital_repr_copyright_cc_license": "cc_by",
                        "digital_repr_copyright_current_rightholder": "rightholder_not_us",
                        "digital_repr_copyright_rights_acquired": "not_applicable",
                        "digital_repr_film_fixation_cc_license": "not_applicable",
                        "digital_repr_film_fixation_current_rightholder": "rightholder_unknown",
                        "digital_repr_film_fixation_rights_acquired": "not_applicable",
                        "digital_repr_ip_rights": {
                            "copyright": "yes",
                            "film_fixation_rights": "no",
                            "other_ip_rights": "no",
                            "phonogram_rights": "no",
                        },
                        "digital_repr_nature": "obj_3d_to_2d",
                        "digital_repr_other_cc_license": "not_applicable",
                        "digital_repr_other_current_rightholder": "rightholder_unknown",
                        "digital_repr_other_rights_acquired": "not_applicable",
                        "digital_repr_phonogram_cc_license": "not_applicable",
                        "digital_repr_phonogram_current_rightholder": "rightholder_unknown",
                        "digital_repr_phonogram_rights_acquired": "not_applicable",
                        "visual_art_work": "yes",
                    },
                    "film_fixation_info": {
                        "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                        "film_fixation_available_no_medium_year": None,
                        "film_fixation_before_1920": "film_fixation_not_made_before_1920",
                        "film_fixation_cc_license": "not_applicable",
                        "film_fixation_current_rightholder": "rightholder_unknown",
                        "film_fixation_producers": [{"country_of_origin": "EU"}],
                        "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                        "film_fixation_published_fixed_medium_year": None,
                        "film_fixation_rights_acquired_to_make_available": "not_applicable",
                        "film_fixation_year": None,
                        "is_compound_film_fixation": "not_compound",
                        "is_film_fixation": "not_film_fixation",
                    },
                    "other_intellectual_property_info": {
                        "critical_edition": "not_critical_edition",
                        "design": "not_design",
                        "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                        "press_publication": "not_press_publication",
                        "press_publication_year": None,
                        "trademark": "not_trademark",
                    },
                    "other_restrictions_info": {
                        "object_administrative_restrictions": "no_administrative_restrictions",
                        "object_contractual_restrictions": "no_contractual_restrictions",
                        "object_discriminatory_content": "does_not_contain_discriminatory",
                        "object_legal_consultation": "no_self_answer",
                        "object_living_identifiable_info": "does_not_contain_identifiable_living",
                        "object_other_problems": "no_other_problems",
                        "object_other_sensitive_content": "does_not_contain_other_sensitive",
                        "object_ownership_status": "own_object",
                        "object_provenance_issues": "provenance_not_troublesome",
                        "object_provenance_traced": "provenance_traced",
                        "object_restrictions_notes": "",
                        "object_sensitive_historical_info": "does_not_contain_sensitive_historical",
                        "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
                    },
                    "performance_info": {
                        "is_compound_performance": "not_compound",
                        "is_performance": "not_performance",
                        "performance_before_1900": "performance_not_made_before_1900",
                        "performance_cc_license": "not_applicable",
                        "performance_current_rightholder": "rightholder_unknown",
                        "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_not_available",
                        "performance_fixed_not_phonogram_available_year": None,
                        "performance_phonogram_available": "performance_phonogram_not_available",
                        "performance_phonogram_available_year": None,
                        "performance_rights_acquired_to_make_available": "not_applicable",
                        "performance_year": None,
                        "performers": [{"country_of_origin": "EU", "identity_known": True}],
                    },
                    "phonogram_info": {
                        "is_compound_phonogram": "not_compound",
                        "is_phonogram": "not_phonogram",
                        "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                        "phonogram_available_no_medium_year": None,
                        "phonogram_before_1900": "phonogram_not_made_before_1900",
                        "phonogram_cc_license": "not_applicable",
                        "phonogram_current_rightholder": "rightholder_unknown",
                        "phonogram_producers": [{"country_of_origin": "EU"}],
                        "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                        "phonogram_published_fixed_medium_year": None,
                        "phonogram_rights_acquired_to_make_available": "not_applicable",
                        "phonogram_year": None,
                    },
                },
            },
            "digital_repr_status": {
                "green": [
                    {
                        "condition": "DigitalRepresentationPhonogramStatus",
                        "explanation": "The digital representation is not protected by phonogram rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationFilmFixationStatus",
                        "explanation": "The digital representation is not protected by film fixation rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationOtherIPStatus",
                        "explanation": "The digital representation is not protected by other IP rights protection.",
                    },
                ],
                "info": [],
                "red": [
                    {
                        "condition": "DigitalRepresentationCopyrightStatus",
                        "explanation": "The digital representation is protected by copyright protection.",
                    }
                ],
                "rights_green": [
                    {
                        "condition": "DigitalRepresentationCopyrightAvailableCCLicense",
                        "explanation": "Even if the digital representation is protected by copyright, it is available under an open content license (e.g., CC0 or CC-BY).",
                    }
                ],
                "rights_yellow": [],
                "yellow": [],
            },
            "film_fixation_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAFilmFixation",
                        "explanation": "It is not protected as a film fixation.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "first_edition_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_ip_rights_status": {
                "green": [
                    {
                        "condition": "NotPressPublication",
                        "explanation": "The object is not a press publication.",
                    },
                    {
                        "condition": "NoOtherIPRights",
                        "explanation": "No other IP rights to consider",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_legal_issues_status": {
                "green": [
                    {
                        "condition": "NoLegalIssues",
                        "explanation": "No legal issues unrelated to intellectual property found.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "performance_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAPerformance",
                        "explanation": "The object does not include a performance.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "phonogram_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAPhonogram",
                        "explanation": "It is not protected as a phonogram.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
        },
    },
    {
        "name": "modern_multimedia_performance_scenario",
        "json": {
            "broadcast_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotABroadcast",
                        "explanation": "It is not protected as a broadcast.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "copyright_status": {
                "green": [],
                "info": [],
                "red": [
                    {
                        "condition": "CopyrightNewWorkNoPublicDomain",
                        "explanation": "The object is a relatively new work (under 70 years since its creation) so it is not in the public domain.",
                    },
                   
                ],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "debug_info": {
                "input_data": {
                    "broadcast_info": {
                        "broadcast_before_1970": "broadcast_not_made_before_1970",
                        "broadcast_cc_license": "not_applicable",
                        "broadcast_current_rightholder": "rightholder_unknown",
                        "broadcast_rights_acquired_to_make_available": "not_applicable",
                        "broadcast_year": None,
                        "broadcasters": [{"country_of_origin": "EU"}],
                        "is_broadcast": "not_broadcast",
                        "is_compound_broadcast": "not_compound",
                    },
                    "copyright_info": {
                        "architecture_country": "XX",
                        "author_alive": "author_alive",
                        "author_death_year": None,
                        "authors": [{"country_of_origin": "FI", "identity_known": True}],
                        "cinematographic_country": "XX",
                        "country_first_publication": "EU",
                        "created_before_1850": "not_made_before_1850",
                        "creation_year": 2000,
                        "current_rightholder": "rightholder_not_us",
                        "first_available_year": 2005,
                        "first_publication_year": None,
                        "internet_first_available": "not_made_available_internet",
                        "is_compound": "not_compound",
                        "is_copyright_work": "work",
                        "is_derivative": "not_derivative",
                        "is_photography": "not_photography",
                        "is_collective": "not_collective_work",
                        "object_cc_license": "not_applicable",
                        "object_copyright_rights_acquired_to_make_available": "not_applicable",
                        "original_rightholder": "human_author",
                        "otherwise_available": "made_available_no_medium",
                        "physically_published": "not_published_on_physical_medium",
                        "simultaneous_publication_countries": ["XX"],
                        "territory_status_changed": False,
                    },
                    "digital_representation_info": {
                        "digital_repr_copyright_cc_license": "not_applicable",
                        "digital_repr_copyright_current_rightholder": "rightholder_unknown",
                        "digital_repr_copyright_rights_acquired": "not_applicable",
                        "digital_repr_film_fixation_cc_license": "not_applicable",
                        "digital_repr_film_fixation_current_rightholder": "rightholder_unknown",
                        "digital_repr_film_fixation_rights_acquired": "limited_license_agreement",
                        "digital_repr_ip_rights": {
                            "copyright": "uncertain",
                            "film_fixation_rights": "uncertain",
                            "other_ip_rights": "uncertain",
                            "phonogram_rights": "yes",
                        },
                        "digital_repr_nature": "obj_2d_to_2d",
                        "digital_repr_other_cc_license": "not_applicable",
                        "digital_repr_other_current_rightholder": "rightholder_unknown",
                        "digital_repr_other_rights_acquired": "license_agreement",
                        "digital_repr_phonogram_cc_license": "not_applicable",
                        "digital_repr_phonogram_current_rightholder": "rightholder_unknown",
                        "digital_repr_phonogram_rights_acquired": "not_applicable",
                        "visual_art_work": "no",
                    },
                    "film_fixation_info": {
                        "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                        "film_fixation_available_no_medium_year": None,
                        "film_fixation_before_1920": "film_fixation_not_made_before_1920",
                        "film_fixation_cc_license": "not_applicable",
                        "film_fixation_current_rightholder": "rightholder_unknown",
                        "film_fixation_producers": [{"country_of_origin": "EU"}],
                        "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                        "film_fixation_published_fixed_medium_year": None,
                        "film_fixation_rights_acquired_to_make_available": "not_applicable",
                        "film_fixation_year": None,
                        "is_compound_film_fixation": "not_compound",
                        "is_film_fixation": "not_film_fixation",
                    },
                    "other_intellectual_property_info": {
                        "critical_edition": "not_critical_edition",
                        "design": "not_design",
                        "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                        "press_publication": "not_press_publication",
                        "press_publication_year": None,
                        "trademark": "not_trademark",
                    },
                    "other_restrictions_info": {
                        "object_administrative_restrictions": "no_administrative_restrictions",
                        "object_contractual_restrictions": "no_contractual_restrictions",
                        "object_discriminatory_content": "does_not_contain_discriminatory",
                        "object_legal_consultation": "no_self_answer",
                        "object_living_identifiable_info": "does_not_contain_identifiable_living",
                        "object_other_problems": "no_other_problems",
                        "object_other_sensitive_content": "does_not_contain_other_sensitive",
                        "object_ownership_status": "own_object",
                        "object_provenance_issues": "provenance_not_troublesome",
                        "object_provenance_traced": "provenance_traced",
                        "object_restrictions_notes": "",
                        "object_sensitive_historical_info": "does_not_contain_sensitive_historical",
                        "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
                    },
                    "performance_info": {
                        "is_compound_performance": "not_compound",
                        "is_performance": "performance",
                        "performance_before_1900": "performance_not_made_before_1900",
                        "performance_cc_license": "cc_by_nd",
                        "performance_current_rightholder": "rightholder_not_us",
                        "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_available",
                        "performance_fixed_not_phonogram_available_year": 2006,
                        "performance_phonogram_available": "performance_phonogram_not_available",
                        "performance_phonogram_available_year": None,
                        "performance_rights_acquired_to_make_available": "not_applicable",
                        "performance_year": 2005,
                        "performers": [
                            {"country_of_origin": "FR", "identity_known": True},
                            {"country_of_origin": "GR", "identity_known": True},
                            {"country_of_origin": "CU", "identity_known": True},
                        ],
                    },
                    "phonogram_info": {
                        "is_compound_phonogram": "not_compound",
                        "is_phonogram": "phonogram",
                        "phonogram_available_no_medium": "phonogram_publically_available_no_medium",
                        "phonogram_available_no_medium_year": 2006,
                        "phonogram_before_1900": "phonogram_not_made_before_1900",
                        "phonogram_cc_license": "cc_by",
                        "phonogram_current_rightholder": "rightholder_not_us",
                        "phonogram_producers": [{"country_of_origin": "FI"}],
                        "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                        "phonogram_published_fixed_medium_year": None,
                        "phonogram_rights_acquired_to_make_available": "not_applicable",
                        "phonogram_year": 2005,
                    },
                },
            },
            "digital_repr_status": {
                "green": [],
                "info": [],
                "red": [
                    {
                        "condition": "DigitalRepresentationPhonogramStatus",
                        "explanation": "The digital representation is protected by phonogram rights protection.",
                    }
                ],
                "rights_green": [
                    {
                        "condition": "DigitalRepresentationOtherIPOnlineAvailable",
                        "explanation": "Even if the digital representation is protected by other IP rights, you have acquired the necessary rights to make it available online.",
                    }
                ],
                "rights_yellow": [
                    {
                        "condition": "DigitalRepresentationFilmFixationOnlineAvailable",
                        "explanation": "Even if the digital representation is protected by film fixation rights, you may make it available online under a limited license or specific legal provisions. Additional verification may be needed.",
                    }
                ],
                "yellow": [
                    {
                        "condition": "DigitalRepresentationCopyrightStatus",
                        "explanation": "It is uncertain whether the digital representation is protected by copyright protection.",
                    },
                    {
                        "condition": "DigitalRepresentationFilmFixationStatus",
                        "explanation": "It is uncertain whether the digital representation is protected by film fixation rights protection.",
                    },
                    {
                        "condition": "DigitalRepresentationOtherIPStatus",
                        "explanation": "It is uncertain whether the digital representation is protected by other IP rights protection.",
                    },
                ],
            },
            "film_fixation_status": {
                "green": [
                    {
                        "condition": "PublicDomainNotAFilmFixation",
                        "explanation": "It is not protected as a film fixation.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "first_edition_status": {
                "green": [],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_ip_rights_status": {
                "green": [
                    {
                        "condition": "NotPressPublication",
                        "explanation": "The object is not a press publication.",
                    },
                    {
                        "condition": "NoOtherIPRights",
                        "explanation": "No other IP rights to consider",
                    },
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "other_legal_issues_status": {
                "green": [
                    {
                        "condition": "NoLegalIssues",
                        "explanation": "No legal issues unrelated to intellectual property found.",
                    }
                ],
                "info": [],
                "red": [],
                "rights_green": [],
                "rights_yellow": [],
                "yellow": [],
            },
            "performance_status": {
                "green": [],
                "info": [],
                "red": [
                    {
                        "condition": "PerformanceStillProtectedArticle3Publication",
                        "explanation": "The performance is still under protection.",
                    }
                ],
                "rights_green": [],
                "rights_yellow": [
                    {
                        "condition": "PerformanceAvailableCCLicense",
                        "explanation": "While the performance is protected, it is available under an open content license. Additional verification of the license terms may be needed.",
                    }
                ],
                "yellow": [],
            },
            "phonogram_status": {
                "green": [],
                "info": [],
                "red": [
                    {
                        "condition": "PhonogramStillProtectedArticle3Publication",
                        "explanation": "The recording is still under protection.",
                    }
                ],
                "rights_green": [
                    {
                        "condition": "PhonogramAvailableCCLicense",
                        "explanation": "While the recording is protected, it is available under an open content license (e.g., CC0 or CC-BY).",
                    }
                ],
                "rights_yellow": [],
                "yellow": [],
            },
        },
    },
]


class TestComprehensiveScenarios(unittest.TestCase):
    def _verify_scenario(self, test_case_json):
        """Helper method to verify a single JSON scenario against all rights statuses"""
        # Extract input data and expected statuses from JSON
        input_data = extract_input_data(test_case_json)
        expected_statuses = extract_expected_statuses(test_case_json)

        # Run calculations
        results = run_comprehensive_test(input_data)

        # Verify all status sections match expected results
        for section_name, expected_section in expected_statuses.items():
            with self.subTest(section=section_name):
                actual_section = results[section_name]
                for category in STATUS_CATEGORIES:
                    expected_entries = expected_section.get(category, [])
                    actual_entries = actual_section.get(category, [])
                    self.assertEqual(
                        len(actual_entries),
                        len(expected_entries),
                        msg=f"Unexpected count in {section_name}.{category}",
                    )
                    self.assertEqual(
                        _normalize_status_entries(actual_entries),
                        _normalize_status_entries(expected_entries),
                        msg=f"Mismatched entries in {section_name}.{category}",
                    )

    def test_diverse_object_scenario(self):
        """Test diverse object scenario - covers all rights statuses"""
        test_case = _get_test_case_by_name("diverse_object_scenario")
        self._verify_scenario(test_case["json"])

    def test_territory_status_changed_scenario(self):
        """Test territory status changed scenario - covers all rights statuses"""
        test_case = _get_test_case_by_name("territory_status_changed_scenario")
        self._verify_scenario(test_case["json"])

    def test_broadcast_pre_1970_territory_changed_scenario(self):
        """Test broadcast pre-1970 with territory status changed - covers all rights statuses"""
        test_case = _get_test_case_by_name("broadcast_pre_1970_territory_changed_scenario")
        self._verify_scenario(test_case["json"])

    def test_non_eea_rule_of_shorter_term_scenario(self):
        """Test non-EEA rule of shorter term scenario - covers all rights statuses"""
        test_case = _get_test_case_by_name("non_eea_rule_of_shorter_term_scenario")
        self._verify_scenario(test_case["json"])

    def test_anonymous_anthology_scenario(self):
        """Test anonymous anthology scenario - covers all rights statuses"""
        test_case = _get_test_case_by_name("anonymous_anthology_scenario")
        self._verify_scenario(test_case["json"])

    def test_modern_multimedia_performance_scenario(self):
        """Test modern multimedia performance scenario - covers all rights statuses"""
        test_case = _get_test_case_by_name("modern_multimedia_performance_scenario")
        self._verify_scenario(test_case["json"])


if __name__ == "__main__":
    unittest.main()

