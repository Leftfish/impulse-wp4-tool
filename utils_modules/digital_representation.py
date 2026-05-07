"""
Digital representation module.

This module contains logic for calculating digital representation status and related intermediate values.
"""

from defaults import ResultsDict
from utils_modules.text_constants import (
    DigitalRepresentationCondition,
    get_explanation,
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

    # Mark digital representation fields as used
    if 'digital_repr_ip_rights' in data:
        mark_used('digital_repr_ip_rights')
    if 'digital_repr_ip_rights_acquired' in data:
        mark_used('digital_repr_ip_rights_acquired')

    # Map form fields to status names using enum values
    status_mapping = {
        'copyright': (DigitalRepresentationCondition.DigitalRepresentationCopyrightStatus.value, 'DigitalRepresentationCopyrightAcquired'),
        'phonogram_rights': (DigitalRepresentationCondition.DigitalRepresentationPhonogramStatus.value, 'DigitalRepresentationPhonogramAcquired'),
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
        'phonogram_rights': {
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


    for field, config in right_type_mapping.items():
        status_name = config['status_name']
        
        # Check if we have RED or YELLOW status for this right
        has_red = any(r['condition'] == status_name for r in results.get('red', []))
        has_yellow = any(r['condition'] == status_name for r in results.get('yellow', []))
        has_green = any(r['condition'] == status_name for r in results.get('green', []))

        # 1. Rightholder check (only if no green status yet)
        rightholder_field = config['rightholder_field']
        mark_used(rightholder_field)
        # Check if there's already a rights_green status for this specific right
        has_rights_green = any(r['condition'] == config['rightholder_condition'] or 
                             r['condition'] == config['cc_license_condition'] or
                             r['condition'] == config['rights_acquired_condition']
                             for r in results.get('rights_green', []))
        if not has_green and not has_rights_green and data.get(rightholder_field) == 'rightholder_us':
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
            _cond = config['rights_acquired_condition']
            ra_green = ['license_agreement']
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

    # Third pass: Check Article 14 CDSM applicability for visual art works
    mark_used('visual_art_work')
    visual_art_work = data.get('visual_art_work')
    if visual_art_work in ['yes', 'uncertain']:
        # Check phonogram rights
        phonogram_value = digital_repr_ip_rights.get('phonogram_rights', 'no')
        if phonogram_value in ['yes', 'uncertain']:
            _cond = DigitalRepresentationCondition.Article14CDSMPhonogram.value
            results['info'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'info', 'digital_representation'),
            })
        
        # Check film fixation rights
        film_fixation_value = digital_repr_ip_rights.get('film_fixation_rights', 'no')
        if film_fixation_value in ['yes', 'uncertain']:
            _cond = DigitalRepresentationCondition.Article14CDSMFilmFixation.value
            results['info'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'info', 'digital_representation'),
            })
        
        # Check other IP rights
        other_ip_value = digital_repr_ip_rights.get('other_ip_rights', 'no')
        if other_ip_value in ['yes', 'uncertain']:
            _cond = DigitalRepresentationCondition.Article14CDSMOtherIP.value
            results['info'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'info', 'digital_representation'),
            })

    # Fourth pass: check if AI was used to create the digital representation
    mark_used('digital_repr_with_ai')
    
    digital_repr_with_ai = data.get('digital_repr_with_ai')
    copyright_value = digital_repr_ip_rights.get('copyright', 'no')
    if digital_repr_with_ai in ['yes', 'uncertain'] and copyright_value in ['yes', 'uncertain']:
        _cond = DigitalRepresentationCondition.DigitalRepresentationAIUsed.value
        results['info'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'info', 'digital_representation'),
        })
                


    return results, used_vars