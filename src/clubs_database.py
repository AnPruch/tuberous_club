"""
Database structure classes.
"""
from typing import Any

import psycopg2
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class Club:
    """
    Club class.
    """
    def __init__(self, name: str, info: tuple[str, str]) -> None:
        """
        Bot initialization.

        Args:
            name (str): name
            info (str): info
        """
        self.name = name
        self.info = info

    def get_info(self) -> str:
        """
        Get info about club.
        """
        return f"{self.name} \n\n{self.info[1]}\n \n \n " \
               f"Подробнее о клубе можешь узнать здесь: \n{self.info[0]}"


class Category:
    """
    Club category class.
    """
    def __init__(self, name: str, clubs: list) -> None:
        """
        Bot initialization

        Args:
            name (str): name
            clubs (list): club list
        """
        self.name = name
        self.clubs = clubs

    def get_club_buttons(self) -> InlineKeyboardMarkup:
        """
        Get club buttons
        """
        markup = InlineKeyboardMarkup()
        row = []
        for club in self.clubs:
            row.append(InlineKeyboardButton(club.name, callback_data=f'club_{club.name}'))

            if len(row) == 2:
                markup.add(*row)
                row = []
        if row:
            markup.add(*row)

        return markup


class Database:
    """
    Database Class.
    """
    def __init__(self, db_name: str, user: str, password: str,
                 host: str, port: str) -> None:
        """
        Initialization of Database class.

        Args:
            db_name (str): Database name
            user (str): Username
            password (str): Database password
            host (str): Database host
            port (str): Database port
        """
        self.connection = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def get_categories(self) -> list | Any:
        """
        Get list of categories.

        Returns:
            list: Club categories
        """
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()

    def get_clubs_by_category(self, category_id: int) -> list | Any:
        """
        Get clubs by category.

        Args:
            category_id (int): ID of category
        Returns:
            list: Clubs
        """
        self.cursor.execute("SELECT name, link, description FROM clubs WHERE category_id = %s",
                            (category_id,))
        return self.cursor.fetchall()

    def load_data(self) -> list:
        """
        Load database info.

        Returns:
            list: Club categories
        """
        categories_data = self.get_categories()
        categories = []
        for category_id, category_name in categories_data:
            clubs_info = self.get_clubs_by_category(category_id)
            clubs = [Club(name, (link, description)) for name, link, description in clubs_info]
            categories.append(Category(category_name, clubs))
        return categories

    def close(self) -> None:
        """
        Close cursor and database.
        """
        self.cursor.close()
        self.connection.close()
