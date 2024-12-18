"""
Token Class Tests.
"""
# pylint: disable=protected-access
import unittest

from src.token_data import Token


class TokenTest(unittest.TestCase):
    """
    TokenTest class functionality.
    """
    def test_fields(self) -> None:
        """
        Initialization test.
        """
        token = Token()
        self.assertIsInstance(token.name, str)
        self.assertIsInstance(token._token, str)

    def test_get_token(self) -> None:
        """
        Get_token method test.
        """
        token = Token()
        self.assertEqual(token._token, token.get_token())
