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

    # Merge with later functions taking precedence on overlapping keys (e.g., CURRENT_YEAR)
    merged = {}
    merged.update(copyright_intermediate)
    merged.update(performance_intermediate)
    merged.update(phonogram_intermediate)
    merged.update(film_fixation_intermediate)
    merged.update(broadcasts_intermediate)
    return merged

def calculate_results(data, intermediate):
    """Calculate final copyright status results based on intermediate values."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': [],
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
    
    # Expect callers to pass unified intermediate values
    merged_intermediate = intermediate or {}

    # Calculate object copyright status
    object_results, object_used_vars = calculate_object_copyright_status(data, merged_intermediate)
    used_vars.update(object_used_vars)
    
    # Calculate performance rights status
    performance_results, performance_used_vars = calculate_performance_rights_status(data, merged_intermediate)
    used_vars.update(performance_used_vars)
    
    # Calculate phonogram rights status
    phonogram_results, phonogram_used_vars = calculate_phonogram_rights_status(data, merged_intermediate)
    used_vars.update(phonogram_used_vars)
    
    # Calculate film fixation rights status
    film_fixation_results, film_fixation_used_vars = calculate_film_fixation_rights_status(data, merged_intermediate)
    used_vars.update(film_fixation_used_vars)
    
    # Calculate broadcasting organisation rights status
    broadcast_results, broadcast_used_vars = calculate_broadcast_rights_status(data, merged_intermediate)
    used_vars.update(broadcast_used_vars)
    
    # Calculate additional object classification status (NEW)
    additional_classification_results, additional_classification_used_vars = calculate_additional_object_classification_status(data, merged_intermediate)
    used_vars.update(additional_classification_used_vars)
    
    # Calculate first edition protection status (NEW)
    first_edition_results = calculate_first_edition_protection_status(data, merged_intermediate)
    
    # Store object copyright results separately
    results['copyright_status'] = {
        'green': object_results['green'],
        'yellow': object_results['yellow'],
        'red': object_results['red'],
        'info': object_results['info']
    }
    
    # Store additional classification results separately
    results['additional_classification_status'] = {
        'green': additional_classification_results['green'],
        'yellow': additional_classification_results['yellow'],
        'red': additional_classification_results['red'],
        'info': additional_classification_results['info']
    }
    
    # Store first edition results separately
    results['first_edition_status'] = {
        'green': first_edition_results['green'],
        'yellow': first_edition_results['yellow'],
        'red': first_edition_results['red'],
        'info': first_edition_results['info']
    }
    
    # Store performance results separately
    results['performance_status'] = {
        'green': performance_results['green'],
        'yellow': performance_results['yellow'],
        'red': performance_results['red'],
        'info': performance_results['info']
    }
    
    # Store phonogram results separately
    results['phonogram_status'] = {
        'green': phonogram_results['green'],
        'yellow': phonogram_results['yellow'],
        'red': phonogram_results['red'],
        'info': phonogram_results['info']
    }
    
    # Store film fixation results separately
    results['film_fixation_status'] = {
        'green': film_fixation_results['green'],
        'yellow': film_fixation_results['yellow'],
        'red': film_fixation_results['red'],
        'info': film_fixation_results['info']
    }
    
    # Store broadcasting organisation results separately
    results['broadcast_status'] = {
        'green': broadcast_results['green'],
        'yellow': broadcast_results['yellow'],
        'red': broadcast_results['red'],
        'info': broadcast_results['info']
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
    results['debug_info'] = {
        'basic_information': {k: data[k] for k in basic_info_fields if k in data},
        'input_data': {k: v for k, v in data.items() if k not in basic_info_fields},
        'used_variables': list(used_vars),
        'unused_variables': [k for k in data.keys() if k not in used_vars]
    }
    
    return results

def generate_markdown_report(results):
    """Generate a markdown report from the results."""
    
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
    
    if copyright_status['red']:
        md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
        for result in copyright_status['red']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if copyright_status['yellow']:
        md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
        for result in copyright_status['yellow']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if copyright_status['green']:
        md_content.append("\n### ✅ Green status. No issues detected.\n")
        for result in copyright_status['green']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if copyright_status['info']:
        md_content.append("\n### 📝 Informational Messages\n")
        for result in copyright_status['info']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
   
    # Add first edition protection section
    if results.get('first_edition_status'):
        md_content.append("\n## First edition protection / posthumous edition status\n")
        first_edition = results['first_edition_status']
        if first_edition['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in first_edition['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in first_edition['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if first_edition['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
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
        
        if performance_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in performance_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if performance_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in performance_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if performance_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in performance_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if performance_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in performance_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add phonogram rights section
    if results.get('phonogram_status'):
        md_content.append("\n## Phonogram rights status of the object\n")
        
        phonogram_status = results['phonogram_status']
        
        if phonogram_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in phonogram_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if phonogram_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in phonogram_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if phonogram_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in phonogram_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if phonogram_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in phonogram_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add film fixation rights section
    if results.get('film_fixation_status'):
        md_content.append("\n## Film fixation rights status of the object\n")
        
        film_fixation_status = results['film_fixation_status']
        
        if film_fixation_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in film_fixation_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if film_fixation_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in film_fixation_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if film_fixation_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in film_fixation_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if film_fixation_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in film_fixation_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    # Add broadcasting organisation rights section
    if results.get('broadcast_status'):
        md_content.append("\n## Broadcasting organisation rights status of the object\n")
        
        broadcast_status = results['broadcast_status']
        
        if broadcast_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in broadcast_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if broadcast_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in broadcast_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if broadcast_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in broadcast_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if broadcast_status['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in broadcast_status['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

    # Add other IP rights section
    if results.get('additional_classification_status'):
        md_content.append("\n## Other IP rights\n")
        additional_classification = results['additional_classification_status']
        if additional_classification['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in additional_classification['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if additional_classification['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in additional_classification['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if additional_classification['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in additional_classification['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        if additional_classification['info']:
            md_content.append("\n### 📝 Informational Messages\n")
            for result in additional_classification['info']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")

    # Add digital representation status section
    md_content.append("\n## IP status of the digital representation of the object\n")
    
    if results.get('digital_repr_status'):
        digital_status = results['digital_repr_status']
        
        if digital_status['red']:
            md_content.append("\n### ❌ Red status. There are legal obstacles.\n")
            for result in digital_status['red']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if digital_status['yellow']:
            md_content.append("\n### ⚠️ Yellow status. The tool is unable to determine the status.\n")
            for result in digital_status['yellow']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
        
        if digital_status['green']:
            md_content.append("\n### ✅ Green status. No issues detected.\n")
            for result in digital_status['green']:
                md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
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
        content.append("\nYellow status. The tool is unable to determine the status.\n")
        for result in copyright_status['yellow']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if copyright_status['green']:
        content.append("\n✅ Green status. No issues detected.\n")
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
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in first_edition['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if first_edition['green']:
            content.append("\n✅ Green status. No issues detected.\n")
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
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in performance_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if performance_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
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
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in phonogram_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if phonogram_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
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
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in film_fixation_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if film_fixation_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
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
        
        if broadcast_status['red']:
            content.append("\nRed status. There are legal obstacles.\n")
            for result in broadcast_status['red']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if broadcast_status['yellow']:
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in broadcast_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if broadcast_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
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
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in additional_classification['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        if additional_classification['green']:
            content.append("\n✅ Green status. No issues detected.\n")
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
            content.append("\nYellow status. The tool is unable to determine the status.\n")
            for result in digital_status['yellow']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
        
        if digital_status['green']:
            content.append("\n✅ Green status. No issues detected.\n")
            for result in digital_status['green']:
                content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    # Add debug information in JSON format
    if results.get('debug_info'):
        content.append("\n🔍 Source Data (JSON):\n")
        import json
        debug_json = json.dumps(results['debug_info'], indent=2, sort_keys=True, default=str)
        content.append(debug_json)
        content.append("\n")
    
    return "".join(content)