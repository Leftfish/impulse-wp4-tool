import json

import utils
import reports
from constants import APP_VERSION

MARKER = "(JSON)"


def parse_report_json(content: str) -> dict:
    i = content.find(MARKER)
    if i == -1:
        raise ValueError(f"Could not find {MARKER!r} marker in report")
    return json.loads(content[i + len(MARKER) :])


def read_report(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return parse_report_json(f.read())


def extract_input_data(input_report):
    debug_info = input_report.get("debug_info", {})
    data = dict(debug_info.get("input_data", {}))
    data.update(debug_info.get("basic_information", {}))
    return data


def recalculate_results_from_report(input_report):
    debug_info = input_report.get("debug_info", {})
    data = extract_input_data(input_report)
    original_version = debug_info.get("app_version")
    intermediate_values = utils.calculate_all_intermediate_values(data)
    results = utils.calculate_results(data, intermediate_values)
    if original_version and original_version != APP_VERSION:
        results["debug_info"]["source_app_version"] = original_version
    return results


def recalculate_results(filename):
    return recalculate_results_from_report(read_report(filename))


def regenerate_report(content: str) -> dict:
    input_report = parse_report_json(content)
    results = recalculate_results_from_report(input_report)
    original_version = input_report.get("debug_info", {}).get("app_version")
    return {
        "results": results,
        "text_report": reports.generate_text_report(results),
        "markdown_report": reports.generate_markdown_report(results),
        "app_version": APP_VERSION,
        "original_app_version": original_version,
    }


def new_report_from_json(filename):
    return reports.generate_text_report(recalculate_results(filename))


def save_report_to_file(report, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python report_from_json.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    print(
        f"Generating report based on data from {input_file} "
        f"and saving it to {output_file} (tool v{APP_VERSION})..."
    )
    save_report_to_file(new_report_from_json(input_file), output_file)
