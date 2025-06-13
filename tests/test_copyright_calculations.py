import unittest
from datetime import datetime
from utils import calculate_intermediate_values, calculate_results, generate_text_report
import json

class TestCopyrightCalculations(unittest.TestCase):
    def setUp(self):
        self.current_year = datetime.now().year

    def test_article1_sec1_2(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2"""
        # Test case where all conditions are met
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'DE'}  # Germany (EEA)
            ],
            'author_death_year': self.current_year - 71  # More than 70 years ago
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['green']))

        # Test case where conditions are not met (author death less than 70 years)
        data['author_death_year'] = self.current_year - 69
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                           for r in results['green']))

    def test_article1_sec1_2_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm"""
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA country
            ],
            'author_death_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm' 
                          for r in results['green']))

    def test_article1_sec3(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3"""
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'FR'}  # France (EEA)
            ],
            'first_publication_year': self.current_year - 71,
            'first_available_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3' 
                          for r in results['green']))

    def test_article1_sec3_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm"""
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'JP'}  # Japan (non-EEA)
            ],
            'first_publication_year': self.current_year - 71,
            'first_available_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm' 
                          for r in results['green']))

    def test_article1_sec6(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec6"""
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'IT'}  # Italy (EEA)
            ],
            'creation_year': self.current_year - 71,
            'physically_published': 'not_published_on_physical_medium',
            'otherwise_available': 'not_made_available_no_medium'
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6' 
                          for r in results['green']))

    def test_article1_sec6_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm"""
        # Test with non-EEA country
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'CN'}  # China (non-EEA)
            ],
            'creation_year': self.current_year - 71,
            'physically_published': 'not_published_on_physical_medium',
            'otherwise_available': 'not_made_available_no_medium'
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm' 
                          for r in results['green']))

        # Test with unknown country
        data['authors'][0]['country_of_origin'] = 'XX'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm' 
                          for r in results['green']))

    def test_article1_sec1_2_plus_sec3(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3"""
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'ES'}  # Spain (EEA)
            ],
            'author_death_year': self.current_year - 71,
            'first_publication_year': self.current_year - 71,
            'first_available_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3' 
                          for r in results['green']))

    def test_article1_sec1_2_plus_sec6(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6"""
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'PT'}  # Portugal (EEA)
            ],
            'author_death_year': self.current_year - 71,
            'creation_year': self.current_year - 71,
            'physically_published': 'not_published_on_physical_medium',
            'otherwise_available': 'not_made_available_no_medium'
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6' 
                          for r in results['green']))

    def test_posthumous_edition(self):
        """Test CopyrightLapsedButPosthumousEditionNotLapsed"""
        # Test case where posthumous edition is still protected
        data = {
            'author_death_year': self.current_year - 100,  # Author died long ago
            'creation_year': self.current_year - 100,      # Work created long ago
            'first_publication_year': self.current_year - 20,  # But published recently
            'first_available_year': self.current_year - 20
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightLapsedButPosthumousEditionNotLapsed' 
                          for r in results['yellow']))

        # Test case where posthumous edition protection has also expired
        data['first_publication_year'] = self.current_year - 30
        data['first_available_year'] = self.current_year - 30
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightLapsedButPosthumousEditionNotLapsed' 
                           for r in results['yellow']))

    def test_not_copyright_work(self):
        """Test when object is not considered a copyright work"""
        data = {
            'is_copyright_work': 'not_work'
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainNotAWork' 
                          for r in results['green']))
        # No other results should be present
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

    def test_pre_1850_work(self):
        """Test when work was created before 1850"""
        data = {
            'created_before_1850': 'made_before_1850'
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainRuleOfThumb' 
                          for r in results['green']))
        # No other results should be present
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

    def test_rights_holder_override(self):
        """Test when institution is the rights holder"""
        # Case 1: Living author but institution has rights
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'current_rightholder': 'rightholder_us',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ]
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN because institution has rights
        self.assertTrue(any(r['condition'] == 'CurrentRightHolderKnown' 
                          for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)

        # Case 2: Recent death but institution has rights
        data['author_alive'] = 'author_dead'
        data['author_death_year'] = self.current_year - 20
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN because institution has rights
        self.assertTrue(any(r['condition'] == 'CurrentRightHolderKnown' 
                          for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)

    def test_rule_of_shorter_term_yellow(self):
        """Test Rule of Shorter Term cases that should be YELLOW"""
        # Case 1: Known authors, non-EEA country, less than 70 years
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}
            ],
            'author_death_year': self.current_year - 50
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm' 
                          for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['green']), 0)

        # Case 2: Anonymous work, non-EEA country, less than 70 years
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': False, 'country_of_origin': 'JP'}
            ],
            'first_publication_year': self.current_year - 50
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm' 
                          for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['green']), 0)

    def test_uncertain_conditions(self):
        """Test conditions that should result in YELLOW status"""
        # Case 1: Uncertain if author is alive
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'uncertain',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}
            ]
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'AuthorAlive' 
                          for r in results['yellow']))

        # Case 2: Legal person was original rights holder
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'original_rightholder': 'legal_person',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'DE'}
            ]
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'OriginalRightholder' 
                          for r in results['yellow']))

        # Case 3: Uncertain original rights holder
        data['original_rightholder'] = 'uncertain'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'OriginalRightholder' 
                          for r in results['yellow']))

    def test_living_author_austria(self):
        """Test case with living author from Austria"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ]
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be RED (but can have yellow too)
        self.assertTrue(any(r['condition'] == 'AuthorAlive' 
                          for r in results['red']))

    def test_recent_death_austria(self):
        """Test case with author from Austria who died recently"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_dead',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ],
            'author_death_year': self.current_year - 50
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be RED (but can have yellow too)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['red']))

    def test_posthumous_edition(self):
        """Test posthumous edition cases"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_dead',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}
            ],
            'author_death_year': self.current_year - 100,
            'first_publication_year': self.current_year - 20
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightLapsedButPosthumousEditionNotLapsed' 
                          for r in results['yellow']))

    def test_green_overrides_rights_holder(self):
        """Test that GREEN status is not affected by rights holder status"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_dead',
            'current_rightholder': 'rightholder_us',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'DE'}
            ],
            'author_death_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN because of time passed, not because of rights holder
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['green']))
        self.assertFalse(any(r['condition'] == 'CurrentRightHolderKnown' 
                           for r in results['green']))

    def test_override_conditions(self):
        """Test that override conditions (not a work, pre-1850) take precedence"""
        # Case 1: Not a copyright work but would otherwise be RED
        data = {
            'is_copyright_work': 'not_work',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ]
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainNotAWork' 
                          for r in results['green']))
        # No other results should be present
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

        # Case 2: Pre-1850 work but would otherwise be RED
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ]
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainRuleOfThumb' 
                          for r in results['green']))
        # No other results should be present
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

        # Case 3: Pre-1850 work with posthumous edition
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'author_death_year': self.current_year - 100,
            'first_publication_year': self.current_year - 20
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainRuleOfThumb' 
                          for r in results['green']))
        # No other results should be present
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

    def test_simplified_override_conditions(self):
        """Test that override conditions work with default values"""
        # Case 1: Not a copyright work with default values
        data = {
            'is_copyright_work': 'not_work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',  # This would normally make it RED
            'current_rightholder': 'rightholder_unknown'  # This would normally affect status
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainNotAWork' 
                          for r in results['green']))
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

        # Case 2: Pre-1850 work with default values
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'author_alive': 'author_alive',  # This would normally make it RED
            'current_rightholder': 'rightholder_unknown'  # This would normally affect status
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'PublicDomainRuleOfThumb' 
                          for r in results['green']))
        self.assertEqual(len(results['yellow']), 0)
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['info']), 0)

    def test_eea_origin_determination(self):
        """Test that EEA origin is determined by either author's country or publication country"""
        # Case 1: Non-EEA author but EEA first publication
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA
            ],
            'country_first_publication': 'DE',  # EEA (Germany)
            'author_death_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        self.assertTrue(intermediate['CountryOfOriginEEAAnyReason'])
        
        # Case 2: EEA author but non-EEA first publication
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}  # EEA (France)
            ],
            'country_first_publication': 'US',  # Non-EEA
            'author_death_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        self.assertTrue(intermediate['CountryOfOriginEEAAnyReason'])
        
        # Case 3: Non-EEA author and first publication, but EEA simultaneous publication
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA
            ],
            'country_first_publication': 'US',  # Non-EEA
            'simultaneous_publication_countries': ['DE'],  # EEA (Germany)
            'author_death_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        self.assertTrue(intermediate['CountryOfOriginEEAAnyReason'])
        
        # Case 4: No EEA connection at all
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA
            ],
            'country_first_publication': 'US',  # Non-EEA
            'simultaneous_publication_countries': ['JP'],  # Non-EEA
            'author_death_year': self.current_year - 71
        }
        intermediate = calculate_intermediate_values(data)
        self.assertFalse(intermediate['CountryOfOriginEEAAnyReason'])

    def test_text_report_json_debug(self):
        """Test that the text report generates valid JSON debug info"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}
            ],
            'author_death_year': self.current_year - 50,
            'object_name': 'Test Object',
            'institution_name': 'ju_art_science'
        }
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Generate the text report
        report = generate_text_report(results)
        
        # Find the debug section
        debug_section = report.split('Source data (JSON):\n')[1].strip()
        
        # Verify it's valid JSON
        try:
            debug_data = json.loads(debug_section)
            self.assertIsInstance(debug_data, dict)
            self.assertIn('input_data', debug_data)
            self.assertIn('used_variables', debug_data)
            self.assertIn('unused_variables', debug_data)
        except json.JSONDecodeError:
            self.fail("Debug section is not valid JSON")

    def test_online_availability_status(self):
        """Test online availability status modifications"""
        # Base case: Work under copyright (RED status)
        base_data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ]
        }
        
        # Test 1: Rights assignment upgrades RED to GREEN
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'rights_assignment'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)

        # Test 2: License agreement upgrades RED to GREEN
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'license_agreement'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)

        # Test 3: Orphan works upgrades RED to YELLOW
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'orphan_works'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)

        # Test 4: Not applicable doesn't change status
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'not_applicable'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['green']))
        self.assertTrue(len(results['red']) > 0)  # Original RED status remains

        # Test 5: Unknown doesn't change status
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'unknown'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['green']))
        self.assertTrue(len(results['red']) > 0)  # Original RED status remains

        # Test 6: Out of commerce upgrades RED to YELLOW
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'out_of_commerce'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)

        # Test 7: No doesn't change status
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'no'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['green']))
        self.assertTrue(len(results['red']) > 0)  # Original RED status remains

    def test_cc_license_status(self):
        """Test CC license status modifications"""
        # Base case: Work under copyright (RED status)
        base_data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ]
        }
        
        # Test 1: CC0 upgrades RED to GREEN
        data = base_data.copy()
        data['object_cc_license'] = 'cc0'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)

        # Test 2: CC-BY upgrades RED to GREEN
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)

        # Test 3: CC-BY-SA upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_sa'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)

        # Test 4: CC-BY-NC-SA upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_nc_sa'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)

        # Test 5: CC-BY-ND upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_nd'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)

        # Test 6: CC-BY-NC-ND upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_nc_nd'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)

        # Test 7: Not applicable doesn't change status
        data = base_data.copy()
        data['object_cc_license'] = 'not_applicable'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['green']))
        self.assertTrue(len(results['red']) > 0)  # Original RED status remains

        # Test 8: CC status is applied before online availability
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_sa'  # Should make it YELLOW
        data['object_copyright_rights_acquired_to_make_available'] = 'license_agreement'  # Should then make it GREEN
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectOnlineAvailable' for r in results['green']))
        self.assertEqual(len(results['red']), 0)
        self.assertEqual(len(results['yellow']), 0)  # Yellow from CC-BY-SA should be upgraded to GREEN by license agreement

        # Test 9: Other open license upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'other_open'
        intermediate = calculate_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'ObjectAvailableCCLicense' for r in results['yellow']))
        self.assertEqual(len(results['red']), 0)
        self.assertTrue(len(results['yellow']) > 0)
        # Verify explanation for other open license
        yellow_result = next(r for r in results['yellow'] if r['condition'] == 'ObjectAvailableCCLicense')
        self.assertTrue('Additional verification of the license terms is needed' in yellow_result['explanation'])

if __name__ == '__main__':
    unittest.main() 