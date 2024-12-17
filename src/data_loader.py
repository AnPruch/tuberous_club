"""
Loading data
"""
import json
from pathlib import Path


class DataLoader:
    """
    DataLoader for additional questions from JSON file.
    """
    def __init__(self, questions_path: str) -> None:
        """
        Initialization of DataLoader.

        Args:
            questions_path (str): path to JSON file
        """
        self.questions_path = questions_path
        self.additional_questions = ""

    def check_path(self) -> None:
        if not isinstance(self.questions_path, str) \
                or not Path(self.questions_path).is_file()\
                or Path(self.questions_path).suffix != '.json':
            raise FileNotFoundError

    def load_questions(self) -> str:
        """
        Load questions.

        Returns:
            str: Information about other questions
        """
        self.check_path()

        with open(self.questions_path, encoding='utf-8', errors='ignore') as q:
            questions = json.load(q)

        self.additional_questions = '\n\n'.join(list((f'<b>{k}</b>\n\t— {v}'
                                                     for k, v in questions.items())))
        return self.additional_questions
