import unittest
from datetime import datetime

from utils import calculate_results, calculate_all_intermediate_values


def base_data():
    return {
        'object_name': 'Test',
        'institution_name': 'Inst',
        'is_copyright_work': 'work',
        # Minimal authors to satisfy intermediate calc; values won't affect broadcast_status
        'authors': [{'identity_known': True, 'country_of_origin': 'DE'}],
        # Defaults for object section to avoid early exits
        'created_before_1850': 'not_made_before_1850',
    }


def run_broadcast(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results['broadcast_status']


class TestBroadcastingRights(unittest.TestCase):
    """Test suite for broadcasting organisation rights calculations."""
    
    # Category 1: Basic broadcast identification tests
    def test_not_a_broadcast_green(self):
        """Test that non-broadcast objects get green status."""
        data = base_data()
        data.update({
            'is_broadcast': 'not_broadcast'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'PublicDomainNotABroadcast' for r in status['green'])

    def test_broadcast_before_1970_green(self):
        """Test that broadcasts made before 1970 get green status."""
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_made_before_1970'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'PublicDomainRuleOfThumbBroadcasts' for r in status['green'])

    def test_compound_broadcast_info(self):
        """Test that compound broadcasts show informational message."""
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'is_compound_broadcast': 'compound'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'CompoundBroadcast' for r in status['info'])

    def test_uncertain_compound_broadcast_info(self):
        """Test that uncertain compound broadcasts show informational message."""
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'is_compound_broadcast': 'uncertain'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'CompoundBroadcast' for r in status['info'])

    # Category 2: Unknown broadcast year tests
    def test_unknown_broadcast_year_yellow(self):
        """Test that unknown broadcast year results in yellow status."""
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970'
            # broadcast_year is None by default
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastYearUnknown' for r in status['yellow'])

    # Category 3: EEA broadcaster tests - 50-year protection
    def test_eea_broadcast_50_years_red(self):
        """Test that EEA broadcasts within 50 years are red."""
        current = datetime.now().year
        y0 = current - 30  # 30 years ago, still protected
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],  # EEA
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastStillProtectedArticle3' for r in status['red'])

    def test_eea_broadcast_51_years_green(self):
        """Test that EEA broadcasts over 50 years are green."""
        current = datetime.now().year
        y0 = current - 51  # 51 years ago, protection lapsed
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],  # EEA
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in status['green'])

    def test_eea_broadcast_exactly_50_years_red(self):
        """Test that EEA broadcasts exactly at 50-year boundary are red."""
        current = datetime.now().year
        y0 = current - 50  # Exactly 50 years ago
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],  # EEA
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastStillProtectedArticle3' for r in status['red'])

    # Category 4: Non-EEA broadcaster tests
    def test_non_eea_broadcast_50_years_yellow(self):
        """Test that non-EEA broadcasts within 50 years are yellow (uncertain)."""
        current = datetime.now().year
        y0 = current - 30  # 30 years ago
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'US'}],  # Non-EEA
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastNonEEAUncertain' for r in status['yellow'])

    def test_non_eea_broadcast_51_years_green(self):
        """Test that non-EEA broadcasts over 50 years are green (would be green even if EEA)."""
        current = datetime.now().year
        y0 = current - 51  # 51 years ago
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'US'}],  # Non-EEA
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastLapsedEvenIfEEA' for r in status['green'])

    # Category 5: Multiple broadcasters tests
    def test_multiple_broadcasters_mixed_eea_non_eea(self):
        """Test that mixed EEA/non-EEA broadcasters result in EEA treatment."""
        current = datetime.now().year
        y0 = current - 30  # 30 years ago, still protected
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [
                {'identity_known': True, 'country_of_origin': 'US'},  # Non-EEA
                {'identity_known': True, 'country_of_origin': 'DE'},  # EEA
                {'identity_known': True, 'country_of_origin': 'JP'}   # Non-EEA
            ],
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastStillProtectedArticle3' for r in status['red'])

    def test_multiple_broadcasters_all_non_eea(self):
        """Test that all non-EEA broadcasters result in yellow status."""
        current = datetime.now().year
        y0 = current - 30  # 30 years ago
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [
                {'identity_known': True, 'country_of_origin': 'US'},  # Non-EEA
                {'identity_known': True, 'country_of_origin': 'JP'},  # Non-EEA
                {'identity_known': True, 'country_of_origin': 'CA'}   # Non-EEA
            ],
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastNonEEAUncertain' for r in status['yellow'])

    def test_multiple_broadcasters_all_non_eea_51_years_green(self):
        """Test that all non-EEA broadcasters over 50 years are green."""
        current = datetime.now().year
        y0 = current - 51  # 51 years ago
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [
                {'identity_known': True, 'country_of_origin': 'US'},  # Non-EEA
                {'identity_known': True, 'country_of_origin': 'JP'},  # Non-EEA
                {'identity_known': True, 'country_of_origin': 'CA'}   # Non-EEA
            ],
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastLapsedEvenIfEEA' for r in status['green'])

    # Category 6: Broadcaster identity tests
    def test_broadcaster_unknown_identity(self):
        """Test that unknown broadcaster identity doesn't affect EEA status."""
        current = datetime.now().year
        y0 = current - 51  # 51 years ago, should be green
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [
                {'identity_known': False, 'country_of_origin': 'DE'},  # Unknown identity, EEA
                {'identity_known': True, 'country_of_origin': 'FR'}     # Known identity, EEA
            ],
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in status['green'])

    def test_broadcaster_unknown_country(self):
        """Test that unknown country doesn't affect EEA status if other broadcasters are EEA."""
        current = datetime.now().year
        y0 = current - 51  # 51 years ago, should be green
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [
                {'identity_known': True, 'country_of_origin': 'XX'},  # Unknown country
                {'identity_known': True, 'country_of_origin': 'DE'}   # EEA country
            ],
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in status['green'])

    def test_broadcaster_all_unknown_country(self):
        """Test that all unknown countries result in yellow status."""
        current = datetime.now().year
        y0 = current - 30  # 30 years ago
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [
                {'identity_known': True, 'country_of_origin': 'XX'},  # Unknown country
                {'identity_known': True, 'country_of_origin': 'XX'}   # Unknown country
            ],
            'broadcast_year': y0
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastNonEEAUncertain' for r in status['yellow'])

    # Category 7: Rights override tests
    def test_broadcast_rightholder_override_green(self):
        """Test that known rightholder overrides to green status."""
        current = datetime.now().year
        y0 = current - 30  # base RED via 50-year protection
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': y0,
            'broadcast_current_rightholder': 'rightholder_us'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastCurrentRightHolderKnown' for r in status['green'])

    def test_broadcast_cc_license_upgrade_green(self):
        """Test that CC0 license overrides to green status."""
        current = datetime.now().year
        y0 = current - 30  # base RED case
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': y0,
            'broadcast_cc_license': 'cc0'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastAvailableCCLicense' for r in status['green'])

    def test_broadcast_cc_license_upgrade_yellow(self):
        """Test that CC-BY-SA license overrides to yellow status."""
        current = datetime.now().year
        y0 = current - 30  # base RED case
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': y0,
            'broadcast_cc_license': 'cc_by_sa'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastAvailableCCLicense' for r in status['yellow'])

    def test_broadcast_rights_acquisition_upgrade_green(self):
        """Test that rights assignment overrides to green status."""
        current = datetime.now().year
        y0 = current - 30  # base RED case
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': y0,
            'broadcast_rights_acquired_to_make_available': 'rights_assignment'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastOnlineAvailable' for r in status['green'])

    def test_broadcast_rights_acquisition_upgrade_yellow(self):
        """Test that orphan works overrides to yellow status."""
        current = datetime.now().year
        y0 = current - 30  # base RED case
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': y0,
            'broadcast_rights_acquired_to_make_available': 'orphan_works'
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastOnlineAvailable' for r in status['yellow'])

    # Category 8: Rights override priority tests
    def test_broadcast_rights_override_priority(self):
        """Test that rights overrides follow correct priority order."""
        current = datetime.now().year
        y0 = current - 30  # base RED case
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': y0,
            'broadcast_current_rightholder': 'rightholder_us',  # Should override to GREEN
            'broadcast_cc_license': 'cc_by_sa',  # Should be ignored due to rightholder
            'broadcast_rights_acquired_to_make_available': 'orphan_works'  # Should be ignored
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'BroadcastCurrentRightHolderKnown' for r in status['green'])
        assert not any(r['condition'] == 'BroadcastAvailableCCLicense' for r in status['yellow'])
        assert not any(r['condition'] == 'BroadcastOnlineAvailable' for r in status['yellow'])

    # Category 9: Edge cases and boundary tests
    def test_broadcast_year_1970_boundary(self):
        """Test the 1970 boundary condition."""
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': 1970  # Exactly 1970, not before
        })
        status = run_broadcast(data)
        # Should be evaluated based on 50-year rule, not the 1970 rule
        current = datetime.now().year
        if current - 1970 > 50:
            assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in status['green'])
        else:
            assert any(r['condition'] == 'BroadcastStillProtectedArticle3' for r in status['red'])

    def test_broadcast_year_1969_boundary(self):
        """Test that 1969 broadcasts use the 1970 rule."""
        data = base_data()
        data.update({
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_made_before_1970',  # 1969 is before 1970
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': 1969
        })
        status = run_broadcast(data)
        assert any(r['condition'] == 'PublicDomainRuleOfThumbBroadcasts' for r in status['green'])

    # Category 10: Integration tests
    def test_broadcast_with_copyright_work(self):
        """Test that broadcast status is independent of copyright work status."""
        data = base_data()
        data.update({
            # Broadcast data
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': 1960,  # Should be GREEN for broadcast
            
            # Copyright work data (should not affect broadcast status)
            'authors': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'author_death_year': 2020,  # Very recent, would be RED for copyright
        })
        
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Broadcast should be GREEN (independent of copyright)
        broadcast_status = results['broadcast_status']
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in broadcast_status['green'])
        
        # Copyright should be RED (independent of broadcast) - copyright results are in main results dict
        assert any(r['condition'] == 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2' for r in results['copyright_status']['red'])

    def test_broadcast_with_performance(self):
        """Test that broadcast status is independent of performance status."""
        data = base_data()
        data.update({
            # Broadcast data
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': 1960,  # Should be GREEN for broadcast
            
            # Performance data (should not affect broadcast status)
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': 2020,  # Very recent, would be RED for performance
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Broadcast should be GREEN (independent of performance)
        broadcast_status = results['broadcast_status']
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in broadcast_status['green'])
        
        # Performance should be RED (independent of broadcast)
        performance_status = results['performance_status']
        assert any(r['condition'] == 'PerformanceStillProtectedArticle3S1' for r in performance_status['red'])

    def test_broadcast_with_phonogram(self):
        """Test that broadcast status is independent of phonogram status."""
        data = base_data()
        data.update({
            # Broadcast data
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': 1960,  # Should be GREEN for broadcast
            
            # Phonogram data (should not affect broadcast status)
            'is_phonogram': 'phonogram',
            'phonogram_producers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'phonogram_year': 2020,  # Very recent, would be RED for phonogram
            'phonogram_published_fixed_medium': 'phonogram_not_published_fixed_medium',
            'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
        })
        
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Broadcast should be GREEN (independent of phonogram)
        broadcast_status = results['broadcast_status']
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in broadcast_status['green'])
        
        # Phonogram should be RED (independent of broadcast)
        phonogram_status = results['phonogram_status']
        assert any(r['condition'] == 'PhonogramStillProtectedArticle3S1' for r in phonogram_status['red'])

    def test_broadcast_with_film_fixation(self):
        """Test that broadcast status is independent of film fixation status."""
        data = base_data()
        data.update({
            # Broadcast data
            'is_broadcast': 'broadcast',
            'broadcast_before_1970': 'broadcast_not_made_before_1970',
            'broadcasters': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'broadcast_year': 1960,  # Should be GREEN for broadcast
            
            # Film fixation data (should not affect broadcast status)
            'is_film_fixation': 'film_fixation',
            'film_fixation_producers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'film_fixation_year': 2020,  # Very recent, would be RED for film fixation
            'film_fixation_published_fixed_medium': 'film_fixation_not_published_fixed_medium',
            'film_fixation_available_no_medium': 'film_fixation_not_publically_available_no_medium'
        })
        
        intermediate = calculate_all_intermediate_values(data)
        results = calculate_results(data, intermediate)
        
        # Broadcast should be GREEN (independent of film fixation)
        broadcast_status = results['broadcast_status']
        assert any(r['condition'] == 'BroadcastProtectionLapsedArticle3' for r in broadcast_status['green'])
        
        # Film fixation should be RED (independent of broadcast)
        film_fixation_status = results['film_fixation_status']
        assert any(r['condition'] == 'FilmFixationStillProtectedArticle3S4S1' for r in film_fixation_status['red'])


if __name__ == '__main__':
    unittest.main()
