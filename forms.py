"""
Forms module for the copyright assessment tool.

This module defines the form structure and validation logic for the copyright assessment tool.
It includes forms for author information, IP rights, and comprehensive copyright status evaluation.
The module uses Flask-WTF for form handling and implements nested form structures for complex
data relationships.
"""

from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    FieldList,
    FormField,
    BooleanField,
    SelectMultipleField,
    RadioField,
    TextAreaField,
)
from wtforms.validators import Optional, NumberRange, Length
from data.country_codes import COUNTRY_CODES, is_eea_country, is_eu_country

from constants import *


class ProducerForm(FlaskForm):
    """
    Subform for producer-specific information.

    This form captures details about individual producers, including their identity status
    and country of origin. It's used as a nested form within CopyrightForm, allowing
    for multiple producers to be added dynamically.
    """

    class Meta:
        # Disable CSRF for subform to prevent token validation issues in nested forms
        csrf = False

    #is_anonymous = BooleanField("The producer is unknown")
    country_of_origin = SelectField(
        "Country of origin of the producer", choices=COUNTRY_CODES, default="EU"
    )

    def get_country_status(self):
        """
        Determine the EU/EEA status of the producer's country.

        Returns:
            dict: Contains boolean flags for EU and EEA membership status
        """
        return {
            "is_eu": is_eu_country(self.country_of_origin.data),
            "is_eea": is_eea_country(self.country_of_origin.data),
        }


class PerformerForm(FlaskForm):
    """
    Subform for performer-specific information.

    This form captures details about individual performers, including their identity status
    and country of origin. It's used as a nested form within CopyrightForm, allowing
    for multiple performers to be added dynamically.
    """

    class Meta:
        # Disable CSRF for subform to prevent token validation issues in nested forms
        csrf = False

    is_anonymous = BooleanField("Performer is anonymous or pseudonymous")
    country_of_origin = SelectField(
        "Country of origin of the performer", choices=COUNTRY_CODES, default="EU"
    )

    def get_country_status(self):
        """
        Determine the EU/EEA status of the performer's country.

        Returns:
            dict: Contains boolean flags for EU and EEA membership status
        """
        return {
            "is_eu": is_eu_country(self.country_of_origin.data),
            "is_eea": is_eea_country(self.country_of_origin.data),
        }


class AuthorForm(FlaskForm):
    """
    Subform for author-specific information.

    This form captures details about individual authors, including their anonymity status
    and country of origin. It's used as a nested form within CopyrightForm, allowing
    for multiple authors to be added dynamically.
    """

    class Meta:
        # Disable CSRF for subform to prevent token validation issues in nested forms
        csrf = False

    is_anonymous = BooleanField("Author is anonymous or pseudonymous")
    country_of_origin = SelectField(
        "Country of origin of the author", choices=COUNTRY_CODES, default="EU"
    )

    def get_country_status(self):
        """
        Determine the EU/EEA status of the author's country.

        Returns:
            dict: Contains boolean flags for EU and EEA membership status
        """
        return {
            "is_eu": is_eu_country(self.country_of_origin.data),
            "is_eea": is_eea_country(self.country_of_origin.data),
        }


class BroadcasterForm(FlaskForm):
    """
    Subform for broadcasting organisation-specific information.
    Mirrors ProducerForm: captures identity status and country of origin.
    """

    class Meta:
        csrf = False

    #is_anonymous = BooleanField("The broadcasting organisation is unknown")
    country_of_origin = SelectField(
        "Country of origin of the broadcasting organisation", choices=COUNTRY_CODES, default="EU"
    )


class IPRightsForm(FlaskForm):
    """
    Form for capturing IP rights coverage information.

    Handles the assessment of different types of IP rights that may apply to
    the digital representation. All fields default to 'no' to ensure conservative
    rights assessment.
    """

    class Meta:
        csrf = False

    # Each field represents a different type of IP right
    # Default value is set to 'no' for conservative rights assessment
    copyright = SelectField(
        IP_RIGHTS_COPYRIGHT_LABEL,
        description=IP_RIGHTS_CHOICES_DESCRIPTION[IP_RIGHTS_COPYRIGHT_LABEL],
        choices=IP_RIGHTS_CHOICES,
        default="no",
    )
    phonogram_rights = SelectField(
        IP_RIGHTS_AUDIO_RECORDINGS_LABEL,
        description=IP_RIGHTS_CHOICES_DESCRIPTION[IP_RIGHTS_AUDIO_RECORDINGS_LABEL],
        choices=IP_RIGHTS_CHOICES,
        default="no",
    )
    film_fixation_rights = SelectField(
        IP_RIGHTS_FILM_FIXATION_LABEL,
        description=IP_RIGHTS_CHOICES_DESCRIPTION[IP_RIGHTS_FILM_FIXATION_LABEL],
        choices=IP_RIGHTS_CHOICES,
        default="no",
    )

    other_ip_rights = SelectField(
        IP_RIGHTS_OTHER_LABEL,
        description=IP_RIGHTS_CHOICES_DESCRIPTION[IP_RIGHTS_OTHER_LABEL],
        choices=IP_RIGHTS_CHOICES,
        default="no",
    )

class CopyrightForm(FlaskForm):
    """
    Main form for copyright assessment.

    This is the primary form that integrates all subforms and captures comprehensive
    information about an object's copyright status.

    The form uses nested structures (FieldList, FormField) to handle complex
    relationships like multiple authors and various types of rights.
    """

    # Section descriptions
    original_object_description = StringField(
        SECTION_ORIGINAL_OBJECT_TITLE, description=SECTION_ORIGINAL_OBJECT_DESCRIPTION
    )

    author_info_description = StringField(
        SECTION_AUTHOR_INFO_TITLE, description=SECTION_AUTHOR_INFO_DESCRIPTION
    )
    
    author_identity_help = StringField(
        "Author Identity Help", description=AUTHOR_IDENTITY_HELP
    )

    creation_publication_description = StringField(
        SECTION_CREATION_PUBLICATION_TITLE,
        description=SECTION_CREATION_PUBLICATION_DESCRIPTION,
    )

    publication_dates_description = StringField(
        SECTION_PUBLICATION_DATES_TITLE,
        description=SECTION_PUBLICATION_DATES_DESCRIPTION,
    )

    rights_info_description = StringField(
        SECTION_RIGHTS_INFO_TITLE, description=SECTION_RIGHTS_INFO_DESCRIPTION
    )

    digital_repr_description = StringField(
        SECTION_DIGITAL_REPR_TITLE, description=SECTION_DIGITAL_REPR_DESCRIPTION
    )

    ip_rights_coverage_description = StringField(
        SECTION_IP_RIGHTS_COVERAGE_TITLE,
        description=SECTION_IP_RIGHTS_COVERAGE_DESCRIPTION,
    )

    digital_repr_rights_availability_description = StringField(
        "Digital Representation Rights Availability",
        description=DIGITAL_REPR_RIGHTS_AVAILABILITY_DESCRIPTION,
    )

    # Basic Information section
    object_name = StringField(OBJECT_NAME_LABEL, description=OBJECT_NAME_DESCRIPTION)

    institution_name = SelectField(
        INSTITUTION_NAME_LABEL,
        description=INSTITUTION_NAME_DESCRIPTION,
        choices=COLLECTION_CHOICES,
    )

    object_collection_ownership = RadioField(
        OBJECT_COLLECTION_OWNERSHIP_LABEL,
        description=OBJECT_COLLECTION_OWNERSHIP_DESCRIPTION,
        choices=OBJECT_COLLECTION_OWNERSHIP_CHOICES,
        default="own_collection",
    )

    object_url = StringField(OBJECT_URL_LABEL, description=OBJECT_URL_DESCRIPTION)

    # General section - Copyright work status
    is_copyright_work = SelectField(
        COPYRIGHT_IS_WORK_QUESTION,
        description=COPYRIGHT_IS_WORK_DESCRIPTION,
        choices=COPYRIGHT_IS_WORK_CHOICES,
        default=COPYRIGHT_IS_WORK_CHOICES[1][0],  # not_work
    )

    # Work characteristics
    created_before_1850 = SelectField(
        COPYRIGHT_IS_BEFORE_1850_QUESTION,
        description=COPYRIGHT_IS_BEFORE_1850_DESCRIPTION,
        choices=COPYRIGHT_IS_BEFORE_1850_CHOICES,
    )

    is_derivative = SelectField(
        COPYRIGHT_IS_DERIVATIVE_QUESTION,
        description=COPYRIGHT_IS_DERIVATIVE_DESCRIPTION,
        choices=COPYRIGHT_IS_DERIVATIVE_CHOICES
    )

    is_compound = SelectField(
        COPYRIGHT_IS_COMPOUND_QUESTION,
        description=COPYRIGHT_IS_COMPOUND_DESCRIPTION,
        choices=COPYRIGHT_IS_COMPOUND_CHOICES
    )

    is_photography = SelectField(
        COPYRIGHT_IS_PHOTOGRAPHY_QUESTION, choices=COPYRIGHT_IS_PHOTOGRAPHY_CHOICES
    )

    is_collective = SelectField(
        COPYRIGHT_IS_COLLECTIVE_WORK_QUESTION,
        description=COPYRIGHT_IS_COLLECTIVE_WORK_DESCRIPTION,
        choices=COPYRIGHT_IS_COLLECTIVE_WORK_CHOICES
    )

    # Authors information - supports multiple authors
    authors = FieldList(FormField(AuthorForm), min_entries=1)

    # Creation and publication details
    creation_year = IntegerField(
        COPYRIGHT_CREATION_YEAR_LABEL,
        description=COPYRIGHT_CREATION_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    physically_published = SelectField(
        COPYRIGHT_PHYSICALLY_PUBLISHED_QUESTION,
        description=COPYRIGHT_PHYSICALLY_PUBLISHED_DESCRIPTION,
        choices=COPYRIGHT_PHYSICALLY_PUBLISHED_CHOICES,
    )

    # Publication location information
    country_first_publication = SelectField(
        COPYRIGHT_COUNTRY_FIRST_PUBLICATION_QUESTION,
        description=COPYRIGHT_COUNTRY_FIRST_PUBLICATION_DESCRIPTION,
        choices=COUNTRY_CODES,
        default="EU",
    )

    # Handle simultaneous publications in multiple countries
    simultaneous_publication_countries = FieldList(
        SelectField(
            COPYRIGHT_SIMULTANEOUS_PUBLICATION_COUNTRY_QUESTION, choices=COUNTRY_CODES
        ),
        min_entries=1,
    )

    territory_status_changed = BooleanField(COPYRIGHT_TERRITORY_STATUS_CHANGED_LABEL)

    # Special cases handling
    cinematographic_country = SelectField(
        CINEMATOGRAPHIC_COUNTRY_LABEL,
        description=CINEMATOGRAPHIC_COUNTRY_DESCRIPTION,
        choices=COUNTRY_CODES,
    )

    architecture_country = SelectField(
        ARCHITECTURE_COUNTRY_LABEL, choices=COUNTRY_CODES
    )

    # Publication and availability details
    otherwise_available = SelectField(
        COPYRIGHT_OTHERWISE_AVAILABLE_QUESTION,
        choices=COPYRIGHT_OTHERWISE_AVAILABLE_CHOICES,
    )

    internet_first_available = SelectField(
        COPYRIGHT_INTERNET_FIRST_AVAILABLE_QUESTION,
        choices=COPYRIGHT_INTERNET_FIRST_AVAILABLE_CHOICES,
    )

    # Publication dates
    first_publication_year = IntegerField(
        COPYRIGHT_FIRST_PUBLICATION_YEAR_QUESTION,
        description=COPYRIGHT_FIRST_PUBLICATION_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    first_available_year = IntegerField(
        COPYRIGHT_FIRST_AVAILABLE_YEAR_QUESTION,
        description=COPYRIGHT_FIRST_AVAILABLE_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    # Rights ownership information
    original_rightholder = SelectField(
        COPYRIGHT_ORIGINAL_RIGHTHOLDER_LABEL,
        description=COPYRIGHT_ORIGINAL_RIGHTHOLDER_DESCRIPTION,
        choices=COPYRIGHT_ORIGINAL_RIGHTHOLDER_CHOICES,
    )

    # Author status
    author_alive = SelectField(
        COPYRIGHT_AUTHOR_ALIVE_LABEL, choices=COPYRIGHT_AUTHOR_ALIVE_CHOICES
    )

    author_death_year = IntegerField(
        COPYRIGHT_AUTHOR_DEATH_YEAR_LABEL,
        description=COPYRIGHT_AUTHOR_DEATH_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['copyright'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['copyright'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )

    object_cc_license = SelectField(
        CC_LICENSE_LABEL['copyright'],
        #description=CC_LICENSE_DESCRIPTION['copyright'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    object_copyright_rights_acquired_to_make_available = SelectField(
        RIGHTS_ACQUIRED_LABEL['copyright'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['copyright'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    # Performance rights section
    performance_description = StringField(
        SECTION_PERFORMANCE_TITLE, description=SECTION_PERFORMANCE_DESCRIPTION
    )
    
    performer_identity_help = StringField(
        "Performer Identity Help", description=PERFORMER_IDENTITY_HELP
    )

    is_performance = SelectField(
        PERFORMANCE_IS_PERFORMANCE_QUESTION,
        description=PERFORMANCE_IS_PERFORMANCE_DESCRIPTION,
        choices=PERFORMANCE_CHOICES,
    )

    performance_before_1900 = SelectField(
        PERFORMANCE_BEFORE_1900_QUESTION, 
        description=PERFORMANCE_BEFORE_1900_DESCRIPTION,
        choices=PERFORMANCE_BEFORE_1900_CHOICES
    )

    is_compound_performance = SelectField(
        PERFORMANCE_IS_COMPOUND_QUESTION, choices=PERFORMANCE_COMPOUND_CHOICES
    )

    # Performers information - supports multiple performers
    performers = FieldList(FormField(PerformerForm), min_entries=1)

    performance_year = IntegerField(
        PERFORMANCE_YEAR_QUESTION,
        description=PERFORMANCE_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    performance_phonogram_available = SelectField(
        PERFORMANCE_PHONOGRAM_AVAILABLE_QUESTION,
        description=PERFORMANCE_PHONOGRAM_AVAILABLE_DESCRIPTION,
        choices=PERFORMANCE_PHONOGRAM_AVAILABLE_CHOICES,
        default="performance_phonogram_not_available"
    )

    performance_phonogram_available_year = IntegerField(
        PERFORMANCE_PHONOGRAM_AVAILABLE_YEAR_QUESTION,
        description=PERFORMANCE_PHONOGRAM_AVAILABLE_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    performance_fixed_not_phonogram_available = SelectField(
        PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_QUESTION,
        description=PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_DESCRIPTION,
        choices=PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_CHOICES,
        default="performance_fixed_not_phonogram_not_available"
    )

    performance_fixed_not_phonogram_available_year = IntegerField(
        PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_YEAR_QUESTION,
        description=PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    performance_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['performance'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['performance'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )

    performance_cc_license = SelectField(
        CC_LICENSE_LABEL['performance'],
        #description=CC_LICENSE_DESCRIPTION['performance'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    performance_rights_acquired_to_make_available = SelectField(
        RIGHTS_ACQUIRED_LABEL['performance'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['performance'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    # Phonogram rights section
    phonogram_description = StringField(
        SECTION_PHONOGRAM_TITLE, description=SECTION_PHONOGRAM_DESCRIPTION
    )
    
    producer_identity_help = StringField(
        "Producer Identity Help", description=PRODUCER_IDENTITY_HELP
    )

    is_phonogram = SelectField(
        PHONOGRAM_IS_PHONOGRAM_QUESTION,
        description=PHONOGRAM_IS_PHONOGRAM_DESCRIPTION,
        choices=PHONOGRAM_CHOICES,
    )

    phonogram_before_1900 = SelectField(
        PHONOGRAM_BEFORE_1900_QUESTION, choices=PHONOGRAM_BEFORE_1900_CHOICES
    )

    is_compound_phonogram = SelectField(
        PHONOGRAM_IS_COMPOUND_QUESTION,
        description=PHONOGRAM_IS_COMPOUND_DESCRIPTION,
        choices=COMPOUND_PHONOGRAM_CHOICES,
    )

    # Producers information - supports multiple producers
    producers = FieldList(FormField(ProducerForm), min_entries=1)

    phonogram_year = IntegerField(
        PHONOGRAM_YEAR_QUESTION,
        description=PHONOGRAM_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    phonogram_published_fixed_medium = SelectField(
        PHONOGRAM_PUBLISHED_FIXED_MEDIUM_QUESTION,
        description=PHONOGRAM_PUBLISHED_FIXED_MEDIUM_DESCRIPTION,
        choices=PHONOGRAM_PUBLISHED_FIXED_MEDIUM_CHOICES,
        default="phonogram_not_published_fixed_medium"
    )

    phonogram_published_fixed_medium_year = IntegerField(
        PHONOGRAM_PUBLISHED_FIXED_MEDIUM_YEAR_QUESTION,
        description=PHONOGRAM_PUBLISHED_FIXED_MEDIUM_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    phonogram_available_no_medium = SelectField(
        PHONOGRAM_AVAILABLE_NO_MEDIUM_QUESTION,
        description=PHONOGRAM_AVAILABLE_NO_MEDIUM_DESCRIPTION,
        choices=PHONOGRAM_NO_MEDIUM_CHOICES,
        default="phonogram_not_publically_available_no_medium"
    )

    phonogram_available_no_medium_year = IntegerField(
        PHONOGRAM_AVAILABLE_NO_MEDIUM_YEAR_QUESTION,
        description=PHONOGRAM_AVAILABLE_NO_MEDIUM_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    phonogram_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['audio_recordings'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['audio_recordings'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )

    phonogram_cc_license = SelectField(
        CC_LICENSE_LABEL['audio_recordings'],
        #description=CC_LICENSE_DESCRIPTION['audio_recordings'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    phonogram_rights_acquired_to_make_available = SelectField(
        RIGHTS_ACQUIRED_LABEL['audio_recordings'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['audio_recordings'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    # Film fixation rights section
    film_fixation_description = StringField(
        SECTION_FILM_FIXATION_TITLE, description=SECTION_FILM_FIXATION_DESCRIPTION
    )
    
    film_fixation_producer_identity_help = StringField(
        "Film Fixation Producer Identity Help", description=FILM_FIXATION_PRODUCER_IDENTITY_HELP
    )

    is_film_fixation = SelectField(
        FILM_IS_FILM_FIXATION_QUESTION,
        description=FILM_IS_FILM_FIXATION_DESCRIPTION,
        choices=FILM_FIXATION_CHOICES,
    )

    film_fixation_before_1920 = SelectField(
        FILM_BEFORE_1920_QUESTION, choices=FILM_FIXATION_BEFORE_1920_CHOICES
    )

    is_compound_film_fixation = SelectField(
        FILM_IS_COMPOUND_QUESTION,
        description=FILM_IS_COMPOUND_DESCRIPTION,
        choices=COMPOUND_FILM_FIXATION_CHOICES,
    )

    # Film fixation producers information - supports multiple producers
    film_fixation_producers = FieldList(FormField(ProducerForm), min_entries=1)

    film_fixation_year = IntegerField(
        FILM_YEAR_QUESTION,
        description=FILM_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    film_fixation_published_fixed_medium = SelectField(
        FILM_PUBLISHED_FIXED_MEDIUM_QUESTION,
        description=FILM_PUBLISHED_FIXED_MEDIUM_DESCRIPTION,
        choices=FILM_FIXATION_PUBLISHED_FIXED_MEDIUM_CHOICES,
        default="film_fixation_not_published_fixed_medium"
    )

    film_fixation_published_fixed_medium_year = IntegerField(
        FILM_PUBLISHED_FIXED_MEDIUM_YEAR_QUESTION,
        description=FILM_PUBLISHED_FIXED_MEDIUM_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    film_fixation_available_no_medium = SelectField(
        FILM_AVAILABLE_NO_MEDIUM_QUESTION,
        description=FILM_AVAILABLE_NO_MEDIUM_DESCRIPTION,
        choices=FILM_FIXATION_NO_MEDIUM_CHOICES,
        default="film_fixation_not_publically_available_no_medium"
    )

    film_fixation_available_no_medium_year = IntegerField(
        FILM_AVAILABLE_NO_MEDIUM_YEAR_QUESTION,
        description=FILM_AVAILABLE_NO_MEDIUM_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    film_fixation_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['film_fixation'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['film_fixation'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )

    film_fixation_cc_license = SelectField(
        CC_LICENSE_LABEL['film_fixation'],
        #description=CC_LICENSE_DESCRIPTION['film_fixation'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    film_fixation_rights_acquired_to_make_available = SelectField(
        RIGHTS_ACQUIRED_LABEL['film_fixation'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['film_fixation'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    # Broadcasting organisation rights section
    broadcast_description = StringField(
        SECTION_BROADCAST_TITLE, description=SECTION_BROADCAST_DESCRIPTION
    )
    
    broadcast_org_identity_help = StringField(
        "Broadcast Org Identity Help", description=BROADCAST_ORG_IDENTITY_HELP
    )

    is_broadcast = SelectField(
        BROADCAST_IS_BROADCAST_QUESTION,
        description=BROADCAST_IS_BROADCAST_DESCRIPTION,
        choices=BROADCAST_CHOICES,
    )

    broadcast_before_1970 = SelectField(
        BROADCAST_BEFORE_1970_QUESTION, choices=BROADCAST_BEFORE_1970_CHOICES
    )

    is_compound_broadcast = SelectField(
        BROADCAST_IS_COMPOUND_QUESTION,
        description=BROADCAST_IS_COMPOUND_DESCRIPTION,
        choices=COMPOUND_BROADCAST_CHOICES,
    )

    broadcasters = FieldList(FormField(BroadcasterForm), min_entries=1)

    broadcast_year = IntegerField(
        BROADCAST_YEAR_QUESTION,
        description=BROADCAST_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)],
    )

    broadcast_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['broadcast'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['broadcast'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )

    broadcast_cc_license = SelectField(
        CC_LICENSE_LABEL['broadcast'],
        #description=CC_LICENSE_DESCRIPTION['broadcast'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    broadcast_rights_acquired_to_make_available = SelectField(
        RIGHTS_ACQUIRED_LABEL['broadcast'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['broadcast'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    # Additional object classification questions
    potential_first_edition_not_work = SelectField(
        POTENTIAL_FIRST_EDITION_NOT_WORK_LABEL,
        description=POTENTIAL_FIRST_EDITION_NOT_WORK_DESCRIPTION,
        choices=POTENTIAL_FIRST_EDITION_NOT_WORK_CHOICES,
        default="not_potential_first_edition_not_work",
    )

    critical_edition = SelectField(
        CRITICAL_EDITION_LABEL,
        description=CRITICAL_EDITION_DESCRIPTION,
        choices=CRITICAL_EDITION_CHOICES,
        default="not_critical_edition",
    )

    press_publication = SelectField(
        PRESS_PUBLICATION_LABEL,
        description=PRESS_PUBLICATION_DESCRIPTION,
        choices=PRESS_PUBLICATION_CHOICES,
        default="not_press_publication",
    )

    press_publication_year = IntegerField(
        PRESS_PUBLICATION_YEAR_LABEL,
        description=PRESS_PUBLICATION_YEAR_DESCRIPTION,
        validators=[Optional(), NumberRange(min=1000, max=datetime.now().year)],
    )

    trademark = SelectField(
        TRADEMARK_LABEL,
        description=TRADEMARK_DESCRIPTION,
        choices=TRADEMARK_CHOICES,
        default="not_trademark",
    )

    design = SelectField(
        DESIGN_LABEL,
        description=OBJECT_DESIGN_DESCRIPTION,
        choices=DESIGN_CHOICES,
        default="not_design",
    )

    design_unregistered = SelectField(
        DESIGN_UNREGISTERED_LABEL,
        description=OBJECT_DESIGN_UNREGISTERED_DESCRIPTION,
        choices=DESIGN_UNREGISTERED_CHOICES,
        default="not_design",
    )

    # Digital representation section
    digital_repr_nature = SelectField(
        DIGITAL_REPR_NATURE_QUESTION, choices=DIGITAL_REPR_NATURE_CHOICES
    )

    visual_art_work = SelectField(
        VISUAL_ART_WORK_QUESTION,
        description=VISUAL_ART_WORK_DESCRIPTION,
        choices=VISUAL_ART_WORK_CHOICES,
        default="no"
    )

    digital_repr_with_ai = SelectField(
        DIGITAL_REPR_AI_QUESTION,
        description=DIGITAL_REPR_AI_DESCRIPTION,
        choices=DIGITAL_REPR_AI_CHOICES,
        default="no"
    )

    # Nested forms for IP rights assessment
    digital_repr_ip_rights = FormField(IPRightsForm)

    digital_repr_copyright_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['copyright'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['copyright'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )
    
    digital_repr_copyright_cc_license = SelectField(
        CC_LICENSE_LABEL['copyright'],
        #description=CC_LICENSE_DESCRIPTION['copyright'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    digital_repr_copyright_rights_acquired = SelectField(
        RIGHTS_ACQUIRED_LABEL['digital_representation'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['copyright'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    digital_repr_phonogram_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['audio_recordings'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['audio_recordings'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )
    
    digital_repr_phonogram_cc_license = SelectField(
        CC_LICENSE_LABEL['audio_recordings'],
        #description=CC_LICENSE_DESCRIPTION['audio_recordings'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    digital_repr_phonogram_rights_acquired = SelectField(
        RIGHTS_ACQUIRED_LABEL['digital_representation'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['audio_recordings'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    digital_repr_film_fixation_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['film_fixation'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['film_fixation'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )
    
    digital_repr_film_fixation_cc_license = SelectField(
        CC_LICENSE_LABEL['film_fixation'],
        #description=CC_LICENSE_DESCRIPTION['film_fixation'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    digital_repr_film_fixation_rights_acquired = SelectField(
        RIGHTS_ACQUIRED_LABEL['digital_representation'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['film_fixation'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )

    digital_repr_other_current_rightholder = SelectField(
        CURRENT_RIGTHHOLDER_QUESTION['other'],
        description=CURRENT_RIGHTHOLDER_DESCRIPTION['other'],
        choices=CURRENT_RIGHTHOLDER_CHOICES,
        default="rightholder_unknown"
    )
    
    digital_repr_other_cc_license = SelectField(
        CC_LICENSE_LABEL['other'],
        #description=CC_LICENSE_DESCRIPTION['other'],
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default="not_applicable",
    )

    digital_repr_other_rights_acquired = SelectField(
        RIGHTS_ACQUIRED_LABEL['digital_representation'],
        #description=RIGHTS_ACQUIRED_DESCRIPTION['other'],
        choices=RIGHTS_ACQUIRED_CHOICES,
        default="not_applicable",
    )


    # Object restrictions and legal consultation section
    object_restrictions_description = StringField(
        SECTION_OBJECT_RESTRICTIONS_TITLE,
        description=SECTION_OBJECT_RESTRICTIONS_DESCRIPTION,
    )

    # Contractual restrictions
    object_contractual_restrictions = SelectField(
        OBJECT_CONTRACTUAL_RESTRICTIONS_QUESTION,
        description=OBJECT_CONTRACTUAL_RESTRICTIONS_DESCRIPTION,
        choices=CONTRACTUAL_RESTRICTIONS_CHOICES,
        default="no_contractual_restrictions",
    )

    # Administrative restrictions
    object_administrative_restrictions = SelectField(
        OBJECT_ADMINISTRATIVE_RESTRICTIONS_QUESTION,
        description=OBJECT_ADMINISTRATIVE_RESTRICTIONS_DESCRIPTION,
        choices=ADMINISTRATIVE_RESTRICTIONS_CHOICES,
        default="no_administrative_restrictions",
    )

    # Ownership status for material objects
    object_ownership_status = SelectField(
        OBJECT_OWNERSHIP_STATUS_QUESTION,
        description=OBJECT_OWNERSHIP_STATUS_DESCRIPTION,
        choices=OWNERSHIP_STATUS_CHOICES,
        default="own_object",
    )

    # Provenance tracing
    object_provenance_traced = SelectField(
        OBJECT_PROVENANCE_TRACED_QUESTION,
        description=OBJECT_PROVENANCE_TRACED_DESCRIPTION,
        choices=PROVENANCE_TRACED_CHOICES,
        default="provenance_traced",
    )

    # Provenance issues
    object_provenance_issues = SelectField(
        OBJECT_PROVENANCE_ISSUES_QUESTION,
        description=OBJECT_PROVENANCE_ISSUES_DESCRIPTION,
        choices=PROVENANCE_ISSUES_CHOICES,
        default="provenance_not_troublesome",
    )

    # Living identifiable information
    object_living_identifiable_info = SelectField(
        OBJECT_LIVING_IDENTIFIABLE_INFO_QUESTION,
        description=OBJECT_LIVING_IDENTIFIABLE_INFO_DESCRIPTION,
        choices=LIVING_IDENTIFIABLE_INFO_CHOICES,
        default="does_not_contain_identifiable_living",
    )

    # Sensitive historical information
    object_sensitive_historical_info = SelectField(
        OBJECT_SENSITIVE_HISTORICAL_INFO_QUESTION,
        description=OBJECT_SENSITIVE_HISTORICAL_INFO_DESCRIPTION,
        choices=SENSITIVE_HISTORICAL_INFO_CHOICES,
        default="does_not_contain_sensitive_historical",
    )

    # Totalitarian associations
    object_totalitarian_associations = SelectField(
        OBJECT_TOTALITARIAN_ASSOCIATIONS_QUESTION,
        description=OBJECT_TOTALITARIAN_ASSOCIATIONS_DESCRIPTION,
        choices=TOTALITARIAN_ASSOCIATIONS_CHOICES,
        default="does_not_contain_totalitarian_associations",
    )

    # Discriminatory content
    object_discriminatory_content = SelectField(
        OBJECT_DISCRIMINATORY_CONTENT_QUESTION,
        description=OBJECT_DISCRIMINATORY_CONTENT_DESCRIPTION,
        choices=DISCRIMINATORY_CONTENT_CHOICES,
        default="does_not_contain_discriminatory",
    )

    # Other sensitive content
    object_other_sensitive_content = SelectField(
        OBJECT_OTHER_SENSITIVE_CONTENT_QUESTION,
        description=OBJECT_OTHER_SENSITIVE_CONTENT_DESCRIPTION,
        choices=OTHER_SENSITIVE_CONTENT_CHOICES,
        default="does_not_contain_other_sensitive",
    )

    # Other problems
    object_other_problems = SelectField(
        OBJECT_OTHER_PROBLEMS_QUESTION,
        description=OBJECT_OTHER_PROBLEMS_DESCRIPTION,
        choices=OTHER_PROBLEMS_CHOICES,
        default="no_other_problems",
    )

    # Legal consultation
    object_legal_consultation = SelectField(
        OBJECT_LEGAL_CONSULTATION_QUESTION,
        description=OBJECT_LEGAL_CONSULTATION_DESCRIPTION,
        choices=LEGAL_CONSULTATION_CHOICES,
        default="no_self_answer",
    )

    # Optional notes for section III
    object_restrictions_notes = TextAreaField(
        OBJECT_RESTRICTIONS_NOTES_LABEL,
        description=OBJECT_RESTRICTIONS_NOTES_DESCRIPTION,
        validators=[Optional(), Length(max=OBJECT_RESTRICTIONS_NOTES_MAXLEN)],
        render_kw={"maxlength": OBJECT_RESTRICTIONS_NOTES_MAXLEN},
    )

    # General notes near submit
    general_notes = TextAreaField(
        GENERAL_NOTES_LABEL,
        description=GENERAL_NOTES_DESCRIPTION,
        validators=[Optional(), Length(max=GENERAL_NOTES_MAXLEN)],
        render_kw={"maxlength": GENERAL_NOTES_MAXLEN},
    )
