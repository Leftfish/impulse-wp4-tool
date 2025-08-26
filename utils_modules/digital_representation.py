"""
Digital representation module.

This module contains logic for calculating digital representation status and related intermediate values.
"""

from datetime import datetime


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
