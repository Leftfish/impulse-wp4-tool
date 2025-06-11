import pytest
from utils import calculate_digital_representation_status

class MockField:
    def __init__(self, data):
        self.data = data

class MockDigitalReprIPRights:
    def __init__(self, copyright='no', audio='no', film='no', performance='no', other='no'):
        self.copyright = MockField(copyright)
        self.audio_recording_rights = MockField(audio)
        self.film_fixation_rights = MockField(film)
        self.performance_rights = MockField(performance)
        self.other_ip_rights = MockField(other)

def test_all_no_gives_green():
    """Test that all 'no' answers result in single green status."""
    rights = MockDigitalReprIPRights()
    result = calculate_digital_representation_status(rights)
    
    assert len(result['green']) == 1
    assert len(result['yellow']) == 0
    assert len(result['red']) == 0
    assert result['green'][0]['condition'] == 'DigitalRepresentationNoProtection'

def test_single_yes_gives_red_and_individual_greens():
    """Test that a single 'yes' answer results in red status and shows individual greens for 'no' answers."""
    rights = MockDigitalReprIPRights(copyright='yes')
    result = calculate_digital_representation_status(rights)
    
    assert len(result['red']) == 1
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    
    # Check that we have green status for each 'no' answer
    green_conditions = {r['condition'] for r in result['green']}
    expected_conditions = {
        'DigitalRepresentationPhonogramStatus',
        'DigitalRepresentationFilmFixationStatus',
        'DigitalRepresentationPerformanceStatus',
        'DigitalRepresentationOtherIPStatus'
    }
    assert green_conditions == expected_conditions

def test_single_uncertain_gives_yellow_and_individual_greens():
    """Test that a single 'uncertain' answer results in yellow status and shows individual greens."""
    rights = MockDigitalReprIPRights(audio='uncertain')
    result = calculate_digital_representation_status(rights)
    
    assert len(result['yellow']) == 1
    assert result['yellow'][0]['condition'] == 'DigitalRepresentationPhonogramStatus'
    assert len(result['red']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights

def test_mixed_statuses():
    """Test that mixed answers result in multiple statuses."""
    rights = MockDigitalReprIPRights(
        copyright='yes',
        audio='uncertain',
        film='yes',
        performance='no',
        other='uncertain'
    )
    result = calculate_digital_representation_status(rights)
    
    assert len(result['red']) == 2  # copyright and film
    assert len(result['yellow']) == 2  # audio and other
    assert len(result['green']) == 1  # performance
    
    # Verify the green status is for performance
    assert result['green'][0]['condition'] == 'DigitalRepresentationPerformanceStatus'

def test_status_names():
    """Test that correct status names are used."""
    rights = MockDigitalReprIPRights(
        copyright='yes',
        audio='yes',
        film='yes',
        performance='yes',
        other='yes'
    )
    result = calculate_digital_representation_status(rights)
    
    status_names = {r['condition'] for r in result['red']}
    expected_names = {
        'DigitalRepresentationCopyrightStatus',
        'DigitalRepresentationPhonogramStatus',
        'DigitalRepresentationFilmFixationStatus',
        'DigitalRepresentationPerformanceStatus',
        'DigitalRepresentationOtherIPStatus'
    }
    
    assert status_names == expected_names

def test_rights_transfer_changes_red_to_green():
    """Test that rights transfer changes red status to green."""
    rights = MockDigitalReprIPRights(copyright='yes')
    rights_acquired = MockDigitalReprIPRights(copyright='right_transfer')
    
    result = calculate_digital_representation_status(rights, rights_acquired)
    
    assert len(result['red']) == 0
    assert len(result['yellow']) == 0
    assert len(result['green']) == 5  # One acquired + four individual greens
    assert any(r['condition'] == 'DigitalRepresentationCopyrightAcquired' for r in result['green'])

def test_employer_rights_changes_yellow_to_green():
    """Test that employer rights changes yellow status to green."""
    rights = MockDigitalReprIPRights(audio='uncertain')
    rights_acquired = MockDigitalReprIPRights(audio='employer_rights')
    
    result = calculate_digital_representation_status(rights, rights_acquired)
    
    assert len(result['yellow']) == 0
    assert len(result['red']) == 0
    assert len(result['green']) == 5  # One acquired + four individual greens
    assert any(r['condition'] == 'DigitalRepresentationPhonogramAcquired' for r in result['green'])

def test_not_applicable_keeps_status():
    """Test that not_applicable doesn't change status."""
    rights = MockDigitalReprIPRights(copyright='yes')
    rights_acquired = MockDigitalReprIPRights(copyright='not_applicable')
    
    result = calculate_digital_representation_status(rights, rights_acquired)
    
    assert len(result['red']) == 1
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'

def test_rights_not_acquired_keeps_status():
    """Test that rights_not_acquired doesn't change status."""
    rights = MockDigitalReprIPRights(copyright='yes')
    rights_acquired = MockDigitalReprIPRights(copyright='rights_not_acquired')
    
    result = calculate_digital_representation_status(rights, rights_acquired)
    
    assert len(result['red']) == 1
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'

def test_unknown_keeps_status():
    """Test that unknown doesn't change status."""
    rights = MockDigitalReprIPRights(copyright='yes')
    rights_acquired = MockDigitalReprIPRights(copyright='unknown')
    
    result = calculate_digital_representation_status(rights, rights_acquired)
    
    assert len(result['red']) == 1
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'

def test_mixed_rights_acquisition():
    """Test mixed scenarios of rights acquisition."""
    rights = MockDigitalReprIPRights(
        copyright='yes',
        audio='uncertain',
        film='yes',
        performance='yes',
        other='uncertain'
    )
    rights_acquired = MockDigitalReprIPRights(
        copyright='right_transfer',
        audio='employer_rights',
        film='not_applicable',
        performance='rights_not_acquired',
        other='unknown'
    )
    
    result = calculate_digital_representation_status(rights, rights_acquired)
    
    assert len(result['red']) == 2  # film and performance remain red
    assert len(result['yellow']) == 1  # other remains yellow
    assert len(result['green']) == 2  # copyright and audio become green
    
    green_conditions = {r['condition'] for r in result['green']}
    assert 'DigitalRepresentationCopyrightAcquired' in green_conditions
    assert 'DigitalRepresentationPhonogramAcquired' in green_conditions

def test_digital_repr_rights_availability_cc0():
    """Test CC0 license upgrades status to GREEN."""
    class MockField:
        def __init__(self, data):
            self.data = data

    class MockForm:
        def __init__(self):
            self.copyright = MockField('yes')
            self.audio_recording_rights = MockField('no')
            self.film_fixation_rights = MockField('no')
            self.performance_rights = MockField('no')
            self.other_ip_rights = MockField('no')

    class MockAvailabilityForm:
        def __init__(self):
            self.copyright = MockField('cc0')
            self.audio_recording_rights = MockField('not_applicable')
            self.film_fixation_rights = MockField('not_applicable')
            self.performance_rights = MockField('not_applicable')
            self.other_ip_rights = MockField('not_applicable')

    results = calculate_digital_representation_status(
        MockForm(),
        digital_repr_rights_availability=MockAvailabilityForm()
    )

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'CC0' in r['explanation'] for r in results['green'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in results['red'])

def test_digital_repr_rights_availability_cc_by_sa():
    """Test CC-BY-SA license upgrades status to YELLOW."""
    class MockField:
        def __init__(self, data):
            self.data = data

    class MockForm:
        def __init__(self):
            self.copyright = MockField('yes')
            self.audio_recording_rights = MockField('no')
            self.film_fixation_rights = MockField('no')
            self.performance_rights = MockField('no')
            self.other_ip_rights = MockField('no')

    class MockAvailabilityForm:
        def __init__(self):
            self.copyright = MockField('cc_by_sa')
            self.audio_recording_rights = MockField('not_applicable')
            self.film_fixation_rights = MockField('not_applicable')
            self.performance_rights = MockField('not_applicable')
            self.other_ip_rights = MockField('not_applicable')

    results = calculate_digital_representation_status(
        MockForm(),
        digital_repr_rights_availability=MockAvailabilityForm()
    )

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'CC-BY-SA' in r['explanation'] for r in results['yellow'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in results['red'])

def test_digital_repr_rights_availability_rights_assignment():
    """Test rights assignment upgrades status to GREEN."""
    class MockField:
        def __init__(self, data):
            self.data = data

    class MockForm:
        def __init__(self):
            self.copyright = MockField('yes')
            self.audio_recording_rights = MockField('no')
            self.film_fixation_rights = MockField('no')
            self.performance_rights = MockField('no')
            self.other_ip_rights = MockField('no')

    class MockAvailabilityForm:
        def __init__(self):
            self.copyright = MockField('rights_assignment')
            self.audio_recording_rights = MockField('not_applicable')
            self.film_fixation_rights = MockField('not_applicable')
            self.performance_rights = MockField('not_applicable')
            self.other_ip_rights = MockField('not_applicable')

    results = calculate_digital_representation_status(
        MockForm(),
        digital_repr_rights_availability=MockAvailabilityForm()
    )

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'acquired the rights through assignment' in r['explanation'] for r in results['green'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in results['red'])

def test_digital_repr_rights_availability_orphan_works():
    """Test orphan works upgrades status to YELLOW."""
    class MockField:
        def __init__(self, data):
            self.data = data

    class MockForm:
        def __init__(self):
            self.copyright = MockField('yes')
            self.audio_recording_rights = MockField('no')
            self.film_fixation_rights = MockField('no')
            self.performance_rights = MockField('no')
            self.other_ip_rights = MockField('no')

    class MockAvailabilityForm:
        def __init__(self):
            self.copyright = MockField('orphan_works')
            self.audio_recording_rights = MockField('not_applicable')
            self.film_fixation_rights = MockField('not_applicable')
            self.performance_rights = MockField('not_applicable')
            self.other_ip_rights = MockField('not_applicable')

    results = calculate_digital_representation_status(
        MockForm(),
        digital_repr_rights_availability=MockAvailabilityForm()
    )

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'orphan works provisions' in r['explanation'] for r in results['yellow'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in results['red'])

def test_digital_repr_rights_availability_multiple_rights():
    """Test handling multiple rights with different availability choices."""
    class MockField:
        def __init__(self, data):
            self.data = data

    class MockForm:
        def __init__(self):
            self.copyright = MockField('yes')
            self.audio_recording_rights = MockField('yes')
            self.film_fixation_rights = MockField('yes')
            self.performance_rights = MockField('no')
            self.other_ip_rights = MockField('no')

    class MockAvailabilityForm:
        def __init__(self):
            self.copyright = MockField('cc0')  # Should upgrade to GREEN
            self.audio_recording_rights = MockField('cc_by_sa')  # Should upgrade to YELLOW
            self.film_fixation_rights = MockField('rights_assignment')  # Should upgrade to GREEN
            self.performance_rights = MockField('not_applicable')  # No change
            self.other_ip_rights = MockField('not_applicable')  # No change

    results = calculate_digital_representation_status(
        MockForm(),
        digital_repr_rights_availability=MockAvailabilityForm()
    )

    # Check copyright status (GREEN)
    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'CC0' in r['explanation'] for r in results['green'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in results['red'])

    # Check audio recording status (YELLOW)
    assert any(r['condition'] == 'DigitalRepresentationPhonogramStatus' 
              and 'CC-BY-SA' in r['explanation'] for r in results['yellow'])
    assert not any(r['condition'] == 'DigitalRepresentationPhonogramStatus' for r in results['red'])

    # Check film fixation status (GREEN)
    assert any(r['condition'] == 'DigitalRepresentationFilmFixationStatus' 
              and 'acquired the rights through assignment' in r['explanation'] for r in results['green'])
    assert not any(r['condition'] == 'DigitalRepresentationFilmFixationStatus' for r in results['red']) 