from utils import calculate_all_intermediate_values

# Test with uncertain values
test_data_uncertain = {
    'phonogram_producers': [
        {'identity_known': True, 'country_of_origin': 'XX'}
    ],
    'recording_published_fixed_medium': 'uncertain',
    'recording_available_no_medium': 'recording_publically_available_no_medium'
}

intermediate_uncertain = calculate_all_intermediate_values(test_data_uncertain)
print("UncertainIfRecordingPublishedOrMadeAvailable:", intermediate_uncertain.get('UncertainIfRecordingPublishedOrMadeAvailable'))
print("All phonogram keys:")
for key, value in intermediate_uncertain.items():
    if 'Phonogram' in key or 'UncertainIfRecording' in key:
        print(f"  {key}: {value}") 