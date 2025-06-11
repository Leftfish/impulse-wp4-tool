from datetime import datetime
from data.country_codes import is_eea_country, is_eu_country

CURRENT_YEAR = datetime.now().year

def calculate_intermediate_values(data):
    """Calculate intermediate boolean values used in copyright calculations."""
    current_year = datetime.now().year
    
    # Author-related calculations
    all_authors_known = all(author.get('identity_known', False) for author in data.get('authors', []))
    all_authors_anonymous = all(not author.get('identity_known', True) for author in data.get('authors', []))
    
    # Country calculations
    country_codes = [author.get('country_of_origin') for author in data.get('authors', [])]
    author_country_eea = any(is_eea_country(code) for code in country_codes if code)
    country_of_origin_unknown = any(code == 'XX' for code in country_codes)
    
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
    
    # Posthumous edition calculations
    is_posthumous = False
    posthumous_edition_dates_unknown = False
    posthumous_edition_publication_after_public_domain = False
    
    # First check if we can determine it's a posthumous publication
    if data.get('first_publication_year') and data.get('author_death_year'):
        is_posthumous = data['first_publication_year'] > data['author_death_year']
        if is_posthumous:
            years_after_death = data['first_publication_year'] - data['author_death_year']
            posthumous_edition_publication_after_public_domain = years_after_death > 70
    elif data.get('author_alive') == 'no':  # We know author is dead but don't have exact years
        is_posthumous = True
        posthumous_edition_dates_unknown = True  # We know it's posthumous but can't calculate years
    
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
        'IsPosthumous': is_posthumous,
        'PosthumousEditionPublicationAfterPublicDomain': posthumous_edition_publication_after_public_domain,
        'PosthumousEditionDatesUnknown': posthumous_edition_dates_unknown
    }

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
    elif cc_license_choice in yellow_upgrade_choices and results['red']:
        # Clear red results as we're upgrading to yellow
        results['red'] = []
        results['yellow'].append({
            'condition': 'ObjectAvailableCCLicense',
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
    elif availability_choice in yellow_upgrade_choices and results['red']:
        # Clear red results as we're upgrading to yellow
        results['red'] = []
        results['yellow'].append({
            'condition': 'ObjectOnlineAvailable',
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
        elif choice in yellow_upgrade_choices and has_red:
            # Remove existing red status
            results['red'] = [r for r in results['red'] if r['condition'] != status_name]
            
            # Add yellow status
            results['yellow'].append({
                'condition': status_name,
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

def calculate_results(data, intermediate):
    """Calculate final copyright status results based on intermediate values."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': [],
        'object_name': data.get('object_name'),
        'institution_name': data.get('institution_name'),
        'digital_repr_status': None,  # Will store digital representation status
        'debug_info': {}  # Add debug info tracking
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
        
        # Prepare debug info
        basic_info_fields = ['object_name', 'institution_name', 'object_url', 'digital_repr_nature']
        results['debug_info'] = {
            'basic_information': {k: data[k] for k in basic_info_fields if k in data},
            'input_data': {k: v for k, v in data.items() if k not in basic_info_fields},
            'used_variables': list(used_vars),
            'unused_variables': [k for k in data.keys() if k not in used_vars]
        }
        return results
    
    if data.get('created_before_1850') == 'made_before_1850':
        mark_used('created_before_1850')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumb',
            'explanation': 'The object is not protected by copyright because it was created before 1850.'
        })
        
        # Prepare debug info
        basic_info_fields = ['object_name', 'institution_name', 'object_url', 'digital_repr_nature']
        results['debug_info'] = {
            'basic_information': {k: data[k] for k in basic_info_fields if k in data},
            'input_data': {k: v for k, v in data.items() if k not in basic_info_fields},
            'used_variables': list(used_vars),
            'unused_variables': [k for k in data.keys() if k not in used_vars]
        }
        return results
    
    # Special case: if both conditions are uncertain but it's from before 1850, it's GREEN
    if (data.get('is_copyright_work') == 'uncertain' and 
        data.get('created_before_1850') == 'made_before_1850'):
        mark_used('is_copyright_work', 'created_before_1850')
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumb',
            'explanation': 'Even though it is uncertain whether this object qualifies as a work, it was created before 1850 and is therefore in the public domain.'
        })
        
        # Prepare debug info
        basic_info_fields = ['object_name', 'institution_name', 'object_url', 'digital_repr_nature']
        results['debug_info'] = {
            'basic_information': {k: data[k] for k in basic_info_fields if k in data},
            'input_data': {k: v for k, v in data.items() if k not in basic_info_fields},
            'used_variables': list(used_vars),
            'unused_variables': [k for k in data.keys() if k not in used_vars]
        }
        return results
    
    # Handle other uncertainty cases
    if data.get('is_copyright_work') == 'uncertain':
        mark_used('is_copyright_work')
        results['yellow'].append({
            'condition': 'UncertainIfWork',
            'explanation': 'It is uncertain whether this object qualifies as a work protected by copyright.'
        })
        
        # Prepare debug info
        basic_info_fields = ['object_name', 'institution_name', 'object_url', 'digital_repr_nature']
        results['debug_info'] = {
            'basic_information': {k: data[k] for k in basic_info_fields if k in data},
            'input_data': {k: v for k, v in data.items() if k not in basic_info_fields},
            'used_variables': list(used_vars),
            'unused_variables': [k for k in data.keys() if k not in used_vars]
        }
        return results
    
    mark_used('created_before_1850')  # Mark as used since we're using it in the evaluation
    
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
        mark_used('authors')
        if intermediate['DeathYearUnknown']:
            mark_used('author_death_year')
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

    # Handle posthumous edition independently
    if intermediate['IsPosthumous']:
        mark_used('first_publication_year', 'author_death_year')
        if intermediate['PosthumousEditionDatesUnknown']:
            if results['green'] or data.get('current_rightholder') != 'rightholder_us':
                results['yellow'].append({
                    'condition': 'CopyrightLapsedButPosthumousEditionUnknown',
                    'explanation': 'This is a posthumous publication, but we cannot determine if its protection has lapsed because the exact years are unknown.'
                })
        elif (intermediate['PosthumousEditionPublicationAfterPublicDomain'] and
              data.get('first_publication_year') and
              (datetime.now().year - data['first_publication_year']) <= 25):
            
            if results['green'] or data.get('current_rightholder') != 'rightholder_us':
                results['yellow'].append({
                    'condition': 'CopyrightLapsedButPosthumousEditionNotLapsed',
                    'explanation': 'Copyright protection of the object lapsed, but the protection of posthumous (first) editions may still apply. Additional verification is needed due to differences between EU member states.'
                })
    
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
    
    md_content = ["# Legal Status Evaluation Report\n"]
    
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
        md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
        for result in results['red']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['yellow']:
        md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
        for result in results['yellow']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['green']:
        md_content.append("\n### ✅ Green status. No issues detected.\n")
        for result in results['green']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['info']:
        md_content.append("\n### 📝 Informational Messages\n")
        for result in results['info']:
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
        md_content.append("\n## 🔍 Source Data (JSON)\n")
        md_content.append("```json\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        md_content.append(debug_json)
        md_content.append("\n```\n")
    
    return "".join(md_content)

def generate_text_report(results):
    """Generate a plain text report from the results."""
    
    content = ["Legal Status Evaluation Report\n"]
    
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
        content.append("\n✅ Green status. No issues detected.\n")
        for result in results['green']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['info']:
        content.append("\nInformational Messages\n")
        for result in results['info']:
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