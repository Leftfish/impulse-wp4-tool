import unittest
from datetime import datetime

from utils import calculate_results, calculate_all_intermediate_values


def base_data():
    return {
        'object_name': 'Test',
        'institution_name': 'Inst',
        'is_copyright_work': 'work',
        # Minimal authors to satisfy intermediate calc; values won't affect performance_status
        'authors': [{'identity_known': True, 'country_of_origin': 'DE'}],
        # Defaults for object section to avoid early exits
        'created_before_1850': 'not_made_before_1850',
    }


def run_perf(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results['performance_status']


class TestPerformanceRights(unittest.TestCase):
    def test_not_a_performance_green(self):
        data = base_data()
        data.update({
            'is_performance': 'not_performance'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PublicDomainNotAPerformance' for r in status['green'])

    def test_before_1900_green(self):
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performance_before_1900': 'performance_made_before_1900'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PublicDomainRuleOfThumbPerformance' for r in status['green'])

    def test_compound_info(self):
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'is_compound_performance': 'compound'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'CompoundPerformance' for r in status['info'])

    def test_unknown_performance_year_yellow(self):
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performance_before_1900': 'not_before_1900'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceYearUnknown' for r in status['yellow'])


    def test_performance_new_but_publication_uncertain(self):
        current = datetime.now().year
        y0 = current - 10
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],  # EEA
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_available',
            'performance_available_no_medium': 'performance_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceStillProtectedArticle3S1' for r in status['red'])

    def test_eea_never_made_publicly_available_green(self):
        current = datetime.now().year
        y0 = current - 60
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],  # EEA
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceProtectionLapsedArticle3S1' for r in status['green'])

    def test_eea_never_made_publicly_available_red(self):
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],  # EEA
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceStillProtectedArticle3S1' for r in status['red'])

    def test_eea_publication_phonogram_in_window_red(self):
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': 1950,
            'performance_phonogram_available': 'performance_phonogram_available',
            'performance_phonogram_available_year': 1990,
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceStillProtectedArticle3Publication' for r in status['red'])

    def test_eea_publication_phonogram_in_window_green(self):
        # Performance 1930, phonogram 1940 → lapse 2010
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': 1930,
            'performance_phonogram_available': 'performance_phonogram_available',
            'performance_phonogram_available_year': 1940,
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceProtectionLapsedArticle3Publication' for r in status['green'])

    def test_eea_missing_event_year_with_yes_yellow(self):
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': 1950,
            'performance_phonogram_available': 'performance_phonogram_available',
            'performance_phonogram_available_year': None,
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceUnknownPublicationExceptions' for r in status['yellow'])

    def test_noneea_would_be_green_becomes_green(self):
        current = datetime.now().year
        y0 = current - 60
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'US'}],  # non-EEA
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceLapsedEvenIfEEA' for r in status['green'])

    def test_noneea_would_be_red_becomes_yellow(self):
        # Perf 1950 with phonogram 1990 (extends to 2060 under EEA) → YELLOW non-EEA
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'US'}],
            'performance_year': 1950,
            'performance_phonogram_available': 'performance_phonogram_available',
            'performance_phonogram_available_year': 1990,
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceNonEEAUncertain' for r in status['yellow'])

    def test_rightholder_override_green(self):
        current = datetime.now().year
        y0 = current - 30  # base RED via never made available
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium',
            'performance_current_rightholder': 'rightholder_us'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceCurrentRightHolderKnown' for r in status['green'])

    def test_cc_license_upgrade_green(self):
        # Base RED case then CC=cc0 → GREEN override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium',
            'performance_cc_license': 'cc0'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceAvailableCCLicense' for r in status['green'])

    def test_rights_acquisition_upgrade_green(self):
        # Base RED case then rights_assignment → GREEN override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium',
            'performance_rights_acquired_to_make_available': 'rights_assignment'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceOnlineAvailable' for r in status['green'])

    def test_rights_acquisition_upgrade_yellow(self):
        # Base RED case then orphan_works → YELLOW override
        current = datetime.now().year
        y0 = current - 30
        data = base_data()
        data.update({
            'is_performance': 'performance',
            'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
            'performance_year': y0,
            'performance_phonogram_available': 'performance_phonogram_not_available',
            'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
            'performance_available_no_medium': 'performance_not_publically_available_no_medium',
            'performance_rights_acquired_to_make_available': 'orphan_works'
        })
        status = run_perf(data)
        assert any(r['condition'] == 'PerformanceOnlineAvailable' for r in status['yellow'])


if __name__ == '__main__':
    unittest.main()


