from flask import Flask, render_template, request, jsonify
from datetime import datetime
from forms import CopyrightForm
from utils import calculate_intermediate_values, calculate_results, generate_markdown_report, generate_text_report
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
        
        # Performers
        'performers': [
            {
                'identity_known': not performer.is_anonymous.data,
                'country_of_origin': performer.country_of_origin.data
            }
            for performer in form.performers
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
    
    # Calculate intermediate values
    intermediate_values = calculate_intermediate_values(data)
    
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