"""
DataLoader Tests.
"""
import unittest
from pathlib import Path

from src.data_loader import DataLoader


class DataLoaderTest(unittest.TestCase):
    """
    DataLoaderTest class functionality.
    """
    def setUp(self) -> None:
        """
        Setup method.
        """
        self.loader_path = Path(__file__).parent / 'loader_test_example.json'
        self.loader = DataLoader(self.loader_path)

    def test_fields(self) -> None:
        """
        Test DataLoader instance fields.
        """
        self.assertEqual(self.loader.questions_path, self.loader_path)

        self.assertIsInstance(self.loader.additional_questions, str)

        self.assertEqual(self.loader.additional_questions, '')

    def test_load_questions_return_value(self) -> None:
        """
        Check return value.
        """
        self.loader.load_questions()

        self.assertIsInstance(self.loader.additional_questions, str)

    def test_load_questions_ideal(self) -> None:
        """
        Ideal scenario.
        """
        self.loader.load_questions()
        expected = "<b>Вопрос</b>\n\t— Ответ\n\n<b>Question</b>\n\t— Answer"
        self.assertEqual(expected, self.loader.additional_questions)

    def test_load_questions_bad_input(self) -> None:
        """
        Bad input scenario.
        """
        bad_inputs = [[], 6]
        bad_path_inputs = ['', 'src', 'questions.txt', 'unknown.json']

        for bad_input in bad_inputs:
            loader = DataLoader(bad_input)  # type: ignore
            self.assertRaises(TypeError, loader.load_questions)

        for bad_input in bad_path_inputs:
            loader = DataLoader(bad_input)
            self.assertRaises(FileNotFoundError, loader.load_questions)
