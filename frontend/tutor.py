import json

class AITutor:
    def __init__(self):
        with open("resources/lessons.json") as f:
            self.lessons = json.load(f)
        with open("resources/quizzes.json") as f:
            self.quizzes = json.load(f)

    def get_lesson(self, topic):
        return self.lessons.get(topic, "Topic not available.")

    def get_quiz(self, topic):
        return self.quizzes.get(topic, "Quiz not available.")

    def check_answer(self, topic, user_answer):
        correct_answer = self.quizzes[topic]["answer"]
        return user_answer.lower() == correct_answer.lower()
