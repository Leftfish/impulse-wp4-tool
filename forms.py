"""
Forms module for the copyright assessment tool.

This module defines the form structure and validation logic for the copyright assessment tool.
It includes forms for author information, IP rights, and comprehensive copyright status evaluation.
The module uses Flask-WTF for form handling and implements nested form structures for complex
data relationships.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FieldList, FormField, BooleanField, SelectMultipleField
from wtforms.validators import Optional, NumberRange
from datetime import datetime
from data.country_codes import COUNTRY_CODES, is_eea_country, is_eu_country

# Constants for digital representation types
# Each tuple contains (value, display_text) where:
# - value: internal identifier used in processing
# - display_text: user-friendly description shown in the form
COLLECTION_CHOICES = [
    ('fictional_test_collection', 'Fictional Test Collection For Test Purposes'),
    ('film_museum_costume', 'Film Museum Potsdam: Costume Design & Scenography Collection'),
    ('film_museum_tech', 'Film Museum Potsdam: Film & Cinema Technology Collection'),
    ('film_museum_props', 'Film Museum Potsdam: Props Collection'),
    ('film_uni_holocaust', 'Film University Babelsberg: Volumetric Contemporary Testimony of Holocaust Survivors Collection'),
    ('heritage_malta_dockyard', 'Heritage Malta: Dockyard Collection'),
    ('heritage_malta_maritime', 'Heritage Malta: Maritime Collection'),
    ('ju_art_science', 'Jagiellonian University: Collections of Art and Scientific Objects'),
    ('ju_humboldt', 'Jagiellonian University: Humboldt'),
    ('ju_natural', 'Jagiellonian University: Natural Collections'),
    ('ju_virtual_museums', 'Jagiellonian University: Virtual Museums'),
    ('ju_patrimonium', 'Jagiellonian University: Patrimonium'),
    ('ju_slub_dresden', 'Jagiellonian University: SLUB Dresden'),
    ('ku_leuven_antiquo', 'KU Leuven: Collectio Academia Antiquo'),
    ('ku_leuven_corble', 'KU Leuven: Corble'),
    ('ku_leuven_glass', 'KU Leuven: Glass Slides'),
    ('ku_leuven_incunabula', 'KU Leuven: Incunabula'),
    ('ku_leuven_jesuitica', 'KU Leuven: Jesuitica'),
    ('ku_leuven_magister', 'KU Leuven: Magister Dixit'),
    ('ku_leuven_manuscripts', 'KU Leuven: Manuscripts'),
    ('ku_leuven_postcards', 'KU Leuven: Picture Postcards'),
    ('ku_leuven_theses', 'KU Leuven: Theses'),
    ('magna_zmien_archives', 'Magna Zmien: Archives'),
    ('magna_zmien_temples', 'Magna Zmien: Temples'),
    ('nkua_3d_scans', 'NKUA Museum: 3D Scans of Scientific Instruments'),
    ('nkua_interviews', 'NKUA Museum: Interviews'),
    ('nkua_mascagni', 'NKUA Museum: Mascagni Atlas'),
    ('nkua_portraits', 'NKUA Museum: Portraits'),
    ('thessaloniki_astir', 'Thessaloniki Festival: Astir Archival'),
    ('thessaloniki_books', 'Thessaloniki Festival: Books'),
    ('thessaloniki_brochures', 'Thessaloniki Festival: Brochures'),
    ('thessaloniki_catalogues', 'Thessaloniki Festival: Festival Catalogues'),
    ('thessaloniki_magazine', 'Thessaloniki Festival: Festival Magazine'),
    ('thessaloniki_megaposters', 'Thessaloniki Festival: Hellafi Megaposters'),
    ('thessaloniki_magazines', 'Thessaloniki Festival: Magazines'),
    ('thessaloniki_photos', 'Thessaloniki Festival: Photos'),
    ('thessaloniki_posters', 'Thessaloniki Festival: Posters'),
    ('thessaloniki_publications', 'Thessaloniki Festival: Publications'),
    ('other', 'Other')
]

DIGITAL_REPR_NATURE_CHOICES = [
    ('obj_2d_to_2d', '2D objects digitized in 2D'),
    ('obj_2d_to_3d', '2D objects digitized in 3D'),
    ('obj_3d_to_2d', '3D objects digitized in 2D'),
    ('obj_3d_to_3d', '3D objects digitized in 3D'),
    ('obj_complex', 'digitized complex object (e.g. scanned book, manuscript)'),
    ('obj_textual', 'digitized version of a textual work (e.g. OCR or transcripts, subtitles, captions)'),
    ('obj_translation', 'translation into a new language'),
    ('obj_audio', 'audio recording'),
    ('obj_audiovisual', 'audiovisual work'),
    ('obj_video_other', 'other video recordings (e.g. recorded interviews)'),
    ('obj_3d_reconstruction', '3D reconstruction'),
    ('other_digital_repr', 'other digital representation')
]

# List of IP rights types that need to be evaluated
# Used to generate form fields and process rights systematically
IP_RIGHTS_TYPES = [
    'copyright',
    'audio_recording_rights',
    'film_fixation_rights',
    'performance_rights',
    'other_ip_rights'
]

# Standard choices for IP rights questions
# Default is set to 'no' by being first in the list
IP_RIGHTS_CHOICES = [
    ('no', 'no'),
    ('yes', 'yes'),
    ('uncertain', 'uncertain')
]

RIGHTS_ACQUISITION_CHOICES = [
    ('not_applicable', 'Not applicable (the digital representation is not covered by this IP right)'),
    ('right_transfer', 'Yes. We have signed a right transfer (assignment) agreement.'),
    ('employer_rights', 'Yes. We acquired the rights as the employer of the person who made the digital representation.'),
    ('rights_not_acquired', 'No, we are not the rightholder'),
    ('unknown', 'We do not know.')
]

# Constants for online availability choices
COMBINED_AVAILABILITY_CHOICES = [
    ('not_applicable', 'Not applicable (not covered by this IP right)'),
    # CC license choices
    ('cc0', 'Yes. Available under Creative Commons: CC0'),
    ('cc_by', 'Yes. Available under Creative Commons: CC-BY'),
    ('cc_by_sa', 'Yes. Available under Creative Commons: CC-BY-SA'),
    ('cc_by_nc_sa', 'Yes. Available under Creative Commons: CC-BY-NC-SA'),
    ('cc_by_nd', 'Yes. Available under Creative Commons: CC-BY-ND'),
    ('cc_by_nc_nd', 'Yes. Available under Creative Commons: CC-BY-NC-ND'),
    ('other_open', 'Yes. Available under a non-CC open content license'),
    # Rights acquisition choices
    ('rights_assignment', 'Yes. Rights assigned through agreement'),
    ('license_agreement', 'Yes. Licensed through agreement'),
    ('employee_rights', 'Yes. Rights acquired through employment'),
    # Legal provisions
    ('orphan_works', 'Yes. Based on orphan works provisions'),
    ('out_of_commerce', 'Yes. Based on out-of-commerce works provisions'),
    ('quote_right', 'Yes. Based on right to quote'),
    ('other_law', 'Yes. Based on other legal provisions'),
    ('no', 'No'),
    ('unknown', 'Unknown')
]

# Keep existing CC_LICENSE_AVAILABILITY_CHOICES for backward compatibility
CC_LICENSE_AVAILABILITY_CHOICES = [
    ('not_applicable', 'No / Not applicable'),
    ('cc0', 'Yes. Available under Creative Commons: CC0'),
    ('cc_by', 'Yes. Available under Creative Commons: CC-BY'),
    ('cc_by_sa', 'Yes. Available under Creative Commons: CC-BY-SA'),
    ('cc_by_nc_sa', 'Yes. Available under Creative Commons: CC-BY-NC-SA'),
    ('cc_by_nd', 'Yes. Available under Creative Commons: CC-BY-ND'),
    ('cc_by_nc_nd', 'Yes. Available under Creative Commons: CC-BY-NC-ND'),
    ('other_open', 'Yes. It is a non-CC open content license.')
]

OBJECT_ONLINE_AVAILABILITY_CHOICES = [
    ('not_applicable', 'Not applicable (no IP rights cover the digital representation)'),
    ('license_agreement', 'Yes. We have entered into a license agreement that includes the right to publicly communicate the digital representation.'),
    ('orphan_works', 'Yes. We base on provisions of law concerning orphan works.'),
    ('out_of_commerce', 'Yes. We base on provisions of law concerning out-of-commerce works.'),
    ('quote_right', 'Yes. We base on provisions of law (right to quote).'),
    ('other_law', 'Yes. We base on other provisions of law.'),
    ('no', 'No.'),
    ('unknown', 'We do not know.')
]

# Performance rights specific choices
PERFORMANCE_CHOICES = [
    ('performance', 'Yes'),
    ('not_performance', 'No'),
    ('uncertain', 'Uncertain')
]

PERFORMANCE_BEFORE_1900_CHOICES = [
    ('performance_made_before_1900', 'Yes'),
    ('performance_not_made_before_1900', 'No'),
    ('uncertain', 'Uncertain')
]

COMPOUND_PERFORMANCE_CHOICES = [
    ('compound', 'Yes'),
    ('not_compound', 'No'),
    ('uncertain', 'Uncertain')
]

PERFORMANCE_PHONOGRAM_AVAILABLE_CHOICES = [
    ('performance_phonogram_available', 'Yes'),
    ('performance_phonogram_not_available', 'No'),
    ('uncertain', 'Uncertain')
]

PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_CHOICES = [
    ('performance_fixed_not_phonogram_available', 'Yes'),
    ('performance_fixed_not_phonogram_not_available', 'No'),
    ('uncertain', 'Uncertain')
]

PERFORMANCE_NO_MEDIUM_CHOICES = [
    ('performance_publically_available_no_medium', 'Yes'),
    ('performance_not_publically_available_no_medium', 'No'),
    ('uncertain', 'Uncertain')
]

# Phonogram rights specific choices
PHONOGRAM_CHOICES = [
    ('phonogram', 'Yes'),
    ('not_phonogram', 'No'),
    ('uncertain', 'Uncertain')
]

PHONOGRAM_BEFORE_1900_CHOICES = [
    ('phonogram_made_before_1900', 'Yes'),
    ('phonogram_not_made_before_1900', 'No'),
    ('uncertain', 'Uncertain')
]

COMPOUND_PHONOGRAM_CHOICES = [
    ('compound', 'Yes'),
    ('not_compound', 'No'),
    ('uncertain', 'Uncertain')
]

PHONOGRAM_PUBLISHED_FIXED_MEDIUM_CHOICES = [
    ('phonogram_published_fixed_medium', 'Yes'),
    ('phonogram_not_published_fixed_medium', 'No'),
    ('uncertain', 'Uncertain')
]

PHONOGRAM_NO_MEDIUM_CHOICES = [
    ('phonogram_publically_available_no_medium', 'Yes'),
    ('phonogram_not_publically_available_no_medium', 'No'),
    ('uncertain', 'Uncertain')
]

# Film fixation rights specific choices
FILM_FIXATION_CHOICES = [
    ('film_fixation', 'Yes'),
    ('not_film_fixation', 'No'),
    ('uncertain', 'Uncertain')
]

FILM_FIXATION_BEFORE_1900_CHOICES = [
    ('film_fixation_made_before_1900', 'Yes'),
    ('film_fixation_not_made_before_1900', 'No'),
    ('uncertain', 'Uncertain')
]

COMPOUND_FILM_FIXATION_CHOICES = [
    ('compound', 'Yes'),
    ('not_compound', 'No'),
    ('uncertain', 'Uncertain')
]

FILM_FIXATION_PUBLISHED_FIXED_MEDIUM_CHOICES = [
    ('film_fixation_published_fixed_medium', 'Yes'),
    ('film_fixation_not_published_fixed_medium', 'No'),
    ('uncertain', 'Uncertain')
]

FILM_FIXATION_NO_MEDIUM_CHOICES = [
    ('film_fixation_publically_available_no_medium', 'Yes'),
    ('film_fixation_not_publically_available_no_medium', 'No'),
    ('uncertain', 'Uncertain')
]

# Broadcasting organisation rights specific choices
BROADCAST_CHOICES = [
    ('broadcast', 'Yes'),
    ('not_broadcast', 'No'),
    ('uncertain', 'Uncertain')
]

BROADCAST_BEFORE_1970_CHOICES = [
    ('broadcast_made_before_1970', 'Yes'),
    ('broadcast_not_made_before_1970', 'No'),
    ('uncertain', 'Uncertain')
]

COMPOUND_BROADCAST_CHOICES = [
    ('compound', 'Yes'),
    ('not_compound', 'No'),
    ('uncertain', 'Uncertain')
]

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
    
    is_anonymous = BooleanField('The producer is unknown')
    country_of_origin = SelectField('Country of Origin', choices=COUNTRY_CODES)

    def get_country_status(self):
        """
        Determine the EU/EEA status of the producer's country.
        
        Returns:
            dict: Contains boolean flags for EU and EEA membership status
        """
        return {
            'is_eu': is_eu_country(self.country_of_origin.data),
            'is_eea': is_eea_country(self.country_of_origin.data)
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
    
    is_anonymous = BooleanField('Performer is anonymous or pseudonymous')
    country_of_origin = SelectField('Country of Origin', choices=COUNTRY_CODES)

    def get_country_status(self):
        """
        Determine the EU/EEA status of the performer's country.
        
        Returns:
            dict: Contains boolean flags for EU and EEA membership status
        """
        return {
            'is_eu': is_eu_country(self.country_of_origin.data),
            'is_eea': is_eea_country(self.country_of_origin.data)
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
    
    is_anonymous = BooleanField('Author is anonymous or pseudonymous')
    country_of_origin = SelectField('Country of Origin', choices=COUNTRY_CODES)

    def get_country_status(self):
        """
        Determine the EU/EEA status of the author's country.
        
        Returns:
            dict: Contains boolean flags for EU and EEA membership status
        """
        return {
            'is_eu': is_eu_country(self.country_of_origin.data),
            'is_eea': is_eea_country(self.country_of_origin.data)
        }

class BroadcasterForm(FlaskForm):
    """
    Subform for broadcasting organisation-specific information.
    Mirrors ProducerForm: captures identity status and country of origin.
    """
    class Meta:
        csrf = False
    
    is_anonymous = BooleanField('The broadcasting organisation is unknown')
    country_of_origin = SelectField('Country of Origin', choices=COUNTRY_CODES)

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
        'Copyright',
        description="Consider if the digital representation is protected by copyright (it was made by a human and is original, i.e. it is its author's own intellectual creation). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.",
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    audio_recording_rights = SelectField(
        'Rights to audio recordings (phonograms)',
        description='Consider if the digital representation is protected by rights to audio recordings or phonograms ( fixation of the sounds of a performance or of other sounds, or of a representation of sounds, other than in the form of a fixation incorporated in a cinematographic or other audiovisual work). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    film_fixation_rights = SelectField(
        'Film fixation rights',
        description='Consider if the digital representation is protected by rights to film fixations or videograms (recording of moving images, with or without sound, regardless of whether it constitutes a cinematographic or audiovisual work). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    performance_rights = SelectField(
        'Performance rights',
        description='Consider if the digital representation is protected by performance rights (the rights that protect  actors, singers, musicians, dancers, and other persons who act, sing, deliver, declaim, play in, interpret, or otherwise perform literary or artistic works or expressions of folklore). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    other_ip_rights = SelectField(
        'Other IP rights',
        description='Consider if the digital representation is protected by any other IP rights. For example, some countries provide protection for non-original photographs (i.e photographs not covered by copyright). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )

class IPRightsAcquiredForm(FlaskForm):
    """
    Form for documenting rights acquisition status.
    
    Captures information about how rights were acquired for different IP types,
    including Creative Commons licenses and other legal mechanisms.
    """
    class Meta:
        csrf = False
    
    # Each field corresponds to a type of IP right and captures how it was acquired
    # Default is 'not_applicable' as defined in RIGHTS_ACQUISITION_CHOICES
    copyright = SelectField('Copyright', choices=RIGHTS_ACQUISITION_CHOICES)
    audio_recording_rights = SelectField('Audio recordings', choices=RIGHTS_ACQUISITION_CHOICES)
    film_fixation_rights = SelectField('Film fixations', choices=RIGHTS_ACQUISITION_CHOICES)
    performance_rights = SelectField('Performance rights', choices=RIGHTS_ACQUISITION_CHOICES)
    other_ip_rights = SelectField('Other IP rights', choices=RIGHTS_ACQUISITION_CHOICES)

class DigitalReprRightsAvailabilityForm(FlaskForm):
    """
    Form for capturing rights availability information for each type of IP right.
    This combines CC license and other rights acquisition options.
    """
    class Meta:
        csrf = False
    
    copyright = SelectField(
        'Copyright',
        description='Availability under open content license or other rights acquisition for copyright.',
        choices=COMBINED_AVAILABILITY_CHOICES,
        default='not_applicable'
    )
    audio_recording_rights = SelectField(
        'Audio recordings',
        description='Availability under open content license or other rights acquisition for audio recording rights.',
        choices=COMBINED_AVAILABILITY_CHOICES,
        default='not_applicable'
    )
    film_fixation_rights = SelectField(
        'Film fixations',
        description='Availability under open content license or other rights acquisition for film fixation rights.',
        choices=COMBINED_AVAILABILITY_CHOICES,
        default='not_applicable'
    )
    performance_rights = SelectField(
        'Performance rights',
        description='Availability under open content license or other rights acquisition for performance rights.',
        choices=COMBINED_AVAILABILITY_CHOICES,
        default='not_applicable'
    )
    other_ip_rights = SelectField(
        'Other IP rights',
        description='Availability under open content license or other rights acquisition for other IP rights.',
        choices=COMBINED_AVAILABILITY_CHOICES,
        default='not_applicable'
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
        'Original Object Description',
        description="The object as such can be a work according to copyright law. The questions below aim to determine whether, if it is indeed a work, it has passed into the public domain. Note that the object must be distinguished from its digital representation - here, we only deal with the former. For example: a painting is the object that is very likely to be an artistic work, while the digital image of the painting is its digital representation; a short story is the object that is very likely to be a literary work, while a digital recording of a person reading the story would be a digital representation."
    )
    
    author_info_description = StringField(
        'Author Information Description',
        description="Depending on the situation, information about the author may be necessary to determine if the work passed into the public domain."
    )
    
    creation_publication_description = StringField(
        'Creation and Publication Description',
        description="Depending on the situation, information about whether the work was published or otherwise made available to the public, as well as when it was created, may be necessary to determine if the work has passed into the public domain."
    )
    
    publication_dates_description = StringField(
        'Publication Dates Description',
        description="Note the difference between publication (that implies a material copy) and other forms of making the work publically available."
    )
    
    rights_info_description = StringField(
        'Rights Information Description',
        description="The information gathered here can not only help establish the status of the object when it is a work under copyright law, but also determine whether it can be used even when it is not in the public domain."
    )
    
    digital_repr_description = StringField(
        'Digital Representation Description',
        description="We assume, to simplify the evaluation, that none of the digital representations that are practically usable as of 2025 and have ever been covered by any IP rights have passed into the public domain due to the lapse of such rights."
    )
    
    ip_rights_coverage_description = StringField(
        'IP Rights Coverage Description',
        description="Depending on the situation, a digital representation may be protected by various rights at the same time."
    )

    # Basic Information section
    object_name = StringField(
        'Name of the object',
        description='Enter the name or title of the object being evaluated.'
    )
    
    institution_name = SelectField(
        'Name of the collection',
        description='Select the collection this object belongs to.',
        choices=COLLECTION_CHOICES
    )

    object_url = StringField(
        'URL',
        description='Enter the URL of the object being evaluated.'
    )

    # General section - Copyright work status
    is_copyright_work = SelectField(
        'Do you consider the object to be a work within the meaning of copyright law (it was made by a human and is original, i.e. it is its author\'s own intellectual creation)? If you select "No" here, skip to part II. of the form.',
        description='For example, works include: books, pamphlets and other writings; lectures, addresses, sermons and other works of the same nature; dramatic or dramatico-musical works; choreographic works and entertainments in dumb show; musical compositions with or without words; cinematographic works to which are assimilated works expressed by a process analogous to cinematography; works of drawing, painting, architecture, sculpture, engraving and lithography; photographic works to which are assimilated works expressed by a process analogous to photography; works of applied art; illustrations, maps, plans, sketches and three-dimensional works relative to geography, topography, architecture or science (Article 2.1 of the Berne Convention)',
        choices=[
            ('work', 'Yes'),
            ('not_work', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='not_work'
    )

    # Work characteristics
    created_before_1850 = SelectField(
        'Was the work created in 1850 or earlier?',
        description='If the object in question is a transformed version of another work, such as a translation or critical edition, you should take into account the date of the creation of the transformed version.',
        choices=[
            ('not_made_before_1850', 'No'),
            ('made_before_1850', 'Yes'),
            ('uncertain', 'Uncertain')
        ]
    )

    is_derivative = SelectField(
        'Is the work in question a derivative work (e.g., adaptation or translation of another work)?',
        choices=[
            ('not_derivative', 'No'),
            ('derivative', 'Yes'),
            ('uncertain', 'Uncertain')
        ]
    )

    is_compound = SelectField(
        'Does the work contain other works (e.g., illustrations, quoted poems, sheet music)?',
        choices=[
            ('not_derivative', 'No'),
            ('derivative', 'Yes'),
            ('uncertain', 'Uncertain')
        ]
    )

    is_photography = SelectField(
        'Is the object a photography or a picture made with a similar technique?',
        choices=[
            ('not_photography', 'No'),
            ('photography_with_notice', 'Yes, and there is a copyright notice on it'),
            ('photography_without_notice', 'Yes, but without a copyright notice on it')
            
        ]
    )

    # Authors information - supports multiple authors
    authors = FieldList(FormField(AuthorForm), min_entries=1)

    # Creation and publication details
    creation_year = IntegerField(
        'When was the work created? Enter the year.',
        description='Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    physically_published = SelectField(
        'Was the work published, i.e. made publicly available on a physical medium (with the rightholder\'s consent), e.g., book publication?',
        description='Publication means manufacture of the copies, provided that the availability of such copies has been such as to satisfy the reasonable requirements of the public. The performance of a dramatic, dramatico-musical, cinematographic or musical work, the public recitation of a literary work, the communication by wire or the broadcasting of literary or artistic works, the exhibition of a work of art and the construction of a work of architecture are not taken into account here.',
        choices=[
            ('published_on_physical_medium', 'Yes'),
            ('not_published_on_physical_medium', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    # Publication location information
    country_first_publication = SelectField(
        'In which country was the work published for the first time?',
        description='If the country is unknown, select "Unknown".',
        choices=COUNTRY_CODES
    )

    # Handle simultaneous publications in multiple countries
    simultaneous_publication_countries = FieldList(
        SelectField(
            'In which country was the work published again, but within thirty days of its first publication?',
            choices=COUNTRY_CODES
        ),
        min_entries=1
    )

    territory_status_changed = BooleanField(
        'When answering the previous questions, did you encounter the problem of changing status of territories (e.g. dissolution of a country, a country obtaining independence from a colonial power etc.)?'
    )

    # Special cases handling
    cinematographic_country = SelectField(
        'If the object in question is a cinematographic work, select the country of the headquarters or habitual residence of the author.',
        description='E.g. amateur cinematographic recordings.',
        choices=COUNTRY_CODES
    )

    architecture_country = SelectField(
        'If the object in question is a work of architecture that was built, or a work incorporated in a building or another structure, select the country of its location.',
        choices=COUNTRY_CODES
    )

    # Publication and availability details
    otherwise_available = SelectField(
        'Was the object otherwise made available to the public with the rightholder\'s consent, e.g., broadcast on radio, TV or via Internet?',
        choices=[
            ('made_available_no_medium', 'Yes'),
            ('not_made_available_no_medium', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    internet_first_available = SelectField(
        'Was the object made available for the first time on a website or in another Internet medium that allows download?',
        choices=[
            ('made_available_internet', 'Yes'),
            ('not_made_available_internet', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    # Publication dates
    first_publication_year = IntegerField(
        'If the work was published, i.e. made publicly available on a physical medium (with the rightholder\'s consent), enter the year of the first publication.',
        description='Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    first_available_year = IntegerField(
        'If the object was otherwise made available to the public with the rightholder\'s consent, e.g., broadcast on radio, TV or via Internet, enter the year.',
        description='Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    # Rights ownership information
    original_rightholder = SelectField(
        'Who originally held the copyright?',
        description='Normally, copyright belongs initially to the author who created the work. Exceptionally copyright law may designate a legal person (e.g., a publisher or an employer) as the initial rightholder. This should not be confused with situations in which the author is the original rightholder and transfers/assigns copyright to another person.',
        choices=[
            ('human_author', 'Author(s)'),
            ('legal_person', 'Another entity (e.g. publisher, film producer)'),
            ('uncertain', 'Uncertain')
        ]
    )

    # Author status
    author_alive = SelectField(
        'Is the identified author (or at least one of the identified co-authors) alive?',
        choices=[
            ('author_alive', 'Yes'),
            ('author_dead', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    author_death_year = IntegerField(
        'If the author (or all the co-authors) passed away, enter the year of death of the author or the last living co-author.',
        description='Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    current_rightholder = SelectField(
        'Do you know who currently holds the copyright?',
        description='This question pertains to copyright ownership. Do not select "Yes" if you are only a licensee or you know only who is holding a license to use the work.',
        choices=[
            ('rightholder_not_us', 'Yes, not our institution'),
            ('rightholder_us', 'Yes, our institution acquired the rights (e.g., due to the work being created by an employee, or entered into a copyright assignment agreement.)'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    object_cc_license = SelectField(
        'If you are not the rightholder, is the object available under a Creative Commons license or another open content license?',
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    object_copyright_rights_acquired_to_make_available = SelectField(
        'If you are not the rightholder, did you otherwise acquire rights that enable you to make the original object available online (e.g. through rights transfer, license agreement, or legal provisions)?',
        choices=OBJECT_ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Performance rights section
    performance_description = StringField(
        'Performance Rights Description',
        description="The questions below aim to determine whether the performance has passed into the public domain. Note that this section is independent from the copyright section above and the digital representation section below."
    )

    is_performance = SelectField(
        'Does the object include a performance (e.g. people dancing, singing, acting, miming, reciting a text)?',
        description='Performers are "actors, singers, musicians, dancers, and other persons who act, sing, deliver, declaim, play in, interpret, or otherwise perform literary or artistic works or expressions of folklore" (WIPO Performances and Phonograms Treaty)',
        choices=PERFORMANCE_CHOICES
    )

    performance_before_1900 = SelectField(
        'Was the performance made in 1900 or earlier?',
        choices=PERFORMANCE_BEFORE_1900_CHOICES
    )

    is_compound_performance = SelectField(
        'Are multiple performances contained in the same object (e.g., a movie which includes acting and singing)?',
        choices=COMPOUND_PERFORMANCE_CHOICES
    )

    # Performers information - supports multiple performers
    performers = FieldList(FormField(PerformerForm), min_entries=1)

    performance_year = IntegerField(
        'When was the performance made?',
        description='If you are uncertain, but know the latest possible date (e.g. the date of the performer\'s death), use this date. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    performance_phonogram_available = SelectField(
        'Was the performance lawfully published on a fixed medium that was a phonogram OR made publically available from a fixed medium that was a phonogram?',
        description='E.g., a vinyl sold in music shops, or music streamed online from a master recording.',
        choices=PERFORMANCE_PHONOGRAM_AVAILABLE_CHOICES
    )

    performance_phonogram_available_year = IntegerField(
        'When was the performance lawfully published on a fixed medium that was a phonogram OR made publically available from a fixed medium that was a phonogram?',
        description='E.g., a vinyl sold in music shops, or music streamed online from a master recording. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    performance_available_no_medium = SelectField(
        'Was the performance lawfully made available without a fixed medium?',
        description='E.g., a radio show was broadcasted, but not registered on a fixed medium.',
        choices=PERFORMANCE_NO_MEDIUM_CHOICES
    )

    performance_available_no_medium_year = IntegerField(
        'When was the performance lawfully made available without a fixed medium?',
        description='E.g., a radio show was broadcasted, but not registered on a fixed medium. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    performance_fixed_not_phonogram_available = SelectField(
        'Was the performance lawfully published on a fixed medium, but not on a phonogram OR made publically available from a fixed medium, but not on a phonogram?',
        description='E.g. a VHS with a recording of a concert, or a video made available online from a master recording.',
        choices=PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_CHOICES
    )

    performance_fixed_not_phonogram_available_year = IntegerField(
        'When was the performance lawfully published on a fixed medium, but not on a phonogram OR made publically available from a fixed medium, but not on a phonogram?',
        description='E.g. a VHS with a recording of a concert, or a video made available online from a master recording. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    performance_current_rightholder = SelectField(
        'Do you know who is currently the rightholder?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright).',
        choices=[
            ('rightholder_not_us', 'Yes, not our institution'),
            ('rightholder_us', 'Yes, our institution acquired the rights (e.g., due to the work being created by an employee, or entered into a copyright assignment agreement.)'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    performance_cc_license = SelectField(
        'If you are not the rightholder, is the object available under a Creative Commons license or another open content license?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright).',
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    performance_rights_acquired_to_make_available = SelectField(
        'If you are not the rightholder, did you otherwise acquire rights that enable you to make the original object available online (e.g. through rights transfer, license agreement, or legal provisions)?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright).',
        choices=OBJECT_ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Phonogram rights section
    phonogram_description = StringField(
        'Phonogram Rights Description',
        description="The questions below aim to determine whether the recording has passed into the public domain. Note that this section is independent from the copyright section above, the performance section above, and the digital representation section below."
    )

    is_phonogram = SelectField(
        'Does the object include a phonogram / an audio recording which is NOT incorporated in a cinematographic or other audiovisual work?',
        description='A phonogram is a "fixation of the sounds of a performance or of other sounds, or of a representation of sounds, other than in the form of a fixation incorporated in a cinematographic or other audiovisual work;" (WIPO Performances and Phonograms Treaty)',
        choices=PHONOGRAM_CHOICES
    )

    phonogram_before_1900 = SelectField(
        'Was the recording made in 1900 or earlier?',
        choices=PHONOGRAM_BEFORE_1900_CHOICES
    )

    is_compound_phonogram = SelectField(
        'Are multiple recordings contained in the same object?',
        description='For example, it is a collection of multiple recordings or a recording that is complex, i.e. it is made from various recordings.',
        choices=COMPOUND_PHONOGRAM_CHOICES
    )

    # Producers information - supports multiple producers
    producers = FieldList(FormField(ProducerForm), min_entries=1)

    phonogram_year = IntegerField(
        'When was the recording made?',
        description='If you are uncertain, but know the latest possible date, use this date. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    phonogram_published_fixed_medium = SelectField(
        'Was the recording lawfully published on a fixed medium?',
        description='E.g., a vinyl sold in music shops.',
        choices=PHONOGRAM_PUBLISHED_FIXED_MEDIUM_CHOICES
    )

    phonogram_published_fixed_medium_year = IntegerField(
        'When was the recording lawfully published on a fixed medium?',
        description='E.g., a vinyl sold in music shops. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    phonogram_available_no_medium = SelectField(
        'Was the recording lawfully made publically available without a fixed medium?',
        description='E.g., a radio show was broadcasted, but not registered on a fixed medium.',
        choices=PHONOGRAM_NO_MEDIUM_CHOICES
    )

    phonogram_available_no_medium_year = IntegerField(
        'When was the recording lawfully made publically available without a fixed medium?',
        description='E.g., a radio show was broadcasted, but not registered on a fixed medium. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    phonogram_current_rightholder = SelectField(
        'Do you know who is currently the rightholder?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright or performances).',
        choices=[
            ('rightholder_not_us', 'Yes, not our institution'),
            ('rightholder_us', 'Yes, our institution acquired the rights (e.g., due to the work being created by an employee, or entered into a copyright assignment agreement.)'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    phonogram_cc_license = SelectField(
        'If you are not the rightholder, is the object available under a Creative Commons license or another open content license?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright or performances).',
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    phonogram_rights_acquired_to_make_available = SelectField(
        'If you are not the rightholder, did you otherwise acquire rights that enable you to make the original object available online (e.g. through rights transfer, license agreement, or legal provisions)?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright or performances).',
        choices=OBJECT_ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Film fixation rights section
    film_fixation_description = StringField(
        'Film Fixation Rights Description',
        description="The questions below aim to determine whether the film fixation has passed into the public domain. Note that this section is independent from the copyright section above, the performance section above, the phonogram section above, and the digital representation section below."
    )

    is_film_fixation = SelectField(
        'Does the object include a film fixation / a cinematographic or other audiovisual work which is NOT incorporated in a cinematographic or other audiovisual work?',
        description='A film fixation is a "fixation of the sounds of a performance or of other sounds, or of a representation of sounds, in the form of a fixation incorporated in a cinematographic or other audiovisual work;" (WIPO Performances and Phonograms Treaty)',
        choices=FILM_FIXATION_CHOICES
    )

    film_fixation_before_1900 = SelectField(
        'Was the film fixation made in 1900 or earlier?',
        choices=FILM_FIXATION_BEFORE_1900_CHOICES
    )

    is_compound_film_fixation = SelectField(
        'Are multiple film fixations contained in the same object?',
        description='For example, it is a collection of multiple film fixations or a film fixation that is complex, i.e. it is made from various film fixations.',
        choices=COMPOUND_FILM_FIXATION_CHOICES
    )

    # Film fixation producers information - supports multiple producers
    film_fixation_producers = FieldList(FormField(ProducerForm), min_entries=1)

    film_fixation_year = IntegerField(
        'When was the film fixation made?',
        description='If you are uncertain, but know the latest possible date, use this date. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    film_fixation_published_fixed_medium = SelectField(
        'Was the film fixation lawfully published on a fixed medium?',
        description='E.g., a DVD sold in shops.',
        choices=FILM_FIXATION_PUBLISHED_FIXED_MEDIUM_CHOICES
    )

    film_fixation_published_fixed_medium_year = IntegerField(
        'When was the film fixation lawfully published on a fixed medium?',
        description='E.g., a DVD sold in shops. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    film_fixation_available_no_medium = SelectField(
        'Was the film fixation lawfully made publically available without a fixed medium?',
        description='E.g., a film was broadcasted on TV, but not registered on a fixed medium.',
        choices=FILM_FIXATION_NO_MEDIUM_CHOICES
    )

    film_fixation_available_no_medium_year = IntegerField(
        'When was the film fixation lawfully made publically available without a fixed medium?',
        description='E.g., a film was broadcasted on TV, but not registered on a fixed medium. Leave blank if the year is unknown.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    film_fixation_current_rightholder = SelectField(
        'Do you know who is currently the rightholder?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright, performances, or phonograms).',
        choices=[
            ('rightholder_not_us', 'Yes, not our institution'),
            ('rightholder_us', 'Yes, our institution acquired the rights (e.g., due to the work being created by an employee, or entered into a copyright assignment agreement.)'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    film_fixation_cc_license = SelectField(
        'If you are not the rightholder, is the object available under a Creative Commons license or another open content license?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright, performances, or phonograms).',
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    film_fixation_rights_acquired_to_make_available = SelectField(
        'If you are not the rightholder, did you otherwise acquire rights that enable you to make the original object available online (e.g. through rights transfer, license agreement, or legal provisions)?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright, performances, or phonograms).',
        choices=OBJECT_ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Broadcasting organisation rights section
    broadcast_description = StringField(
        'Broadcasting Organisation Rights Description',
        description='The questions below aim to determine whether the broadcast has passed into the public domain. Note that this section is independent from the copyright section above, the performance section above, the phonogram section above, the film fixation section above, and the digital representation section below.'
    )

    is_broadcast = SelectField(
        'Does the object include a broadcast?',
        description='“broadcasting” means the transmission by wireless means for public reception of sounds or of images and sounds (International Convention for the Protection of Performers, Producers of Phonograms and Broadcasting Organizations). The notion includes TV broadcasts, radio broadcasts, as well as internet broadcasts other than video-on-demand similar services.',
        choices=BROADCAST_CHOICES
    )

    broadcast_before_1970 = SelectField(
        'Was the broadcast made in 1970 or earlier?',
        choices=BROADCAST_BEFORE_1970_CHOICES
    )

    is_compound_broadcast = SelectField(
        'Are multiple broadcasts contained in the same object?',
        description='For example, it is a collection of multiple broadcasts.',
        choices=COMPOUND_BROADCAST_CHOICES
    )

    broadcasters = FieldList(FormField(BroadcasterForm), min_entries=1)

    broadcast_year = IntegerField(
        'When was the broadcast made?',
        description='If you are uncertain, but know the latest possible date, use this date.',
        validators=[Optional(), NumberRange(min=-9999, max=datetime.now().year)]
    )

    broadcast_current_rightholder = SelectField(
        'Do you know who is currently the rightholder?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright or performances).',
        choices=[
            ('rightholder_not_us', 'Yes, not our institution'),
            ('rightholder_us', 'Yes, our institution acquired the rights (e.g., due to the work being created by an employee, or entered into a copyright assignment agreement.)'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    broadcast_cc_license = SelectField(
        'If you are not the rightholder, is the object available under a Creative Commons license or another open content license?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright or performances).',
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    broadcast_rights_acquired_to_make_available = SelectField(
        'If you are not the rightholder, did you otherwise acquire rights that enable you to make the original object available online (e.g. through rights transfer, license agreement, or legal provisions)?',
        description='Note that this question is independent from similar questions pertaining to other rights (e.g. copyright or performances).',
        choices=OBJECT_ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Additional object classification questions
    potential_first_edition_not_work = SelectField(
        'If the object is not a work, has it already been published or otherwise made available to the public?',
        description='The object may not be a work because, for example, it is specifically excluded from copyright protection. Some countries exclude protection of official documents and similar content.',
        choices=[
            ('not_potential_first_edition_not_work', 'No'),
            ('potential_first_edition_not_work', 'Yes'),
            ('uncertain', 'Uncertain')
        ],
        default='not_potential_first_edition_not_work'
    )

    critical_edition = SelectField(
        'Is the object a so-called critical edition (scholarly edition, scientific edition) of a work of a text?',
        description='An edition can qualify as critical when a work has been restored thanks to the analysis and embedding of data and other components that have been preliminarily selected.',
        choices=[
            ('not_critical_edition', 'No'),
            ('critical_edition', 'Yes'),
            ('uncertain', 'Uncertain')
        ],
        default='not_critical_edition'
    )

    press_publication = SelectField(
        'Is the object a press publication?',
        description='A "press publication" is a a collection composed mainly of literary works of a journalistic nature, but which can also include other works or other subject matter, and which satisfies three conditions: (a) it is an individual item within a periodical or regularly updated publication under a single title, such as a newspaper or a general or special interest magazine; (b) it has the purpose of providing the general public with information related to news or other topics; and (c) it is published in any media under the initiative, editorial responsibility and control of a service provider. Periodicals that are published for scientific or academic purposes, such as scientific journals, are not press publications.',
        choices=[
            ('not_press_publication', 'No'),
            ('press_publication', 'Yes'),
            ('uncertain', 'Uncertain')
        ],
        default='not_press_publication'
    )

    press_publication_year = IntegerField(
        'If the object is a press publication, when was it published?',
        description='Enter a four-digit year value.',
        validators=[Optional(), NumberRange(min=1000, max=datetime.now().year)]
    )

    trademark = SelectField(
        'Was the object registerd as a trademark OR does it depict a trademark?',
        description='A trademark is a sign such as a word, logo, slogan, shape or sound that identifies goods or services as coming from a particular business and distinguishes them from those of others. Trademarks may be registered in a single countries or for the whole European Union through the European Union Intellectual Property Office (EUIPO).',
        choices=[
            ('not_trademark', 'No'),
            ('trademark', 'Yes'),
            ('uncertain', 'Uncertain')
        ],
        default='not_trademark'
    )

    design = SelectField(
        'Was the object registered as a design during the last 25 years OR does it depict a design registered during the last 25 years?',
        description='A design protects the appearance of a product, including its shape, patterns, lines, contours or colours. Designs may be registered in single EU countries or for the whole European Union through the European Union Intellectual Property Office (EUIPO).',
        choices=[
            ('not_design', 'No'),
            ('design', 'Yes'),
            ('uncertain', 'Uncertain')
        ],
        default='not_design'
    )

    # Digital representation section
    digital_repr_nature = SelectField(
        'What is the nature of the digital representation?',
        choices=DIGITAL_REPR_NATURE_CHOICES
    )
    
    # Nested forms for IP rights assessment
    digital_repr_ip_rights = FormField(IPRightsForm)
    digital_repr_ip_rights_acquired = FormField(IPRightsAcquiredForm)
    
    digital_repr_cc_license = SelectField(
        'If you are not the rightholder of the rights in the digital representation, is it available under a Creative Commons license or another open content license?',
        choices=CC_LICENSE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )
    
    digital_repr_rights_acquired_to_make_available = SelectField(
        'Did you otherwise acquire rights that enable you to make the digital representation itself available online (e.g. through rights transfer, license agreement, or legal provisions)?',
        choices=COMBINED_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Add new combined form
    digital_repr_rights_availability = FormField(
        DigitalReprRightsAvailabilityForm,
        description='Is the digital representation available under a Creative Commons license or another open content license, or did you otherwise acquire rights that enable you to make the digital representation available online, in connection with all the relevant rights?'
    )

    # Object restrictions and legal consultation section
    object_restrictions_description = StringField(
        'Object Restrictions and Legal Consultation Description',
        description="This section covers contractual and administrative restrictions that may limit the scope of use of the object, as well as legal consultation status."
    )

    # Contractual restrictions
    object_contractual_restrictions = SelectField(
        'Are there any contractual restrictions that limit the scope of use of the object (e.g. an agreement with the owner)?',
        choices=[
            ('contractual_restrictions', 'Yes'),
            ('no_contractual_restrictions', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='no_contractual_restrictions'
    )

    # Administrative restrictions
    object_administrative_restrictions = SelectField(
        'Are there any administrative restrictions that limit the scope of use of the object?',
        description='For example, export controls, museum policies, institutional rules, or government regulations that restrict the way you can use the object.',
        choices=[
            ('administrative_restrictions', 'Yes'),
            ('no_administrative_restrictions', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='no_administrative_restrictions'
    )

    # Ownership status for material objects
    object_ownership_status = SelectField(
        'If it is a material object (e.g. sculptures, scientific equipment, paintings), what is the ownership status?',
        description='Please select the option that best describes your legal situation with respect to ownership and usage.',
        choices=[
            ('own_object', 'We own the object.'),
            ('contractual_arrangements', 'We do not own the object, but we have contractual arrangements with the owner that allow us to use it.'),
            ('legal_provisions', 'We do not own the object, but we can rely on provisions of law to use it.'),
            ('no_basis', 'We do not own the object and we have no clear basis for its use.'),
            ('unknown_owner', 'We do not know who the owner is.'),
            ('other', 'Other.')
        ],
        default='own_object'
    )

    # Provenance tracing
    object_provenance_traced = SelectField(
        'If it is a material object, is the provenance well-traced?',
        description='For example, do we have reliable records of the chain of ownership and transfer?',
        choices=[
            ('provenance_traced', 'Yes'),
            ('provenance_not_traced', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='provenance_traced'
    )

    # Provenance issues
    object_provenance_issues = SelectField(
        'If it is a material object, is its provenance associated with troublesome issues (war, colonial, and similar)?',
        description='For example, confiscations, looting, or colonial acquisitions.',
        choices=[
            ('provenance_troublesome', 'Yes'),
            ('provenance_not_troublesome', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='provenance_not_troublesome'
    )

    # Living identifiable information
    object_living_identifiable_info = SelectField(
        'Does the object contain information (names, image, voice) about living people that can be identified?',
        description='For example, photographs, audio recordings, or manuscripts mentioning living persons.',
        choices=[
            ('contains_identifiable_living', 'Yes'),
            ('does_not_contain_identifiable_living', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='does_not_contain_identifiable_living'
    )

    # Sensitive historical information
    object_sensitive_historical_info = SelectField(
        'Does the object contain sensitive, potentially defamatory information about someone (e.g., WW2 collaboration), including people who are no longer alive?',
        description='For example, documents suggesting misconduct or criminal activity.',
        choices=[
            ('contains_sensitive_historical', 'Yes'),
            ('does_not_contain_sensitive_historical', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='does_not_contain_sensitive_historical'
    )

    # Totalitarian associations
    object_totalitarian_associations = SelectField(
        'Does the object contain something (e.g., content, symbolics) that could be associated with racist, nationalist, or totalitarian ideologies?',
        description='For example, symbols, slogans, propaganda.',
        choices=[
            ('contains_totalitarian_associations', 'Yes'),
            ('does_not_contain_totalitarian_associations', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='does_not_contain_totalitarian_associations'
    )

    # Discriminatory content
    object_discriminatory_content = SelectField(
        'Does the object contain content discriminatory or derogatory towards a person, group, or ethnicity?',
        description='For example, racist caricatures, slurs, or mocking representations.',
        choices=[
            ('contains_discriminatory', 'Yes'),
            ('does_not_contain_discriminatory', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='does_not_contain_discriminatory'
    )

    # Other sensitive content
    object_other_sensitive_content = SelectField(
        'Does the object contain content that, in your opinion, is otherwise sensitive?',
        description='For example, violent, disturbing, or culturally offensive material.',
        choices=[
            ('contains_other_sensitive', 'Yes'),
            ('does_not_contain_other_sensitive', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='does_not_contain_other_sensitive'
    )

    # Other problems
    object_other_problems = SelectField(
        'Are there any reasons not covered above, that in your opinion would be problematic?',
        description='For example, ethical, cultural, or political concerns not addressed in previous questions.',
        choices=[
            ('other_problems', 'Yes'),
            ('no_other_problems', 'No'),
            ('uncertain', 'Uncertain')
        ],
        default='no_other_problems'
    )

    # Legal consultation
    object_legal_consultation = SelectField(
        'Have we consulted a copyright lawyer about the legal status of the object?',
        description='Please specify the type of consultation or reason for not consulting.',
        choices=[
            ('in_house_lawyer', 'Yes, with an in-house lawyer.'),
            ('external_lawyer', 'Yes, with an external lawyer.'),
            ('no_self_answer', 'No. We can answer these questions ourselves.'),
            ('no_funds', 'No. We do not have the funds to hire a lawyer.'),
            ('no_other_reason', 'No, other reason.')
        ],
        default='no_self_answer'
    )

    def get_publication_status(self):
        """
        Analyze the EU/EEA status of all publication countries.
        
        Evaluates both first publication and simultaneous publications to determine
        if any occurred in EU/EEA countries.
        
        Returns:
            dict: Contains EU/EEA status for first publication, list of simultaneous
                 publications, and whether any publication was in EEA
        """
        first_pub = self.country_first_publication.data
        simul_pubs = [country.data for country in self.simultaneous_publication_countries]
        
        return {
            'first_publication': {
                'is_eu': is_eu_country(first_pub),
                'is_eea': is_eea_country(first_pub)
            },
            'simultaneous_publications': [
                {
                    'country': country,
                    'is_eu': is_eu_country(country),
                    'is_eea': is_eea_country(country)
                }
                for country in simul_pubs
            ],
            'any_eea': is_eea_country(first_pub) or any(is_eea_country(c) for c in simul_pubs)
        }

    def get_authors_status(self):
        """
        Get the EU/EEA status for all authors' countries.
        
        Returns:
            list: List of dictionaries containing EU/EEA status for each author's country
        """
        return [author_form.get_country_status() for author_form in self.authors] 