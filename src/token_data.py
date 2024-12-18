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
        self.token = ''   # input your token string
        self.name = 'hsetuberous_bot'

    def get_token(self) -> str:
        """
        Get token
        """
        return self.token


TOKEN = Token().get_token()
print(TOKEN)
