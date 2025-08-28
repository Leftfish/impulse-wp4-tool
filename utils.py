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
    
    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)

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
    object_copyright_results, object_used_vars = calculate_object_copyright_status(data, merged_intermediate)
    used_vars.update(object_used_vars)
    
    # Calculate performance rights status
    object_performance_results, performance_used_vars = calculate_performance_rights_status(data, merged_intermediate)
    used_vars.update(performance_used_vars)
    
    # Calculate phonogram rights status
    object_phonogram_results, phonogram_used_vars = calculate_phonogram_rights_status(data, merged_intermediate)
    used_vars.update(phonogram_used_vars)
    
    # Calculate film fixation rights status
    object_film_fixation_results, film_fixation_used_vars = calculate_film_fixation_rights_status(data, merged_intermediate)
    used_vars.update(film_fixation_used_vars)
    
    # Calculate broadcasting organisation rights status
    object_broadcast_results, broadcast_used_vars = calculate_broadcast_rights_status(data, merged_intermediate)
    used_vars.update(broadcast_used_vars)
    
    # Calculate additional object classification status (NEW)
    object_additional_classification_results, additional_classification_used_vars = calculate_additional_object_classification_status(data, merged_intermediate)
    used_vars.update(additional_classification_used_vars)
    
    # Calculate other legal issues status (NEW)
    other_legal_issues_results = calculate_other_legal_issues_status(data, merged_intermediate)
    
    # Calculate first edition protection status (NEW)
    object_first_edition_results = calculate_first_edition_protection_status(data, merged_intermediate)
    
    # Store object copyright results separately
    update_results('copyright_status', object_copyright_results)

    # Store additional classification results separately
    update_results('additional_classification_status', object_additional_classification_results)
    
    # Store first edition results separately
    update_results('first_edition_status', object_first_edition_results)
    
    # Store performance results separately
    update_results('performance_status', object_performance_results)
   
     # Store phonogram results separately
    update_results('phonogram_status', object_phonogram_results)
    
    # Store film fixation results separately
    update_results('film_fixation_status', object_film_fixation_results)
      
    # Store broadcasting organisation results separately
    update_results('broadcast_status', object_broadcast_results)
    
    # Store other legal issues results separately
    results['other_legal_issues_status'] = {
        'statuses': other_legal_issues_results['statuses'],
        'mark_used': other_legal_issues_results['mark_used']
    }
    
    # Calculate digital representation status
    if 'digital_repr_ip_rights' in data:
        mark_used('digital_repr_ip_rights')
        mark_used('digital_repr_ip_rights_acquired')
        mark_used('digital_repr_rights_availability')  # Mark this as used too
        
        # Create a mock object that matches the structure expected by calculate_digital_representation_status
        class MockField:
            def __init__(self, data):
                self.data = data

        class MockDigitalReprIPRights:
            def __init__(self, rights_dict):
                self.copyright = MockField(rights_dict.get('copyright', 'not_applicable'))
                self.audio_recording_rights = MockField(rights_dict.get('audio_recording_rights', 'not_applicable'))
                self.film_fixation_rights = MockField(rights_dict.get('film_fixation_rights', 'not_applicable'))
                self.performance_rights = MockField(rights_dict.get('performance_rights', 'not_applicable'))
                self.other_ip_rights = MockField(rights_dict.get('other_ip_rights', 'not_applicable'))

        mock_rights = MockDigitalReprIPRights(data['digital_repr_ip_rights'])
        
        # Create mock objects for both acquired rights and availability
        mock_rights_acquired = None
        if 'digital_repr_ip_rights_acquired' in data:
            mock_rights_acquired = MockDigitalReprIPRights(data['digital_repr_ip_rights_acquired'])
            
        mock_rights_availability = None
        if 'digital_repr_rights_availability' in data:
            mock_rights_availability = MockDigitalReprIPRights(data['digital_repr_rights_availability'])
        
        results['digital_repr_status'] = calculate_digital_representation_status(
            mock_rights,
            mock_rights_acquired,
            mock_rights_availability
        )
    
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

def generate_markdown_report(results):
    """Generate a markdown report from the results."""

    def add_statuses_to_md(status, legal_issue_type, md_content):
        if not (status['rights_green'] or status['rights_yellow']):
            if status['red']:
                md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
                for result in status['red']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            if status['yellow']:
                md_content.append("\n### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
                for result in status['yellow']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            if status['green']:
                md_content.append("\n### ✅ Green status.\n")
                for result in status['green']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            if status['info']:
                md_content.append("\n### 📝 Informational Messages\n")
                for result in status['info']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        else:
            md_content.append(f"\n#### 📝. The object in question is protected by {legal_issue_type} on a following basis:\n")
            for result in status['green'] + status['yellow'] + status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

            md_content.append("\n#### However, the following legal bases to use it apply:\n")
            if status['rights_green']:
                md_content.append("\n#### ✅ Green status.\n")
                for result in status['rights_green']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
            elif status['rights_yellow']:
                md_content.append("\n#### ⚠️ Yellow status. There are issues that require further investigation.\n")
                for result in status['rights_yellow']:
                    md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    md_content = ["# Report\n"]
    
    # Add object and institution information
    object_name = results.get('object_name') or "unknown"
    institution_name = results.get('institution_name') or "unknown"
    md_content.extend([
        f"\n**Object:** {object_name}",
        f"\n**Institution:** {institution_name}\n"
    ])
    
    # Add explanation of priority order
    md_content.append("\n> Note: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n")
    
    # Add copyright status section
    md_content.append("\n## Copyright status of the object\n")

    copyright_status = results['copyright_status']
    add_statuses_to_md(copyright_status, 'copyright', md_content)

    # Add first edition protection section (if applicable)
    if any([len(status) for status in results.get('first_edition_status').values()]):
        md_content.append("\n## First edition protection / posthumous edition status\n")
        first_edition = results['first_edition_status']
        
        if first_edition['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in first_edition['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['yellow']:
            md_content.append("\n### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in first_edition['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['green']:
            md_content.append("\n### ✅ Green status.\n")
            for result in first_edition['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in first_edition['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

    # Add performance rights section
    if results.get('performance_status'):
        md_content.append("\n## Performance rights status of the object\n")
        performance_status = results['performance_status']
        add_statuses_to_md(performance_status, 'performance rights', md_content)
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        md_content.append("\n## Phonogram rights status of the object\n")        
        phonogram_status = results['phonogram_status']
        add_statuses_to_md(phonogram_status, 'phonogram rights', md_content)

    # Add film fixation rights section
    if results.get('film_fixation_status'):
        md_content.append("\n## Film fixation rights status of the object\n")        
        film_fixation_status = results['film_fixation_status']
        add_statuses_to_md(film_fixation_status, 'film fixation rights', md_content)

    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        broadcast_status = results['broadcast_status']
        md_content.append("\n## Broadcasting organisation rights status of the object\n")
        add_statuses_to_md(broadcast_status, 'broadcasting organisation rights', md_content)

    # Add other IP rights section
    if results.get('additional_classification_status'):
        md_content.append("\n## Other IP rights\n")
        additional_classification = results['additional_classification_status']
        add_statuses_to_md(additional_classification, 'additional classification rights', md_content)

    # Add digital representation status section
    md_content.append("\n## IP status of the digital representation of the object\n")
    
    if results.get('digital_repr_status'):
        digital_status = results['digital_repr_status']
        
        if digital_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in digital_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if digital_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in digital_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if digital_status['green']:
            md_content.append("\n### ✅ Green status.\n")
            for result in digital_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add other legal issues section
    if results.get('other_legal_issues_status'):
        md_content.append("\n## Other legal issues\n")
        
        other_legal_issues_status = results['other_legal_issues_status']
        statuses = other_legal_issues_status['statuses']
        
        # Group statuses by type
        red_statuses = [s for s in statuses if s['status'] == 'RED']
        yellow_statuses = [s for s in statuses if s['status'] == 'YELLOW']
        green_statuses = [s for s in statuses if s['status'] == 'GREEN']
        
        if red_statuses:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in red_statuses:
                md_content.append(f"- {result['explanation']}\n")
        
        if yellow_statuses:
            md_content.append("\n### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in yellow_statuses:
                md_content.append(f"- {result['explanation']}\n")
        
        if green_statuses:
            md_content.append("\n### ✅ Green status.\n")
            for result in green_statuses:
                md_content.append(f"- {result['explanation']}\n")
    
    # Add debug information
    if results.get('debug_info'):
        md_content.append("\n## 🔍 Source data (JSON)\n")
        md_content.append("```json\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        md_content.append(debug_json)
        md_content.append("\n```\n")
    
    return "".join(md_content)

def generate_text_report(results):
    """Generate a plain text report from the results."""
    
    content = ["Report\n"]
    
    # Add object and institution information
    object_name = results.get('object_name') or "unknown"
    institution_name = results.get('institution_name') or "unknown"
    content.extend([
        f"\nObject: {object_name}",
        f"\nInstitution: {institution_name}\n"
    ])
    
    # Add explanation of priority order
    content.append("\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n")
    
    # Add copyright status section
    content.append("\nCopyright status of the object\n")
    content.append("=" * 30 + "\n")
    
    copyright_status = results['copyright_status']

    if copyright_status['red']:
        content.append("\nRed status. There are legal obstacles.\n")
        for result in copyright_status['red']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if copyright_status['yellow']:
        content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
        for result in copyright_status['yellow']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if copyright_status['green']:
        content.append("\n✅ Green status.\n")
        for result in copyright_status['green']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if copyright_status['info']:
        content.append("\nInformational Messages\n")
        for result in copyright_status['info']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")

    # Add first edition protection section
    if results.get('first_edition_status'):
        content.append("\nFirst edition protection / posthumous edition status\n")
        content.append("=" * 30 + "\n")
        first_edition = results['first_edition_status']
        if first_edition['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in first_edition['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['yellow']:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in first_edition['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['green']:
            content.append("\n✅ Green status.\n")
            for result in first_edition['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['info']:
            content.append("\nInformational Messages\n")
            for result in first_edition['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")

    # Add performance rights section
    if results.get('performance_status'):
        content.append("\nPerformance rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        performance_status = results['performance_status']
        
        if performance_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in performance_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['yellow']:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in performance_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['green']:
            content.append("\n✅ Green status.\n")
            for result in performance_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['info']:
            content.append("\nInformational Messages\n")
            for result in performance_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        content.append("\nPhonogram rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        phonogram_status = results['phonogram_status']

        if phonogram_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in phonogram_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['yellow']:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in phonogram_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['green']:
            content.append("\n✅ Green status.\n")
            for result in phonogram_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['info']:
            content.append("\nInformational Messages\n")
            for result in phonogram_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add film fixation rights section
    if results.get('film_fixation_status'):
        content.append("\nFilm fixation rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        film_fixation_status = results['film_fixation_status']
        
        if film_fixation_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in film_fixation_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['yellow']:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in film_fixation_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['green']:
            content.append("\n✅ Green status.\n")
            for result in film_fixation_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['info']:
            content.append("\nInformational Messages\n")
            for result in film_fixation_status['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        content.append("\nBroadcasting organisation rights status of the object\n")
        content.append("=" * 30 + "\n")
        
        broadcast_status = results['broadcast_status']
        
        if True: #not broadcast_status['rights_green'] and not broadcast_status['rights_yellow']:
            if broadcast_status['red']:
                content.append("\nRed status. There are legal obstacles.\n")
                for result in broadcast_status['red']:
                    content.append(f"- {result['condition']}: {result['explanation']}\n")
            
            if broadcast_status['yellow']:
                content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
                for result in broadcast_status['yellow']:
                    content.append(f"- {result['condition']}: {result['explanation']}\n")
            
            if broadcast_status['green']:
                content.append("\n✅ Green status.\n")
                for result in broadcast_status['green']:
                    content.append(f"- {result['condition']}: {result['explanation']}\n")
            
            if broadcast_status['info']:
                content.append("\nInformational Messages\n")
                for result in broadcast_status['info']:
                    content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add other IP rights section
    if results.get('other_ip_rights_status'):
        content.append("\nOther IP rights\n")
        content.append("=" * 30 + "\n")
        additional_classification = results['additional_classification_status']
        if additional_classification['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in additional_classification['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['yellow']:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in additional_classification['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['green']:
            content.append("\n✅ Green status.\n")
            for result in additional_classification['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['info']:
            content.append("\nInformational Messages\n")
            for result in additional_classification['info']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")


# Add digital representation status section
    content.append("\nIP status of the digital representation of the object\n")
    content.append("=" * 30 + "\n")
    
    if results.get('digital_repr_status'):
        digital_status = results['digital_repr_status']
        
        if digital_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in digital_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if digital_status['yellow']:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in digital_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if digital_status['green']:
            content.append("\n✅ Green status.\n")
            for result in digital_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add other legal issues section
    if results.get('other_legal_issues_status'):
        content.append("\nOther legal issues\n")
        content.append("=" * 30 + "\n")
        
        other_legal_issues_status = results['other_legal_issues_status']
        statuses = other_legal_issues_status['statuses']
        
        # Group statuses by type
        red_statuses = [s for s in statuses if s['status'] == 'RED']
        yellow_statuses = [s for s in statuses if s['status'] == 'YELLOW']
        green_statuses = [s for s in statuses if s['status'] == 'GREEN']
        
        if red_statuses:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in red_statuses:
                content.append(f"- {result['explanation']}\n")
        
        if yellow_statuses:
            content.append("\nYellow status. There is either insufficient data or the nature of the issue requires further investigation.\n")
            for result in yellow_statuses:
                content.append(f"- {result['explanation']}\n")
        
        if green_statuses:
            content.append("\n✅ Green status.\n")
            for result in green_statuses:
                content.append(f"- {result['explanation']}\n")
    
    # Add debug information in JSON format
    if results.get('debug_info'):
        content.append("\n🔍 Source Data (JSON):\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        content.append(debug_json)
        content.append("\n")
    
    return "".join(content)