import requests
import random
import os

#word_url = requests.get("https://random-word-api.herokuapp.com/word?length=5")
#dictionary_url = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/")

class WordFetcher():
    def __init__(self, word_length: int, word_amount: int):
        self.word_length = word_length
        self.word_amount = word_amount

    def return_word(self) -> list[str]:
        return requests.get(url=f"https://random-word-api.herokuapp.com/word?length={self.word_length}&number={self.word_amount}").json()


# This class fetches word of the day from a Wordly api
class WordleGame:
    def __init__(self):
        # Get random 5 letter word
        self.word = requests.get(url="https://random-word-api.herokuapp.com/word?length=5").json()[0].lower()
        
        # Get word definition
        self.definition = self.get_definition()
        self.attempts = 6
        
    def get_definition(self):
        try:
            response = requests.get(url=f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.word}").json()
            return response[0]['meanings'][0]['definitions'][0]['definition']
        except:
            return "Definition not found"

    def play(self):
        print("Welcome to Wordle!")
        print(f"You have {self.attempts} attempts to guess the 5-letter word.")
        print("Hint - Definition:", self.definition)
        
        while self.attempts > 0:
            guess = input("\nEnter your guess: ").lower()
            
            if len(guess) != 5:
                print("Please enter a 5-letter word!")
                continue
                
            if guess == self.word:
                print("🎉 Congratulations! You won!")
                return
                
            # Show feedback
            feedback = ""
            for i in range(5):
                if guess[i] == self.word[i]:
                    feedback += "🟩"  # Correct letter, correct position
                elif guess[i] in self.word:
                    feedback += "🟨"  # Correct letter, wrong position
                else:
                    feedback += "⬜"  # Wrong letter
                    
            print(feedback)
            self.attempts -= 1
            print(f"Attempts remaining: {self.attempts}")
            
        print(f"\nGame Over! The word was: {self.word}")

if __name__ == "__main__":
    game = WordleGame()
    game.play()
    