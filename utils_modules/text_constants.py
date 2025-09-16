from enum import Enum
from typing import Dict


class CopyrightCondition(str, Enum):
    """Enum mirroring existing condition string literals (subset for now).
    Use .value to emit the exact same strings in results.
    """
    # Public domain / general notices (subset; extend as needed)
    PublicDomainNotAWork = 'CopyrightPublicDomainNotAWork'
    PublicDomainRuleOfThumb = 'CopyrightPublicDomainRuleOfThumb'

    # Article 1 Section 1-2 and variants
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2 = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2'
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2RuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm'
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3 = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3'
    CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec6 = 'CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6'

    # Article 1 Section 3 and variants
    CopyrightPublicDomainRightsLapsedArticle1Sec3 = 'CopyrightPublicDomainRightsLapsedArticle1Sec3'
    CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm'

    # Article 1 Section 4
    CopyrightPublicDomainArticle1Section4LegalPerson = 'CopyrightPublicDomainArticle1Section4LegalPerson'
    
    # Article 1 Section 6 and variants
    CopyrightPublicDomainRightsLapsedArticle1Sec6 = 'CopyrightPublicDomainRightsLapsedArticle1Sec6'
    CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm'
    CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication = 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication'
    CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm = 'CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm'


    # Other notices used in this module (subset)
    CopyrightAuthorAlive = 'CopyrightAuthorAlive'
    CurrentRightHolderKnown = 'CurrentRightHolderKnown'
    CopyrightObjectOnlineAvailable = 'CopyrightObjectOnlineAvailable'
    CopyrightObjectAvailableCCLicense = 'CopyrightObjectAvailableCCLicense'
    FirstEditionProtection = 'FirstEditionProtection'
    CopyrightDerivativeWork = 'CopyrightDerivativeWork'
    CopyrightCompoundWork = 'CopyrightCompoundWork'
    Photography = 'Photography'
    CopyrightTerritoryStatusChanged = 'CopyrightTerritoryStatusChanged'
    CopyrightUncertainIfWork = 'CopyrightUncertainIfWork'
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


class FilmFixationCondition(str, Enum):
    """Enum mirroring existing film fixation condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Informational conditions
    CompoundFilmFixation = 'CompoundFilmFixation'
    
    # Public domain conditions
    PublicDomainNotAFilmFixation = 'PublicDomainNotAFilmFixation'
    PublicDomainRuleOfThumbFilmFixation = 'PublicDomainRuleOfThumbFilmFixation'
    
    # Uncertainty conditions
    FilmFixationYearUnknown = 'FilmFixationYearUnknown'
    FilmFixationUnknownPublicationExceptions = 'FilmFixationUnknownPublicationExceptions'
    
    # Article 3 Section 4 conditions
    FilmFixationProtectionLapsedArticle3S4S1 = 'FilmFixationProtectionLapsedArticle3S4S1'
    FilmFixationStillProtectedArticle3S4S1 = 'FilmFixationStillProtectedArticle3S4S1'
    FilmFixationProtectionLapsedArticle3S4S2 = 'FilmFixationProtectionLapsedArticle3S4S2'
    FilmFixationStillProtectedArticle3S4S2 = 'FilmFixationStillProtectedArticle3S4S2'
    
    # Non-EEA conditions
    FilmFixationNonEEAUncertain = 'FilmFixationNonEEAUncertain'
    FilmFixationLapsedEvenIfEEA = 'FilmFixationLapsedEvenIfEEA'
    
    # Rights conditions
    FilmFixationCurrentRightHolderKnown = 'FilmFixationCurrentRightHolderKnown'
    FilmFixationAvailableCCLicense = 'FilmFixationAvailableCCLicense'
    FilmFixationOnlineAvailable = 'FilmFixationOnlineAvailable'


class PhonogramCondition(str, Enum):
    """Enum mirroring existing phonogram condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Informational conditions
    CompoundPhonogram = 'CompoundPhonogram'

    # Public domain conditions
    PublicDomainNotAPhonogram = 'PublicDomainNotAPhonogram'
    PublicDomainRuleOfThumbPhonogram = 'PublicDomainRuleOfThumbPhonogram'

    # Uncertainty conditions
    PhonogramYearUnknown = 'PhonogramYearUnknown'
    PhonogramUnknownPublicationExceptions = 'PhonogramUnknownPublicationExceptions'

    # Article 3 Section 1 conditions
    PhonogramProtectionLapsedArticle3S1 = 'PhonogramProtectionLapsedArticle3S1'
    PhonogramStillProtectedArticle3S1 = 'PhonogramStillProtectedArticle3S1'

    # Article 3 Publication conditions
    PhonogramProtectionLapsedArticle3Publication = 'PhonogramProtectionLapsedArticle3Publication'
    PhonogramStillProtectedArticle3Publication = 'PhonogramStillProtectedArticle3Publication'

    # Non-EEA conditions
    PhonogramNonEEAUncertain = 'PhonogramNonEEAUncertain'
    PhonogramLapsedEvenIfEEA = 'PhonogramLapsedEvenIfEEA'

    # Rights conditions
    PhonogramCurrentRightHolderKnown = 'PhonogramCurrentRightHolderKnown'
    PhonogramAvailableCCLicense = 'PhonogramAvailableCCLicense'
    PhonogramOnlineAvailable = 'PhonogramOnlineAvailable'


class BroadcastingCondition(str, Enum):
    """Enum mirroring existing broadcasting condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Informational conditions
    CompoundBroadcast = 'CompoundBroadcast'

    # Public domain conditions
    PublicDomainNotABroadcast = 'PublicDomainNotABroadcast'
    PublicDomainRuleOfThumbBroadcasts = 'PublicDomainRuleOfThumbBroadcasts'

    # Uncertainty conditions
    BroadcastYearUnknown = 'BroadcastYearUnknown'

    # Article-based conditions (EEA focus)
    BroadcastProtectionLapsedArticle3 = 'BroadcastProtectionLapsedArticle3'
    BroadcastStillProtectedArticle3 = 'BroadcastStillProtectedArticle3'

    # Non-EEA conditions
    BroadcastNonEEAUncertain = 'BroadcastNonEEAUncertain'
    BroadcastLapsedEvenIfEEA = 'BroadcastLapsedEvenIfEEA'

    # Rights conditions
    BroadcastCurrentRightHolderKnown = 'BroadcastCurrentRightHolderKnown'
    BroadcastAvailableCCLicense = 'BroadcastAvailableCCLicense'
    BroadcastOnlineAvailable = 'BroadcastOnlineAvailable'


class DigitalRepresentationCondition(str, Enum):
    """Enum mirroring existing digital representation condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Status conditions
    DigitalRepresentationCopyrightStatus = 'DigitalRepresentationCopyrightStatus'
    DigitalRepresentationPhonogramStatus = 'DigitalRepresentationPhonogramStatus'
    DigitalRepresentationFilmFixationStatus = 'DigitalRepresentationFilmFixationStatus'
    DigitalRepresentationPerformanceStatus = 'DigitalRepresentationPerformanceStatus'
    DigitalRepresentationOtherIPStatus = 'DigitalRepresentationOtherIPStatus'
    
    # Additional conditions (for yellow upgrades)
    DigitalRepresentationAdditionalCopyrightStatus = 'DigitalRepresentationAdditionalCopyrightStatus'
    DigitalRepresentationAdditionalPhonogramStatus = 'DigitalRepresentationAdditionalPhonogramStatus'
    DigitalRepresentationAdditionalFilmFixationStatus = 'DigitalRepresentationAdditionalFilmFixationStatus'
    DigitalRepresentationAdditionalPerformanceStatus = 'DigitalRepresentationAdditionalPerformanceStatus'
    DigitalRepresentationAdditionalOtherIPStatus = 'DigitalRepresentationAdditionalOtherIPStatus'


class OtherLegalIssuesCondition(str, Enum):
    """Enum mirroring existing other legal issues condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Warning conditions (yellow)
    HasContractualRestrictions = 'HasContractualRestrictions'
    HasAdministrativeRestrictions = 'HasAdministrativeRestrictions'
    HasOwnershipIssues = 'HasOwnershipIssues'
    ProvenanceNotTraced = 'ProvenanceNotTraced'
    HasProvenanceIssues = 'HasProvenanceIssues'
    ContainsLivingIdentifiableInfo = 'ContainsLivingIdentifiableInfo'
    ContainsSensitiveHistoricalInfo = 'ContainsSensitiveHistoricalInfo'
    ContainsTotalitarianAssociations = 'ContainsTotalitarianAssociations'
    ContainsDiscriminatoryContent = 'ContainsDiscriminatoryContent'
    ContainsOtherSensitiveContent = 'ContainsOtherSensitiveContent'
    HasOtherProblems = 'HasOtherProblems'
    
    # Success condition (green)
    NoLegalIssues = 'NoLegalIssues'


class AdditionalClassificationCondition(str, Enum):
    """Enum mirroring existing additional classification condition string literals.
    Use .value to emit the exact same strings in results.
    """
    # Warning conditions (yellow)
    PublicationNotAWork = 'PublicationNotAWork'
    CriticalEdition = 'CriticalEdition'
    Trademark = 'Trademark'
    Design = 'Design'
    
    # Success conditions (green)
    NotPressPublication = 'NotPressPublication'
    PressPublicationLapsed = 'PressPublicationLapsed'
    NoOtherIPRights = 'NoOtherIPRights'
    
    # Restriction conditions (red)
    PressPublicationProtected = 'PressPublicationProtected'

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

COPYRIGHT_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Informational conditions (info)
    CopyrightCondition.CopyrightDerivativeWork.value: {
        # same explanation used for both definite and uncertain branches
        'info': 'This is a derivative work. This means that you also need to verify the status of the original work.',
        'info_uncertain': 'This may be a derivative work. This means that you also need to verify the status of the original work.'
    },
    # For the uncertain case we keep the literal fallback; centralization optional
    CopyrightCondition.CopyrightCompoundWork.value: {
        'info': 'This is a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.',
        'info_uncertain': 'This may be a compound work. It means that you also have to verify - separately! - the status of all the particular work that make it up, for example each illustration in a magazine.'
    },
    CopyrightCondition.Photography.value: {
        'info': '''Some countries protect photographies that are not original (i.e. not protected by copyright), and the scope of protection may be equivalent to copyright. 
            Aside from that, regulations in some countries used to grant copyright protection to photographies on condition that a copyright notice is made on a copy. This practice differed between countries, so we proceed on the assumption that it does not affect our assesment.'''
    },
    CopyrightCondition.CopyrightTerritoryStatusChanged.value: {
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
    CopyrightCondition.CopyrightUncertainIfWork.value: {
        'yellow': 'It is uncertain whether this object qualifies as a work protected by copyright.'
    },
    CopyrightCondition.CopyrightAuthorAlive.value: {
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
        'yellow': 'First edition protection applies for 25 years from first publication or making available ({first_edition_year}). The work is in public domain ({public_domain_reason}), but the first edition may still be protected.'
    },
}


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




# Film fixation rights explanation dictionaries
FILM_FIXATION_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Informational conditions
    FilmFixationCondition.CompoundFilmFixation.value: {
        'info': 'This film fixation is, in fact, a collection of multiple film fixations or it is made from various film fixations. The analysis must be performed for each separately.'
    },
    
    # Public domain conditions
    FilmFixationCondition.PublicDomainNotAFilmFixation.value: {
        'green': 'It is not protected as a film fixation.'
    },
    FilmFixationCondition.PublicDomainRuleOfThumbFilmFixation.value: {
        'green': 'Given the time the film fixation was made, it has passed to the public domain.'
    },
    
    # Uncertainty conditions
    FilmFixationCondition.FilmFixationYearUnknown.value: {
        'yellow': 'It is impossible to determine if a film fixation is still protected.'
    },
    FilmFixationCondition.FilmFixationUnknownPublicationExceptions.value: {
        'yellow': 'It is impossible to determine if the film fixation is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.'
    },
    
    # Article 3 Section 4 conditions
    FilmFixationCondition.FilmFixationProtectionLapsedArticle3S4S1.value: {
        'green': 'The film fixation was protected but the protection has lapsed.'
    },
    FilmFixationCondition.FilmFixationStillProtectedArticle3S4S1.value: {
        'red': 'The film fixation is still under protection.'
    },
    FilmFixationCondition.FilmFixationProtectionLapsedArticle3S4S2.value: {
        'green': 'The film fixation was protected but the protection has lapsed.'
    },
    FilmFixationCondition.FilmFixationStillProtectedArticle3S4S2.value: {
        'red': 'The film fixation is still under protection.'
    },
    
    # Non-EEA conditions
    FilmFixationCondition.FilmFixationNonEEAUncertain.value: {
        'yellow': 'Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.',
        'yellow_uncertain': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the film fixation would not have lapsed even under EEA rules, the status is uncertain.'
    },
    FilmFixationCondition.FilmFixationLapsedEvenIfEEA.value: {
        'green': 'Country of origin appears to be outside the EEA, but the film fixation would have lost protection even if the country of origin were in the EEA.'
    },
    
    # Rights conditions
    FilmFixationCondition.FilmFixationCurrentRightHolderKnown.value: {
        'rights_green': 'Even if the film fixation is protected by film fixation rights, you are the rightholder.'
    },
    FilmFixationCondition.FilmFixationAvailableCCLicense.value: {
        'rights_green': 'Even if the film fixation is protected, it is available under an open content license (e.g., CC0 or CC‑BY).',
        'rights_yellow': 'Even if the film fixation is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
    },
    FilmFixationCondition.FilmFixationOnlineAvailable.value: {
        'rights_green': 'Even if the film fixation is protected, you have acquired the necessary rights to make it available online.',
        'rights_yellow': 'Even if the film fixation is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
    }
}




# Phonogram rights explanation dictionaries
PHONOGRAM_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Informational conditions
    PhonogramCondition.CompoundPhonogram.value: {
        'info': 'This recording is, in fact, a collection of multiple recording or it is made from various recording. The analysis must be performed for each separately.'
    },

    # Public domain conditions
    PhonogramCondition.PublicDomainNotAPhonogram.value: {
        'green': 'It is not protected as a phonogram.'
    },
    PhonogramCondition.PublicDomainRuleOfThumbPhonogram.value: {
        'green': 'Given the time the recording was made, it has passed to the public domain.'
    },

    # Uncertainty conditions
    PhonogramCondition.PhonogramYearUnknown.value: {
        'yellow': 'It is impossible to determine if a recording is still protected.'
    },
    PhonogramCondition.PhonogramUnknownPublicationExceptions.value: {
        'yellow': 'It is impossible to determine if the recording is still protected, because the protection may be calculated according to the date of an unknown or unspecified event.'
    },

    # Article 3 Section 1 conditions
    PhonogramCondition.PhonogramProtectionLapsedArticle3S1.value: {
        'green': 'The recording was protected but the protection has lapsed.'
    },
    PhonogramCondition.PhonogramStillProtectedArticle3S1.value: {
        'red': 'The recording is still under protection.'
    },

    # Article 3 Publication conditions
    PhonogramCondition.PhonogramProtectionLapsedArticle3Publication.value: {
        'green': 'The recording was protected but the protection has lapsed.'
    },
    PhonogramCondition.PhonogramStillProtectedArticle3Publication.value: {
        'red': 'The recording is still under protection.'
    },

    # Non-EEA conditions
    PhonogramCondition.PhonogramNonEEAUncertain.value: {
        'yellow': 'Country of origin appears to be outside the EEA. The status depends on an unknown or unspecified event date, so it is uncertain.',
        'yellow_uncertain': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the recording would not have lapsed even under EEA rules, the status is uncertain.'
    },
    PhonogramCondition.PhonogramLapsedEvenIfEEA.value: {
        'green': 'Country of origin appears to be outside the EEA, but the recording would have lost protection even if the country of origin were in the EEA.'
    },

    # Rights conditions
    PhonogramCondition.PhonogramCurrentRightHolderKnown.value: {
        'rights_green': 'The recording is protected by phonogram rights, but you are the rightholder.'
    },
    PhonogramCondition.PhonogramAvailableCCLicense.value: {
        'rights_green': 'While the recording is protected, it is available under an open content license (e.g., CC0 or CC‑BY).',
        'rights_yellow': 'While the recording is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
    },
    PhonogramCondition.PhonogramOnlineAvailable.value: {
        'rights_green': 'While the recording is protected, you have acquired the necessary rights to make it available online.',
        'rights_yellow': 'While the recording is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
    }
}




# Broadcasting rights explanation dictionaries
BROADCAST_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Informational conditions
    BroadcastingCondition.CompoundBroadcast.value: {
        'info': 'This broadcast is, in fact, a collection of multiple broadcasts or it is made from various broadcasts. The analysis must be performed for each separately.'
    },

    # Public domain conditions
    BroadcastingCondition.PublicDomainNotABroadcast.value: {
        'green': 'It is not protected as a broadcast.'
    },
    BroadcastingCondition.PublicDomainRuleOfThumbBroadcasts.value: {
        'green': 'Given the time the broadcast was made, it has passed to the public domain.'
    },

    # Uncertainty conditions
    BroadcastingCondition.BroadcastYearUnknown.value: {
        'yellow': 'It is impossible to determine if a broadcast is still protected, because the year of the broadcast is unknown.'
    },

    # Article-based conditions (EEA focus)
    BroadcastingCondition.BroadcastProtectionLapsedArticle3.value: {
        'green': 'The broadcast was protected but the protection has lapsed.'
    },
    BroadcastingCondition.BroadcastStillProtectedArticle3.value: {
        'red': 'The broadcast is still under protection.'
    },

    # Non-EEA conditions
    BroadcastingCondition.BroadcastNonEEAUncertain.value: {
        'yellow': 'Country of origin appears to be outside the EEA. Non-EEA terms are not implemented; since the broadcast would not have lapsed even under EEA rules, the status is uncertain.'
    },
    BroadcastingCondition.BroadcastLapsedEvenIfEEA.value: {
        'green': 'Country of origin appears to be outside the EEA, but the broadcast would have lost protection even if the country of origin were in the EEA.'
    },

    # Rights conditions
    BroadcastingCondition.BroadcastCurrentRightHolderKnown.value: {
        'rights_green': 'Even if the broadcast is protected by broadcasting organisation rights, you are the rightholder.'
    },
    BroadcastingCondition.BroadcastAvailableCCLicense.value: {
        'rights_green': 'Even if the broadcast is protected, it is available under an open content license (e.g., CC0 or CC‑BY).',
        'rights_yellow': 'Even if the broadcast is protected, it is available under an open content license. Additional verification of the license terms may be needed.'
    },
    BroadcastingCondition.BroadcastOnlineAvailable.value: {
        'rights_green': 'Even if the broadcast is protected, you have acquired the necessary rights to make it available online.',
        'rights_yellow': 'Even if the broadcast is protected, you may make it available online under specific legal provisions. Additional verification may be needed.'
    }
}




# Digital representation rights explanation dictionaries
DIGITAL_REPRESENTATION_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Status conditions with templates
    DigitalRepresentationCondition.DigitalRepresentationCopyrightStatus.value: {
        'red': 'The digital representation is protected by {right_type}.',
        'yellow': 'It is uncertain whether the digital representation is protected by {right_type}.',
        'green': 'The digital representation is not protected by {right_type}.',
        'rights_green': 'The institution has {license_type}.',
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationPhonogramStatus.value: {
        'red': 'The digital representation is protected by {right_type}.',
        'yellow': 'It is uncertain whether the digital representation is protected by {right_type}.',
        'green': 'The digital representation is not protected by {right_type}.',
        'rights_green': 'The institution has {license_type}.',
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationFilmFixationStatus.value: {
        'red': 'The digital representation is protected by {right_type}.',
        'yellow': 'It is uncertain whether the digital representation is protected by {right_type}.',
        'green': 'The digital representation is not protected by {right_type}.',
        'rights_green': 'The institution has {license_type}.',
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationPerformanceStatus.value: {
        'red': 'The digital representation is protected by {right_type}.',
        'yellow': 'It is uncertain whether the digital representation is protected by {right_type}.',
        'green': 'The digital representation is not protected by {right_type}.',
        'rights_green': 'The institution has {license_type}.',
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationOtherIPStatus.value: {
        'red': 'The digital representation is protected by {right_type}.',
        'yellow': 'It is uncertain whether the digital representation is protected by {right_type}.',
        'green': 'The digital representation is not protected by {right_type}.',
        'rights_green': 'The institution has {license_type}.',
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    
    # Additional conditions (for yellow upgrades)
    DigitalRepresentationCondition.DigitalRepresentationAdditionalCopyrightStatus.value: {
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationAdditionalPhonogramStatus.value: {
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationAdditionalFilmFixationStatus.value: {
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationAdditionalPerformanceStatus.value: {
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    },
    DigitalRepresentationCondition.DigitalRepresentationAdditionalOtherIPStatus.value: {
        'rights_yellow': 'The {right_type} is available under {license_type}.'
    }
}

# Rights availability explanation templates
DIGITAL_REPRESENTATION_RIGHTS_TEMPLATES: Dict[str, str] = {
    'cc0': 'CC0 (public domain dedication)',
    'cc_by': 'CC BY license',
    'rights_assignment': 'acquired the rights through assignment',
    'license_agreement': 'acquired the rights through license agreement',
    'employee_rights': 'acquired the rights as the employer',
    'cc_by_sa': 'CC BY-SA license',
    'cc_by_nc_sa': 'CC BY-NC-SA license',
    'cc_by_nd': 'CC BY-ND license',
    'cc_by_nc_nd': 'CC BY-NC-ND license',
    'other_open': 'other open license',
    'orphan_works': 'orphan works provisions',
    'out_of_commerce': 'out-of-commerce provisions',
    'quote_right': 'quotation rights',
    'other_law': 'other legal provisions',
    'rights_not_acquired': 'rights not acquired'  # FIX: Add missing key
}

# Right type descriptions
DIGITAL_REPRESENTATION_RIGHT_TYPES: Dict[str, str] = {
    'copyright': 'copyright protection',
    'audio_recording_rights': 'phonogram rights protection',
    'film_fixation_rights': 'film fixation rights protection',
    'performance_rights': 'performance rights protection',
    'other_ip_rights': 'other IP rights protection'
}




# Other legal issues explanation dictionaries
OTHER_LEGAL_ISSUES_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Warning conditions (yellow)
    OtherLegalIssuesCondition.HasContractualRestrictions.value: {
        'yellow': 'It is necessary to review the agreements pertaining to the use of the work to determine the scope of possible obstacles.'
    },
    OtherLegalIssuesCondition.HasAdministrativeRestrictions.value: {
        'yellow': 'There may be restrictions stemming from administrative legal regulations.'
    },
    OtherLegalIssuesCondition.HasOwnershipIssues.value: {
        'yellow': 'Although ownership rights to the physical object are not a restriction to its online use, there may be other legal risks caused by the infringement of such rights by the institution'
    },
    OtherLegalIssuesCondition.ProvenanceNotTraced.value: {
        'yellow': 'Although uncertain or unknown provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution'
    },
    OtherLegalIssuesCondition.HasProvenanceIssues.value: {
        'yellow': 'Although troublesome provenance of the object does not per se restrict its online use, it may invite other legal risks on the side of the institution'
    },
    OtherLegalIssuesCondition.ContainsLivingIdentifiableInfo.value: {
        'yellow': 'The use of the object may lead to personal data processing, and depending on the exact context, require a legal basis under the General Data Protection Regulation'
    },
    OtherLegalIssuesCondition.ContainsSensitiveHistoricalInfo.value: {
        'yellow': 'The use of the object may expose the institution to defamation claims or similar liability'
    },
    OtherLegalIssuesCondition.ContainsTotalitarianAssociations.value: {
        'yellow': 'The use of the object may expose the institution to liability under hate-speech and similar legal regulations'
    },
    OtherLegalIssuesCondition.ContainsDiscriminatoryContent.value: {
        'yellow': 'The use of the object may expose the institution to liability under hate-speech and similar legal regulations'
    },
    OtherLegalIssuesCondition.ContainsOtherSensitiveContent.value: {
        'yellow': 'The use of the object may expose the institution to liability on grounds other than IP, personal data protection, personal rights or hate-speech laws'
    },
    OtherLegalIssuesCondition.HasOtherProblems.value: {
        'yellow': 'There are other legal issues that require verification.'
    },
    
    # Success condition (green)
    OtherLegalIssuesCondition.NoLegalIssues.value: {
        'green': 'No legal issues unrelated to intellectual property found.'
    }
}




# Additional classification explanation dictionaries
ADDITIONAL_CLASSIFICATION_CONDITION_TEXTS_BY_COLOR: Dict[str, Dict[str, str]] = {
    # Warning conditions (yellow)
    AdditionalClassificationCondition.PublicationNotAWork.value: {
        'yellow': 'In some EU member states, such publications obtain protection equivalent to copyright.'
    },
    AdditionalClassificationCondition.CriticalEdition.value: {
        'yellow': 'In some EU member states, such publications obtain protection equivalent or closely similar to copyright.'
    },
    AdditionalClassificationCondition.Trademark.value: {
        'yellow': 'There may be obstacles stemming from trademark law.'
    },
    AdditionalClassificationCondition.Design.value: {
        'yellow': 'There may be obstacles stemming from design law.',
        'red': 'There may be obstacles stemming from design law.'
    },
    
    # Success conditions (green)
    AdditionalClassificationCondition.NotPressPublication.value: {
        'green': 'The object is not a press publication.'
    },
    AdditionalClassificationCondition.PressPublicationLapsed.value: {
        'green': 'If the object was protected as a press publication, it has lapsed (published in {press_publication_year}, protection expired in {expiry_year}).'
    },
    AdditionalClassificationCondition.NoOtherIPRights.value: {
        'green': 'No other IP rights to consider'
    },
    
    # Restriction conditions (red)
    AdditionalClassificationCondition.PressPublicationProtected.value: {
        'red': 'The object may be protected as a press publication (published in {press_publication_year}, protection until {expiry_year}).',
        'red_no_year': 'The object may be protected as a press publication (publication year not provided).'
    }
}



# Mapping of condition types to their explanation dictionaries
CONDITION_EXPLANATION_DICTIONARIES = {
    'copyright': COPYRIGHT_CONDITION_TEXTS_BY_COLOR,
    'performance': PERFORMANCE_CONDITION_TEXTS_BY_COLOR,
    'film_fixation': FILM_FIXATION_CONDITION_TEXTS_BY_COLOR,
    'phonogram': PHONOGRAM_CONDITION_TEXTS_BY_COLOR,
    'broadcast': BROADCAST_CONDITION_TEXTS_BY_COLOR,
    'digital_representation': DIGITAL_REPRESENTATION_CONDITION_TEXTS_BY_COLOR,
    'other_legal_issues': OTHER_LEGAL_ISSUES_CONDITION_TEXTS_BY_COLOR,
    'additional_classification': ADDITIONAL_CLASSIFICATION_CONDITION_TEXTS_BY_COLOR,
}


def get_explanation(condition: str, color: str, condition_type: str = None, **fmt: object) -> str:
    """Return centralized explanation text for a given condition and color.
    
    Args:
        condition: The condition string to look up
        color: The color/status (e.g., 'green', 'yellow', 'red')
        condition_type: Optional type hint to speed up lookup (e.g., 'copyright', 'performance')
        **fmt: Formatting parameters for template substitution
    
    Returns:
        Formatted explanation text, or empty string if not found
    """
    # If condition_type is provided, use that dictionary directly
    if condition_type and condition_type in CONDITION_EXPLANATION_DICTIONARIES:
        template_dict = CONDITION_EXPLANATION_DICTIONARIES[condition_type]
    else:
        # Fallback: search through all dictionaries
        template_dict = None
        for dict_name, explanation_dict in CONDITION_EXPLANATION_DICTIONARIES.items():
            if condition in explanation_dict:
                template_dict = explanation_dict
                break
        
        if template_dict is None:
            return ''
    
    template = template_dict.get(condition, {}).get(color)
    if template is None:
        return ''
    
    try:
        return template.format(**fmt)
    except Exception:
        return template




COPYRIGHT_TERM = 70
FIRST_EDITION_TERM = 25
BROADCAST_RIGHTS_TERM = 50
FILM_FIXATION_TERM = 50
PHONOGRAM_TERM = 50
PHONOGRAM_EXTENSION_LONG = 70
PHONOGRAM_EXTENSION_SHORT = 50
PERFORMANCE_TERM = 50
PERFORMANCE_EXTENSION_LONG = 70
PERFORMANCE_EXTENSION_SHORT = 50
PRESS_PUBLICATION_TERM = 2