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
    """Test that all 'no' answers result in green status."""
    rights = MockDigitalReprIPRights()
    result = calculate_digital_representation_status(rights)
    
    assert len(result['green']) == 1
    assert len(result['yellow']) == 0
    assert len(result['red']) == 0
    assert result['green'][0]['condition'] == 'DigitalRepresentationNoProtection'

def test_single_yes_gives_red():
    """Test that a single 'yes' answer results in red status."""
    rights = MockDigitalReprIPRights(copyright='yes')
    result = calculate_digital_representation_status(rights)
    
    assert len(result['red']) == 1
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'
    assert len(result['yellow']) == 0
    assert len(result['green']) == 0

def test_single_uncertain_gives_yellow():
    """Test that a single 'uncertain' answer results in yellow status."""
    rights = MockDigitalReprIPRights(audio='uncertain')
    result = calculate_digital_representation_status(rights)
    
    assert len(result['yellow']) == 1
    assert result['yellow'][0]['condition'] == 'DigitalRepresentationPhonogramStatus'
    assert len(result['red']) == 0
    assert len(result['green']) == 0

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
    assert len(result['green']) == 0  # not all no

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