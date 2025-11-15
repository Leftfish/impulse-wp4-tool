# pylint: disable=line-too-long

# Application version (A.B.C.D)
APP_VERSION = "0.4.3+dig_repr_rebuild_in_progress"


# Basic information about the object (form constants)
OBJECT_NAME_LABEL = "Name of the object"
OBJECT_NAME_DESCRIPTION = "Enter the name or title of the object being evaluated."

INSTITUTION_NAME_LABEL = "Name of the collection"
INSTITUTION_NAME_DESCRIPTION = "Select the collection this object belongs to."

OBJECT_URL_LABEL = "URL"
OBJECT_URL_DESCRIPTION = "Enter the URL of the object being evaluated."

OBJECT_COLLECTION_OWNERSHIP_LABEL = "Collection ownership"
OBJECT_COLLECTION_OWNERSHIP_DESCRIPTION = "Specify whether the object is in your institution's collection or another institution's collection."
OBJECT_COLLECTION_OWNERSHIP_CHOICES = [
    ("own_collection", "The object is in the collection of my institution"),
    ("other_institution", "The object is in the collection of another institution"),
]

COLLECTION_CHOICES = [
    ("fictional_test_collection", "Fictional Test Collection For Test Purposes"),
    (
        "film_museum_costume",
        "Film Museum Potsdam: Costume Design & Scenography Collection",
    ),
    ("film_museum_tech", "Film Museum Potsdam: Film & Cinema Technology Collection"),
    ("film_museum_props", "Film Museum Potsdam: Props Collection"),
    (
        "film_uni_holocaust",
        "Film University Babelsberg: Volumetric Contemporary Testimony of Holocaust Survivors Collection",
    ),
    ("heritage_malta_dockyard", "Heritage Malta: Dockyard Collection"),
    ("heritage_malta_maritime", "Heritage Malta: Maritime Collection"),
    (
        "ju_art_science",
        "Jagiellonian University: Collections of Art and Scientific Objects",
    ),
    ("ju_humboldt", "Jagiellonian University: Humboldt"),
    ("ju_natural", "Jagiellonian University: Natural Collections"),
    ("ju_virtual_museums", "Jagiellonian University: Virtual Museums"),
    ("ju_patrimonium", "Jagiellonian University: Patrimonium"),
    ("ju_slub_dresden", "Jagiellonian University: SLUB Dresden"),
    ("ku_leuven_antiquo", "KU Leuven: Collectio Academia Antiquo"),
    ("ku_leuven_corble", "KU Leuven: Corble"),
    ("ku_leuven_glass", "KU Leuven: Glass Slides"),
    ("ku_leuven_incunabula", "KU Leuven: Incunabula"),
    ("ku_leuven_jesuitica", "KU Leuven: Jesuitica"),
    ("ku_leuven_magister", "KU Leuven: Magister Dixit"),
    ("ku_leuven_manuscripts", "KU Leuven: Manuscripts"),
    ("ku_leuven_postcards", "KU Leuven: Picture Postcards"),
    ("ku_leuven_theses", "KU Leuven: Theses"),
    ("magna_zmien_archives", "Magna Zmien: Archives"),
    ("magna_zmien_temples", "Magna Zmien: Temples"),
    ("nkua_3d_scans", "NKUA Museum: 3D Scans of Scientific Instruments"),
    ("nkua_interviews", "NKUA Museum: Interviews"),
    ("nkua_mascagni", "NKUA Museum: Mascagni Atlas"),
    ("nkua_portraits", "NKUA Museum: Portraits"),
    ("thessaloniki_astir", "Thessaloniki Festival: Astir Archival"),
    ("thessaloniki_books", "Thessaloniki Festival: Books"),
    ("thessaloniki_brochures", "Thessaloniki Festival: Brochures"),
    ("thessaloniki_catalogues", "Thessaloniki Festival: Festival Catalogues"),
    ("thessaloniki_magazine", "Thessaloniki Festival: Festival Magazine"),
    ("thessaloniki_megaposters", "Thessaloniki Festival: Hellafi Megaposters"),
    ("thessaloniki_magazines", "Thessaloniki Festival: Magazines"),
    ("thessaloniki_photos", "Thessaloniki Festival: Photos"),
    ("thessaloniki_posters", "Thessaloniki Festival: Posters"),
    ("thessaloniki_publications", "Thessaloniki Festival: Publications"),
    ("europeana", "Europeana"),
    ("wikidata", "Wikidata"),
    ("other", "Other"),
]

# Object: copyright protection (form constants)

COPYRIGHT_IS_WORK_QUESTION = 'Do you consider the object to be a work within the meaning of copyright law (it was made by a human and is original, i.e. it is its author\'s own intellectual creation)? If you select "No" here, skip to part I.2 of the form.'

COPYRIGHT_IS_WORK_DESCRIPTION = "For example, works include: books, pamphlets and other writings; lectures, addresses, sermons and other works of the same nature; dramatic or dramatico-musical works; choreographic works and entertainments in dumb show; musical compositions with or without words; cinematographic works to which are assimilated works expressed by a process analogous to cinematography; works of drawing, painting, architecture, sculpture, engraving and lithography; photographic works to which are assimilated works expressed by a process analogous to photography; works of applied art; illustrations, maps, plans, sketches and three-dimensional works relative to geography, topography, architecture or science (Article 2.1 of the Berne Convention)"

COPYRIGHT_IS_WORK_CHOICES = [
    ("work", "Yes"),
    ("not_work", "No"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_IS_BEFORE_1850_QUESTION = "Was the work created in 1850 or earlier?"
COPYRIGHT_IS_BEFORE_1850_DESCRIPTION = (
    "If the object in question is a derivative or another transformed version of another work, such as a translation or critical edition, "
    "you should take into account the date of the creation of the transformed version."
)
COPYRIGHT_IS_BEFORE_1850_CHOICES = [
    ("not_made_before_1850", "No"),
    ("made_before_1850", "Yes"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_IS_DERIVATIVE_QUESTION = "Is the work in question a derivative work?"
COPYRIGHT_IS_DERIVATIVE_DESCRIPTION = "Examples of derivative works include adaptations or translations."
COPYRIGHT_IS_DERIVATIVE_CHOICES = [
    ("not_derivative", "No"),
    ("derivative", "Yes"),
    ("uncertain", "Uncertain"),
]
COPYRIGHT_IS_COMPOUND_QUESTION = "Does the work contain other works (e.g., illustrations, quoted poems, sheet music)?"
COPYRIGHT_IS_COMPOUND_DESCRIPTION = "For example, a book that contains illustrations, photographs or quoted poems; a video with background music."
COPYRIGHT_IS_COMPOUND_CHOICES = [
    ("not_compound", "No"),
    ("compound", "Yes"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_IS_PHOTOGRAPHY_QUESTION = (
    "Is the object a photography or a picture made with a similar technique?"
)
COPYRIGHT_IS_PHOTOGRAPHY_CHOICES = [
    ("not_photography", "No"),
    ("photography_with_notice", "Yes, and there is a copyright notice on it"),
    ("photography_without_notice", "Yes, but without a copyright notice on it"),
]

COPYRIGHT_PHYSICALLY_PUBLISHED_QUESTION = "Was the work published, i.e. made publicly available on a physical medium (e.g. a printed book, a CD) with the rightholder's consent?"

COPYRIGHT_PHYSICALLY_PUBLISHED_DESCRIPTION = (
    "Publication means manufacture of physical copies, provided that the availability of such copies has been such as to satisfy the reasonable requirements of the public. "
    "The performance of a dramatic, dramatico-musical, cinematographic or musical work, the public recitation of a literary work, the communication by wire or the broadcasting of literary or artistic works, "
    "the exhibition of a work of art and the construction of a work of architecture are not taken into account here."
)

COPYRIGHT_PHYSICALLY_PUBLISHED_CHOICES = [
    ("published_on_physical_medium", "Yes"),
    ("not_published_on_physical_medium", "No"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_COUNTRY_FIRST_PUBLICATION_QUESTION = (
    "In which country was the work published for the first time?"
)

COPYRIGHT_COUNTRY_FIRST_PUBLICATION_DESCRIPTION = (
    'If the country is unknown, select "Unknown".'
)

COPYRIGHT_SIMULTANEOUS_PUBLICATION_COUNTRY_QUESTION = "If the work was republished within thirty days of its first publication, indicate the country in which that subsequent publication took place."

COPYRIGHT_OTHERWISE_AVAILABLE_QUESTION = "Regardless of whether it was published or not, was the object otherwise made available to the public with the rightholder’s consent, for example through radio or TV broadcasting, or via the Internet?"

COPYRIGHT_INTERNET_FIRST_AVAILABLE_QUESTION = "If the object was first made available on the Internet, was it possible for users to download a copy (as opposed to accessing it through streaming only)?"

COPYRIGHT_FIRST_PUBLICATION_YEAR_QUESTION = "If the work was published, i.e. made publicly available on a physical medium (e.g. a printed book, a CD) with the rightholder's consent, indicate the year of the first publication."
COPYRIGHT_FIRST_PUBLICATION_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. For BC dates, enter a negative number (e.g., -500 for 500 BC). If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

COPYRIGHT_FIRST_AVAILABLE_YEAR_QUESTION = "If the object was made available to the public with the rightholder’s consent in a manner other than publication (e.g., through radio or TV broadcasting, or via the Internet), indicate the year when it was first made available."
COPYRIGHT_FIRST_AVAILABLE_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. For BC dates, enter a negative number (e.g., -500 for 500 BC). If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

COPYRIGHT_CREATION_YEAR_LABEL = "When was the work created? Enter the year. "

COPYRIGHT_CREATION_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025).Do not enter anything (leave the field blank) if the year is unknown. For BC dates, enter a negative number (e.g., -500 for 500 BC). If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

COPYRIGHT_TERRITORY_STATUS_CHANGED_LABEL = "When answering the previous questions, did you encounter the problem of changing status of territories (e.g. dissolution of a country, a country obtaining independence from a colonial power etc.)?"

CINEMATOGRAPHIC_COUNTRY_LABEL = "If the object is a cinematographic work, indicate the country of the producer’s headquarters or habitual residence (i.e., the country where the producer normally lives and has the centre of their life interests)."
CINEMATOGRAPHIC_COUNTRY_DESCRIPTION = "E.g. amateur cinematographic recordings."

ARCHITECTURE_COUNTRY_LABEL = "If the object in question is a work of architecture that was built, or a work incorporated in a building or another structure, select the country of its location."

COPYRIGHT_OTHERWISE_AVAILABLE_CHOICES = [
    ("made_available_no_medium", "Yes"),
    ("not_made_available_no_medium", "No"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_INTERNET_FIRST_AVAILABLE_CHOICES = [
    ("not_made_available_internet", "No / Not applicable"),
    ("made_available_internet", "Yes"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_ORIGINAL_RIGHTHOLDER_LABEL = "Who originally held the copyright?"
COPYRIGHT_ORIGINAL_RIGHTHOLDER_DESCRIPTION = "Normally, copyright belongs initially to the author who created the work. Exceptionally copyright law may designate a legal person (e.g., a publisher or an employer) as the initial rightholder. This should not be confused with situations in which the author is the original rightholder and transfers/assigns copyright to another person."
COPYRIGHT_ORIGINAL_RIGHTHOLDER_CHOICES = [
    ("human_author", "Author(s)"),
    ("legal_person", "Another entity (e.g. publisher, film producer)"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_AUTHOR_ALIVE_LABEL = (
    "Is the identified (i.e. not anonymous and not pseudonymous) author, or at least one of the identified co-authors, still alive?"
)
COPYRIGHT_AUTHOR_ALIVE_CHOICES = [
    ("author_alive", "Yes"),
    ("author_dead", "No"),
    ("uncertain", "Uncertain"),
]

COPYRIGHT_AUTHOR_DEATH_YEAR_LABEL = "If the author (or all the co-authors) passed away, enter the year of death of the author or the last living co-author."
COPYRIGHT_AUTHOR_DEATH_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. For BC dates, enter a negative number (e.g., -500 for 500 BC). If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

# Object: performance protection (form constants)

PERFORMANCE_IS_PERFORMANCE_QUESTION = "Do you consider the object to include a performance (e.g. people dancing, singing, acting, miming, reciting a text)? If you select \"No\" here, skip to part I.3 of the form."
PERFORMANCE_IS_PERFORMANCE_DESCRIPTION = 'Performers are "actors, singers, musicians, dancers, and other persons who act, sing, deliver, declaim, play in, interpret, or otherwise perform literary or artistic works or expressions of folklore" (WIPO Performances and Phonograms Treaty)'
PERFORMANCE_CHOICES = [
    ("not_performance", "No"),
    ("performance", "Yes"),
    ("uncertain", "Uncertain"),
]

PERFORMANCE_BEFORE_1900_QUESTION = "Was the performance made in 1900 or earlier?"
PERFORMANCE_BEFORE_1900_DESCRIPTION = "Note that this question concerns the original performance, not any copies made some time after the performance took place."
PERFORMANCE_BEFORE_1900_CHOICES = [
    ("performance_not_made_before_1900", "No"),
    ("performance_made_before_1900", "Yes"),
    ("uncertain", "Uncertain"),
]

PERFORMANCE_IS_COMPOUND_QUESTION = "Are multiple performances contained in the same object (e.g., a movie which includes acting and singing)?"
PERFORMANCE_COMPOUND_CHOICES = [
    ("not_compound", "No"),
    ("compound", "Yes"),
    ("uncertain", "Uncertain"),
]

PERFORMANCE_YEAR_QUESTION = "When was the performance made?"

PERFORMANCE_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. For BC dates, enter a negative number (e.g., -500 for 500 BC). If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

PERFORMANCE_PHONOGRAM_AVAILABLE_QUESTION = "Was the performance lawfully published on a physical medium that was a phonogram OR made publically available from a fixed medium that was a phonogram?"
PERFORMANCE_PHONOGRAM_AVAILABLE_DESCRIPTION = "A phonogram is a \"fixation of the sounds of a performance or of other sounds, or of a representation of sounds, other than in the form of a fixation incorporated in a cinematographic or other audiovisual work;\" (WIPO Performances and Phonograms Treaty) E.g., a vinyl sold in music shops, or music streamed online from a master recording."

PERFORMANCE_PHONOGRAM_AVAILABLE_CHOICES = [
    ("performance_phonogram_available", "Yes"),
    ("performance_phonogram_not_available", "No"),
    ("uncertain", "Uncertain"),
]

PERFORMANCE_PHONOGRAM_AVAILABLE_YEAR_QUESTION = "If you answered “Yes” to the previous question, please specify the year of the first such event."
PERFORMANCE_PHONOGRAM_AVAILABLE_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_QUESTION = "Was the performance lawfully published on a physical medium, but not on a phonogram OR made publically available from a fixed medium, but not on a phonogram?"

PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_DESCRIPTION = "E.g. a VHS with a recording of a concert, or a video made available online from a master recording."

PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_CHOICES = [
    ("performance_fixed_not_phonogram_available", "Yes"),
    ("performance_fixed_not_phonogram_not_available", "No"),
    ("uncertain", "Uncertain"),
]

PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_YEAR_QUESTION = "If you answered “Yes” to the previous question, please specify the year of the first such event."

PERFORMANCE_FIXED_NOT_PHONOGRAM_AVAILABLE_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

# Object: phonogram rights (form constants)

PHONOGRAM_IS_PHONOGRAM_QUESTION = "Do you consider the object to include a phonogram?  If you select \"No\" here, skip to part I.4 of the form."
PHONOGRAM_IS_PHONOGRAM_DESCRIPTION = 'A phonogram is a "fixation of the sounds of a performance or of other sounds, or of a representation of sounds, other than in the form of a fixation incorporated in a cinematographic or other audiovisual work;" (WIPO Performances and Phonograms Treaty)'
PHONOGRAM_CHOICES = [
    ("not_phonogram", "No"),
    ("phonogram", "Yes"),
    ("uncertain", "Uncertain"),
]

PHONOGRAM_BEFORE_1900_QUESTION = "Was the recording made in 1900 or earlier?"

PHONOGRAM_BEFORE_1900_CHOICES = [
    ("phonogram_not_made_before_1900", "No"),
    ("phonogram_made_before_1900", "Yes"),
    ("uncertain", "Uncertain"),
]

PHONOGRAM_IS_COMPOUND_QUESTION = "Are multiple recordings contained in the same object?"

PHONOGRAM_IS_COMPOUND_DESCRIPTION = "For example, it is a collection of multiple recordings or a recording that is complex, i.e. it is made from various recordings."

COMPOUND_PHONOGRAM_CHOICES = [
    ("not_compound", "No"),
    ("compound", "Yes"),
    ("uncertain", "Uncertain"),
]

PHONOGRAM_YEAR_QUESTION = "When was the recording made?"

PHONOGRAM_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

PHONOGRAM_PUBLISHED_FIXED_MEDIUM_QUESTION = (
    "Was the recording lawfully published on a physical medium?"
)

PHONOGRAM_PUBLISHED_FIXED_MEDIUM_DESCRIPTION = "E.g., a vinyl sold in music shops."

PHONOGRAM_PUBLISHED_FIXED_MEDIUM_CHOICES = [
    ("phonogram_published_fixed_medium", "Yes"),
    ("phonogram_not_published_fixed_medium", "No"),
    ("uncertain", "Uncertain"),
]

PHONOGRAM_PUBLISHED_FIXED_MEDIUM_YEAR_QUESTION = (
    "If you answered “Yes” to the previous question, please specify the year of the first such event."
)

PHONOGRAM_PUBLISHED_FIXED_MEDIUM_YEAR_DESCRIPTION = (
    "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."
)

PHONOGRAM_AVAILABLE_NO_MEDIUM_QUESTION = (
    "Was the recording lawfully made publically available without a fixed medium?"
)

PHONOGRAM_AVAILABLE_NO_MEDIUM_DESCRIPTION = (
    "E.g., a radio show was broadcasted, but not registered on a physical medium."
)

PHONOGRAM_NO_MEDIUM_CHOICES = [
    ("phonogram_publically_available_no_medium", "Yes"),
    ("phonogram_not_publically_available_no_medium", "No"),
    ("uncertain", "Uncertain"),
]

PHONOGRAM_AVAILABLE_NO_MEDIUM_YEAR_QUESTION = (
    "If you answered “Yes” to the previous question, please specify the year of the first such event."
)

PHONOGRAM_AVAILABLE_NO_MEDIUM_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

# Object: film fixation rights (form constants)

FILM_IS_FILM_FIXATION_QUESTION = "Do you consider the object to include a film fixation / a cinematographic or other audiovisual work which is NOT incorporated in a cinematographic or other audiovisual work?  If you select \"No\" here, skip to part I.5 of the form."
FILM_IS_FILM_FIXATION_DESCRIPTION = 'The first fixation of a film (videogram) refers to a fixation of a cinematographic or audiovisual work, or any sequence of moving images, whether or not accompanied by sound. It is important to note that the first fixation of a film (videogram) may concern both materials that constitute audiovisual works protected by copyright law (for example, feature films or documentaries) and other sequences of moving images that do not themselves qualify as works under copyright law — such as surveillance camera footage, simple interview recordings, or short social-media clips.'

FILM_FIXATION_CHOICES = [
    ("not_film_fixation", "No"),
    ("film_fixation", "Yes"),
    ("uncertain", "Uncertain"),
]

FILM_BEFORE_1900_QUESTION = "Was the film fixation made in 1900 or earlier?"
FILM_FIXATION_BEFORE_1900_CHOICES = [
    ("film_fixation_not_made_before_1900", "No"),
    ("film_fixation_made_before_1900", "Yes"),
    ("uncertain", "Uncertain"),
]

FILM_IS_COMPOUND_QUESTION = "Are multiple film fixations contained in the same object?"
FILM_IS_COMPOUND_DESCRIPTION = "For example, it is a collection of multiple film fixations or a film fixation that is complex, i.e. it is made from various film fixations."
COMPOUND_FILM_FIXATION_CHOICES = [
    ("not_compound", "No"),
    ("compound", "Yes"),
    ("uncertain", "Uncertain"),
]
FILM_YEAR_QUESTION = "When was the film fixation made?"

FILM_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."

FILM_PUBLISHED_FIXED_MEDIUM_QUESTION = (
    "Was the film fixation lawfully published on a physical medium?"
)

FILM_PUBLISHED_FIXED_MEDIUM_DESCRIPTION = "E.g., a DVD sold in shops."

FILM_FIXATION_PUBLISHED_FIXED_MEDIUM_CHOICES = [
    ("film_fixation_published_fixed_medium", "Yes"),
    ("film_fixation_not_published_fixed_medium", "No"),
    ("uncertain", "Uncertain"),
]

FILM_PUBLISHED_FIXED_MEDIUM_YEAR_QUESTION = (
    "If you answered “Yes” to the previous question, please specify the year of the first such event."
)

FILM_PUBLISHED_FIXED_MEDIUM_YEAR_DESCRIPTION = (
    "Enter the year as a four-digit year value (e.g. 2025). ter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."
)

FILM_AVAILABLE_NO_MEDIUM_QUESTION = (
    "Was the film fixation lawfully made publically available without a fixed medium?"
)

FILM_AVAILABLE_NO_MEDIUM_DESCRIPTION = (
    "E.g., a film was broadcasted on TV, but not registered on a physical medium."
)

FILM_FIXATION_NO_MEDIUM_CHOICES = [
    ("film_fixation_publically_available_no_medium", "Yes"),
    ("film_fixation_not_publically_available_no_medium", "No"),
    ("uncertain", "Uncertain"),
]

FILM_AVAILABLE_NO_MEDIUM_YEAR_QUESTION = "If you answered “Yes” to the previous question, please specify the year of the first such event."

FILM_AVAILABLE_NO_MEDIUM_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."


# Object: broadcasting organisation rights (form constants)

BROADCAST_IS_BROADCAST_QUESTION = "Do you consider the object to include a broadcast?  If you select \"No\" here, skip to part I.6 of the form."

BROADCAST_IS_BROADCAST_DESCRIPTION = (
    "“broadcasting” means the transmission by wireless means for public reception of sounds or of images and sounds (International Convention for the Protection of Performers, Producers of Phonograms and Broadcasting Organizations). "
    "The notion includes TV broadcasts, radio broadcasts, as well as internet broadcasts other than video-on-demand similar services."
)

BROADCAST_CHOICES = [
    ("not_broadcast", "No"),
    ("broadcast", "Yes"),
    ("uncertain", "Uncertain"),
]

BROADCAST_BEFORE_1970_QUESTION = "Was the broadcast made in 1970 or earlier?"

BROADCAST_BEFORE_1970_CHOICES = [
    ("broadcast_not_made_before_1970", "No"),
    ("broadcast_made_before_1970", "Yes"),
    ("uncertain", "Uncertain"),
]

BROADCAST_IS_COMPOUND_QUESTION = "Are multiple broadcasts contained in the same object?"

BROADCAST_IS_COMPOUND_DESCRIPTION = (
    "For example, it is a documentary film in which multiple broadcasts of TV news programs are incorporated."
)

COMPOUND_BROADCAST_CHOICES = [
    ("not_compound", "No"),
    ("compound", "Yes"),
    ("uncertain", "Uncertain"),
]

BROADCAST_YEAR_QUESTION = "When was the broadcast made?"

BROADCAST_YEAR_DESCRIPTION = (
    "Enter the year as a four-digit year value (e.g. 2025). Do not enter anything (leave the field blank) if the year is unknown. If you know the timespan, enter the latest possible year (e.g. if you know something happened between 1930 and 1960, enter 1960)."
)

# Object: other IP rights (form constants)
POTENTIAL_FIRST_EDITION_NOT_WORK_LABEL = "If the object is not a work, has it already been published ( i.e. made publicly available on a physical medium, such as a printed book, a CD) or otherwise made available to the public?"

POTENTIAL_FIRST_EDITION_NOT_WORK_DESCRIPTION = "In some countries, publications of materials that are not protected by copyright (e.g., some countries exclude protection of official documents and similar content) may nonetheless enjoy IP protection, for example under related rights to first editions."

POTENTIAL_FIRST_EDITION_NOT_WORK_CHOICES = [
    ("not_potential_first_edition_not_work", "No (either it is a work or it has been published or made available to the public)"),
    ("potential_first_edition_not_work", "Yes"),
    ("uncertain", "Uncertain"),
]

CRITICAL_EDITION_LABEL = "Is the object a so-called critical edition (scholarly edition, scientific edition) of a work or a text?"
CRITICAL_EDITION_DESCRIPTION = "An edition can qualify as critical when a work has been restored thanks to the analysis and embedding of data and other components that have been preliminarily selected."

CRITICAL_EDITION_CHOICES = [
    ("not_critical_edition", "No"),
    ("critical_edition", "Yes"),
    ("uncertain", "Uncertain"),
]

PRESS_PUBLICATION_LABEL = "Is the object a press publication?"
PRESS_PUBLICATION_DESCRIPTION = 'A "press publication" is a a collection composed mainly of literary works of a journalistic nature, but which can also include other works or other subject matter, and which satisfies three conditions: (a) it is an individual item within a periodical or regularly updated publication under a single title, such as a newspaper or a general or special interest magazine; (b) it has the purpose of providing the general public with information related to news or other topics; and (c) it is published in any media under the initiative, editorial responsibility and control of a service provider. Periodicals that are published for scientific or academic purposes, such as scientific journals, are not press publications.'

PRESS_PUBLICATION_CHOICES = [
    ("not_press_publication", "No"),
    ("press_publication", "Yes"),
    ("uncertain", "Uncertain"),
]

PRESS_PUBLICATION_YEAR_LABEL = (
    "If you answered \"Yes\" to the question about the object being a press publication, indicate the year when it was published."
)
PRESS_PUBLICATION_YEAR_DESCRIPTION = "Enter the year as a four-digit year value (e.g. 2025)."

TRADEMARK_LABEL = (
    "Is the object a trademark (registered or unregistered) OR does it depict a trademark?"
)
TRADEMARK_DESCRIPTION = "A trademark is a sign such as a word, logo, slogan, shape or sound that identifies goods or services as coming from a particular business and distinguishes them from others. Trademarks may be registered in a single countries or for the whole European Union through the European Union Intellectual Property Office (EUIPO)."

TRADEMARK_CHOICES = [
    ("not_trademark", "No"),
    ("trademark", "Yes"),
    ("uncertain", "Uncertain"),
]

DESIGN_LABEL = "Was the object registered as a design during the last 25 years OR does it depict a design registered during the last 25 years?"

DESIGN_CHOICES = [("not_design", "No"), ("design", "Yes"), ("uncertain", "Uncertain")]

# Object: non-IP restrictions (form constants)

OBJECT_CONTRACTUAL_RESTRICTIONS_QUESTION = "Are there any contractual restrictions that limit the scope of use of the object?"
OBJECT_CONTRACTUAL_RESTRICTIONS_DESCRIPTION = "For example: agreements with the owner that restrict the way you can use the object."

CONTRACTUAL_RESTRICTIONS_CHOICES = [
    ("contractual_restrictions", "Yes"),
    ("no_contractual_restrictions", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_ADMINISTRATIVE_RESTRICTIONS_QUESTION = "Are there any administrative restrictions that limit the scope of use of the object?"

OBJECT_ADMINISTRATIVE_RESTRICTIONS_DESCRIPTION = "For example: cultural heritage codes, export controls, museum policies, institutional rules, or government regulations that restrict the way you can use the object."

ADMINISTRATIVE_RESTRICTIONS_CHOICES = [
    ("administrative_restrictions", "Yes"),
    ("no_administrative_restrictions", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_OWNERSHIP_STATUS_QUESTION = "If it is a material object (e.g. sculptures, scientific equipment, paintings), what is the ownership status?"

OBJECT_OWNERSHIP_STATUS_DESCRIPTION = "Please select the option that best describes your legal situation with respect to ownership and usage."

OWNERSHIP_STATUS_CHOICES = [
    ("own_object", "We own the object."),
    (
        "contractual_arrangements",
        "We do not own the object, but we have contractual arrangements with the owner that allow us to use it.",
    ),
    (
        "legal_provisions",
        "We do not own the object, but we can rely on provisions of law to use it.",
    ),
    ("no_basis", "We do not own the object and we have no clear basis for its use."),
    ("unknown_owner", "We do not know who the owner is."),
    ("other", "Other."),
]

OBJECT_PROVENANCE_TRACED_QUESTION = (
    "If it is a material object, is the provenance well-traced?"
)

OBJECT_PROVENANCE_TRACED_DESCRIPTION = (
    "Do you have reliable records of the chain of ownership and transfer?"
)

PROVENANCE_TRACED_CHOICES = [
    ("provenance_traced", "Yes"),
    ("provenance_not_traced", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_PROVENANCE_ISSUES_QUESTION = "If it is a material object, is its provenance associated with troublesome issues (war, colonial, and similar)?"

OBJECT_PROVENANCE_ISSUES_DESCRIPTION = (
    "For example: confiscations, looting, or colonial acquisitions."
)

PROVENANCE_ISSUES_CHOICES = [
    ("provenance_troublesome", "Yes"),
    ("provenance_not_troublesome", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_LIVING_IDENTIFIABLE_INFO_QUESTION = "Does the object contain information (names, image, voice) about living people that can be identified?"

OBJECT_LIVING_IDENTIFIABLE_INFO_DESCRIPTION = "For example: photographs, audio recordings, or manuscripts mentioning living persons."

LIVING_IDENTIFIABLE_INFO_CHOICES = [
    ("contains_identifiable_living", "Yes"),
    ("does_not_contain_identifiable_living", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_SENSITIVE_HISTORICAL_INFO_QUESTION = "Does the object contain sensitive, potentially defamatory information about someone (e.g., WW2 collaboration), including people who are no longer alive?"

OBJECT_SENSITIVE_HISTORICAL_INFO_DESCRIPTION = (
    "For example: documents suggesting misconduct or criminal activity."
)

SENSITIVE_HISTORICAL_INFO_CHOICES = [
    ("contains_sensitive_historical", "Yes"),
    ("does_not_contain_sensitive_historical", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_TOTALITARIAN_ASSOCIATIONS_QUESTION = "Does the object contain something (e.g., content, symbolics) that could be associated with racist, nationalist, or totalitarian ideologies?"

OBJECT_TOTALITARIAN_ASSOCIATIONS_DESCRIPTION = (
    "For example: symbols, slogans, propaganda."
)

TOTALITARIAN_ASSOCIATIONS_CHOICES = [
    ("contains_totalitarian_associations", "Yes"),
    ("does_not_contain_totalitarian_associations", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_DISCRIMINATORY_CONTENT_QUESTION = "Does the object contain content discriminatory or derogatory towards a person, group, or ethnicity?"

OBJECT_DISCRIMINATORY_CONTENT_DESCRIPTION = (
    "For example: racist caricatures, slurs, or mocking representations."
)

DISCRIMINATORY_CONTENT_CHOICES = [
    ("contains_discriminatory", "Yes"),
    ("does_not_contain_discriminatory", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_OTHER_SENSITIVE_CONTENT_QUESTION = (
    "Does the object contain content that, in your opinion, is otherwise sensitive?"
)

OBJECT_OTHER_SENSITIVE_CONTENT_DESCRIPTION = (
    "For example: violent, disturbing, or culturally offensive material."
)

OTHER_SENSITIVE_CONTENT_CHOICES = [
    ("contains_other_sensitive", "Yes"),
    ("does_not_contain_other_sensitive", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_OTHER_PROBLEMS_QUESTION = "Are there any reasons not covered above, that in your opinion would be problematic?"

OBJECT_OTHER_PROBLEMS_DESCRIPTION = "For example: ethical, cultural, or political concerns not addressed in previous questions."

OTHER_PROBLEMS_CHOICES = [
    ("other_problems", "Yes"),
    ("no_other_problems", "No"),
    ("uncertain", "Uncertain"),
]

OBJECT_LEGAL_CONSULTATION_QUESTION = (
    "Have you consulted a lawyer about the legal status of the object (concerning intellectual property or other issues)?"
)
OBJECT_LEGAL_CONSULTATION_DESCRIPTION = (
    "Please specify the type of consultation or reason for not consulting."
)

LEGAL_CONSULTATION_CHOICES = [
    ("in_house_lawyer", "Yes, with an in-house lawyer."),
    ("external_lawyer", "Yes, with an external lawyer."),
    ("no_self_answer", "No. We can answer these questions ourselves."),
    ("no_funds", "No. We do not have the funds to hire a lawyer."),
    ("no_other_reason", "No, other reason."),
]

# Notes field for Section III
OBJECT_RESTRICTIONS_NOTES_LABEL = "If you selected 'Yes' or 'Uncertain' in any of the fields above, describe briefly the reasons."
OBJECT_RESTRICTIONS_NOTES_DESCRIPTION = "Optional. Max 1000 characters."
OBJECT_RESTRICTIONS_NOTES_MAXLEN = 1000

# General notes at the end of the form
GENERAL_NOTES_LABEL = "Do you have any other notes or remarks about the object?"
GENERAL_NOTES_DESCRIPTION = "Optional. Max 1000 characters."
GENERAL_NOTES_MAXLEN = 1000

# Digital representation of the object (form constants)
DIGITAL_REPR_NATURE_QUESTION = "What is the nature of the digital representation?"

DIGITAL_REPR_NATURE_CHOICES = [
    ("obj_2d_to_2d", "2D objects digitized in 2D"),
    ("obj_2d_to_3d", "2D objects digitized in 3D"),
    ("obj_3d_to_2d", "3D objects digitized in 2D"),
    ("obj_3d_to_3d", "3D objects digitized in 3D"),
    ("obj_complex", "digitized complex object (e.g. scanned book, manuscript)"),
    (
        "obj_textual",
        "digitized version of a textual work (e.g. OCR or transcripts, subtitles, captions)",
    ),
    ("obj_translation", "translation into a new language"),
    ("obj_audio", "audio recording"),
    ("obj_audiovisual", "audiovisual work"),
    ("obj_video_other", "other video recordings (e.g. recorded interviews)"),
    ("obj_3d_reconstruction", "3D reconstruction"),
    ("other_digital_repr", "other digital representation"),
]

DIGITAL_REPR_RIGHTS_ACQUIRED_QUESTION = "Did you otherwise acquire rights that enable you to make the digital representation itself available online and allow others to use it or modify it (e.g. through rights transfer, license agreement, or legal provisions)?"
DIGITAL_REPR_RIGHTS_AVAILABILITY_DESCRIPTION = """According to your knowledge, is the digital representation itself covered by any of the following intellectual property rights? Please note that a digital representation may be protected by several rights at the same time (for example, copyright in an audiovisual work and neighbouring rights in a videogram, in the case of a creative video recording of an interview). Furthermore, is the digital representation made available under a Creative Commons or another open content licence, or have you otherwise acquired rights that enable you to make it available online and allow others to use or modify it?"""

COMBINED_AVAILABILITY_CHOICES = [
    ("not_applicable", "Not applicable (not covered by this IP right)"),
    # CC license choices
    ("cc0", "Yes. Available under Creative Commons: CC0"),
    ("cc_by", "Yes. Available under Creative Commons: CC-BY"),
    ("cc_by_sa", "Yes. Available under Creative Commons: CC-BY-SA"),
    ("cc_by_nc_sa", "Yes. Available under Creative Commons: CC-BY-NC-SA"),
    ("cc_by_nd", "Yes. Available under Creative Commons: CC-BY-ND"),
    ("cc_by_nc_nd", "Yes. Available under Creative Commons: CC-BY-NC-ND"),
    ("other_open", "Yes. Available under a non-CC open content license"),
    # Rights acquisition choices
    ("rights_assignment", "Yes. Rights assigned through agreement"),
    ("license_agreement", "Yes. Licensed through agreement"),
    ("employee_rights", "Yes. Rights acquired through employment"),
    # Legal provisions, such as exceptions and limitations
    ("orphan_works", "Yes. Based on orphan works provisions"),
    ("out_of_commerce", "Yes. Based on out-of-commerce works provisions"),
    ("quote_right", "Yes. Based on right to quote"),
    ("other_law", "Yes. Based on other legal provisions"),
    ("no", "No"),
    ("unknown", "Unknown"),
]

COMBINED_AVAILABILITY_CHOICES_DESCRIPTION = {
    "copyright": "Availability under open content license or other rights acquisition for copyright.",
    "audio_recordings": "Availability under open content license or other rights acquisition for audio recording rights.",
    "film_fixation": "Availability under open content license or other rights acquisition for film fixation rights.",
    "performance": "Availability under open content license or other rights acquisition for performance rights.",
    "other": "Availability under open content license or other rights acquisition for other rights.",
}

# Rights acquisition constants

CURRENT_RIGTHHOLDER_QUESTION = {'copyright': 'Do you know who currently holds the copyright?',
    'performance': 'Do you know who currently holds the performance rights?',
    'audio_recordings': 'Do you know who currently holds the audio recording rights?',
    'film_fixation': 'Do you know who currently holds the film fixation rights?',
    'broadcast': 'Do you know who currently holds the broadcast rights?',
    'other': 'Do you know who currently holds the rights?'
    }

CURRENT_RIGHTHOLDER_DESCRIPTION = {'copyright': 'This question refers to copyright ownership. Please do not select “Yes” if you are only a licensee or if you know only who holds a licence to use the work.',
    'performance': "Note that this question is independent from similar questions pertaining to other rights (e.g. copyright). Please do not select “Yes” if you are only a licensee or if you know only who holds a licence to use the work.",
    'audio_recordings': "Please note that this question is separate from similar questions concerning other rights (e.g., copyright). Please do not select “Yes” if you are only a licensee or if you know only who holds a licence to use the work.",
    'film_fixation': "Note that this question is independent from similar questions pertaining to other rights (e.g. copyright). Please do not select “Yes” if you are only a licensee or if you know only who holds a licence to use the work.",
    'broadcast': "Please note that this question is separate from similar questions concerning other rights (e.g., copyright). Please do not select “Yes” if you are only a licensee or if you know only who holds a licence to use the work.",
    'other': "Please note that this question is separate from similar questions concerning other rights (e.g., copyright). Please do not select “Yes” if you are only a licensee or if you know only who holds a licence to use the work."
    }

CURRENT_RIGHTHOLDER_CHOICES = [
    ("rightholder_not_us", "Yes, and it is not our institution"),
    (
        "rightholder_us",
        "Yes, our institution acquired the rights (e.g., due to the work being created by an employee, or entered into a copyright assignment agreement.)",
    ),
    ("rightholder_unknown", "No"),
    ("uncertain", "Uncertain"),
]

RIGHTS_ACQUIRED_LABEL = {'copyright': "Are you otherwise authorised to make the original object available online and to allow others to use and modify it (e.g., through a rights transfer, a licence agreement, or by law)?",
    'performance': "Are you otherwise authorised to make the original object available online and to allow others to use and modify it (e.g., through a rights transfer, a licence agreement, or by law)?",
    'audio_recordings': "Are you otherwise authorised to make the original object available online and to allow others to use and modify it (e.g., through a rights transfer, a licence agreement, or by law)?",
    'film_fixation': "Are you otherwise authorised to make the original object available online and to allow others to use and modify it (e.g., through a rights transfer, a licence agreement  , or by law)?",
    'broadcast': "Are you otherwise authorised to make the original object available online and to allow others to use and modify it (e.g., through a rights transfer, a licence agreement, or by law)?",
    'other': "Are you otherwise authorised to make the original object available online and to allow others to use and modify it (e.g., through a rights transfer, a licence agreement, or by law)?",
    'digital_representation': "Did you otherwise acquire rights that enable you to make the digital representation itself available online and allow others to use it or modify it (e.g. through rights transfer, license agreement, or legal provisions)?"
    }

RIGHTS_ACQUIRED_DESCRIPTION = {'copyright': "Note that this question is independent from similar questions pertaining to other rights (e.g. performance, audio recordings).",
    'performance': "Note that this question is independent from similar questions pertaining to other rights (e.g. copyright).",
    'audio_recordings': "Please note that this question is separate from similar questions concerning other rights (e.g., copyright).",
    'film_fixation': "Note that this question is independent from similar questions pertaining to other rights (e.g. copyright, performances, or phonograms).",
    'broadcast': "Please note that this question is separate from similar questions concerning other rights (e.g., copyright).",
    'other': "Please note that this question is separate from similar questions concerning other rights (e.g., copyright)."
    }

RIGHTS_ACQUIRED_CHOICES = [
    ("no", "No."),
    (
        "license_agreement",
        "We have entered into a license agreement that includes the right to publicly communicate and allow others to use the object/digital representation.",
    ),
    (
        "limited_license_agreement",
        "We have entered into a license agreement that includes the right to publicly communicate the object/digital representation, but we are not authorized to allow others to use or modify it.",
    ),
    ("orphan_works", "We base on provisions of law concerning orphan works."),
    (
        "out_of_commerce",
        "We base on provisions of law concerning out-of-commerce works.",
    ),
    ("quote_right", "We base on provisions of the relevant IP statute that deal with exceptions or limitations (such as right to quote)."),
    ("other_law", "We base on other provisions of law."),
    
    ("unknown", "We do not know."),
    (
        "not_applicable",
        "Not applicable.",
    )
]
CC_LICENSE_LABEL = {'copyright': "If you are not the rightholder, is the object available under a Creative Commons license or another open content license?",
    'performance': "If you are not the rightholder, is the object available under a Creative Commons license or another open content license?",
    'audio_recordings': "If you are not the rightholder, is the object available under a Creative Commons license or another open content license?",
    'film_fixation': "If you are not the rightholder, is the object available under a Creative Commons license or another open content license?",
    'broadcast': "If you are not the rightholder, is the object available under a Creative Commons license or another open content license?",
    'other': "If you are not the rightholder, is the object available under a Creative Commons license or another open content license?"
    }

CC_LICENSE_DESCRIPTION = {'copyright': "If you are the rightholder, select \"Not applicable\". Note that this question is independent from similar questions pertaining to other rights (e.g. performance, audio recordings).",
    'performance': "If you are the rightholder, select \"Not applicable\". Note that this question is independent from similar questions pertaining to other rights (e.g. copyright).",
    'audio_recordings': "If you are the rightholder, select \"Not applicable\". Please note that this question is separate from similar questions concerning other rights (e.g., copyright).",
    'film_fixation': "If you are the rightholder, select \"Not applicable\". Note that this question is independent from similar questions pertaining to other rights (e.g. copyright, performances, or phonograms).",
    'broadcast': "If you are the rightholder, select \"Not applicable\". Please note that this question is separate from similar questions concerning other rights (e.g., copyright).",
    'other': "If you are the rightholder, select \"Not applicable\". Please note that this question is separate from similar questions concerning other rights (e.g., copyright)."
    }

CC_LICENSE_AVAILABILITY_CHOICES = [
    ("no", "No"),
    ("not_applicable", "Not applicable (e.g. because the object is not covered by the right or our institution is the rightholder)"),
    ("cc0", "Yes. Available under Creative Commons: CC0"),
    ("cc_by", "Yes. Available under Creative Commons: CC-BY"),
    ("cc_by_sa", "Yes. Available under Creative Commons: CC-BY-SA"),
    ("cc_by_nc_sa", "Yes. Available under Creative Commons: CC-BY-NC-SA"),
    ("cc_by_nd", "Yes. Available under Creative Commons: CC-BY-ND"),
    ("cc_by_nc_nd", "Yes. Available under Creative Commons: CC-BY-NC-ND"),
    ("other_open", "Yes. It is a non-CC open content license."),
]

DIGITAL_REPR_COPYRIGHT_CURRENTRIGHTHOLDER_QUESTION = ''
DIGITAL_REPR_COPYRIGHT_CURRENTRIGHTHOLDER_DESCRIPTION = ''
DIGITAL_REPR_COPYRIGHT_CC_LICENSE_LABEL = ''
DIGITAL_REPR_COPYRIGHT_CC_LICENSE_DESCRIPTION = ''
DIGITAL_REPR_COPYRIGHT_RIGHTS_ACQUIRED_LABEL = ''
DIGITAL_REPR_COPYRIGHT_RIGHTS_ACQUIRED_DESCRIPTION = ''


# Section titles and descriptions
SECTION_ORIGINAL_OBJECT_TITLE = "Original Object Description"
SECTION_ORIGINAL_OBJECT_DESCRIPTION = (
    "The object as such can be a work according to copyright law. The questions below aim to determine whether, "
    "if it is indeed a work, it has passed into the public domain. Note that the object must be distinguished from its digital representation - here, we only deal with the former. "
    "For example: a painting is the object that is very likely to be an artistic work, while the digital image of the painting is its digital representation; "
    "a short story is the object that is very likely to be a literary work, while a digital recording of a person reading the story would be a digital representation."
)

SECTION_AUTHOR_INFO_TITLE = "Author Information Description"
SECTION_AUTHOR_INFO_DESCRIPTION = "Information about the author may be necessary to determine if the work passed into the public domain."

# Helper texts for identity defaults
AUTHOR_IDENTITY_HELP = ("Add information about the country of origin of at least one author and whether the author's identity is known.",
    "By default, the author's identity is considered known. Check the box if the work was made available anonymously or pseudonymously, and the author's identity was not later admitted or established.")
PERFORMER_IDENTITY_HELP = ("Add information about the country of origin of at least one performer and whether the performer's identity is known.",
    "By default, the performer's identity is considered known. Check the box if the performer is anonymous or pseudonymous.")
PRODUCER_IDENTITY_HELP = ("Add information about the country of origin of at least one producer and whether the producer's identity is known. A producer is the person, or the legal entity, who or which takes the initiative and has the responsibility for the first fixation of the sounds of a performance or other sounds, or the representations of sounds (WIPO Performances and Phonograms Treaty)",
    "By default, the producer's identity is considered known. Check the box if the producer is unknown.")
FILM_FIXATION_PRODUCER_IDENTITY_HELP = ("Add information about the country of origin of at least one film fixation producer and whether the film fixation producer's identity is known.",
    "By default, the film fixation producer's identity is considered known. Check the box if the film fixation producer unknown.")
BROADCAST_ORG_IDENTITY_HELP = ("Add information about the country of origin of at least one broadcasting organization and whether the broadcasting organization's identity is known.",
    "By default, the broadcasting organisation's identity is considered known. Check the box if the identity is unknown.")


SECTION_CREATION_PUBLICATION_TITLE = "Creation and Publication Description"
SECTION_CREATION_PUBLICATION_DESCRIPTION = "Information about whether the work was published or otherwise made available to the public, as well as when it was created, may be necessary to determine if the work has passed into the public domain."

SECTION_PUBLICATION_DATES_TITLE = "Publication Dates Description"
SECTION_PUBLICATION_DATES_DESCRIPTION = "Note the difference between publication (that implies a material copy) and other forms of making the work publically available (e.g., making available on the Internet)."

SECTION_RIGHTS_INFO_TITLE = "Rights Information Description"
SECTION_RIGHTS_INFO_DESCRIPTION = (
    "The information gathered here can not only help establish the status of the object when it is a work under copyright law, "
    "but also determine whether it can be used even when it is not in the public domain."
)

SECTION_DIGITAL_REPR_TITLE = "Digital Representation Description"
SECTION_DIGITAL_REPR_DESCRIPTION = "We assume that none of the digital representations that are practically usable and have ever been covered by any IP rights have passed into the public domain."

SECTION_IP_RIGHTS_COVERAGE_TITLE = "IP Rights Coverage Description"
SECTION_IP_RIGHTS_COVERAGE_DESCRIPTION = "It is important to distinguish between the digitised object itself (e.g. a painting or a sculpture) and its digital representation (e.g. a photograph of the painting, a photo of the sculpture, or a video recording of an interview). "

SECTION_PERFORMANCE_TITLE = "Performance Rights Description"
SECTION_PERFORMANCE_DESCRIPTION = (
    "The questions below aim to determine whether the performance has passed into the public domain. "
    "Note that this section is independent from the copyright section above and the digital representation section below."
)

SECTION_PHONOGRAM_TITLE = "Phonogram Rights Description"
SECTION_PHONOGRAM_DESCRIPTION = (
    "The questions below aim to determine whether the recording has passed into the public domain. "
    "Note that this section is independent from the copyright section above, "
    "the performance section above, and the digital representation section below."
)

SECTION_FILM_FIXATION_TITLE = "Film Fixation Rights Description"
SECTION_FILM_FIXATION_DESCRIPTION = (
    "The questions below aim to determine whether the film fixation has passed into the public domain. "
    "Note that this section is independent from the copyright section above, "
    "the performance section above, the phonogram section above, and the digital representation section below."
)

SECTION_BROADCAST_TITLE = "Broadcasting Organisation Rights Description"
SECTION_BROADCAST_DESCRIPTION = (
    "The questions below aim to determine whether the broadcast has passed into the public domain. "
    "Note that this section is independent from the copyright section above, "
    "the performance section above, the phonogram section above, the film fixation section above, and the digital representation section below."
)

SECTION_OBJECT_RESTRICTIONS_TITLE = (
    "Object Restrictions and Legal Consultation Description"
)
SECTION_OBJECT_RESTRICTIONS_DESCRIPTION = "This section addresses contractual, administrative, and other restrictions arising from the sensitive nature of the object that may limit its use, and provides information on its legal consultation status."

OBJECT_DESIGN_DESCRIPTION = (
    "A design protects the appearance of a product, including its shape, patterns, lines, contours or colours. "
    "Designs may be registered in single EU countries or for the whole European Union through the European Union Intellectual Property Office (EUIPO)."
)

# Nested Form Fields - IPRightsForm
IP_RIGHTS_COPYRIGHT_LABEL = "Copyright"
IP_RIGHTS_AUDIO_RECORDINGS_LABEL = "Rights to audio recordings (phonograms)"
IP_RIGHTS_FILM_FIXATION_LABEL = "Film fixation rights"
IP_RIGHTS_OTHER_LABEL = "Other IP rights"

# List of IP rights types that need to be evaluated
# Used to generate form fields and process rights systematically
IP_RIGHTS_TYPES = [
    "copyright",
    "audio_recording_rights",
    "film_fixation_rights",
    "other_ip_rights",
]

# Standard choices for IP rights questions
# Default is set to 'no' by being first in the list
IP_RIGHTS_CHOICES = [("no", "No"), ("yes", "Yes"), ("uncertain", "Uncertain")]

IP_RIGHTS_CHOICES_DESCRIPTION = {
    "Copyright": "Consider if the digital representation is protected by copyright (it was made by a human and is original, i.e. it is its author's own intellectual creation). For example, a photograph of a sculpture may be original, but it is highly unlikely that a simple 2D scan of a manuscript is original. Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.",
    "Rights to audio recordings (phonograms)": "Consider if the digital representation is protected by rights to audio recordings or phonograms (fixation of the sounds of a performance or of other sounds, or of a representation of sounds, other than in the form of a fixation incorporated in a cinematographic or other audiovisual work). For example, a first recording of a performance of a traditional song would be a phonogram, even if the song itself is in the public domain. Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.",
    "Film fixation rights": "Consider if the digital representation is protected by rights to film fixations or videograms (film fixation is a recording a series of images that create the impression of movement, regardless of whether they are accompanied by sound). For example, a first recording of an interview would be a film fixation. Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.",
    "Other IP rights": "Consider if the digital representation is protected by any other IP rights. For example, some countries provide protection for non-original photographs (i.e photographs not covered by copyright). Note that this question pertains only to the digital representaion. An object can be protected while the representation is not, or vice versa.",
}