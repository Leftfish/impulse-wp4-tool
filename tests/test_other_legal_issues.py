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
from datetime import datetime
from utils_modules.other_legal_issues import (
    calculate_intermediate_values_other_legal_issues,
    calculate_other_legal_issues_status
)


class TestOtherLegalIssues(unittest.TestCase):
    """Test cases for other legal issues logic."""

    def setUp(self):
        """Set up test data."""
        self.current_year = datetime.now().year
        self.intermediate = {'CURRENT_YEAR': self.current_year}
        
        # Base data with no issues
        self.base_no_issues_data = {
            'object_contractual_restrictions': 'no_contractual_restrictions',
            'object_administrative_restrictions': 'no_administrative_restrictions',
            'object_ownership_status': 'own_object',
            'object_provenance_traced': 'provenance_traced',
            'object_provenance_issues': 'provenance_not_troublesome',
            'object_living_identifiable_info': 'does_not_contain_identifiable_living',
            'object_sensitive_historical_info': 'does_not_contain_sensitive_historical',
            'object_totalitarian_associations': 'does_not_contain_totalitarian_associations',
            'object_discriminatory_content': 'does_not_contain_discriminatory',
            'object_other_sensitive_content': 'does_not_contain_other_sensitive',
            'object_other_problems': 'no_other_problems'
        }

    def test_contractual_restrictions_yes(self):
        """Test object_contractual_restrictions = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_contractual_restrictions'] = 'contractual_restrictions'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['HasContractualRestrictions'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('It is necessary to review the agreements pertaining to the use of the work to determine the scope of possible obstacles.', results['statuses'][0]['explanation'])
        self.assertIn('HasContractualRestrictions', results['mark_used'])

    def test_contractual_restrictions_no(self):
        """Test object_contractual_restrictions = no -> no YELLOW."""
        data = self.base_no_issues_data.copy()
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertFalse(intermediate['HasContractualRestrictions'])
        # Should have GREEN status since no issues found
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'GREEN')

    def test_administrative_restrictions_yes(self):
        """Test object_administrative_restrictions = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_administrative_restrictions'] = 'administrative_restrictions'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['HasAdministrativeRestrictions'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('There may be restrictions stemming from administrative legal regulations.', results['statuses'][0]['explanation'])
        self.assertIn('HasAdministrativeRestrictions', results['mark_used'])

    def test_ownership_status_no_basis(self):
        """Test object_ownership_status = no_basis -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_ownership_status'] = 'no_basis'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['HasOwnershipIssues'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('ownership rights to the physical object', results['statuses'][0]['explanation'])
        self.assertIn('HasOwnershipIssues', results['mark_used'])

    def test_ownership_status_unknown_owner(self):
        """Test object_ownership_status = unknown_owner -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_ownership_status'] = 'unknown_owner'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['HasOwnershipIssues'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')

    def test_ownership_status_own_object(self):
        """Test object_ownership_status = own_object -> no YELLOW."""
        data = self.base_no_issues_data.copy()
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertFalse(intermediate['HasOwnershipIssues'])
        # Should have GREEN status since no issues found
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'GREEN')

    def test_provenance_not_traced(self):
        """Test object_provenance_traced = not traced -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_provenance_traced'] = 'provenance_not_traced'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['ProvenanceNotTraced'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('uncertain or unknown provenance', results['statuses'][0]['explanation'])
        self.assertIn('ProvenanceNotTraced', results['mark_used'])

    def test_provenance_traced(self):
        """Test object_provenance_traced = traced -> no YELLOW."""
        data = self.base_no_issues_data.copy()
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertFalse(intermediate['ProvenanceNotTraced'])
        # Should have GREEN status since no issues found
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'GREEN')

    def test_provenance_issues_troublesome(self):
        """Test object_provenance_issues = troublesome -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_provenance_issues'] = 'provenance_troublesome'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['HasProvenanceIssues'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('troublesome provenance', results['statuses'][0]['explanation'])
        self.assertIn('HasProvenanceIssues', results['mark_used'])

    def test_living_identifiable_info_yes(self):
        """Test object_living_identifiable_info = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_living_identifiable_info'] = 'contains_identifiable_living'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['ContainsLivingIdentifiableInfo'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('personal data processing', results['statuses'][0]['explanation'])
        self.assertIn('ContainsLivingIdentifiableInfo', results['mark_used'])

    def test_sensitive_historical_info_yes(self):
        """Test object_sensitive_historical_info = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_sensitive_historical_info'] = 'contains_sensitive_historical'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['ContainsSensitiveHistoricalInfo'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('defamation claims', results['statuses'][0]['explanation'])
        self.assertIn('ContainsSensitiveHistoricalInfo', results['mark_used'])

    def test_totalitarian_associations_yes(self):
        """Test object_totalitarian_associations = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_totalitarian_associations'] = 'contains_totalitarian_associations'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['ContainsTotalitarianAssociations'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('hate-speech', results['statuses'][0]['explanation'])
        self.assertIn('ContainsTotalitarianAssociations', results['mark_used'])

    def test_discriminatory_content_yes(self):
        """Test object_discriminatory_content = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_discriminatory_content'] = 'contains_discriminatory'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['ContainsDiscriminatoryContent'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('hate-speech', results['statuses'][0]['explanation'])
        self.assertIn('ContainsDiscriminatoryContent', results['mark_used'])

    def test_other_sensitive_content_yes(self):
        """Test object_other_sensitive_content = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_other_sensitive_content'] = 'contains_other_sensitive'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['ContainsOtherSensitiveContent'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('liability on grounds other than IP', results['statuses'][0]['explanation'])
        self.assertIn('ContainsOtherSensitiveContent', results['mark_used'])

    def test_other_problems_yes(self):
        """Test object_other_problems = yes -> YELLOW."""
        data = self.base_no_issues_data.copy()
        data['object_other_problems'] = 'other_problems'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertTrue(intermediate['HasOtherProblems'])
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'YELLOW')
        self.assertIn('other legal issues that require verification', results['statuses'][0]['explanation'])
        self.assertIn('HasOtherProblems', results['mark_used'])

    def test_multiple_issues(self):
        """Test multiple issues -> multiple YELLOW statuses."""
        data = self.base_no_issues_data.copy()
        data['object_contractual_restrictions'] = 'contractual_restrictions'
        data['object_administrative_restrictions'] = 'administrative_restrictions'
        data['object_ownership_status'] = 'no_basis'
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertEqual(len(results['statuses']), 3)
        all_yellow = all(status['status'] == 'YELLOW' for status in results['statuses'])
        self.assertTrue(all_yellow)
        self.assertEqual(len(results['mark_used']), 3)
        self.assertIn('HasContractualRestrictions', results['mark_used'])
        self.assertIn('HasAdministrativeRestrictions', results['mark_used'])
        self.assertIn('HasOwnershipIssues', results['mark_used'])

    def test_no_issues_green_status(self):
        """Test no issues -> GREEN status."""
        data = self.base_no_issues_data.copy()
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        self.assertEqual(len(results['statuses']), 1)
        self.assertEqual(results['statuses'][0]['status'], 'GREEN')
        self.assertIn('no identified legal issues', results['statuses'][0]['explanation'])
        self.assertIn('NoIssuesFound', results['mark_used'])

    def test_uncertain_values(self):
        """Test uncertain values -> YELLOW statuses."""
        data = {
            'object_contractual_restrictions': 'uncertain',
            'object_administrative_restrictions': 'uncertain',
            'object_provenance_traced': 'uncertain',
            'object_provenance_issues': 'uncertain',
            'object_living_identifiable_info': 'uncertain',
            'object_sensitive_historical_info': 'uncertain',
            'object_totalitarian_associations': 'uncertain',
            'object_discriminatory_content': 'uncertain',
            'object_other_sensitive_content': 'uncertain',
            'object_other_problems': 'uncertain'
        }
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        # All uncertain values should result in YELLOW statuses
        self.assertEqual(len(results['statuses']), 10)
        all_yellow = all(status['status'] == 'YELLOW' for status in results['statuses'])
        self.assertTrue(all_yellow)

    def test_missing_fields(self):
        """Test missing fields -> YELLOW statuses (uncertain values)."""
        data = {}  # Empty data
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        results = calculate_other_legal_issues_status(data, intermediate)
        
        # Missing fields should be treated as uncertain and generate YELLOW statuses
        self.assertEqual(len(results['statuses']), 10)
        all_yellow = all(status['status'] == 'YELLOW' for status in results['statuses'])
        self.assertTrue(all_yellow)

    def test_intermediate_values_calculation(self):
        """Test intermediate values calculation."""
        data = {
            'object_contractual_restrictions': 'contractual_restrictions',
            'object_administrative_restrictions': 'no_administrative_restrictions',
            'object_ownership_status': 'own_object',
            'object_provenance_traced': 'provenance_traced',
            'object_provenance_issues': 'provenance_troublesome',
            'object_living_identifiable_info': 'does_not_contain_identifiable_living',
            'object_sensitive_historical_info': 'contains_sensitive_historical',
            'object_totalitarian_associations': 'does_not_contain_totalitarian_associations',
            'object_discriminatory_content': 'contains_discriminatory',
            'object_other_sensitive_content': 'does_not_contain_other_sensitive',
            'object_other_problems': 'no_other_problems'
        }
        intermediate = calculate_intermediate_values_other_legal_issues(data)
        
        # Check specific intermediate values
        self.assertTrue(intermediate['HasContractualRestrictions'])
        self.assertFalse(intermediate['HasAdministrativeRestrictions'])
        self.assertFalse(intermediate['HasOwnershipIssues'])
        self.assertFalse(intermediate['ProvenanceNotTraced'])
        self.assertTrue(intermediate['HasProvenanceIssues'])
        self.assertFalse(intermediate['ContainsLivingIdentifiableInfo'])
        self.assertTrue(intermediate['ContainsSensitiveHistoricalInfo'])
        self.assertFalse(intermediate['ContainsTotalitarianAssociations'])
        self.assertTrue(intermediate['ContainsDiscriminatoryContent'])
        self.assertFalse(intermediate['ContainsOtherSensitiveContent'])
        self.assertFalse(intermediate['HasOtherProblems'])


if __name__ == '__main__':
    unittest.main()
