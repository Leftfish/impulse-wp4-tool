"""
Additional object classification module.

This module contains logic for calculating status of additional object classification fields:
- potential_first_edition_not_work
- critical_edition
- press_publication
- press_publication_year
- trademark
- design
"""
from defaults import ResultsDict
from datetime import datetime
from utils_modules.text_constants import (
    AdditionalClassificationCondition,
    get_explanation,
    PRESS_PUBLICATION_TERM,
)


def calculate_additional_object_classification_status(data, intermediate):
    """Calculate status for additional object classification fields."""
    results = ResultsDict()
    
    # Track variable usage
    used_vars = set()
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
    
    current_year = intermediate.get('CURRENT_YEAR', datetime.now().year)

    # Rationale: some countries protect first editions of objects
    # that are not works, so yes or uncertain: YELLOW STATUS
    potential_first_edition = data.get('potential_first_edition_not_work')
    mark_used('potential_first_edition_not_work')

    if potential_first_edition in ['potential_first_edition_not_work', 'uncertain']:
        _cond = AdditionalClassificationCondition.PublicationNotAWork.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
        })
    
    # Rationale: some countries protect scientific/critical_edition 
    # by related rights, so yes or uncertain: YELLOW STATUS
    critical_edition = data.get('critical_edition')
    mark_used('critical_edition')

    if critical_edition in ['critical_edition', 'uncertain']:
        _cond = AdditionalClassificationCondition.CriticalEdition.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
        })
    
    # Rationale: the press publication right (Art. 15 CDSM Directive)
    press_publication = data.get('press_publication')
    press_publication_year = data.get('press_publication_year')
    mark_used('press_publication')
    
    if press_publication_year is not None:
        mark_used('press_publication_year')
    
    if press_publication == 'not_press_publication':
        _cond = AdditionalClassificationCondition.NotPressPublication.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'additional_classification'),
        })
    elif press_publication == 'press_publication':
        if press_publication_year and press_publication_year > 0:
            if current_year > press_publication_year + PRESS_PUBLICATION_TERM:
                _cond = AdditionalClassificationCondition.PressPublicationLapsed.value
                results['green'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'green', 'additional_classification', 
                                                  press_publication_year=press_publication_year,
                                                  expiry_year=press_publication_year + 2),
                })
            else:
                _cond = AdditionalClassificationCondition.PressPublicationProtected.value
                results['red'].append({
                    'condition': _cond,
                    'explanation': get_explanation(_cond, 'red', 'additional_classification',
                                                  press_publication_year=press_publication_year,
                                                  expiry_year=press_publication_year + 2),
                })
        else:
            # No year provided, it might be protected
            _cond = AdditionalClassificationCondition.PressPublicationProtected.value
            results['yellow'].append({
                'condition': _cond,
                'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
            })
    elif press_publication == 'uncertain':
        _cond = AdditionalClassificationCondition.PressPublicationUncertain.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
        })

    
    # Rationale: depending on the context, trademark protection may be
    # relevant, so yes or uncertain: YELLOW STATUS
    trademark = data.get('trademark')
    mark_used('trademark')
    if trademark in ['trademark', 'uncertain']:
        _cond = AdditionalClassificationCondition.Trademark.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
        })
    
    # Rationale: depending on the context, design protection may be
    # relevant, so yes or uncertain: YELLOW STATUS
    design_status = data.get('design')
    mark_used('design')
    if design_status in ['design', 'uncertain']:
        _cond = AdditionalClassificationCondition.Design.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
        })

    unregistered_design_status = data.get('design_unregistered')
    mark_used('design_unregistered')
    if unregistered_design_status in ['design', 'uncertain']:
        _cond = AdditionalClassificationCondition.UnregisteredDesign.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'additional_classification'),
        })
    
    # Rationale: if none of the above rights are relevant, then GREEN
    if potential_first_edition not in ['potential_first_edition_not_work', 'uncertain'] and \
        critical_edition not in ['critical_edition', 'uncertain'] and \
        press_publication not in ['press_publication', 'uncertain'] and \
        trademark not in ['trademark', 'uncertain'] and \
        design_status not in ['design', 'uncertain']:
        _cond = AdditionalClassificationCondition.NoOtherIPRights.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'additional_classification'),
        })

    return results, used_vars




