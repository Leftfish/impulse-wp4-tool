from datetime import datetime
from data.country_codes import is_eea_country, is_eu_country

CURRENT_YEAR = datetime.now().year

def calculate_intermediate_values(data):
    """Calculate intermediate boolean values used in copyright calculations."""
    current_year = datetime.now().year
    
    # Author-related calculations
    all_authors_known = all(author.get('identity_known', False) for author in data.get('authors', []))
    all_authors_anonymous = all(not author.get('identity_known', True) for author in data.get('authors', []))
    
    # Country calculations
    country_codes = [author.get('country_of_origin') for author in data.get('authors', [])]
    country_of_origin_eea = any(is_eea_country(code) for code in country_codes if code)
    country_of_origin_unknown = any(code == 'XX' for code in country_codes)
    
    # Time-based calculations
    more_than_70_years_since_death = False
    if data.get('author_death_year'):
        more_than_70_years_since_death = (current_year - data['author_death_year']) > 70
    
    more_than_70_years_since_first_available = False
    first_available_year = min(
        filter(None, [
            data.get('first_publication_year'),
            data.get('first_available_year')
        ]),
        default=None
    )
    if first_available_year:
        more_than_70_years_since_first_available = (current_year - first_available_year) > 70
    
    more_than_70_years_since_creation = False
    if data.get('creation_year'):
        more_than_70_years_since_creation = (current_year - data['creation_year']) > 70
    
    # Publication status
    never_made_publicly_available = (
        data.get('physically_published') == 'not_published_on_physical_medium' and
        data.get('otherwise_available') == 'not_made_available_no_medium'
    )
    
    # Posthumous edition calculations
    posthumous_edition_publication_after_public_domain = False
    if data.get('first_publication_year') and data.get('author_death_year'):
        years_after_death = data['first_publication_year'] - data['author_death_year']
        posthumous_edition_publication_after_public_domain = years_after_death > 70
    
    return {
        'AllAuthorsKnown': all_authors_known,
        'AllAuthorsAnonymousOrPseudonymous': all_authors_anonymous,
        'CountryOfOriginEEAAnyReason': country_of_origin_eea,
        'CountryOfOriginUnknown': country_of_origin_unknown,
        'MoreThan70YearsSinceDeath': more_than_70_years_since_death,
        'MoreThan70YearsSinceFirstAvailable': more_than_70_years_since_first_available,
        'MoreThan70YearsSinceCreation': more_than_70_years_since_creation,
        'NeverMadePubliclyAvailable': never_made_publicly_available,
        'PosthumousEditionPublicationAfterPublicDomain': posthumous_edition_publication_after_public_domain
    }

def calculate_results(data, intermediate):
    """Calculate final copyright status results based on intermediate values."""
    results = {
        'green': [],
        'yellow': [],
        'red': [],
        'info': [],
        'object_name': data.get('object_name'),
        'institution_name': data.get('institution_name')
    }
    
    # Simple override conditions - these take precedence over everything
    if data.get('is_copyright_work') == 'no':
        results['green'].append({
            'condition': 'PublicDomainNotAWork',
            'explanation': 'The object is not protected by copyright because it is not a work.'
        })
        return results
    
    if data.get('created_before_1850') == 'yes':
        results['green'].append({
            'condition': 'PublicDomainRuleOfThumb',
            'explanation': 'The object is not protected by copyright because it was created before 1850.'
        })
        return results

    # Store all possible results first
    potential_results = {
        'green': [],
        'yellow': [],
        'red': []
    }
    
    # Check uncertain conditions that lead to YELLOW status
    if data.get('author_alive') == 'uncertain':
        potential_results['yellow'].append({
            'condition': 'AuthorAlive',
            'explanation': 'It is uncertain if the author is alive so it is impossible to verify if enough time passed since the author\'s death.'
        })
    
    if data.get('original_rightholder') == 'legal_person':
        potential_results['yellow'].append({
            'condition': 'OriginalRightholder',
            'explanation': 'The author was not the first rightholder, e.g. the rights belonged to a publisher from the moment the work was created. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
        })
    
    if data.get('original_rightholder') == 'uncertain':
        potential_results['yellow'].append({
            'condition': 'OriginalRightholder',
            'explanation': 'It is uncertain who the first rightholder was. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
        })
    
    # Check copyright lapse conditions
    
    # Article 1 Section 1-2 (EEA countries)
    if (intermediate['AllAuthorsKnown'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsKnown'] and intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['red'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2',
            'explanation': 'The object is still under copyright because fewer than 70 years passed since the author\'s death.'
        })
    
    # Article 1 Section 1-2 Rule of Shorter Term (non-EEA countries)
    if (intermediate['AllAuthorsKnown'] and 
        not intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsKnown'] and not intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })
    
    # Article 1 Section 3 (EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsAnonymousOrPseudonymous'] and intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['red'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3',
            'explanation': 'The object is still under copyright because fewer than 70 years passed since it was first made available.'
        })
    
    # Article 1 Section 3 Rule of Shorter Term (non-EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        not intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['AllAuthorsAnonymousOrPseudonymous'] and not intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })
    
    # Article 1 Section 6 (EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['NeverMadePubliclyAvailable'] and 
        intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceCreation']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
          intermediate['NeverMadePubliclyAvailable'] and 
          intermediate['CountryOfOriginEEAAnyReason']):
        potential_results['red'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6',
            'explanation': 'The object is still under copyright because fewer than 70 years passed since its creation.'
        })
    
    # Article 1 Section 6 Rule of Shorter Term (non-EEA countries)
    if (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
        intermediate['NeverMadePubliclyAvailable'] and 
        (not intermediate['CountryOfOriginEEAAnyReason'] or intermediate['CountryOfOriginUnknown']) and 
        intermediate['MoreThan70YearsSinceCreation']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif (intermediate['AllAuthorsAnonymousOrPseudonymous'] and 
          intermediate['NeverMadePubliclyAvailable'] and 
          (not intermediate['CountryOfOriginEEAAnyReason'] or intermediate['CountryOfOriginUnknown'])):
        potential_results['yellow'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm',
            'explanation': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.'
        })

    # Article 1 Section 1-2 Plus Section 3
    if (intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath'] and 
        intermediate['MoreThan70YearsSinceFirstAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['CountryOfOriginEEAAnyReason']:
        potential_results['red'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3',
            'explanation': 'The object is still under copyright because fewer than 70 years passed since either the author\'s death or first availability.'
        })

    # Article 1 Section 1-2 Plus Section 6
    if (intermediate['CountryOfOriginEEAAnyReason'] and 
        intermediate['MoreThan70YearsSinceDeath'] and 
        intermediate['MoreThan70YearsSinceCreation'] and 
        intermediate['NeverMadePubliclyAvailable']):
        potential_results['green'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6',
            'explanation': 'The object used to be protected by copyright, but it has lapsed.'
        })
    elif intermediate['CountryOfOriginEEAAnyReason'] and intermediate['NeverMadePubliclyAvailable']:
        potential_results['red'].append({
            'condition': 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6',
            'explanation': 'The object is still under copyright because fewer than 70 years passed since either the author\'s death or creation.'
        })

    # Check if author is alive - this adds to RED status
    if data.get('author_alive') == 'author_alive':
        potential_results['red'].append({
            'condition': 'AuthorAlive',
            'explanation': 'Object under copyright. At least one co-author is still alive.'
        })
    
    # Apply results based on priority, but handle posthumous edition separately
    if potential_results['green']:
        # If we have any GREEN results, use them
        results['green'].extend(potential_results['green'])
    elif data.get('current_rightholder') == 'rightholder_us':
        # If we're the rights holder and there's no GREEN status, override with GREEN
        results['green'].append({
            'condition': 'CurrentRightHolderKnown',
            'explanation': 'The object is protected by copyright, but you are the rightholder.'
        })
    else:
        # Otherwise, use all potential results
        results['green'].extend(potential_results['green'])
        results['yellow'].extend(potential_results['yellow'])
        results['red'].extend(potential_results['red'])

    # Handle posthumous edition independently
    # This can add YELLOW status even if we have GREEN status
    if (intermediate['PosthumousEditionPublicationAfterPublicDomain'] and
        data.get('first_publication_year') and
        (datetime.now().year - data['first_publication_year']) <= 25):
        
        # Only add posthumous edition status if we're not the rights holder
        # or if we already have GREEN status for other reasons
        if results['green'] or data.get('current_rightholder') != 'rightholder_us':
            results['yellow'].append({
                'condition': 'CopyrightLapsedButPosthumousEditionNotLapsed',
                'explanation': 'Copyright protection of the object lapsed, but the protection of posthumous (first) editions may still apply. Additional verification is needed due to differences between EU member states.'
            })
    
    return results

def generate_markdown_report(results):
    """Generate a markdown report from the results."""
    
    md_content = ["# Copyright Status Evaluation Report\n"]
    
    if results.get('compound_alert'):
        md_content.append("\n⚠️ **Caution, compound work!!!**\n")
    
    if results['green']:
        md_content.append("\n## ✅ Green Status\n")
        for result in results['green']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['yellow']:
        md_content.append("\n## ⚠️ Yellow Status (Requires Attention)\n")
        for result in results['yellow']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['red']:
        md_content.append("\n## ❌ Red Status (Not Free to Use)\n")
        for result in results['red']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    if results['info']:
        md_content.append("\n## 📝 Informational Messages\n")
        for result in results['info']:
            md_content.append(f"- **{result['condition']}**: {result['explanation']}\n")
    
    return "".join(md_content)

def generate_text_report(results):
    """Generate a plain text report from the results."""
    
    content = ["Copyright Status Evaluation Report\n"]
    
    # Add object and institution information if available
    if results.get('object_name'):
        content.append(f"\nObject: {results['object_name']}")
    if results.get('institution_name'):
        content.append(f"\nInstitution: {results['institution_name']}")
    
    if results.get('compound_alert'):
        content.append("\nCAUTION: Compound work!!!\n")
    
    if results['green']:
        content.append("\nGREEN Status\n")
        for result in results['green']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['yellow']:
        content.append("\nYELLOW Status (Requires Attention)\n")
        for result in results['yellow']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['red']:
        content.append("\nRED Status (Not Free to Use)\n")
        for result in results['red']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    if results['info']:
        content.append("\nInformational Messages\n")
        for result in results['info']:
            content.append(f"- {result['condition']}: {result['explanation']}\n")
    
    return "".join(content) 