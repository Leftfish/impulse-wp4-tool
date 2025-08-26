"""
Other legal issues module.

This module contains logic for calculating other legal issues status and related intermediate values.
"""


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
    statuses = []
    used_conditions = []
    
    # Check each condition and add YELLOW statuses
    if intermediate_values['HasContractualRestrictions']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'It is necessary to review the agreements pertaining to the use of the work to determine the scope of possible obstacles.'
        })
        used_conditions.append('HasContractualRestrictions')
    
    if intermediate_values['HasAdministrativeRestrictions']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'There may be restrictions stemming from administrative legal regulations.'
        })
        used_conditions.append('HasAdministrativeRestrictions')
    
    if intermediate_values['HasOwnershipIssues']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'Although ownership rights to the physical object are not a restriction to its online use, there may be other legal risks caused by the infringement of such rights by the institution'
        })
        used_conditions.append('HasOwnershipIssues')
    
    if intermediate_values['ProvenanceNotTraced']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'Although uncertain or unknown provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution'
        })
        used_conditions.append('ProvenanceNotTraced')
    
    if intermediate_values['HasProvenanceIssues']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'Although troublesome provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution'
        })
        used_conditions.append('HasProvenanceIssues')
    
    if intermediate_values['ContainsLivingIdentifiableInfo']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'The use of the object may lead to personal data processing, and depending on the exact context, require a legal basis under the General Data Protection Regulation'
        })
        used_conditions.append('ContainsLivingIdentifiableInfo')
    
    if intermediate_values['ContainsSensitiveHistoricalInfo']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'The use of the object may expose the institution to defamation claims or similar liability'
        })
        used_conditions.append('ContainsSensitiveHistoricalInfo')
    
    if intermediate_values['ContainsTotalitarianAssociations']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'The use of the object may expose the institution to liability under hate-speech and similar legal regulations'
        })
        used_conditions.append('ContainsTotalitarianAssociations')
    
    if intermediate_values['ContainsDiscriminatoryContent']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'The use of the object may expose the institution to liability under hate-speech and similar legal regulations'
        })
        used_conditions.append('ContainsDiscriminatoryContent')
    
    if intermediate_values['ContainsOtherSensitiveContent']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'The use of the object may expose the institution to liability on grounds other than IP, personal data protection, personal rights or hate-speech laws'
        })
        used_conditions.append('ContainsOtherSensitiveContent')
    
    if intermediate_values['HasOtherProblems']:
        statuses.append({
            'status': 'YELLOW',
            'explanation': 'There are other legal issues that require verification.'
        })
        used_conditions.append('HasOtherProblems')
    
    # If no YELLOW statuses found, add GREEN status
    if not statuses:
        statuses.append({
            'status': 'GREEN',
            'explanation': 'There seem to be no identified legal issues unrelated to IP, personal data protection, personal rights or hate-speech laws'
        })
        used_conditions.append('NoIssuesFound')
    
    return {
        'statuses': statuses,
        'mark_used': used_conditions
    }
