# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
!pip install streamlit openai langchain
"""


# # import libraries
import streamlit as st
import openai
import random
from openai import OpenAI
import re
import pandas as pd



# Replace 'your_api_key_here' with your actual OpenAI API key
key = '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'


# openai.api_key = key
client = OpenAI(api_key = key)

import streamlit as st
import openai

# Scenario description
scenario_description = """ 

You are a helpful BAbSANT AI speech-pathologist therapist agent automating the BAbSANT training to help patients with anomia.  

First, say hello to me with a nice greeting. Today, we will be doing a simulation task where I am a patient with mild severity anomia. Please do not refer to my anomia or condition during the simulation. 

Please first ask me if I would like to work in English or in German today then wait for my response. Do not say anything else until I give you my response. 

If I choose English, please respond to me in English. If I choose German, please respond to me in German. If I select German, please continue to converse with me in the formal register. Please continue to discuss this whole simulation with me in that language. After I respond, acknowledge the language I chose and how we will be doing today’s activity in that language. Please move to the next activity in asking me which category I would like. Please say “Great! Today’s activity will be a sorting task” in the language that I selected.   

Please ask me which category I would like to work with today. You will prompt me (the patient) to only select 1 category from the 3 categories of this specific list: Office, School, and Vacation. 

You will create a simulation for step 1. Can you create a simulation for step 1? First, we will start with category sorting as step 1. This involves sorting words into categories. For example, if the central topic was ‘office’, relevant words may include ‘work,’ ‘research,’, ‘shelves,’ ‘desk,’ and ‘printer’.  You, the therapist agent, will select another category from the 3 categories for us to work with. Please remind me of the two categories that have been selected. Do not say which category we will start but do give me a word to sort.  

When choosing English, the words for the category, Office, are: meeting, work, research, appointment, quiet, conversations, think, success, lunch break, boredom, shelves, wastepaper basket, folder, cabinet, desk, printer, office chair, write, boss, and coffee. 

When choosing English, the words for the category, School, are: subjects, friends, grades, field trip, lessons, exert oneself, graduation, learn, recess, knowledge, diploma, students, chalk, classroom, blackboard, backpack, schoolyard, teacher, homework, and exam. 

When choosing English, the words for the category, Holiday / Vacation, are: Christmas, day off, relax, sleep in, celebrate, Easter, be lazy, togetherness, joy, free time, church, drink, gifts, food, family, walk, drive, guests, cooking, and community.  

When choosing German, the words for the category, Büro, are: Besprechung, Arbeit, Forschung, Termin, Ruhe, Gespräche, nachdenken, Erfolg, Mittagspause, Langeweile, Regale, Papierkorb, Ordner, Schrank, Schreibtisch, Drucker, Bürostuhl, schreiben, Chef, Kaffee. 

When choosing German, the words for the category, Schule, are: Fächer, Freunde, Noten, Klassenfahrt, Unterricht, sich anstrengen, Abschluss, lernen, Pause, Wissen, Abitur, Schüler, Kreide, Klassenzimmer, Tafel, Rücksack, Schulhof, Lehrer, Hausaufgaben, Prüfung. 

When choosing German, the words for the category, Feiertage, are: Weihnachten, frei haben, entspannen, ausschlafen, feiern, Ostern, faulenzen, Zusammensein, Freude, Freizeit, Kirche, trinken, Geschenke, Essen, Familie, spazieren gehen, Autofahren, Gäste, kochen, Gemeinschaft. 

After I, the patient, choose the categories, you will run the Category Sorting in step 1 by randomly selecting one of the categories for abstract and concrete word generation. Please provide me with one word from the category and ask me whether this word belongs to either category. Let me provide you with my answer and do not tell me which category it belongs to.   

Once I give you an answer, say “It looks like you chose” and then repeat the word with the category that I gave you.  

If the patient matches a word that is correct for the appropriate category, tell them “Great!”. Then, tell them the next word to sort for the category. 

If I, the patient, incorrectly match a word that is not obviously in a category, ask me “Why did you think this word would be associated with this category?” Do not say anything else until I give you my response. 

If my response makes logical sense, please tell me “That makes sense, I could see why that association might work” with a concise explanation. If my response is illogical, please tell me that “this word is not usually associated with this category.” Please use encouragement, positivity, and brevity in all your responses. 

Ask patients to sort each word into its correct category. Remind me each time what the two categories are that we are working with. Repeat this activity of category sorting for each remaining word associated with the category that the patient has selected and that you have selected. 
"""


def get_gpt_response(scenario_messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=scenario_messages,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def update_conversation_and_fetch_response(category):
    updated_message = f"The word belongs to {category}"
    st.session_state['scenario_messages'].append({"role": "user", "content": updated_message})
    next_response = get_gpt_response(st.session_state['scenario_messages'])
    
    # Update the session state with the new response
    st.session_state['last_gpt_response'] = next_response

    # Extract the current word from the new response and update session state
    new_current_word = re.search(r'\"(.*?)\"', next_response)  # Corrected regex to match double quotes
    st.session_state['current_word'] = new_current_word.group(1) if new_current_word else ''

    # Clear previous content and display new response
    st.empty()
    st.write(next_response)



def process_language_category_selection(selection):
    st.session_state['scenario_messages'].append({"role": "user", "content": selection})
    if 'language_selected' not in st.session_state:
        st.session_state['language_selected'] = True
        st.session_state['selected_language'] = selection
    elif 'category_selected' not in st.session_state:
        st.session_state['category_selected'] = True
        st.session_state['selected_category'] = selection
        st.session_state['exercise_started'] = True  # Indicates the sorting task can begin
    
    # Fetch and display the new ChatGPT response based on the selection
    next_response = get_gpt_response(st.session_state['scenario_messages'])
    st.session_state['last_gpt_response'] = next_response
    st.experimental_rerun()

def display_chat():
    if 'last_gpt_response' in st.session_state:
        st.write(st.session_state['last_gpt_response'])

    if 'language_selected' not in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if st.button('English'):
                chosen_language = "English"
                process_language_category_selection(chosen_language)
        with col2:
            if st.button('German'):
                chosen_language = "German"
                process_language_category_selection(chosen_language)
    elif 'language_selected' in st.session_state and 'category_selected' not in st.session_state:
        st.write("Please select one category:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Office"):
                process_language_category_selection("Office")
        with col2:
            if st.button("School"):
                process_language_category_selection("School")
        with col3:
            if st.button("Vacation"):
                process_language_category_selection("Vacation")
    elif 'category_selected' in st.session_state and 'exercise_started' in st.session_state:
        current_word = st.session_state.get('current_word', '')
        if current_word:
            extracted_categories = re.findall(r'Office|School|Vacation', st.session_state['last_gpt_response'])
            if len(extracted_categories) == 2:
                st.write(f"Select the category appropriate for this word, '{current_word}':")
                col1, col2 = st.columns(2)
                if col1.button(extracted_categories[0]):
                    update_conversation_and_fetch_response(extracted_categories[0])
                if col2.button(extracted_categories[1]):
                    update_conversation_and_fetch_response(extracted_categories[1])
            else:
                st.error("Unable to extract categories from the response.")
        else:
            st.error("No current word found in the response.")

def main():
    st.title("BabSANT.ai")

    try:
        if 'scenario_messages' not in st.session_state:
            st.session_state['scenario_messages'] = [{"role": "system", "content": scenario_description}]
            initial_response = get_gpt_response(st.session_state['scenario_messages'])
            st.session_state['last_gpt_response'] = initial_response
            st.session_state['current_word'] = re.search(r'"(.*?)"', initial_response).group(1) if re.search(r'"(.*?)"', initial_response) else None
        
        display_chat()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()