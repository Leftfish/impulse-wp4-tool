from flask import Flask, render_template, request, jsonify
from datetime import datetime
from forms import CopyrightForm
from utils import calculate_all_intermediate_values, calculate_results, generate_markdown_report, generate_text_report
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # to be changed later, for now we are just testing

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CopyrightForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            result = process_form(form)
            return jsonify(result)
    return render_template('index.html', form=form)

def process_form(form):
    """Process the form data and return results."""
    data = {
        # Basic information
        'object_name': form.object_name.data,
        'institution_name': form.institution_name.data,
        'object_url': form.object_url.data,
        
        # Work type
        'is_copyright_work': form.is_copyright_work.data,
        'is_derivative': form.is_derivative.data,
        'is_compound': form.is_compound.data,
        'is_photography': form.is_photography.data,
        
        # Authors
        'authors': [
            {
                'identity_known': not author.is_anonymous.data,
                'country_of_origin': author.country_of_origin.data
            }
            for author in form.authors
        ],
        
        # Creation and publication
        'creation_year': form.creation_year.data,
        'created_before_1850': form.created_before_1850.data,
        'physically_published': form.physically_published.data,
        'country_first_publication': form.country_first_publication.data,
        'simultaneous_publication_countries': form.simultaneous_publication_countries.data,
        'territory_status_changed': form.territory_status_changed.data,
        'cinematographic_country': form.cinematographic_country.data,
        'architecture_country': form.architecture_country.data,
        'otherwise_available': form.otherwise_available.data,
        'internet_first_available': form.internet_first_available.data,
        'first_publication_year': form.first_publication_year.data,
        'first_available_year': form.first_available_year.data,
        
        # Rights ownership
        'original_rightholder': form.original_rightholder.data,
        'author_alive': form.author_alive.data,
        'author_death_year': form.author_death_year.data,
        'current_rightholder': form.current_rightholder.data,
        
        # Object rights
        'object_cc_license': form.object_cc_license.data,
        'object_copyright_rights_acquired_to_make_available': form.object_copyright_rights_acquired_to_make_available.data,
        
        # Performers
        'performers': [
            {
                'identity_known': not performer.is_anonymous.data,
                'country_of_origin': performer.country_of_origin.data
            }
            for performer in form.performers
        ],
        
        # Performance section
        'is_performance': form.is_performance.data,
        'performance_before_1900': form.performance_before_1900.data,
        'is_compound_performance': form.is_compound_performance.data,
        'performance_year': form.performance_year.data,
        'performance_phonogram_available': form.performance_phonogram_available.data,
        'performance_phonogram_available_year': form.performance_phonogram_available_year.data,
        'performance_available_no_medium': form.performance_available_no_medium.data,
        'performance_available_no_medium_year': form.performance_available_no_medium_year.data,
        'performance_fixed_not_phonogram_available': form.performance_fixed_not_phonogram_available.data,
        'performance_fixed_not_phonogram_available_year': form.performance_fixed_not_phonogram_available_year.data,
        'performance_current_rightholder': form.performance_current_rightholder.data,
        'performance_cc_license': form.performance_cc_license.data,
        'performance_rights_acquired_to_make_available': form.performance_rights_acquired_to_make_available.data,

        # Producers (for phonograms)
        'phonogram_producers': [
            {
                'identity_known': not producer.is_anonymous.data,
                'country_of_origin': producer.country_of_origin.data
            }
            for producer in form.producers
        ],
        
        # Phonogram section
        'is_phonogram': form.is_phonogram.data,
        'phonogram_before_1900': form.phonogram_before_1900.data,
        'is_compound_phonogram': form.is_compound_phonogram.data,
        'phonogram_year': form.phonogram_year.data,
        'phonogram_published_fixed_medium': form.phonogram_published_fixed_medium.data,
        'phonogram_published_fixed_medium_year': form.phonogram_published_fixed_medium_year.data,
        'phonogram_available_no_medium': form.phonogram_available_no_medium.data,
        'phonogram_available_no_medium_year': form.phonogram_available_no_medium_year.data,
        'phonogram_current_rightholder': form.phonogram_current_rightholder.data,
        'phonogram_cc_license': form.phonogram_cc_license.data,
        'phonogram_rights_acquired_to_make_available': form.phonogram_rights_acquired_to_make_available.data,

        # Broadcasters (for broadcasting organisation rights)
        'broadcasters': [
            {
                'identity_known': not broadcaster.is_anonymous.data,
                'country_of_origin': broadcaster.country_of_origin.data
            }
            for broadcaster in form.broadcasters
        ],
        
        # Broadcasting organisation rights section
        'is_broadcast': form.is_broadcast.data,
        'broadcast_before_1970': form.broadcast_before_1970.data,
        'is_compound_broadcast': form.is_compound_broadcast.data,
        'broadcast_year': form.broadcast_year.data,
        'broadcast_current_rightholder': form.broadcast_current_rightholder.data,
        'broadcast_cc_license': form.broadcast_cc_license.data,
        'broadcast_rights_acquired_to_make_available': form.broadcast_rights_acquired_to_make_available.data,

        # Film fixation producers (for film fixations)
        'film_fixation_producers': [
            {
                'identity_known': not producer.is_anonymous.data,
                'country_of_origin': producer.country_of_origin.data
            }
            for producer in form.film_fixation_producers
        ],
        
        # Film fixation section
        'is_film_fixation': form.is_film_fixation.data,
        'film_fixation_before_1900': form.film_fixation_before_1900.data,
        'is_compound_film_fixation': form.is_compound_film_fixation.data,
        'film_fixation_year': form.film_fixation_year.data,
        'film_fixation_published_fixed_medium': form.film_fixation_published_fixed_medium.data,
        'film_fixation_published_fixed_medium_year': form.film_fixation_published_fixed_medium_year.data,
        'film_fixation_available_no_medium': form.film_fixation_available_no_medium.data,
        'film_fixation_available_no_medium_year': form.film_fixation_available_no_medium_year.data,
        'film_fixation_current_rightholder': form.film_fixation_current_rightholder.data,
        'film_fixation_cc_license': form.film_fixation_cc_license.data,
        'film_fixation_rights_acquired_to_make_available': form.film_fixation_rights_acquired_to_make_available.data,

        # Digital representation data
        'digital_repr_nature': form.digital_repr_nature.data,
        'digital_repr_ip_rights': {
            'copyright': form.digital_repr_ip_rights.copyright.data,
            'audio_recording_rights': form.digital_repr_ip_rights.audio_recording_rights.data,
            'film_fixation_rights': form.digital_repr_ip_rights.film_fixation_rights.data,
            'performance_rights': form.digital_repr_ip_rights.performance_rights.data,
            'other_ip_rights': form.digital_repr_ip_rights.other_ip_rights.data
        },
        'digital_repr_ip_rights_acquired': {
            'copyright': form.digital_repr_ip_rights_acquired.copyright.data,
            'audio_recording_rights': form.digital_repr_ip_rights_acquired.audio_recording_rights.data,
            'film_fixation_rights': form.digital_repr_ip_rights_acquired.film_fixation_rights.data,
            'performance_rights': form.digital_repr_ip_rights_acquired.performance_rights.data,
            'other_ip_rights': form.digital_repr_ip_rights_acquired.other_ip_rights.data
        },
        'digital_repr_cc_license': form.digital_repr_cc_license.data,
        'digital_repr_rights_acquired_to_make_available': form.digital_repr_rights_acquired_to_make_available.data,
        
        # Add rights availability data
        'digital_repr_rights_availability': {
            'copyright': form.digital_repr_rights_availability.copyright.data,
            'audio_recording_rights': form.digital_repr_rights_availability.audio_recording_rights.data,
            'film_fixation_rights': form.digital_repr_rights_availability.film_fixation_rights.data,
            'performance_rights': form.digital_repr_rights_availability.performance_rights.data,
            'other_ip_rights': form.digital_repr_rights_availability.other_ip_rights.data
        }
    }
    
    # Calculate unified intermediate values (copyright + performance)
    intermediate_values = calculate_all_intermediate_values(data)
    
    # Calculate results
    results = calculate_results(data, intermediate_values)
    
    # Generate markdown report for HTML display
    md_report = generate_markdown_report(results)
    html_report = markdown.markdown(md_report)
    
    # Generate plain text report for download
    text_report = generate_text_report(results)
    
    return {
        'html': html_report,
        'text': text_report,
        'results': results
    }

if __name__ == '__main__':
    app.run(debug=True) 