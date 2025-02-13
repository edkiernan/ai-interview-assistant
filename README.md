# ai-interview-assistant
The tool I built to assist with my interview was a python script which records a response from a question I, the interviewer, ask and based on the transcribed response and context of the previous question provides the most relevant follow up question. This follow up question is determined based on a branching tree of categories and subcategories leading to specific questions, which were created with fleshing out this project's Problem Statement in mind. The goal of this tool is to allow myself to be fully engaged and participating in the interview in order to get the best responses from the interviewee, while I allow an AI assistant to parse through pre-prepared potential follow up questions. Ideally this tool works in such a manner that I engage with a single question and that question's response at time, prodding at small details in the response for clarification, while the mental labor, awkwardness, and distraction of looking through a script for pre-prepared questions is passed off to an assistant. 

I utilized OpenAI’s chat-gpt-4o-mini model via an API to suggest the follow up question based on a given response and list of pre-prepared questions, as well as Google's transcription found through the Python Speech Recognition library. 


## Questions
See the file [get_ai_response.py](get_ai_response.py) to get an exact look at the logic and tree structure of this tool. Below is the opening question and follow-up tree in bulleted format.

Opening Question
* "What is a piece of technology that you use in your daily life that you don't like / you don't feel comfortable using? This piece of technology can be used in your personal life, work, etc."

Follow-up Tree: 
* "general_dislike"
    * "initial"
        * "What about this technology makes it difficult for you?"
        * "Did your dislike develop as you learned more about the technology, or was it frustrating from the start?"
        * "How does this technology compare to similar alternatives?"
    * "reasons"
        * "Is it due to usability, security, or another factor?"
        * "Do you think the issue is with the design or how the tech was implemented?"
    * "impact"
        * "How has this technology affected your work or daily life?"
        * "Have you found any workarounds to make it more bearable?"
* "improvements"
    * "features"
        * "What features would improve your experience with the technology?"
        * "If you could redesign this technology, what would you change? Functionality changes? Visual changes?"
    * "alternatives"
        * "Are there existing technologies that solve these problems better?"
        * "What elements from other technologies would you incorporate into this one?"
* "learning_experience"
    * "methods"
        * "How do you feel when learning to use new technology? Excited, anxious, something else?"
        * "What methods help you learn new technology the best? Hands on experimentation, watching someone else use the tech first, etc?"
    * "frustrations"
        * "What aspects of learning new technology frustrates you the most?"
        * "Have you ever given up on learning a technology due to its complexity?"
    * "preferences"
        * "What role does documentation play in your learning process?"
        * "What is a reasonable time / energy commitment to learning a new technology that makes a daily task easier / more efficient?
* "goals"
    * "functional_goals"
        * "What do you hope to be able to accomplish?"
        * "What's not working, if anything?"
    * "formal_goals"
        * "What needs to exist that doesn't currently exist with the technology?"
    * "economic_goals": 
        * "What would you spend on this technology?"
    * "time_based_goals"
        * "Is there something that takes too much time?"
        * "Is there something that happens too quickly, is not thorough enough?"