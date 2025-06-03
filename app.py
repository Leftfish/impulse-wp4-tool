from flask import Flask, render_template, request, jsonify
from datetime import datetime
from forms import CopyrightForm
from utils import calculate_intermediate_values, calculate_results, generate_markdown_report, generate_text_report
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

COMPOUND_ALERT = "Caution, compound work!!!"

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
    # Convert form data to dictionary
    data = {
        'object_name': form.object_name.data,
        'institution_name': form.institution_name.data,
        'is_copyright_work': form.is_copyright_work.data,
        'created_before_1850': form.created_before_1850.data,
        'is_derivative': form.is_derivative.data,
        'is_compound': form.is_compound.data,
        'is_photography': form.is_photography.data,
        'authors': [
            {
                'identity_known': not author.is_anonymous.data,
                'country_of_origin': author.country_of_origin.data
            }
            for author in form.authors
        ],
        'creation_year': form.creation_year.data or 0,
        'physically_published': form.physically_published.data,
        'country_first_publication': form.country_first_publication.data,
        'simultaneous_publication_countries': [
            country.data for country in form.simultaneous_publication_countries
        ],
        'territory_status_changed': form.territory_status_changed.data,
        'cinematographic_country': form.cinematographic_country.data,
        'architecture_country': form.architecture_country.data,
        'otherwise_available': form.otherwise_available.data,
        'internet_first_available': form.internet_first_available.data,
        'first_publication_year': form.first_publication_year.data or 0,
        'first_available_year': form.first_available_year.data or 0,
        'original_rightholder': form.original_rightholder.data,
        'author_alive': form.author_alive.data,
        'author_death_year': form.author_death_year.data or 0,
        'current_rightholder': form.current_rightholder.data
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