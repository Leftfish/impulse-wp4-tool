import unittest
from datetime import datetime
from utils import calculate_all_intermediate_values, calculate_results, generate_text_report

# Backward-compatible alias within tests: use unified intermediates everywhere
calculate_intermediate_values_copyright = calculate_all_intermediate_values
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
            'author_death_year': self.current_year - 71,  # More than 70 years ago
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['copyright_status']['green']))

        # Test case where conditions are not met (author death less than 70 years)
        data['author_death_year'] = self.current_year - 70
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                           for r in results['copyright_status']['green']))

    def test_article1_sec1_2_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm"""
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA country
            ],
            'author_death_year': self.current_year - 71,
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm' 
                          for r in results['copyright_status']['green']))

    def test_article1_sec3(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3"""
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'FR'}  # France (EEA)
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 71,
            'first_available_year': self.current_year - 71
            
            
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3' 
                          for r in results['copyright_status']['green']))
        
    def test_article1_sec3_uncertain_publication(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3"""
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'NL'}  # Netherlands (EEA)
            ],
            'physically_published': 'uncertain',
            'otherwise_available': 'uncertain'
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3' 
                          for r in results['copyright_status']['red']))
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3' 
                          for r in results['copyright_status']['yellow']))

    def test_article1_sec3_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm"""
        data = {
            'authors': [
                {'identity_known': False, 'country_of_origin': 'JP'}  # Japan (non-EEA)
            ],
            'first_publication_year': self.current_year - 71,
            'first_available_year': self.current_year - 71
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm' 
                          for r in results['copyright_status']['green']))

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
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6' 
                          for r in results['copyright_status']['green']))

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
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm' 
                          for r in results['copyright_status']['green']))

        # Test with unknown country
        data['authors'][0]['country_of_origin'] = 'XX'
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm' 
                          for r in results['copyright_status']['green']))
    '''
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
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        print(json.dumps(results, indent=2))
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3' 
                          for r in results['copyright_status']['green']))
    '''
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
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6' 
                          for r in results['copyright_status']['green']))

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
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should have first edition protection (YELLOW) in the specialized section
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection'
                          for r in results['first_edition_status']['yellow']))
        # Copyright should be GREEN (entered public domain)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2'
                          for r in results['copyright_status']['green']))

    def test_not_copyright_work(self):
        """Test when object is not considered a copyright work"""
        data = {
            'is_copyright_work': 'not_work'
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainNotAWork' 
                          for r in results['copyright_status']['green']))
        # No other results should be present
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

    def test_pre_1850_work(self):
        """Test when work was created before 1850"""
        data = {
            'created_before_1850': 'made_before_1850',
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))
        # No other results should be present
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

    def test_pre_1850_work_with_digital_representation(self):
        """Test that digital representation analysis runs even when object is pre-1850 (Bug #1 fix)"""
        data = {
            'created_before_1850': 'made_before_1850',
            'digital_repr_ip_rights': {
                'copyright': 'yes',
                'audio_recording_rights': 'no',
                'film_fixation_rights': 'no',
                'performance_rights': 'no',
                'other_ip_rights': 'no'
            }
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Object should be GREEN
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))
        
        # Digital representation should be analyzed (RED for copyright)
        self.assertIsNotNone(results['digital_repr_status'])
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
                          for r in results['digital_repr_status']['red']))
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationPhonogramStatus' 
                          for r in results['digital_repr_status']['green']))

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
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN because institution has rights
        self.assertTrue(any(r['condition'] == 'CurrentRightHolderKnown' 
                          for r in results['copyright_status']['rights_green']))

        # Case 2: Recent death but institution has rights
        data['author_alive'] = 'author_dead'
        data['author_death_year'] = self.current_year - 20
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN because institution has rights
        self.assertTrue(any(r['condition'] == 'CurrentRightHolderKnown' 
                          for r in results['copyright_status']['rights_green']))

    def test_rule_of_shorter_term_yellow(self):
        """Test Rule of Shorter Term cases that should be YELLOW"""
        # Case 1: Known authors, non-EEA country, less than 70 years
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}
            ],
            'author_death_year': self.current_year - 50,
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm' 
                          for r in results['copyright_status']['yellow']))


    def test_rule_of_shorter_term_yellow_anonymous(self):
        # Case 2: Anonymous work, non-EEA country, less than 70 years
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': False, 'country_of_origin': 'JP'}
            ],
            'first_publication_year': self.current_year - 50,
            'country_first_publication': 'JP'
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm' 
                          for r in results['copyright_status']['yellow']))

    def test_late_publication_of_anonymous_works(self):
        # Case 1: early anonymous work, first published very recently and after it passed to the public domain
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': False, 'country_of_origin': 'FR'}
            ],
            'first_publication_year': self.current_year - 10,
            'creation_year': self.current_year - 100
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)

        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication'
                          for r in results['copyright_status']['green']))
        
        # Case 2: anonymous work published very recently, but year of creation unknown
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': False, 'country_of_origin': 'FR'}
            ],
            'first_publication_year': self.current_year - 10,
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)

        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication'
                          for r in results['copyright_status']['yellow']))

    def test_uncertain_conditions(self):
        """Test conditions that should result in YELLOW status"""
        # Case 1: Uncertain if author is alive
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'uncertain',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightAuthorAlive' 
                          for r in results['copyright_status']['yellow']))

        # Case 2: Legal person was original rights holder
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'original_rightholder': 'legal_person',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'DE'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainArticle1Section4LegalPerson' 
                          for r in results['copyright_status']['yellow']))

        # Case 3: Uncertain original rights holder
        data['original_rightholder'] = 'uncertain'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainArticle1Section4LegalPerson' 
                          for r in results['copyright_status']['yellow']))

    def test_living_author_austria(self):
        """Test case with living author from Austria"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be RED (but can have yellow too)
        self.assertTrue(any(r['condition'] == 'CopyrightAuthorAlive' 
                          for r in results['copyright_status']['red']))

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
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be RED (but can have yellow too)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['copyright_status']['red']))

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
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should have first edition protection (YELLOW) in the specialized section
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection'
                          for r in results['first_edition_status']['yellow']))
        # Copyright should be GREEN (entered public domain)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2'
                          for r in results['copyright_status']['green']))

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
            'author_death_year': self.current_year - 71,
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN because of time passed, not because of rights holder
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['copyright_status']['green']))
        self.assertFalse(any(r['condition'] == 'CurrentRightHolderKnown' 
                           for r in results['copyright_status']['green']))

    def test_override_conditions(self):
        """Test that override conditions (not a work, pre-1850) take precedence"""
        # Case 1: Not a copyright work but would otherwise be RED
        data = {
            'is_copyright_work': 'not_work',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainNotAWork' 
                          for r in results['copyright_status']['green']))
        # No other results should be present
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

        # Case 2: Pre-1850 work but would otherwise be RED
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))
        # No other results should be present
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

        # Case 3: Pre-1850 work with posthumous edition
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'author_death_year': self.current_year - 100,
            'first_publication_year': self.current_year - 20
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection'
                          for r in results['first_edition_status']['yellow']))
        # No other results should be present
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

    def test_simplified_override_conditions(self):
        """Test that override conditions work with default values"""
        # Case 1: Not a copyright work with default values
        data = {
            'is_copyright_work': 'not_work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',  # This would normally make it RED
            'current_rightholder': 'rightholder_unknown',  # This would normally affect status
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions

            
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainNotAWork' 
                          for r in results['copyright_status']['green']))
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

        # Case 2: Pre-1850 work with default values
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'author_alive': 'author_alive',  # This would normally make it RED
            'current_rightholder': 'rightholder_unknown',  # This would normally affect status
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should be GREEN only
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))
        self.assertEqual(len(results['copyright_status']['yellow']), 0)
        self.assertEqual(len(results['copyright_status']['red']), 0)
        self.assertEqual(len(results['copyright_status']['info']), 0)

    def test_eea_origin_determination(self):
        """Test that EEA origin is determined by either author's country or publication country"""
        # Case 1: Non-EEA author but EEA first publication
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA
            ],
            'country_first_publication': 'DE',  # EEA (Germany)
            'author_death_year': self.current_year - 71,
            'physically_published': 'published_on_physical_medium',
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_intermediate_values_copyright(data)
        print(json.dumps(intermediate, indent=2))
        self.assertTrue(intermediate['CountryOfOriginEEAAnyReason'])
        
        # Case 2: EEA author but non-EEA first publication
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}  # EEA (France)
            ],
            'physically_published': 'published_on_physical_medium',
            'country_first_publication': 'US',  # Non-EEA
            'author_death_year': self.current_year - 71,
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_all_intermediate_values(data)
        self.assertTrue(intermediate['CountryOfOriginEEAAnyReason'])
        
        # Case 3: Non-EEA author and first publication, but EEA simultaneous publication
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA
            ],
            'physically_published': 'published_on_physical_medium',
            'country_first_publication': 'US',  # Non-EEA
            'simultaneous_publication_countries': ['DE'],  # EEA (Germany)
            'author_death_year': self.current_year - 71,
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_all_intermediate_values(data)
        self.assertTrue(intermediate['CountryOfOriginEEAAnyReason'])
        
        # Case 4: No EEA connection at all
        data = {
            'authors': [
                {'identity_known': True, 'country_of_origin': 'US'}  # Non-EEA
            ],
            'country_first_publication': 'US',  # Non-EEA
            'simultaneous_publication_countries': ['JP'],  # Non-EEA
            'author_death_year': self.current_year - 71,
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        intermediate = calculate_all_intermediate_values(data)
        self.assertFalse(intermediate['CountryOfOriginEEAAnyReason'])


    def test_first_edition_protection_pre_1850_recent_publication(self):
        """Test Case 1: Pre-1850 work, first published in 2020"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'first_publication_year': self.current_year - 5  # Published 5 years ago
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should have first edition protection (YELLOW)
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection' 
                          for r in results['first_edition_status']['yellow']))
        # Copyright should still be GREEN
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))

    def test_first_edition_protection_pre_1850_old_publication(self):
        """Test Case 2: Pre-1850 work, first published in 1990"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'first_publication_year': self.current_year - 35  # Published 35 years ago
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should NOT have first edition protection (protection lapsed)
        self.assertFalse(any(r['condition'] == 'FirstEditionProtection' 
                           for r in results['first_edition_status']['yellow']))
        # Copyright should still be GREEN
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))

    def test_first_edition_protection_anonymous_eea_recent_publication(self):
        """Test Case 3: Anonymous work, EEA origin, created 1940, first published 2020"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': False, 'country_of_origin': 'DE'}  # Anonymous, EEA
            ],
            'creation_year': self.current_year - 85,  # Created 85 years ago (1940)
            'first_publication_year': self.current_year - 5  # Published 5 years ago (2020)
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should have first edition protection (YELLOW)
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection' 
                          for r in results['first_edition_status']['yellow']))
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication'
                          for r in results['copyright_status']['green']))

    def test_first_edition_protection_known_author_before_public_domain(self):
        """Test Case 4: Non-anonymous author, EEA origin, author dies 1940, published 2000"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}  # Known, EEA
            ],
            'author_death_year': self.current_year - 85,  # Died 85 years ago (1940)
            'first_publication_year': self.current_year - 25  # Published 25 years ago (2000)
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should NOT have first edition protection (published before entering public domain)
        self.assertFalse(any(r['condition'] == 'FirstEditionProtection' 
                           for r in results['first_edition_status']['yellow']))
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['copyright_status']['green']))
        

    def test_first_edition_protection_known_author_after_public_domain(self):
        """Test Case 5: Non-anonymous author, EEA origin, author dies 1940, published 2020"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}  # Known, EEA
            ],
            'author_death_year': self.current_year - 85,  # Died 85 years ago (1940)
            'first_publication_year': self.current_year - 5  # Published 5 years ago (2020)
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should have first edition protection (YELLOW)
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection' 
                          for r in results['first_edition_status']['yellow']))
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['copyright_status']['green']))

    def test_first_edition_protection_first_available_than_published(self):
        """Test Case 6: Non-anonymous author, EEA origin, author dies 1905, first available 1990, published 2010"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'FR'}  # Known, EEA
            ],
            'author_death_year': self.current_year - 120,  # Died 100 years ago (1905)
            'first_available_year': self.current_year - 30,  # First available 30 years ago (1990)
            'first_publication_year': self.current_year - 15  # Published 15 years ago (2010)
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should NOT have first edition protection (published before entering public domain)
        self.assertFalse(any(r['condition'] == 'FirstEditionProtection' 
                           for r in results['first_edition_status']['yellow']))
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' 
                          for r in results['copyright_status']['green']))


    def test_first_edition_protection_no_publication_year(self):
        """Test that first edition protection is not applied when no publication year is given"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850'
            # No first_publication_year
        }
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Should NOT have first edition protection
        self.assertFalse(any(r['condition'] == 'FirstEditionProtection' 
                           for r in results['first_edition_status']['yellow']))
        # Copyright should still be GREEN
        self.assertTrue(any(r['condition'] == 'CopyrightPublicDomainRuleOfThumb' 
                          for r in results['copyright_status']['green']))

    def test_first_edition_protection_edge_case_25_years(self):
        """Test edge case where publication was exactly 25 years ago"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'first_publication_year': self.current_year - 25  # Exactly 25 years ago
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should have first edition protection (YELLOW) - exactly 25 years
        self.assertTrue(any(r['condition'] == 'FirstEditionProtection' 
                          for r in results['first_edition_status']['yellow']))

    def test_first_edition_protection_edge_case_26_years(self):
        """Test edge case where publication was 26 years ago"""
        data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'made_before_1850',
            'first_publication_year': self.current_year - 26  # 26 years ago
        }
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        # Should NOT have first edition protection (protection lapsed)
        self.assertFalse(any(r['condition'] == 'FirstEditionProtection' 
                           for r in results['first_edition_status']['yellow']))

    def test_online_availability_status(self):
        """Test online availability status modifications"""
        # Base case: Work under copyright (RED status)
        base_data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        
        # Test 1: Rights assignment upgrades RED to GREEN
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'rights_assignment'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_green']))

        # Test 2: License agreement upgrades RED to GREEN
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'license_agreement'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_green']))

        # Test 3: Orphan works upgrades RED to YELLOW
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'orphan_works'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_yellow']))

        # Test 4: Not applicable doesn't change status
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'not_applicable'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_green']))
        self.assertTrue(len(results['copyright_status']['red']) > 0)  # Original RED status remains

        # Test 5: Unknown doesn't change status
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'unknown'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_green']))
        self.assertTrue(len(results['copyright_status']['red']) > 0)  # Original RED status remains

        # Test 6: Out of commerce upgrades RED to YELLOW
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'out_of_commerce'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_yellow']))

        # Test 7: No doesn't change status
        data = base_data.copy()
        data['object_copyright_rights_acquired_to_make_available'] = 'no'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertFalse(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_green']))
        self.assertTrue(len(results['copyright_status']['red']) > 0)  # Original RED status remains

    def test_cc_license_status(self):
        """Test CC license status modifications"""
        # Base case: Work under copyright (RED status)
        base_data = {
            'is_copyright_work': 'work',
            'created_before_1850': 'not_made_before_1850',
            'author_alive': 'author_alive',
            'authors': [
                {'identity_known': True, 'country_of_origin': 'AT'}
            ],
            'physically_published': 'published_on_physical_medium', # to avoid issues with first editions
            'first_publication_year': self.current_year - 35 # to avoid issues with first editions
        }
        
        # Test 1: CC0 upgrades RED to GREEN
        data = base_data.copy()
        data['object_cc_license'] = 'cc0'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_green']))

        # Test 2: CC-BY upgrades RED to GREEN
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_green']))

        # Test 3: CC-BY-SA upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_sa'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_yellow']))

        # Test 4: CC-BY-NC-SA upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_nc_sa'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_yellow']))

        # Test 5: CC-BY-ND upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_nd'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_yellow']))

        # Test 6: CC-BY-NC-ND upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_nc_nd'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_yellow']))

        # Test 7: Not applicable doesn't change status
        data = base_data.copy()
        data['object_cc_license'] = 'not_applicable'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)

        self.assertFalse(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_green']))
        self.assertTrue(len(results['copyright_status']['red']) > 0)  # Original RED status remains

        # Test 8: CC status is applied before online availability
        data = base_data.copy()
        data['object_cc_license'] = 'cc_by_sa'  # Should make it YELLOW
        data['object_copyright_rights_acquired_to_make_available'] = 'license_agreement'  # Should then make it GREEN
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectOnlineAvailable' for r in results['copyright_status']['rights_green']))

        # Test 9: Other open license upgrades RED to YELLOW
        data = base_data.copy()
        data['object_cc_license'] = 'other_open'
        intermediate = calculate_intermediate_values_copyright(data)
        results = calculate_results(data, intermediate)
        
        self.assertTrue(any(r['condition'] == 'CopyrightObjectAvailableCCLicense' for r in results['copyright_status']['rights_yellow']))

if __name__ == '__main__':
    unittest.main() 
