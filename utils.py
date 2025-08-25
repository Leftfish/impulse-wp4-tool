from datetime import datetime
from data.country_codes import is_eea_country

CURRENT_YEAR = datetime.now().year

def calculate_intermediate_values_copyright(data):
    """Calculate intermediate boolean values used in copyright calculations."""
    current_year = datetime.now().year
    
    # Author-related calculations
    all_authors_known = all(author.get('identity_known', False) for author in data.get('authors', []))
    all_authors_anonymous = all(not author.get('identity_known', True) for author in data.get('authors', []))
    
    # Country calculations
    country_codes = [author.get('country_of_origin') for author in data.get('authors', [])]
    author_country_eea = any(is_eea_country(code) for code in country_codes if code)
    country_of_origin_unknown = all(code == 'XX' for code in country_codes)
    
    # Publication country calculations
    first_pub_country = data.get('country_first_publication')
    simul_pub_countries = data.get('simultaneous_publication_countries', [])
    publication_country_eea = (
        (first_pub_country and is_eea_country(first_pub_country)) or
        any(is_eea_country(code) for code in simul_pub_countries if code)
    )
    
    # Combined EEA status - true if either author or publication is from EEA
    country_of_origin_eea = author_country_eea or publication_country_eea
    
    # Time-based calculations with uncertainty flags
    death_year_unknown = not data.get('author_death_year')
    more_than_70_years_since_death = False
    if data.get('author_death_year'):
        more_than_70_years_since_death = (current_year - data['author_death_year']) > 70
    
    # First available year calculations
    first_available_year = min(
        filter(None, [
            data.get('first_publication_year'),
            data.get('first_available_year')
        ]),
        default=None
    )
    first_available_year_unknown = first_available_year is None
    more_than_70_years_since_first_available = False
    if first_available_year:
        more_than_70_years_since_first_available = (current_year - first_available_year) > 70
    
    # Creation year calculations
    creation_year_unknown = not data.get('creation_year')
    more_than_70_years_since_creation = False
    if data.get('creation_year'):
        more_than_70_years_since_creation = (current_year - data['creation_year']) > 70
    
    # Publication status
    never_made_publicly_available = (
        data.get('physically_published') == 'not_published_on_physical_medium' and
        data.get('otherwise_available') == 'not_made_available_no_medium'
    )
    
    return {
        'AllAuthorsKnown': all_authors_known,
        'AllAuthorsAnonymousOrPseudonymous': all_authors_anonymous,
        'CountryOfOriginEEAAnyReason': country_of_origin_eea,
        'CountryOfOriginUnknown': country_of_origin_unknown,
        'MoreThan70YearsSinceDeath': more_than_70_years_since_death,
        'DeathYearUnknown': death_year_unknown,
        'MoreThan70YearsSinceFirstAvailable': more_than_70_years_since_first_available,
        'FirstAvailableYearUnknown': first_available_year_unknown,
        'MoreThan70YearsSinceCreation': more_than_70_years_since_creation,
        'CreationYearUnknown': creation_year_unknown,
        'NeverMadePubliclyAvailable': never_made_publicly_available,
    }

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
        'CURRENT_YEAR': current_year
    }

def calculate_intermediate_values_broadcasts(data):
    """Calculate intermediate boolean values used in broadcasting organisation rights calculations."""
    current_year = datetime.now().year
    
    # Use namespaced broadcasters
    broadcasters = data.get('broadcasters', [])
    
    # Broadcaster-related calculations
    all_broadcasters_known = all(broadcaster.get('identity_known', False) for broadcaster in broadcasters)
    all_broadcasters_pseudonymous_or_anonymous = all(not broadcaster.get('identity_known', True) for broadcaster in broadcasters)
    
    # Broadcaster country calculations
    broadcaster_country_codes = [broadcaster.get('country_of_origin') for broadcaster in broadcasters]
    country_of_origin_eea_broadcasts = any(is_eea_country(code) for code in broadcaster_country_codes if code)
    country_of_origin_unknown_broadcasts = all(code == 'XX' for code in broadcaster_country_codes)
    
    return {
        'AllBroadcastersKnownBroadcasts': all_broadcasters_known,
        'AllBroadcastersPseudonymousOrAnonymousBroadcasts': all_broadcasters_pseudonymous_or_anonymous,
        'CountryOfOriginEEABroadcasts': country_of_origin_eea_broadcasts,
        'CountryOfOriginUnknownBroadcasts': country_of_origin_unknown_broadcasts,
        'CURRENT_YEAR': current_year
    }

def calculate_all_intermediate_values(data):
    """Calculate and return a unified dictionary of intermediate values
    for both copyright and performance calculations.
    """
    copyright_intermediate = calculate_intermediate_values_copyright(data)
    performance_intermediate = calculate_intermediate_values_performances(data)
    phonogram_intermediate = calculate_intermediate_values_phonograms(data)
    film_fixation_intermediate = calculate_intermediate_values_film_fixations(data)
    broadcasts_intermediate = calculate_intermediate_values_broadcasts(data)

    # Merge with later functions taking precedence on overlapping keys (e.g., CURRENT_YEAR)
    merged = {}
    merged.update(copyright_intermediate)
    merged.update(performance_intermediate)
    merged.update(phonogram_intermediate)
    merged.update(film_fixation_intermediate)
    merged.update(broadcasts_intermediate)
    return merged

def apply_cc_license_status(results, cc_license_choice):
    """Apply status changes based on CC license choice."""
    
    # These choices upgrade status to GREEN if currently RED or YELLOW
    green_upgrade_choices = ['cc0', 'cc_by']
    
    # These choices upgrade status to YELLOW if currently RED
    yellow_upgrade_choices = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
    
    # Skip if not applicable
    if cc_license_choice in ['not_applicable']:
        return results
    
    explanations = {
        'cc0': 'While the work is protected by copyright, it is available under CC0, which allows unrestricted use.',
        'cc_by': 'While the work is protected by copyright, it is available under CC-BY, which allows use with attribution.',
        'cc_by_sa': 'While the work is protected by copyright, it is available under CC-BY-SA. Additional verification may be needed due to the ShareAlike requirement.',
        'cc_by_nc_sa': 'While the work is protected by copyright, it is available under CC-BY-NC-SA. Additional verification may be needed due to the ShareAlike requirement.',
        'cc_by_nd': 'While the work is protected by copyright, it is available under CC-BY-ND. Additional verification may be needed due to the Non-Derivative requirement.',
        'cc_by_nc_nd': 'While the work is protected by copyright, it is available under CC-BY-NC-ND. Additional verification may be needed due to the Non-Derivative requirement.',
        'other_open': 'While the work is protected by copyright, it is available under an open content license. Additional verification of the license terms is needed.'
    }
    
    if cc_license_choice in green_upgrade_choices and (results['red'] or results['yellow']):
        # Clear red and yellow results as we're upgrading to green
        results['red'] = []
        results['yellow'] = []
        results['green'].append({
            'condition': 'ObjectAvailableCCLicense',
            'explanation': explanations[cc_license_choice]
        })
    elif cc_license_choice in yellow_upgrade_choices:
        if results['red']:
            # Clear red results as we're upgrading to yellow
            results['red'] = []
            results['yellow'].append({
                'condition': 'ObjectAvailableCCLicense',
                'explanation': explanations[cc_license_choice]
            })
        elif results['yellow']:
            # Add additional yellow status without clearing existing ones
            results['yellow'].append({
                'condition': 'AdditionalObjectAvailableCCLicense',
                'explanation': explanations[cc_license_choice]
            })
    
    return results

def apply_online_availability_status(results, availability_choice):
    """Apply status changes based on online availability choice."""
    
    # These choices upgrade status to GREEN if currently RED or YELLOW
    green_upgrade_choices = ['rights_assignment', 'license_agreement', 'employee_rights']
    
    # These choices upgrade status to YELLOW if currently RED
    yellow_upgrade_choices = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
    
    # Skip if not applicable or unknown
    if availability_choice in ['not_applicable', 'unknown', 'no']:
        return results
    
    explanations = {
        'rights_assignment': 'While the work is protected by copyright, you have acquired the necessary rights through assignment to make it available online.',
        'license_agreement': 'While the work is protected by copyright, you have acquired the necessary rights through license to make it available online.',
        'employee_rights': 'While the work is protected by copyright, you have acquired the necessary rights as an employer to make it available online.',
        'orphan_works': 'While the work is protected by copyright, you can make it available online based on orphan works provisions, but additional verification may be needed.',
        'out_of_commerce': 'While the work is protected by copyright, you can make it available online based on out-of-commerce works provisions, but additional verification may be needed.',
        'quote_right': 'While the work is protected by copyright, you can make it available online based on the right to quote, but additional verification may be needed.',
        'other_law': 'While the work is protected by copyright, you can make it available online based on other legal provisions, but additional verification may be needed.'
    }
    
    if availability_choice in green_upgrade_choices and (results['red'] or results['yellow']):
        # Clear red and yellow results as we're upgrading to green
        results['red'] = []
        results['yellow'] = []
        results['green'].append({
            'condition': 'ObjectOnlineAvailable',
            'explanation': explanations[availability_choice]
        })
    elif availability_choice in yellow_upgrade_choices:
        if results['red']:
            # Clear red results as we're upgrading to yellow
            results['red'] = []
            results['yellow'].append({
                'condition': 'ObjectOnlineAvailable',
                'explanation': explanations[availability_choice]
            })
        elif results['yellow']:
            # Add additional yellow status without clearing existing ones
            results['yellow'].append({
                'condition': 'AdditionalObjectOnlineAvailable',
                'explanation': explanations[availability_choice]
            })
    
    return results

def apply_digital_repr_rights_availability_status(results, rights_availability_data):
    """Apply status changes based on rights availability choices for each IP right."""
    
    # These choices upgrade status to GREEN if currently RED or YELLOW
    green_upgrade_choices = ['cc0', 'cc_by', 'rights_assignment', 'license_agreement', 'employee_rights']
    
    # These choices upgrade status to YELLOW if currently RED
    yellow_upgrade_choices = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open',
                            'orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
    
    # Skip if not applicable
    if not rights_availability_data:
        return results

    # Map IP rights to their status names
    status_mapping = {
        'copyright': ('DigitalRepresentationCopyrightStatus', 'Digital representation copyright'),
        'audio_recording_rights': ('DigitalRepresentationPhonogramStatus', 'Audio recording rights'),
        'film_fixation_rights': ('DigitalRepresentationFilmFixationStatus', 'Film fixation rights'),
        'performance_rights': ('DigitalRepresentationPerformanceStatus', 'Performance rights'),
        'other_ip_rights': ('DigitalRepresentationOtherIPStatus', 'Other IP rights')
    }

    # Explanation templates for different types of availability
    explanation_templates = {
        'cc0': 'While the {right_type} is protected, it is available under CC0, which allows unrestricted use.',
        'cc_by': 'While the {right_type} is protected, it is available under CC-BY, which allows use with attribution.',
        'cc_by_sa': 'While the {right_type} is protected, it is available under CC-BY-SA. Additional verification may be needed due to the ShareAlike requirement.',
        'cc_by_nc_sa': 'While the {right_type} is protected, it is available under CC-BY-NC-SA. Additional verification may be needed due to the ShareAlike requirement.',
        'cc_by_nd': 'While the {right_type} is protected, it is available under CC-BY-ND. Additional verification may be needed due to the Non-Derivative requirement.',
        'cc_by_nc_nd': 'While the {right_type} is protected, it is available under CC-BY-NC-ND. Additional verification may be needed due to the Non-Derivative requirement.',
        'other_open': 'While the {right_type} is protected, it is available under an open content license. Additional verification of the license terms is needed.',
        'rights_assignment': 'While the {right_type} is protected, the institution has acquired the rights through assignment.',
        'license_agreement': 'While the {right_type} is protected, the institution has acquired the rights through license.',
        'employee_rights': 'While the {right_type} is protected, the institution has acquired the rights as the employer.',
        'orphan_works': 'While the {right_type} is protected, it can be used based on orphan works provisions. Additional verification may be needed.',
        'out_of_commerce': 'While the {right_type} is protected, it can be used based on out-of-commerce works provisions. Additional verification may be needed.',
        'quote_right': 'While the {right_type} is protected, it can be used based on the right to quote. Additional verification may be needed.',
        'other_law': 'While the {right_type} is protected, it can be used based on other legal provisions. Additional verification may be needed.'
    }

    # Process each IP right
    for right_field, (status_name, right_description) in status_mapping.items():
        choice = getattr(rights_availability_data, right_field).data
        
        # Skip if not applicable or no change needed
        if choice in ['not_applicable', 'no', 'unknown']:
            continue

        # Check if we have a matching red or yellow status to upgrade
        has_red = any(r['condition'] == status_name for r in results['red'])
        has_yellow = any(r['condition'] == status_name for r in results['yellow'])

        if choice in green_upgrade_choices and (has_red or has_yellow):
            # Remove existing status
            results['red'] = [r for r in results['red'] if r['condition'] != status_name]
            results['yellow'] = [r for r in results['yellow'] if r['condition'] != status_name]
            
            # Add green status
            results['green'].append({
                'condition': status_name,
                'explanation': explanation_templates[choice].format(right_type=right_description)
            })
        elif choice in yellow_upgrade_choices:
            if has_red:
                # Remove existing red status
                results['red'] = [r for r in results['red'] if r['condition'] != status_name]
                
                # Add yellow status
                results['yellow'].append({
                    'condition': status_name,
                    'explanation': explanation_templates[choice].format(right_type=right_description)
                })
            elif has_yellow:
                # Add additional yellow status without clearing existing ones
                results['yellow'].append({
                    'condition': f'Additional{status_name}',
                    'explanation': explanation_templates[choice].format(right_type=right_description)
                })

    return results

def calculate_digital_representation_status(digital_repr_ip_rights, digital_repr_ip_rights_acquired=None, digital_repr_rights_availability=None):
    """Calculate initial status for digital representation IP rights."""
    results = {
        'green': [],
        'yellow': [],
        'red': []
    }
    
    # Map form fields to status names
    status_mapping = {
        'copyright': ('DigitalRepresentationCopyrightStatus', 'DigitalRepresentationCopyrightAcquired'),
        'audio_recording_rights': ('DigitalRepresentationPhonogramStatus', 'DigitalRepresentationPhonogramAcquired'),
        'film_fixation_rights': ('DigitalRepresentationFilmFixationStatus', 'DigitalRepresentationFilmFixationAcquired'),
        'performance_rights': ('DigitalRepresentationPerformanceStatus', 'DigitalRepresentationPerformanceAcquired'),
        'other_ip_rights': ('DigitalRepresentationOtherIPStatus', 'DigitalRepresentationOtherIPAcquired')
    }
    
    # Map rights to human-readable descriptions
    right_descriptions = {
        'copyright': 'copyright protection',
        'audio_recording_rights': 'phonogram rights protection',
        'film_fixation_rights': 'film fixation rights protection',
        'performance_rights': 'performance rights protection',
        'other_ip_rights': 'other IP rights protection'
    }
    
    all_no = True  # Track if all answers are 'no'
    status_by_right = {}  # Track status for each right for later modification
    individual_greens = []  # Track individual green statuses
    
    # First pass: Calculate initial statuses
    for field, (status_name, _) in status_mapping.items():
        value = getattr(digital_repr_ip_rights, field).data
        if value == 'yes':
            all_no = False
            results['red'].append({
                'condition': status_name,
                'explanation': f'The digital representation is protected by {right_descriptions[field]}.'
            })
            status_by_right[field] = 'red'
        elif value == 'uncertain':
            all_no = False
            results['yellow'].append({
                'condition': status_name,
                'explanation': f'It is uncertain whether the digital representation is protected by {right_descriptions[field]}.'
            })
            status_by_right[field] = 'yellow'
        elif value == 'no':
            individual_greens.append({
                'condition': status_name,
                'explanation': f'The digital representation is not protected by {right_descriptions[field]}.'
            })
            status_by_right[field] = 'green'
    
    # Add individual green statuses only if we have some red or yellow statuses
    if not all_no:
        results['green'].extend(individual_greens)
    
    # Second pass: Apply rights acquisition modifications if available
    if digital_repr_ip_rights_acquired:
        for field, (status_name, acquired_status_name) in status_mapping.items():
            if field not in status_by_right:
                continue
                
            acquisition_value = getattr(digital_repr_ip_rights_acquired, field).data
            
            if acquisition_value in ['right_transfer', 'employer_rights']:
                # Remove existing red/yellow status for this right
                if status_by_right[field] == 'red':
                    results['red'] = [r for r in results['red'] if r['condition'] != status_name]
                elif status_by_right[field] == 'yellow':
                    results['yellow'] = [r for r in results['yellow'] if r['condition'] != status_name]
                
                # Add green status for rights acquisition
                results['green'].append({
                    'condition': acquired_status_name,
                    'explanation': f'While the digital representation is protected by {right_descriptions[field]}, ' + 
                                 ('the institution has acquired the rights through transfer.' if acquisition_value == 'right_transfer'
                                  else 'the institution has acquired the rights as the employer.')
                })
    
    # Add overall no protection status if all answers were no
    if all_no:
        results['green'].append({
            'condition': 'DigitalRepresentationNoProtection',
            'explanation': 'The digital representation is not protected by any IP rights.'
        })

    # Third pass: Apply rights availability modifications if available
    if digital_repr_rights_availability:
        results = apply_digital_repr_rights_availability_status(results, digital_repr_rights_availability)
    
    return results

def calculate_object_copyright_status(data, intermediate):
    """Calculate copyright status for the original object only."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Add informational notices based on work type
    if data.get('is_derivative') == 'derivative':
        mark_used('is_derivative')
        results['info'].append({
            'condition': 'DerivativeWork',
            'explanation': 'This is a derivative work. This means that you also need to verify the status of the original work.'
        })
    elif data.get('is_derivative') == 'uncertain':
        mark_used('is_derivative')
        results['info'].append({
            'condition': 'DerivativeWork',
            'explanation': 'This may be a derivative work. This means that you also need to verify the status of the original work.'
        })
    
    if data.get('is_compound') == 'compound':
        mark_used('is_compound')
        results['info'].append({
            'condition': 'CompoundWork',
            'explanation': 'This is a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.'
        })
    elif data.get('is_compound') == 'uncertain':
        mark_used('is_compound')
        results['info'].append({
            'condition': 'CompoundWork',
            'explanation': 'This may be a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.'
        })
    
    if data.get('is_photography') in ['photography_with_notice', 'photography_without_notice']:
        mark_used('is_photography')
        results['info'].append({
            'condition': 'Photography',
            'explanation': 'For photographies, some countries used to assume that without a copyright notice made on a copy, a photography is not protected by copyright. This practice differed between countries, so we proceed on the assumption that it does not affect our assesment.'
        })
    
    if data.get('territory_status_changed'):
        mark_used('territory_status_changed')
        results['info'].append({
            'condition': 'TerritoryStatusChanged',
            'explanation': 'Problems with international succession were encountered.'
        })
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_copyright_work') == 'not_work':
        mark_used('is_copyright_work')
        results['green'].append({
            'condition': 'PublicDomainNotAWork',
            'explanation': 'The object is not protected by copyright because it is not a work.'
        })
        return results, used_vars
    
    if data.get('created_before_1850') == 'made_before_1850':
        mark_used('created_before_1850')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumb',
            'explanation': 'The object is not protected by copyright because it was created before 1850.'
        })
        return results, used_vars
    
    # Special case: if both conditions are uncertain but it's from before 1850, it's GREEN
    if (data.get('is_copyright_work') == 'uncertain' and 
        data.get('created_before_1850') == 'made_before_1850'):
        mark_used('is_copyright_work', 'created_before_1850')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumb',
            'explanation': 'Even though it is uncertain whether this object qualifies as a work, it was created before 1850 and is therefore in the public domain.'
        })
        return results, used_vars
    
    # Handle other uncertainty cases
    if data.get('is_copyright_work') == 'uncertain':
        mark_used('is_copyright_work')
        results['yellow'].append({
            'condition': 'UncertainIfWork',
            'explanation': 'It is uncertain whether this object qualifies as a work protected by copyright.'
        })
        return results, used_vars
    
    
    # Store all possible results first
    potential_results = {
        'green': [],
        'yellow': [],
        'red': []
    }
    
    # Check uncertain conditions that lead to YELLOW status
    if not intermediate['AllAuthorsAnonymousOrPseudonymous'] and data.get('author_alive') == 'uncertain':
        mark_used('author_alive')
        potential_results['yellow'].append({
            'condition': 'AuthorAlive',
            'explanation': 'It is uncertain if the author is alive so it is impossible to verify if enough time passed since the author\'s death.'
        })
    
    if data.get('original_rightholder') == 'legal_person':
        mark_used('original_rightholder')
        potential_results['yellow'].append({
            'condition': 'OriginalRightholder',
            'explanation': 'The author was not the first rightholder, e.g. the rights belonged to a publisher from the moment the work was created. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
        })
    
    if data.get('original_rightholder') == 'uncertain':
        mark_used('original_rightholder')
        potential_results['yellow'].append({
            'condition': 'OriginalRightholder',
            'explanation': 'It is uncertain who the first rightholder was. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
        })
    
    # Check copyright lapse conditions
    
    # Article 1 Section 1-2 (EEA countries)
    if (intermediate['AllAuthorsKnown'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath']):
        mark_used('authors')  # Mark authors data as used
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsKnown'] and intermediate['CountryOfOriginEEAAnyReason']:
        mark_used('author_death_year')
        if intermediate['DeathYearUnknown']:
            potential_results['yellow'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2',
                'explanation': 'Unable to determine if copyright has lapsed because the author\'s death year is unknown.'
            })
        else:
            mark_used('author_death_year')
            potential_results['red'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2',
                'explanation': 'The object is still under copyright because fewer than 70 years passed since the author\'s death.'
            })
    
    # Article 1 Section 1-2 Rule of Shorter Term (non-EEA countries)
    if (intermediate['AllAuthorsKnown'] and 
        not intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsKnown'] and not intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })
    
    # Article 1 Section 3 (EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsAnonymousOrPseudonymous'] and intermediate['CountryOfOriginEEAAnyReason']:
        if intermediate['FirstAvailableYearUnknown']:
            potential_results['yellow'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3',
                'explanation': 'Unable to determine if copyright has lapsed because the year when the work was first made available is unknown.'
            })
        else:
            potential_results['red'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3',
                'explanation': 'The object is still under copyright because fewer than 70 years passed since it was first made available.'
            })
    
    # Article 1 Section 3 Rule of Shorter Term (non-EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        not intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsAnonymousOrPseudonymous'] and not intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })
    
    # Article 1 Section 6 (EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['NeverMadePubliclyAvailable'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceCreation']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
          intermediate['NeverMadePubliclyAvailable'] and 
          intermediate['CountryOfOriginEEAAnyReason']):
        if intermediate['CreationYearUnknown']:
            potential_results['yellow'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6',
                'explanation': 'Unable to determine if copyright has lapsed because the creation year is unknown.'
            })
        else:
            potential_results['red'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6',
                'explanation': 'The object is still under copyright because fewer than 70 years passed since its creation.'
            })
    
    # Article 1 Section 6 Rule of Shorter Term (non-EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['NeverMadePubliclyAvailable'] and 
        (not intermediate['CountryOfOriginEEAAnyReason'] or intermediate['CountryOfOriginUnknown']) and 
        intermediate['MoreThan70YearsSinceCreation']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
          intermediate['NeverMadePubliclyAvailable'] and 
          (not intermediate['CountryOfOriginEEAAnyReason'] or intermediate['CountryOfOriginUnknown'])):
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })

    # Article 1 Section 6 - Late Publication Case (EEA countries)
    # For anonymous works that were not made available within 70 years of creation
    # but were published later (after entering public domain)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceCreation'] and
        data.get('first_publication_year') and
        data.get('creation_year') and
        (data['first_publication_year'] - data['creation_year']) > 70 and
        not intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication',
            'explanation': 'The object used to be protected by copyright, but it has lapsed. The work was not made available within 70 years of creation, so it entered public domain 70 years after creation.'
        })
    elif (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
          intermediate['CountryOfOriginEEAAnyReason'] and
          data.get('first_publication_year') and
          data.get('creation_year') and
          (data['first_publication_year'] - data['creation_year']) > 70 and
          not intermediate['MoreThan70YearsSinceFirstAvailable']):
        if intermediate['CreationYearUnknown']:
            potential_results['yellow'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication',
                'explanation': 'Unable to determine if copyright has lapsed because the creation year is unknown.'
            })
        else:
            potential_results['red'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication',
                'explanation': 'The object is still under copyright because fewer than 70 years passed since its creation.'
            })

    # Article 1 Section 6 - Late Publication Case (non-EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        (not intermediate['CountryOfOriginEEAAnyReason'] or intermediate['CountryOfOriginUnknown']) and 
        intermediate['MoreThan70YearsSinceCreation'] and
        data.get('first_publication_year') and
        data.get('creation_year') and
        (data['first_publication_year'] - data['creation_year']) > 70):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed. The work was not made available within 70 years of creation, so it entered public domain 70 years after creation.'
        })
    elif (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
          (not intermediate['CountryOfOriginEEAAnyReason'] or intermediate['CountryOfOriginUnknown']) and
          data.get('first_publication_year') and
          data.get('creation_year') and
          (data['first_publication_year'] - data['creation_year']) > 70):
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })

    # Article 1 Section 1-2 Plus Section 3
    if (intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath'] and 
        intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['CountryOfOriginEEAAnyReason']:
        if intermediate['DeathYearUnknown'] or intermediate['FirstAvailableYearUnknown']:
            potential_results['yellow'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3',
                'explanation': 'Unable to determine if copyright has lapsed because either the author\'s death year or the first availability year is unknown.'
            })
        else:
            potential_results['red'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3',
                'explanation': 'The object is still under copyright because fewer than 70 years passed since either the author\'s death or first availability.'
            })

    # Article 1 Section 1-2 Plus Section 6
    if (intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath'] and 
        intermediate['MoreThan70YearsSinceCreation'] and 
        intermediate['NeverMadePubliclyAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['CountryOfOriginEEAAnyReason'] and intermediate['NeverMadePubliclyAvailable']:
        if intermediate['DeathYearUnknown'] or intermediate['CreationYearUnknown']:
            potential_results['yellow'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6',
                'explanation': 'Unable to determine if copyright has lapsed because either the author\'s death year or creation year is unknown.'
            })
        else:
            potential_results['red'].append({
                'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6',
                'explanation': 'The object is still under copyright because fewer than 70 years passed since either the author\'s death or creation.'
            })

    # Check if author is alive - this adds to RED status
    if not intermediate['AllAuthorsAnonymousOrPseudonymous'] and data.get('author_alive') == 'author_alive':
        potential_results['red'].append({
            'condition': 'AuthorAlive',
            'explanation': 'Object under copyright. At least one co-author is still alive.'
        })
    
    # Apply results based on priority
    if potential_results['green']:
        results['green'].extend(potential_results['green'])
    elif data.get('current_rightholder') == 'rightholder_us':
        mark_used('current_rightholder')
        results['green'].append({
            'condition': 'CurrentRightHolderKnown',
            'explanation': 'The object is protected by copyright, but you are the rightholder.'
        })
    else:
        results['green'].extend(potential_results['green'])
        results['yellow'].extend(potential_results['yellow'])
        results['red'].extend(potential_results['red'])


    
    # Apply CC license status after initial calculations but before online availability
    mark_used('object_cc_license')
    results = apply_cc_license_status(
        results,
        data.get('object_cc_license')
    )
    
    # Apply online availability status after CC license status
    mark_used('object_copyright_rights_acquired_to_make_available')
    results = apply_online_availability_status(
        results,
        data.get('object_copyright_rights_acquired_to_make_available')
    )
    
    return results, used_vars

def calculate_performance_rights_status(data, intermediate):
    """Calculate performance rights status for the original object only."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_performance') == 'not_performance':
        mark_used('is_performance')
        results['green'].append({
            'condition': 'PublicDomainNotAPerformance',
            'explanation': 'The object does not include a performance.'
        })
        return results, used_vars
    
    if data.get('performance_before_1900') == 'performance_made_before_1900':
        mark_used('performance_before_1900')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumbPerformance',
            'explanation': 'The performance was made before 1900.'
        })
        return results, used_vars
    
    # Add compound performance info message if needed
    if data.get('is_compound_performance') in ['compound', 'uncertain']:
        mark_used('is_compound_performance')
        results['info'].append({
            'condition': 'CompoundPerformance',
            'explanation': 'This is a compound performance. You need to verify the status of each performance separately.'
        })
    
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
        results['yellow'].append({
            'condition': 'PerformanceYearUnknown',
            'explanation': 'It is impossible to determine if a performance is still protected.'
        })

    # 5) Known performance year logic (EEA focus)
    if not before_1900 and performance_year and country_eea_perf:
        initial_lapse_year = performance_year + 50

        # b) Article 3 s.1 sentence 1: never made publicly available
        if never_made_publicly_available_perf:
            if current_year_val > initial_lapse_year:
                results['green'].append({
                    'condition': 'PerformanceProtectionLapsedArticle3S1',
                    'explanation': 'The performance was protected but the protection has lapsed.'
                })
            else:
                results['red'].append({
                    'condition': 'PerformanceStillProtectedArticle3S1',
                    'explanation': 'The performance is still under protection.'
                })
        else:
            # c) Publication exceptions (sentences 2 and 3)
            if uncertain_pub_or_available or missing_event_years:
                results['yellow'].append({
                    'condition': 'PerformanceUnknownPublicationExceptions',
                    'explanation': 'It is impossible to determine if the performance is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.'
                })
            else:
                extended_lapses = []

                # Helper to check inclusive range
                def in_initial_window(y: int) -> bool:
                    return performance_year <= y <= initial_lapse_year

                # Phonogram published/made available year → extend to event_year + 70
                if isinstance(phonogram_year, int) and in_initial_window(phonogram_year):
                    extended_lapses.append(phonogram_year + 70)

                # Available without a medium year → extend to event_year + 50
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    extended_lapses.append(no_medium_year + 50)

                # Available from fixed not phonogram year → extend to event_year + 50
                if isinstance(fixed_not_phonogram_year, int) and in_initial_window(fixed_not_phonogram_year):
                    extended_lapses.append(fixed_not_phonogram_year + 50)

                # If no extensions, fall back to initial window end
                if not extended_lapses:
                    extended_lapses.append(initial_lapse_year)

                max_lapse = max(extended_lapses)
                if current_year_val > max_lapse:
                    results['green'].append({
                        'condition': 'PerformanceProtectionLapsedArticle3Publication',
                        'explanation': 'The performance was protected but the protection has lapsed.'
                    })
                else:
                    results['red'].append({
                        'condition': 'PerformanceStillProtectedArticle3Publication',
                        'explanation': 'The performance is still under protection.'
                    })

    # Non-EEA branch: do not change EEA logic; mirror it to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1900 and performance_year and not country_eea_perf:
        initial_lapse_year = performance_year + 50

        # If uncertain publication/availability or missing event years → YELLOW
        if uncertain_pub_or_available or missing_event_years:
            results['yellow'].append({
                'condition': 'PerformanceNonEEAUncertain',
                'explanation': 'Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.'
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
                    extended_lapses.append(phonogram_year + 70)

                no_medium_year = data.get('performance_available_no_medium_year')
                if isinstance(no_medium_year, int) and in_initial_window(no_medium_year):
                    extended_lapses.append(no_medium_year + 50)

                fixed_not_phonogram_year = data.get('performance_fixed_not_phonogram_available_year')
                if isinstance(fixed_not_phonogram_year, int) and in_initial_window(fixed_not_phonogram_year):
                    extended_lapses.append(fixed_not_phonogram_year + 50)

                if not extended_lapses:
                    extended_lapses.append(initial_lapse_year)

                max_lapse = max(extended_lapses)
                would_be_green = current_year_val > max_lapse

            if would_be_green:
                results['green'].append({
                    'condition': 'PerformanceLapsedEvenIfEEA',
                    'explanation': 'Country of origin appears to be outside the EEA, but the performance would have lost protection even if the country of origin were in the EEA.'
                })
            else:
                results['yellow'].append({
                    'condition': 'PerformanceNonEEAUncertain',
                    'explanation': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the performance would not have lapsed even under EEA rules, the status is uncertain.'
                })

    # Performance-specific rights overrides (mirror copyright logic)
    # 1) Current rightholder override (green if ours and no prior green)
    mark_used('performance_current_rightholder')
    if not results['green'] and data.get('performance_current_rightholder') == 'rightholder_us':
        results['green'].append({
            'condition': 'PerformanceCurrentRightHolderKnown',
            'explanation': 'The performance is protected by performance rights, but you are the rightholder.'
        })

    # 2) CC license override for performance
    mark_used('performance_cc_license')
    cc_choice = data.get('performance_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        perf_cc_green = ['cc0', 'cc_by']
        perf_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in perf_cc_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'PerformanceAvailableCCLicense',
                'explanation': 'While the performance is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in perf_cc_yellow:
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'PerformanceAvailableCCLicense',
                    'explanation': 'While the performance is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalPerformanceAvailableCCLicense',
                    'explanation': 'The performance may be available under an open content license. Additional verification may be needed.'
                })

    # 3) Rights acquisition override for performance
    mark_used('performance_rights_acquired_to_make_available')
    ra_choice = data.get('performance_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        perf_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        perf_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in perf_ra_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'PerformanceOnlineAvailable',
                'explanation': 'While the performance is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in perf_ra_yellow:
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'PerformanceOnlineAvailable',
                    'explanation': 'While the performance is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalPerformanceOnlineAvailable',
                    'explanation': 'There may be legal provisions allowing online availability of the performance. Additional verification may be needed.'
                })
    
    return results, used_vars

def calculate_phonogram_rights_status(data, intermediate):
    """Calculate phonogram rights status for the original object only."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
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
    
    # Add compound phonogram info message if needed
    if data.get('is_compound_phonogram') in ['compound', 'uncertain']:
        mark_used('is_compound_phonogram')
        results['info'].append({
            'condition': 'CompoundPhonogram',
            'explanation': 'This recording is, in fact, a collection of multiple recording or it is made from various recording. The analysis must be performed for each separately.'
        })
    
    # Year-based logic when not before 1900
    phonogram_year = data.get('phonogram_year')
    before_1900 = data.get('phonogram_before_1900') == 'phonogram_made_before_1900'
    country_eea_phonogram = intermediate.get('CountryOfOriginEEAPhonograms', False)
    never_made_publicly_available_phonogram = intermediate.get('NeverMadePubliclyAvailablePhonograms', False)
    uncertain_pub_or_available = intermediate.get('UncertainIfPhonogramPublishedOrMadeAvailable', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # 4) Unknown phonogram year (but not before 1900)
    if not before_1900 and not phonogram_year:
        results['yellow'].append({
            'condition': 'PhonogramYearUnknown',
            'explanation': 'It is impossible to determine if a recording is still protected.'
        })
        return results, used_vars

    # 5) Known phonogram year logic (EEA focus)
    if not before_1900 and phonogram_year and country_eea_phonogram:
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
        else:
            # c) Publication exceptions (sentences 2 and 3)
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
        results['green'].append({
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
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'PhonogramAvailableCCLicense',
                'explanation': 'While the recording is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in phonogram_cc_yellow:
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'PhonogramAvailableCCLicense',
                    'explanation': 'While the recording is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalPhonogramAvailableCCLicense',
                    'explanation': 'The recording may be available under an open content license. Additional verification may be needed.'
                })

    # 3) Rights acquisition override for phonogram
    mark_used('phonogram_rights_acquired_to_make_available')
    ra_choice = data.get('phonogram_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        phonogram_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        phonogram_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in phonogram_ra_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'PhonogramOnlineAvailable',
                'explanation': 'While the recording is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in phonogram_ra_yellow:
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'PhonogramOnlineAvailable',
                    'explanation': 'While the recording is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalPhonogramOnlineAvailable',
                    'explanation': 'There may be legal provisions allowing online availability of the recording. Additional verification may be needed.'
                })
    
    return results, used_vars

def calculate_film_fixation_rights_status(data, intermediate):
    """Calculate film fixation rights status based on Article 3 sec. 4."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
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
    never_made_publicly_available_film_fixation = intermediate.get('NeverMadePubliclyAvailableFilmFixations', False)
    uncertain_pub_or_available = intermediate.get('UncertainIfFilmFixationPublishedOrMadeAvailable', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # 4) Unknown film fixation year (but not before 1900)
    if not before_1900 and not film_fixation_year:
        results['yellow'].append({
            'condition': 'FilmFixationYearUnknown',
            'explanation': 'It is impossible to determine if a film fixation is still protected.'
        })
        return results, used_vars

    # 5) Known film fixation year logic (EEA focus)
    if not before_1900 and film_fixation_year and country_eea_film_fixation:
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

        # b) Article 3 sec. 4 sent. 1: never made publicly available
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
        else:
            # c) Publication exceptions (sentences 2 and 3)
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

                # Fixed medium published year → extend to event_year + 50 (Article 3 sec. 4 sent. 2)
                fixed_medium_year = data.get('film_fixation_published_fixed_medium_year')
                if isinstance(fixed_medium_year, int) and in_initial_window(fixed_medium_year):
                    film_fixation_extended_protection_lapses.append(fixed_medium_year + 50)

                # Available without a medium year → extend to event_year + 50 (Article 3 sec. 4 sent. 2)
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
                # Publication exceptions (use event-based extensions with 50 years)
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

    # Film fixation-specific rights overrides (mirror phonogram logic)
    # 1) Current rightholder override (green if ours and no prior green)
    mark_used('film_fixation_current_rightholder')
    if not results['green'] and data.get('film_fixation_current_rightholder') == 'rightholder_us':
        results['green'].append({
            'condition': 'FilmFixationCurrentRightHolderKnown',
            'explanation': 'The film fixation is protected by film fixation rights, but you are the rightholder.'
        })

    # 2) CC license override for film fixation
    mark_used('film_fixation_cc_license')
    cc_choice = data.get('film_fixation_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        film_fixation_cc_green = ['cc0', 'cc_by']
        film_fixation_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in film_fixation_cc_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'FilmFixationAvailableCCLicense',
                'explanation': 'While the film fixation is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in film_fixation_cc_yellow:
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'FilmFixationAvailableCCLicense',
                    'explanation': 'While the film fixation is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalFilmFixationAvailableCCLicense',
                    'explanation': 'The film fixation may be available under an open content license. Additional verification may be needed.'
                })

    # 3) Rights acquisition override for film fixation
    mark_used('film_fixation_rights_acquired_to_make_available')
    ra_choice = data.get('film_fixation_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        film_fixation_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        film_fixation_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in film_fixation_ra_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'FilmFixationOnlineAvailable',
                'explanation': 'While the film fixation is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in film_fixation_ra_yellow:
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'FilmFixationOnlineAvailable',
                    'explanation': 'While the film fixation is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalFilmFixationOnlineAvailable',
                    'explanation': 'There may be legal provisions allowing online availability of the film fixation. Additional verification may be needed.'
                })
    
    return results, used_vars

def calculate_first_edition_protection_status(data, intermediate):
    """Calculate first edition protection status for any public domain work."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Only check if we have a first publication year
    if not data.get('first_publication_year'):
        return results
    
    first_pub_year = data['first_publication_year']
    current_year = datetime.now().year
    
    # Check if first publication was within last 25 years
    if (current_year - first_pub_year) <= 25:
        
        # Determine if this is a first edition of a public domain work
        is_first_edition_candidate = False
        public_domain_reason = ""
        
        # Case 1: Pre-1850 work
        if data.get('created_before_1850') == 'made_before_1850':
            is_first_edition_candidate = True
            public_domain_reason = "created before 1850"
            
        # Case 2: Anonymous work that entered public domain before publication
        elif (data.get('is_copyright_work') == 'work' and 
              intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
              data.get('creation_year') and
              first_pub_year > (data['creation_year'] + 70)):
            is_first_edition_candidate = True
            public_domain_reason = f"anonymous work entered public domain in {data['creation_year'] + 70}"
            
        # Case 3: Known author who died more than 70 years before publication
        elif (data.get('author_death_year') and 
              first_pub_year > (data['author_death_year'] + 70)):
            is_first_edition_candidate = True
            public_domain_reason = f"author died in {data['author_death_year']}, entered public domain in {data['author_death_year'] + 70}"
        
        # Apply first edition protection if candidate
        if is_first_edition_candidate:
            results['yellow'].append({
                'condition': 'FirstEditionProtection',
                'explanation': f'First edition protection applies for 25 years from first publication ({first_pub_year}). The work is in public domain ({public_domain_reason}), but the first edition may be protected until {first_pub_year + 25}.'
            })
    
    return results

def calculate_results(data, intermediate):
    """Calculate final copyright status results based on intermediate values."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': [],
        'object_name': data.get('object_name'),
        'institution_name': data.get('institution_name'),
        'performance_status': None,  # Will store performance rights status
        'phonogram_status': None,  # Will store phonogram rights status
        'film_fixation_status': None,  # Will store film fixation rights status
        'broadcast_status': None,  # Will store broadcasting organisation rights status
        'digital_repr_status': None,  # Will store digital representation status
        'debug_info': {}  # Add debug info tracking
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Expect callers to pass unified intermediate values
    merged_intermediate = intermediate or {}

    # Calculate object copyright status
    object_results, object_used_vars = calculate_object_copyright_status(data, merged_intermediate)
    used_vars.update(object_used_vars)
    
    # Calculate performance rights status
    performance_results, performance_used_vars = calculate_performance_rights_status(data, merged_intermediate)
    used_vars.update(performance_used_vars)
    
    # Calculate phonogram rights status
    phonogram_results, phonogram_used_vars = calculate_phonogram_rights_status(data, merged_intermediate)
    used_vars.update(phonogram_used_vars)
    
    # Calculate film fixation rights status
    film_fixation_results, film_fixation_used_vars = calculate_film_fixation_rights_status(data, merged_intermediate)
    used_vars.update(film_fixation_used_vars)
    
    # Calculate broadcasting organisation rights status
    broadcast_results, broadcast_used_vars = calculate_broadcast_rights_status(data, merged_intermediate)
    used_vars.update(broadcast_used_vars)
    
    # Calculate additional object classification status (NEW)
    additional_classification_results, additional_classification_used_vars = calculate_additional_object_classification_status(data, merged_intermediate)
    used_vars.update(additional_classification_used_vars)
    
    # Calculate first edition protection status (NEW)
    first_edition_results = calculate_first_edition_protection_status(data, merged_intermediate)
    
    # Copy object results to main results
    results['green'].extend(object_results['green'])
    results['yellow'].extend(object_results['yellow'])
    results['red'].extend(object_results['red'])
    results['info'].extend(object_results['info'])
    
    # Add additional classification results to main results
    results['green'].extend(additional_classification_results['green'])
    results['yellow'].extend(additional_classification_results['yellow'])
    results['red'].extend(additional_classification_results['red'])
    results['info'].extend(additional_classification_results['info'])
    
    # Store additional classification results separately
    results['additional_classification_status'] = {
        'green': additional_classification_results['green'],
        'yellow': additional_classification_results['yellow'],
        'red': additional_classification_results['red'],
        'info': additional_classification_results['info']
    }
    
    # Store first edition results separately
    results['first_edition_status'] = {
        'green': first_edition_results['green'],
        'yellow': first_edition_results['yellow'],
        'red': first_edition_results['red'],
        'info': first_edition_results['info']
    }
    
    # Store performance results separately
    results['performance_status'] = {
        'green': performance_results['green'],
        'yellow': performance_results['yellow'],
        'red': performance_results['red'],
        'info': performance_results['info']
    }
    
    # Store phonogram results separately
    results['phonogram_status'] = {
        'green': phonogram_results['green'],
        'yellow': phonogram_results['yellow'],
        'red': phonogram_results['red'],
        'info': phonogram_results['info']
    }
    
    # Store film fixation results separately
    results['film_fixation_status'] = {
        'green': film_fixation_results['green'],
        'yellow': film_fixation_results['yellow'],
        'red': film_fixation_results['red'],
        'info': film_fixation_results['info']
    }
    
    # Store broadcasting organisation results separately
    results['broadcast_status'] = {
        'green': broadcast_results['green'],
        'yellow': broadcast_results['yellow'],
        'red': broadcast_results['red'],
        'info': broadcast_results['info']
    }
    
    # Calculate digital representation status
    if 'digital_repr_ip_rights' in data:
        mark_used('digital_repr_ip_rights')
        mark_used('digital_repr_ip_rights_acquired')
        mark_used('digital_repr_rights_availability')  # Mark this as used too
        
        # Create a mock object that matches the structure expected by calculate_digital_representation_status
        class MockField:
            def __init__(self, data):
                self.data = data

        class MockDigitalReprIPRights:
            def __init__(self, rights_dict):
                self.copyright = MockField(rights_dict.get('copyright', 'not_applicable'))
                self.audio_recording_rights = MockField(rights_dict.get('audio_recording_rights', 'not_applicable'))
                self.film_fixation_rights = MockField(rights_dict.get('film_fixation_rights', 'not_applicable'))
                self.performance_rights = MockField(rights_dict.get('performance_rights', 'not_applicable'))
                self.other_ip_rights = MockField(rights_dict.get('other_ip_rights', 'not_applicable'))

        mock_rights = MockDigitalReprIPRights(data['digital_repr_ip_rights'])
        
        # Create mock objects for both acquired rights and availability
        mock_rights_acquired = None
        if 'digital_repr_ip_rights_acquired' in data:
            mock_rights_acquired = MockDigitalReprIPRights(data['digital_repr_ip_rights_acquired'])
            
        mock_rights_availability = None
        if 'digital_repr_rights_availability' in data:
            mock_rights_availability = MockDigitalReprIPRights(data['digital_repr_rights_availability'])
        
        results['digital_repr_status'] = calculate_digital_representation_status(
            mock_rights,
            mock_rights_acquired,
            mock_rights_availability
        )
    
    # Prepare debug info
    basic_info_fields = ['object_name', 'institution_name', 'object_url', 'digital_repr_nature']
    results['debug_info'] = {
        'basic_information': {k: data[k] for k in basic_info_fields if k in data},
        'input_data': {k: v for k, v in data.items() if k not in basic_info_fields},
        'used_variables': list(used_vars),
        'unused_variables': [k for k in data.keys() if k not in used_vars]
    }
    
    return results

def generate_markdown_report(results):
    """Generate a markdown report from the results."""
    
    md_content = ["# Report\n"]
    
    # Add object and institution information
    object_name = results.get('object_name') or "unknown"
    institution_name = results.get('institution_name') or "unknown"
    md_content.extend([
        f"\n**Object:** {object_name}",
        f"\n**Institution:** {institution_name}\n"
    ])
    
    # Add explanation of priority order
    md_content.append("\n> Note: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n")
    
    # Add copyright status section
    md_content.append("\n## Copyright status of the object\n")
    
    if results['red']:
        md_content.append("\n### \u274c Red status. There are legal obstacles.\n")
        for result in results['red']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['yellow']:
        md_content.append("\n### \u26a0\ufe0f Yellow status. The tool is unable to determine the status.\n")
        for result in results['yellow']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['green']:
        md_content.append("\n### \u2705 Green status. No issues detected.\n")
        for result in results['green']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['info']:
        md_content.append("\n### \ud83d\udcdd Informational Messages\n")
        for result in results['info']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

    # Add additional object classification section (NEW)
    if results.get('additional_classification_status'):
        md_content.append("\n## Additional Object Classification Status\n")
        additional_classification = results['additional_classification_status']
        if additional_classification['red']:
            md_content.append("\n### \u274c Red status. There are legal obstacles.\n")
            for result in additional_classification['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if additional_classification['yellow']:
            md_content.append("\n### \u26a0\ufe0f Yellow status. The tool is unable to determine the status.\n")
            for result in additional_classification['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if additional_classification['green']:
            md_content.append("\n### \u2705 Green status. No issues detected.\n")
            for result in additional_classification['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if additional_classification['info']:
            md_content.append("\n### \ud83d\udcdd Informational Messages\n")
            for result in additional_classification['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

    # Add first edition protection section (NEW)
    if results.get('first_edition_status'):
        md_content.append("\n## First edition protection / posthumous edition status\n")
        first_edition = results['first_edition_status']
        if first_edition['red']:
            md_content.append("\n### \u274c Red status. There are legal obstacles.\n")
            for result in first_edition['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['yellow']:
            md_content.append("\n### \u26a0\ufe0f Yellow status. The tool is unable to determine the status.\n")
            for result in first_edition['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['green']:
            md_content.append("\n### \u2705 Green status. No issues detected.\n")
            for result in first_edition['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['info']:
            md_content.append("\n### \ud83d\udcdd Informational Messages\n")
            for result in first_edition['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add performance rights section
    if results.get('performance_status'):
        md_content.append("\n## Performance rights status of the object\n")
        
        performance_status = results['performance_status']
        
        if performance_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in performance_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if performance_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in performance_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if performance_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in performance_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if performance_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in performance_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        md_content.append("\n## Phonogram rights status of the object\n")
        
        phonogram_status = results['phonogram_status']
        
        if phonogram_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in phonogram_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if phonogram_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in phonogram_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if phonogram_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in phonogram_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if phonogram_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in phonogram_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add film fixation rights section
    if results.get('film_fixation_status'):
        md_content.append("\n## Film fixation rights status of the object\n")
        
        film_fixation_status = results['film_fixation_status']
        
        if film_fixation_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in film_fixation_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if film_fixation_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in film_fixation_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if film_fixation_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in film_fixation_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if film_fixation_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in film_fixation_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        md_content.append("\n## Broadcasting organisation rights status of the object\n")
        
        broadcast_status = results['broadcast_status']
        
        if broadcast_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in broadcast_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if broadcast_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in broadcast_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if broadcast_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in broadcast_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if broadcast_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in broadcast_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add digital representation status section
    md_content.append("\n## IP status of the digital representation of the object\n")
    
    if results.get('digital_repr_status'):
        digital_status = results['digital_repr_status']
        
        if digital_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in digital_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if digital_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in digital_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if digital_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in digital_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add debug information
    if results.get('debug_info'):
        md_content.append("\n## 🔍 Source data (JSON)\n")
        md_content.append("```json\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        md_content.append(debug_json)
        md_content.append("\n```\n")
    
    return "".join(md_content)

def generate_text_report(results):
    """Generate a plain text report from the results."""
    
    content = ["Report\n"]
    
    # Add object and institution information
    object_name = results.get('object_name') or "unknown"
    institution_name = results.get('institution_name') or "unknown"
    content.extend([
        f"\nObject: {object_name}",
        f"\nInstitution: {institution_name}\n"
    ])
    
    # Add explanation of priority order
    content.append("\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n")
    
    # Add copyright status section
    content.append("\nCopyright status of the object\n")
    content.append("=" * 30 + "\n")
    
    if results['red']:
        content.append("\nRed status. There are legal obstacles.\n")
        for result in results['red']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['yellow']:
        content.append("\nYellow status. The tool is unable to determine the status.\n")
        for result in results['yellow']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['green']:
        content.append("\n\u2705 Green status. No issues detected.\n")
        for result in results['green']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['info']:
        content.append("\nInformational Messages\n")
        for result in results['info']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")

    # Add additional object classification section (NEW)
    if results.get('additional_classification_status'):
        content.append("\nAdditional Object Classification Status\n")
        content.append("=" * 30 + "\n")
        additional_classification = results['additional_classification_status']
        if additional_classification['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in additional_classification['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in additional_classification['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in additional_classification['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['info']:
            content.append("\nInformational Messages\n")
            for result in additional_classification['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")

    # Add first edition protection section (NEW)
    if results.get('first_edition_status'):
        content.append("\nFirst edition protection / posthumous edition status\n")
        content.append("=" * 30 + "\n")
        first_edition = results['first_edition_status']
        if first_edition['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in first_edition['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in first_edition['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['green']:
            content.append("\n\u2705 Green status. No issues detected.\n")
            for result in first_edition['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['info']:
            content.append("\nInformational Messages\n")
            for result in first_edition['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")

    # Add performance rights section
    if results.get('performance_status'):
        content.append("\nPerformance rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        performance_status = results['performance_status']
        
        if performance_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in performance_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in performance_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in performance_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['info']:
            content.append("\nInformational Messages\n")
            for result in performance_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        content.append("\nPhonogram rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        phonogram_status = results['phonogram_status']
        
        if phonogram_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in phonogram_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in phonogram_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in phonogram_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['info']:
            content.append("\nInformational Messages\n")
            for result in phonogram_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add film fixation rights section
    if results.get('film_fixation_status'):
        content.append("\nFilm fixation rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        film_fixation_status = results['film_fixation_status']
        
        if film_fixation_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in film_fixation_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in film_fixation_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in film_fixation_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['info']:
            content.append("\nInformational Messages\n")
            for result in film_fixation_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        content.append("\nBroadcasting organisation rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        broadcast_status = results['broadcast_status']
        
        if broadcast_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in broadcast_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if broadcast_status['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in broadcast_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if broadcast_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in broadcast_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if broadcast_status['info']:
            content.append("\nInformational Messages\n")
            for result in broadcast_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add digital representation status section
    content.append("\nIP status of the digital representation of the object\n")
    content.append("=" * 30 + "\n")
    
    if results.get('digital_repr_status'):
        digital_status = results['digital_repr_status']
        
        if digital_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in digital_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if digital_status['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in digital_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if digital_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in digital_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add debug information in JSON format
    if results.get('debug_info'):
        content.append("\n🔍 Source Data (JSON):\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        content.append(debug_json)
        content.append("\n")
    
    return "".join(content) 

def calculate_additional_object_classification_status(data, intermediate):
    """Calculate status for additional object classification fields."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    current_year = intermediate.get('CURRENT_YEAR', datetime.now().year)
    
    # 1. potential_first_edition_not_work - yes or uncertain: YELLOW STATUS
    potential_first_edition = data.get('potential_first_edition_not_work')
    mark_used('potential_first_edition_not_work')
    if potential_first_edition in ['potential_first_edition_not_work', 'uncertain']:
        results['yellow'].append({
            'condition': 'PublicationNotAWork',
            'explanation': 'In some EU member states, such publications obtain protection equivalent to copyright.'
        })
    
    # 2. critical_edition - yes or uncertain: YELLOW STATUS
    critical_edition = data.get('critical_edition')
    mark_used('critical_edition')
    if critical_edition in ['critical_edition', 'uncertain']:
        results['yellow'].append({
            'condition': 'CriticalEdition',
            'explanation': 'In some EU member states, such publications obtain protection equivalent or closely similar to copyright.'
        })
    
    # 3. press_publication logic
    press_publication = data.get('press_publication')
    press_publication_year = data.get('press_publication_year')
    
    mark_used('press_publication')
    if press_publication_year is not None:
        mark_used('press_publication_year')
    
    if press_publication == 'not_press_publication':
        results['green'].append({
            'condition': 'NotPressPublication',
            'explanation': 'The object is not a press publication.'
        })
    elif press_publication in ['press_publication', 'uncertain']:
        if press_publication_year and press_publication_year > 0:
            if current_year > press_publication_year + 2:
                results['green'].append({
                    'condition': 'PressPublicationLapsed',
                    'explanation': f'If the object was protected as a press publication, it has lapsed (published in {press_publication_year}, protection expired in {press_publication_year + 2}).'
                })
            else:
                results['red'].append({
                    'condition': 'PressPublicationProtected',
                    'explanation': f'The object may be protected as a press publication (published in {press_publication_year}, protection until {press_publication_year + 2}).'
                })
        else:
            # No year provided, assume it might be protected
            results['red'].append({
                'condition': 'PressPublicationProtected',
                'explanation': 'The object may be protected as a press publication (publication year not provided).'
            })
    
    # 4. trademark - yes or uncertain: YELLOW STATUS
    trademark = data.get('trademark')
    mark_used('trademark')
    if trademark in ['trademark', 'uncertain']:
        results['yellow'].append({
            'condition': 'Trademark',
            'explanation': 'There may be obstacles stemming from trademark law.'
        })
    
    # 5. design - yes: YELLOW STATUS, uncertain: RED STATUS
    design_status = data.get('design')
    mark_used('design')
    if design_status == 'design':
        results['yellow'].append({
            'condition': 'Design',
            'explanation': 'There may be obstacles stemming from design law.'
        })
    elif design_status == 'uncertain':
        results['red'].append({
            'condition': 'Design',
            'explanation': 'There may be obstacles stemming from design law.'
        })
    
    return results, used_vars

def calculate_broadcast_rights_status(data, intermediate):
    """Calculate broadcasting organisation rights status for the original object only."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': []
    }
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_broadcast') == 'not_broadcast':
        mark_used('is_broadcast')
        results['green'].append({
            'condition': 'PublicDomainNotABroadcast',
            'explanation': 'It is not protected as a broadcast.'
        })
        return results, used_vars
    
    if data.get('broadcast_before_1970') == 'broadcast_made_before_1970':
        mark_used('broadcast_before_1970')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumbBroadcasts',
            'explanation': 'Given the time the broadcast was made, it has passed to the public domain.'
        })
        return results, used_vars
    
    # Add compound broadcast info message if needed
    if data.get('is_compound_broadcast') in ['compound', 'uncertain']:
        mark_used('is_compound_broadcast')
        results['info'].append({
            'condition': 'CompoundBroadcast',
            'explanation': 'This broadcast is, in fact, a collection of multiple broadcast or it is made from various broadcast. The analysis must be performed for each separately.'
        })
    
    # Year-based logic when not before 1970
    broadcast_year = data.get('broadcast_year')
    before_1970 = data.get('broadcast_before_1970') == 'broadcast_made_before_1970'
    country_eea_broadcast = intermediate.get('CountryOfOriginEEABroadcasts', False)
    current_year_val = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # Unknown broadcast year (but not before 1970)
    if not before_1970 and not broadcast_year:
        results['yellow'].append({
            'condition': 'BroadcastYearUnknown',
            'explanation': 'It is impossible to determine if a broadcast is still protected.'
        })
        return results, used_vars

    # Known broadcast year logic (EEA focus)
    if not before_1970 and broadcast_year and country_eea_broadcast:
        broadcast_initial_protection_lapse = broadcast_year + 50

        if current_year_val > broadcast_initial_protection_lapse:
            results['green'].append({
                'condition': 'BroadcastProtectionLapsedArticle3',
                'explanation': 'The broadcast was protected but the protection has lapsed.'
            })
        else:
            results['red'].append({
                'condition': 'BroadcastStillProtectedArticle3',
                'explanation': 'The broadcast is still under protection.'
            })

    # Non-EEA branch: mirror EEA logic to decide GREEN (if it would lapse even under EEA) or YELLOW (otherwise)
    if not before_1970 and broadcast_year and not country_eea_broadcast:
        broadcast_initial_protection_lapse = broadcast_year + 50

        would_be_green = current_year_val > broadcast_initial_protection_lapse

        if would_be_green:
            results['green'].append({
                'condition': 'BroadcastLapsedEvenIfEEA',
                'explanation': 'Country of origin appears to be outside the EEA, but the broadcast would have lost protection even if the country of origin were in the EEA.'
            })
        else:
            results['yellow'].append({
                'condition': 'BroadcastNonEEAUncertain',
                'explanation': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the broadcast would not have lapsed even under EEA rules, the status is uncertain.'
            })

    # Broadcasting-specific rights overrides (mirror phonogram logic)
    # 1) Current rightholder override (green if ours - highest priority)
    mark_used('broadcast_current_rightholder')
    if data.get('broadcast_current_rightholder') == 'rightholder_us':
        results['red'] = []
        results['yellow'] = []
        results['green'].append({
            'condition': 'BroadcastCurrentRightHolderKnown',
            'explanation': 'The broadcast is protected by broadcasting organisation rights, but you are the rightholder.'
        })
        return results, used_vars  # Early return - highest priority

    # 2) CC license override for broadcast (medium priority)
    mark_used('broadcast_cc_license')
    cc_choice = data.get('broadcast_cc_license')
    if cc_choice and cc_choice != 'not_applicable':
        broadcast_cc_green = ['cc0', 'cc_by']
        broadcast_cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
        if cc_choice in broadcast_cc_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'BroadcastAvailableCCLicense',
                'explanation': 'While the broadcast is protected, it is available under an open content license (e.g., CC0 or CC‑BY).'
            })
        elif cc_choice in broadcast_cc_yellow and (results['red'] or results['yellow']):
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'BroadcastAvailableCCLicense',
                    'explanation': 'While the broadcast is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalBroadcastAvailableCCLicense',
                    'explanation': 'The broadcast may be available under an open content license. Additional verification may be needed.'
                })
        return results, used_vars  # Early return - medium priority

    # 3) Rights acquisition override for broadcast (lowest priority)
    mark_used('broadcast_rights_acquired_to_make_available')
    ra_choice = data.get('broadcast_rights_acquired_to_make_available')
    if ra_choice and ra_choice not in ['not_applicable', 'unknown', 'no']:
        broadcast_ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
        broadcast_ra_yellow = ['orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
        if ra_choice in broadcast_ra_green and (results['red'] or results['yellow']):
            results['red'] = []
            results['yellow'] = []
            results['green'].append({
                'condition': 'BroadcastOnlineAvailable',
                'explanation': 'While the broadcast is protected, you have acquired the necessary rights to make it available online.'
            })
        elif ra_choice in broadcast_ra_yellow and (results['red'] or results['yellow']):
            if results['red']:
                results['red'] = []
                results['yellow'].append({
                    'condition': 'BroadcastOnlineAvailable',
                    'explanation': 'While the broadcast is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
                })
            elif results['yellow']:
                results['yellow'].append({
                    'condition': 'AdditionalBroadcastOnlineAvailable',
                    'explanation': 'There may be legal provisions allowing online availability of the broadcast. Additional verification may be needed.'
                })
    
    return results, used_vars