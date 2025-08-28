"""
Film fixation rights module.

This module contains logic for calculating film fixation rights status and related intermediate values.
"""

from defaults import ResultsDict
from datetime import datetime
from data.country_codes import is_eea_country


def calculate_intermediate_values_film_fixations(data):
    """Calculate intermediate boolean values used in film fixation rights calculations."""
    current_year = datetime.now().year

    # Use namespaced producers
    producers = data.get('film_fixation_producers', [])
    
    # Producer-related calculations
    all_producers_known = all(producer.get('identity_known', False) for producer in producers)
    all_producers_pseudonymous_or_anonymous = all(not producer.get('identity_known', True) for producer in producers)

    # Producer country calculations
    producer_country_codes = [producer.get('country_of_origin') for producer in producers]
    country_of_origin_eea_film_fixations = any(is_eea_country(code) for code in producer_country_codes if code)
    country_of_origin_unknown_film_fixations = all(code == 'XX' for code in producer_country_codes)

    # Film fixation publication status
    never_made_publicly_available = (
        data.get('film_fixation_published_fixed_medium') == 'film_fixation_not_published_fixed_medium' and
        data.get('film_fixation_available_no_medium') == 'film_fixation_not_publically_available_no_medium'
    )
    
    # Check if any film fixation publication/availability field is uncertain
    uncertain_if_film_fixation_published_or_made_available = (
        data.get('film_fixation_published_fixed_medium') == 'uncertain' or
        data.get('film_fixation_available_no_medium') == 'uncertain'
    )
    
    return {
        'AllProducersKnownFilmFixations': all_producers_known,
        'AllProducersPseudonymousOrAnonymousFilmFixations': all_producers_pseudonymous_or_anonymous,
        'CountryOfOriginEEAFilmFixations': country_of_origin_eea_film_fixations,
        'CountryOfOriginUnknownFilmFixations': country_of_origin_unknown_film_fixations,
        'NeverMadePubliclyAvailableFilmFixations': never_made_publicly_available,
        'UncertainIfFilmFixationPublishedOrMadeAvailable': uncertain_if_film_fixation_published_or_made_available,
        'CURRENT_YEAR': current_year,
    }


def calculate_film_fixation_rights_status(data, intermediate):
    """Calculate film fixation rights status for the original object only."""
    results = ResultsDict()

    # Track variable usage
    used_vars = set()

    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_film_fixation') == 'not_film_fixation':
        mark_used('is_film_fixation')
        results['green'].append({
            'condition': 'PublicDomainNotAFilmFixation',
            'explanation': 'It is not protected as a film fixation.'
        })
        return results, used_vars
    
    if data.get('film_fixation_before_1900') == 'film_fixation_made_before_1900':
        mark_used('film_fixation_before_1900')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumbFilmFixation',
            'explanation': 'Given the time the film fixation was made, it has passed to the public domain.'
        })
        return results, used_vars
    
    # Add compound film fixation info message if needed
    if data.get('is_compound_film_fixation') in ['compound', 'uncertain']:
        mark_used('is_compound_film_fixation')
        results['info'].append({
            'condition': 'CompoundFilmFixation',
            'explanation': 'This film fixation is, in fact, a collection of multiple film fixations or it is made from various film fixations. The analysis must be performed for each separately.'
        })
    
    # Year-based logic when not before 1900
    film_fixation_year = data.get('film_fixation_year')
    before_1900 = data.get('film_fixation_before_1900') == 'film_fixation_made_before_1900'
    country_eea_film_fixation = intermediate.get('CountryOfOriginEEAFilmFixations', False)
    used_vars.update(['film_fixation_producers'])
    never_made_publicly_available_film_fixation = intermediate.get('NeverMadePubliclyAvailableFilmFixations', False)
    uncertain_pub_or_available = intermediate.get('UncertainIfFilmFixationPublishedOrMadeAvailable', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # 4) Unknown film fixation year (but not before 1900)
    if not before_1900 and not film_fixation_year:
        mark_used('film_fixation_year')
        results['yellow'].append({
            'condition': 'FilmFixationYearUnknown',
            'explanation': 'It is impossible to determine if a film fixation is still protected.'
        })

    # 5) Known film fixation year logic (EEA focus)
    if not before_1900 and film_fixation_year and country_eea_film_fixation:
        film_fixation_initial_protection_lapse = film_fixation_year + 50
        mark_used('film_fixation_year', 'film_fixation_producers')
        # Resolve event years and detect missing years when a 'yes' selection was made
        fixed_medium_year = data.get('film_fixation_published_fixed_medium_year')
        no_medium_year = data.get('film_fixation_available_no_medium_year')

        fixed_medium_yes = data.get('film_fixation_published_fixed_medium') == 'film_fixation_published_fixed_medium'
        no_medium_yes = data.get('film_fixation_available_no_medium') == 'film_fixation_publically_available_no_medium'

        missing_event_years = (
            (fixed_medium_yes and not isinstance(fixed_medium_year, int)) or
            (no_medium_yes and not isinstance(no_medium_year, int))
        )

        # b) Article 3 sec. 3 sent. 1: never made publicly available
        if never_made_publicly_available_film_fixation:
            if current_year_val > film_fixation_initial_protection_lapse:
                results['green'].append({
                    'condition': 'FilmFixationProtectionLapsedArticle3S4S1',
                    'explanation': 'The film fixation was protected but the protection has lapsed.'
                })
            else:
                results['red'].append({
                    'condition': 'FilmFixationStillProtectedArticle3S4S1',
                    'explanation': 'The film fixation is still under protection.'
                })
        
        elif (uncertain_pub_or_available or missing_event_years) and current_year_val <= film_fixation_initial_protection_lapse:
            results['red'].append({
                    'condition': 'FilmFixationStillProtectedArticle3S4S1',
                    'explanation': 'The film fixation is still under protection.'
                })
        
        else:
            # c) Publication exceptions (sentences 2 and 3)
            mark_used('film_fixation_year', 'film_fixations_published_fixed_medium_year', 'film_fixations_available_no_medium_year')
            if uncertain_pub_or_available or missing_event_years:
                
                results['yellow'].append({
                    'condition': 'FilmFixationUnknownPublicationExceptions',
                    'explanation': 'It is impossible to determine if the film fixation is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.'
                })
            else:
                film_fixation_extended_protection_lapses = []
                
                # Helper to check inclusive range
                def in_initial_window(y: int) -> bool:
                    return film_fixation_year <= y <= film_fixation_initial_protection_lapse

                # Fixed medium published year → extend to event_year + 50
                fixed_medium_year = data.get('film_fixation_published_fixed_medium_year')
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    film_fixation_extended_protection_lapses.append(fixed_medium_year + 50)

                # Available without a medium year → extend to event_year + 50
                no_medium_year = data.get('film_fixation_available_no_medium_year')
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    film_fixation_extended_protection_lapses.append(no_medium_year + 50)

                # If no extensions, fall back to initial window end
                if not film_fixation_extended_protection_lapses:
                    film_fixation_extended_protection_lapses.append(film_fixation_initial_protection_lapse)

                max_lapse = max(film_fixation_extended_protection_lapses)
                
                
                if current_year_val > max_lapse:
                    results['green'].append({
                        'condition': 'FilmFixationProtectionLapsedArticle3S4S2',
                        'explanation': 'The film fixation was protected but the protection has lapsed.'
                    })
                else:
                    results['red'].append({
                        'condition': 'FilmFixationStillProtectedArticle3S4S2',
                        'explanation': 'The film fixation is still under protection.'
                    })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1900 and film_fixation_year and not country_eea_film_fixation:
        film_fixation_initial_protection_lapse = film_fixation_year + 50

        # Resolve event years and detect missing years when a 'yes' selection was made
        fixed_medium_year = data.get('film_fixation_published_fixed_medium_year')
        no_medium_year = data.get('film_fixation_available_no_medium_year')

        fixed_medium_yes = data.get('film_fixation_published_fixed_medium') == 'film_fixation_published_fixed_medium'
        no_medium_yes = data.get('film_fixation_available_no_medium') == 'film_fixation_publically_available_no_medium'

        missing_event_years = (
            (fixed_medium_yes and not isinstance(fixed_medium_year, int)) or
            (no_medium_yes and not isinstance(no_medium_year, int))
        )
        mark_used('film_fixation_year', 'film_fixations_published_fixed_medium_year', 'film_fixations_available_no_medium_year')
        
        # If uncertain publication/availability or missing event years → YELLOW
        if uncertain_pub_or_available or missing_event_years:
            results['yellow'].append({
                'condition': 'FilmFixationNonEEAUncertain',
                'explanation': 'Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.'
            })
        else:
            would_be_green = False

            if never_made_publicly_available_film_fixation:
                # Same check as EEA: lapsed if current year past initial lapse
                would_be_green = current_year_val > film_fixation_initial_protection_lapse
            else:
                # Publication exceptions (use event-based extensions)
                def in_initial_window(y: int) -> bool:
                    return film_fixation_year <= y <= film_fixation_initial_protection_lapse

                film_fixation_extended_protection_lapses = []
                fixed_medium_year = data.get('film_fixation_published_fixed_medium_year')
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    film_fixation_extended_protection_lapses.append(fixed_medium_year + 50)

                no_medium_year = data.get('film_fixation_available_no_medium_year')
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    film_fixation_extended_protection_lapses.append(no_medium_year + 50)

                if not film_fixation_extended_protection_lapses:
                    film_fixation_extended_protection_lapses.append(film_fixation_initial_protection_lapse)

                max_lapse = max(film_fixation_extended_protection_lapses)
                would_be_green = current_year_val > max_lapse

            
            if would_be_green:
                results['green'].append({
                    'condition': 'FilmFixationLapsedEvenIfEEA',
                    'explanation': 'Country of origin appears to be outside the EEA, but the film fixation would have lost protection even if the country of origin were in the EEA.'
                })
            else:
                results['yellow'].append({
                    'condition': 'FilmFixationNonEEAUncertain',
                    'explanation': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the film fixation would not have lapsed even under EEA rules, the status is uncertain.'
                })

    # Film fixation-specific rights overrides (mirror performance logic)
    # 1) Current rightholder override (green if ours and no prior green)
    mark_used('film_fixation_current_rightholder')
    if not results['green'] and data.get('film_fixation_current_rightholder') == 'rightholder_us':
        results['rights_green'].append({
            'condition': 'FilmFixationCurrentRightHolderKnown',
            'explanation': 'Even if the film fixation is protected by film fixation rights, you are the rightholder.'
        })

    # 2) CC license override for film fixation
    mark_used('film_fixation_cc_license')
    cc_choice = data.get('film_fixation_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        film_fixation_cc_green = ['cc0', 'cc_by']
        film_fixation_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in film_fixation_cc_green and (results['red'] or results['yellow']):
            results['rights_green'].append({
                'condition': 'FilmFixationAvailableCCLicense',
                'explanation': 'Even if the film fixation is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in film_fixation_cc_yellow and (results['red'] or results['yellow']):
                results['rights_yellow'].append({
                    'condition': 'FilmFixationAvailableCCLicense',
                    'explanation': 'Even if the film fixation is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
                })

    # 3) Rights acquisition override for film fixation
    mark_used('film_fixation_rights_acquired_to_make_available')
    ra_choice = data.get('film_fixation_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        film_fixation_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        film_fixation_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in film_fixation_ra_green and (results['red'] or results['yellow']):
            results['rights_green'].append({
                'condition': 'FilmFixationOnlineAvailable',
                'explanation': 'Even if the film fixation is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in film_fixation_ra_yellow and (results['red'] or results['yellow']):
            results['rights_yellow'].append({
                    'condition': 'FilmFixationOnlineAvailable',
                    'explanation': 'Even if the film fixation is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
                })
    
    return results, used_vars
