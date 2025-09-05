"""
Other legal issues module.

This module contains logic for calculating other legal issues status and related intermediate values.
"""

from defaults import ResultsDict
from utils_modules.text_constants import (
    OtherLegalIssuesCondition,
    get_explanation,
)

def calculate_intermediate_values_other_legal_issues(data):
    """Calculate intermediate boolean values for other legal issues assessment."""
    return {
        'HasContractualRestrictions': data.get('object_contractual_restrictions') != 'no_contractual_restrictions',
        'HasAdministrativeRestrictions': data.get('object_administrative_restrictions') != 'no_administrative_restrictions',
        'HasOwnershipIssues': data.get('object_ownership_status') in ['no_basis', 'unknown_owner', 'other'],
        'ProvenanceNotTraced': data.get('object_provenance_traced') != 'provenance_traced',
        'HasProvenanceIssues': data.get('object_provenance_issues') != 'provenance_not_troublesome',
        'ContainsLivingIdentifiableInfo': data.get('object_living_identifiable_info') != 'does_not_contain_identifiable_living',
        'ContainsSensitiveHistoricalInfo': data.get('object_sensitive_historical_info') != 'does_not_contain_sensitive_historical',
        'ContainsTotalitarianAssociations': data.get('object_totalitarian_associations') != 'does_not_contain_totalitarian_associations',
        'ContainsDiscriminatoryContent': data.get('object_discriminatory_content') != 'does_not_contain_discriminatory',
        'ContainsOtherSensitiveContent': data.get('object_other_sensitive_content') != 'does_not_contain_other_sensitive',
        'HasOtherProblems': data.get('object_other_problems') != 'no_other_problems'
    }


def calculate_other_legal_issues_status(data, intermediate_values):
    """Calculate the status for other legal issues."""
    results = ResultsDict()
    
    # Track variable usage
    used_vars = set()

    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)
       
    # Check each condition and add YELLOW statuses
    mark_used('object_contractual_restrictions')
    if intermediate_values['HasContractualRestrictions']:
        _cond = OtherLegalIssuesCondition.HasContractualRestrictions.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_administrative_restrictions')
    if intermediate_values['HasAdministrativeRestrictions']:
        _cond = OtherLegalIssuesCondition.HasAdministrativeRestrictions.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_ownership_status')
    if intermediate_values['HasOwnershipIssues']:
        _cond = OtherLegalIssuesCondition.HasOwnershipIssues.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_provenance_traced')
    if intermediate_values['ProvenanceNotTraced']:
        _cond = OtherLegalIssuesCondition.ProvenanceNotTraced.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_provenance_issues')
    if intermediate_values['HasProvenanceIssues']:
        _cond = OtherLegalIssuesCondition.HasProvenanceIssues.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_living_identifiable_info')
    if intermediate_values['ContainsLivingIdentifiableInfo']:
        _cond = OtherLegalIssuesCondition.ContainsLivingIdentifiableInfo.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_sensitive_historical_info')
    if intermediate_values['ContainsSensitiveHistoricalInfo']:
        _cond = OtherLegalIssuesCondition.ContainsSensitiveHistoricalInfo.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_totalitarian_associations')
    if intermediate_values['ContainsTotalitarianAssociations']:
        _cond = OtherLegalIssuesCondition.ContainsTotalitarianAssociations.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_discriminatory_content')
    if intermediate_values['ContainsDiscriminatoryContent']:
        _cond = OtherLegalIssuesCondition.ContainsDiscriminatoryContent.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_other_sensitive_content')
    if intermediate_values['ContainsOtherSensitiveContent']:
        _cond = OtherLegalIssuesCondition.ContainsOtherSensitiveContent.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    mark_used('object_other_problems')
    if intermediate_values['HasOtherProblems']:
        _cond = OtherLegalIssuesCondition.HasOtherProblems.value
        results['yellow'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'yellow', 'other_legal_issues'),
        })

    if not results['yellow']:
        _cond = OtherLegalIssuesCondition.NoLegalIssues.value
        results['green'].append({
            'condition': _cond,
            'explanation': get_explanation(_cond, 'green', 'other_legal_issues'),
        })

    return results, used_vars
