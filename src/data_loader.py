"""
Loading data
"""
import json
from pathlib import Path


class DataLoader:
    """
    DataLoader for additional questions from JSON file.
    """
    def __init__(self, questions_path: str | Path) -> None:
        """
        Initialization of DataLoader.

        Args:
            questions_path (str): path to JSON file
        """
        self.questions_path = questions_path
        self.additional_questions = ""

    def check_path(self) -> None:
        """
        Check path to JSON file.
        """
        if not isinstance(self.questions_path, (str, Path)):
            raise TypeError

        if isinstance(self.questions_path, str):
            self.questions_path = Path(self.questions_path)

        if not self.questions_path.exists() or self.questions_path.suffix != '.json':
            raise FileNotFoundError

    def load_questions(self) -> None:
        """
        Load questions.

        Returns:
            str: Information about other questions
        """
        self.check_path()

        with open(str(self.questions_path), encoding='utf-8') as q:
            questions = json.load(q)

        self.additional_questions = '\n\n'.join(list((f'<b>{k}</b>\n\t— {v}'
                                                     for k, v in questions.items())))
