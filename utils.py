from datetime import datetime
from data.country_codes import is_eea_country, is_eu_country

CURRENT_YEAR = datetime.now().year

def calculate_intermediate_values(data):
    """Calculate all intermediate values based on form data."""
    
    # Extract author information
    authors = data.get('authors', [])
    
    # Calculate author-related values
    all_authors_known = all(author.get('identity_known', False) for author in authors)
    all_authors_pseudonymous = all(not author.get('identity_known', True) for author in authors)
    
    # Calculate country of origin values
    author_countries = [author.get('country_of_origin') for author in authors]
    country_origin_eea_nationality = any(is_eea_country(country) for country in author_countries)
    country_origin_unknown = all(country == 'XX' for country in author_countries)
    
    # Calculate publication-related values
    first_pub_year = data.get('first_publication_year', 0)
    first_available_year = data.get('first_available_year', 0)
    creation_year = data.get('creation_year', 0)
    author_death_year = data.get('author_death_year', 0)
    
    # Calculate EEA-related values
    country_first_pub_eea = is_eea_country(data.get('country_first_publication'))
    simultaneous_countries = data.get('simultaneous_publication_countries', [])
    country_simultaneous_pub_eea = any(is_eea_country(country) for country in simultaneous_countries)
    cinematographic_country_eea = is_eea_country(data.get('cinematographic_country'))
    architecture_country_eea = is_eea_country(data.get('architecture_country'))
    
    # Calculate availability-related values
    never_made_public = (
        data.get('physically_published') == 'not_published_on_physical_medium' and 
        data.get('otherwise_available') == 'not_made_available_no_medium'
    )
    
    # Calculate time-related values
    more_than_70_years_since_death = (
        CURRENT_YEAR - author_death_year > 70 if author_death_year != 0 else False
    )
    more_than_70_years_since_creation = (
        CURRENT_YEAR - creation_year > 70 if creation_year != 0 else False
    )
    
    # Calculate availability years
    min_availability_year = None
    if first_pub_year != 0 and first_available_year != 0:
        min_availability_year = min(first_pub_year, first_available_year)
    elif first_pub_year != 0:
        min_availability_year = first_pub_year
    elif first_available_year != 0:
        min_availability_year = first_available_year
        
    more_than_70_years_since_first_available = (
        CURRENT_YEAR - min_availability_year > 70 if min_availability_year else False
    )
    
    # Calculate country of origin EEA status
    country_origin_eea_publication = (
        country_first_pub_eea or 
        country_simultaneous_pub_eea or 
        cinematographic_country_eea or 
        architecture_country_eea
    )
    
    country_origin_eea_any_reason = (
        country_origin_eea_nationality or country_origin_eea_publication
    )
    
    # Calculate posthumous publication values
    max_availability_year = max(first_pub_year or 0, first_available_year or 0)
    
    posthumous_death_year = (
        max_availability_year > (author_death_year + 70)
        if author_death_year != 0 and max_availability_year != 0
        else False
    )
    
    posthumous_creation_year = (
        max_availability_year > (creation_year + 70)
        if creation_year != 0 and max_availability_year != 0
        else False
    )

    return {
        'AllAuthorsKnown': all_authors_known,
        'AllAuthorsPseudonymousOrAnonymous': all_authors_pseudonymous,
        'CountryOfOriginEEADueToNationality': country_origin_eea_nationality,
        'CountryOfOriginEEADueToPublication': country_origin_eea_publication,
        'CountryOfOriginEEAAnyReason': country_origin_eea_any_reason,
        'CountryOfOriginUnknown': country_origin_unknown,
        'NeverMadePubliclyAvailable': never_made_public,
        'MoreThan70YearsSinceDeath': more_than_70_years_since_death,
        'MoreThan70YearsSinceCreation': more_than_70_years_since_creation,
        'MoreThan70YearsSinceFirstAvailable': more_than_70_years_since_first_available,
        'PosthumousEditionPublicationAfterPublicDomainByDeathYear': posthumous_death_year,
        'PosthumousEditionPublicationAfterPublicDomainByCreationYear': posthumous_creation_year
    }

def calculate_results(data, intermediate_values):
    """Calculate final results based on form data and intermediate values."""
    
    results = {
        'green': [],
        'yellow': [],
        'red': []
    }
    
    # Check for compound work alert
    if data.get('is_compound') in ['compound', 'uncertain']:
        results['compound_alert'] = True
    
    # GREEN results
    if data.get('is_copyright_work') == 'not_work':
        results['green'].append({
            'condition': 'PublicDomainNotAWork',
            'comment': 'The object is not protected by copyright because it is not a work.'
        })
        
    if data.get('created_before_1850') == 'made_before_1850':
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumb',
            'comment': 'The object is not protected by copyright because it was created so early that copyright, if it existed, has lapsed.'
        })
        
    if data.get('current_rightholder') == 'rightholder_us':
        results['green'].append({
            'condition': 'CurrentRightHolderKnown',
            'comment': 'The object is protected by copyright, but you are the rightholder.'
        })
    
    # Calculate copyright lapse conditions
    if (intermediate_values['AllAuthorsKnown'] and 
        intermediate_values['CountryOfOriginEEAAnyReason'] and 
        intermediate_values['MoreThan70YearsSinceDeath']):
        results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2',
            'comment': 'The object used to be protected by copyright, but it has lapsed.'
        })
    
    if (intermediate_values['AllAuthorsKnown'] and 
        not intermediate_values['CountryOfOriginEEAAnyReason'] and 
        intermediate_values['MoreThan70YearsSinceDeath']):
        results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm',
            'comment': 'The object used to be protected by copyright, but it has lapsed.'
        })
    
    # YELLOW results
    if data.get('original_rightholder') == 'legal_person':
        results['yellow'].append({
            'condition': 'OriginalRightholder',
            'comment': 'The author was not the first rightholder, e.g. the rights belonged to a publisher from the moment the work was created. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
        })
    
    if data.get('original_rightholder') == 'uncertain':
        results['yellow'].append({
            'condition': 'OriginalRightholder',
            'comment': 'It is uncertain who the first rightholder was. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
        })
    
    if data.get('author_alive') == 'uncertain':
        results['yellow'].append({
            'condition': 'AuthorAlive',
            'comment': "It is uncertain if the author is alive so it is impossible to verify if enough time passed since the author's death."
        })
    
    # RED results
    if data.get('author_alive') == 'author_alive':
        results['red'].append({
            'condition': 'AuthorAlive',
            'comment': 'Object under copyright. At least one co-author is still alive.'
        })
    
    # Add more conditions as per specifications...
    
    return results

def generate_markdown_report(results):
    """Generate a markdown report from the results."""
    
    md_content = ["# Copyright Status Evaluation Report\n"]
    
    if results.get('compound_alert'):
        md_content.append("\n⚠️ **Caution, compound work!!!**\n")
    
    if results['green']:
        md_content.append("\n## ✅ Green Status\n")
        for result in results['green']:
            md_content.append(f"- **{result['condition']}**: {result['comment']}\n")
    
    if results['yellow']:
        md_content.append("\n## ⚠️ Yellow Status (Requires Attention)\n")
        for result in results['yellow']:
            md_content.append(f"- **{result['condition']}**: {result['comment']}\n")
    
    if results['red']:
        md_content.append("\n## ❌ Red Status (Not Free to Use)\n")
        for result in results['red']:
            md_content.append(f"- **{result['condition']}**: {result['comment']}\n")
    
    return "".join(md_content) 