from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, FieldList, FormField, BooleanField
from wtforms.validators import Optional, NumberRange
from datetime import datetime
from data.country_codes import COUNTRY_CODES, is_eea_country, is_eu_country

class AuthorForm(FlaskForm):
    class Meta:
        # This is crucial - it disables CSRF for the subform
        csrf = False
    
    identity_known = BooleanField('Identity known (this author is not anonymous or pseudonymous)')
    country_of_origin = SelectField('Country of Origin', choices=COUNTRY_CODES)

    def get_country_status(self):
        """Get the EU/EEA status of the author's country."""
        return {
            'is_eu': is_eu_country(self.country_of_origin.data),
            'is_eea': is_eea_country(self.country_of_origin.data)
        }

class CopyrightForm(FlaskForm):
    object_name = StringField(
        'Name of the object',
        description='Enter the name or title of the object being evaluated.'
    )
    
    institution_name = StringField(
        'Name of the institution',
        description='Enter the name of your institution.'
    )

    is_copyright_work = SelectField(
        'Do you consider the object to be a work within the meaning of copyright law (it was made by a human and is original, i.e. it is its author\'s own intellectual creation)?',
        description='For example, works include: books, pamphlets and other writings; lectures, addresses, sermons and other works of the same nature; dramatic or dramatico-musical works; choreographic works and entertainments in dumb show; musical compositions with or without words; cinematographic works to which are assimilated works expressed by a process analogous to cinematography; works of drawing, painting, architecture, sculpture, engraving and lithography; photographic works to which are assimilated works expressed by a process analogous to photography; works of applied art; illustrations, maps, plans, sketches and three-dimensional works relative to geography, topography, architecture or science (Article 2.1 of the Berne Convention)',
        choices=[
            ('work', 'Yes'),
            ('not_work', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    created_before_1850 = SelectField(
        'Was the work created in 1850 or earlier?',
        description='If the object in question is a transformed version of another work, such as a translation or critical edition, you should take into account the date of the creation of the transformed version.',
        choices=[
            ('made_before_1850', 'Yes'),
            ('not_made_before_1850', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    is_derivative = SelectField(
        'Is the work in question a derivative work (e.g., adaptation or translation of another work)?',
        choices=[
            ('derivative', 'Yes'),
            ('not_derivative', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    is_compound = SelectField(
        'Does the work contain other works (e.g., illustrations, quoted poems, sheet music)?',
        choices=[
            ('compound', 'Yes'),
            ('not_compound', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    is_photography = SelectField(
        'Is the object a photography or a picture made with a similar technique?',
        choices=[
            ('photography_with_notice', 'Yes, and there is a copyright notice on it'),
            ('photography_without_notice', 'Yes, but without a copyright notice on it'),
            ('not_photography', 'No')
        ]
    )

    authors = FieldList(FormField(AuthorForm), min_entries=1)

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

    country_first_publication = SelectField(
        'In which country was the work published for the first time?',
        description='If the country is unknown, select "Unknown".',
        choices=COUNTRY_CODES
    )

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

    cinematographic_country = SelectField(
        'If the object in question is a cinematographic work, select the country of the headquarters or habitual residence of the author.',
        description='E.g. amateur cinematographic recordings.',
        choices=COUNTRY_CODES
    )

    architecture_country = SelectField(
        'If the object in question is a work of architecture that was built, or a work incorporated in a building or another structure, select the country of its location.',
        choices=COUNTRY_CODES
    )

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

    original_rightholder = SelectField(
        'Who originally held the copyright?',
        description='Normally, copyright belongs initially to the author who created the work. Exceptionally copyright law may designate a legal person (e.g., a publisher or an employer) as the initial rightholder. This should not be confused with situations in which the author is the original rightholder and transfers/assigns copyright to another person.',
        choices=[
            ('human_author', 'Author(s)'),
            ('legal_person', 'Another entity (e.g. publisher, film producer)'),
            ('uncertain', 'Uncertain')
        ]
    )

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
            ('rightholder_us', 'Yes, our institution'),
            ('rightholder_not_us', 'Yes, not our institution'),
            ('rightholder_unknown', 'No'),
            ('uncertain', 'Uncertain')
        ]
    )

    def get_publication_status(self):
        """Get the EU/EEA status of publication countries."""
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
        """Get the EU/EEA status of all authors."""
        return [author_form.get_country_status() for author_form in self.authors] 