import os
import json

from flask import Flask, render_template, request, jsonify
from forms import CopyrightForm
from utils import calculate_all_intermediate_values, calculate_results
from reports import generate_markdown_report, generate_text_report
import markdown
import secrets
from dotenv import load_dotenv
from constants import APP_VERSION


# Load environment variables from .env file
load_dotenv()

DEBUG = os.getenv("FLASK_DEBUG", "").lower() in ("", "1", "true", "yes", "on")

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_hex(32))

@app.context_processor
def inject_app_version():
    return {"app_version": APP_VERSION}


@app.after_request
def add_version_header(response):
    response.headers["X-App-Version"] = APP_VERSION
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    form = CopyrightForm()
    if request.method == "POST":
        if form.validate_on_submit():
            result = process_form(form)
            return jsonify(result)
        else:
            # Log validation errors
            print("=" * 50)
            print("FORM VALIDATION FAILED")
            print("=" * 50)
            print(json.dumps(form.errors, indent=2, default=str))
            print("=" * 50)
    return render_template("index.html", form=form)

@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/explanations")
def explanations():
    return render_template("explanations.html")


@app.get("/version")
def version():
    return jsonify({"version": APP_VERSION})


def process_form(form):
    """Process the form data and return results."""
    data = {
        # Basic information
        "object_name": form.object_name.data,
        "institution_name": form.institution_name.data,
        "object_collection_ownership": form.object_collection_ownership.data,
        "object_url": form.object_url.data,
        "general_notes": form.general_notes.data,
        "copyright_info": {
            "is_copyright_work": form.is_copyright_work.data,
            "is_derivative": form.is_derivative.data,
            "is_compound": form.is_compound.data,
            "is_collective": form.is_collective.data,
            "is_photography": form.is_photography.data,
            "authors": [
                {
                    "identity_known": not author.is_anonymous.data,
                    "country_of_origin": author.country_of_origin.data,
                }
                for author in form.authors
            ],
            "creation_year": form.creation_year.data,
            "created_before_1850": form.created_before_1850.data,
            "physically_published": form.physically_published.data,
            "country_first_publication": form.country_first_publication.data,
            "simultaneous_publication_countries": form.simultaneous_publication_countries.data,
            "territory_status_changed": form.territory_status_changed.data,
            "cinematographic_country": form.cinematographic_country.data,
            "architecture_country": form.architecture_country.data,
            "otherwise_available": form.otherwise_available.data,
            "internet_first_available": form.internet_first_available.data,
            "first_publication_year": form.first_publication_year.data,
            "first_available_year": form.first_available_year.data,
            "original_rightholder": form.original_rightholder.data,
            "author_alive": form.author_alive.data,
            "author_death_year": form.author_death_year.data,
            "current_rightholder": form.current_rightholder.data,
            "object_cc_license": form.object_cc_license.data,
            "object_copyright_rights_acquired_to_make_available": form.object_copyright_rights_acquired_to_make_available.data,
        },
        "performance_info": {
            "performers": [
                {
                    "identity_known": not performer.is_anonymous.data,
                    "country_of_origin": performer.country_of_origin.data,
                }
                for performer in form.performers
            ],
            "is_performance": form.is_performance.data,
            "performance_before_1900": form.performance_before_1900.data,
            "is_compound_performance": form.is_compound_performance.data,
            "performance_year": form.performance_year.data,
            "performance_phonogram_available": form.performance_phonogram_available.data,
            "performance_phonogram_available_year": form.performance_phonogram_available_year.data,
            "performance_fixed_not_phonogram_available": form.performance_fixed_not_phonogram_available.data,
            "performance_fixed_not_phonogram_available_year": form.performance_fixed_not_phonogram_available_year.data,
            "performance_current_rightholder": form.performance_current_rightholder.data,
            "performance_cc_license": form.performance_cc_license.data,
            "performance_rights_acquired_to_make_available": form.performance_rights_acquired_to_make_available.data,
        },
        "phonogram_info": {
            "phonogram_producers": [
                {
                    "country_of_origin": producer.country_of_origin.data,
                }
                for producer in form.producers
            ],
            "is_phonogram": form.is_phonogram.data,
            "phonogram_before_1900": form.phonogram_before_1900.data,
            "is_compound_phonogram": form.is_compound_phonogram.data,
            "phonogram_year": form.phonogram_year.data,
            "phonogram_published_fixed_medium": form.phonogram_published_fixed_medium.data,
            "phonogram_published_fixed_medium_year": form.phonogram_published_fixed_medium_year.data,
            "phonogram_available_no_medium": form.phonogram_available_no_medium.data,
            "phonogram_available_no_medium_year": form.phonogram_available_no_medium_year.data,
            "phonogram_current_rightholder": form.phonogram_current_rightholder.data,
            "phonogram_cc_license": form.phonogram_cc_license.data,
            "phonogram_rights_acquired_to_make_available": form.phonogram_rights_acquired_to_make_available.data,
        },
        "broadcast_info": {
            "is_broadcast": form.is_broadcast.data,
            "broadcast_before_1970": form.broadcast_before_1970.data,
            "is_compound_broadcast": form.is_compound_broadcast.data,
            "broadcast_year": form.broadcast_year.data,
            "broadcast_current_rightholder": form.broadcast_current_rightholder.data,
            "broadcast_cc_license": form.broadcast_cc_license.data,
            "broadcast_rights_acquired_to_make_available": form.broadcast_rights_acquired_to_make_available.data,
            "broadcasters": [
                {
                    "country_of_origin": broadcaster.country_of_origin.data,
                }
                for broadcaster in form.broadcasters
            ],
        },
        "film_fixation_info": {
            "film_fixation_producers": [
                {
                    "country_of_origin": producer.country_of_origin.data,
                }
                for producer in form.film_fixation_producers
            ],
            "is_film_fixation": form.is_film_fixation.data,
            "film_fixation_before_1920": form.film_fixation_before_1920.data,
            "is_compound_film_fixation": form.is_compound_film_fixation.data,
            "film_fixation_year": form.film_fixation_year.data,
            "film_fixation_published_fixed_medium": form.film_fixation_published_fixed_medium.data,
            "film_fixation_published_fixed_medium_year": form.film_fixation_published_fixed_medium_year.data,
            "film_fixation_available_no_medium": form.film_fixation_available_no_medium.data,
            "film_fixation_available_no_medium_year": form.film_fixation_available_no_medium_year.data,
            "film_fixation_current_rightholder": form.film_fixation_current_rightholder.data,
            "film_fixation_cc_license": form.film_fixation_cc_license.data,
            "film_fixation_rights_acquired_to_make_available": form.film_fixation_rights_acquired_to_make_available.data,
        },
        "other_intellectual_property_info": {
            "potential_first_edition_not_work": form.potential_first_edition_not_work.data,
            "critical_edition": form.critical_edition.data,
            "press_publication": form.press_publication.data,
            "press_publication_year": form.press_publication_year.data,
            "trademark": form.trademark.data,
            "design": form.design.data,
        },
        "digital_representation_info": {
            "digital_repr_nature": form.digital_repr_nature.data,
            "visual_art_work": form.visual_art_work.data,
            "digital_repr_with_ai": form.digital_repr_with_ai.data,
            "digital_repr_ip_rights": {
                "copyright": form.digital_repr_ip_rights.copyright.data,
                "phonogram_rights": form.digital_repr_ip_rights.phonogram_rights.data,
                "film_fixation_rights": form.digital_repr_ip_rights.film_fixation_rights.data,
                "other_ip_rights": form.digital_repr_ip_rights.other_ip_rights.data,
            },
            
            # Separate questions for copyright
            "digital_repr_copyright_current_rightholder": form.digital_repr_copyright_current_rightholder.data,
            "digital_repr_copyright_cc_license": form.digital_repr_copyright_cc_license.data,
            "digital_repr_copyright_rights_acquired": form.digital_repr_copyright_rights_acquired.data,
            # Separate questions for phonogram (audio recording rights)
            "digital_repr_phonogram_current_rightholder": form.digital_repr_phonogram_current_rightholder.data,
            "digital_repr_phonogram_cc_license": form.digital_repr_phonogram_cc_license.data,
            "digital_repr_phonogram_rights_acquired": form.digital_repr_phonogram_rights_acquired.data,
            # Separate questions for film fixation
            "digital_repr_film_fixation_current_rightholder": form.digital_repr_film_fixation_current_rightholder.data,
            "digital_repr_film_fixation_cc_license": form.digital_repr_film_fixation_cc_license.data,
            "digital_repr_film_fixation_rights_acquired": form.digital_repr_film_fixation_rights_acquired.data,
            # Separate questions for other IP rights
            "digital_repr_other_current_rightholder": form.digital_repr_other_current_rightholder.data,
            "digital_repr_other_cc_license": form.digital_repr_other_cc_license.data,
            "digital_repr_other_rights_acquired": form.digital_repr_other_rights_acquired.data,
        },
        "other_restrictions_info": {
            "object_contractual_restrictions": form.object_contractual_restrictions.data,
            "object_administrative_restrictions": form.object_administrative_restrictions.data,
            "object_ownership_status": form.object_ownership_status.data,
            "object_provenance_traced": form.object_provenance_traced.data,
            "object_provenance_issues": form.object_provenance_issues.data,
            "object_living_identifiable_info": form.object_living_identifiable_info.data,
            "object_sensitive_historical_info": form.object_sensitive_historical_info.data,
            "object_totalitarian_associations": form.object_totalitarian_associations.data,
            "object_discriminatory_content": form.object_discriminatory_content.data,
            "object_other_sensitive_content": form.object_other_sensitive_content.data,
            "object_other_problems": form.object_other_problems.data,
            "object_legal_consultation": form.object_legal_consultation.data,
            "object_restrictions_notes": form.object_restrictions_notes.data,
        },
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

    return {"html": html_report, "text": text_report, "results": results}


if __name__ == "__main__":
    app.run(debug=DEBUG)
