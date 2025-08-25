from utils import calculate_film_fixation_rights_status, calculate_intermediate_values_film_fixations

print("=== SIMPLE FILM FIXATION TEST ===")

# Test case 1: Not a film fixation
test_data_1 = {
    'is_film_fixation': 'not_film_fixation'
}

intermediate_1 = calculate_intermediate_values_film_fixations(test_data_1)
results_1, _ = calculate_film_fixation_rights_status(test_data_1, intermediate_1)

print("Test 1 - Not a film fixation:")
print(f"GREEN: {len(results_1['green'])}")
print(f"YELLOW: {len(results_1['yellow'])}")
print(f"RED: {len(results_1['red'])}")
if results_1['green']:
    print(f"  Condition: {results_1['green'][0]['condition']}")

# Test case 2: Pre-1900 film fixation
test_data_2 = {
    'is_film_fixation': 'film_fixation',
    'film_fixation_before_1900': 'film_fixation_made_before_1900'
}

intermediate_2 = calculate_intermediate_values_film_fixations(test_data_2)
results_2, _ = calculate_film_fixation_rights_status(test_data_2, intermediate_2)

print("\nTest 2 - Pre-1900 film fixation:")
print(f"GREEN: {len(results_2['green'])}")
print(f"YELLOW: {len(results_2['yellow'])}")
print(f"RED: {len(results_2['red'])}")
if results_2['green']:
    print(f"  Condition: {results_2['green'][0]['condition']}")

print("\nTest completed successfully!") 