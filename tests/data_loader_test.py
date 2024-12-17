import unittest
from src.data_loader import DataLoader


class DataLoaderTest(unittest.TestCase):
    """
    DataLoaderTest class functionality.
    """
    def setUp(self) -> None:
        """
        Setup method.
        """
        self.loader_path = 'loader_test_example.json'
        self.loader = DataLoader(self.loader_path)

    def test_fields(self):
        self.assertEqual(self.loader.questions_path, self.loader_path)

        self.assertIsInstance(self.loader.additional_questions, str)

        self.assertEqual(self.loader.additional_questions, '')

    def test_load_questions_return_value(self):
        self.loader.load_questions()

        self.assertIsInstance(self.loader.additional_questions, str)

        expected = "<b>Вопрос</b>\n\t— Ответ\n\n<b>Question</b>\n\t— Answer"
        self.assertEqual(expected, self.loader.additional_questions)

    def test_load_questions_bad_input(self):
        bad_inputs = [[], '', 'src', 6, 'questions.txt', 'unknown.json']

        for input in bad_inputs:
            loader = DataLoader(input)
            self.assertRaises(FileNotFoundError, loader.load_questions)
