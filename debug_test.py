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

# Debug integration test issues
print("\n=== DEBUG INTEGRATION TEST ISSUES ===")

# Test what keys are returned by calculate_results
test_data_integration = {
    'object_name': 'Test Integration',
    'institution_name': 'Test Institution',
    'is_copyright_work': 'work',
    'is_performance': 'performance',
    'is_phonogram': 'phonogram',
    
    # Copyright data
    'authors': [{'identity_known': True, 'country_of_origin': 'DE'}],
    'author_death_year': 1950,
    'created_before_1850': 'not_made_before_1850',
    
    # Performance data
    'performers': [{'identity_known': True, 'country_of_origin': 'DE'}],
    'performance_year': 2020,
    'performance_phonogram_available': 'performance_phonogram_not_available',
    'performance_fixed_not_phonogram_available': 'performance_fixed_not_phonogram_not_available',
    'performance_available_no_medium': 'performance_not_publically_available_no_medium',
    
    # Phonogram data
    'phonogram_year': 1960,
    'phonogram_producers': [{'identity_known': True, 'country_of_origin': 'DE'}],
    'phonogram_published_fixed_medium': 'phonogram_not_published_fixed_medium',
    'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
}

intermediate_integration = calculate_all_intermediate_values(test_data_integration)
results_integration = calculate_results(test_data_integration, intermediate_integration)

print("Available keys in results:", list(results_integration.keys()))

if 'copyright_status' in results_integration:
    print("Copyright status found!")
    copyright_status = results_integration['copyright_status']
    print("Copyright GREEN:", len(copyright_status.get('green', [])))
    print("Copyright YELLOW:", len(copyright_status.get('yellow', [])))
    print("Copyright RED:", len(copyright_status.get('red', [])))
else:
    print("Copyright status NOT found!")
    # Check what copyright-related keys exist
    copyright_keys = [k for k in results_integration.keys() if 'copyright' in k.lower()]
    print("Copyright-related keys:", copyright_keys)

if 'performance_status' in results_integration:
    print("Performance status found!")
    performance_status = results_integration['performance_status']
    print("Performance GREEN:", len(performance_status.get('green', [])))
    print("Performance YELLOW:", len(performance_status.get('yellow', [])))
    print("Performance RED:", len(performance_status.get('red', [])))
else:
    print("Performance status NOT found!")

if 'phonogram_status' in results_integration:
    print("Phonogram status found!")
    phonogram_status = results_integration['phonogram_status']
    print("Phonogram GREEN:", len(phonogram_status.get('green', [])))
    print("Phonogram YELLOW:", len(phonogram_status.get('yellow', [])))
    print("Phonogram RED:", len(phonogram_status.get('red', [])))
else:
    print("Phonogram status NOT found!")

# Debug copyright conditions specifically
print("\n=== DEBUG COPYRIGHT CONDITIONS ===")
print("Main results GREEN:", len(results_integration.get('green', [])))
print("Main results YELLOW:", len(results_integration.get('yellow', [])))
print("Main results RED:", len(results_integration.get('red', [])))

print("Main results GREEN conditions:")
for result in results_integration.get('green', []):
    print(f"  - {result['condition']}: {result['explanation']}")

print("Main results RED conditions:")
for result in results_integration.get('red', []):
    print(f"  - {result['condition']}: {result['explanation']}")

# Test the specific copyright case from the failing test
print("\n=== DEBUG COPYRIGHT TEST CASE ===")
test_data_copyright = {
    'object_name': 'Test Copyright',
    'institution_name': 'Test Institution',
    'is_copyright_work': 'work',
    'is_phonogram': 'phonogram',
    
    # Copyright data
    'authors': [{'identity_known': True, 'country_of_origin': 'US'}],
    'author_death_year': 2020,  # Very recent, should be RED
    'created_before_1850': 'not_made_before_1850',
    
    # Phonogram data
    'phonogram_year': 1960,
    'phonogram_producers': [{'identity_known': True, 'country_of_origin': 'DE'}],
    'phonogram_published_fixed_medium': 'phonogram_not_published_fixed_medium',
    'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
}

intermediate_copyright = calculate_all_intermediate_values(test_data_copyright)
results_copyright = calculate_results(test_data_copyright, intermediate_copyright)

print("Copyright test case RED conditions:")
for result in results_copyright.get('red', []):
    print(f"  - {result['condition']}: {result['explanation']}")

print("Copyright test case GREEN conditions:")
for result in results_copyright.get('green', []):
    print(f"  - {result['condition']}: {result['explanation']}")

# Debug the intermediate values for copyright
print("\n=== DEBUG COPYRIGHT INTERMEDIATE VALUES ===")
print("AllAuthorsKnown:", intermediate_copyright.get('AllAuthorsKnown'))
print("CountryOfOriginEEAAnyReason:", intermediate_copyright.get('CountryOfOriginEEAAnyReason'))
print("MoreThan70YearsSinceDeath:", intermediate_copyright.get('MoreThan70YearsSinceDeath'))
print("DeathYearUnknown:", intermediate_copyright.get('DeathYearUnknown'))

# Test with EEA author to see if that makes a difference
print("\n=== DEBUG COPYRIGHT TEST CASE (EEA AUTHOR) ===")
test_data_copyright_eea = {
    'object_name': 'Test Copyright EEA',
    'institution_name': 'Test Institution',
    'is_copyright_work': 'work',
    'is_phonogram': 'phonogram',
    
    # Copyright data - EEA author
    'authors': [{'identity_known': True, 'country_of_origin': 'DE'}],
    'author_death_year': 2020,  # Very recent, should be RED
    'created_before_1850': 'not_made_before_1850',
    
    # Phonogram data
    'phonogram_year': 1960,
    'phonogram_producers': [{'identity_known': True, 'country_of_origin': 'DE'}],
    'phonogram_published_fixed_medium': 'phonogram_not_published_fixed_medium',
    'phonogram_available_no_medium': 'phonogram_not_publically_available_no_medium'
}

intermediate_copyright_eea = calculate_all_intermediate_values(test_data_copyright_eea)
results_copyright_eea = calculate_results(test_data_copyright_eea, intermediate_copyright_eea)

print("Copyright EEA test case RED conditions:")
for result in results_copyright_eea.get('red', []):
    print(f"  - {result['condition']}: {result['explanation']}")

print("Copyright EEA test case GREEN conditions:")
for result in results_copyright_eea.get('green', []):
    print(f"  - {result['condition']}: {result['explanation']}")

print("Copyright EEA intermediate values:")
print("AllAuthorsKnown:", intermediate_copyright_eea.get('AllAuthorsKnown'))
print("CountryOfOriginEEAAnyReason:", intermediate_copyright_eea.get('CountryOfOriginEEAAnyReason'))
print("MoreThan70YearsSinceDeath:", intermediate_copyright_eea.get('MoreThan70YearsSinceDeath'))
print("DeathYearUnknown:", intermediate_copyright_eea.get('DeathYearUnknown')) 