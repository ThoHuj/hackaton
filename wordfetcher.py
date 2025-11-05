import requests

#word_url = requests.get("https://random-word-api.herokuapp.com/word?length=5")
#dictionary_url = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/")

class WordFetcher():
    def __init__(self, word_length: int, word_amount: int):
        self.word_length = word_length
        self.word_amount = word_amount

    def return_word(self) -> list[str]:
        return requests.get(url=f"https://random-word-api.herokuapp.com/word?length={self.word_length}&number={self.word_amount}").json()
