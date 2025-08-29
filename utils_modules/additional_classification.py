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


def calculate_additional_object_classification_status(data, intermediate):
    """Calculate status for additional object classification fields."""
    results = ResultsDict()
    
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
    
    if potential_first_edition not in ['potential_first_edition_not_work', 'uncertain'] and \
        critical_edition not in ['critical_edition', 'uncertain'] and \
        press_publication not in ['press_publication', 'uncertain'] and \
        trademark not in ['trademark', 'uncertain'] and \
        design_status not in ['design', 'uncertain']:
        results['green'].append({
            'condition': 'NoOtherIPRights',
            'explanation': 'No other IP rights to consider'
        })

    return results, used_vars


