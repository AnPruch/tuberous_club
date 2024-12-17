"""
Tokening data for the bot.
"""


class Token:
    """
    Token class
    """
    def __init__(self) -> None:
        """
        Initialization
        """
        self.token = '7604474051:AAErnNbDz427QWCrT4IBl039aCebdZx17fM'  # input your token string
        self.name = 'hsetuberous_bot'

    def get_token(self) -> str:
        """
        Get token
        """
        return self.token


TOKEN = Token().get_token()
print(TOKEN)
