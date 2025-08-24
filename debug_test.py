from utils import calculate_all_intermediate_values, calculate_results

# Test data for phonogram status calculation (EEA)
test_data_eea = {
    'object_name': 'Test Recording (EEA)',
    'institution_name': 'Test Institution',
    'is_phonogram': 'phonogram',
    'phonogram_before_1900': 'phonogram_not_made_before_1900',
    'phonogram_year': 1960,
    'phonogram_producers': [
        {'identity_known': True, 'country_of_origin': 'DE'}
    ],
    'phonogram_published_fixed_medium': 'phonogram_not_published_fixed_medium',
    'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
}

# Test data for phonogram status calculation (Non-EEA)
test_data_non_eea = {
    'object_name': 'Test Recording (Non-EEA)',
    'institution_name': 'Test Institution',
    'is_phonogram': 'phonogram',
    'phonogram_before_1900': 'phonogram_not_made_before_1900',
    'phonogram_year': 1960,
    'phonogram_producers': [
        {'identity_known': True, 'country_of_origin': 'US'}
    ],
    'phonogram_published_fixed_medium': 'phonogram_not_published_fixed_medium',
    'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
}

# Test EEA case
print("=== EEA PHONOGRAM STATUS TEST ===")
intermediate_eea = calculate_all_intermediate_values(test_data_eea)
results_eea = calculate_results(test_data_eea, intermediate_eea)

if results_eea.get('phonogram_status'):
    phonogram_status = results_eea['phonogram_status']
    print(f"Object: {results_eea['object_name']}")
    
    if phonogram_status['green']:
        print("GREEN:")
        for result in phonogram_status['green']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if phonogram_status['yellow']:
        print("YELLOW:")
        for result in phonogram_status['yellow']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if phonogram_status['red']:
        print("RED:")
        for result in phonogram_status['red']:
            print(f"  - {result['condition']}: {result['explanation']}")

# Test Non-EEA case
print("\n=== NON-EEA PHONOGRAM STATUS TEST ===")
intermediate_non_eea = calculate_all_intermediate_values(test_data_non_eea)
results_non_eea = calculate_results(test_data_non_eea, intermediate_non_eea)

if results_non_eea.get('phonogram_status'):
    phonogram_status = results_non_eea['phonogram_status']
    print(f"Object: {results_non_eea['object_name']}")
    
    if phonogram_status['green']:
        print("GREEN:")
        for result in phonogram_status['green']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if phonogram_status['yellow']:
        print("YELLOW:")
        for result in phonogram_status['yellow']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if phonogram_status['red']:
        print("RED:")
        for result in phonogram_status['red']:
            print(f"  - {result['condition']}: {result['explanation']}")

print("\n=== INTERMEDIATE VALUES COMPARISON ===")
print("EEA CountryOfOriginEEAPhonograms:", intermediate_eea.get('CountryOfOriginEEAPhonograms'))
print("Non-EEA CountryOfOriginEEAPhonograms:", intermediate_non_eea.get('CountryOfOriginEEAPhonograms')) 

# Test data for phonogram with missing publication year
test_data_phonogram_missing_year = {
    'object_name': 'Test Phonogram (Missing Year)',
    'institution_name': 'Test Institution',
    'is_phonogram': 'phonogram',
    'phonogram_before_1900': 'phonogram_not_made_before_1900',
    'phonogram_year': 1960,
    'phonogram_producers': [
        {'identity_known': True, 'country_of_origin': 'DE'}
    ],
    'phonogram_published_fixed_medium': 'phonogram_published_fixed_medium',  # Yes, but year is missing
    'phonogram_published_fixed_medium_year': None,  # Missing year
    'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
}

# Test data for performance with missing publication year
test_data_performance_missing_year = {
    'object_name': 'Test Performance (Missing Year)',
    'institution_name': 'Test Institution',
    'is_performance': 'performance',
    'performance_before_1900': 'performance_not_made_before_1900',
    'performance_year': 1960,
    'performers': [
        {'identity_known': True, 'country_of_origin': 'DE'}
    ],
    'performance_phonogram_available': 'performance_phonogram_available',  # Yes, but year is missing
    'performance_phonogram_available_year': None,  # Missing year
    'performance_available_no_medium': 'performance_not_publically_available_no_medium',
    'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available'
}

print("=== PHONOGRAM WITH MISSING PUBLICATION YEAR ===")
intermediate_phonogram = calculate_all_intermediate_values(test_data_phonogram_missing_year)
results_phonogram = calculate_results(test_data_phonogram_missing_year, intermediate_phonogram)

if results_phonogram.get('phonogram_status'):
    phonogram_status = results_phonogram['phonogram_status']
    print(f"Object: {results_phonogram['object_name']}")
    
    if phonogram_status['green']:
        print("GREEN:")
        for result in phonogram_status['green']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if phonogram_status['yellow']:
        print("YELLOW:")
        for result in phonogram_status['yellow']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if phonogram_status['red']:
        print("RED:")
        for result in phonogram_status['red']:
            print(f"  - {result['condition']}: {result['explanation']}")

print("\n=== PERFORMANCE WITH MISSING PUBLICATION YEAR ===")
intermediate_performance = calculate_all_intermediate_values(test_data_performance_missing_year)
results_performance = calculate_results(test_data_performance_missing_year, intermediate_performance)

if results_performance.get('performance_status'):
    performance_status = results_performance['performance_status']
    print(f"Object: {results_performance['object_name']}")
    
    if performance_status['green']:
        print("GREEN:")
        for result in performance_status['green']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if performance_status['yellow']:
        print("YELLOW:")
        for result in performance_status['yellow']:
            print(f"  - {result['condition']}: {result['explanation']}")
    
    if performance_status['red']:
        print("RED:")
        for result in performance_status['red']:
            print(f"  - {result['condition']}: {result['explanation']}")

print("\n=== INTERMEDIATE VALUES COMPARISON ===")
print("Phonogram UncertainIfPhonogramPublishedOrMadeAvailable:", intermediate_phonogram.get('UncertainIfPhonogramPublishedOrMadeAvailable'))
print("Performance UncertainIfPerformancePublishedOrMadeAvailable:", intermediate_performance.get('UncertainIfPerformancePublishedOrMadeAvailable')) 