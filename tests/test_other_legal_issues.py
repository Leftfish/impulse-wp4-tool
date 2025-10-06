# pylint: disable=unsubscriptable-object, missing-function-docstring, missing-module-docstring, missing-class-docstring, line-too-long

"""
Test suite for other legal issues functionality.

This module tests the logic for other legal issues fields:
- object_contractual_restrictions
- object_administrative_restrictions
- object_ownership_status
- object_provenance_traced
- object_provenance_issues
- object_living_identifiable_info
- object_sensitive_historical_info
- object_totalitarian_associations
- object_discriminatory_content
- object_other_sensitive_content
- object_other_problems
"""

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
        },
        "film_fixation_info": {},
        "performance_info": {},
        "phonogram_info": {},
        "other_intellectual_property_info": {},
        "other_restrictions_info": {
            "object_contractual_restrictions": "no_contractual_restrictions",
            "object_administrative_restrictions": "no_administrative_restrictions",
            "object_ownership_status": "own_object",
            "object_provenance_traced": "provenance_traced",
            "object_provenance_issues": "provenance_not_troublesome",
            "object_living_identifiable_info": "does_not_contain_identifiable_living",
            "object_sensitive_historical_info": "does_not_contain_sensitive_historical",
            "object_totalitarian_associations": "does_not_contain_totalitarian_associations",
            "object_discriminatory_content": "does_not_contain_discriminatory",
            "object_other_sensitive_content": "does_not_contain_other_sensitive",
            "object_other_problems": "no_other_problems",
        },
    }


def run_other_issues(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results["other_legal_issues_status"]


class TestOtherLegalIssues(unittest.TestCase):
    """Test cases for other legal issues logic."""

    def test_contractual_restrictions_yes(self):
        """Test object_contractual_restrictions = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_contractual_restrictions"
        ] = "contractual_restrictions"

        results = run_other_issues(data)
        assert any(
            r["condition"] == "HasContractualRestrictions" for r in results["yellow"]
        )

    def test_contractual_restrictions_no(self):
        """Test object_contractual_restrictions = no -> no YELLOW."""
        data = base_data()
        results = run_other_issues(data)

        # Should have GREEN status since no issues found
        self.assertEqual(len(results["yellow"]), 0)
        self.assertEqual(len(results["green"]), 1)
        self.assertEqual(results["green"][0]["condition"], "NoLegalIssues")

    def test_administrative_restrictions_yes(self):
        """Test object_administrative_restrictions = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_administrative_restrictions"
        ] = "administrative_restrictions"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(
            results["yellow"][0]["condition"], "HasAdministrativeRestrictions"
        )
        self.assertIn(
            "There may be restrictions stemming from administrative legal regulations.",
            results["yellow"][0]["explanation"],
        )

    def test_ownership_status_no_basis(self):
        """Test object_ownership_status = no_basis -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"]["object_ownership_status"] = "no_basis"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "HasOwnershipIssues")
        self.assertIn(
            "ownership rights to the physical object",
            results["yellow"][0]["explanation"],
        )

    def test_ownership_status_unknown_owner(self):
        """Test object_ownership_status = unknown_owner -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"]["object_ownership_status"] = "unknown_owner"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "HasOwnershipIssues")

    def test_ownership_status_own_object(self):
        """Test object_ownership_status = own_object -> no YELLOW."""
        data = base_data()

        results = run_other_issues(data)

        # Should have GREEN status since no issues found
        self.assertEqual(len(results["green"]), 1)
        self.assertEqual(results["green"][0]["condition"], "NoLegalIssues")

    def test_provenance_not_traced(self):
        """Test object_provenance_traced = not traced -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_provenance_traced"
        ] = "provenance_not_traced"

        results = run_other_issues(data)
        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "ProvenanceNotTraced")

    def test_provenance_traced(self):
        """Test object_provenance_traced = traced -> no YELLOW."""
        data = base_data()

        results = run_other_issues(data)

        # Should have GREEN status since no issues found
        self.assertEqual(len(results["green"]), 1)
        self.assertEqual(results["green"][0]["condition"], "NoLegalIssues")

    def test_provenance_issues_troublesome(self):
        """Test object_provenance_issues = troublesome -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_provenance_issues"
        ] = "provenance_troublesome"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "HasProvenanceIssues")

    def test_living_identifiable_info_yes(self):
        """Test object_living_identifiable_info = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_living_identifiable_info"
        ] = "contains_identifiable_living"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(
            results["yellow"][0]["condition"], "ContainsLivingIdentifiableInfo"
        )

    def test_sensitive_historical_info_yes(self):
        """Test object_sensitive_historical_info = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_sensitive_historical_info"
        ] = "contains_sensitive_historical"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(
            results["yellow"][0]["condition"], "ContainsSensitiveHistoricalInfo"
        )

    def test_totalitarian_associations_yes(self):
        """Test object_totalitarian_associations = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_totalitarian_associations"
        ] = "contains_totalitarian_associations"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(
            results["yellow"][0]["condition"], "ContainsTotalitarianAssociations"
        )

    def test_discriminatory_content_yes(self):
        """Test object_discriminatory_content = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_discriminatory_content"
        ] = "contains_discriminatory"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(
            results["yellow"][0]["condition"], "ContainsDiscriminatoryContent"
        )

    def test_other_sensitive_content_yes(self):
        """Test object_other_sensitive_content = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"][
            "object_other_sensitive_content"
        ] = "contains_other_sensitive"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(
            results["yellow"][0]["condition"], "ContainsOtherSensitiveContent"
        )

    def test_other_problems_yes(self):
        """Test object_other_problems = yes -> YELLOW."""
        data = base_data()
        data["other_restrictions_info"]["object_other_problems"] = "other_problems"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 1)
        self.assertEqual(results["yellow"][0]["condition"], "HasOtherProblems")

    def test_multiple_issues(self):
        """Test multiple issues -> multiple YELLOW statuses."""
        data = base_data()
        data["other_restrictions_info"][
            "object_contractual_restrictions"
        ] = "contractual_restrictions"
        data["other_restrictions_info"][
            "object_administrative_restrictions"
        ] = "administrative_restrictions"
        data["other_restrictions_info"]["object_ownership_status"] = "no_basis"

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 3)
        assert any(
            r["condition"] == "HasContractualRestrictions" for r in results["yellow"]
        )
        assert any(
            r["condition"] == "HasAdministrativeRestrictions" for r in results["yellow"]
        )
        assert any(r["condition"] == "HasOwnershipIssues" for r in results["yellow"])

    def test_no_issues_green_status(self):
        """Test no issues -> GREEN status."""
        data = base_data()

        results = run_other_issues(data)

        self.assertEqual(len(results["yellow"]), 0)
        self.assertEqual(len(results["green"]), 1)
        assert any(r["condition"] == "NoLegalIssues" for r in results["green"])

    def test_uncertain_values(self):
        """Test uncertain values -> YELLOW statuses."""
        data = base_data()
        data["other_restrictions_info"].update(
            {
                "object_contractual_restrictions": "uncertain",
                "object_administrative_restrictions": "uncertain",
                "object_provenance_traced": "uncertain",
                "object_provenance_issues": "uncertain",
                "object_living_identifiable_info": "uncertain",
                "object_sensitive_historical_info": "uncertain",
                "object_totalitarian_associations": "uncertain",
                "object_discriminatory_content": "uncertain",
                "object_other_sensitive_content": "uncertain",
                "object_other_problems": "uncertain",
            }
        )

        results = run_other_issues(data)

        # All uncertain values should result in YELLOW statuses
        self.assertEqual(len(results["yellow"]), 10)
        self.assertTrue(
            all(
                r["condition"]
                in [
                    "HasContractualRestrictions",
                    "HasAdministrativeRestrictions",
                    "HasOwnershipIssues",
                    "ProvenanceNotTraced",
                    "HasProvenanceIssues",
                    "ContainsLivingIdentifiableInfo",
                    "ContainsSensitiveHistoricalInfo",
                    "ContainsTotalitarianAssociations",
                    "ContainsDiscriminatoryContent",
                    "ContainsOtherSensitiveContent",
                    "HasOtherProblems",
                ]
                for r in results["yellow"]
            )
        )

    def test_missing_fields(self):
        """Test missing fields -> YELLOW statuses (uncertain values)."""
        data = {
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
            "broadcast_info": {},
            "other_restrictions_info": {}
        }  # Empty data

        results = run_other_issues(data)

        # Missing fields should be treated as uncertain and generate YELLOW statuses
        self.assertEqual(len(results["yellow"]), 10)
        self.assertTrue(
            all(
                r["condition"]
                in [
                    "HasContractualRestrictions",
                    "HasAdministrativeRestrictions",
                    "HasOwnershipIssues",
                    "ProvenanceNotTraced",
                    "HasProvenanceIssues",
                    "ContainsLivingIdentifiableInfo",
                    "ContainsSensitiveHistoricalInfo",
                    "ContainsTotalitarianAssociations",
                    "ContainsDiscriminatoryContent",
                    "ContainsOtherSensitiveContent",
                    "HasOtherProblems",
                ]
                for r in results["yellow"]
            )
        )


if __name__ == "__main__":
    unittest.main()
