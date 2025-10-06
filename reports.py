from datetime import datetime
import json

def generate_short_report(results):
    """Generate a short summary report from the results."""

    short_report = """"""
    yellows = []
    reds = []
    for _, status in results.items():
        if isinstance(status, dict):
            if status.get("red", []) and not (
                status.get("rights_green", []) or status.get("rights_yellow", [])
            ):
                reds.append(status["red"][0])
            if status.get("rights_red", []) and not (
                status.get("rights_green", []) or status.get("rights_yellow", [])
            ):
                reds.append(status["rights_red"][0])
            if status.get("yellow", []) and not (status.get("rights_green", [])):
                yellows.append(status["yellow"][0])
            if status.get("rights_yellow", []) and not (status.get("rights_green", [])):
                yellows.append(status["rights_yellow"][0])

    if reds:
        short_report += (
            "**❌ Red status. There are legal obstacles to using the object online:** "
        )
        status_codes = []
        for item in reds:
            status_codes.append(item["condition"])
        short_report += f"{'; '.join(status_codes)}"

    elif yellows:
        short_report += "**⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation:** "
        status_codes = []
        for item in yellows:
            status_codes.append(item["condition"])
        short_report += f"{'; '.join(status_codes)}"

    else:
        short_report += "**✅ Green status. There are no legal obstacles to using the object online.**"

    return short_report


def generate_markdown_report(results):
    """Generate a markdown report from the results."""

    def add_statuses_to_md(status, legal_issue_type, md_content):
        if status["info"]:
            md_content.append(f"\n##### 📝 Informational Messages: {legal_issue_type}\n")
            for result in status["info"]:
                md_content.append(
                    f"- **{result['condition']}**: {result['explanation']}\n"
                )

        if not (status["rights_green"] or status["rights_yellow"]):
            if status["green"]:
                md_content.append(
                    f"\n##### ✅ Green status. No issues caused by {legal_issue_type}\n"
                )
                for result in status["green"]:
                    md_content.append(
                        f"- **{result['condition']}**: {result['explanation']}\n"
                    )
                # return md_content

            if status["red"]:
                md_content.append(
                    f"\n##### ❌ Red status. There are legal obstacles caused by {legal_issue_type}.\n"
                )
                for result in status["red"]:
                    md_content.append(
                        f"- **{result['condition']}**: {result['explanation']}\n"
                    )

            if status["yellow"]:
                md_content.append(
                    f"\n##### ⚠️ Yellow status. There is either insufficient data or the nature of the issue requires further investigation in connection with {legal_issue_type}.\n"
                )
                for result in status["yellow"]:
                    md_content.append(
                        f"- **{result['condition']}**: {result['explanation']}\n"
                    )

        else:
            md_content.append(
                "\n#### The following legal bases to use the object apply:\n"
            )
            if status["rights_green"]:
                md_content.append(
                    "\n##### ✅ Green status. The bases below are sufficient to use the object online\n"
                )
                for result in status["rights_green"]:
                    md_content.append(
                        f"- **{result['condition']}**: {result['explanation']}\n"
                    )
            elif status["rights_yellow"]:
                md_content.append(
                    "\n##### ⚠️ Yellow status. The bases below may be sufficient, but require further investigation.\n"
                )
                for result in status["rights_yellow"]:
                    md_content.append(
                        f"- **{result['condition']}**: {result['explanation']}\n"
                    )

            md_content.append(
                f"\n##### 📝. At the same time, the object is protected by {legal_issue_type} on a following basis:\n"
            )
            for result in status["green"] + status["yellow"] + status["red"]:
                md_content.append(
                    f"- **{result['condition']}**: {result['explanation']}\n"
                )

        return md_content

    md_content = []
    md_content.append("\n## Short Report\n")
    md_content.append(
        "\nNote: the short report provides a quick, simplified summary. If there are any definite obstacles, it will display only a RED status. If there are no definite obstacles, but at least one problematic issue, it will display a YELLOW status. Otherwise, the status will be GREEN.\n\n\n"
    )
    md_content.append(generate_short_report(results))

    md_content.append("\n## Full Report\n")
    # Add object and institution information
    object_name = results.get("object_name") or "unknown"
    institution_name = results.get("institution_name") or "unknown"
    md_content.extend(
        [f"\n**Object:** {object_name}", f"\n**Institution:** {institution_name}\n"]
    )

    # Add explanation of priority order
    md_content.append(
        "\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n"
    )

    # Add copyright status section
    md_content.append("\n### Copyright status of the object\n")

    if results.get("copyright_status"):
        copyright_status = results["copyright_status"]
        md_content = add_statuses_to_md(copyright_status, "copyright", md_content)

    # Add first edition protection section (if applicable)
    if any([len(status) for status in results.get("first_edition_status").values()]):
        md_content.append(
            "\n### First edition protection / posthumous edition status\n"
        )
        first_edition = results["first_edition_status"]
        md_content = add_statuses_to_md(
            first_edition, "first edition protection", md_content
        )

    # Add performance rights section
    if results.get("performance_status"):
        md_content.append("\n### Performance rights status of the object\n")
        performance_status = results["performance_status"]
        md_content = add_statuses_to_md(
            performance_status, "performance rights", md_content
        )

    # Add phonogram rights section
    if results.get("phonogram_status"):
        md_content.append("\n### Phonogram rights status of the object\n")
        phonogram_status = results["phonogram_status"]
        md_content = add_statuses_to_md(
            phonogram_status, "phonogram rights", md_content
        )

    # Add film fixation rights section
    if results.get("film_fixation_status"):
        md_content.append("\n### Film fixation rights status of the object\n")
        film_fixation_status = results["film_fixation_status"]
        md_content = add_statuses_to_md(
            film_fixation_status, "film fixation rights", md_content
        )

    # Add broadcasting organisation rights section
    if results.get("broadcast_status"):
        broadcast_status = results["broadcast_status"]
        md_content.append(
            "\n### Broadcasting organisation rights status of the object\n"
        )
        md_content = add_statuses_to_md(
            broadcast_status, "broadcasting organisation rights", md_content
        )

    # Add other IP rights section
    if results.get("other_ip_rights_status"):
        md_content.append("\n### Other IP rights\n")
        additional_classification = results["other_ip_rights_status"]
        md_content = add_statuses_to_md(
            additional_classification, "additional classification rights", md_content
        )

    # Add digital representation status section
    if results.get("digital_repr_status"):
        md_content.append(
            "\n### IP status of the digital representation of the object\n"
        )
        digital_representation_status = results["digital_repr_status"]
        md_content = add_statuses_to_md(
            digital_representation_status,
            "rights to the digital representation of the object",
            md_content,
        )

    # Add other legal issues section
    if results.get("other_legal_issues_status"):
        md_content.append("\n### Other legal issues\n")
        other_legal_issues_status = results["other_legal_issues_status"]
        add_statuses_to_md(
            other_legal_issues_status,
            "other legal issues (unrelated to IP)",
            md_content,
        )

    # Add debug information
    if results.get("debug_info"):
        md_content.append("\n#### 🔍 Source data (JSON)\n")
        md_content.append("```json\n")

        debug_json = json.dumps(
            results["debug_info"], indent=2, sort_keys=True, default=str
        )
        md_content.append(debug_json)
        md_content.append("\n```\n")

    return "".join(md_content)


def generate_text_report(results):
    """Generate a plain text report from the results."""

    def add_statuses_to_txt(status, legal_issue_type, txt_content):
        if status["info"]:
            txt_content.append(f"\nInformational Messages: {legal_issue_type}\n")
            for result in status["info"]:
                txt_content.append(
                    f"- {result['condition']}: {result['explanation']}\n"
                )

        if not (status["rights_green"] or status["rights_yellow"]):
            if status["green"]:
                txt_content.append(
                    f"\nGreen status. No issues caused by {legal_issue_type}\n"
                )
                for result in status["green"]:
                    txt_content.append(
                        f"- {result['condition']}: {result['explanation']}\n"
                    )
                # return txt_content

            if status["red"]:
                txt_content.append(
                    f"\nRed status. There are legal obstacles caused by {legal_issue_type}.\n"
                )
                for result in status["red"]:
                    txt_content.append(
                        f"- {result['condition']}: {result['explanation']}\n"
                    )

            if status["yellow"]:
                txt_content.append(
                    f"\nYellow status. There is either insufficient data or the nature of the issue requires further investigation in connection with {legal_issue_type}.\n"
                )
                for result in status["yellow"]:
                    txt_content.append(
                        f"- {result['condition']}: {result['explanation']}\n"
                    )

        else:
            txt_content.append("\nThe following legal bases to use the object apply:\n")
            if status["rights_green"]:
                txt_content.append(
                    "\nGreen status. The bases below are sufficient to use the object online\n"
                )
                for result in status["rights_green"]:
                    txt_content.append(
                        f"- {result['condition']}: {result['explanation']}\n"
                    )
            elif status["rights_yellow"]:
                txt_content.append(
                    "\nYellow status. The bases below may be sufficient, but require further investigation.\n"
                )
                for result in status["rights_yellow"]:
                    txt_content.append(
                        f"- {result['condition']}: {result['explanation']}\n"
                    )

            txt_content.append(
                f"\nAt the same time, the object is protected by {legal_issue_type} on a following basis:\n"
            )
            for result in status["green"] + status["yellow"] + status["red"]:
                txt_content.append(
                    f"- {result['condition']}: {result['explanation']}\n"
                )

        return txt_content

    txt_content = ["Report\n"]

    # Add object and institution information
    object_name = results.get("object_name") or "unknown"
    institution_name = results.get("institution_name") or "unknown"
    txt_content.extend(
        [f"\nObject: {object_name}", f"\nInstitution: {institution_name}\n"]
    )

    # Add explanation of priority order
    txt_content.append(
        "\nNote: Results are shown in order of priority - Red status (legal obstacles) takes precedence over Yellow status (uncertain conditions), which takes precedence over Green status (no issues).\n"
    )

    # Add copyright status section
    txt_content.append("\nCopyright status of the object\n")

    if results.get("copyright_status"):
        copyright_status = results["copyright_status"]
        txt_content = add_statuses_to_txt(copyright_status, "copyright", txt_content)

    # Add first edition protection section (if applicable)
    if any([len(status) for status in results.get("first_edition_status").values()]):
        txt_content.append("\nFirst edition protection / posthumous edition status\n")
        first_edition = results["first_edition_status"]
        txt_content = add_statuses_to_txt(
            first_edition, "first edition protection", txt_content
        )

    # Add performance rights section
    if results.get("performance_status"):
        txt_content.append("\nPerformance rights status of the object\n")
        performance_status = results["performance_status"]
        txt_content = add_statuses_to_txt(
            performance_status, "performance rights", txt_content
        )

    # Add phonogram rights section
    if results.get("phonogram_status"):
        txt_content.append("\nPhonogram rights status of the object\n")
        phonogram_status = results["phonogram_status"]
        txt_content = add_statuses_to_txt(
            phonogram_status, "phonogram rights", txt_content
        )

    # Add film fixation rights section
    if results.get("film_fixation_status"):
        txt_content.append("\nFilm fixation rights status of the object\n")
        film_fixation_status = results["film_fixation_status"]
        txt_content = add_statuses_to_txt(
            film_fixation_status, "film fixation rights", txt_content
        )

    # Add broadcasting organisation rights section
    if results.get("broadcast_status"):
        broadcast_status = results["broadcast_status"]
        txt_content.append("\nBroadcasting organisation rights status of the object\n")
        txt_content = add_statuses_to_txt(
            broadcast_status, "broadcasting organisation rights", txt_content
        )

    # Add other IP rights section
    if results.get("other_ip_rights_status"):
        txt_content.append("\nOther IP rights\n")
        additional_classification = results["other_ip_rights_status"]
        txt_content = add_statuses_to_txt(
            additional_classification, "additional classification rights", txt_content
        )

    # Add digital representation status section
    if results.get("digital_repr_status"):
        txt_content.append("\nIP status of the digital representation of the object\n")
        digital_representation_status = results["digital_repr_status"]
        txt_content = add_statuses_to_txt(
            digital_representation_status,
            "rights to the digital representation of the object",
            txt_content,
        )

    # Add other legal issues section
    if results.get("other_legal_issues_status"):
        txt_content.append("\nOther legal issues\n")
        other_legal_issues_status = results["other_legal_issues_status"]
        add_statuses_to_txt(
            other_legal_issues_status,
            "other legal issues (unrelated to IP)",
            txt_content,
        )

    # Add debug information
    if results.get("debug_info"):
        txt_content.append("\nSource data (JSON)\n")
        txt_content.append("\n")

        debug_json = json.dumps(
            results["debug_info"], indent=2, sort_keys=True, default=str
        )
        txt_content.append(debug_json)
        txt_content.append("\n")

    return "".join(txt_content)
