import json
from typing import Dict, List, TypedDict, Any
from constants import APP_VERSION

# Constants used for rendering
MD_SHORT_RED = "**❌ Red status. There are legal obstacles to using the object online:** "
MD_SHORT_YELLOW = "**⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation:** "
MD_SHORT_GREEN = "**✅ Green status. There are no legal obstacles to using the object online.**"

MD_NOTE_SHORT = (
    "\nNote: the short report provides a quick, simplified summary. If there are any definite obstacles, it will display only a RED status. If there are no definite obstacles, but at least one problematic issue, it will display a YELLOW status. Otherwise, the status will be GREEN.\n\n\n"
)

MD_NOTE_PRIORITY = (
    "\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n"
)

TXT_NOTE_PRIORITY = (
    "\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n"
)

_MD_FMT = {
    "info_heading": "\n###### 📝 Informational Messages: {t}\n",
    "green_heading": "\n###### ✅ Green status. No issues caused by {t}\n",
    "red_heading": "\n###### ❌ Red status. There are legal obstacles caused by {t}.\n",
    "yellow_heading": "\n###### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation in connection with {t}.\n",
    "rights_preamble": "\n##### The following legal bases to use the object apply:\n",
    "rights_green_heading": "\n###### ✅ Green status. The bases below are sufficient to use the object online\n",
    "rights_yellow_heading": "\n###### ⚠️ Yellow status. The bases below may be sufficient, but require further investigation.\n",
    "atsame_heading": "\n###### 📝 At the same time, protection under {t} applies:\n",
    "item": "- **{cond}**: {expl}\n",
}

_TXT_FMT = {
    "info_heading": "\nInformational Messages: {t}\n",
    "green_heading": "\nGreen status. No issues caused by {t}\n",
    "red_heading": "\nRed status. There are legal obstacles caused by {t}.\n",
    "yellow_heading": "\nYellow status. There is either insufficient data or the nature of the issue requires further investigation in connection with {t}.\n",
    "rights_preamble": "\nThe following legal bases to use the object apply:\n",
    "rights_green_heading": "\nGreen status. The bases below are sufficient to use the object online\n",
    "rights_yellow_heading": "\nYellow status. The bases below may be sufficient, but require further investigation.\n",
    "atsame_heading": "\nAt the same time, the object is protected by {t} on a following basis:\n",
    "item": "- {cond}: {expl}\n",
}

# Guard helpers
def has_copyright(results: Dict[str, Any]) -> bool:
    return bool(results.get("copyright_status"))


def has_first_edition_content(results: Dict[str, Any]) -> bool:
    return any([len(status) for status in results.get("first_edition_status").values()])


def has_performance(results: Dict[str, Any]) -> bool:
    return bool(results.get("performance_status"))


def has_phonogram(results: Dict[str, Any]) -> bool:
    return bool(results.get("phonogram_status"))


def has_film_fixation(results: Dict[str, Any]) -> bool:
    return bool(results.get("film_fixation_status"))


def has_broadcast(results: Dict[str, Any]) -> bool:
    return bool(results.get("broadcast_status"))


def has_other_ip_rights(results: Dict[str, Any]) -> bool:
    return bool(results.get("other_ip_rights_status"))


def has_digital_repr(results: Dict[str, Any]) -> bool:
    return bool(results.get("digital_repr_status"))


def has_other_legal_issues(results: Dict[str, Any]) -> bool:
    return bool(results.get("other_legal_issues_status"))


# Section declarations (order matters)
_SECTIONS = [
    {
        "key": "copyright_status",
        "md_heading": "\n### Copyright status of the object\n",
        "txt_heading": "\nCopyright status of the object\n",
        "issue_type": "copyright",
        "guard": has_copyright,
    },
    {
        "key": "first_edition_status",
        "md_heading": "\n### First edition protection / posthumous edition status\n",
        "txt_heading": "\nFirst edition protection / posthumous edition status\n",
        "issue_type": "first edition protection",
        # original guard: any([len(status) for status in results.get("first_edition_status").values()])
        "guard": has_first_edition_content,
    },
    {
        "key": "performance_status",
        "md_heading": "\n### Performance rights status of the object\n",
        "txt_heading": "\nPerformance rights status of the object\n",
        "issue_type": "performance rights",
        "guard": has_performance,
    },
    {
        "key": "phonogram_status",
        "md_heading": "\n### Phonogram rights status of the object\n",
        "txt_heading": "\nPhonogram rights status of the object\n",
        "issue_type": "phonogram rights",
        "guard": has_phonogram,
    },
    {
        "key": "film_fixation_status",
        "md_heading": "\n### Film fixation rights status of the object\n",
        "txt_heading": "\nFilm fixation rights status of the object\n",
        "issue_type": "film fixation rights",
        "guard": has_film_fixation,
    },
    {
        "key": "broadcast_status",
        "md_heading": "\n### Broadcasting organisation rights status of the object\n",
        "txt_heading": "\nBroadcasting organisation rights status of the object\n",
        "issue_type": "broadcasting organisation rights",
        "guard": has_broadcast,
    },
    {
        "key": "other_ip_rights_status",
        "md_heading": "\n### Other IP rights\n",
        "txt_heading": "\nOther IP rights\n",
        "issue_type": "additional classification rights",
        "guard": has_other_ip_rights,
    },
    {
        "key": "digital_repr_status",
        "md_heading": "\n### IP status of the digital representation of the object\n",
        "txt_heading": "\nIP status of the digital representation of the object\n",
        "issue_type": "rights to the digital representation of the object",
        "guard": has_digital_repr,
        "is_digital_repr": True,  # Flag to indicate this needs subheadings
    },
    {
        "key": "other_legal_issues_status",
        "md_heading": "\n### Other legal issues\n",
        "txt_heading": "\nOther legal issues\n",
        "issue_type": "other legal issues (unrelated to IP)",
        "guard": has_other_legal_issues,
    },
]


class StatusEntry(TypedDict):
    condition: str
    explanation: str


class StatusDict(TypedDict):
    info: List[StatusEntry]
    green: List[StatusEntry]
    yellow: List[StatusEntry]
    red: List[StatusEntry]
    rights_green: List[StatusEntry]
    rights_yellow: List[StatusEntry]


def _filter_status_by_prefix(status: StatusDict, condition_prefix: str) -> StatusDict:
    """Filter a status dict to only include entries matching the condition prefix."""
    def matches_prefix(entry: StatusEntry) -> bool:
        condition = entry["condition"]
        # Direct prefix match
        if condition.startswith(condition_prefix):
            return True
        # Special handling for Article14CDSM conditions
        if condition_prefix == "DigitalRepresentationPhonogram" and condition == "Article14CDSMPhonogram":
            return True
        if condition_prefix == "DigitalRepresentationFilmFixation" and condition == "Article14CDSMFilmFixation":
            return True
        if condition_prefix == "DigitalRepresentationOtherIP" and condition == "Article14CDSMOtherIP":
            return True
        return False
    
    return {
        "info": [e for e in status.get("info", []) if matches_prefix(e)],
        "green": [e for e in status.get("green", []) if matches_prefix(e)],
        "yellow": [e for e in status.get("yellow", []) if matches_prefix(e)],
        "red": [e for e in status.get("red", []) if matches_prefix(e)],
        "rights_green": [e for e in status.get("rights_green", []) if matches_prefix(e)],
        "rights_yellow": [e for e in status.get("rights_yellow", []) if matches_prefix(e)],
    }


def _render_status(status: StatusDict, legal_issue_type: str, out_list: List[str], fmt: Dict[str, str]) -> List[str]:
    if status["info"]:
        out_list.append(fmt["info_heading"].format(t=legal_issue_type))
        for result in status["info"]:
            out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))

    if not (status["rights_green"] or status["rights_yellow"]):
        if status["green"]:
            out_list.append(fmt["green_heading"].format(t=legal_issue_type))
            for result in status["green"]:
                out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))

        if status["red"]:
            out_list.append(fmt["red_heading"].format(t=legal_issue_type))
            for result in status["red"]:
                out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))

        if status["yellow"]:
            out_list.append(fmt["yellow_heading"].format(t=legal_issue_type))
            for result in status["yellow"]:
                out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))
    else:
        out_list.append(fmt["rights_preamble"]) 
        if status["rights_green"]:
            out_list.append(fmt["rights_green_heading"])
            for result in status["rights_green"]:
                out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))
        elif status["rights_yellow"]:
            out_list.append(fmt["rights_yellow_heading"])
            for result in status["rights_yellow"]:
                out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))

        out_list.append(fmt["atsame_heading"].format(t=legal_issue_type))
        for result in status["green"] + status["yellow"] + status["red"]:
            out_list.append(fmt["item"].format(cond=result["condition"], expl=result["explanation"]))

    return out_list


def generate_short_report(results: Dict[str, Any]):
    """Generate a short summary report from the results.

    Invariants:
    - RED takes precedence over YELLOW; if any definite obstacle exists, report RED only.
    - If no RED but any YELLOW (without applicable rights_green), report YELLOW.
    - Otherwise report GREEN.
    - Texts are preserved exactly; do not normalize whitespace/emojis.
    """

    def _get_condition_prefix(condition_name: str) -> str:
        """Extract the IP right type prefix from a digital representation condition name."""
        for prefix in ["DigitalRepresentationCopyright", "DigitalRepresentationPhonogram", 
                      "DigitalRepresentationFilmFixation", "DigitalRepresentationOtherIP"]:
            if condition_name.startswith(prefix):
                return prefix
        return None

    def _collect_short_statuses(res: Dict[str, Any]):
        yellows_local = []
        reds_local = []
        for status_key, status in res.items():
            if isinstance(status, dict):
                # Check if this is digital representation (needs per-right-type checking)
                is_digital_repr = status_key == "digital_repr_status"
                
                # Handle red statuses: per-right-type for digital_repr, global for others
                if status.get("red", []):
                    if is_digital_repr:
                        # For digital representation: check each red entry individually
                        # against matching rights_green/rights_yellow for the same IP right type
                        rights_green_list = status.get("rights_green", [])
                        rights_yellow_list = status.get("rights_yellow", [])
                        for red_entry in status["red"]:
                            red_condition = red_entry["condition"]
                            condition_prefix = _get_condition_prefix(red_condition)
                            
                            # Check if there's a matching rights_green or rights_yellow for the same IP right type
                            has_matching_rights = False
                            if condition_prefix:
                                has_matching_rights = any(
                                    green_entry["condition"].startswith(condition_prefix)
                                    for green_entry in rights_green_list
                                ) or any(
                                    yellow_entry["condition"].startswith(condition_prefix)
                                    for yellow_entry in rights_yellow_list
                                )
                            
                            # Only include this red if there's no matching rights for the same IP right
                            if not has_matching_rights:
                                reds_local.append(red_entry)
                    else:
                        # For other sections: global check (existing logic)
                        if not (status.get("rights_green", []) or status.get("rights_yellow", [])):
                            reds_local.extend(status["red"])
                
                if status.get("rights_red", []) and not (
                    status.get("rights_green", []) or status.get("rights_yellow", [])
                ):
                        reds_local.extend(status["rights_red"])
                
                if status.get("yellow", []) and not (status.get("rights_green", [])):
                        yellows_local.extend(status["yellow"])
                
                # Handle rights_yellow: per-right-type for digital_repr, global for others
                if status.get("rights_yellow", []):
                    if is_digital_repr:
                        # For digital representation: check each rights_yellow individually
                        # against matching rights_green for the same IP right type
                        rights_green_list = status.get("rights_green", [])
                        for yellow_entry in status["rights_yellow"]:
                            yellow_condition = yellow_entry["condition"]
                            condition_prefix = _get_condition_prefix(yellow_condition)
                            
                            # Check if there's a matching rights_green for the same IP right type
                            has_matching_rights_green = False
                            if condition_prefix:
                                has_matching_rights_green = any(
                                    green_entry["condition"].startswith(condition_prefix)
                                    for green_entry in rights_green_list
                                )
                            
                            # Only include this yellow if there's no matching green for the same IP right
                            if not has_matching_rights_green:
                                yellows_local.append(yellow_entry)
                    else:
                        # For other sections: global check (existing logic)
                        if not status.get("rights_green", []):
                            yellows_local.extend(status["rights_yellow"])
        return reds_local, yellows_local

    short_report = """"""
    reds, yellows = _collect_short_statuses(results)

    if reds:
        short_report += MD_SHORT_RED
        status_codes = []
        for item in reds:
            status_codes.append(item["condition"])
        short_report += f"{'; '.join(status_codes)}"

    elif yellows:
        short_report += MD_SHORT_YELLOW
        status_codes = []
        for item in yellows:
            status_codes.append(item["condition"])
        short_report += f"{'; '.join(status_codes)}"

    else:
        short_report += MD_SHORT_GREEN

    return short_report


def generate_markdown_report(results: Dict[str, Any]):
    """Generate a markdown report from the results.

    Invariants:
    - Section order strictly follows `_SECTIONS`.
    - Branching in status rendering identical to original implementation.
    - Exact strings (including punctuation and emojis) are preserved.
    """

    def add_statuses_to_md(status, legal_issue_type, md_content):
        return _render_status(status, legal_issue_type, md_content, _MD_FMT)

    md_content = []
    md_content.append("\n## Short Report\n")
    md_content.append(MD_NOTE_SHORT)
    md_content.append(generate_short_report(results))

    md_content.append("\n## Full Report\n")
    # Add object and institution information
    object_name = results.get("object_name") or "unknown"
    institution_name = results.get("institution_name") or "unknown"
    url = results.get("object_url") or "unknown"
    md_content.extend(
        [f"\n**Object:** {object_name}", f"\n**Institution:** {institution_name}", f"\n**URL:** {url}", "\n"]
    )

    # Add explanation of priority order
    md_content.append(MD_NOTE_PRIORITY)

    # Unified section iteration
    for section in _SECTIONS:
        if section["guard"](results):
            md_content.append(section["md_heading"])
            
            # Special handling for digital representation: split into subheadings
            if section.get("is_digital_repr"):
                # Define subheadings for each IP right type
                digital_repr_subsections = [
                    {
                        "md_subheading": "\n#### Copyright\n",
                        "txt_subheading": "\nCopyright\n",
                        "condition_prefix": "DigitalRepresentationCopyright",
                    },
                    {
                        "md_subheading": "\n#### Rights to audio recordings (phonograms)\n",
                        "txt_subheading": "\nRights to audio recordings (phonograms)\n",
                        "condition_prefix": "DigitalRepresentationPhonogram",
                    },
                    {
                        "md_subheading": "\n#### Film fixation rights\n",
                        "txt_subheading": "\nFilm fixation rights\n",
                        "condition_prefix": "DigitalRepresentationFilmFixation",
                    },
                    {
                        "md_subheading": "\n#### Other IP rights\n",
                        "txt_subheading": "\nOther IP rights\n",
                        "condition_prefix": "DigitalRepresentationOtherIP",
                    },
                ]
                
                full_status = results[section["key"]]
                for subsection in digital_repr_subsections:
                    # Filter statuses for this subsection
                    filtered_status = _filter_status_by_prefix(full_status, subsection["condition_prefix"])
                    
                    # Only render if there's any content for this subsection
                    has_content = any([
                        filtered_status["info"],
                        filtered_status["green"],
                        filtered_status["yellow"],
                        filtered_status["red"],
                        filtered_status["rights_green"],
                        filtered_status["rights_yellow"],
                    ])
                    
                    if has_content:
                        md_content.append(subsection["md_subheading"])
                        md_content = add_statuses_to_md(
                            filtered_status, section["issue_type"], md_content
                        )
            else:
                # Normal rendering for other sections
                md_content = add_statuses_to_md(
                    results[section["key"]], section["issue_type"], md_content
                )

    md_content.append(f"\n*Report generated by tool v{APP_VERSION}*\n")

    # Add debug information
    _append_debug_json_md(md_content, results)

    return "".join(md_content)


def generate_text_report(results: Dict[str, Any]):
    """Generate a plain text report from the results.

    Invariants mirror the markdown variant; formatting differs (no bold/emojis, no code fences).
    """

    def add_statuses_to_txt(status, legal_issue_type, txt_content):
        return _render_status(status, legal_issue_type, txt_content, _TXT_FMT)

    txt_content = ["Report\n"]

    # Add object and institution information
    object_name = results.get("object_name") or "unknown"
    institution_name = results.get("institution_name") or "unknown"
    url = results.get("object_url") or "unknown"
    txt_content.extend(
        [f"\nObject: {object_name}", f"\nInstitution: {institution_name}", f"\nURL: {url}", "\n"]
    )

    # Add explanation of priority order
    txt_content.append(TXT_NOTE_PRIORITY)

    # Unified section iteration
    for section in _SECTIONS:
        if section["guard"](results):
            txt_content.append(section["txt_heading"])
            
            # Special handling for digital representation: split into subheadings
            if section.get("is_digital_repr"):
                # Define subheadings for each IP right type
                digital_repr_subsections = [
                    {
                        "md_subheading": "\n#### Copyright\n",
                        "txt_subheading": "\nCopyright\n",
                        "condition_prefix": "DigitalRepresentationCopyright",
                    },
                    {
                        "md_subheading": "\n#### Rights to audio recordings (phonograms)\n",
                        "txt_subheading": "\nRights to audio recordings (phonograms)\n",
                        "condition_prefix": "DigitalRepresentationPhonogram",
                    },
                    {
                        "md_subheading": "\n#### Film fixation rights\n",
                        "txt_subheading": "\nFilm fixation rights\n",
                        "condition_prefix": "DigitalRepresentationFilmFixation",
                    },
                    {
                        "md_subheading": "\n#### Other IP rights\n",
                        "txt_subheading": "\nOther IP rights\n",
                        "condition_prefix": "DigitalRepresentationOtherIP",
                    },
                ]
                
                full_status = results[section["key"]]
                for subsection in digital_repr_subsections:
                    # Filter statuses for this subsection
                    filtered_status = _filter_status_by_prefix(full_status, subsection["condition_prefix"])
                    
                    # Only render if there's any content for this subsection
                    has_content = any([
                        filtered_status["info"],
                        filtered_status["green"],
                        filtered_status["yellow"],
                        filtered_status["red"],
                        filtered_status["rights_green"],
                        filtered_status["rights_yellow"],
                    ])
                    
                    if has_content:
                        txt_content.append(subsection["txt_subheading"])
                        txt_content = add_statuses_to_txt(
                            filtered_status, section["issue_type"], txt_content
                        )
            else:
                # Normal rendering for other sections
                txt_content = add_statuses_to_txt(
                    results[section["key"]], section["issue_type"], txt_content
                )

    txt_content.append(f"\nReport generated by tool v{APP_VERSION}\n")

    # Add debug information
    _append_debug_json_txt(txt_content, results)

    return "".join(txt_content)


def _append_debug_json_md(md_content: List[str], results: Dict[str, Any]):
    md_content.append("\n#### 🔍 Results, inputs and debug data (JSON)\n")
    md_content.append("```json\n")
    debug_json = json.dumps(results, indent=2, sort_keys=True, default=str)
    md_content.append(debug_json)
    md_content.append("\n```\n")


def _append_debug_json_txt(txt_content: List[str], results: Dict[str, Any]):
    txt_content.append("\nResults, inputs and debug data (JSON)\n")
    txt_content.append("\n")
    debug_json = json.dumps(results, indent=2, sort_keys=True, default=str)
    txt_content.append(debug_json)
    txt_content.append("\n")
