# pylint: disable=unsubscriptable-object, missing-function-docstring, missing-module-docstring, missing-class-docstring, line-too-long

import unittest
from datetime import datetime

from utils import calculate_results, calculate_all_intermediate_values


def base_data():
    return {
        "object_name": "Test",
        "institution_name": "Inst",
        "broadcast_info": {},
        "copyright_info": {
            "is_copyright_work": "work",
            "authors": [{"identity_known": True, "country_of_origin": "DE"}],
            "created_before_1850": "not_made_before_1850",
        },
        "digital_representation_info": {
            "digital_repr_ip_rights": {},
            "digital_repr_rights_availability": {},
            "digital_repr_ip_rights_acquired": {},
        },
        "film_fixation_info": {},
        "performance_info": {},
        "phonogram_info": {},
        "other_intellectual_property_info": {},
        "other_restrictions_info": {},
    }


def run_film_fixation(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results["film_fixation_status"]


class TestFilmFixationRights(unittest.TestCase):
    def test_not_a_film_fixation_green(self):
        data = base_data()
        data["film_fixation_info"].update({"is_film_fixation": "not_film_fixation"})
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "PublicDomainNotAFilmFixation" for r in status["green"]
        )

    def test_film_fixation_before_1900_green(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_made_before_1900",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "PublicDomainRuleOfThumbFilmFixation"
            for r in status["green"]
        )

    def test_compound_film_fixation_info(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "is_compound_film_fixation": "compound",
            }
        )
        status = run_film_fixation(data)
        assert any(r["condition"] == "CompoundFilmFixation" for r in status["info"])

    def test_unknown_film_fixation_year_yellow(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationYearUnknown" for r in status["yellow"]
        )

    def test_eea_never_made_publicly_available_green(self):
        current = datetime.now().year
        y0 = current - 60
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],  # EEA
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    def test_eea_never_made_publicly_available_red(self):
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],  # EEA
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S1"
            for r in status["red"]
        )

    def test_eea_publication_fixed_medium_in_window_red(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": 1990,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S2"
            for r in status["red"]
        )

    def test_eea_publication_fixed_medium_in_window_green(self):
        # Film fixation 1930, published 1940 → lapse 1990 (50 years from publication)
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1930,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": 1940,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S2"
            for r in status["green"]
        )

    def test_eea_publication_no_medium_in_window_red(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_publically_available_no_medium",
                "film_fixation_available_no_medium_year": 1990,
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S2"
            for r in status["red"]
        )

    def test_eea_publication_no_medium_in_window_green(self):
        # Film fixation 1930, made available 1940 → lapse 1990 (50 years from availability)
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1930,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_publically_available_no_medium",
                "film_fixation_available_no_medium_year": 1940,
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S2"
            for r in status["green"]
        )

    def test_eea_multiple_publication_events_green(self):
        # Film fixation 1930, published 1940, made available 1950 → latest event (1950) determines protection
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1930,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": 1940,
                "film_fixation_available_no_medium": "film_fixation_publically_available_no_medium",
                "film_fixation_available_no_medium_year": 1950,
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S2"
            for r in status["green"]
        )

    def test_eea_multiple_publication_events_red(self):
        # Film fixation 1950, published 1960, made available 1990 → latest event (1990) extends protection
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": 1960,
                "film_fixation_available_no_medium": "film_fixation_publically_available_no_medium",
                "film_fixation_available_no_medium_year": 1990,
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S2"
            for r in status["red"]
        )

    def test_eea_missing_fixed_medium_year_with_yes_yellow(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": None,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationUnknownPublicationExceptions"
            for r in status["yellow"]
        )

    def test_eea_missing_no_medium_year_with_yes_yellow(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_publically_available_no_medium",
                "film_fixation_available_no_medium_year": None,
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationUnknownPublicationExceptions"
            for r in status["yellow"]
        )

    def test_eea_uncertain_publication_yellow(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "uncertain",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationUnknownPublicationExceptions"
            for r in status["yellow"]
        )

    def test_noneea_would_be_green_becomes_green(self):
        current = datetime.now().year
        y0 = current - 60
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "US"}
                ],  # non-EEA
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationLapsedEvenIfEEA" for r in status["green"]
        )

    def test_noneea_would_be_red_becomes_yellow(self):
        # Film fixation 1950 with publication 1990 (extends to 2040 under EEA) → YELLOW non-EEA
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "US"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": 1990,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationNonEEAUncertain" for r in status["yellow"]
        )

    def test_noneea_missing_event_year_yellow(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "US"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": None,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationNonEEAUncertain" for r in status["yellow"]
        )

    def test_film_fixation_rightholder_override_green(self):
        current = datetime.now().year
        y0 = current - 30  # base RED via never made available
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                "film_fixation_current_rightholder": "rightholder_us",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationCurrentRightHolderKnown"
            for r in status["rights_green"]
        )

    def test_film_fixation_cc_license_upgrade_green(self):
        # Base RED case then CC=cc0 → GREEN override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                "film_fixation_cc_license": "cc0",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationAvailableCCLicense"
            for r in status["rights_green"]
        )

    def test_film_fixation_cc_license_upgrade_yellow(self):
        # Base RED case then CC=cc_by_sa → YELLOW override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                "film_fixation_cc_license": "cc_by_sa",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationAvailableCCLicense"
            for r in status["rights_yellow"]
        )

    def test_film_fixation_rights_acquisition_upgrade_green(self):
        # Base RED case then rights_assignment → GREEN override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                "film_fixation_rights_acquired_to_make_available": "rights_assignment",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationOnlineAvailable"
            for r in status["rights_green"]
        )

    def test_film_fixation_rights_acquisition_upgrade_yellow(self):
        # Base RED case then orphan_works → YELLOW override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
                "film_fixation_rights_acquired_to_make_available": "orphan_works",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationOnlineAvailable"
            for r in status["rights_yellow"]
        )

    def test_film_fixation_exactly_50_years_red(self):
        current = datetime.now().year
        y0 = current - 50  # Exactly at 50-year boundary
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S1"
            for r in status["red"]
        )

    def test_film_fixation_exactly_51_years_green(self):
        current = datetime.now().year
        y0 = current - 51  # Just over 50-year boundary
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    def test_film_fixation_exactly_50_years_after_publication_red(self):
        current = datetime.now().year
        y0 = current - 50  # Exactly at 50-year publication boundary
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": y0,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S2"
            for r in status["red"]
        )

    def test_film_fixation_exactly_51_years_after_publication_green(self):
        current = datetime.now().year
        y0 = current - 51  # Just over 50-year publication boundary
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": y0,
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S2"
            for r in status["green"]
        )

    # Complex Scenarios (Category 9)
    def test_film_fixation_multiple_producers_eea(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"},  # EEA
                    {"identity_known": True, "country_of_origin": "FR"},  # EEA
                    {"identity_known": True, "country_of_origin": "US"},  # Non-EEA
                ],
                "film_fixation_year": 1960,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    def test_film_fixation_multiple_producers_non_eea(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "US"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "JP"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "CA"},  # Non-EEA
                ],
                "film_fixation_year": 1960,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationLapsedEvenIfEEA" for r in status["green"]
        )

    def test_film_fixation_producer_unknown_identity(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {
                        "identity_known": False,
                        "country_of_origin": "DE",
                    },  # Unknown identity, EEA
                    {
                        "identity_known": True,
                        "country_of_origin": "FR",
                    },  # Known identity, EEA
                ],
                "film_fixation_year": 1960,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    def test_film_fixation_producer_unknown_country(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {
                        "identity_known": True,
                        "country_of_origin": "XX",
                    },  # Unknown country
                    {"identity_known": True, "country_of_origin": "DE"},  # EEA country
                ],
                "film_fixation_year": 1960,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    # Integration Tests (Category 10)
    def test_film_fixation_with_copyright_work(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                # Film fixation data
                "is_film_fixation": "film_fixation",
                "film_fixation_year": 1960,
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        data["copyright_info"].update(
            {
                # Copyright work data (should not affect film fixation status)
                "authors": [{"identity_known": True, "country_of_origin": "DE"}],
                "author_death_year": 2020,  # Very recent, would be RED for copyright
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # Film fixation should be GREEN (independent of copyright)
        film_fixation_status = results["film_fixation_status"]
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in film_fixation_status["green"]
        )

        # Copyright should be RED (independent of film fixation) - copyright results are in main results dict
        assert any(
            r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
            for r in results["copyright_status"]["red"]
        )

    def test_film_fixation_with_performance(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                # Film fixation data
                "is_film_fixation": "film_fixation",
                "film_fixation_year": 1960,
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        data["performance_info"].update(
            {
                # Performance data (should not affect film fixation status)
                "is_performance": "performance",
                "performers": [{"identity_known": True, "country_of_origin": "DE"}],
                "performance_year": 2020,  # Very recent, would be RED for performance
                "performance_phonogram_available": "performance_phonogram_not_available",
                "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_not_available",
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # Film fixation should be GREEN (independent of performance)
        film_fixation_status = results["film_fixation_status"]
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in film_fixation_status["green"]
        )

        # Performance should be RED (independent of film fixation)
        performance_status = results["performance_status"]
        assert any(
            r["condition"] == "PerformanceStillProtectedArticle3S1"
            for r in performance_status["red"]
        )

    def test_film_fixation_with_phonogram(self):
        data = base_data()
        data["film_fixation_info"].update(
            {
                # Film fixation data
                "is_film_fixation": "film_fixation",
                "film_fixation_year": 1960,
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        data["phonogram_info"].update(
            {
                # Phonogram data (should not affect film fixation status)
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 2020,  # Very recent, would be RED for phonogram
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # Film fixation should be GREEN (independent of phonogram)
        film_fixation_status = results["film_fixation_status"]
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in film_fixation_status["green"]
        )

        # Phonogram should be RED (independent of film fixation)
        phonogram_status = results["phonogram_status"]
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3S1"
            for r in phonogram_status["red"]
        )

    def test_film_fixation_all_rights_types(self):
        data = base_data()
        data["copyright_info"].update(
            {
                # Copyright: old enough to be public domain
                "authors": [{"identity_known": True, "country_of_origin": "DE"}],
                "author_death_year": 1950,
            }
        )
        data["performance_info"].update(
            {
                # Performance: recent, still protected
                "is_performance": "performance",
                "performers": [{"identity_known": True, "country_of_origin": "DE"}],
                "performance_year": 2020,
                "performance_phonogram_available": "performance_phonogram_not_available",
                "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_not_available",
            }
        )
        data["phonogram_info"].update(
            {
                # Phonogram: recent, still protected
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 2020,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )

        data["film_fixation_info"].update(
            {
                # Film fixation: old enough to be public domain
                "is_film_fixation": "film_fixation",
                "film_fixation_year": 1960,
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # All four statuses should be calculated independently
        # Copyright results are in main results dict
        performance_status = results["performance_status"]
        phonogram_status = results["phonogram_status"]
        film_fixation_status = results["film_fixation_status"]

        assert any(
            r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
            for r in results["copyright_status"]["green"]
        )
        assert any(
            r["condition"] == "PerformanceStillProtectedArticle3S1"
            for r in performance_status["red"]
        )
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3S1"
            for r in phonogram_status["red"]
        )
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in film_fixation_status["green"]
        )

    # Additional Edge Cases and Boundary Conditions (Category 11)
    def test_film_fixation_uncertain_film_fixation_type(self):
        """Test when is_film_fixation is 'uncertain'"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "uncertain",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
            }
        )
        status = run_film_fixation(data)
        # Should fall through to year-based logic since it's not 'not_film_fixation'
        assert any(
            r["condition"] == "FilmFixationYearUnknown" for r in status["yellow"]
        )

    def test_film_fixation_uncertain_before_1900(self):
        """Test when film_fixation_before_1900 is 'uncertain'"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "uncertain",
            }
        )
        status = run_film_fixation(data)
        # Should fall through to year-based logic since it's not 'film_fixation_made_before_1900'
        assert any(
            r["condition"] == "FilmFixationYearUnknown" for r in status["yellow"]
        )

    def test_film_fixation_empty_producers_list(self):
        """Test with empty producers list"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [],
                "film_fixation_year": 1960,
            }
        )
        status = run_film_fixation(data)
        # Should be treated as non-EEA since no producers
        assert any(
            r["condition"] == "FilmFixationLapsedEvenIfEEA" for r in status["green"]
        )

    def test_film_fixation_producer_missing_country(self):
        """Test producer with missing country_of_origin"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [
                    {"identity_known": True}
                ],  # Missing country_of_origin
                "film_fixation_year": 1960,
            }
        )
        status = run_film_fixation(data)
        # Should be treated as non-EEA since country is None
        assert any(
            r["condition"] == "FilmFixationLapsedEvenIfEEA" for r in status["green"]
        )

    def test_film_fixation_producer_none_country(self):
        """Test producer with None country_of_origin"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": None}
                ],
                "film_fixation_year": 1960,
            }
        )
        status = run_film_fixation(data)
        # Should be treated as non-EEA since country is None
        assert any(
            r["condition"] == "FilmFixationLapsedEvenIfEEA" for r in status["green"]
        )

    def test_film_fixation_publication_outside_window(self):
        """Test publication year outside the initial protection window"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": 2010,  # Outside window (1950-2000)
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        # Should use initial protection period (1950 + 50 = 2000)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S2"
            for r in status["green"]
        )

    def test_film_fixation_new_but_uncertain_publication(self):
        current = datetime.now().year
        y0 = current - 10
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": y0,
                "film_fixation_published_fixed_medium": "uncertain",
                "film_fixation_available_no_medium": "uncertain",
            }
        )
        status = run_film_fixation(data)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S1"
            for r in status["red"]
        )

    def test_film_fixation_availability_outside_window(self):
        """Test availability year outside the initial protection window"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_publically_available_no_medium",
                "film_fixation_available_no_medium_year": 2010,  # Outside window (1950-2000)
            }
        )
        status = run_film_fixation(data)
        # Should use initial protection period (1950 + 50 = 2000)
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S2"
            for r in status["green"]
        )

    # Rights Override Edge Cases (Category 12)
    def test_film_fixation_rightholder_override_with_green(self):
        """Test rightholder override when already GREEN"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_made_before_1900",  # Already GREEN
                "film_fixation_current_rightholder": "rightholder_us",
            }
        )
        status = run_film_fixation(data)
        # Should remain GREEN with original condition, not override
        assert any(
            r["condition"] == "PublicDomainRuleOfThumbFilmFixation"
            for r in status["green"]
        )
        # Should NOT have rightholder override
        assert not any(
            r["condition"] == "FilmFixationCurrentRightHolderKnown"
            for r in status["green"]
        )

    def test_film_fixation_cc_license_with_green(self):
        """Test CC license when already GREEN"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_made_before_1900",  # Already GREEN
                "film_fixation_cc_license": "cc0",
            }
        )
        status = run_film_fixation(data)
        # Should remain GREEN with original condition
        assert any(
            r["condition"] == "PublicDomainRuleOfThumbFilmFixation"
            for r in status["green"]
        )
        # Should NOT have CC license override
        assert not any(
            r["condition"] == "FilmFixationAvailableCCLicense" for r in status["green"]
        )

    def test_film_fixation_rights_acquisition_with_green(self):
        """Test rights acquisition when already GREEN"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_made_before_1900",  # Already GREEN
                "film_fixation_rights_acquired_to_make_available": "rights_assignment",
            }
        )
        status = run_film_fixation(data)
        # Should remain GREEN with original condition
        assert any(
            r["condition"] == "PublicDomainRuleOfThumbFilmFixation"
            for r in status["green"]
        )
        # Should NOT have rights acquisition override
        assert not any(
            r["condition"] == "FilmFixationOnlineAvailable" for r in status["green"]
        )

    # Data Validation and Error Handling (Category 13)
    def test_film_fixation_invalid_publication_year_string(self):
        """Test with invalid publication year (string instead of int)"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": 1950,
                "film_fixation_published_fixed_medium": "film_fixation_published_fixed_medium",
                "film_fixation_published_fixed_medium_year": "invalid_year",  # String instead of int
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        # Should treat as missing year
        assert any(
            r["condition"] == "FilmFixationUnknownPublicationExceptions"
            for r in status["yellow"]
        )

    def test_film_fixation_negative_year(self):
        """Test with negative year values"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": -100,  # Negative year
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        # Should still calculate protection period (negative year + 50)
        current_year = datetime.now().year
        protection_end = -100 + 50
        if current_year > protection_end:
            assert any(
                r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
                for r in status["green"]
            )
        else:
            assert any(
                r["condition"] == "FilmFixationStillProtectedArticle3S4S1"
                for r in status["red"]
            )

    # Performance and Stress Testing (Category 14)
    def test_film_fixation_many_producers(self):
        """Test with many producers (performance test)"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": True, "country_of_origin": "FR"},
                    {"identity_known": True, "country_of_origin": "IT"},
                    {"identity_known": True, "country_of_origin": "ES"},
                    {"identity_known": True, "country_of_origin": "NL"},
                    {"identity_known": True, "country_of_origin": "BE"},
                    {"identity_known": True, "country_of_origin": "AT"},
                    {"identity_known": True, "country_of_origin": "SE"},
                    {"identity_known": True, "country_of_origin": "DK"},
                    {"identity_known": True, "country_of_origin": "FI"},
                ],
                "film_fixation_year": 1960,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        # All producers are EEA, should be GREEN
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    def test_film_fixation_mixed_producers_many(self):
        """Test with many mixed EEA/non-EEA producers"""
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"},  # EEA
                    {"identity_known": True, "country_of_origin": "US"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "FR"},  # EEA
                    {"identity_known": True, "country_of_origin": "JP"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "IT"},  # EEA
                    {"identity_known": True, "country_of_origin": "CA"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "ES"},  # EEA
                    {"identity_known": True, "country_of_origin": "AU"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "NL"},  # EEA
                    {"identity_known": True, "country_of_origin": "BR"},  # Non-EEA
                ],
                "film_fixation_year": 1960,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        # Has EEA producers, should be GREEN
        assert any(
            r["condition"] == "FilmFixationProtectionLapsedArticle3S4S1"
            for r in status["green"]
        )

    # Future-Proofing Tests (Category 15)
    def test_film_fixation_future_year(self):
        """Test with future film fixation year"""
        future_year = datetime.now().year + 10
        data = base_data()
        data["film_fixation_info"].update(
            {
                "is_film_fixation": "film_fixation",
                "film_fixation_before_1900": "film_fixation_not_made_before_1900",
                "film_fixation_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "film_fixation_year": future_year,
                "film_fixation_published_fixed_medium": "film_fixation_not_published_fixed_medium",
                "film_fixation_available_no_medium": "film_fixation_not_publically_available_no_medium",
            }
        )
        status = run_film_fixation(data)
        # Future year should be RED (protection hasn't started yet)
        assert any(
            r["condition"] == "FilmFixationStillProtectedArticle3S4S1"
            for r in status["red"]
        )


if __name__ == "__main__":
    unittest.main()
