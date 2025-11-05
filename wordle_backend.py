import streamlit as st
import pandas as pd
import random
from ollama import chat, ChatResponse

# --- Backend setup ---
words_database = pd.read_csv("word_data.csv")
WORD_LENGTH = 5  # assuming 5-letter words like Wordle
MAX_ATTEMPTS = 6

# --- Helper functions ---
def pick_random_word():
    return words_database.iloc[random.randint(0, len(words_database) - 1)][0].upper()

def check_guess(guess, correct):
    """Return list of color codes for a given guess."""
    result = []
    correct_letters = list(correct)
    guess_letters = list(guess)

    # First pass: greens
    for i in range(WORD_LENGTH):
        if guess_letters[i] == correct_letters[i]:
            result.append("🟩")
            correct_letters[i] = None
        else:
            result.append(None)

    # Second pass: yellows and grays
    for i in range(WORD_LENGTH):
        if result[i] is None:
            if guess_letters[i] in correct_letters:
                result[i] = "🟨"
                correct_letters[correct_letters.index(guess_letters[i])] = None
            else:
                result[i] = "⬜"
    return result


def render_grid(attempts):
    """Render the Wordle grid with colored squares."""
    for guess, feedback in attempts:
        cols = st.columns(WORD_LENGTH)
        for i in range(WORD_LENGTH):
            cols[i].markdown(
                f"<div style='text-align:center; font-size:32px;'>{feedback[i]}</div>",
                unsafe_allow_html=True,
            )

    # Empty rows
    for _ in range(MAX_ATTEMPTS - len(attempts)):
        cols = st.columns(WORD_LENGTH)
        for i in range(WORD_LENGTH):
            cols[i].markdown(
                "<div style='text-align:center; font-size:32px; color:gray;'>⬛</div>",
                unsafe_allow_html=True,
            )


# --- Streamlit App ---
st.set_page_config(page_title="Wordle Clone", layout="centered")

st.title("🟩 Wordle Clone 🎯")
st.caption("Guess the hidden word in six tries!")

# Initialize session state
if "attempts" not in st.session_state:
    st.session_state.attempts = []
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "correct_word" not in st.session_state:
    st.session_state.correct_word = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False


# --- Start game logic ---
if not st.session_state.game_started:
    if st.button("Start Game 🚀"):
        st.session_state.correct_word = pick_random_word()
        st.session_state.game_started = True
        st.session_state.attempts = []
        st.session_state.game_over = False
        st.rerun()
    st.info("Click 'Start Game' to begin 💅")
else:
    # Game in progress
    render_grid(st.session_state.attempts)

    if not st.session_state.game_over:
        with st.form("guess_form"):
            guess = st.text_input(
                "Enter your guess:",
                max_chars=WORD_LENGTH,
                placeholder=f"{WORD_LENGTH} letters",
            ).upper()
            submitted = st.form_submit_button("Submit")

            if submitted:
                if len(guess) != WORD_LENGTH:
                    st.warning(f"Your guess must be {WORD_LENGTH} letters long!")
                elif guess not in [w.upper() for w in words_database.iloc[:, 0]]:
                    st.warning("That word isn't in the list, darling 💅")
                else:
                    feedback = check_guess(guess, st.session_state.correct_word)
                    st.session_state.attempts.append((guess, feedback))

                    if guess == st.session_state.correct_word:
                        st.success(f"YAS QUEEN 💚 You guessed it! The word was {st.session_state.correct_word}.")
                        st.session_state.game_over = True
                    elif len(st.session_state.attempts) >= MAX_ATTEMPTS:
                        st.error(f"GAME OVER 💀 The correct word was {st.session_state.correct_word}.")
                        st.session_state.game_over = True

    if st.session_state.game_over:
        # Show definition using Ollama
        with st.spinner("Fetching word meaning..."):
            try:
                response: ChatResponse = chat(model='gemma3', messages=[
                    {
                        'role': 'user',
                        'content': f"Explain the meaning of the English word '{st.session_state.correct_word}' in one short paragraph.",
                    },
                ])
                definition = response.message.content
                st.info(f"📘 **Meaning of {st.session_state.correct_word}:**\n\n{definition}")
            except Exception as e:
                st.warning(f"Couldn't fetch word meaning: {e}")

        if st.button("Play Again 💫"):
            st.session_state.correct_word = pick_random_word()
            st.session_state.attempts = []
            st.session_state.game_over = False
            st.session_state.game_started = True
            st.rerun()


st.subheader(st.session_state.correct_word)