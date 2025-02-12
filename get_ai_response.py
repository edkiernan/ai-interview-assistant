import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Define beginning question
beginning_question = "What is a piece of technology that you don't like and that you don't feel comfortable using? "

# Define structured follow-up questions with deeper branching
followup_groups = {
    "general_dislike": {
        "initial": [
            "What about this technology makes it difficult for you?",
            "Did your dislike develop over time, or was it frustrating from the start?",
            "How does this technology compare to alternatives?"
        ],
        "reasons": [
            "Is it due to usability, security, or another factor?",
            "Do you think the issue is with the design or with how it is implemented?"
        ],
        "impact": [
            "How has this technology affected your work or daily life?",
            "Have you found any workarounds to make it more bearable?"
        ]
    },
    "improvements": {
        "features": [
            "What features would improve your experience?",
            "If you could redesign this technology, what would you change?"
        ],
        "alternatives": [
            "Are there existing technologies that solve these problems better?",
            "What elements from other technologies would you incorporate into this one?"
        ]
    },
    "learning_experience": {
        "methods": [
            "How do you feel when learning to use new technology?",
            "What methods help you learn new technology the best?"
        ],
        "frustrations": [
            "What aspects of learning new technology frustrate you the most?",
            "Have you ever given up on learning a technology due to its complexity?"
        ],
        "preferences": [
            "Do you prefer step-by-step guidance or hands-on experimentation?",
            "What role does documentation play in your learning process?"
        ]
    },
    "goals": {
        "functional_goals": [
            "What do you hope to be able to accomplish?",
            "What's not working, if anything?"
        ],
        "formal_goals": [
            "What form should the solution take? Option? Setting? Control?",
            "What needs to exist that doesn't currently exist?"
        ],
        "economic_goals": [
            "What would they spend?",
            "How much is this worth?"
        ],
        "time_based_goals": [
            "Is there something that takes too much time?",
            "Is there something that happens too quickly or with not enough steps?"
        ]
    },
    "facts": {
        "functional_facts": [
            "What's there now?",
            "What solutions exist that might apply?"
        ],
        "formal_facts": [
            "What form does it currently take?",
            "What are the possibilities?"
        ],
        "economic_facts": [
            "What's the current cost?",
            "What are the current expenses?"
        ],
        "time_based_facts": [
            "How long does it take now?",
            "When does it happen?",
            "What are the factors that determine how long it takes?"
        ]
    },
    "concepts": {
        "functional_concepts": [
            "How do they think it should work?",
            "What solutions should be implemented?"
        ],
        "formal_concepts": [
            "What do they think it should look like?",
            "Where should the solution live?"
        ],
        "economic_concepts": [
            "How much do they think it should cost?",
            "How do they perceive the value?"
        ],
        "time_based_concepts": [
            "How much time should it take?",
            "When should it happen?"
        ]
    }
}


def determine_followup_category(response_text, previous_question):
    """Uses AI to determine the most relevant follow-up category based on the response."""
    prompt = (
        "An interviewer is asking about someone's experience with technology. "
        f"The previous question was: '{previous_question}'\n"
        f"The interviewee responded: '{response_text}'\n"
        "Which category of follow-up questions is most relevant: general_dislike, improvements, or learning_experience? "
        "Just return the category name as plain text."
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
        category = response.choices[0].message.content.strip()
        return category if category in followup_groups else "general_dislike"
    except Exception as e:
        print("API Request failed:", e)
        return "general_dislike"

def get_best_followup(response_text, previous_question):
    """Selects the best follow-up question from the chosen category."""
    category = determine_followup_category(response_text, previous_question)
    subcategories = list(followup_groups[category].keys())
    
    prompt = (
        "Based on the following response, select the best follow-up question.\n"
        f"Response: '{response_text}'\n"
        "Possible follow-up questions:\n"
        + "\n".join([f"- {q}" for subcat in subcategories for q in followup_groups[category][subcat]]) + "\n"
        "Just return the best follow-up question as plain text."
    )
    
    try:
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            #model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("API Request failed:", e)
        return followup_groups[category][subcategories[0]][0]

if __name__ == "__main__":
    previous_question = beginning_question
    #response_text_1 = "I struggle with using touch-screen keyboards efficiently."
    response_text_2 = "The online gradebook system I use as a teacher is difficult to use at it is very buggy and overall confusing."
    best_followup = get_best_followup(response_text_2, previous_question)
    print("Follow-up question:", best_followup)


