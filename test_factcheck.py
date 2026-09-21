import unittest
from app import normalize_date, normalize_name, values_match


class TestWikiFactCheck(unittest.TestCase):

    def test_birth_date_same(self):
        self.assertTrue(
            values_match(
                "Birth Date",
                "17 September 1950",
                "Narendra Modi was born on 17 September 1950 in Vadnagar."
            )
        )

    def test_birth_date_year_fallback(self):
        self.assertTrue(
            values_match(
                "Birth Date",
                "17 September 1950",
                "He was born in 1950."
            )
        )

    def test_founder_natural_sentence(self):
        self.assertTrue(
            values_match(
                "Founder",
                "Larry Page; Sergey Brin",
                "Google was founded by Larry Page and Sergey Brin."
            )
        )

    def test_founder_exact_phrase_not_required(self):
        self.assertTrue(
            values_match(
                "Founder",
                "Larry Page; Sergey Brin",
                "The company was created by Larry Page together with Sergey Brin."
            )
        )

    def test_founder_mismatch(self):
        self.assertFalse(
            values_match(
                "Founder",
                "Larry Page; Sergey Brin",
                "Google was founded by Steve Jobs and Bill Gates."
            )
        )

    def test_location_normalization(self):
        self.assertTrue(
            values_match(
                "Location",
                "Mountain View, California, U.S.",
                "The company is headquartered in Mountain View, California, U.S."
            )
        )

    def test_name_normalization(self):
        self.assertEqual(normalize_name("Larry Page (born 1973)"), "larry page")

    def test_date_normalization(self):
        self.assertEqual(normalize_date("17 September 1950"), "1950-09-17")


if __name__ == "__main__":
    unittest.main()
