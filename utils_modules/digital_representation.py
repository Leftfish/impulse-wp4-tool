"""
Digital representation module.

This module contains logic for calculating digital representation status and related intermediate values.
"""

from defaults import ResultsDict
from datetime import datetime


def calculate_digital_representation_status(data, intermediate=None):
    """Calculate initial status for digital representation IP rights."""
    
    # Track variable usage
    used_vars = set()

    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    # Extract digital representation data from the main data dictionary
    digital_repr_ip_rights = data.get('digital_repr_ip_rights', {})
    digital_repr_rights_availability = data.get('digital_repr_rights_availability', {})

    # Mark digital representation fields as used
    if 'digital_repr_ip_rights' in data:
        mark_used('digital_repr_ip_rights')
    if 'digital_repr_ip_rights_acquired' in data:
        mark_used('digital_repr_ip_rights_acquired')
    if 'digital_repr_rights_availability' in data:
        mark_used('digital_repr_rights_availability')
    
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
    
    results = {protection_type: ResultsDict() for protection_type in status_mapping}
    results = ResultsDict()
    
    # First pass: Calculate initial statuses
    mark_used('digital_repr_ip_rights')
    for field, (status_name, _) in status_mapping.items():
        value = digital_repr_ip_rights.get(field, 'not_applicable')
        if value == 'yes':
            results['red'].append({
                'condition': status_name,
                'explanation': f'The digital representation is protected by {right_descriptions[field]}.'
            })
        elif value == 'uncertain':
            results['yellow'].append({
                'condition': status_name,
                'explanation': f'It is uncertain whether the digital representation is protected by {right_descriptions[field]}.'
            })
        elif value == 'no':
            results['green'].append({
                'condition': status_name,
                'explanation': f'The digital representation is not protected by {right_descriptions[field]}.'
            })
    
    
    # Second pass: Apply rights availability modifications if available
    results = apply_digital_repr_rights_availability_status(results, digital_repr_rights_availability)

    return results, used_vars


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
        'copyright': ('DigitalRepresentationCopyrightStatus', 'digital representation copyright'),
        'audio_recording_rights': ('DigitalRepresentationPhonogramStatus', 'digital representation phonogram'),
        'film_fixation_rights': ('DigitalRepresentationFilmFixationStatus', 'digital representation film fixation'),
        'performance_rights': ('DigitalRepresentationPerformanceStatus', 'digital representation performance'),
        'other_ip_rights': ('DigitalRepresentationOtherIPStatus', 'digital representation other IP')
    }

    # Explanation templates for different types of availability
    explanation_templates = {
        'cc0': 'The {right_type} is available under CC0 (public domain dedication).',
        'cc_by': 'The {right_type} is available under CC BY license.',
        'rights_assignment': 'The institution has acquired the rights through assignment.',
        'license_agreement': 'The institution has acquired the rights through license agreement.',
        'employee_rights': 'The institution has acquired the rights as the employer.',
        'cc_by_sa': 'The {right_type} is available under CC BY-SA license.',
        'cc_by_nc_sa': 'The {right_type} is available under CC BY-NC-SA license.',
        'cc_by_nd': 'The {right_type} is available under CC BY-ND license.',
        'cc_by_nc_nd': 'The {right_type} is available under CC BY-NC-ND license.',
        'other_open': 'The {right_type} is available under other open license.',
        'orphan_works': 'The {right_type} is available under orphan works provisions.',
        'out_of_commerce': 'The {right_type} is available under out-of-commerce provisions.',
        'quote_right': 'The {right_type} is available under quotation rights.',
        'other_law': 'The {right_type} is available under other legal provisions.'
    }

    for field, (status_name, right_description) in status_mapping.items():
        choice = rights_availability_data.get(field, 'not_applicable')
        
        if choice == 'not_applicable':
            continue
        
        has_red = any(r['condition'] == status_name for r in results.get('red', []))
        has_yellow = any(r['condition'] == status_name for r in results.get('yellow', []))

        if choice in green_upgrade_choices and (has_red or has_yellow):
            # Remove existing status
            results['red'] = [r for r in results.get('red', []) if r['condition'] != status_name]
            results['yellow'] = [r for r in results.get('yellow', []) if r['condition'] != status_name]

            # Add green status
            print("Adding green status:", status_name)
            results['green'].append({
                'condition': status_name,
                'explanation': explanation_templates[choice].format(right_type=right_description)
            })

        elif choice in yellow_upgrade_choices:
            if has_red:
                # Remove existing red status
                results['red'] = [r for r in results.get('red', []) if r['condition'] != status_name]

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
