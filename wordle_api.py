# wordle_api.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import random
from ollama import chat, ChatResponse

app = FastAPI()

words_database = pd.read_csv("word_data.csv")
WORD_LENGTH = 5
MAX_ATTEMPTS = 6

def pick_random_word():
    return words_database.iloc[random.randint(0, len(words_database) - 1)][0].upper()

def check_guess(guess, correct):
    result = []
    correct_letters = list(correct)
    guess_letters = list(guess)

    for i in range(WORD_LENGTH):
        if guess_letters[i] == correct_letters[i]:
            result.append("🟩")
            correct_letters[i] = None
        else:
            result.append(None)

    for i in range(WORD_LENGTH):
        if result[i] is None:
            if guess_letters[i] in correct_letters:
                result[i] = "🟨"
                correct_letters[correct_letters.index(guess_letters[i])] = None
            else:
                result[i] = "⬜"
    return result


# --- Models ---
class GuessRequest(BaseModel):
    guess: str
    correct_word: str


# --- Routes ---
@app.get("/start")
def start_game():
    """Start a new game."""
    word = pick_random_word()
    return {"correct_word": word}

@app.post("/check")
def check_guess_api(request: GuessRequest):
    feedback = check_guess(request.guess.upper(), request.correct_word.upper())
    return {"feedback": feedback, "is_correct": request.guess.upper() == request.correct_word.upper()}

@app.get("/meaning/{word}")
def get_word_meaning(word: str):
    """Ask Ollama (Gemma3) to explain the word briefly."""
    try:
        response: ChatResponse = chat(model='gemma3', messages=[
            {
                'role': 'user',
                'content': f"Explain the meaning of the English word '{word}' in one short paragraph.",
            },
        ])
        return {"meaning": response.message.content}
    except Exception as e:
        return {"error": str(e)}