# pylint: disable=unsubscriptable-object, missing-function-docstring, missing-module-docstring, missing-class-docstring, line-too-long

import unittest
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
            # Separate questions for copyright
            "digital_repr_copyright_current_rightholder": None,
            "digital_repr_copyright_cc_license": "not_applicable",
            "digital_repr_copyright_rights_acquired": "no",
            # Separate questions for phonogram
            "digital_repr_phonogram_current_rightholder": None,
            "digital_repr_phonogram_cc_license": "not_applicable",
            "digital_repr_phonogram_rights_acquired": "no",
            # Separate questions for film fixation
            "digital_repr_film_fixation_current_rightholder": None,
            "digital_repr_film_fixation_cc_license": "not_applicable",
            "digital_repr_film_fixation_rights_acquired": "no",
            # Separate questions for other IP
            "digital_repr_other_current_rightholder": None,
            "digital_repr_other_cc_license": "not_applicable",
            "digital_repr_other_rights_acquired": "no",
        },
        "film_fixation_info": {},
        "performance_info": {},
        "phonogram_info": {},
        "other_intellectual_property_info": {},
        "other_restrictions_info": {},
    }


def run_digital_repr(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results["digital_repr_status"]


class TestDigitalRepresentation(unittest.TestCase):
    def test_all_no_gives_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        status = run_digital_repr(data)
        self.assertEqual(len(status["green"]), 4)
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["red"]), 0)

    def test_single_yes_gives_red_and_individual_greens(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(
            status["red"][0]["condition"], "DigitalRepresentationCopyrightStatus"
        )
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["green"]), 3)
        self.assertEqual(
            {r["condition"] for r in status["green"]},
            {
                "DigitalRepresentationPhonogramStatus",
                "DigitalRepresentationFilmFixationStatus",
                "DigitalRepresentationOtherIPStatus",
            },
        )

    def test_single_uncertain_gives_yellow_and_individual_greens(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "uncertain",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        status = run_digital_repr(data)
        self.assertEqual(len(status["yellow"]), 1)
        self.assertEqual(
            status["yellow"][0]["condition"], "DigitalRepresentationPhonogramStatus"
        )
        self.assertEqual(len(status["red"]), 0)
        self.assertEqual(len(status["green"]), 3)

    def test_mixed_statuses(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "uncertain",
                "film_fixation_rights": "no",
                "other_ip_rights": "uncertain",
            }
        )
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["yellow"]), 2)
        self.assertEqual(len(status["green"]), 1)
        self.assertEqual(
            status["green"][0]["condition"], "DigitalRepresentationFilmFixationStatus"
        )

    def test_status_names(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "yes",
                "film_fixation_rights": "yes",
                "other_ip_rights": "yes",
            }
        )
        status = run_digital_repr(data)
        status_names = {r["condition"] for r in status["red"]}
        self.assertEqual(
            status_names,
            {
                "DigitalRepresentationCopyrightStatus",
                "DigitalRepresentationPhonogramStatus",
                "DigitalRepresentationFilmFixationStatus",
                "DigitalRepresentationOtherIPStatus",
            },
        )

    def test_license_agreement_turns_red_to_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "license_agreement"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)  # Still red (protected)
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["green"]), 3)  # Other rights are green
        self.assertEqual(len(status["rights_green"]), 1)  # But has rights_green
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightOnlineAvailable"
                for r in status["rights_green"]
            )
        )

    def test_cc_by_sa_turns_red_to_rights_yellow(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc_by_sa"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)  # Still red (protected)
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["rights_yellow"]), 1)  # But has rights_yellow
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightAvailableCCLicense"
                for r in status["rights_yellow"]
            )
        )

    def test_multiple_rights_mixed_availability(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "yes",
                "film_fixation_rights": "yes",
                "other_ip_rights": "no",
            }
        )
        # Copyright: CC0 (green)
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc0"
        # Phonogram: CC BY-SA (yellow)
        data["digital_representation_info"]["digital_repr_phonogram_cc_license"] = "cc_by_sa"
        # Film fixation: no separate questions, stays red
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 3)  # All three are protected
        self.assertEqual(len(status["rights_green"]), 1)  # Copyright has rights_green
        self.assertEqual(len(status["rights_yellow"]), 1)  # Phonogram has rights_yellow
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightAvailableCCLicense"
                for r in status["rights_green"]
            )
        )
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationPhonogramAvailableCCLicense"
                for r in status["rights_yellow"]
            )
        )
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationFilmFixationStatus"
                for r in status["red"]
            )
        )

    def test_yellow_rights_acquired_on_uncertain_gives_rights_yellow(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "uncertain",  # yields initial YELLOW
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        # Apply a YELLOW rights acquired on top of an existing YELLOW
        data["digital_representation_info"]["digital_repr_phonogram_rights_acquired"] = "quote_right"
        status = run_digital_repr(data)
        self.assertEqual(len(status["yellow"]), 1)  # Still yellow (uncertain)
        self.assertEqual(len(status["rights_yellow"]), 1)  # But has rights_yellow
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationPhonogramOnlineAvailable"
                for r in status["rights_yellow"]
            )
        )

    def test_rights_acquired_separate_question_works(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        # Use separate rights_acquired question
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)  # Still red (protected)
        self.assertEqual(len(status["rights_green"]), 1)  # But has rights_green
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )

    def test_employee_rights_changes_red_to_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)  # Still red (protected)
        self.assertEqual(len(status["rights_green"]), 1)  # But has rights_green
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )

    def test_not_applicable_keeps_status(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "not_applicable"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["green"]), 3)
        self.assertEqual(len(status["rights_green"]), 0)
        self.assertEqual(
            status["red"][0]["condition"], "DigitalRepresentationCopyrightStatus"
        )

    def test_no_rights_acquired_keeps_status(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "no"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["green"]), 3)
        self.assertEqual(len(status["rights_green"]), 0)
        self.assertEqual(
            status["red"][0]["condition"], "DigitalRepresentationCopyrightStatus"
        )

    def test_unknown_keeps_status(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "unknown"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["yellow"]), 0)
        self.assertEqual(len(status["green"]), 3)
        self.assertEqual(len(status["rights_green"]), 0)
        self.assertEqual(
            status["red"][0]["condition"], "DigitalRepresentationCopyrightStatus"
        )

    def test_orphan_works_turns_red_to_rights_yellow(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "orphan_works"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)  # Still red (protected)
        self.assertEqual(len(status["rights_yellow"]), 1)  # But has rights_yellow
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightOnlineAvailable"
                for r in status["rights_yellow"]
            )
        )

    def test_used_variables_tracking_separate_questions(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc0"
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "license_agreement"
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        used_vars = set(results["debug_info"].get("used_variables", []))
        # Ensure separate question fields are tracked
        self.assertTrue(
            {
                "digital_repr_ip_rights",
                "digital_repr_copyright_current_rightholder",
                "digital_repr_copyright_cc_license",
                "digital_repr_copyright_rights_acquired",
            }.issubset(used_vars)
        )

    # ========== Rightholder Tests ==========
    
    def test_rightholder_us_copyright_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)  # Still red (protected)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )

    def test_rightholder_us_phonogram_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "yes",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_phonogram_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationPhonogramCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )

    def test_rightholder_us_film_fixation_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "no",
                "film_fixation_rights": "yes",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_film_fixation_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationFilmFixationCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )

    def test_rightholder_us_other_ip_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "yes",
            }
        )
        data["digital_representation_info"]["digital_repr_other_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationOtherIPCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )

    def test_rightholder_not_us_no_change(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_not_us"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["rights_green"]), 0)

    def test_rightholder_only_if_no_green_status(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",  # Already green
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        status = run_digital_repr(data)
        # Should not add rights_green if already green
        self.assertEqual(len(status["green"]), 4)
        self.assertEqual(len(status["rights_green"]), 0)

    # ========== CC License Tests ==========
    
    def test_cc0_copyright_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc0"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightAvailableCCLicense"
                for r in status["rights_green"]
            )
        )

    def test_cc_by_copyright_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc_by"
        status = run_digital_repr(data)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightAvailableCCLicense"
                for r in status["rights_green"]
            )
        )

    def test_cc_by_nc_sa_copyright_gives_rights_yellow(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc_by_nc_sa"
        status = run_digital_repr(data)
        self.assertEqual(len(status["red"]), 1)
        self.assertEqual(len(status["rights_yellow"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightAvailableCCLicense"
                for r in status["rights_yellow"]
            )
        )

    def test_cc_license_all_yellow_variants(self):
        yellow_licenses = ["cc_by_sa", "cc_by_nc_sa", "cc_by_nd", "cc_by_nc_nd", "other_open"]
        for license_type in yellow_licenses:
            with self.subTest(license=license_type):
                data = base_data()
                data["digital_representation_info"]["digital_repr_ip_rights"].update(
                    {
                        "copyright": "yes",
                        "phonogram_rights": "no",
                        "film_fixation_rights": "no",
                        "other_ip_rights": "no",
                    }
                )
                data["digital_representation_info"]["digital_repr_copyright_cc_license"] = license_type
                status = run_digital_repr(data)
                self.assertEqual(len(status["rights_yellow"]), 1, f"Failed for {license_type}")

    def test_cc_license_phonogram_all_variants(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "yes",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_phonogram_cc_license"] = "cc0"
        status = run_digital_repr(data)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationPhonogramAvailableCCLicense"
                for r in status["rights_green"]
            )
        )

    # ========== Rights Acquired Tests ==========
    
    def test_license_agreement_gives_rights_green(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "license_agreement"
        status = run_digital_repr(data)
        self.assertEqual(len(status["rights_green"]), 1)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightOnlineAvailable"
                for r in status["rights_green"]
            )
        )

    def test_license_acquired_all_ip_rights(self):
        # Test phonogram
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "yes",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_phonogram_rights_acquired"] = "license_agreement"
        status = run_digital_repr(data)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationPhonogramOnlineAvailable"
                for r in status["rights_green"]
            )
        )

        # Test film fixation
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "no",
                "film_fixation_rights": "yes",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_film_fixation_rights_acquired"] = "license_agreement"
        status = run_digital_repr(data)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationFilmFixationOnlineAvailable"
                for r in status["rights_green"]
            )
        )

        # Test other IP
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "no",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "yes",
            }
        )
        data["digital_representation_info"]["digital_repr_other_rights_acquired"] = "license_agreement"
        status = run_digital_repr(data)
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationOtherIPOnlineAvailable"
                for r in status["rights_green"]
            )
        )

    # ========== Combination and Precedence Tests ==========
    
    def test_rightholder_takes_precedence_over_cc_license(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc0"
        status = run_digital_repr(data)
        # Both should be present, but rightholder should be checked first
        self.assertEqual(len(status["rights_green"]), 2)  # Both rightholder and CC license
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightCurrentRightHolderKnown"
                for r in status["rights_green"]
            )
        )
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightAvailableCCLicense"
                for r in status["rights_green"]
            )
        )

    def test_multiple_separate_questions_all_applied(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_current_rightholder"] = "rightholder_us"
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc_by"
        status = run_digital_repr(data)
        # All three should add to rights_green
        self.assertEqual(len(status["rights_green"]), 2)

    def test_cc_license_on_uncertain_status(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "uncertain",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_cc_license"] = "cc0"
        status = run_digital_repr(data)
        self.assertEqual(len(status["yellow"]), 1)  # Still yellow (uncertain)
        self.assertEqual(len(status["rights_green"]), 1)  # But has rights_green

    def test_license_acquired_on_uncertain_status(self):
        data = base_data()
        data["digital_representation_info"]["digital_repr_ip_rights"].update(
            {
                "copyright": "uncertain",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "other_ip_rights": "no",
            }
        )
        data["digital_representation_info"]["digital_repr_copyright_rights_acquired"] = "license_agreement"
        status = run_digital_repr(data)
        self.assertEqual(len(status["yellow"]), 1)  # Still yellow (uncertain)
        self.assertEqual(len(status["rights_green"]), 1)  # But has rights_green


if __name__ == "__main__":
    unittest.main()

