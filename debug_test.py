from utils import calculate_intermediate_values, calculate_results, generate_text_report

# Test case that's failing
data = {
    'is_copyright_work': 'work',
    'created_before_1850': 'not_made_before_1850',
    'authors': [
        {'identity_known': False, 'country_of_origin': 'DE'}  # Anonymous, EEA
    ],
    'creation_year': 2025 - 85,  # Created 85 years ago (1940)
    'first_publication_year': 2025 - 5  # Published 5 years ago (2020)
}

intermediate = calculate_intermediate_values(data)
results = calculate_results(data, intermediate)

print("=== INTERMEDIATE VALUES ===")
for key, value in intermediate.items():
    print(f"{key}: {value}")

print("\n=== COPYRIGHT RESULTS ===")
print("GREEN:", [r['condition'] for r in results['green']])
print("YELLOW:", [r['condition'] for r in results['yellow']])
print("RED:", [r['condition'] for r in results['red']])

print("\n=== FIRST EDITION RESULTS ===")
if 'first_edition_status' in results:
    print("GREEN:", [r['condition'] for r in results['first_edition_status']['green']])
    print("YELLOW:", [r['condition'] for r in results['first_edition_status']['yellow']])
    print("RED:", [r['condition'] for r in results['first_edition_status']['red']])
else:
    print("No first_edition_status found")

print("\n=== TEXT REPORT ===")
report = generate_text_report(results)
print(report) 