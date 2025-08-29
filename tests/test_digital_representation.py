import pytest
from utils_modules.digital_representation import calculate_digital_representation_status

def test_all_no_gives_green():
    """Test that all 'no' answers result in single green status."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'no',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['green']) == 5
    assert len(result['yellow']) == 0
    assert len(result['red']) == 0

def test_single_yes_gives_red_and_individual_greens():
    """Test that a single 'yes' answer results in red status and shows individual greens for 'no' answers."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
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
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'no',
            'audio_recording_rights': 'uncertain',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['yellow']) == 1
    assert result['yellow'][0]['condition'] == 'DigitalRepresentationPhonogramStatus'
    assert len(result['red']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights

def test_mixed_statuses():
    """Test that mixed answers result in multiple statuses."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'uncertain',
            'film_fixation_rights': 'yes',
            'performance_rights': 'no',
            'other_ip_rights': 'uncertain'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['red']) == 2  # copyright and film
    assert len(result['yellow']) == 2  # audio and other
    assert len(result['green']) == 1  # performance
    
    # Verify the green status is for performance
    assert result['green'][0]['condition'] == 'DigitalRepresentationPerformanceStatus'

def test_status_names():
    """Test that correct status names are used."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'yes',
            'film_fixation_rights': 'yes',
            'performance_rights': 'yes',
            'other_ip_rights': 'yes'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
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
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'right_transfer',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['red']) == 0
    assert len(result['yellow']) == 0
    assert len(result['green']) == 5  # 4 individual greens + 1 acquired rights green
    assert any(r['condition'] == 'DigitalRepresentationCopyrightAcquired' for r in result['green'])

def test_employer_rights_changes_red_to_green():
    """Test that employer rights changes red status to green."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'employer_rights',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['red']) == 0
    assert len(result['yellow']) == 0
    assert len(result['green']) == 5  # 4 individual greens + 1 acquired rights green
    assert any(r['condition'] == 'DigitalRepresentationCopyrightAcquired' for r in result['green'])

def test_not_applicable_keeps_status():
    """Test that not_applicable doesn't change status."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'not_applicable',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['red']) == 1
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'

def test_rights_not_acquired_keeps_status():
    """Test that rights_not_acquired doesn't change status."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'rights_not_acquired',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['red']) == 1
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'

def test_unknown_keeps_status():
    """Test that unknown doesn't change status."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'unknown',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    assert len(result['red']) == 1
    assert len(result['yellow']) == 0
    assert len(result['green']) == 4  # Individual greens for other rights
    assert result['red'][0]['condition'] == 'DigitalRepresentationCopyrightStatus'

def test_mixed_rights_acquisition():
    """Test mixed scenarios of rights acquisition."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'yes',
            'film_fixation_rights': 'uncertain',
            'performance_rights': 'no',
            'other_ip_rights': 'yes'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'right_transfer',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'employer_rights',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'rights_not_acquired'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    # Should have 2 acquired rights (copyright and film), 1 red (other), 1 yellow (audio), 1 green (performance)
    assert len(result['red']) == 1  # other_ip_rights
    assert len(result['yellow']) == 1  # audio_recording_rights
    assert len(result['green']) == 3  # performance + 2 acquired rights
    
    # Check acquired rights are present
    acquired_conditions = {r['condition'] for r in result['green']}
    assert 'DigitalRepresentationCopyrightAcquired' in acquired_conditions
    assert 'DigitalRepresentationFilmFixationAcquired' in acquired_conditions

def test_digital_repr_rights_availability_cc_by_sa():
    """Test CC BY-SA upgrades status to YELLOW."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_rights_availability': {
            'copyright': 'cc_by_sa',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'CC BY-SA license' in r['explanation'] for r in result['yellow'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in result['red'])

def test_digital_repr_rights_availability_rights_assignment():
    """Test rights assignment upgrades status to GREEN."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_rights_availability': {
            'copyright': 'rights_assignment',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'acquired the rights through assignment' in r['explanation'] for r in result['green'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in result['red'])

def test_digital_repr_rights_availability_orphan_works():
    """Test orphan works upgrades status to YELLOW."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_rights_availability': {
            'copyright': 'orphan_works',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)

    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'orphan works provisions' in r['explanation'] for r in result['yellow'])
    assert not any(r['condition'] == 'DigitalRepresentationCopyrightStatus' for r in result['red'])

def test_digital_repr_rights_availability_multiple_rights():
    """Test handling multiple rights with different availability choices."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'yes',
            'film_fixation_rights': 'yes',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_rights_availability': {
            'copyright': 'cc0',
            'audio_recording_rights': 'cc_by_sa',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)

    # copyright should be green (cc0), audio should be yellow (cc_by_sa), film should be red (not_applicable)
    assert any(r['condition'] == 'DigitalRepresentationCopyrightStatus' 
              and 'CC0' in r['explanation'] for r in result['green'])
    assert any(r['condition'] == 'DigitalRepresentationPhonogramStatus' 
              and 'CC BY-SA license' in r['explanation'] for r in result['yellow'])
    assert any(r['condition'] == 'DigitalRepresentationFilmFixationStatus' for r in result['red'])

def test_used_variables_tracking():
    """Test that used variables are properly tracked."""
    data = {
        'digital_repr_ip_rights': {
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': 'right_transfer',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        },
        'digital_repr_rights_availability': {
            'copyright': 'cc0',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        }
    }
    result, used_vars = calculate_digital_representation_status(data)
    
    expected_vars = {'digital_repr_ip_rights', 'digital_repr_ip_rights_acquired', 'digital_repr_rights_availability'}
    assert used_vars == expected_vars 