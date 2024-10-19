"""
Tokening data for the bot.
"""


class Token:
    def __init__(self) -> None:
        self.token = '7604474051:AAErnNbDz427QWCrT4IBl039aCebdZx17fM'
        self.name = 'hsetuberous_bot'

    def get_token(self) -> str:
        return self.token


if __name__ == '__main__':
    token = Token().get_token()
    print(token)
