"""
Phonogram rights module.

This module contains logic for calculating phonogram rights status and related intermediate values.
"""

from defaults import ResultsDict
from utils_modules.text_constants import (
    PhonogramCondition,
    get_explanation,
    PHONOGRAM_TERM,
    PHONOGRAM_EXTENSION_SHORT,
    PHONOGRAM_EXTENSION_LONG,
)

from datetime import datetime
from data.country_codes import is_eea_country


def calculate_intermediate_values_phonograms(data):
    """Calculate intermediate boolean values used in phonogram rights calculations."""
    current_year = datetime.now().year
    
    # Use namespaced producers
    producers = data.get('phonogram_producers', [])
    
    # Producer-related calculations
    #all_producers_known = all(producer.get('identity_known', False) for producer in producers)
    #all_producers_pseudonymous_or_anonymous = all(not producer.get('identity_known', True) for producer in producers)
    
    # Producer country calculations
    # Country of origin depends on the first rightholder, i.e. producer
    producer_country_codes = [producer.get('country_of_origin') for producer in producers]
    country_of_origin_eea_phonograms = any(is_eea_country(code) for code in producer_country_codes if code)
    country_of_origin_unknown_phonograms = all(code == 'XX' for code in producer_country_codes)
    
    # Phonogram publication status
    never_made_publicly_available = (
        data.get('phonogram_published_fixed_medium') == 'phonogram_not_published_fixed_medium' and
        data.get('phonogram_available_no_medium') == 'phonogram_not_publically_available_no_medium'
    )
    
    # Check if any phonogram publication/availability field is uncertain
    uncertain_if_phonogram_published_or_made_available = (
        data.get('phonogram_published_fixed_medium') == 'uncertain' or
        data.get('phonogram_available_no_medium') == 'uncertain'
    )
    
    return {
        #'AllProducersKnownPhonograms': all_producers_known,
        #'AllProducersPseudonymousOrAnonymousPhonograms': all_producers_pseudonymous_or_anonymous,
        'CountryOfOriginEEAPhonograms': country_of_origin_eea_phonograms,
        'CountryOfOriginUnknownPhonograms': country_of_origin_unknown_phonograms,
        'NeverMadePubliclyAvailablePhonograms': never_made_publicly_available,
        'UncertainIfPhonogramPublishedOrMadeAvailable': uncertain_if_phonogram_published_or_made_available,
        'CURRENT_YEAR': current_year
    }


def calculate_phonogram_rights_status(data, intermediate):
    """Calculate phonogram rights status for the original object only."""
    results = ResultsDict()
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Add compound phonogram info message if needed
    if data.get('is_compound_phonogram') in ['compound', 'uncertain']:
        mark_used('is_compound_phonogram')
        _cond = PhonogramCondition.CompoundPhonogram.value
        results['info'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'info', 'phonogram'),
        })

    # Simple override conditions - these take precedence over everything
    # Rationale: if not a phonogram, it's not protected by the related right
    # and if made before 1900, in all likelihood not protected
    if data.get('is_phonogram') == 'not_phonogram':
        mark_used('is_phonogram')
        _cond = PhonogramCondition.PublicDomainNotAPhonogram.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'phonogram'),
        })
        return results, used_vars
    
    if data.get('phonogram_before_1900') == 'phonogram_made_before_1900':
        mark_used('phonogram_before_1900')
        _cond = PhonogramCondition.PublicDomainRuleOfThumbPhonogram.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'phonogram'),
        })
        return results, used_vars
    
    
    
    # Year-based logic when not before 1900
    phonogram_year = data.get('phonogram_year')
    before_1900 = data.get('phonogram_before_1900') == 'phonogram_made_before_1900'
    country_eea_phonogram = intermediate.get('CountryOfOriginEEAPhonograms', False)
    never_made_publicly_available_phonogram = intermediate.get('NeverMadePubliclyAvailablePhonograms', False)
    uncertain_pub_or_available = intermediate.get('UncertainIfPhonogramPublishedOrMadeAvailable', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # Unknown phonogram year (but not before 1900)
    # Rationale: if we don't know the year, we cannot determine
    # if it's protected or not (e.g. whether the publication fell within
    # the initial 50-year term)
    if not before_1900 and not phonogram_year:
        mark_used('phonogram_year')
        _cond = PhonogramCondition.PhonogramYearUnknown.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'phonogram'),
        })

    # Known phonogram year logic 
    # Rationale: Article 3(2) Term Directive for EEA
    # we do not take into account the reversion rights from article 3(2a)
    if not before_1900 and phonogram_year and country_eea_phonogram:
        phonogram_initial_protection_lapse = phonogram_year + PHONOGRAM_TERM
        mark_used('phonogram_year', 'phonogram_producers')

        # Resolve event years and detect missing years when a 'yes' selection was made
        fixed_medium_year = data.get('phonogram_published_fixed_medium_year')
        no_medium_year = data.get('phonogram_available_no_medium_year')

        fixed_medium_yes = data.get('phonogram_published_fixed_medium') == 'phonogram_published_fixed_medium'
        no_medium_yes = data.get('phonogram_available_no_medium') == 'phonogram_publically_available_no_medium'

        missing_event_years = (
            (fixed_medium_yes and not isinstance(fixed_medium_year, int)) or
            (no_medium_yes and not isinstance(no_medium_year, int))
        )

        # Article 3 sec. 2 sent. 1: never made publicly available
        if never_made_publicly_available_phonogram:
            if current_year_val > phonogram_initial_protection_lapse:
                _cond = PhonogramCondition.PhonogramProtectionLapsedArticle3S1.value
                results['green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'green', 'phonogram'),
                })
            else:
                _cond = PhonogramCondition.PhonogramStillProtectedArticle3S1.value
                results['red'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'red', 'phonogram'),
                })
        if (uncertain_pub_or_available or missing_event_years) and current_year_val <= phonogram_initial_protection_lapse:
            _cond = PhonogramCondition.PhonogramStillProtectedArticle3S1.value
            results['red'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'red', 'phonogram'),
                })
        else:
            # Extensions sentences 2 and 3)
            mark_used('phonogram_year', 'phonogram_published_fixed_medium_year', 'phonogram_available_no_medium_year')
            
            if uncertain_pub_or_available or missing_event_years:
                _cond = PhonogramCondition.PhonogramUnknownPublicationExceptions.value
                results['yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'yellow', 'phonogram'),
                })
            else:
                phonogram_extended_protection_lapse = phonogram_initial_protection_lapse
                
                fixed_medium_year = data.get('phonogram_published_fixed_medium_year')
                no_medium_year = data.get('phonogram_available_no_medium_year')


                # Helper to check inclusive range
                def in_initial_window(y: int) -> bool:
                    return phonogram_year <= y <= phonogram_initial_protection_lapse

                # Fixed medium published year → extend to event_year + 70
                # Per Article 3(2) sent. 2 this is the prioritized extension
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    phonogram_extended_protection_lapse = fixed_medium_year + PHONOGRAM_EXTENSION_LONG

                # Available without a medium year → extend to event_year + 70
                # Applies only if there was no publication on a fixed medium
                elif isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    phonogram_extended_protection_lapse = no_medium_year + PHONOGRAM_EXTENSION_LONG

                max_lapse = phonogram_extended_protection_lapse

                if current_year_val > max_lapse:
                    _cond = PhonogramCondition.PhonogramProtectionLapsedArticle3Publication.value
                    results['green'].append({
                        'condition': _cond,
                        'explanation': get_explanation(_cond, 'green', 'phonogram'),
                    })
                else:
                    _cond = PhonogramCondition.PhonogramStillProtectedArticle3Publication.value
                    results['red'].append({
                        'condition': _cond,
                        'explanation': get_explanation(_cond, 'red', 'phonogram'),
                    })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1900 and phonogram_year and not country_eea_phonogram:
        phonogram_initial_protection_lapse = phonogram_year + PHONOGRAM_EXTENSION_SHORT

        # Resolve event years and detect missing years when a 'yes' selection was made
        fixed_medium_year = data.get('phonogram_published_fixed_medium_year')
        no_medium_year = data.get('phonogram_available_no_medium_year')

        fixed_medium_yes = data.get('phonogram_published_fixed_medium') == 'phonogram_published_fixed_medium'
        no_medium_yes = data.get('phonogram_available_no_medium') == 'phonogram_publically_available_no_medium'

        missing_event_years = (
            (fixed_medium_yes and not isinstance(fixed_medium_year, int)) or
            (no_medium_yes and not isinstance(no_medium_year, int))
        )
        mark_used('phonogram_year', 'phonogram_published_fixed_medium_year', 'phonogram_available_no_medium_year')

        # If uncertain publication/availability or missing event years → YELLOW
        if uncertain_pub_or_available or missing_event_years:
            _cond = PhonogramCondition.PhonogramNonEEAUncertain.value
            results['yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'yellow', 'phonogram'),
            })
        else:
            would_be_green = False

            if never_made_publicly_available_phonogram:
                # Same check as EEA: lapsed if current year past initial lapse
                would_be_green = current_year_val > phonogram_initial_protection_lapse
            else:
                # Publication exceptions (use event-based extensions)
                def in_initial_window(y: int) -> bool:
                    return phonogram_year <= y <= phonogram_initial_protection_lapse

                phonogram_extended_protection_lapse = phonogram_initial_protection_lapse
                
                fixed_medium_year = data.get('phonogram_published_fixed_medium_year')
                no_medium_year = data.get('phonogram_available_no_medium_year')


                # Helper to check inclusive range
                def in_initial_window(y: int) -> bool:
                    return phonogram_year <= y <= phonogram_initial_protection_lapse

                # Fixed medium published year → extend to event_year + 70
                # Per Article 3(2) sent. 2 this is the prioritized extension
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    phonogram_extended_protection_lapse = fixed_medium_year + PHONOGRAM_EXTENSION_LONG

                # Available without a medium year → extend to event_year + 70
                # Applies only if there was no publication on a fixed medium
                elif isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    phonogram_extended_protection_lapse = no_medium_year + PHONOGRAM_EXTENSION_LONG

                max_lapse = phonogram_extended_protection_lapse

                would_be_green = current_year_val > max_lapse

            if would_be_green:
                _cond = PhonogramCondition.PhonogramLapsedEvenIfEEA.value
                results['green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'green', 'phonogram'),
                })
            else:
                _cond = PhonogramCondition.PhonogramNonEEAUncertain.value
                results['yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'yellow_uncertain', 'phonogram'),
                })

    # Phonogram-specific rights overrides (mirror performance logic)
    # 1) Current rightholder override (rights green if ours and no prior green)
    mark_used('phonogram_current_rightholder')
    if not results['green'] and data.get('phonogram_current_rightholder') == 'rightholder_us':
        _cond = PhonogramCondition.PhonogramCurrentRightHolderKnown.value
        results['rights_green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'rights_green', 'phonogram'),
        })

    # 2) CC license override for phonogram: logic similar to copyright
    mark_used('phonogram_cc_license')
    cc_choice = data.get('phonogram_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        phonogram_cc_green = ['cc0', 'cc_by']
        phonogram_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in phonogram_cc_green and (results['red'] or results['yellow']):
            _cond = PhonogramCondition.PhonogramAvailableCCLicense.value
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'phonogram'),
            })
        elif cc_choice in phonogram_cc_yellow and (results['red'] or results['yellow']):
            _cond = PhonogramCondition.PhonogramAvailableCCLicense.value
            results['rights_yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_yellow', 'phonogram'),
            })

    # 3) Rights acquisition override for phonogram
    # logic similar to copyright
    mark_used('phonogram_rights_acquired_to_make_available')
    ra_choice = data.get('phonogram_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        phonogram_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        phonogram_ra_yellow = ['limited_license_agreement', 'orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in phonogram_ra_green and (results['red'] or results['yellow']):
            _cond = PhonogramCondition.PhonogramOnlineAvailable.value
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'phonogram'),
            })
        elif ra_choice in phonogram_ra_yellow and (results['red'] or results['yellow']):
            _cond = PhonogramCondition.PhonogramOnlineAvailable.value
            results['rights_yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'rights_yellow', 'phonogram'),
                })

    return results, used_vars





