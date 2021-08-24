import streamlit as st
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch
import time as t


tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium') # import of DialoGPT
model = AutoModelWithLMHead.from_pretrained('Output Film + Livre') # import of the results of the training for the movies, interviewsand books datasets merged together

st.sidebar.title("Fine Tuning of the DialoGPT for french language. \n This version is based on a dataset based on movies subtitiles and interviews."
                 "\n The chatbot may take 30 secs before responding.\n The model handles a conversation of 4 rounds. ")
st.title("""   French DialoGPT bot
""")

def get_text(step):
    input_text = st.text_input("You (turn " + str(step +1) +"): " )
    # Streamlit is not built to host chatbots and is not dynamic thus there is a need for stopping the process when the user did not write his/her answer
    if not input_text:
        st.warning('Please input a sentence, the bot will answer quickly.')
        st.stop()
    return input_text

for step in range(4):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    user_input = get_text(step)

    new_user_input_ids = tokenizer.encode(user_input+ tokenizer.eos_token, return_tensors='pt')
    # print(new_user_input_ids)

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens,
    chat_history_ids = model.generate(
        bot_input_ids, max_length=3000,
        pad_token_id=tokenizer.eos_token_id,
        top_p=0.92, top_k=75
    )
    st.text_area("Bot :", value=tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True), height=80, max_chars=None, key=None)
    # pretty print last ouput tokens from bot