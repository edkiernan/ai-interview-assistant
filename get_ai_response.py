import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Define beginning question and possible follow-ups
beginning_question = '''What is a piece of technology that you don't like and that you don't feel comfortable using?
                        It can be a technology for work, school or personal use.'''

following_up_questions = [
    "What is a piece of technology you dislike and feel uncomfortable using, and what about it makes it difficult for you?",
    "Did your dislike for this technology develop over time, or did you find it frustrating from the start? What changed or reinforced your feelings?",
    "How does this technology compare to others that serve a similar purpose, and what aspects make it better or worse?",
    "What features or elements are missing from this technology that would improve your experience, and how would you design them?",
    "How do you feel when learning to use new technology, and what factors influence whether the experience is positive or negative for you?",
    "Can you describe the best technology youve ever used and what made it stand out to you?",
    "What is the worst technology youve ever used, and what specific challenges made it difficult or frustrating?",
    "When learning new technology, what methods help you the most, and why do they work well for you?",
    "What learning experiences have been the most frustrating for you when trying to use new technology, and what would have made them better?",
    "Do you prefer technology that gradually introduces features over time or one that lets you explore freely? How does this preference impact how you interact with new tools?"
]


def get_best_followup(response_text):
    prompt = (
        "For context, an interviewer is interviewing someone about their problems with technology.\n"
        f"The interviewer asked: '{beginning_question}'\n"
        f"The interviewee responded: '{response_text}'\n"
        "Here are three possible follow-up questions:\n"
        f"1. {following_up_questions[0]}\n"
        f"2. {following_up_questions[1]}\n"
        f"3. {following_up_questions[2]}\n"
        "Based on the response, which question would be the best follow-up? "
        "Just return the best follow-up question as plain text."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        best_question = response.choices[0].message.content.strip()
        return best_question
    except Exception as e:
        print("API Request failed:", e)
        return None

if __name__ == "__main__":
    response_text = "I love painting landscapes."
    best_followup = get_best_followup(response_text)
