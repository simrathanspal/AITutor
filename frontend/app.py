import streamlit as st
from tutor import AITutor

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/styles.css")


# Initialize tutor
tutor = AITutor()
student_name = 'Student Name' # collected from login name

# App Title
st.title(f"CodeBlossom - {student_name}'s AI Mentor 🌸")

# Sidebar for Navigation
st.sidebar.title("Navigation")
sections = ["Home", "Lessons", "Quiz","Progress-Tracker", "Doubts", "Feedback"]
selected_section = st.sidebar.radio("Go to:", sections)

# Render content based on selected section
if selected_section == "Home":
    st.header("🌸 Welcome Back to CodeBlossom!")
    st.write("Where dreams take root.")

elif selected_section == "Lessons":
    st.header("🌸 Lessons for You")
    st.write("Choose a Topic to Learn")
    topics = list(tutor.lessons.keys())
    topic = st.selectbox("Select a topic:", topics)
    if topic:
        lesson = tutor.get_lesson(topic)
        st.subheader(f"Lesson: {topic}")
        st.write(lesson)

elif selected_section == "Quiz":
    st.header("🌸 Test Your Knowledge")
    st.write("Take a quiz to test your understanding of the topics.")
    topic = st.selectbox("Select a topic for the quiz:", list(tutor.quizzes.keys()))
    if topic:
        question = tutor.quizzes[topic]["question"]
        st.write(f"**Question:** {question}")
        user_answer = st.text_input("Your Answer")
        if st.button("Submit"):
            if tutor.check_answer(topic, user_answer):
                st.success("Correct!")
            else:
                st.error("Incorrect. Try again!")

elif selected_section == "Progress-Tracker":
    st.header("🌸 Productivity tool")

elif selected_section == "Doubts":
    st.header("🌸 Share Your Doubts")
    queries = st.text_area("Post your doubts, to connect with mentors")
    if st.button("Submit Queries"):
        with open("queries.txt", "a") as f:
            f.write(queries + "\n")
        st.success("Thank you for your queries!")

elif selected_section == "Feedback":
    st.header("🌸 Share Your Thoughts")
    feedback = st.text_area("What do you think about lecture?")
    if st.button("Submit Feedback"):
        with open("feedback.txt", "a") as f:
            f.write(feedback + "\n")
        st.success("Thank you for your feedback!")