import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END, START

load_dotenv()

genai=ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv('GOOGLE_API_KEY'))

class CodeReviewState(TypedDict):
    question: str
    user_solution: str
    language: str
    optimized_solution: str
    feedback: str
    detailed_explanation: str
    user_satisfied: bool


language_prompt=ChatPromptTemplate.from_template(
"""You are a code language classifier. Identify if the given code snippet is written in Python or C++.
Code:
{user_solution}
Respond with only "python" or "cpp".
""")

def parse_language(response):
    return {"language": response.content.strip().lower()}

language_chain=language_prompt | genai | RunnableLambda(parse_language)


python_prompt=ChatPromptTemplate.from_template(
"""You are a Python expert. Given a problem, write the most optimal Python solution (best time and space complexity).
Do not provide any explanation, just the code.
Question:
{question}
""")

def parse_python_solution(response):
    return {"optimized_solution": response.content.strip()}

python_opt_chain=python_prompt | genai | RunnableLambda(parse_python_solution)



cpp_prompt=ChatPromptTemplate.from_template(
"""You are a C++ expert. Given a problem, write the most optimal C++ solution (best time and space complexity).
Do not provide any explanation, just the code.
Question:
{question}
"""
)

def parse_cpp_solution(response):
    return {"optimized_solution": response.content.strip()}

cpp_opt_chain=cpp_prompt | genai | RunnableLambda(parse_cpp_solution)



feedback_prompt=ChatPromptTemplate.from_template(
"""You are a code reviewer. Compare the user's solution with the optimized one and provide a short simple review including suggestions on correctness, readability, time and space complexity.
User Solution:
{user_solution}

Optimized Solution:
{optimized_solution}

Feedback:
"""
)

def parse_feedback(response):
    return {"feedback": response.content.strip()}

feedback_chain=feedback_prompt | genai | RunnableLambda(parse_feedback)


explanation_prompt=ChatPromptTemplate.from_template(
"""You are a helpful tutor. Compare the user's solution with the optimal one and give a detailed explanation of mistakes, inefficiencies, and how to improve them.

Question:
{question}

User Solution:
{user_solution}

Optimized Solution:
{optimized_solution}

Detailed Explanation:
"""
)

def parse_explanation(response):
    return {"detailed_explanation": response.content.strip()}

explanation_chain=explanation_prompt | genai | RunnableLambda(parse_explanation)


def human_in_loop(state: CodeReviewState) -> dict:
    return {"user_satisfied": False}  


def route_by_language(state: CodeReviewState) -> str:
    return "python agent" if state["language"] == "python" else "cpp agent"

def review_decision(state: CodeReviewState) -> str:
    return "end_edge" if state.get("user_satisfied", False) else "explanation"


builder = StateGraph(CodeReviewState)

builder.add_node("language_detection", language_chain)
builder.add_node("python agent", python_opt_chain)
builder.add_node("cpp agent", cpp_opt_chain)
builder.add_node("feedback", feedback_chain)
builder.add_node("explanation", explanation_chain)
builder.add_node("user_review", RunnableLambda(human_in_loop))

builder.add_edge(START,"language_detection")

builder.add_conditional_edges("language_detection",route_by_language,{
    "python agent": "python agent",
    "cpp agent": "cpp agent",
})

builder.add_edge("python agent", "feedback")
builder.add_edge("cpp agent", "feedback")
builder.add_edge("feedback", "user_review")
builder.add_conditional_edges("user_review",review_decision,{
    "end_edge": END,
    "explanation": "explanation",
})
builder.add_edge("explanation", "user_review")
app = builder.compile()


