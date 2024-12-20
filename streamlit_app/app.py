import streamlit as st
import os

# TO ADD IN CONFIG
css_path = f"styles/styles.css"
student_name = 'Aarthy'
code_blossom_symbol = '🌸'

# Load the CSS
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        css_content = f.read()
        print(css_content)
else:
    print(f"{css_path} does not exist.")

# app
st.title(f"{code_blossom_symbol} Hello - {student_name}! {code_blossom_symbol}")
queries = st.text_area("Type here ")
if st.button("Ask Question"):
    with open("questions.txt", "a") as f:
        f.write(queries + "\n")
    st.success("Thank you for your question!")

# Goes to DB ---  for now its questions.txt
# read it
# give to llm
# get response

# reading it
# ----

st.subheader("Your Questions:")
def read_questions(file_path="questions.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.readlines()
    return []

questions = read_questions()
if questions:
    last_question = questions[-1].strip()
    st.write(f"Processing question: {last_question}")
else:
    st.info("No questions have been asked yet.")

# pass the last_question to the LLM

