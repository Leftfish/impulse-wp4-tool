"""
Digital representation module.

This module contains logic for calculating digital representation status and related intermediate values.
"""

from defaults import ResultsDict
from utils_modules.text_constants import (
    DigitalRepresentationCondition,
    get_explanation,
    DIGITAL_REPRESENTATION_RIGHTS_TEMPLATES,
    DIGITAL_REPRESENTATION_RIGHT_TYPES,
)


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

    # Map form fields to status names using enum values
    status_mapping = {
        'copyright': (DigitalRepresentationCondition.DigitalRepresentationCopyrightStatus.value, 'DigitalRepresentationCopyrightAcquired'),
        'audio_recording_rights': (DigitalRepresentationCondition.DigitalRepresentationPhonogramStatus.value, 'DigitalRepresentationPhonogramAcquired'),
        'film_fixation_rights': (DigitalRepresentationCondition.DigitalRepresentationFilmFixationStatus.value, 'DigitalRepresentationFilmFixationAcquired'),
        'other_ip_rights': (DigitalRepresentationCondition.DigitalRepresentationOtherIPStatus.value, 'DigitalRepresentationOtherIPAcquired')
    }

    results = {protection_type: ResultsDict() for protection_type in status_mapping}
    results = ResultsDict()

    # First pass: Calculate initial statuses
    mark_used('digital_repr_ip_rights')
    for field, (status_name, _) in status_mapping.items():
        value = digital_repr_ip_rights.get(field, 'not_applicable')
        right_type = DIGITAL_REPRESENTATION_RIGHT_TYPES[field]

        if value == 'yes':
            results['red'].append({
                'condition': status_name,
                'explanation': get_explanation(status_name, 'red', 'digital_representation', right_type=right_type)
            })
        elif value == 'uncertain':
            results['yellow'].append({
                'condition': status_name,
                'explanation': get_explanation(status_name, 'yellow', 'digital_representation', right_type=right_type)
            })
        elif value == 'no':
            results['green'].append({
                'condition': status_name,
                'explanation': get_explanation(status_name, 'green', 'digital_representation', right_type=right_type)
            })

    # Second pass: Process three separate questions for each IP right
    # Map each IP right to its corresponding field names and condition names
    right_type_mapping = {
        'copyright': {
            'status_name': DigitalRepresentationCondition.DigitalRepresentationCopyrightStatus.value,
            'rightholder_field': 'digital_repr_copyright_current_rightholder',
            'rightholder_condition': DigitalRepresentationCondition.DigitalRepresentationCopyrightCurrentRightHolderKnown.value,
            'cc_license_field': 'digital_repr_copyright_cc_license',
            'cc_license_condition': DigitalRepresentationCondition.DigitalRepresentationCopyrightAvailableCCLicense.value,
            'rights_acquired_field': 'digital_repr_copyright_rights_acquired',
            'rights_acquired_condition': DigitalRepresentationCondition.DigitalRepresentationCopyrightOnlineAvailable.value,
        },
        'audio_recording_rights': {
            'status_name': DigitalRepresentationCondition.DigitalRepresentationPhonogramStatus.value,
            'rightholder_field': 'digital_repr_phonogram_current_rightholder',
            'rightholder_condition': DigitalRepresentationCondition.DigitalRepresentationPhonogramCurrentRightHolderKnown.value,
            'cc_license_field': 'digital_repr_phonogram_cc_license',
            'cc_license_condition': DigitalRepresentationCondition.DigitalRepresentationPhonogramAvailableCCLicense.value,
            'rights_acquired_field': 'digital_repr_phonogram_rights_acquired',
            'rights_acquired_condition': DigitalRepresentationCondition.DigitalRepresentationPhonogramOnlineAvailable.value,
        },
        'film_fixation_rights': {
            'status_name': DigitalRepresentationCondition.DigitalRepresentationFilmFixationStatus.value,
            'rightholder_field': 'digital_repr_film_fixation_current_rightholder',
            'rightholder_condition': DigitalRepresentationCondition.DigitalRepresentationFilmFixationCurrentRightHolderKnown.value,
            'cc_license_field': 'digital_repr_film_fixation_cc_license',
            'cc_license_condition': DigitalRepresentationCondition.DigitalRepresentationFilmFixationAvailableCCLicense.value,
            'rights_acquired_field': 'digital_repr_film_fixation_rights_acquired',
            'rights_acquired_condition': DigitalRepresentationCondition.DigitalRepresentationFilmFixationOnlineAvailable.value,
        },
        'other_ip_rights': {
            'status_name': DigitalRepresentationCondition.DigitalRepresentationOtherIPStatus.value,
            'rightholder_field': 'digital_repr_other_current_rightholder',
            'rightholder_condition': DigitalRepresentationCondition.DigitalRepresentationOtherIPCurrentRightHolderKnown.value,
            'cc_license_field': 'digital_repr_other_cc_license',
            'cc_license_condition': DigitalRepresentationCondition.DigitalRepresentationOtherIPAvailableCCLicense.value,
            'rights_acquired_field': 'digital_repr_other_rights_acquired',
            'rights_acquired_condition': DigitalRepresentationCondition.DigitalRepresentationOtherIPOnlineAvailable.value,
        },
    }

    # Track which IP rights used separate questions (for fallback logic per right)
    rights_using_separate_questions = set()

    for field, config in right_type_mapping.items():
        status_name = config['status_name']
        
        # Check if we have RED or YELLOW status for this right
        has_red = any(r['condition'] == status_name for r in results.get('red', []))
        has_yellow = any(r['condition'] == status_name for r in results.get('yellow', []))
        has_green = any(r['condition'] == status_name for r in results.get('green', []))

        # 1. Rightholder check (only if no green status yet, similar to performance.py line 280)
        rightholder_field = config['rightholder_field']
        mark_used(rightholder_field)
        # Check if there's already a rights_green status for this specific right
        has_rights_green = any(r['condition'] == config['rightholder_condition'] or 
                             r['condition'] == config['cc_license_condition'] or
                             r['condition'] == config['rights_acquired_condition']
                             for r in results.get('rights_green', []))
        if not has_green and not has_rights_green and data.get(rightholder_field) == 'rightholder_us':
            rights_using_separate_questions.add(field)
            _cond = config['rightholder_condition']
            results['rights_green'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'rights_green', 'digital_representation'),
            })

        # 2. CC license check
        cc_field = config['cc_license_field']
        mark_used(cc_field)
        cc_choice = data.get(cc_field)
        if cc_choice and cc_choice not in ['no', 'not_applicable']:
            rights_using_separate_questions.add(field)
            _cond = config['cc_license_condition']
            cc_green = ['cc0', 'cc_by']
            cc_yellow = ['cc_by_sa', 'cc_by_nc_sa', 'cc_by_nd', 'cc_by_nc_nd', 'other_open']
            if cc_choice in cc_green and (has_red or has_yellow):
                results['rights_green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'rights_green', 'digital_representation'),
                })
            elif cc_choice in cc_yellow and (has_red or has_yellow):
                results['rights_yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'rights_yellow', 'digital_representation'),
                })

        # 3. Rights acquired check
        rights_field = config['rights_acquired_field']
        mark_used(rights_field)
        rights_choice = data.get(rights_field)
        if rights_choice and rights_choice not in ['not_applicable', 'unknown', 'no']:
            rights_using_separate_questions.add(field)
            _cond = config['rights_acquired_condition']
            ra_green = ['rights_assignment', 'license_agreement', 'employee_rights']
            ra_yellow = ['limited_license_agreement', 'orphan_works', 'out_of_commerce', 'quote_right', 'other_law']
            if rights_choice in ra_green and (has_red or has_yellow):
                results['rights_green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'rights_green', 'digital_representation'),
                })
            elif rights_choice in ra_yellow and (has_red or has_yellow):
                results['rights_yellow'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'rights_yellow', 'digital_representation'),
                })

    # Third pass: Fallback to combined question (for rights that didn't use separate questions)
    # Only use combined question for rights that didn't have separate question values
    # This maintains backward compatibility
    '''rights_availability_data = digital_repr_rights_availability
    if not rights_availability_data:
        rights_availability_data = data.get('digital_repr_ip_rights_acquired', {})
    
    if rights_availability_data:
        # Only apply combined question for rights that didn't use separate questions
        filtered_rights_data = {
            field: choice for field, choice in rights_availability_data.items()
            if field not in rights_using_separate_questions
        }
        if filtered_rights_data:
            results = apply_digital_repr_rights_availability_status(results, filtered_rights_data)
    '''
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

    # Map IP rights to their status names using enum values
    status_mapping = {
        'copyright': (DigitalRepresentationCondition.DigitalRepresentationCopyrightStatus.value, 'digital representation copyright'),
        'audio_recording_rights': (DigitalRepresentationCondition.DigitalRepresentationPhonogramStatus.value, 'digital representation phonogram'),
        'film_fixation_rights': (DigitalRepresentationCondition.DigitalRepresentationFilmFixationStatus.value, 'digital representation film fixation'),
        'other_ip_rights': (DigitalRepresentationCondition.DigitalRepresentationOtherIPStatus.value, 'digital representation other IP')
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
            
            license_type = DIGITAL_REPRESENTATION_RIGHTS_TEMPLATES.get(choice, choice)
            results['green'].append({
                'condition': status_name,
                'explanation': get_explanation(status_name, 'rights_green', 'digital_representation', right_type=right_description, license_type=license_type)
            })

        elif choice in yellow_upgrade_choices:
            if has_red:
                # Remove existing red status
                results['red'] = [r for r in results.get('red', []) if r['condition'] != status_name]

                # Add yellow status
                license_type = DIGITAL_REPRESENTATION_RIGHTS_TEMPLATES.get(choice, choice)
                results['yellow'].append({
                    'condition': status_name,
                    'explanation': get_explanation(status_name, 'rights_yellow', 'digital_representation', right_type=right_description, license_type=license_type)
                })
            elif has_yellow:
                # Add additional yellow status without clearing existing ones
                additional_status_name = f'Additional{status_name}'
                license_type = DIGITAL_REPRESENTATION_RIGHTS_TEMPLATES.get(choice, choice)
                results['yellow'].append({
                    'condition': additional_status_name,
                    'explanation': get_explanation(additional_status_name, 'rights_yellow', 'digital_representation', right_type=right_description, license_type=license_type)
                })


    return results
