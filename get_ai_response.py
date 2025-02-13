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
        "general": [
            "What about this technology makes it difficult for you?",
            "Did your dislike develop as you learned more about the technology, or was it frustrating from the start?",
            "How does this technology compare to similar alternatives?"
        ],
        "reasons": [
            "Is it due to usability, security, or another factor?",
            "Do you think the issue is with the design or how the tech was implemented?"
        ],
        "impact": [
            "How has this technology affected your work or daily life?",
            "Have you found any workarounds to make it more bearable?"
        ]
    },
    "improvements": {
        "general": [
            "What features would improve your experience with the technology?",
            "If you could redesign this technology, what would you change? Functionality changes? Visual changes?"
        ],
        "alternatives": [
            "Are there existing technologies that solve these problems better?",
            "What elements from other technologies would you incorporate into this one?"
        ]
    },
    "learning_experience": {
        "general": [
            "How do you feel when learning to use new technology? Excited, anxious, something else?",
            "What methods help you learn new technology the best? Hands-on experimentation, watching someone else use the tech first, etc?"
        ],
        "frustrations": [
            "What aspects of learning new technology frustrate you the most?",
            "Have you ever given up on learning a technology due to its complexity?"
        ],
        "preferences": [
            "What role does documentation play in your learning process?",
            "What is a reasonable time/energy commitment to learning a new technology that makes a daily task easier/more efficient?"
        ]
    },
    "goals": {
        "general": [
            "What do you hope to be able to accomplish?",
            "What's not working, if anything?"
        ],
        "formal_goals": [
            "What needs to exist that doesn't currently exist with the technology?"
        ],
        "economic_goals": [
            "What would you spend on this technology?"
        ],
        "time_based_goals": [
            "Is there something that takes too much time?",
            "Is there something that happens too quickly, is not thorough enough?"
        ]
    }
}

# Initialize remaining subcategories dictionary
remaining_subcategories = {category: set(followup_groups[category].keys()) for category in followup_groups}
remaining_categories = set(followup_groups.keys())

def determine_followup_category(response_text, previous_question):
    """Uses AI to determine the most relevant follow-up category based on the response."""
    available_categories = list(remaining_categories)
    
    prompt = (
        "An interviewer is asking about someone's experience with technology. "
        f"The previous question was: '{previous_question}'\n"
        f"The interviewee responded: '{response_text}'\n"
        f"Which category of follow-up questions is most relevant: {', '.join(available_categories)}? "
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
    
def determine_followup_subcategory(response_text, previous_question, category):
    """Uses AI to determine the most relevant follow-up subcategory based on the response."""
    available_subcategories = list(remaining_subcategories[category])
    
    if not available_subcategories:
        return "general"  # Fallback if all subcategories are used
    
    prompt = (
        "An interviewer is asking about someone's experience with technology. "
        f"The previous question was: '{previous_question}'\n"
        f"The interviewee responded: '{response_text}'\n"
        f"Which subcategory of follow-up questions is most relevant: {', '.join(available_subcategories)}? "
        "Just return the subcategory name as plain text."
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
        subcat = response.choices[0].message.content.strip()
        return subcat if subcat in remaining_subcategories[category] else "general"
    except Exception as e:
        print("API Request failed:", e)
        return "general"

def get_best_followup(response_text, previous_question):
    """Selects the best follow-up question from the chosen category and subcategory."""
    while(True):
        category = determine_followup_category(response_text, previous_question)
        
        # if category not in remaining_categories:
        #     print(f"All categories exhausted. Resetting categories.")
        #     remaining_categories.update(followup_groups.keys())

        subcat = determine_followup_subcategory(response_text, previous_question, category)
        
        if subcat not in remaining_subcategories[category]:  
            print("\n")
            print(f"{subcat} not in remaing subcategories for {category}")
            print(f"All subcategories exhausted for {category}. Removing category.")
            remaining_categories.remove(category)
            print("\n")
        else:
            break

    questions = followup_groups[category][subcat]
    
    prompt = (
        "Based on the following response, select the best follow-up question.\n"
        f"Response: '{response_text}'\n"
        "Possible follow-up questions:\n"
        + "\n".join([f"- {q}" for q in questions]) + "\n"
        "Just return the best follow-up question as plain text."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        best_question = response.choices[0].message.content.strip()
        
        # Remove the selected subcategory
        remaining_subcategories[category].remove(subcat)
        
        return best_question
    except Exception as e:
        print("API Request failed:", e)
        return questions[0]  # Fallback to first question if API fails

if __name__ == "__main__":
    previous_question = beginning_question
    response_text_1 = "The online gradebook system I use as a teacher is difficult to use as it is very buggy and overall confusing."
    response_text_2 = "Our project management software constantly crashes and makes collaboration frustrating instead of easier."  
    response_text_3 = "I find smart home assistants unreliable—sometimes they misunderstand commands, and other times they just don't respond at all."  
    response_text_4 = "The new POS system at work is incredibly slow, and the interface is cluttered with unnecessary options, making transactions take longer."  
    response_text_5 = "I struggle with using modern video conferencing tools because they often have hidden settings that make it hard to troubleshoot issues on the fly."  

    
    best_followup_1 = get_best_followup(response_text_1, previous_question)
    print("Follow-up question:", best_followup_1)
    best_followup_2 = get_best_followup(response_text_2, best_followup_1)
    print("Follow-up question:", best_followup_2)
    best_followup_3 = get_best_followup(response_text_3, best_followup_2)
    print("Follow-up question:", best_followup_3)
    best_followup_4 = get_best_followup(response_text_4, best_followup_3)
    print("Follow-up question:", best_followup_4)
    best_followup_5 = get_best_followup(response_text_5, best_followup_4)
    print("Follow-up question:", best_followup_5)
    