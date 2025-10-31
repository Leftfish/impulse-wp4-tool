import json

import utils
import reports

MARKER = "(JSON)"

def read_report(filename):
    with open(filename, "r", encoding="utf-8") as f:
        full_report = f.read()
        i = full_report.find(MARKER)
        return json.loads(full_report[i + len(MARKER):])


def recalculate_results(filename):
    input_report = read_report(filename)
    data = input_report['debug_info']['input_data']
    intermediate_values = utils.calculate_all_intermediate_values(data)
    results = utils.calculate_results(data, intermediate_values)
    return results

def new_report_from_json(filename):
    return reports.generate_text_report(recalculate_results(filename))


def save_report_to_file(report, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)

if __name__== "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python report_from_json.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    print(f'Generating report based on data from {input_file} and saving it to {output_file}...')
    save_report_to_file(new_report_from_json(input_file), output_file)
