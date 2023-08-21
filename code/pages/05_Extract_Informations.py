import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper
import regex as re
import os
from random import randint

def clear_chat_data():
    st.session_state['chat_history'] = []
    st.session_state['chat_source_documents'] = []
    st.session_state['chat_askedquestion'] = ''
    st.session_state['chat_question'] = ''
    st.session_state['chat_followup_questions'] = []
    answer_with_citations = ""

def questionAsked():
    st.session_state.chat_askedquestion = st.session_state["input"+str(st.session_state ['input_message_key'])]
    st.session_state.chat_question = st.session_state.chat_askedquestion

# Callback to assign the follow-up question is selected by the user
def ask_followup_question(followup_question):
    st.session_state.chat_askedquestion = followup_question
    st.session_state['input_message_key'] = st.session_state['input_message_key'] + 1

try :
    # Initialize chat history
    if 'chat_question' not in st.session_state:
            st.session_state['chat_question'] = ''
    if 'chat_askedquestion' not in st.session_state:
        st.session_state.chat_askedquestion = ''
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if 'chat_source_documents' not in st.session_state:
        st.session_state['chat_source_documents'] = []
    if 'chat_followup_questions' not in st.session_state:
        st.session_state['chat_followup_questions'] = []
    if 'input_message_key' not in st.session_state:
        st.session_state ['input_message_key'] = 1

    llm_helper = LLMHelper()

    # Input questions
    input_text1 = st.text_input("You: ", placeholder="type your question", value=st.session_state.chat_askedquestion, key="input"+str(st.session_state ['input_message_key']), on_change=questionAsked)
    input_text2 = st.text_input("You: ", placeholder="type your question", value=st.session_state.chat_askedquestion, key="input"+str(st.session_state ['input_message_key']), on_change=questionAsked)
    input_text3 = st.text_input("You: ", placeholder="type your question", value=st.session_state.chat_askedquestion, key="input"+str(st.session_state ['input_message_key']), on_change=questionAsked)
    input_text4 = st.text_input("You: ", placeholder="type your question", value=st.session_state.chat_askedquestion, key="input"+str(st.session_state ['input_message_key']), on_change=questionAsked)
    input_text5 = st.text_input("You: ", placeholder="type your question", value=st.session_state.chat_askedquestion, key="input"+str(st.session_state ['input_message_key']), on_change=questionAsked)
    
    queries= [input_text1,input_text2,input_text3,input_text4,input_text5]
    if st.button('Start information extraction'):
        llm_helper.get_tender_information(queries)

    # If a question is asked execute the request to get the result, context, sources
    if st.session_state.chat_askedquestion:
        st.session_state['chat_question'] = st.session_state.chat_askedquestion
        st.session_state.chat_askedquestion = ""
        st.session_state['chat_question'], result, context, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['chat_question'], st.session_state['chat_history'])    
        result, chat_followup_questions_list = llm_helper.extract_followupquestions(result)
        st.session_state['chat_history'].append((st.session_state['chat_question'], result))
        st.session_state['chat_source_documents'].append(sources)


    # Displays the chat history
    if st.session_state['chat_history']:
        history_range = range(len(st.session_state['chat_history'])-1, -1, -1)
        for i in range(len(st.session_state['chat_history'])-1, -1, -1):

            # This history entry is the latest one - also show follow-up questions, buttons to access source(s) context(s) 
            if i == history_range.start:
                answer_with_citations, sourceList, matchedSourcesList, linkList, filenameList = llm_helper.get_links_filenames(st.session_state['chat_history'][i][1], st.session_state['chat_source_documents'][i])
                st.session_state['chat_history'][i] = st.session_state['chat_history'][i][:1] + (answer_with_citations,)

                answer_with_citations = re.sub(r'\$\^\{(.*?)\}\$', r'(\1)', st.session_state['chat_history'][i][1]).strip() # message() does not get Latex nor html

                # Display proposed follow-up questions which can be clicked on to ask that question automatically
                if len(st.session_state['chat_followup_questions']) > 0:
                    st.markdown('**Proposed follow-up questions:**')
                with st.container():
                    for questionId, followup_question in enumerate(st.session_state['chat_followup_questions']):
                        if followup_question:
                            str_followup_question = re.sub(r"(^|[^\\\\])'", r"\1\\'", followup_question)
                            st.button(str_followup_question, key=randint(1000,99999), on_click=ask_followup_question, args=(followup_question, ))
                    
                for questionId, followup_question in enumerate(st.session_state['chat_followup_questions']):
                    if followup_question:
                        str_followup_question = re.sub(r"(^|[^\\\\])'", r"\1\\'", followup_question)

            answer_with_citations = re.sub(r'\$\^\{(.*?)\}\$', r'(\1)', st.session_state['chat_history'][i][1]) # message() does not get Latex nor html
           # message(answer_with_citations ,key=str(i)+'answers', avatar_style=ai_avatar_style, seed=ai_seed)
            st.markdown(f'\n\nSources: {st.session_state["chat_source_documents"][i]}')
            #message(st.session_state['chat_history'][i][0], is_user=True, key=str(i)+'user' + '_user', avatar_style=user_avatar_style, seed=user_seed)

except Exception:
    st.error()
    
