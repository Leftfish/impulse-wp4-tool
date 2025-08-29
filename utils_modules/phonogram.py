"""
Phonogram rights module.

This module contains logic for calculating phonogram rights status and related intermediate values.
"""

from defaults import ResultsDict

from datetime import datetime
from data.country_codes import is_eea_country


def calculate_intermediate_values_phonograms(data):
    """Calculate intermediate boolean values used in phonogram rights calculations."""
    current_year = datetime.now().year
    
    # Use namespaced producers
    producers = data.get('phonogram_producers', [])
    
    # Producer-related calculations
    all_producers_known = all(producer.get('identity_known', False) for producer in producers)
    all_producers_pseudonymous_or_anonymous = all(not producer.get('identity_known', True) for producer in producers)
    
    # Producer country calculations
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
        'AllProducersKnownPhonograms': all_producers_known,
        'AllProducersPseudonymousOrAnonymousPhonograms': all_producers_pseudonymous_or_anonymous,
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
        results['info'].append({
            'condition': 'CompoundPhonogram',
            'explanation': 'This recording is, in fact, a collection of multiple recording or it is made from various recording. The analysis must be performed for each separately.'
        })

    # Simple override conditions - these take precedence over everything
    if data.get('is_phonogram') == 'not_phonogram':
        mark_used('is_phonogram')
        results['green'].append({
            'condition': 'PublicDomainNotAPhonogram',
            'explanation': 'It is not protected as a phonogram.'
        })
        return results, used_vars
    
    if data.get('phonogram_before_1900') == 'phonogram_made_before_1900':
        mark_used('phonogram_before_1900')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumbPhonogram',
            'explanation': 'Given the time the recording was made, it has passed to the public domain.'
        })
        return results, used_vars
    
    
    
    # Year-based logic when not before 1900
    phonogram_year = data.get('phonogram_year')
    before_1900 = data.get('phonogram_before_1900') == 'phonogram_made_before_1900'
    country_eea_phonogram = intermediate.get('CountryOfOriginEEAPhonograms', False)
    never_made_publicly_available_phonogram = intermediate.get('NeverMadePubliclyAvailablePhonograms', False)
    uncertain_pub_or_available = intermediate.get('UncertainIfPhonogramPublishedOrMadeAvailable', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # 4) Unknown phonogram year (but not before 1900)
    if not before_1900 and not phonogram_year:
        mark_used('phonogram_year')
        results['yellow'].append({
            'condition': 'PhonogramYearUnknown',
            'explanation': 'It is impossible to determine if a recording is still protected.'
        })

    # 5) Known phonogram year logic (EEA focus)
    if not before_1900 and phonogram_year and country_eea_phonogram:
        phonogram_initial_protection_lapse = phonogram_year + 50
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

        # b) Article 3 sec. 2 sent. 1: never made publicly available
        if never_made_publicly_available_phonogram:
            if current_year_val > phonogram_initial_protection_lapse:
                results['green'].append({
                    'condition': 'PhonogramProtectionLapsedArticle3S1',
                    'explanation': 'The recording was protected but the protection has lapsed.'
                })
            else:
                results['red'].append({
                    'condition': 'PhonogramStillProtectedArticle3S1',
                    'explanation': 'The recording is still under protection.'
                })
        if (uncertain_pub_or_available or missing_event_years) and current_year_val <= phonogram_initial_protection_lapse:
            results['red'].append({
                    'condition': 'PhonogramStillProtectedArticle3S1',
                    'explanation': 'The recording is still under protection.'
                })
        else:
            # c) Publication exceptions (sentences 2 and 3)
            mark_used('phonogram_year', 'phonogram_published_fixed_medium_year', 'phonogram_available_no_medium_year')
            
            if uncertain_pub_or_available or missing_event_years:
                results['yellow'].append({
                    'condition': 'PhonogramUnknownPublicationExceptions',
                    'explanation': 'It is impossible to determine if the recording is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.'
                })
            else:
                phonogram_extended_protection_lapses = []
                

                # Helper to check inclusive range
                def in_initial_window(y: int) -> bool:
                    return phonogram_year <= y <= phonogram_initial_protection_lapse

                # Fixed medium published year → extend to event_year + 70
                fixed_medium_year = data.get('phonogram_published_fixed_medium_year')
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    phonogram_extended_protection_lapses.append(fixed_medium_year + 70)

                # Available without a medium year → extend to event_year + 70
                no_medium_year = data.get('phonogram_available_no_medium_year')
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    phonogram_extended_protection_lapses.append(no_medium_year + 70)

                # If no extensions, fall back to initial window end
                if not phonogram_extended_protection_lapses:
                    phonogram_extended_protection_lapses.append(phonogram_initial_protection_lapse)

                max_lapse = max(phonogram_extended_protection_lapses)
                if current_year_val > max_lapse:
                    results['green'].append({
                        'condition': 'PhonogramProtectionLapsedArticle3Publication',
                        'explanation': 'The recording was protected but the protection has lapsed.'
                    })
                else:
                    results['red'].append({
                        'condition': 'PhonogramStillProtectedArticle3Publication',
                        'explanation': 'The recording is still under protection.'
                    })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1900 and phonogram_year and not country_eea_phonogram:
        phonogram_initial_protection_lapse = phonogram_year + 50

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
            results['yellow'].append({
                'condition': 'PhonogramNonEEAUncertain',
                'explanation': 'Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.'
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

                phonogram_extended_protection_lapses = []
                fixed_medium_year = data.get('phonogram_published_fixed_medium_year')
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    phonogram_extended_protection_lapses.append(fixed_medium_year + 70)

                no_medium_year = data.get('phonogram_available_no_medium_year')
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    phonogram_extended_protection_lapses.append(no_medium_year + 70)

                if not phonogram_extended_protection_lapses:
                    phonogram_extended_protection_lapses.append(phonogram_initial_protection_lapse)

                max_lapse = max(phonogram_extended_protection_lapses)
                would_be_green = current_year_val > max_lapse

            if would_be_green:
                results['green'].append({
                    'condition': 'PhonogramLapsedEvenIfEEA',
                    'explanation': 'Country of origin appears to be outside the EEA, but the recording would have lost protection even if the country of origin were in the EEA.'
                })
            else:
                results['yellow'].append({
                    'condition': 'PhonogramNonEEAUncertain',
                    'explanation': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the recording would not have lapsed even under EEA rules, the status is uncertain.'
                })

    # Phonogram-specific rights overrides (mirror performance logic)
    # 1) Current rightholder override (green if ours and no prior green)
    mark_used('phonogram_current_rightholder')
    if not results['green'] and data.get('phonogram_current_rightholder') == 'rightholder_us':
        results['rights_green'].append({
            'condition': 'PhonogramCurrentRightHolderKnown',
            'explanation': 'The recording is protected by phonogram rights, but you are the rightholder.'
        })

    # 2) CC license override for phonogram
    mark_used('phonogram_cc_license')
    cc_choice = data.get('phonogram_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        phonogram_cc_green = ['cc0', 'cc_by']
        phonogram_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in phonogram_cc_green and (results['red'] or results['yellow']):
            results['rights_green'].append({
                'condition': 'PhonogramAvailableCCLicense',
                'explanation': 'While the recording is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in phonogram_cc_yellow and (results['red'] or results['yellow']):
            results['rights_yellow'].append({
                'condition': 'PhonogramAvailableCCLicense',
                'explanation': 'While the recording is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
            })

    # 3) Rights acquisition override for phonogram
    mark_used('phonogram_rights_acquired_to_make_available')
    ra_choice = data.get('phonogram_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        phonogram_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        phonogram_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in phonogram_ra_green and (results['red'] or results['yellow']):
            results['rights_green'].append({
                'condition': 'PhonogramOnlineAvailable',
                'explanation': 'While the recording is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in phonogram_ra_yellow and (results['red'] or results['yellow']):
                results['rights_yellow'].append({
                    'condition': 'PhonogramOnlineAvailable',
                    'explanation': 'While the recording is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
                })    
    return results, used_vars



