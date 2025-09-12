from datetime import datetime
from data.country_codes import is_eea_country

# Import from modularized rights calculation modules
from utils_modules.additional_classification import calculate_additional_object_classification_status

from utils_modules.copyright import (
    calculate_intermediate_values_copyright,
    calculate_object_copyright_status,
    calculate_first_edition_protection_status
)
from utils_modules.performance import (
    calculate_intermediate_values_performances,
    calculate_performance_rights_status
)
from utils_modules.phonogram import (
    calculate_intermediate_values_phonograms,
    calculate_phonogram_rights_status
)
from utils_modules.film_fixation import (
    calculate_intermediate_values_film_fixations,
    calculate_film_fixation_rights_status
)
from utils_modules.broadcasting import (
    calculate_intermediate_values_broadcast,
    calculate_broadcast_rights_status
)
from utils_modules.digital_representation import calculate_digital_representation_status

from utils_modules.other_legal_issues import (
    calculate_intermediate_values_other_legal_issues,
    calculate_other_legal_issues_status
)

CURRENT_YEAR = datetime.now().year

def calculate_all_intermediate_values(data):
    """Calculate and return a unified dictionary of intermediate values
    for both copyright and performance calculations.
    """
    copyright_intermediate = calculate_intermediate_values_copyright(data)
    performance_intermediate = calculate_intermediate_values_performances(data)
    phonogram_intermediate = calculate_intermediate_values_phonograms(data)
    film_fixation_intermediate = calculate_intermediate_values_film_fixations(data)
    broadcasts_intermediate = calculate_intermediate_values_broadcast(data)
    other_legal_issues_intermediate = calculate_intermediate_values_other_legal_issues(data)

    # Merge with later functions taking precedence on overlapping keys (e.g., CURRENT_YEAR)
    merged = {}
    merged.update(copyright_intermediate)
    merged.update(performance_intermediate)
    merged.update(phonogram_intermediate)
    merged.update(film_fixation_intermediate)
    merged.update(broadcasts_intermediate)
    merged.update(other_legal_issues_intermediate)
    return merged

def calculate_results(data, intermediate):
    """Calculate final copyright status results based on intermediate values."""
    results = {
        'object_name': data.get('object_name'),
        'institution_name': data.get('institution_name'),
        'copyright_status': None, # Will store object copyright status
        'performance_status': None,  # Will store performance rights status
        'phonogram_status': None,  # Will store phonogram rights status
        'film_fixation_status': None,  # Will store film fixation rights status
        'broadcast_status': None,  # Will store broadcasting organisation rights status
        'digital_repr_status': None,  # Will store digital representation status
        'debug_info': {}  # Add debug info tracking
    }
    
    # Track variable usage
    used_vars = set()

    # Helper function to update the results
    def update_results(issue_name, issue_results):
        results[issue_name] = {
        'green': issue_results.get('green', []),
        'yellow': issue_results.get('yellow', []),
        'red': issue_results.get('red', []),
        'info': issue_results.get('info', []),
        'rights_green': issue_results.get('rights_green', []),
        'rights_yellow': issue_results.get('rights_yellow', [])
        }
    
    # Expect callers to pass unified intermediate values
    merged_intermediate = intermediate or {}

    # Calculate object copyright status
    
    object_copyright_results, object_copyright_used_vars = calculate_object_copyright_status(data, merged_intermediate)
    object_first_edition_results, object_first_edition_used_vars = calculate_first_edition_protection_status(data, merged_intermediate)
    used_vars.update(object_copyright_used_vars)
    used_vars.update(object_first_edition_used_vars)
    
    # Calculate performance rights status
    object_performance_results, object_performance_used_vars = calculate_performance_rights_status(data, merged_intermediate)
    used_vars.update(object_performance_used_vars)
    
    # Calculate phonogram rights status
    object_phonogram_results, object_phonogram_used_vars = calculate_phonogram_rights_status(data, merged_intermediate)
    used_vars.update(object_phonogram_used_vars)
    
    # Calculate film fixation rights status
    object_film_fixation_results, object_film_fixation_used_vars = calculate_film_fixation_rights_status(data, merged_intermediate)
    used_vars.update(object_film_fixation_used_vars)
    
    # Calculate broadcasting organisation rights status
    object_broadcast_results, object_broadcast_used_vars = calculate_broadcast_rights_status(data, merged_intermediate)
    used_vars.update(object_broadcast_used_vars)
    
    # Calculate additional object classification status 
    object_additional_classification_results, object_additional_classification_used_vars = calculate_additional_object_classification_status(data, merged_intermediate)
    used_vars.update(object_additional_classification_used_vars)
    
    # Calculate other legal issues status (NEW)
    other_legal_issues_results, other_legal_issues_used_vars = calculate_other_legal_issues_status(data, merged_intermediate)
    used_vars.update(other_legal_issues_used_vars)

    # Calculate digital representation status
    digital_repr_results, digital_repr_used_vars = calculate_digital_representation_status(data, merged_intermediate)
    used_vars.update(digital_repr_used_vars)
    
    # Store the results
    #update_results('copyright_status', object_copyright_results)
    results['copyright_status'] = object_copyright_results
    results['first_edition_status'] = object_first_edition_results
    results['performance_status'] = object_performance_results
    results['phonogram_status'] = object_phonogram_results
    results['film_fixation_status'] = object_film_fixation_results
    results['broadcast_status'] = object_broadcast_results
    results['additional_classification_status'] = object_additional_classification_results
    results['other_legal_issues_status'] = other_legal_issues_results
    results['digital_repr_status'] = digital_repr_results

    # Prepare debug info
    basic_info_fields = ['object_name', 'institution_name', 'object_url', 'digital_repr_nature']
    other_legal_issues_fields = [
        'object_contractual_restrictions', 'object_administrative_restrictions', 
        'object_ownership_status', 'object_provenance_traced', 'object_provenance_issues',
        'object_living_identifiable_info', 'object_sensitive_historical_info',
        'object_totalitarian_associations', 'object_discriminatory_content',
        'object_other_sensitive_content', 'object_other_problems', 'object_legal_consultation'
    ]
    results['debug_info'] = {
        'basic_information': {k: data[k] for k in basic_info_fields if k in data},
        'other_legal_issues': {k: data[k] for k in other_legal_issues_fields if k in data},
        'input_data': {k: v for k, v in data.items() if k not in basic_info_fields + other_legal_issues_fields},
        'used_variables': list(used_vars),
        'unused_variables': [k for k in data.keys() if k not in used_vars]
    }
    
    return results

def generate_short_report(results):
    """Generate a short summary report from the results."""

    short_report = ''''''
    yellows = []
    reds = []
    for key, status in results.items():
        if isinstance(status, dict):
            if status.get('red', []): 
                reds.append(status['red'][0])
            if status.get('rights_red', []): 
                reds.append(status['rights_red'][0])
            if status.get('yellow', []): 
                yellows.append(status['yellow'][0])
            if status.get('rights_yellow', []): 
                yellows.append(status['rights_yellow'][0])

    if reds:
        short_report += "**❌ Red status. There are legal obstacles to using the object online:** "
        status_codes = []
        for item in reds:
            status_codes.append(item['condition'])
        short_report += f"{'; '.join(status_codes)}"

    elif yellows:
        short_report += "**⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation:** "
        status_codes = []
        for item in yellows:
            status_codes.append(item['condition'])
        short_report += f"{'; '.join(status_codes)}"

    return short_report

def generate_markdown_report(results):
    """Generate a markdown report from the results."""

    def add_statuses_to_md(status, legal_issue_type, md_content):
        if status['info']:
                md_content.append(f"\n##### 📝 Informational Messages: {legal_issue_type}\n")
                for result in status['info']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if not (status['rights_green'] or status['rights_yellow']):
            if status['green']:
                md_content.append(f"\n##### ✅ Green status. No issues caused by {legal_issue_type}\n")
                for result in status['green']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
                #return md_content
            
            if status['red']:
                md_content.append(f"\n##### ❌ Red status. There are legal obstacles caused by {legal_issue_type}.\n")
                for result in status['red']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

            if status['yellow']:
                md_content.append(f"\n##### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation in connection with {legal_issue_type}.\n")
                for result in status['yellow']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            
            
        else:
            md_content.append("\n#### The following legal bases to use the object apply:\n")
            if status['rights_green']:
                md_content.append("\n##### ✅ Green status. The bases below are sufficient to use the object online\n")
                for result in status['rights_green']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            elif status['rights_yellow']:
                md_content.append("\n##### ⚠️ Yellow status. The bases below may be sufficient, but require further investigation.\n")
                for result in status['rights_yellow']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            
            md_content.append(f"\n##### 📝. At the same time, the object is protected by {legal_issue_type} on a following basis:\n")
            for result in status['green'] + status['yellow'] + status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

            
        return md_content
    
    md_content = []
    md_content.append("\n## Short Report\n")
    md_content.append("\nNote: the short report provides a quick, simplified summary. If there are any definite obstacles, it will display only a RED status. If there are no definite obstacles, but at least one problematic issue, it will display a YELLOW status.\n\n\n")
    md_content.append(generate_short_report(results))

    md_content.append("\n## Full Report\n")
    # Add object and institution information
    object_name = results.get('object_name') or "unknown"
    institution_name = results.get('institution_name') or "unknown"
    md_content.extend([
        f"\n**Object:** {object_name}",
        f"\n**Institution:** {institution_name}\n"
    ])
    
    # Add explanation of priority order
    md_content.append("\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n")
    
    # Add copyright status section
    md_content.append("\n### Copyright status of the object\n")

    if results.get('copyright_status'):
        copyright_status = results['copyright_status']
        md_content = add_statuses_to_md(copyright_status, 'copyright', md_content)

    # Add first edition protection section (if applicable)
    if any([len(status) for status in results.get('first_edition_status').values()]):
        md_content.append("\n### First edition protection / posthumous edition status\n")
        first_edition = results['first_edition_status']
        md_content = add_statuses_to_md(first_edition, 'first edition protection', md_content)

    # Add performance rights section
    if results.get('performance_status'):
        md_content.append("\n### Performance rights status of the object\n")
        performance_status = results['performance_status']
        md_content = add_statuses_to_md(performance_status, 'performance rights', md_content)
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        md_content.append("\n### Phonogram rights status of the object\n")        
        phonogram_status = results['phonogram_status']
        md_content = add_statuses_to_md(phonogram_status, 'phonogram rights', md_content)

    # Add film fixation rights section
    if results.get('film_fixation_status'):
        md_content.append("\n### Film fixation rights status of the object\n")        
        film_fixation_status = results['film_fixation_status']
        md_content = add_statuses_to_md(film_fixation_status, 'film fixation rights', md_content)

    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        broadcast_status = results['broadcast_status']
        md_content.append("\n### Broadcasting organisation rights status of the object\n")
        md_content = add_statuses_to_md(broadcast_status, 'broadcasting organisation rights', md_content)

    # Add other IP rights section
    if results.get('additional_classification_status'):
        md_content.append("\n### Other IP rights\n")
        additional_classification = results['additional_classification_status']
        md_content = add_statuses_to_md(additional_classification, 'additional classification rights', md_content)

    # Add digital representation status section
    if results.get('digital_repr_status'):
        md_content.append("\n### IP status of the digital representation of the object\n")
        digital_representation_status = results['digital_repr_status']
        #print(digital_representation_status)
        md_content = add_statuses_to_md(digital_representation_status, f'rights to the digital representation of the object', md_content)
    
    # Add other legal issues section
    if results.get('other_legal_issues_status'):
        md_content.append("\n### Other legal issues\n")
        other_legal_issues_status = results['other_legal_issues_status']
        add_statuses_to_md(other_legal_issues_status, 'other legal issues (unrelated to IP)', md_content)

    # Add debug information
    if results.get('debug_info'):
        md_content.append("\n#### 🔍 Source data (JSON)\n")
        md_content.append("```json\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        md_content.append(debug_json)
        md_content.append("\n```\n")
    
    return "".join(md_content)

def generate_text_report(results):
    """Generate a plain text report from the results."""

    def add_statuses_to_txt(status, legal_issue_type, txt_content):
        if status['info']:
                txt_content.append(f"\nInformational Messages: {legal_issue_type}\n")
                for result in status['info']:
                    txt_content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if not (status['rights_green'] or status['rights_yellow']):
            if status['green']:
                txt_content.append(f"\nGreen status. No issues caused by {legal_issue_type}\n")
                for result in status['green']:
                    txt_content.append(f"- {result['condition']}: {result['explanation']}\n")
                #return txt_content
            
            if status['red']:
                txt_content.append(f"\nRed status. There are legal obstacles caused by {legal_issue_type}.\n")
                for result in status['red']:
                    txt_content.append(f"- {result['condition']}: {result['explanation']}\n")

            if status['yellow']:
                txt_content.append(f"\nYellow status. There is either insufficient data or the nature of the issue requires further investigation in connection with {legal_issue_type}.\n")
                for result in status['yellow']:
                    txt_content.append(f"- {result['condition']}: {result['explanation']}\n")
            
            
        else:
            txt_content.append("\nThe following legal bases to use the object apply:\n")
            if status['rights_green']:
                txt_content.append("\nGreen status. The bases below are sufficient to use the object online\n")
                for result in status['rights_green']:
                    txt_content.append(f"- {result['condition']}: {result['explanation']}\n")
            elif status['rights_yellow']:
                txt_content.append("\nYellow status. The bases below may be sufficient, but require further investigation.\n")
                for result in status['rights_yellow']:
                    txt_content.append(f"- {result['condition']}: {result['explanation']}\n")
            
            txt_content.append(f"\nAt the same time, the object is protected by {legal_issue_type} on a following basis:\n")
            for result in status['green'] + status['yellow'] + status['red']:
                txt_content.append(f"- {result['condition']}: {result['explanation']}\n")

            
        return txt_content
    
    txt_content = ["Report\n"]
    
    # Add object and institution information
    object_name = results.get('object_name') or "unknown"
    institution_name = results.get('institution_name') or "unknown"
    txt_content.extend([
        f"\nObject: {object_name}",
        f"\nInstitution: {institution_name}\n"
    ])
    
    # Add explanation of priority order
    txt_content.append("\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n")
    
    # Add copyright status section
    txt_content.append("\nCopyright status of the object\n")

    if results.get('copyright_status'):
        copyright_status = results['copyright_status']
        txt_content = add_statuses_to_txt(copyright_status, 'copyright', txt_content)

    # Add first edition protection section (if applicable)
    if any([len(status) for status in results.get('first_edition_status').values()]):
        txt_content.append("\nFirst edition protection / posthumous edition status\n")
        first_edition = results['first_edition_status']
        txt_content = add_statuses_to_txt(first_edition, 'first edition protection', txt_content)

    # Add performance rights section
    if results.get('performance_status'):
        txt_content.append("\nPerformance rights status of the object\n")
        performance_status = results['performance_status']
        txt_content = add_statuses_to_txt(performance_status, 'performance rights', txt_content)
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        txt_content.append("\nPhonogram rights status of the object\n")        
        phonogram_status = results['phonogram_status']
        txt_content = add_statuses_to_txt(phonogram_status, 'phonogram rights', txt_content)

    # Add film fixation rights section
    if results.get('film_fixation_status'):
        txt_content.append("\nFilm fixation rights status of the object\n")        
        film_fixation_status = results['film_fixation_status']
        txt_content = add_statuses_to_txt(film_fixation_status, 'film fixation rights', txt_content)

    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        broadcast_status = results['broadcast_status']
        txt_content.append("\nBroadcasting organisation rights status of the object\n")
        txt_content = add_statuses_to_txt(broadcast_status, 'broadcasting organisation rights', txt_content)

    # Add other IP rights section
    if results.get('additional_classification_status'):
        txt_content.append("\nOther IP rights\n")
        additional_classification = results['additional_classification_status']
        txt_content = add_statuses_to_txt(additional_classification, 'additional classification rights', txt_content)

    # Add digital representation status section
    if results.get('digital_repr_status'):
        txt_content.append("\nIP status of the digital representation of the object\n")
        digital_representation_status = results['digital_repr_status']
        #print(digital_representation_status)
        txt_content = add_statuses_to_txt(digital_representation_status, f'rights to the digital representation of the object', txt_content)
    
    # Add other legal issues section
    if results.get('other_legal_issues_status'):
        txt_content.append("\nOther legal issues\n")
        other_legal_issues_status = results['other_legal_issues_status']
        add_statuses_to_txt(other_legal_issues_status, 'other legal issues (unrelated to IP)', txt_content)

    # Add debug information
    if results.get('debug_info'):
        txt_content.append("\nSource data (JSON)\n")
        txt_content.append("\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        txt_content.append(debug_json)
        txt_content.append("\n")
    
    return "".join(txt_content)