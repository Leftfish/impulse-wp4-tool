"""
Copyright module.

This module contains logic for calculating copyright status and related intermediate values.
"""

from defaults import ResultsDict
from utils_modules.text_constants import (
    COPYRIGHT_CC_LICENSE_EXPLANATIONS,
    COPYRIGHT_RIGHTS_EXPLANATIONS,
    COPYRIGHT_TERM,
    FIRST_EDITION_TERM,
    CopyrightCondition,
    get_explanation,
)

from datetime import datetime
from data.country_codes import is_eea_country


def calculate_intermediate_values_copyright(data):
    """Calculate intermediate boolean values used in copyright calculations.
    The intermediate values are then passed to the main calculation function."""
    current_year = datetime.now().year

    # Author-related calculations: are they anonymous or not
    # Rationale: if all authors are anonymous, we cannot apply the rule of 70 years since death
    all_authors_known = all(
        author.get("identity_known", False) for author in data.get("authors", [])
    )
    all_authors_anonymous = all(
        not author.get("identity_known", True) for author in data.get("authors", [])
    )

    # Country calculations
    # Rationale: if any author or publication is from EEA, we apply the EEA rules
    # Otherwise, we either apply the rule of shorter term or we refrain from giving a definite answer,
    # as it would require implementing detailed information about the national legislations
    country_codes = [
        author.get("country_of_origin", "XX") for author in data.get("authors", [])
    ]
    author_country_eea = any(is_eea_country(code) for code in country_codes if code)
    country_of_origin_unknown = all(code == "XX" for code in country_codes)

    # Publication status
    # Rationale: it matters for the country of origin (if published in EEA, we apply EEA rules)
    # as well as other rules, e.g. whether the work can be protected under first-edition provisions
    was_published = data.get("physically_published") == "published_on_physical_medium"

    # Publication country calculations
    # Rationale: where the work was published matters for the country of origin too
    if was_published:
        first_pub_country = data.get("country_first_publication")
        simul_pub_countries = data.get("simultaneous_publication_countries", [])
        publication_country_eea = (
            first_pub_country and is_eea_country(first_pub_country)
        ) or any(is_eea_country(code) for code in simul_pub_countries if code)
    else:
        publication_country_eea = False

    # Combined EEA status - True if either author or publication is from EEA
    country_of_origin_eea = author_country_eea or publication_country_eea

    # Time-based calculations with uncertainty flags
    # Relevant for calculations dependent on the lapse of 70 years since death
    death_year_unknown = not data.get("author_death_year")
    more_than_70_years_since_death = False
    if data.get("author_death_year"):
        more_than_70_years_since_death = (
            current_year - data["author_death_year"]
        ) > COPYRIGHT_TERM

    # First available year calculations
    # Rationale: calculations dependent on the lapse of 70 years since first availability
    # as well as, potentially, first editions
    first_available_year = min(
        filter(
            None, [data.get("first_publication_year"), data.get("first_available_year")]
        ),
        default=None,
    )    

    first_available_year_unknown = first_available_year is None
    more_than_70_years_since_first_available = False
    if first_available_year:
        more_than_70_years_since_first_available = (
            current_year - first_available_year
        ) > COPYRIGHT_TERM

    # Creation year calculations
    # Rationale: calculations dependent on the lapse of 70 years since creation
    # and, potentially, if the work is very new (fewer than 70 years since creation)
    # it is in all likelihood still under copyright
    creation_year_unknown = not data.get("creation_year")
    more_than_70_years_since_creation = False
    if data.get("creation_year"):
        more_than_70_years_since_creation = (
            current_year - data["creation_year"]
        ) > COPYRIGHT_TERM

    # Publication status
    # Rationale: to be used to jump to the logic covering unpublished works
    never_made_publicly_available = (
        data.get("physically_published") == "not_published_on_physical_medium"
        and data.get("otherwise_available") == "not_made_available_no_medium"
    )

    uncertain_if_publically_available = (
        data.get("physically_published") == "uncertain"
        and data.get("otherwise_available") == "uncertain"
    )

    return {
        "AllAuthorsKnown": all_authors_known,
        "AllAuthorsAnonymousOrPseudonymous": all_authors_anonymous,
        "CountryOfOriginEEAAuthor": author_country_eea,
        "CountryOfOriginEEAPublication": publication_country_eea,
        "CountryOfOriginEEAAnyReason": country_of_origin_eea,
        "CountryOfOriginUnknown": country_of_origin_unknown,
        "MoreThan70YearsSinceDeath": more_than_70_years_since_death,
        "DeathYearUnknown": death_year_unknown,
        "MoreThan70YearsSinceFirstAvailable": more_than_70_years_since_first_available,
        "FirstAvailableYearUnknown": first_available_year_unknown,
        "MoreThan70YearsSinceCreation": more_than_70_years_since_creation,
        "CreationYearUnknown": creation_year_unknown,
        "NeverMadePubliclyAvailable": never_made_publicly_available,
        "UncertainWhenPublicallyAvailable": not never_made_publicly_available and (uncertain_if_publically_available or first_available_year_unknown)
    }


def apply_open_content_license_status(results, cc_license_choice):
    """Apply status changes based on CC or other open-content license choice."""

    # These choices upgrade status to GREEN if currently RED or YELLOW
    green_rights_status = ["cc0", "cc_by"]

    # These choices upgrade status to YELLOW if currently RED
    # Rationale: these licenses have some restrictions, so they don't guarantee full open access
    yellow_rights_status = [
        "cc_by_sa",
        "cc_by_nc_sa",
        "cc_by_nd",
        "cc_by_nc_nd",
        "other_open",
    ]

    # Skip if not applicable
    if cc_license_choice in ["no", "not_applicable"]:
        pass

    explanations = COPYRIGHT_CC_LICENSE_EXPLANATIONS

    if cc_license_choice in green_rights_status and (
        results["red"] or results["yellow"]
    ):
        results["rights_green"].append(
            {
                "condition": CopyrightCondition.CopyrightObjectAvailableCCLicense.value,
                "explanation": explanations[cc_license_choice],
            }
        )
    elif cc_license_choice in yellow_rights_status:
        if results["red"] or results["yellow"]:
            results["rights_yellow"].append(
                {
                    "condition": CopyrightCondition.CopyrightObjectAvailableCCLicense.value,
                    "explanation": explanations[cc_license_choice],
                }
            )
    return results


def apply_online_availability_status(results, availability_choice):
    """Apply status changes based on online availability choice."""

    # These choices upgrade status to GREEN if currently RED or YELLOW
    green_rights_status = ["rights_assignment", "license_agreement", "employee_rights"]

    # These choices upgrade status to YELLOW if currently RED
    # Rationale: these statuses indicate some level of uncertainty or limitation regarding rights
    # due to various discrepancies in national implementations, or other complexities

    yellow_rights_status = [
        "orphan_works",
        "limited_license_agreement",
        "out_of_commerce",
        "quote_right",
        "other_law",
    ]

    explanations = COPYRIGHT_RIGHTS_EXPLANATIONS

    if availability_choice in green_rights_status and (
        results["red"] or results["yellow"]
    ):
        results["rights_green"].append(
            {
                "condition": CopyrightCondition.CopyrightObjectOnlineAvailable.value,
                "explanation": explanations[availability_choice],
            }
        )
    elif availability_choice in yellow_rights_status:
        if results["red"] or results["yellow"]:
            results["rights_yellow"].append(
                {
                    "condition": CopyrightCondition.CopyrightObjectOnlineAvailable.value,
                    "explanation": explanations[availability_choice],
                }
            )

    return results


def calculate_object_copyright_status(data, intermediate):
    """Calculate copyright status for the original object only."""
    results = ResultsDict()
    

    # Track variable usage
    used_vars = set()

    # Helper function to mark variables as used
    def mark_used(*vars):
        used_vars.update(vars)

    # Add informational notices based on work type
    if data.get("is_derivative") == "derivative":
        mark_used("is_derivative")
        _cond = CopyrightCondition.CopyrightDerivativeWork.value
        results["info"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "info", "copyright"),
            }
        )
    if data.get("is_derivative") == "uncertain":
        mark_used("is_derivative")
        _cond = CopyrightCondition.CopyrightDerivativeWork.value
        results["info"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "info_uncertain", "copyright"),
            }
        )

    if data.get("is_compound") == "compound":
        mark_used("is_compound")
        _cond = CopyrightCondition.CopyrightCompoundWork.value
        results["info"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "info", "copyright"),
            }
        )
    if data.get("is_compound") == "uncertain":
        mark_used("is_compound")
        _cond = CopyrightCondition.CopyrightCompoundWork.value
        results["info"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "info_uncertain", "copyright"),
            }
        )
    
    if data.get("is_photography") in [
        "photography_with_notice",
        "photography_without_notice",
    ]:
        mark_used("is_photography")
        _cond = CopyrightCondition.Photography.value
        results["info"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "info", "copyright"),
            }
        )

    if data.get("territory_status_changed"):
        mark_used("territory_status_changed")
        _cond = CopyrightCondition.CopyrightTerritoryStatusChanged.value
        results["info"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "info", "copyright"),
            }
        )

    # Simple override conditions - these take precedence over everything
    # Rationale: if, e.g., something is not a work, it cannot be under copyright
    # if something was made before 1850, it is in all likelihood in the public domain
    # (but we still need to check for first edition status later on)
    if data.get("is_copyright_work") == "not_work":
        mark_used("is_copyright_work")
        _cond = CopyrightCondition.PublicDomainNotAWork.value
        results["green"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "green", "copyright"),
            }
        )
        return results, used_vars

    if data.get("created_before_1850") == "made_before_1850":
        mark_used("created_before_1850")
        _cond = CopyrightCondition.PublicDomainRuleOfThumb.value
        results["green"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "green", "copyright"),
            }
        )
        return results, used_vars

    # Special case: if uncertain whether it is a work but it's from before 1850, it's GREEN
    if (
        data.get("is_copyright_work") == "uncertain"
        and data.get("created_before_1850") == "made_before_1850"
    ):
        mark_used("is_copyright_work", "created_before_1850")
        _cond = CopyrightCondition.PublicDomainRuleOfThumb.value
        results["green"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "green_uncertain_work", "copyright"),
            }
        )
        return results, used_vars

    # Rationale: if uncertain whether it is a work, we can either display YELLOW and
    # dispense with further calculations, or continue with the calculations
    # We choose to continue, as there might be other conditions that lead to GREEN status
    if data.get("is_copyright_work") == "uncertain":
        mark_used("is_copyright_work")
        _cond = CopyrightCondition.CopyrightUncertainIfWork.value
        results["yellow"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "yellow", "copyright"),
            }
        )
    
    # Easy rule of thumb (EEA countries): new work - RED status
    # Non-EEA countries: new work - YELLOW status
    if (
        intermediate["CountryOfOriginEEAAnyReason"]
        and data.get("creation_year")
        and not intermediate["MoreThan70YearsSinceCreation"]
    ): 
        mark_used("authors", "creation_year")
        _cond = (
            CopyrightCondition.CopyrightNewWorkNoPublicDomain.value
        )
        
        results["red"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "red", "copyright"),
            }
        )
        return results, used_vars
    
    if (
        not intermediate["CountryOfOriginEEAAnyReason"]
        and data.get("creation_year")
        and not intermediate["MoreThan70YearsSinceCreation"]
    ): 
        mark_used("authors", "creation_year")
        
        _cond = (
            CopyrightCondition.CopyrightNewWorkNoPublicDomain.value
        )
        results["yellow"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "yellow", "copyright"),
            }
        )
        return results, used_vars

    # Check uncertain conditions that lead to YELLOW status
    # Rationale: if we have no idea if the authors is alive or not, we cannot state
    # if the work is in the public domain or not. But a license might still be valid
    # so we comment out the early exit!

    if (
        not intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and data.get("author_alive") == "uncertain"
    ):
        mark_used("authors", "author_alive")
        _cond = CopyrightCondition.CopyrightAuthorAlive.value
        results["yellow"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "yellow", "copyright"),
            }
        )

    # This leads to YELLOW due to the possible differences between the EU member states, 
    # allowed by Article 1 sec. 4 of the Term Directive
    # Rationale: this app does not take into account national implementations of the Term Directive
    # Article 1(4) begins with " Where a Member State provides..."
    # Again, a license may still be valid!
    
    if data.get("original_rightholder") == "legal_person":
        mark_used("original_rightholder")
        _cond = (
            CopyrightCondition.CopyrightPublicDomainArticle1Section4LegalPerson.value
        )
        results["yellow"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "yellow_legal_person", "copyright"),
            }
        )

    if data.get("original_rightholder") == "uncertain":
        mark_used("original_rightholder")
        _cond = (
            CopyrightCondition.CopyrightPublicDomainArticle1Section4LegalPerson.value
        )
        results["yellow"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "yellow_uncertain_rightholder", "copyright"),
            }
        )

    # Check copyright lapse conditions

    # Mark used data that allowed us to find the country of origin
    if intermediate["CountryOfOriginEEAAuthor"]:
        mark_used("country_of_origin")
    if intermediate["CountryOfOriginEEAPublication"]:
        mark_used("country_first_publication", "simultaneous_publication_countries")

    
    # Article 1 Section 1-2 (EEA countries)
    # Rationale: the simple case: author(s) known, country of origin from EEA
    # lapse after 70 years post mortem auctoris applies

    if (
        intermediate["AllAuthorsKnown"]
        and intermediate["CountryOfOriginEEAAnyReason"]
    ):
        if (
            intermediate["MoreThan70YearsSinceDeath"]
            ):
            mark_used("authors", "author_death_year")
            _cond = CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2.value
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        elif (
            intermediate["DeathYearUnknown"]
            ):
            mark_used("authors", "author_death_year")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )
        else:
            mark_used("authors", "author_death_year")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2.value
            )
            results["red"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "red", "copyright"),
                }
            )

    # Article 1 Section 1-2 Rule of Shorter Term (non-EEA countries)
    # Rationale: this applies the rule of shorter term from Article 7(1) of the Term Directive

    if (
        intermediate["AllAuthorsKnown"]
        and not intermediate["CountryOfOriginEEAAnyReason"]
    ):
        if (
            intermediate["MoreThan70YearsSinceDeath"]
            ):
            mark_used("authors", "author_death_year")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2RuleOfShorterTerm.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        else:
            mark_used("authors")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2RuleOfShorterTerm.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )

    # Article 1 Section 3 (EEA countries)
    # Rationale: anonymous or pseudonymous works, lapse after 70 years since first made available

    if (
        intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and intermediate["CountryOfOriginEEAAnyReason"]
        and not intermediate["NeverMadePubliclyAvailable"]
        ):

        if (
            intermediate["MoreThan70YearsSinceFirstAvailable"]
        ):
            mark_used("authors", "available_year")
            _cond = CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3.value
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        elif (
            intermediate["FirstAvailableYearUnknown"]
        ):
            mark_used("authors", "available_year")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )

        elif (
            not intermediate["MoreThan70YearsSinceFirstAvailable"]
            and not intermediate["FirstAvailableYearUnknown"]
        ):
            mark_used("authors", "available_year")
            _cond = CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3.value
            results["red"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "red", "copyright"),
                }
            )


    # Article 1 Section 3 Rule of Shorter Term (non-EEA countries)
    # Rationale: Rule of shorter term per Article 7(1) Term Directive

    if (
        intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and not intermediate["CountryOfOriginEEAAnyReason"]):

        if (
            intermediate["MoreThan70YearsSinceFirstAvailable"]
        ):
            mark_used("authors", "available_year")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        else:
            mark_used("authors", "available_year")
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )

    # Article 1 Section 4 handled above
    # Rationale: we decided to apply YELLOW status because we do not implement
    # detailed national implementations of the Term Directive

    # Article 1 Section 5 skipped because it is not a substantive rule per se
    # Article 1(5) only tells us how to calculate the term of protection for each volume etc.

    # Article 1 Section 6 (EEA countries)
    # Rationale: anonymous or pseudonymous works that never made publicly available
    # so we can't apply sections 1-3 and revert to the creation year

    if (
        intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and intermediate["NeverMadePubliclyAvailable"]
        and intermediate["CountryOfOriginEEAAnyReason"]
    ):
        if (
            intermediate["MoreThan70YearsSinceCreation"]
            ):
            mark_used(
                "authors", "otherwise_available", "physically_published", "creation_year"
            )
            _cond = CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6.value
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        elif (
            intermediate["CreationYearUnknown"]
            ):
                mark_used(
                    "authors",
                    "otherwise_available",
                    "physically_published",
                    "creation_year",
                )
                _cond = (
                    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6.value
                )
                results["yellow"].append(
                    {
                        "condition": _cond,
                        "explanation": get_explanation(_cond, "yellow", "copyright"),
                    }
                )
        else:
            mark_used(
                "authors",
                "otherwise_available",
                "physically_published",
                "creation_year",
            )
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6.value
            )
            results["red"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "red", "copyright"),
                }
            )

    # Article 1 Section 6 Rule of Shorter Term (non-EEA countries)
    # Rationale: rule of shorter term per Article 7(1) Term Directive

    if (
        intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and intermediate["NeverMadePubliclyAvailable"]
        and (
            not intermediate["CountryOfOriginEEAAnyReason"]
            or intermediate["CountryOfOriginUnknown"]
        )
    ):
        if (
        intermediate["MoreThan70YearsSinceCreation"]
        ):
            mark_used(
                "authors", "otherwise_available", "physically_published", "creation_year"
            )
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        else:
            mark_used(
                "authors", "otherwise_available", "physically_published", "creation_year"
            )
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )

    # Article 1 Section 6 - Late Publication Case (EEA countries)
    # For anonymous works that were not made available within 70 years of creation
    # but were published later (after entering public domain) we do not "revive"
    # protection; the work remains in the public domain

    if (
        intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and intermediate["CountryOfOriginEEAAnyReason"]):

        if (
            data.get("first_publication_year")
            and data.get("creation_year")
            and (data["first_publication_year"] - data["creation_year"]) > COPYRIGHT_TERM
            ):
            mark_used(
                "authors", "physically_published", "first_publication_year", "creation_year"
            )
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        elif (
            data.get("first_publication_year")
            and intermediate["CreationYearUnknown"]
            and not intermediate["MoreThan70YearsSinceFirstAvailable"]
        ):
                mark_used(
                    "authors",
                    "physically_published",
                    "first_publication_year",
                    "creation_year",
                )
                _cond = (
                    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication.value
                )
                _template = get_explanation(_cond, "yellow", "copyright")
                _expl = (
                    (
                        _template
                        and _template.format(
                            first_publication_year=data.get("first_publication_year")
                        )
                    )
                )
                results["yellow"].append({"condition": _cond, "explanation": _expl})

    # Article 1 Section 6 - Late Publication Case (non-EEA countries)
    # Rationale: rule of shorter term per Article 7(1) Term Directive

    if (
        intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and (
            not intermediate["CountryOfOriginEEAAnyReason"]
            or intermediate["CountryOfOriginUnknown"]
        )):

        if (
            data.get("first_publication_year")
            and data.get("creation_year")
            and (data["first_publication_year"] - data["creation_year"]) > COPYRIGHT_TERM
        ):
            mark_used(
                "authors", "physically_published", "first_publication_year", "creation_year"
            )
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        elif (
            data.get("first_publication_year")
            and intermediate["CreationYearUnknown"]
            and not intermediate["MoreThan70YearsSinceFirstAvailable"]
        ):
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )

    # Check if duplicates with Article 1(3) logic. If fewer than 70 years passed since the first publication
    # it would normally trigger. But it shouldn't, because it is a LATE publication which took place
    # after the work went into the public domain. Perhaps there is another first edition right, but that's 
    # another story
    _SEC6_STATUS = [CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication.value,
                    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm.value]
    _SEC3_STATUS = [CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3.value,
                    CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm.value]
    if any(
        s["condition"] in _SEC6_STATUS
        for s in results["green"]
    ):
        results["red"] = [
            s for s in results["red"]
            if not s["condition"] in _SEC3_STATUS
        ]
    
    
    # Article 1 Section 1-2 Plus Section 3 (EEA countries)
    if (
        intermediate["CountryOfOriginEEAAnyReason"]
        and len(data.get("authors", [])) > 1
        and (not intermediate["AllAuthorsKnown"])
        and (not intermediate["AllAuthorsAnonymousOrPseudonymous"]) 
        and not intermediate["NeverMadePubliclyAvailable"]
        ):
        if (intermediate["MoreThan70YearsSinceDeath"]
        and intermediate["MoreThan70YearsSinceFirstAvailable"]
        ):
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        elif (
            intermediate["DeathYearUnknown"]
            or (intermediate["FirstAvailableYearUnknown"])
        ):
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )
        else:
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3.value
            )
            results["red"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "red", "copyright"),
                }
            )
    
    # Article 1 Section 1-2 Plus Section 3 (non-EEA countries)
    # Rationale: rule of shorter term
    if (
        (not intermediate["CountryOfOriginEEAAnyReason"]
            or intermediate["CountryOfOriginUnknown"])
        and len(data.get("authors", [])) > 1
        and (not intermediate["AllAuthorsKnown"])
        and (not intermediate["AllAuthorsAnonymousOrPseudonymous"])
        and not intermediate["NeverMadePubliclyAvailable"]
        ):
        if (intermediate["MoreThan70YearsSinceDeath"]
        and intermediate["MoreThan70YearsSinceFirstAvailable"]
        ):
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm.value
            )
            results["green"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "green", "copyright"),
                }
            )
        else:
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright"),
                }
            )
        


    # Article 1 Section 1-2 Plus Section 6
    # Rationale: to cover edge cases not caught by previous rules
    if (
        intermediate["CountryOfOriginEEAAnyReason"]
        and intermediate["MoreThan70YearsSinceDeath"]
        and intermediate["MoreThan70YearsSinceCreation"]
        and intermediate["NeverMadePubliclyAvailable"]
    ):
        _cond = (
            CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec6.value
        )
        results["green"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "green", "copyright"),
            }
        )
    elif (
        intermediate["CountryOfOriginEEAAnyReason"]
        and intermediate["NeverMadePubliclyAvailable"]
    ):
        if intermediate["DeathYearUnknown"] or intermediate["CreationYearUnknown"]:
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec6.value
            )
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright")
                    or "Unable to determine if copyright has lapsed because either the author's death year or creation year is unknown.",
                }
            )
        else:
            _cond = (
                CopyrightCondition.CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec6.value
            )
            results["red"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "red", "copyright")
                    or "The object is still under copyright because fewer than 70 years passed since either the author's death or creation.",
                }
            )

    # Check if the known author is alive - this downgrades any YELLOW to RED status
    if (
        not intermediate["AllAuthorsAnonymousOrPseudonymous"]
        and data.get("author_alive") == "author_alive"
    ):
        results["yellow"] = []
        _cond = CopyrightCondition.CopyrightAuthorAlive.value
        results["red"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "red", "copyright"),
            }
        )

    # Check if the institution is the rightholder
    # Rationale: if the institution is the rightholder, there are no obstacles in 
    # making the object available online
    mark_used("current_rightholder")
    if data.get("current_rightholder") == "rightholder_us":
        _cond = CopyrightCondition.CurrentRightHolderKnown.value
        results["rights_green"].append(
            {
                "condition": _cond,
                "explanation": get_explanation(_cond, "rights_green", "copyright"),
            }
        )

    # Apply CC license status after initial calculations but before online availability
    mark_used("object_cc_license")
    results = apply_open_content_license_status(results, data.get("object_cc_license"))

    # Apply online availability status after CC license status
    mark_used("object_copyright_rights_acquired_to_make_available")
    results = apply_online_availability_status(
        results, data.get("object_copyright_rights_acquired_to_make_available")
    )

    return results, used_vars


def calculate_first_edition_protection_status(data, intermediate):
    """Calculate first edition protection status for any public domain work."""
    results = ResultsDict()
    used_vars = set()

    #Only check if we have a first publication year: disabled because we want YELLOW 
    #status if we don't know if/when it was first published
    #if not (data.get("first_publication_year") or data.get("first_available_year")):
    #    return results, used_vars

    first_pub_year = data.get("first_publication_year", None)
    first_available_year = data.get("first_available_year") if data.get("internet_first_available") == "made_available_internet" else 0
    

    if first_pub_year and first_available_year:
        first_edition_year = min(first_pub_year, first_available_year)
    elif first_pub_year:
        first_edition_year = first_pub_year
    elif first_available_year:
        first_edition_year = first_available_year
    else:
        first_edition_year = 0

    current_year = datetime.now().year
    
    # Check if first publication was within last 25 years or the date is unknown (so it could fall within the last 25 years)
    if intermediate["UncertainWhenPublicallyAvailable"] or ((current_year - first_edition_year) <= FIRST_EDITION_TERM):
        
        # Determine if this is a first edition of a public domain work
        # Alternative option: unknown when it was published, so still possible, that protection applies
        is_first_edition_candidate = False
        public_domain_reason = ""

        # Case 1: Pre-1850 work is automatically a first-edition candidate
        if data.get("created_before_1850") == "made_before_1850":
            is_first_edition_candidate = True
            public_domain_reason = "created before 1850"

        # Case 2: Anonymous work that entered public domain before publication
        elif (
            data.get("is_copyright_work") == "work"
            and intermediate["AllAuthorsAnonymousOrPseudonymous"]
            and data.get("creation_year")
            and first_edition_year
            and first_edition_year > (data["creation_year"] + COPYRIGHT_TERM)
        ):
            is_first_edition_candidate = True
            public_domain_reason = (
                f"anonymous work entered public domain in {data['creation_year'] + COPYRIGHT_TERM}"
            )

        # Case 3: Known author who died more than 70 years before publication
        elif data.get("author_death_year") and first_edition_year > (
            data["author_death_year"] + COPYRIGHT_TERM
        ):
            is_first_edition_candidate = True
            public_domain_reason = f"author died in {data['author_death_year']}, entered public domain in {data['author_death_year'] + COPYRIGHT_TERM}"

        # Apply first edition protection if candidate
        if is_first_edition_candidate:
            _cond = CopyrightCondition.FirstEditionProtection.value
            results["yellow"].append(
                {
                    "condition": _cond,
                    "explanation": get_explanation(_cond, "yellow", "copyright").format(
                        first_edition_year=first_edition_year if first_edition_year else "unknown",
                        public_domain_reason=public_domain_reason
                    ),
                }
            )

        

    return results, used_vars
