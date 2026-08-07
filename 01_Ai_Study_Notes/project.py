import os
from typing import TypedDict

class PipelineState(TypedDict):
    topic_input: str
    explanation: str
    key_points: str
    quiz: str
    final_notes: str


from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest"
)
# 1. receive_topic
# 2. generate_explanation
# 3. generate_key_points
# 4. generate_quiz
# 5. generate_final_notes
# creating nodes

def generate_explanation(state: PipelineState) -> dict:

    prompt = f"""
You are an expert teacher.

Explain the following topic in simple and easy English.

Topic:
{state["topic_input"]}

Instructions:
- Use simple language.
- Explain step by step.
- Keep the explanation between 150 and 200 words.
- Make it easy for beginners to understand.
"""

    response = llm.invoke(prompt)    
    return {
    "explanation": response.content[0]["text"].strip()
}

def generate_key_points(state: PipelineState) -> dict:
    prompt = f"""
You are an expert teacher.

Generate the most important key points for the following topic.

Topic:
{state["explanation"]}

Instructions:
- Give 5 key points.
- Use bullet points.
- Keep each point short and easy to understand.
"""
    response = llm.invoke(prompt)

    return {
        "key_points": response.content[0]["text"].strip()
}
def generate_quiz(state: PipelineState)->dict:
    prompt = f"""
You are an expert teacher.

Create a short quiz for the following topic.

Topic:
{state["key_points"]}

Instructions:
- Generate exactly 5 multiple-choice questions.
- Each question should have 4 options (A, B, C, D).
- Clearly mention the correct answer after each question.
"""
    response = llm.invoke(prompt)

    return {
     "quiz": response.content[0]["text"].strip()
}
def generate_final_notes(state:PipelineState)-> dict:
    prompt = f"""
You are an expert teacher.

Create well-organized study notes using the information below.

Topic:
{state["topic_input"]}

Explanation:
{state["explanation"]}

Key Points:
{state["key_points"]}

Quiz:
{state["quiz"]}

Instructions:
- Add a clear title.
- Organize the notes with headings.
- Keep the formatting clean and readable.
- Include all sections:
  1. Topic
  2. Explanation
  3. Key Points
  4. Quiz
- Do not add extra information.
"""
    response = llm.invoke(prompt)

    return {
    "final_notes": response.content[0]["text"].strip()
}

# now create graph using edges

from langgraph.graph import StateGraph, START, END

graph = StateGraph(PipelineState)

graph.add_node("explanation", generate_explanation)
graph.add_node("key_points", generate_key_points)
graph.add_node("quiz", generate_quiz)
graph.add_node("final_notes", generate_final_notes)

graph.add_edge(START,"explanation")
graph.add_edge("explanation","key_points")
graph.add_edge("key_points","quiz")
graph.add_edge("quiz","final_notes")
graph.add_edge("final_notes",END)

app = graph.compile()

topic = input("Enter a topic: ")
result = app.invoke(
    {
        "topic_input": topic
    }
)

file_name = topic.replace(" ", "_") + "Notes.md"

with open(file_name, "w", encoding="utf-8") as file:
    file.write(result["final_notes"])

print(f"\n notes saved successfully as '{file_name}'")