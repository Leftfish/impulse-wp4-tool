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


def run_phonogram(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results


class TestPhonogramRights(unittest.TestCase):
    def test_not_a_phonogram_green(self):
        data = base_data()
        data["phonogram_info"].update({"is_phonogram": "not_phonogram"})
        results = run_phonogram(data)

        assert any(
            r["condition"] == "PublicDomainNotAPhonogram"
            for r in results["phonogram_status"]["green"]
        )

    def test_phonogram_before_1900_green(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_before_1900": "phonogram_made_before_1900",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PublicDomainRuleOfThumbPhonogram"
            for r in results["phonogram_status"]["green"]
        )

    def test_compound_phonogram_info(self):
        data = base_data()
        data["phonogram_info"].update(
            {"is_phonogram": "phonogram", "is_compound_phonogram": "compound"}
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "CompoundPhonogram"
            for r in results["phonogram_status"]["info"]
        )

    def test_unknown_phonogram_year_yellow(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_before_1900": "phonogram_not_made_before_1900",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramYearUnknown"
            for r in results["phonogram_status"]["yellow"]
        )

    def test_eea_never_made_publicly_available_green(self):
        current = datetime.now().year
        y0 = current - 60
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],  # EEA
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

    def test_eea_never_made_publicly_available_red(self):
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],  # EEA
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3S1"
            for r in results["phonogram_status"]["red"]
        )

    def test_eea_publication_fixed_medium_in_window_red(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": 1990,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3Publication"
            for r in results["phonogram_status"]["red"]
        )

    def test_eea_publication_fixed_medium_in_window_green(self):
        # Phonogram 1930, published 1940 → lapse 2010
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1930,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": 1940,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3Publication"
            for r in results["phonogram_status"]["green"]
        )

    def test_eea_publication_no_medium_in_window_red(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_publically_available_no_medium",
                "phonogram_available_no_medium_year": 1990,
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3Publication"
            for r in results["phonogram_status"]["red"]
        )

    def test_eea_publication_no_medium_in_window_green(self):
        # Phonogram 1930, made available 1940 → lapse 2010
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1930,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_publically_available_no_medium",
                "phonogram_available_no_medium_year": 1940,
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3Publication"
            for r in results["phonogram_status"]["green"]
        )

    def test_eea_multiple_publication_events_green(self):
        # Phonogram 1930, published 1940, made available 1950 → latest event (1950) determines protection
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1930,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": 1940,
                "phonogram_available_no_medium": "phonogram_publically_available_no_medium",
                "phonogram_available_no_medium_year": 1950,
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3Publication"
            for r in results["phonogram_status"]["green"]
        )

    def test_eea_multiple_publication_events_red(self):
        # Phonogram 1950, published 1960, made available 1990 → latest event (1990) extends protection
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": 1960,
                "phonogram_available_no_medium": "phonogram_publically_available_no_medium",
                "phonogram_available_no_medium_year": 1990,
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3Publication"
            for r in results["phonogram_status"]["red"]
        )

    def test_eea_missing_fixed_medium_year_with_yes_yellow(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": None,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramUnknownPublicationExceptions"
            for r in results["phonogram_status"]["yellow"]
        )

    def test_eea_missing_no_medium_year_with_yes_yellow(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_publically_available_no_medium",
                "phonogram_available_no_medium_year": None,
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramUnknownPublicationExceptions"
            for r in results["phonogram_status"]["yellow"]
        )

    def test_eea_uncertain_publication_yellow(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "uncertain",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramUnknownPublicationExceptions"
            for r in results["phonogram_status"]["yellow"]
        )

    def test_noneea_would_be_green_becomes_green(self):
        current = datetime.now().year
        y0 = current - 60
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "US"}
                ],  # non-EEA
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramLapsedEvenIfEEA"
            for r in results["phonogram_status"]["green"]
        )

    def test_noneea_would_be_red_becomes_yellow(self):
        # Phonogram 1950 with publication 1990 (extends to 2060 under EEA) → YELLOW non-EEA
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "US"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": 1990,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramNonEEAUncertain"
            for r in results["phonogram_status"]["yellow"]
        )

    def test_noneea_missing_event_year_yellow(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "US"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": None,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramNonEEAUncertain"
            for r in results["phonogram_status"]["yellow"]
        )

    def test_phonogram_rightholder_override_green(self):
        current = datetime.now().year
        y0 = current - 30  # base RED via never made available
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                "phonogram_current_rightholder": "rightholder_us",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramCurrentRightHolderKnown"
            for r in results["phonogram_status"]["rights_green"]
        )

    def test_phonogram_cc_license_upgrade_green(self):
        # Base RED case then CC=cc0 → GREEN override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                "phonogram_cc_license": "cc0",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramAvailableCCLicense"
            for r in results["phonogram_status"]["rights_green"]
        )

    def test_phonogram_cc_license_upgrade_yellow(self):
        # Base RED case then CC=cc_by_sa → YELLOW override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                "phonogram_cc_license": "cc_by_sa",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramAvailableCCLicense"
            for r in results["phonogram_status"]["rights_yellow"]
        )

    def test_phonogram_rights_acquisition_upgrade_green(self):
        # Base RED case then rights_assignment → GREEN override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                "phonogram_rights_acquired_to_make_available": "rights_assignment",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramOnlineAvailable"
            for r in results["phonogram_status"]["rights_green"]
        )

    def test_phonogram_rights_acquisition_upgrade_yellow(self):
        # Base RED case then orphan_works → YELLOW override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
                "phonogram_rights_acquired_to_make_available": "orphan_works",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramOnlineAvailable"
            for r in results["phonogram_status"]["rights_yellow"]
        )

    def test_phonogram_new_but_uncertain_publication(self):
        current = datetime.now().year
        y0 = current - 10
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "uncertain",
                "phonogram_available_no_medium": "uncertain",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3S1"
            for r in results["phonogram_status"]["red"]
        )

    def test_phonogram_exactly_50_years_red(self):
        current = datetime.now().year
        y0 = current - 50  # Exactly at 50-year boundary
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3S1"
            for r in results["phonogram_status"]["red"]
        )

    def test_phonogram_exactly_51_years_green(self):
        current = datetime.now().year
        y0 = current - 51  # Just over 50-year boundary
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": y0,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

    def test_phonogram_exactly_70_years_after_publication_red(self):
        current = datetime.now().year
        y0 = current - 70  # Exactly at 70-year publication boundary
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": y0,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramStillProtectedArticle3Publication"
            for r in results["phonogram_status"]["red"]
        )

    def test_phonogram_exactly_71_years_after_publication_green(self):
        current = datetime.now().year
        y0 = current - 71  # Just over 70-year publication boundary
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_year": 1950,
                "phonogram_published_fixed_medium": "phonogram_published_fixed_medium",
                "phonogram_published_fixed_medium_year": y0,
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3Publication"
            for r in results["phonogram_status"]["green"]
        )

    # Complex Scenarios (Category 9)
    def test_phonogram_multiple_producers_eea(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"},  # EEA
                    {"identity_known": True, "country_of_origin": "FR"},  # EEA
                    {"identity_known": True, "country_of_origin": "US"},  # Non-EEA
                ],
                "phonogram_year": 1960,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

    def test_phonogram_multiple_producers_non_eea(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "US"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "JP"},  # Non-EEA
                    {"identity_known": True, "country_of_origin": "CA"},  # Non-EEA
                ],
                "phonogram_year": 1960,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramLapsedEvenIfEEA"
            for r in results["phonogram_status"]["green"]
        )

    def test_phonogram_producer_unknown_identity(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {
                        "identity_known": False,
                        "country_of_origin": "DE",
                    },  # Unknown identity, EEA
                    {
                        "identity_known": True,
                        "country_of_origin": "FR",
                    },  # Known identity, EEA
                ],
                "phonogram_year": 1960,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

    def test_phonogram_producer_unknown_country(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                "is_phonogram": "phonogram",
                "phonogram_producers": [
                    {
                        "identity_known": True,
                        "country_of_origin": "XX",
                    },  # Unknown country
                    {"identity_known": True, "country_of_origin": "DE"},  # EEA country
                ],
                "phonogram_year": 1960,
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )
        results = run_phonogram(data)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

    # Integration Tests (Category 10)
    def test_phonogram_with_copyright_work(self):
        data = base_data()

        data["phonogram_info"].update(
            {
                # Phonogram data
                "is_phonogram": "phonogram",
                "phonogram_year": 1960,
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )

        data["copyright_info"].update(
            {
                # Copyright work data (should not affect phonogram status)
                "authors": [{"identity_known": True, "country_of_origin": "DE"}],
                "author_death_year": 2020,  # Very recent, would be RED for copyright
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # Phonogram should be GREEN (independent of copyright)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

        # Copyright should be RED (independent of phonogram) - copyright results are in main results dict
        assert any(
            r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
            for r in results["copyright_status"]["red"]
        )

    def test_phonogram_with_performance(self):
        data = base_data()
        data["phonogram_info"].update(
            {
                # Phonogram data
                "is_phonogram": "phonogram",
                "phonogram_year": 1960,
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )

        data["performance_info"].update(
            {
                # Performance data (should not affect phonogram status)
                "is_performance": "performance",
                "performers": [{"identity_known": True, "country_of_origin": "DE"}],
                "performance_year": 2020,  # Very recent, would be RED for performance
                "performance_phonogram_available": "performance_phonogram_not_available",
                "performance_fixed_not_phonogram_available": "performance_fixed_not_phonogram_not_available",
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # Phonogram should be GREEN (independent of performance)
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )

        # Performance should be RED (independent of phonogram)
        assert any(
            r["condition"] == "PerformanceStillProtectedArticle3S1"
            for r in results["performance_status"]["red"]
        )

    def test_phonogram_all_rights_types(self):
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
                # Phonogram: old enough to be public domain
                "is_phonogram": "phonogram",
                "phonogram_year": 1960,
                "phonogram_producers": [
                    {"identity_known": True, "country_of_origin": "DE"}
                ],
                "phonogram_published_fixed_medium": "phonogram_not_published_fixed_medium",
                "phonogram_available_no_medium": "phonogram_not_publically_available_no_medium",
            }
        )

        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)

        # All three statuses should be calculated independently
        # Copyright results are in main results dict

        assert any(
            r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
            for r in results["copyright_status"]["green"]
        )
        assert any(
            r["condition"] == "PerformanceStillProtectedArticle3S1"
            for r in results["performance_status"]["red"]
        )
        assert any(
            r["condition"] == "PhonogramProtectionLapsedArticle3S1"
            for r in results["phonogram_status"]["green"]
        )


if __name__ == "__main__":
    unittest.main()
