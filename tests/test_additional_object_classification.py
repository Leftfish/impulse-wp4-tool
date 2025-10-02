"""
Test suite for additional object classification functionality.

This module tests the new logic for additional object classification fields:
- potential_first_edition_not_work
- critical_edition
- press_publication
- press_publication_year
- trademark
- design
"""

import unittest
from datetime import datetime
from utils import calculate_additional_object_classification_status, calculate_all_intermediate_values


class TestAdditionalObjectClassification(unittest.TestCase):
    """Test cases for additional object classification logic."""

    def setUp(self):
        """Set up test data."""
        self.current_year = datetime.now().year
        self.intermediate = {'CURRENT_YEAR': self.current_year}

    def test_potential_first_edition_not_work_yes(self):
        """Test potential_first_edition_not_work = yes -> YELLOW."""
        data = {'potential_first_edition_not_work': 'potential_first_edition_not_work'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('potential_first_edition_not_work', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'PublicationNotAWork')
        self.assertIn('protection equivalent to copyright', results['yellow'][0]['explanation'])

    def test_potential_first_edition_not_work_uncertain(self):
        """Test potential_first_edition_not_work = uncertain -> YELLOW."""
        data = {'potential_first_edition_not_work': 'uncertain'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('potential_first_edition_not_work', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'PublicationNotAWork')

    def test_potential_first_edition_not_work_no(self):
        """Test potential_first_edition_not_work = no -> no status."""
        data = {'potential_first_edition_not_work': 'not_potential_first_edition_not_work'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('potential_first_edition_not_work', used_vars)
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
    

    def test_critical_edition_yes(self):
        """Test critical_edition = yes -> YELLOW."""
        data = {'critical_edition': 'critical_edition'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('critical_edition', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'CriticalEdition')
        self.assertIn('protection equivalent or closely similar to copyright', results['yellow'][0]['explanation'])

    def test_critical_edition_uncertain(self):
        """Test critical_edition = uncertain -> YELLOW."""
        data = {'critical_edition': 'uncertain'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('critical_edition', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'CriticalEdition')

    def test_critical_edition_no(self):
        """Test critical_edition = no -> no status."""
        data = {'critical_edition': 'not_critical_edition'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('critical_edition', used_vars)
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)

    def test_press_publication_not_press_publication(self):
        """Test press_publication = no -> GREEN."""
        data = {'press_publication': 'not_press_publication'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('press_publication', used_vars)
        self.assertEqual(results['green'][0]['condition'], 'NotPressPublication')
        self.assertIn('not a press publication', results['green'][0]['explanation'])

    def test_press_publication_yes_with_year_lapsed(self):
        """Test press_publication = yes with year > current_year + 2 -> GREEN."""
        old_year = self.current_year - 5
        data = {
            'press_publication': 'press_publication',
            'press_publication_year': old_year
        }
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('press_publication', used_vars)
        self.assertIn('press_publication_year', used_vars)
        self.assertEqual(len(results['green']), 1)
        self.assertEqual(results['green'][0]['condition'], 'PressPublicationLapsed')
        self.assertIn('has lapsed', results['green'][0]['explanation'])

    def test_press_publication_yes_with_year_protected(self):
        """Test press_publication = yes with year <= current_year + 2 -> RED."""
        recent_year = self.current_year - 1
        data = {
            'press_publication': 'press_publication',
            'press_publication_year': recent_year
        }
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('press_publication', used_vars)
        self.assertIn('press_publication_year', used_vars)
        self.assertEqual(len(results['red']), 1)
        self.assertEqual(results['red'][0]['condition'], 'PressPublicationProtected')
        self.assertIn('may be protected', results['red'][0]['explanation'])

    def test_press_publication_uncertain_no_year(self):
        """Test press_publication = uncertain with no year -> RED."""
        data = {'press_publication': 'uncertain'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('press_publication', used_vars)
        self.assertEqual(len(results['red']), 1)
        self.assertEqual(results['red'][0]['condition'], 'PressPublicationProtected')
        self.assertIn('publication year not provided', results['red'][0]['explanation'])

    def test_press_publication_yes_no_year(self):
        """Test press_publication = yes with no year -> RED."""
        data = {'press_publication': 'press_publication'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('press_publication', used_vars)
        self.assertEqual(len(results['red']), 1)
        self.assertEqual(results['red'][0]['condition'], 'PressPublicationProtected')

    def test_trademark_yes(self):
        """Test trademark = yes -> YELLOW."""
        data = {'trademark': 'trademark'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('trademark', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'Trademark')
        self.assertIn('obstacles stemming from trademark law', results['yellow'][0]['explanation'])

    def test_trademark_uncertain(self):
        """Test trademark = uncertain -> YELLOW."""
        data = {'trademark': 'uncertain'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('trademark', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'Trademark')

    def test_trademark_no(self):
        """Test trademark = no -> no status."""
        data = {'trademark': 'not_trademark'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('trademark', used_vars)
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)

    def test_design_yes(self):
        """Test design = yes -> YELLOW."""
        data = {'design': 'design'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('design', used_vars)
        self.assertEqual(len(results['yellow']), 1)
        self.assertEqual(results['yellow'][0]['condition'], 'Design')
        self.assertIn('obstacles stemming from design law', results['yellow'][0]['explanation'])

    def test_design_uncertain(self):
        """Test design = uncertain -> RED."""
        data = {'design': 'uncertain'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('design', used_vars)
        self.assertEqual(len(results['red']), 1)
        self.assertEqual(results['red'][0]['condition'], 'Design')
        self.assertIn('obstacles stemming from design law', results['red'][0]['explanation'])

    def test_design_no(self):
        """Test design = no -> no status."""
        data = {'design': 'not_design'}
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('design', used_vars)
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)

    def test_no_other_rights(self):
        """Test if no IP rights status is properly assigned."""
        data = {
            'potential_first_edition_not_work': 'not_potential_first_edition_not_work',
            'critical_edition': 'not_critical_edition',
            'press_publication': 'not_press_publication',
            'trademark': 'not_trademark',
            'design_status': 'not_design'
        }
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)


        self.assertIn('potential_first_edition_not_work', used_vars)
        self.assertIn('critical_edition', used_vars)
        self.assertIn('press_publication', used_vars)
        self.assertIn('trademark', used_vars)
        self.assertIn('design', used_vars)

        self.assertEqual(len(results['green']), 2)
        self.assertEqual(results['green'][1]['condition'], 'NoOtherIPRights')
        self.assertIn('No other IP rights to consider', results['green'][1]['explanation'])

    def test_multiple_conditions(self):
        """Test multiple conditions together."""
        data = {
            'potential_first_edition_not_work': 'potential_first_edition_not_work',
            'critical_edition': 'critical_edition',
            'press_publication': 'not_press_publication',
            'trademark': 'trademark',
            'design': 'design'
        }
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        # Should have 4 yellow statuses and 1 green status
        self.assertEqual(len(results['yellow']), 4)
        self.assertEqual(len(results['green']), 1)
        self.assertEqual(len(results['red']), 0)
        
        # Check that all fields are marked as used
        expected_used = {'potential_first_edition_not_work', 'critical_edition', 
                        'press_publication', 'trademark', 'design'}
        self.assertTrue(expected_used.issubset(used_vars))

    def test_press_publication_year_zero(self):
        """Test press_publication_year = 0 (blank) -> RED."""
        data = {
            'press_publication': 'press_publication',
            'press_publication_year': 0
        }
        results, used_vars = calculate_additional_object_classification_status(data, self.intermediate)
        
        self.assertIn('press_publication', used_vars)
        self.assertIn('press_publication_year', used_vars)
        self.assertEqual(len(results['red']), 1)
        self.assertEqual(results['red'][0]['condition'], 'PressPublicationProtected')


if __name__ == '__main__':
    unittest.main()
