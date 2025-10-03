import unittest
from utils import calculate_results, calculate_all_intermediate_values


def base_data():
    return {
        'object_name': 'Test',
        'institution_name': 'Inst',
        'authors': [{'identity_known': True, 'country_of_origin': 'DE'}],
        'created_before_1850': 'not_made_before_1850',

        'performance_info': {},
        'phonogram_info': {},
        'broadcast_info': {},
        'film_fixation_info': {},

        'digital_representation_info': {
            'digital_repr_ip_rights': {},
            'digital_repr_rights_availability': {},
            'digital_repr_ip_rights_acquired': {}
        }
    }


def run_digital_repr(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results['digital_repr_status']


class TestDigitalRepresentation(unittest.TestCase):
    def test_all_no_gives_green(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'no',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        })
        status = run_digital_repr(data)
        self.assertEqual(len(status['green']), 5)
        self.assertEqual(len(status['yellow']), 0)
        self.assertEqual(len(status['red']), 0)

    def test_single_yes_gives_red_and_individual_greens(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        })
        status = run_digital_repr(data)
        self.assertEqual(len(status['red']), 1)
        self.assertEqual(status['red'][0]['condition'], 'DigitalRepresentationCopyrightStatus')
        self.assertEqual(len(status['yellow']), 0)
        self.assertEqual(len(status['green']), 4)
        self.assertEqual(
            {r['condition'] for r in status['green']},
            {
                'DigitalRepresentationPhonogramStatus',
                'DigitalRepresentationFilmFixationStatus',
                'DigitalRepresentationPerformanceStatus',
                'DigitalRepresentationOtherIPStatus',
            },
        )

    def test_single_uncertain_gives_yellow_and_individual_greens(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'no',
            'audio_recording_rights': 'uncertain',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        })
        status = run_digital_repr(data)
        self.assertEqual(len(status['yellow']), 1)
        self.assertEqual(status['yellow'][0]['condition'], 'DigitalRepresentationPhonogramStatus')
        self.assertEqual(len(status['red']), 0)
        self.assertEqual(len(status['green']), 4)

    def test_mixed_statuses(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'yes',
            'audio_recording_rights': 'uncertain',
            'film_fixation_rights': 'yes',
            'performance_rights': 'no',
            'other_ip_rights': 'uncertain'
        })
        status = run_digital_repr(data)
        self.assertEqual(len(status['red']), 2)
        self.assertEqual(len(status['yellow']), 2)
        self.assertEqual(len(status['green']), 1)
        self.assertEqual(status['green'][0]['condition'], 'DigitalRepresentationPerformanceStatus')

    def test_status_names(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'yes',
            'audio_recording_rights': 'yes',
            'film_fixation_rights': 'yes',
            'performance_rights': 'yes',
            'other_ip_rights': 'yes'
        })
        status = run_digital_repr(data)
        status_names = {r['condition'] for r in status['red']}
        self.assertEqual(status_names, {
            'DigitalRepresentationCopyrightStatus',
            'DigitalRepresentationPhonogramStatus',
            'DigitalRepresentationFilmFixationStatus',
            'DigitalRepresentationPerformanceStatus',
            'DigitalRepresentationOtherIPStatus'
        })

    def test_rights_assignment_turns_red_to_green(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        })
        data['digital_representation_info']['digital_repr_rights_availability'].update({
            'copyright': 'rights_assignment',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        })
        status = run_digital_repr(data)
        self.assertEqual(len(status['red']), 0)
        self.assertEqual(len(status['yellow']), 0)
        self.assertEqual(len(status['green']), 5)
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationCopyrightStatus'
                            for r in status['green']))

    def test_cc_by_sa_turns_red_to_yellow(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'yes',
            'audio_recording_rights': 'no',
            'film_fixation_rights': 'no',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        })
        data['digital_representation_info']['digital_repr_rights_availability'].update({
            'copyright': 'cc_by_sa',
            'audio_recording_rights': 'not_applicable',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        })
        status = run_digital_repr(data)
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationCopyrightStatus'
                            and 'CC BY-SA license' in r['explanation'] for r in status['yellow']))
        self.assertFalse(any(r['condition'] == 'DigitalRepresentationCopyrightStatus'
                             for r in status['red']))

    def test_multiple_rights_mixed_availability(self):
        data = base_data()
        data['digital_representation_info']['digital_repr_ip_rights'].update({
            'copyright': 'yes',
            'audio_recording_rights': 'yes',
            'film_fixation_rights': 'yes',
            'performance_rights': 'no',
            'other_ip_rights': 'no'
        })
        data['digital_representation_info']['digital_repr_rights_availability'].update({
            'copyright': 'cc0',
            'audio_recording_rights': 'cc_by_sa',
            'film_fixation_rights': 'not_applicable',
            'performance_rights': 'not_applicable',
            'other_ip_rights': 'not_applicable'
        })
        status = run_digital_repr(data)
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationCopyrightStatus'
                            and 'CC0' in r['explanation'] for r in status['green']))
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationPhonogramStatus'
                            and 'CC BY-SA license' in r['explanation'] for r in status['yellow']))
        self.assertTrue(any(r['condition'] == 'DigitalRepresentationFilmFixationStatus' for r in status['red']))


if __name__ == '__main__':
    unittest.main()