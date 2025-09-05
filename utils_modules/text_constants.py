from enum import Enum
from typing import Dict


class CopyrightCondition(str, Enum):
    """Enum mirroring existing condition string literals (subset for now).
    Use .value to emit the exact same strings in results.
    """
    # Public domain / general notices (subset; extend as needed)
    PublicDomainNotAWork = 'PublicDomainNotAWork'
    PublicDomainRuleOfThumb = 'PublicDomainRuleOfThumb'

    # Article 1 Section 1-2 and variants
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2 = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2'
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2RuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm'
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3 = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3'
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec6 = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6'

    # Article 1 Section 3 and variants
    CopyrightPublicDomainRightsLapsedArticle1Sec3 = 'CopyrightPublicDomainRightsLapsedArticle1Sec3'
    CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm'

    # Article 1 Section 6 and variants
    CopyrightPublicDomainRightsLapsedArticle1Sec6 = 'CopyrightPublicDomainRightsLapsedArticle1Sec6'
    CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm'
    CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication = 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication'
    CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm'

    # Article 1 Section 4 Legal Person
    CopyrightPublicDomainArticle1Section4LegalPerson = 'CopyrightPublicDomainArticle1Section4LegalPerson'

    # Other notices used in this module (subset)
    AuthorAlive = 'AuthorAlive'
    CurrentRightHolderKnown = 'CurrentRightHolderKnown'
    ObjectOnlineAvailable = 'ObjectOnlineAvailable'
    ObjectAvailableCCLicense = 'ObjectAvailableCCLicense'
    FirstEditionProtection = 'FirstEditionProtection'
    DerivativeWork = 'DerivativeWork'
    CompoundWork = 'CompoundWork'
    Photography = 'Photography'
    TerritoryStatusChanged = 'TerritoryStatusChanged'
    UncertainIfWork = 'UncertainIfWork'
    # (do not duplicate above entries)


class PerformanceCondition(str, Enum):
    """Enum mirroring existing performance condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Informational conditions
    CompoundPerformance = 'CompoundPerformance'
    
    # Public domain conditions
    PublicDomainNotAPerformance = 'PublicDomainNotAPerformance'
    PublicDomainRuleOfThumbPerformance = 'PublicDomainRuleOfThumbPerformance'
    
    # Uncertainty conditions
    PerformanceYearUnknown = 'PerformanceYearUnknown'
    PerformanceUnknownPublicationExceptions = 'PerformanceUnknownPublicationExceptions'
    
    # Article 3 Section 1 conditions
    PerformanceProtectionLapsedArticle3S1 = 'PerformanceProtectionLapsedArticle3S1'
    PerformanceStillProtectedArticle3S1 = 'PerformanceStillProtectedArticle3S1'
    
    # Article 3 Publication conditions
    PerformanceProtectionLapsedArticle3Publication = 'PerformanceProtectionLapsedArticle3Publication'
    PerformanceStillProtectedArticle3Publication = 'PerformanceStillProtectedArticle3Publication'
    
    # Non-EEA conditions
    PerformanceNonEEAUncertain = 'PerformanceNonEEAUncertain'
    PerformanceLapsedEvenIfEEA = 'PerformanceLapsedEvenIfEEA'
    
    # Rights conditions
    PerformanceCurrentRightHolderKnown = 'PerformanceCurrentRightHolderKnown'
    PerformanceAvailableCCLicense = 'PerformanceAvailableCCLicense'
    PerformanceOnlineAvailable = 'PerformanceOnlineAvailable'


# Centralized explanation dictionaries (moved verbatim from copyright.py)

COPYRIGHT_CC_LICENSE_EXPLANATIONS: Dict[str, str] = {
    'cc0': 'While the work is protected by copyright, it is available under CC0, which allows unrestricted use.',
    'cc_by': 'While the work is protected by copyright, it is available under CC-BY, which allows use with attribution.',
    'cc_by_sa': 'While the work is protected by copyright, it is available under CC-BY-SA. Additional verification may be needed due to the ShareAlike requirement.',
    'cc_by_nc_sa': 'While the work is protected by copyright, it is available under CC-BY-NC-SA. Additional verification may be needed due to the ShareAlike requirement.',
    'cc_by_nd': 'While the work is protected by copyright, it is available under CC-BY-ND. Additional verification may be needed due to the Non-Derivative requirement.',
    'cc_by_nc_nd': 'While the work is protected by copyright, it is available under CC-BY-NC-ND. Additional verification may be needed due to the Non-Derivative requirement.',
    'other_open': 'While the work is protected by copyright, it is available under an open content license. Additional verification of the license terms is needed.'
}


COPYRIGHT_RIGHTS_EXPLANATIONS: Dict[str, str] = {
    'rights_assignment': 'While the work is protected by copyright, you have acquired the necessary rights through assignment to make it available online.',
    'license_agreement': 'While the work is protected by copyright, you have acquired the necessary rights through license to make it available online.',
    'employee_rights': 'While the work is protected by copyright, you have acquired the necessary rights as an employer to make it available online.',
    'orphan_works': 'While the work is protected by copyright, you can make it available online based on orphan works provisions, but additional verification may be needed.',
    'out_of_commerce': 'While the work is protected by copyright, you can make it available online based on out-of-commerce works provisions, but additional verification may be needed.',
    'quote_right': 'While the work is protected by copyright, you can make it available online based on the right to quote, but additional verification may be needed.',
    'other_law': 'While the work is protected by copyright, you can make it available online based on other legal provisions, but additional verification may be needed.'
}


# Placeholder for future centralization of per-condition, per-color explanation texts
COPYRIGHT_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Informational conditions (info)
    CopyrightCondition.DerivativeWork.value: {
        # same explanation used for both definite and uncertain branches
        'info': 'This is a derivative work. This means that you also need to verify the status of the original work.',
        'info_uncertain': 'This may be a derivative work. This means that you also need to verify the status of the original work.'
    },
    # For the uncertain case we keep the literal fallback; centralization optional
    CopyrightCondition.CompoundWork.value: {
        'info': 'This is a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.',
        'info_uncertain': 'This may be a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.'
    },
    CopyrightCondition.Photography.value: {
        'info': '''Some countries protect photographies that are not original (i.e. not protected by copyright), and the scope of protection may be equivalent to copyright. 
            Aside from that, regulations in some countries used to grant copyright protection to photographies on condition that a copyright notice is made on a copy. This practice differed between countries, so we proceed on the assumption that it does not affect our assesment.'''
    },
    CopyrightCondition.TerritoryStatusChanged.value: {
        'info': 'Problems with international succession were encountered.'
    },

    # Simple green overrides
    CopyrightCondition.PublicDomainNotAWork.value: {
        'green': 'The object is not protected by copyright because it is not a work.'
    },
    CopyrightCondition.PublicDomainRuleOfThumb.value: {
        'green': 'The object is not protected by copyright because it was created before 1850.',
        'green_uncertain_work': 'Even though it is uncertain whether this object qualifies as a work, it was created before 1850 and is therefore in the public domain.'
    },
    # Uncertainty and early exit conditions
    CopyrightCondition.UncertainIfWork.value: {
        'yellow': 'It is uncertain whether this object qualifies as a work protected by copyright.'
    },
    CopyrightCondition.AuthorAlive.value: {
        'yellow': 'It is uncertain if the author is alive so it is impossible to verify if enough time passed since the author\'s death.',
        'red': 'Object under copyright. At least one identified (i.e. non-anonymous/pseudonymous) author or co-author is still alive.'
    },
    CopyrightCondition.CopyrightPublicDomainArticle1Section4LegalPerson.value: {
        'yellow_legal_person': 'The author was not the first rightholder, e.g. the rights belonged to a publisher from the moment the work was created. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.',
        'yellow_uncertain_rightholder': 'It is uncertain who the first rightholder was. EU member states regulate this issue in different ways and depending on the country, the work may or may not be in the public domain.'
    },
    CopyrightCondition.CurrentRightHolderKnown.value: {
        'rights_green': 'Even if the object is protected by copyright, you are the rightholder.'
    },
    # Keys mirror condition string values; inner keys are 'green'|'yellow'|'red'.
    # Fill progressively. Any missing entry will be safely handled by call-site fallbacks.

    # Article 1 Section 1-2
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'Unable to determine if copyright has lapsed because the author\'s death year is unknown.',
        'red': 'The object is still under copyright because fewer than 70 years passed since the author\'s death.',
    },

    # Article 1 Section 1-2 Rule of Shorter Term
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2RuleOfShorterTerm.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.',
    },

    # Article 1 Section 3
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'Unable to determine if copyright has lapsed because the year when the work was first made available is unknown.',
        'red': 'The object is still under copyright because fewer than 70 years passed since it was first made available.',
    },

    # Article 1 Section 3 Rule of Shorter Term
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.',
    },

    # Article 1 Section 6
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'Unable to determine if copyright has lapsed because the creation year is unknown.',
        'red': 'The object is still under copyright because fewer than 70 years passed since its creation.',
    },

    # Article 1 Section 6 Rule of Shorter Term
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.',
    },

    # Article 1 Section 6 Late Publication (EEA)
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed. The work was not made available within 70 years of creation, so it entered public domain 70 years after creation.',
        'yellow': 'Unable to determine if copyright has lapsed because the creation year is unknown. The work was published in {first_publication_year}, which may have been more than 70 years after the creation of the work.',
    },

    # Article 1 Section 6 Late Publication (non-EEA, Rule of Shorter Term)
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed. The work was not made available within 70 years of creation, so it entered public domain 70 years after creation.',
        'yellow': 'According to the EU rules, the work would not be in the public domain. But the country of origin of the work is outside of the European Economic Area. It is possible that in this country, the term of copyright protection is shorter than in the EU, but this tool does not implement all the world\'s copyright systems.',
    },

    # Combined sections
    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'Unable to determine if copyright has lapsed because either the author\'s death year or the first availability year is unknown.',
        'red': 'The object is still under copyright because fewer than 70 years passed since either the author\'s death or first availability.',
    },

    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec6.value: {
        'green': 'The object used to be protected by copyright, but it has lapsed.',
        'yellow': 'Unable to determine if copyright has lapsed because either the author\'s death year or creation year is unknown.',
        'red': 'The object is still under copyright because fewer than 70 years passed since either the author\'s death or creation.',
    },
    CopyrightCondition.FirstEditionProtection.value: {
        'yellow': 'First edition protection applies for 25 years from first publication or making available ({first_edition_year}). The work is in public domain ({public_domain_reason}), but the first edition may be protected until {protection_until_year}.'
    },
}


def get_copyright_explanation(condition: str, color: str, **fmt: object) -> str:
    """Return centralized explanation text for a given condition and color.
    Falls back to empty string if not found; supports optional formatting.
    """
    template = COPYRIGHT_CONDITION_TEXTS_BY_COLOR.get(condition, {}).get(color)
    if template is None:
        return ''
    try:
        return template.format(**fmt)
    except Exception:
        return template


# Performance rights explanation dictionaries
PERFORMANCE_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Informational conditions
    PerformanceCondition.CompoundPerformance.value: {
        'info': 'This is a compound performance. You need to verify the status of each performance separately.'
    },
    
    # Public domain conditions
    PerformanceCondition.PublicDomainNotAPerformance.value: {
        'green': 'The object does not include a performance.'
    },
    PerformanceCondition.PublicDomainRuleOfThumbPerformance.value: {
        'green': 'The performance was made before 1900.'
    },
    
    # Uncertainty conditions
    PerformanceCondition.PerformanceYearUnknown.value: {
        'yellow': 'It is impossible to determine if a performance is still protected.'
    },
    PerformanceCondition.PerformanceUnknownPublicationExceptions.value: {
        'yellow': 'It is impossible to determine if the performance is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.'
    },
    
    # Article 3 Section 1 conditions
    PerformanceCondition.PerformanceProtectionLapsedArticle3S1.value: {
        'green': 'The performance was protected but the protection has lapsed.'
    },
    PerformanceCondition.PerformanceStillProtectedArticle3S1.value: {
        'red': 'The performance is still under protection.'
    },
    
    # Article 3 Publication conditions
    PerformanceCondition.PerformanceProtectionLapsedArticle3Publication.value: {
        'green': 'The performance was protected but the protection has lapsed.'
    },
    PerformanceCondition.PerformanceStillProtectedArticle3Publication.value: {
        'red': 'The performance is still under protection.'
    },
    
    # Non-EEA conditions
    PerformanceCondition.PerformanceNonEEAUncertain.value: {
        'yellow': 'Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.',
        'yellow_uncertain': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the performance would not have lapsed even under EEA rules, the status is uncertain.'
    },
    PerformanceCondition.PerformanceLapsedEvenIfEEA.value: {
        'green': 'Country of origin appears to be outside the EEA, but the performance would have lost protection even if the country of origin were in the EEA.'
    },
    
    # Rights conditions
    PerformanceCondition.PerformanceCurrentRightHolderKnown.value: {
        'rights_green': 'The performance is protected by performance rights, but you are the rightholder.'
    },
    PerformanceCondition.PerformanceAvailableCCLicense.value: {
        'rights_green': 'While the performance is protected, it is available under an open content license (e.g., CC0 or CC‑BY).',
        'rights_yellow': 'While the performance is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
    },
    PerformanceCondition.PerformanceOnlineAvailable.value: {
        'rights_green': 'While the performance is protected, you have acquired the necessary rights to make it available online.',
        'rights_yellow': 'While the performance is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
    }
}


def get_performance_explanation(condition: str, color: str, **fmt: object) -> str:
    """Return centralized explanation text for a given performance condition and color.
    Falls back to empty string if not found; supports optional formatting.
    """
    template = PERFORMANCE_CONDITION_TEXTS_BY_COLOR.get(condition, {}).get(color)
    if template is None:
        return ''
    try:
        return template.format(**fmt)
    except Exception:
        return template


COPYRIGHT_TERM = 70
FIRST_EDITION_TERM = 25