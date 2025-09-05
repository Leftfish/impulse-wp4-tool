"""
Performance rights module.

This module contains logic for calculating performance rights status and related intermediate values.
"""

from datetime import datetime

from defaults import ResultsDict
from utils_modules.text_constants import (
    PerformanceCondition,
    get_explanation,
    PERFORMANCE_TERM,
    PERFORMANCE_EXTENSION_SHORT,
    PERFORMANCE_EXTENSION_LONG,
)
from data.country_codes import is_eea_country


def calculate_intermediate_values_performances(data):
    """Calculate intermediate boolean values used in performance rights calculations."""
    current_year = datetime.now().year

    # Performance-related calculations
    all_performers_known = all(performer.get('identity_known', False) for performer in data.get('performers', []))
    all_performers_pseudonymous_or_anonymous = all(not performer.get('identity_known', True) for performer in data.get('performers', []))

    # Performance country calculations
    performer_country_codes = [performer.get('country_of_origin') for performer in data.get('performers', [])]
    country_of_origin_eea_performance = any(is_eea_country(code) for code in performer_country_codes if code)
    country_of_origin_unknown_performance = all(code == 'XX' for code in performer_country_codes)

    # Performance publication status
    never_made_publicly_available_performance = (
        data.get('performance_phonogram_available') == 'performance_phonogram_not_available' and
        data.get('performance_fixed_not_phonogram_available') == 'performance_fixed_not_phonogram_not_available' and
        data.get('performance_available_no_medium') == 'performance_not_publically_available_no_medium'
    )

    # Check if any performance publication/availability field is uncertain
    uncertain_if_performance_published_or_made_available = (
        data.get('performance_phonogram_available') == 'uncertain' or
        data.get('performance_fixed_not_phonogram_available') == 'uncertain' or
        data.get('performance_available_no_medium') == 'uncertain'
    )

    return {
        'AllPerformersKnown': all_performers_known,
        'AllPerformersPseudonymousOrAnonymous': all_performers_pseudonymous_or_anonymous,
        'CountryOfOriginEEAPerformance': country_of_origin_eea_performance,
        'CountryOfOriginUnknownPerformance': country_of_origin_unknown_performance,
        'NeverMadePubliclyAvailablePerformance': never_made_publicly_available_performance,
        'UncertainIfPerformancePublishedOrMadeAvailable': uncertain_if_performance_published_or_made_available,
        'CURRENT_YEAR': current_year
    }


def calculate_performance_rights_status(data, intermediate):
    """Calculate performance rights status for the original object only."""
    results = ResultsDict()

    # Track variable usage
    used_vars = set()

    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)

    # Add compound performance info message if needed
    if data.get('is_compound_performance') in ['compound', 'uncertain']:
        mark_used('is_compound_performance')
        _cond = PerformanceCondition.CompoundPerformance.value
        results['info'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'info', 'performance'),
        })

    # Simple override conditions - these take precedence over everything
    if data.get('is_performance') == 'not_performance':
        mark_used('is_performance')
        _cond = PerformanceCondition.PublicDomainNotAPerformance.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'performance'),
        })
        return results, used_vars

    if data.get('performance_before_1900') == 'performance_made_before_1900':
        mark_used('performance_before_1900')
        _cond = PerformanceCondition.PublicDomainRuleOfThumbPerformance.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'performance'),
        })
        return results, used_vars


    # Year-based logic when not before 1900
    performance_year = data.get('performance_year')
    before_1900 = data.get('performance_before_1900') == 'performance_made_before_1900'
    country_eea_perf = intermediate.get('CountryOfOriginEEAPerformance', False)
    never_made_publicly_available_perf = intermediate.get('NeverMadePubliclyAvailablePerformance', False)
    uncertain_pub_or_available = intermediate.get('UncertainIfPerformancePublishedOrMadeAvailable', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # Resolve event years and detect missing years when a 'yes' selection was made
    phonogram_year = data.get('performance_phonogram_available_year')
    no_medium_year = data.get('performance_available_no_medium_year')
    fixed_not_phonogram_year = data.get('performance_fixed_not_phonogram_available_year')

    phonogram_yes = data.get('performance_phonogram_available') == 'performance_phonogram_available'
    no_medium_yes = data.get('performance_available_no_medium') == 'performance_publically_available_no_medium'
    fixed_not_phonogram_yes = data.get('performance_fixed_not_phonogram_available') == 'performance_fixed_not_phonogram_available'

    missing_event_years = (
        (phonogram_yes and not isinstance(phonogram_year, int)) or
        (no_medium_yes and not isinstance(no_medium_year, int)) or
        (fixed_not_phonogram_yes and not isinstance(fixed_not_phonogram_year, int))
    )

    # 4) Unknown performance year (but not before 1900)
    if not before_1900 and not performance_year:
        mark_used('performance_year')
        _cond = PerformanceCondition.PerformanceYearUnknown.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'performance'),
        })

    # 5) Known performance year logic (EEA focus)
    if not before_1900 and performance_year and country_eea_perf:
        initial_lapse_year = performance_year + PERFORMANCE_TERM
        mark_used('performance_year', 'performers')
        # b) Article 3 s.1 sentence 1: never made publicly available
        if never_made_publicly_available_perf:
            if current_year_val > initial_lapse_year:
                _cond = PerformanceCondition.PerformanceProtectionLapsedArticle3S1.value
                results['green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'green', 'performance'),
                })
            else:
                _cond = PerformanceCondition.PerformanceStillProtectedArticle3S1.value
                results['red'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'red', 'performance'),
                })

        if (uncertain_pub_or_available or missing_event_years) and current_year_val <= initial_lapse_year:
            _cond = PerformanceCondition.PerformanceStillProtectedArticle3S1.value
            results['red'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'red', 'performance'),
                })

        else:
            # c) Publication exceptions (sentences 2 and 3)
            mark_used('performance_year', 'performance_phonogram_available_year', 'performance_available_no_medium_year', 'performance_fixed_not_phonogram_available_year')
            if uncertain_pub_or_available or missing_event_years:
                _cond = PerformanceCondition.PerformanceUnknownPublicationExceptions.value
                results['yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'yellow', 'performance'),
                })
            else:
                extended_lapses = []

                # Helper to check inclusive range
                def in_initial_window(y: int) -> bool:
                    return performance_year <= y <= initial_lapse_year

                # Phonogram published/made available year → extend to event_year + 70
                if isinstance(phonogram_year, int) and in_initial_window(phonogram_year):
                    extended_lapses.append(phonogram_year + PERFORMANCE_EXTENSION_LONG)

                # Available without a medium year → extend to event_year + 50
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    extended_lapses.append(no_medium_year + PERFORMANCE_EXTENSION_SHORT)

                # Available from fixed not phonogram year → extend to event_year + 50
                if isinstance(fixed_not_phonogram_year, int) and in_initial_window(fixed_not_phonogram_year):
                    extended_lapses.append(fixed_not_phonogram_year + PERFORMANCE_EXTENSION_SHORT)

                # If no extensions, fall back to initial window end
                if not extended_lapses:
                    extended_lapses.append(initial_lapse_year)

                max_lapse = max(extended_lapses)
                if current_year_val > max_lapse:
                    _cond = PerformanceCondition.PerformanceProtectionLapsedArticle3Publication.value
                    results['green'].append({
                        'condition': _cond,
                        'explanation': get_explanation(_cond, 'green', 'performance'),
                    })
                else:
                    _cond = PerformanceCondition.PerformanceStillProtectedArticle3Publication.value
                    results['red'].append({
                        'condition': _cond,
                        'explanation': get_explanation(_cond, 'red', 'performance'),
                    })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1900 and performance_year and not country_eea_perf:
        initial_lapse_year = performance_year + PERFORMANCE_TERM

        mark_used('performance_year', 'performance_phonogram_available_year', 'performance_available_no_medium_year', 'performance_fixed_not_phonogram_available_year')
        # If uncertain publication/availability or missing event years → YELLOW
        if uncertain_pub_or_available or missing_event_years:
            _cond = PerformanceCondition.PerformanceNonEEAUncertain.value
            results['yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'yellow', 'performance'),
            })
        else:
            would_be_green = False

            if never_made_publicly_available_perf:
                # Same check as EEA: lapsed if current year past initial lapse
                would_be_green = current_year_val > initial_lapse_year
            else:
                # Publication exceptions (use event-based extensions)
                def in_initial_window(y: int) -> bool:
                    return performance_year <= y <= initial_lapse_year

                extended_lapses = []
                phonogram_year = data.get('performance_phonogram_available_year')
                if isinstance(phonogram_year, int) and in_initial_window(phonogram_year):
                    extended_lapses.append(phonogram_year + PERFORMANCE_EXTENSION_LONG)

                no_medium_year = data.get('performance_available_no_medium_year')
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    extended_lapses.append(no_medium_year + PERFORMANCE_EXTENSION_SHORT)

                fixed_not_phonogram_year = data.get('performance_fixed_not_phonogram_available_year')
                if isinstance(fixed_not_phonogram_year, int) and in_initial_window(fixed_not_phonogram_year):
                    extended_lapses.append(fixed_not_phonogram_year + PERFORMANCE_EXTENSION_SHORT)

                if not extended_lapses:
                    extended_lapses.append(initial_lapse_year)

                max_lapse = max(extended_lapses)
                would_be_green = current_year_val > max_lapse

            if would_be_green:
                _cond = PerformanceCondition.PerformanceLapsedEvenIfEEA.value
                results['green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'green', 'performance'),
                })
            else:
                _cond = PerformanceCondition.PerformanceNonEEAUncertain.value
                results['yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'yellow_uncertain', 'performance'),
                })

    # Performance-specific rights overrides (mirror copyright logic)
    # 1) Current rightholder override (green if ours and no prior green)
    mark_used('performance_current_rightholder')
    if not results['green'] and data.get('performance_current_rightholder') == 'rightholder_us':
        _cond = PerformanceCondition.PerformanceCurrentRightHolderKnown.value
        results['rights_green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'rights_green', 'performance'),
        })

    # 2) CC license override for performance
    mark_used('performance_cc_license')
    cc_choice = data.get('performance_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        perf_cc_green = ['cc0', 'cc_by']
        perf_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in perf_cc_green and (results['red'] or results['yellow']):
            _cond = PerformanceCondition.PerformanceAvailableCCLicense.value
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'performance'),
            })
        elif cc_choice in perf_cc_yellow and (results['red'] or results['yellow']):
            _cond = PerformanceCondition.PerformanceAvailableCCLicense.value
            results['rights_yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_yellow', 'performance'),
            })

    # 3) Rights acquisition override for performance
    mark_used('performance_rights_acquired_to_make_available')
    ra_choice = data.get('performance_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        perf_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        perf_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in perf_ra_green and (results['red'] or results['yellow']):
            _cond = PerformanceCondition.PerformanceOnlineAvailable.value
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'performance'),
            })
        elif ra_choice in perf_ra_yellow and (results['red'] or results['yellow']):
            _cond = PerformanceCondition.PerformanceOnlineAvailable.value
            results['rights_yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_yellow', 'performance'),
            })

    return results, used_vars
