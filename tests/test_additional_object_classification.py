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
        "digital_representation_info": {},
        "film_fixation_info": {},
        "performance_info": {},
        "phonogram_info": {},
        "other_intellectual_property_info": {},
        "other_restrictions_info": {},
    }


def run_other_ip(data: dict) -> dict:
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results["other_ip_rights_status"]


class TestAdditionalObjectClassification(unittest.TestCase):
    """Test cases for additional object classification logic."""

    def setUp(self):
        """Set up test data."""
        self.current_year = datetime.now().year
        self.intermediate = {"CURRENT_YEAR": self.current_year}

    def test_potential_first_edition_not_work_yes(self):
        """Test potential_first_edition_not_work = yes -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"potential_first_edition_not_work": "potential_first_edition_not_work"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "PublicationNotAWork")
        self.assertIn(
            "protection equivalent to copyright", results["yellow"][0]["explanation"]
        )

    def test_potential_first_edition_not_work_uncertain(self):
        """Test potential_first_edition_not_work = uncertain -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"potential_first_edition_not_work": "uncertain"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "PublicationNotAWork")

    def test_potential_first_edition_not_work_no(self):
        """Test potential_first_edition_not_work = no -> no status."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"potential_first_edition_not_work": "not_potential_first_edition_not_work"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 0)
        self.assertEqual(len(results["red"]), 0)

    def test_critical_edition_yes(self):
        """Test critical_edition = yes -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"critical_edition": "critical_edition"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "CriticalEdition")
        self.assertIn(
            "protection equivalent or closely similar to copyright",
            results["yellow"][0]["explanation"],
        )

    def test_critical_edition_uncertain(self):
        """Test critical_edition = uncertain -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"critical_edition": "uncertain"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "CriticalEdition")

    def test_critical_edition_no(self):
        """Test critical_edition = no -> no status."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"critical_edition": "not_critical_edition"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 0)
        self.assertEqual(len(results["red"]), 0)

    def test_press_publication_not_press_publication(self):
        """Test press_publication = no -> GREEN."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"press_publication": "not_press_publication"}
        )
        results = run_other_ip(data)

        self.assertEqual(results["green"][0]["condition"], "NotPressPublication")
        self.assertIn("not a press publication", results["green"][0]["explanation"])

    def test_press_publication_yes_with_year_lapsed(self):
        """Test press_publication = yes with year > current_year + 2 -> GREEN."""
        old_year = self.current_year - 5
        data = base_data()
        data["other_intellectual_property_info"].update(
            {
                "press_publication": "press_publication",
                "press_publication_year": old_year,
            }
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["green"]), 1)
        self.assertEqual(results["green"][0]["condition"], "PressPublicationLapsed")
        self.assertIn("has lapsed", results["green"][0]["explanation"])

    def test_press_publication_yes_with_year_protected(self):
        """Test press_publication = yes with year <= current_year + 2 -> RED."""
        recent_year = self.current_year - 1
        data = base_data()
        data["other_intellectual_property_info"].update(
            {
                "press_publication": "press_publication",
                "press_publication_year": recent_year,
            }
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["red"]), 1)
        self.assertEqual(results["red"][0]["condition"], "PressPublicationProtected")
        self.assertIn("may be protected", results["red"][0]["explanation"])

    def test_press_publication_uncertain_no_year(self):
        """Test press_publication = uncertain with no year -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"press_publication": "uncertain"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "PressPublicationUncertain")

    def test_press_publication_yes_no_year(self):
        """Test press_publication = yes with no year -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"press_publication": "press_publication"}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "PressPublicationProtected")

    def test_trademark_yes(self):
        """Test trademark = yes -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update({"trademark": "trademark"})
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "Trademark")
        self.assertIn(
            "obstacles stemming from trademark law", results["yellow"][0]["explanation"]
        )

    def test_trademark_uncertain(self):
        """Test trademark = uncertain -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update({"trademark": "uncertain"})
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "Trademark")

    def test_trademark_no(self):
        """Test trademark = no -> no status."""
        data = base_data()
        data["other_intellectual_property_info"].update({"trademark": "not_trademark"})
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 0)
        self.assertEqual(len(results["red"]), 0)

    def test_design_yes(self):
        """Test design = yes -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update({"design": "design"})
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "Design")
        self.assertIn(
            "obstacles stemming from design law", results["yellow"][0]["explanation"]
        )

    def test_design_uncertain(self):
        """Test design = uncertain -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update({"design": "uncertain"})
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "Design")
        

    def test_design_no(self):
        """Test design = no -> no status."""
        data = base_data()
        data["other_intellectual_property_info"].update({"design": "not_design"})
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 0)
        self.assertEqual(len(results["red"]), 0)

    def test_no_other_rights(self):
        """Test if no IP rights status is properly assigned."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {
                "potential_first_edition_not_work": "not_potential_first_edition_not_work",
                "critical_edition": "not_critical_edition",
                "press_publication": "not_press_publication",
                "trademark": "not_trademark",
                "design_status": "not_design",
            }
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["green"]), 2)
        self.assertEqual(results["green"][1]["condition"], "NoOtherIPRights")
        self.assertIn(
            "No other IP rights to consider", results["green"][1]["explanation"]
        )

    def test_multiple_conditions(self):
        """Test multiple conditions together."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {
                "potential_first_edition_not_work": "potential_first_edition_not_work",
                "critical_edition": "critical_edition",
                "press_publication": "not_press_publication",
                "trademark": "trademark",
                "design": "design",
            }
        )
        results = run_other_ip(data)

        # Should have 4 yellow statuses and 1 green status
        self.assertEqual(len(results["yellow"]), 4)
        self.assertEqual(len(results["green"]), 1)
        self.assertEqual(len(results["red"]), 0)

        # Check that all fields are marked as used
        expected_used = {
            "potential_first_edition_not_work",
            "critical_edition",
            "press_publication",
            "trademark",
            "design",
        }

    def test_press_publication_year_zero(self):
        """Test press_publication_year = 0 (blank) -> YELLOW."""
        data = base_data()
        data["other_intellectual_property_info"].update(
            {"press_publication": "press_publication", "press_publication_year": 0}
        )
        results = run_other_ip(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "PressPublicationProtected")


if __name__ == "__main__":
    unittest.main()
