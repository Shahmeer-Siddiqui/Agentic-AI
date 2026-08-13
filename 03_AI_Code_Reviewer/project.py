import os
from typing import TypedDict

class pipelinestate(TypedDict):
    user_code: str
    language: str

    code_summary: str
    detected_issues: str
    bug_fixes: str
    optimized_code: str
    best_practices: str
    security_review: str
    final_report: str

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="poolside/laguna-s-2.1:free", 
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

# now create nodes
def summarize_code(state:pipelinestate):
    prompt = f"""
        You are an expert software engineer.

Analyze the given code.

Explain:

1. What this code does.
2. Main logic.
3. Functions used.
4. Time Complexity (if applicable).

Keep the explanation simple.

Code:
{state["user_code"]}
"""
    response = llm.invoke(prompt)
    return {"code_summary": response.content.strip()}

def detect_bugs(state:pipelinestate):
    prompt = f"""
You are an expert code reviewer.

Find all issues in the code.

Include:

- Syntax Errors
- Logical Errors
- Runtime Errors
- Missing Imports
- Edge Cases
- Incorrect Variable Usage

Return everything in bullet points.

Code:

{state["user_code"]}
"""
    response = llm.invoke(prompt)
    return {"detected_issues": response.content.strip()}

def optimize_code(state:pipelinestate):
    prompt = f"""
Optimize the following code.

Requirements:

- Improve readability
- Improve performance
- Reduce duplicate code
- Use better variable names
- Follow clean coding principles

Return only the optimized code.

Code:

{state["user_code"]}
"""
    response = llm.invoke(prompt)
    return {"optimized_code": response.content.strip()}

def review_best_practices(state:pipelinestate):
    prompt = f"""
Review this code according to software engineering best practices.

Check:

- Naming Convention
- Comments
- Function Design
- Code Formatting
- Modularity
- Readability
- Maintainability

Explain improvements.

Code:

{state["user_code"]}
"""
    response = llm.invoke(prompt)
    return {"best_practices": response.content.strip()}

def security_review(state:pipelinestate):
    prompt = f"""
Perform a security review.

Find:

- SQL Injection Risks
- Hardcoded Passwords
- API Keys
- Unsafe File Operations
- Command Injection
- XSS
- Insecure Coding

Explain every issue.

Code:

{state["user_code"]}
"""
    response = llm.invoke(prompt)
    return {"security_review": response.content.strip()}

def generate_report(state:pipelinestate):
    prompt = f"""
Create a professional code review report.

Include sections:

# Code Summary

# Issues Found

# Suggested Fixes

# Optimized Version

# Best Practices

# Security Analysis

# Overall Rating (/10)

# Final Recommendation

Use professional formatting.

"Code Summary"
{state["code_summary"]}

"detected_issues"
{state["detected_issues"]}

"optimized_code"
{state["optimized_code"]}

"best_practices"
{state["best_practices"]}

"security_review"
{state["security_review"]}

"""
    response = llm.invoke(prompt)
    return {"final_report": response.content.strip()}

# now create graph

from langgraph.graph import StateGraph, START, END

graph = StateGraph(pipelinestate)

graph.add_node("summary", summarize_code)
graph.add_node("bugs", detect_bugs)
graph.add_node("optimize", optimize_code)
graph.add_node("practices", review_best_practices)
graph.add_node("security", security_review)
graph.add_node("report", generate_report)

graph.add_edge(START, "summary")
graph.add_edge("summary", "bugs")
graph.add_edge("bugs", "optimize")
graph.add_edge("optimize", "practices")
graph.add_edge("practices", "security")
graph.add_edge("security", "report")
graph.add_edge("report", END)

app = graph.compile()

print("Paste your code (type END on a new line when finished):")

lines = []

while True:
    line = input()
    if line == "END":
        break
    lines.append(line)

topic = "\n".join(lines)

result = app.invoke(
    {
        "user_code": topic,
        "language": "Python"
    }
)

print(result["final_report"])
