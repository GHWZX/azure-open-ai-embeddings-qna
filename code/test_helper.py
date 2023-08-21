from utilities.helper import LLMHelper

def test_get_tender_information():
    llm_helper = LLMHelper()
    input_text1 = "What is the tender reference code?"
    input_text2= "What is the submission due date?"
    input_text3= "What is the contractor institutes and their codes?"
    input_text4= "Which products are part of this tender?"
    queries= [input_text1,input_text2,input_text3,input_text4]
    
    llm_helper.get_tender_information(queries)
    
if __name__ == '__main__':
    test_get_tender_information()