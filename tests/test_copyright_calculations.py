# pylint: disable=unsubscriptable-object, missing-function-docstring, missing-module-docstring, missing-class-docstring, line-too-long

import unittest
from datetime import datetime
from utils import (
    calculate_all_intermediate_values,
    calculate_results,
    calculate_intermediate_values_copyright,
)


def base_data():
    return {
        "object_name": "Test",
        "institution_name": "Inst",
        "broadcast_info": {},
        "copyright_info": {
            "is_copyright_work": "work",
            "authors": [{"identity_known": True, "country_of_origin": "DE"}],
            "created_before_1850": "not_made_before_1850",
        },
        "digital_representation_info": {},
        "film_fixation_info": {},
        "performance_info": {},
        "phonogram_info": {},
        "other_intellectual_property_info": {},
        "other_restrictions_info": {},
    }


def run_copyright(data):
    intermediate = calculate_all_intermediate_values(data)
    results = calculate_results(data, intermediate)
    return results


class TestCopyrightCalculations(unittest.TestCase):
    def setUp(self):
        self.current_year = datetime.now().year

    def test_article1_sec1_2(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2"""
        # Test case where all conditions are met
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "DE"}  # Germany (EEA)
                ],
                "author_death_year": self.current_year - 71,  # More than 70 years ago
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )

        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

        # Test case where conditions are not met (author death less than 70 years)
        data["copyright_info"]["author_death_year"] = self.current_year - 70
        results = run_copyright(data)

        self.assertFalse(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec1_2_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm"""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {
                        "identity_known": True,
                        "country_of_origin": "US",
                    }  # Non-EEA country
                ],
                "author_death_year": self.current_year - 71,
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec3(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3"""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": False, "country_of_origin": "FR"}  # France (EEA)
                ],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year - 71,
                "first_available_year": self.current_year - 71,
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec3"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec3_uncertain_publication(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3"""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {
                        "identity_known": False,
                        "country_of_origin": "NL",
                    }  # Netherlands (EEA)
                ],
                "physically_published": "uncertain",
                "otherwise_available": "uncertain",
            }
        )
        results = run_copyright(data)

        self.assertFalse(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec3"
                for r in results["copyright_status"]["red"]
            )
        )
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec3"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_article1_sec3_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm"""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {
                        "identity_known": False,
                        "country_of_origin": "JP",
                    }  # Japan (non-EEA)
                ],
                "first_publication_year": self.current_year - 71,
                "first_available_year": self.current_year - 71,
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec6(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec6"""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": False, "country_of_origin": "IT"}  # Italy (EEA)
                ],
                "creation_year": self.current_year - 71,
                "physically_published": "not_published_on_physical_medium",
                "otherwise_available": "not_made_available_no_medium",
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec6"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec6_rule_of_shorter_term(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm"""
        # Test with non-EEA country
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {
                        "identity_known": False,
                        "country_of_origin": "CN",
                    }  # China (non-EEA)
                ],
                "creation_year": self.current_year - 71,
                "physically_published": "not_published_on_physical_medium",
                "otherwise_available": "not_made_available_no_medium",
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

        # Test with unknown country
        data["copyright_info"]["authors"][0]["country_of_origin"] = "XX"

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6RuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec1_2_plus_sec3_green_mixed_authors(self):
        """EEA work, three authors (two known, one anonymous): green when both term limbs pass."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": False, "country_of_origin": "DE"},
                ],
                "physically_published": "published_on_physical_medium",
                "author_death_year": 1950,
                "first_publication_year": 1940,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec1_2_plus_sec3_yellow_death_unknown(self):
        """Mixed authors: yellow when last known co-author death year is unknown."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": False, "country_of_origin": "DE"},
                ],
                "physically_published": "published_on_physical_medium",
                "first_publication_year": 1940,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_article1_sec1_2_plus_sec3_yellow_publication_unknown(self):
        """Mixed authors: yellow when first publication / availability year is unknown."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": False, "country_of_origin": "DE"},
                ],
                "author_death_year": 1945,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_article1_sec1_2_plus_sec3_red_mixed_authors(self):
        """Mixed authors: red when both years are known but fewer than 70 years have passed."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": True, "country_of_origin": "DE"},
                    {"identity_known": False, "country_of_origin": "DE"},
                ],
                "physically_published": "published_on_physical_medium",
                "author_death_year": 1980,
                "first_publication_year": 1970,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec3"
                for r in results["copyright_status"]["red"]
            )
        )

    def test_article1_sec1_2_plus_sec3_green_non_eea_two_anons_countries_unknown(self):
        """Non-EEA / unknown-origin path: green when both term limbs pass (countries all XX)."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "XX"},
                    {"identity_known": False, "country_of_origin": "XX"},
                    {"identity_known": False, "country_of_origin": "XX"},
                ],
                "physically_published": "published_on_physical_medium",
                "author_death_year": 1950,
                "first_publication_year": 1950,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec1_2_plus_sec3_green_non_eea_two_anons_all_non_eea(self):
        """Non-EEA path: green when both term limbs pass (all authors non-EEA)."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                ],
                "physically_published": "published_on_physical_medium",
                "author_death_year": 1950,
                "first_publication_year": 1950,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_article1_sec1_2_plus_sec3_yellow_non_eea_two_anons_publication_unknown(self):
        """Non-EEA path: yellow when first publication / availability is unknown."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                ],
                "author_death_year": 1950,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_article1_sec1_2_plus_sec3_yellow_non_eea_two_anons_death_unknown(self):
        """Non-EEA path: yellow when last known co-author death year is unknown."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                ],
                "physically_published": "published_on_physical_medium",
                "first_publication_year": 1950,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_article1_sec1_2_plus_sec3_yellow_non_eea_two_anons_term_not_lapsed(self):
        """Non-EEA path: yellow when dates known but green limb not met (no red in this branch)."""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                    {"identity_known": False, "country_of_origin": "US"},
                ],
                "physically_published": "published_on_physical_medium",
                "author_death_year": 1970,
                "first_publication_year": 1970,
            }
        )
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1_2PlusSec3RuleOfShorterTerm"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_article1_sec1_2_plus_sec6(self):
        """Test CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6"""
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {
                        "identity_known": True,
                        "country_of_origin": "PT",
                    }  # Portugal (EEA)
                ],
                "author_death_year": self.current_year - 71,
                "creation_year": self.current_year - 71,
                "physically_published": "not_published_on_physical_medium",
                "otherwise_available": "not_made_available_no_medium",
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2PlusSec6"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_not_copyright_work(self):
        """Test when object is not considered a copyright work"""
        data = base_data()
        data["copyright_info"].update({"is_copyright_work": "not_work"})

        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainNotAWork"
                for r in results["copyright_status"]["green"]
            )
        )
        # No other results should be present
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

    def test_pre_1850_work(self):
        """Test when work was created before 1850"""
        data = base_data()
        data["copyright_info"].update(
            {
                "created_before_1850": "made_before_1850",
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )
        # No other results should be present
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

    def test_pre_1850_work_with_digital_representation(self):
        """Test that digital representation analysis runs even when object is pre-1850 (Bug #1 fix)"""
        data = base_data()
        data["copyright_info"].update({"created_before_1850": "made_before_1850"})
        data["digital_representation_info"] = {
            "digital_repr_ip_rights": {
                "copyright": "yes",
                "phonogram_rights": "no",
                "film_fixation_rights": "no",
                "performance_rights": "no",
                "other_ip_rights": "no",
            }
        }

        results = run_copyright(data)

        # Object should be GREEN
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )

        # Digital representation should be analyzed (RED for copyright)
        self.assertIsNotNone(results["digital_repr_status"])
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationCopyrightStatus"
                for r in results["digital_repr_status"]["red"]
            )
        )
        self.assertTrue(
            any(
                r["condition"] == "DigitalRepresentationPhonogramStatus"
                for r in results["digital_repr_status"]["green"]
            )
        )

    def test_rights_holder_override(self):
        """Test when institution is the rights holder"""
        # Case 1: Living author but institution has rights
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_alive",
                "current_rightholder": "rightholder_us",
                "authors": [{"identity_known": True, "country_of_origin": "AT"}],
            }
        )
        results = run_copyright(data)

        # Should be GREEN because institution has rights
        self.assertTrue(
            any(
                r["condition"] == "CurrentRightHolderKnown"
                for r in results["copyright_status"]["rights_green"]
            )
        )

        # Case 2: Recent death but institution has rights
        data["copyright_info"]["author_alive"] = "author_dead"
        data["copyright_info"]["author_death_year"] = self.current_year - 20

        results = run_copyright(data)

        # Should be GREEN because institution has rights
        self.assertTrue(
            any(
                r["condition"] == "CurrentRightHolderKnown"
                for r in results["copyright_status"]["rights_green"]
            )
        )

    def test_rule_of_shorter_term_yellow(self):
        """Test Rule of Shorter Term cases that should be YELLOW"""
        # Case 1: Known authors, non-EEA country, less than 70 years
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [{"identity_known": True, "country_of_origin": "US"}],
                "author_death_year": self.current_year - 50,
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2RuleOfShorterTerm"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_rule_of_shorter_term_yellow_anonymous(self):
        # Case 2: Anonymous work, non-EEA country, less than 70 years
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [{"identity_known": False, "country_of_origin": "JP"}],
                "first_publication_year": self.current_year - 50,
                "country_first_publication": "JP",
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec3RuleOfShorterTerm"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_late_publication_of_anonymous_works(self):
        # Case 1: early anonymous work, first published very recently and after it passed to the public domain
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [{"identity_known": False, "country_of_origin": "FR"}],
                "first_publication_year": self.current_year - 10,
                "creation_year": self.current_year - 100,
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication"
                for r in results["copyright_status"]["green"]
            )
        )

        # Case 2: anonymous work published very recently, but year of creation unknown
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [{"identity_known": False, "country_of_origin": "FR"}],
                "first_publication_year": self.current_year - 10,
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_late_publication_of_anonymous_works_non_eea(self):
        # Case 1: early anonymous work, first published very recently and after it passed to the public domain
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [{"identity_known": False, "country_of_origin": "XX"}],
                "first_publication_year": self.current_year - 10,
                "creation_year": self.current_year - 100,
            }
        )

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm"
                for r in results["copyright_status"]["green"]
            )
        )

        # Case 2: anonymous work published very recently, but year of creation unknown
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [{"identity_known": False, "country_of_origin": "XX"}],
                "first_publication_year": self.current_year - 10,
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublicationRuleOfShorterTerm"
                for r in results["copyright_status"]["yellow"]
            )
        )


    def test_uncertain_conditions(self):
        """Test conditions that should result in YELLOW status"""
        # Case 1: Uncertain if author is alive
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "uncertain",
                "authors": [{"identity_known": True, "country_of_origin": "FR"}],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightAuthorAlive"
                for r in results["copyright_status"]["yellow"]
            )
        )

        # Case 2: Legal person was original rights holder
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "original_rightholder": "legal_person",
                "authors": [{"identity_known": True, "country_of_origin": "DE"}],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainArticle1Section4LegalPerson"
                for r in results["copyright_status"]["yellow"]
            )
        )

        # Case 3: Uncertain original rights holder
        data["copyright_info"]["original_rightholder"] = "uncertain"

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainArticle1Section4LegalPerson"
                for r in results["copyright_status"]["yellow"]
            )
        )

    def test_living_author_austria(self):
        """Test case with living author from Austria"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_alive",
                "authors": [{"identity_known": True, "country_of_origin": "AT"}],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be RED (but can have yellow too)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightAuthorAlive"
                for r in results["copyright_status"]["red"]
            )
        )

    def test_recent_death_austria(self):
        """Test case with author from Austria who died recently"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_dead",
                "authors": [{"identity_known": True, "country_of_origin": "AT"}],
                "author_death_year": self.current_year - 50,
            }
        )
        results = run_copyright(data)

        # Should be RED (but can have yellow too)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["red"]
            )
        )

    def test_green_overrides_rights_holder(self):
        """Test that GREEN status is not affected by rights holder status"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_dead",
                "current_rightholder": "rightholder_us",
                "authors": [{"identity_known": True, "country_of_origin": "DE"}],
                "author_death_year": self.current_year - 71,
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be GREEN because of time passed, not because of rights holder
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )
        self.assertFalse(
            any(
                r["condition"] == "CurrentRightHolderKnown"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_override_conditions(self):
        """Test that override conditions (not a work, pre-1850) take precedence"""
        # Case 1: Not a copyright work but would otherwise be RED
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "not_work",
                "author_alive": "author_alive",
                "authors": [{"identity_known": True, "country_of_origin": "AT"}],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainNotAWork"
                for r in results["copyright_status"]["green"]
            )
        )
        # No other results should be present
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

        # Case 2: Pre-1850 work but would otherwise be RED
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "author_alive": "author_alive",
                "authors": [{"identity_known": True, "country_of_origin": "AT"}],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )
        # No other results should be present
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

        # Case 3: Pre-1850 work with posthumous edition
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "author_death_year": self.current_year - 100,
                "first_publication_year": self.current_year - 20,
            }
        )
        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # No other results should be present
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

    def test_simplified_override_conditions(self):
        """Test that override conditions work with default values"""
        # Case 1: Not a copyright work with default values
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "not_work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_alive",  # This would normally make it RED
                "current_rightholder": "rightholder_unknown",  # This would normally affect status
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainNotAWork"
                for r in results["copyright_status"]["green"]
            )
        )
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

        # Case 2: Pre-1850 work with default values
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "author_alive": "author_alive",  # This would normally make it RED
                "current_rightholder": "rightholder_unknown",  # This would normally affect status
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        results = run_copyright(data)

        # Should be GREEN only
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )
        self.assertEqual(len(results["copyright_status"]["yellow"]), 0)
        self.assertEqual(len(results["copyright_status"]["red"]), 0)
        self.assertEqual(len(results["copyright_status"]["info"]), 0)

    def test_eea_origin_determination(self):
        """Test that EEA origin is determined by either author's country or publication country"""
        # Case 1: Non-EEA author but EEA first publication
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"}  # Non-EEA
                ],
                "country_first_publication": "DE",  # EEA (Germany)
                "author_death_year": self.current_year - 71,
                "physically_published": "published_on_physical_medium",
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        intermediate = calculate_intermediate_values_copyright(data["copyright_info"])
        self.assertTrue(intermediate["CountryOfOriginEEAAnyReason"])

        # Case 2: EEA author but non-EEA first publication
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "FR"}  # EEA (France)
                ],
                "physically_published": "published_on_physical_medium",
                "country_first_publication": "US",  # Non-EEA
                "author_death_year": self.current_year - 71,
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        intermediate = calculate_intermediate_values_copyright(data["copyright_info"])
        self.assertTrue(intermediate["CountryOfOriginEEAAnyReason"])

        # Case 3: Non-EEA author and first publication, but EEA simultaneous publication
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"}  # Non-EEA
                ],
                "physically_published": "published_on_physical_medium",
                "country_first_publication": "US",  # Non-EEA
                "simultaneous_publication_countries": ["DE"],  # EEA (Germany)
                "author_death_year": self.current_year - 71,
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        intermediate = calculate_intermediate_values_copyright(data["copyright_info"])
        self.assertTrue(intermediate["CountryOfOriginEEAAnyReason"])

        # Case 4: No EEA connection at all
        data = base_data()
        data["copyright_info"].update(
            {
                "authors": [
                    {"identity_known": True, "country_of_origin": "US"}  # Non-EEA
                ],
                "country_first_publication": "US",  # Non-EEA
                "simultaneous_publication_countries": ["JP"],  # Non-EEA
                "author_death_year": self.current_year - 71,
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )
        intermediate = calculate_intermediate_values_copyright(data["copyright_info"])
        self.assertFalse(intermediate["CountryOfOriginEEAAnyReason"])

    def test_first_posthumous_edition(self):
        """Test posthumous edition cases"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_dead",
                "authors": [{"identity_known": True, "country_of_origin": "FR"}],
                "author_death_year": self.current_year - 100,
                "first_publication_year": self.current_year - 20,
            }
        )

        results = run_copyright(data)

        # Should have first edition protection (YELLOW) in the specialized section
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_pre_1850_recent_publication(self):
        """Test Case 1: Pre-1850 work, first published in 2020"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "first_publication_year": self.current_year
                - 5,  # Published 5 years ago
            }
        )
        results = run_copyright(data)

        # Should have first edition protection (YELLOW)
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should still be GREEN
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_pre_1850_old_publication(self):
        """Test Case 2: Pre-1850 work, first published in 1990"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "first_publication_year": self.current_year
                - 35,  # Published 35 years ago
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection (protection lapsed)
        self.assertFalse(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should still be GREEN
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_anonymous_eea_recent_publication(self):
        """Test Case 3: Anonymous work, EEA origin, created 1940, first published 2020"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [
                    {
                        "identity_known": False,
                        "country_of_origin": "DE",
                    }  # Anonymous, EEA
                ],
                "creation_year": self.current_year - 85,  # Created 85 years ago (1940)
                "first_publication_year": self.current_year
                - 5,  # Published 5 years ago (2020)
            }
        )
        results = run_copyright(data)

        # Should have first edition protection (YELLOW)
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(
            any(
                r["condition"]
                == "CopyrightPublicDomainRightsLapsedArticle1Sec6LatePublication"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_known_author_before_public_domain(self):
        """Test Case 4: Non-anonymous author, EEA origin, author dies 1940, published 2000"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [
                    {"identity_known": True, "country_of_origin": "FR"}  # Known, EEA
                ],
                "author_death_year": self.current_year - 85,  # Died 85 years ago (1940)
                "first_publication_year": self.current_year
                - 25,  # Published 25 years ago (2000)
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection (published before entering public domain)
        self.assertFalse(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_known_author_after_public_domain(self):
        """Test Case 5: Non-anonymous author, EEA origin, author dies 1940, published 2020"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [
                    {"identity_known": True, "country_of_origin": "FR"}  # Known, EEA
                ],
                "author_death_year": self.current_year - 85,  # Died 85 years ago (1940)
                "first_publication_year": self.current_year
                - 5,  # Published 5 years ago (2020)
            }
        )
        results = run_copyright(data)

        # Should have first edition protection (YELLOW)
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain in 2010)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_first_available_than_published(self):
        """Test Case 6: Non-anonymous author, EEA origin, author dies 1905, first available 1990, published 2010"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [
                    {"identity_known": True, "country_of_origin": "FR"}  # Known, EEA
                ],
                "author_death_year": self.current_year
                - 120,  # Died 100 years ago (1905)
                "internet_first_available": "made_available_internet",
                "first_available_year": self.current_year
                - 30,  # First available 30 years ago (1990)
                "first_publication_year": self.current_year
                - 15,  # Published 15 years ago (2010)
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection (published before entering public domain)
        self.assertFalse(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_first_available_not_permanent(self):
        """Test Case 7: Non-anonymous author, EEA origin, author dies 1905, first available 2010 but no-download"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [
                    {"identity_known": True, "country_of_origin": "FR"}  # Known, EEA
                ],
                "author_death_year": self.current_year
                - 120,  # Died 100 years ago (1905)
                "internet_first_available": "not_made_available_internet",
                "first_available_year": self.current_year
                - 15,  # First available 15 years ago (2010)
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection (not made available with a possibility to download)
        self.assertFalse(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_first_available_to_download(self):
        """Test Case 8: Non-anonymous author, EEA origin, author dies 1905, first available 2010 and download possible"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "authors": [
                    {"identity_known": True, "country_of_origin": "FR"}  # Known, EEA
                ],
                "author_death_year": self.current_year
                - 120,  # Died 100 years ago (1905)
                "internet_first_available": "made_available_internet",
                "first_available_year": self.current_year
                - 15,  # First available 15 years ago (2010)
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection (not made available with a possibility to download)
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should be GREEN (entered public domain)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRightsLapsedArticle1Sec1-2"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_no_publication(self):
        """Test that first edition protection is not applied when no publication year is given"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "physically_published": "not_published_on_physical_medium",
                "otherwise_available": "not_made_available_no_medium"
                # No first_publication_year
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection
        self.assertFalse(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should still be GREEN
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_no_publication_year(self):
        """Test that first edition protection is not applied when no publication year is given"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "physically_published": "published_on_physical_medium",
                # No first_publication_year
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )
        # Copyright should still be GREEN
        self.assertTrue(
            any(
                r["condition"] == "CopyrightPublicDomainRuleOfThumb"
                for r in results["copyright_status"]["green"]
            )
        )

    def test_first_edition_protection_edge_case_25_years(self):
        """Test edge case where publication was exactly 25 years ago"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "first_publication_year": self.current_year
                - 25,  # Exactly 25 years ago
            }
        )
        results = run_copyright(data)

        # Should have first edition protection (YELLOW) - exactly 25 years
        self.assertTrue(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )

    def test_first_edition_protection_edge_case_26_years(self):
        """Test edge case where publication was 26 years ago"""
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "made_before_1850",
                "first_publication_year": self.current_year - 26,  # 26 years ago
            }
        )
        results = run_copyright(data)

        # Should NOT have first edition protection (protection lapsed)
        self.assertFalse(
            any(
                r["condition"] == "FirstEditionProtection"
                for r in results["first_edition_status"]["yellow"]
            )
        )

    def test_online_availability_status(self):
        """Test online availability status modifications"""
        # Base case: Work under copyright (RED status)
        data = base_data()
        data["copyright_info"].update(
            {
                "is_copyright_work": "work",
                "created_before_1850": "not_made_before_1850",
                "author_alive": "author_alive",
                "authors": [{"identity_known": True, "country_of_origin": "AT"}],
                "physically_published": "published_on_physical_medium",  # to avoid issues with first editions
                "first_publication_year": self.current_year
                - 35,  # to avoid issues with first editions
            }
        )

        # Test 1: Rights assignment upgrades RED to GREEN
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "rights_assignment"

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_green"]
            )
        )

        # Test 2: License agreement upgrades RED to GREEN
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "license_agreement"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_green"]
            )
        )

        # Test 3: Orphan works upgrades RED to YELLOW
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "orphan_works"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )

        # Test 4: Not applicable doesn't change status
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "not_applicable"
        results = run_copyright(data)

        self.assertFalse(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_green"]
            )
        )
        self.assertTrue(
            len(results["copyright_status"]["red"]) > 0
        )  # Original RED status remains

        # Test 5: Unknown doesn't change status
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "unknown"
        results = run_copyright(data)

        self.assertFalse(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_green"]
            )
        )
        self.assertTrue(
            len(results["copyright_status"]["red"]) > 0
        )  # Original RED status remains

        # Test 6: Out of commerce upgrades RED to YELLOW
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "out_of_commerce"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )

        # Test 7: No doesn't change status
        data = data.copy()
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "no"
        results = run_copyright(data)

        self.assertFalse(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_green"]
            )
        )
        self.assertTrue(
            len(results["copyright_status"]["red"]) > 0
        )  # Original RED status remains

    def test_cc_license_status(self):
        """Test CC license status modifications"""
        # Base case: Work under copyright (RED status)
        initial_data = base_data()

        # Test 1: CC0 upgrades RED to GREEN
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "cc0"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_green"]
            )
        )

        # Test 2: CC-BY upgrades RED to GREEN
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "cc_by"
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_green"]
            )
        )

        # Test 3: CC-BY-SA upgrades RED to YELLOW
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "cc_by_sa"

        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )

        # Test 4: CC-BY-NC-SA upgrades RED to YELLOW
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "cc_by_nc_sa"
        results = run_copyright(data)
        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )

        # Test 5: CC-BY-ND upgrades RED to YELLOW
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "cc_by_nd"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )

        # Test 6: CC-BY-NC-ND upgrades RED to YELLOW
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "cc_by_nc_nd"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )

        # Test 7: Not applicable doesn't change status
        data = initial_data.copy()
        data["copyright_info"]["object_cc_license"] = "not_applicable"
        data["copyright_info"].update({"author_alive": "author_alive"})
        results = run_copyright(data)

        self.assertFalse(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_green"]
            )
        )
        self.assertTrue(
            len(results["copyright_status"]["red"]) > 0
        )  # Original RED status remains

        # Test 8: CC status is applied before online availability
        data = initial_data.copy()
        data["copyright_info"].update({"author_alive": "author_alive"})
        data["copyright_info"][
            "object_cc_license"
        ] = "cc_by_sa"  # Should make it YELLOW
        data["copyright_info"][
            "object_copyright_rights_acquired_to_make_available"
        ] = "license_agreement"  # Should then make it GREEN
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectOnlineAvailable"
                for r in results["copyright_status"]["rights_green"]
            )
        )

        # Test 9: Other open license upgrades RED to YELLOW
        data = initial_data.copy()
        data["copyright_info"].update({"author_alive": "author_alive"})
        data["copyright_info"]["object_cc_license"] = "other_open"
        results = run_copyright(data)

        self.assertTrue(
            any(
                r["condition"] == "CopyrightObjectAvailableCCLicense"
                for r in results["copyright_status"]["rights_yellow"]
            )
        )


if __name__ == "__main__":
    unittest.main()
