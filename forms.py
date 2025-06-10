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
    ('obj_3d_reconstruction', '3D reconstruction')
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

CC_LICENSE_CHOICES = [
    ('not_applicable', 'Not applicable (the digital representation is not covered by this IP right)'),
    ('right_transfer', 'Yes. We have signed a right transfer (assignment) agreement.'),
    ('employer_rights', 'Yes. We acquired the rights as the employer of the person who made the digital representation.'),
    ('cc0', 'No, but the digital representation is available under Creative Commons: CC0'),
    ('cc_by', 'No, but the digital representation is available under Creative Commons: CC-BY'),
    ('cc_by_sa', 'No, but the digital representation is available under Creative Commons: CC-BY-SA'),
    ('cc_by_nc_sa', 'No, but the digital representation is available under Creative Commons: CC-BY-NC-SA'),
    ('cc_by_nd', 'No, but the digital representation is available under Creative Commons: CC-BY-ND'),
    ('cc_by_nc_nd', 'No, but the digital representation is available under Creative Commons: CC-BY-NC-ND'),
    ('other_open', 'No, but the digital representation is available under another open content license'),
    ('no_license', 'No, and the digital representation is not available under any open content license.'),
    ('unknown', 'We do not know.')
]

ONLINE_AVAILABILITY_CHOICES = [
    ('not_applicable', 'Not applicable (no IP rights cover the digital representation)'),
    ('rights_assignment', 'Yes. We have entered into a rights assignment agreement that included the assignment of the right to publicly communicate the digital representation.'),
    ('license_agreement', 'Yes. We have entered into a license agreement that includes the right to publicly communicate the digital representation.'),
    ('employee_rights', 'Yes. We acquired the rights due to the work being created by an employee.'),
    ('cc0', 'Yes. The digital representation is available under Creative Commons: CC0'),
    ('cc_by', 'Yes. The digital representation is available under Creative Commons: CC-BY'),
    ('cc_by_sa', 'Yes. The digital representation is available under Creative Commons: CC-BY-SA'),
    ('cc_by_nc_sa', 'Yes. The digital representation is available under Creative Commons: CC-BY-NC-SA'),
    ('cc_by_nd', 'Yes. The digital representation is available under Creative Commons: CC-BY-ND'),
    ('cc_by_nc_nd', 'Yes. The digital representation is available under Creative Commons: CC-BY-NC-ND'),
    ('other_open', 'Yes. The digitization is available under another open content license'),
    ('orphan_works', 'Yes. We base on provisions of law concerning orphan works.'),
    ('out_of_commerce', 'Yes. We base on provisions of law concerning out-of-commerce works.'),
    ('quote_right', 'Yes. We base on provisions of law (right to quote).'),
    ('other_law', 'Yes. We base on other provisions of law.'),
    ('no', 'No.'),
    ('unknown', 'We do not know.')
]

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
        description="Describe igital representation is protected by copyright (it was made by a human and is original, i.e. it is its author's own intellectual creation). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.",
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    audio_recording_rights = SelectField(
        'Rights to audio recordings (phonograms)',
        description='Describe whether the digital representation is protected by rights to audio recordings or phonograms ( fixation of the sounds of a performance or of other sounds, or of a representation of sounds, other than in the form of a fixation incorporated in a cinematographic or other audiovisual work). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    film_fixation_rights = SelectField(
        'Film fixation rights',
        description='Describe whether the digital representation is protected by rights to film fixations or videograms (recording of moving images, with or without sound, regardless of whether it constitutes a cinematographic or audiovisual work). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    performance_rights = SelectField(
        'Performance rights',
        description='Describe whether the digital representation is protected by performance rights (the rights that protect  actors, singers, musicians, dancers, and other persons who act, sing, deliver, declaim, play in, interpret, or otherwise perform literary or artistic works or expressions of folklore). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
        choices=IP_RIGHTS_CHOICES,
        default='no'
    )
    other_ip_rights = SelectField(
        'Other IP rights',
        description='Describe whether the digital representation is protected by any other IP rights. For example, some countries provide protection for non-original photographs (i.e photographs not covered by copyright). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.',
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
    # Default is 'not_applicable' as defined in CC_LICENSE_CHOICES
    copyright = SelectField('Copyright', choices=CC_LICENSE_CHOICES)
    audio_recording_rights = SelectField('Audio recordings', choices=CC_LICENSE_CHOICES)
    film_fixation_rights = SelectField('Film fixations', choices=CC_LICENSE_CHOICES)
    performance_rights = SelectField('Performance rights', choices=CC_LICENSE_CHOICES)
    other_ip_rights = SelectField('Other IP rights', choices=CC_LICENSE_CHOICES)

class CopyrightForm(FlaskForm):
    """
    Main form for copyright assessment.
    
    This is the primary form that integrates all subforms and captures comprehensive
    information about an object's copyright status, including:
    - Basic object information
    - Author details (supports multiple authors)
    - Creation and publication data
    - Rights status and ownership
    - Digital representation details
    
    The form uses nested structures (FieldList, FormField) to handle complex
    relationships like multiple authors and various types of rights.
    """
    # Basic Information section
    object_name = StringField(
        'Name of the object',
        description='Enter the name or title of the object being evaluated.'
    )
    
    institution_name = StringField(
        'Name of the institution',
        description='Enter the name of your institution.'
    )

    object_url = StringField(
        'URL',
        description='Enter the URL of the object being evaluated.'
    )

    # General section - Copyright work status
    is_copyright_work = SelectField(
        'Do you consider the object to be a work within the meaning of copyright law (it was made by a human and is original, i.e. it is its author\'s own intellectual creation)?',
        description='For example, works include: books, pamphlets and other writings; lectures, addresses, sermons and other works of the same nature; dramatic or dramatico-musical works; choreographic works and entertainments in dumb show; musical compositions with or without words; cinematographic works to which are assimilated works expressed by a process analogous to cinematography; works of drawing, painting, architecture, sculpture, engraving and lithography; photographic works to which are assimilated works expressed by a process analogous to photography; works of applied art; illustrations, maps, plans, sketches and three-dimensional works relative to geography, topography, architecture or science (Article 2.1 of the Berne Convention)',
        choices=[
            ('work', 'Yes'),
            ('not_work', 'No'),
            ('uncertain', 'Uncertain')
        ]
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
            ('rightholder_us', 'Yes, our institution'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    object_copyright_rights_acquired_to_make_available = SelectField(
        'Did you acquire rights that enable you to make the digital representation available online, in connection with all the relevant rights?',
        choices=ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
    )

    # Digital representation section
    digital_repr_nature = SelectField(
        'What is the nature of the digital representation?',
        choices=DIGITAL_REPR_NATURE_CHOICES
    )
    
    # Nested forms for IP rights assessment
    digital_repr_ip_rights = FormField(IPRightsForm)
    digital_repr_ip_rights_acquired = FormField(IPRightsAcquiredForm)
    
    digital_repr_rights_acquired_to_make_available = SelectField(
        'Did you acquire rights that enable you to make the digital representation available online, in connection with all the relevant rights?',
        choices=ONLINE_AVAILABILITY_CHOICES,
        default='not_applicable'
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