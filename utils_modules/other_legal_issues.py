"""
Other legal issues module.

This module contains logic for calculating other legal issues status and related intermediate values.
"""

from defaults import ResultsDict

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
        results['yellow'].append({
            'condition': 'HasContractualRestrictions',
            'explanation': 'It is necessary to review the agreements pertaining to the use of the work to determine the scope of possible obstacles.'
        })

    mark_used('object_administrative_restrictions')
    if intermediate_values['HasAdministrativeRestrictions']:
        results['yellow'].append({
            'condition': 'HasAdministrativeRestrictions',
            'explanation': 'There may be restrictions stemming from administrative legal regulations.'
        })

    mark_used('object_ownership_status')
    if intermediate_values['HasOwnershipIssues']:
        results['yellow'].append({
            'condition': 'HasOwnershipIssues',
            'explanation': 'Although ownership rights to the physical object are not a restriction to its online use, there may be other legal risks caused by the infringement of such rights by the institution'
        })

    mark_used('object_provenance_traced')
    if intermediate_values['ProvenanceNotTraced']:
        results['yellow'].append({
            'condition': 'ProvenanceNotTraced',
            'explanation': 'Although uncertain or unknown provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution'
        })

    mark_used('object_provenance_issues')
    if intermediate_values['HasProvenanceIssues']:
        results['yellow'].append({
            'condition': 'HasProvenanceIssues',
            'explanation': 'Although troublesome provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution'
        })

    mark_used('object_living_identifiable_info')
    if intermediate_values['ContainsLivingIdentifiableInfo']:
        results['yellow'].append({
            'condition': 'ContainsLivingIdentifiableInfo',
            'explanation': 'The use of the object may lead to personal data processing, and depending on the exact context, require a legal basis under the General Data Protection Regulation'
        })

    mark_used('object_sensitive_historical_info')
    if intermediate_values['ContainsSensitiveHistoricalInfo']:
        results['yellow'].append({
            'condition': 'ContainsSensitiveHistoricalInfo',
            'explanation': 'The use of the object may expose the institution to defamation claims or similar liability'
        })

    mark_used('object_totalitarian_associations')
    if intermediate_values['ContainsTotalitarianAssociations']:
        results['yellow'].append({
            'condition': 'ContainsTotalitarianAssociations',
            'explanation': 'The use of the object may expose the institution to liability under hate-speech and similar legal regulations'
        })

    mark_used('object_discriminatory_content')
    if intermediate_values['ContainsDiscriminatoryContent']:
        results['yellow'].append({
            'condition': 'ContainsDiscriminatoryContent',
            'explanation': 'The use of the object may expose the institution to liability under hate-speech and similar legal regulations'
        })

    mark_used('object_other_sensitive_content')
    if intermediate_values['ContainsOtherSensitiveContent']:
        results['yellow'].append({
            'condition': 'ContainsOtherSensitiveContent',
            'explanation': 'The use of the object may expose the institution to liability on grounds other than IP, personal data protection, personal rights or hate-speech laws'
        })

    mark_used('object_other_problems')
    if intermediate_values['HasOtherProblems']:
        results['yellow'].append({
            'condition': 'HasOtherProblems',
            'explanation': 'There are other legal issues that require verification.'
        })

    if not results['yellow']:
        results['green'].append({
            'condition': 'NoLegalIssues',
            'explanation': 'No legal issues unrelated to intellectual property found.'
        })

    return results, used_vars
