"""
Clubs Database Classes Tests.
"""
import unittest

from src.clubs_database import Category, Club


class ClubTest(unittest.TestCase):
    """
    ClubTest class functionality.
    """
    def setUp(self) -> None:
        self.name = 'Club'
        self.info = ('<link>', 'Description.')
        self.club = Club(name=self.name,
                         info=self.info)

    def test_fields(self) -> None:
        """
        Initialization test.
        """
        self.assertEqual(self.club.name, self.name)
        self.assertEqual(self.club.info, self.info)

    def test_get_info_return_value(self) -> None:
        """
        Check return value.
        """
        self.assertIsInstance(self.club.get_info(), str)

    def test_get_info_ideal(self) -> None:
        """
        Ideal scenario.
        """
        expected = "Club \n\nDescription.\n \n \n Подробнее о клубе можешь узнать здесь: \n<link>"
        self.assertEqual(expected, self.club.get_info())

    def test_bad_input(self) -> None:
        """
        Bad input scenario.
        """
        bad_name_inputs = [[], 6, ]
        bad_info_inputs = [0, '', {}, (1,), ('one', 'two', 'three')]

        for bad_name in bad_name_inputs:
            with self.assertRaises(TypeError):
                Club(bad_name, self.info)  # type: ignore

        for bad_info in bad_info_inputs:
            with self.assertRaises(TypeError):
                Club(self.name, bad_info)  # type: ignore


class CategoryTest(unittest.TestCase):
    """
    CategoryTest class functionality.
    """
    def test_fields(self) -> None:
        """
        Initialization test.
        """
        name = 'Media'
        clubs = ['Club1', 'Club2']
        category = Category(name, clubs)
        self.assertEqual(category.name, name)
        self.assertEqual(category.clubs, clubs)

    def test_bad_input(self) -> None:
        """
        Bad input scenario.
        """
        name = 'Media'
        clubs = ['Club1', 'Club2']

        bad_name_inputs = [[], 6, (), {}]
        bad_clubs_inputs = [0, '', {}, ()]

        for bad_name in bad_name_inputs:
            with self.assertRaises(TypeError):
                Category(bad_name, clubs)  # type: ignore

        for bad_clubs in bad_clubs_inputs:
            with self.assertRaises(TypeError):
                Category(name, bad_clubs)  # type: ignore
