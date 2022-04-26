"""Codejail plugin test"""
import unittest

from tutorcodejail.plugin import patches


class CodejailPluginTest(unittest.TestCase):
    """
    Test case for tutor codejail plugin.
    """

    def test_patches(self):
        """
        Test total patches for codejail plugin.

        Expected results:
            - Total patches expected from patches dir
        """
        expected_patches = [
            "cms-env",
            "lms-env",
            "local-docker-compose-dev-services",
            "local-docker-compose-jobs-services",
            "local-docker-compose-services",
        ]

        all_patches = patches()
        keys_patches = list(all_patches.keys())
        keys_patches.sort()

        self.assertEqual(keys_patches, expected_patches)
