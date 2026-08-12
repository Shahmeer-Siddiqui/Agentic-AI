import os
from typing import TypedDict

class Pipelinestate(TypedDict):
    user_idea: str
    idea_summary: str
    requirements: str
    features: str
    architecture: str
    database_design: str
    api_plan: str
    tech_stack: str
    development_roadmap: str
    final_blueprint: str

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="poolside/laguna-s-2.1:free",  # Alternative free model
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

# now creates nodes

def receive_idea(state: Pipelinestate)->dict:
    prompt = f"""You are a senior software consultant.

Understand the software idea.

Write only a short summary.

Maximum 120 words.

Do not suggest features.

Software Idea:
{state["user_idea"]}"""

    response = llm.invoke(prompt)
    return {"idea_summary": response.content.strip()}

def analyze_requirements(state:Pipelinestate)->dict:
    prompt = f"""You are a Business Analyst.

Create the software requirements.

Return only:

Functional Requirements

Non Functional Requirements

Must Have

Optional

Maximum 350 words.

Idea Summary

{state["idea_summary"]}"""

    response = llm.invoke(prompt)

    return {"requirements": response.content.strip()}

def extract_features(state:Pipelinestate)->dict:
    prompt = f"""You are a Product Manager.

Generate features from requirements.

Create only

Core Features

Advanced Features

Future Enhancements

Maximum 300 words.

Requirements

{state["requirements"]}"""

    response = llm.invoke(prompt)
    return {"features":response.content.strip()}

def design_architecture(state:Pipelinestate)->dict:
    prompt = f"""You are a Software Architect.

Design a High-Level Architecture.

Include

Frontend

Backend

Authentication

Database

Storage

External Services

Explain communication briefly.

Maximum 350 words.

Features

{state["features"]}"""

    response = llm.invoke(prompt)
    return {"architecture": response.content.strip()}

def design_database(state:Pipelinestate)->dict:
    prompt = f"""You are a Database Architect.

Design the database.

For every table include

Table Name

Purpose

Primary Key

Foreign Key

Important Columns

Relationships

Maximum 10 tables.

Requirements

{state["requirements"]}

Features

{state["features"]}"""

    response = llm.invoke(prompt)
    return {"database_design": response.content.strip()}

def plan_api(state:Pipelinestate)->dict:
    prompt = f"""You are a Backend Architect.

Create REST APIs.

For every endpoint include

Method

URL

Purpose

Authentication

Maximum 20 endpoints.

Features

{state["features"]}

Database Design

{state["database_design"]}"""

    response = llm.invoke(prompt)
    return {"api_plan": response.content.strip()}

def recommend_tech_stack(state:Pipelinestate)->dict:

    prompt = f"""You are a Software Consultant.

Recommend

Frontend

Backend

Database

Authentication

Hosting

Deployment

Testing

Version Control

Explain each in one line.

Requirements

{state["requirements"]}"""

    response = llm.invoke(prompt)
    return {"tech_stack":response.content.strip()}

def create_development_roadmap(state:Pipelinestate)->dict:
    prompt = f"""You are an Agile Project Manager.

Create a roadmap.

Phase 1

Phase 2

Phase 3

Phase 4

Deliverables

Timeline

Maximum 250 words.

Features

{state["features"]}"""

    response = llm.invoke(prompt)
    return {"development_roadmap":response.content.strip()}

def generate_final_blueprint(state:Pipelinestate)->dict:
    prompt = f"""You are a Technical Documentation Writer.

Create a professional Markdown Software Blueprint.

Do NOT generate new content.

Only organize the following sections.

# Project Summary

{state["idea_summary"]}

# Requirements

{state["requirements"]}

# Features

{state["features"]}

# Architecture

{state["architecture"]}

# Database Design

{state["database_design"]}

# API Plan

{state["api_plan"]}

# Technology Stack

{state["tech_stack"]}

# Development Roadmap

{state["development_roadmap"]}

Keep formatting clean.

Do not rewrite sections.

Do not expand anything.

Do NOT generate new content."""

    response = llm.invoke(prompt)
    return {"final_blueprint": response.content.strip()}

# now create graph using edges

from langgraph.graph import StateGraph, START, END

graph = StateGraph(Pipelinestate)

#  user_idea: str
    # requirements: str
    # features: str
    # architecture: str
    # database_design: str
    # api_plan: str
    # tech_stack: str
    # development_roadmap: str
    # final_blueprint: str

graph.add_node("user_idea",receive_idea)
graph.add_node("requirements",analyze_requirements)
graph.add_node("features",extract_features)
graph.add_node("architecture",design_architecture)
graph.add_node("database_design",design_database)
graph.add_node("api_plan",plan_api)
graph.add_node("tech_stack",recommend_tech_stack)
graph.add_node("development_roadmap",create_development_roadmap)
graph.add_node("final_blueprint",generate_final_blueprint)

graph.add_edge(START,"user_idea")
graph.add_edge("user_idea","requirements")
graph.add_edge("requirements","features")
graph.add_edge("features","architecture")
graph.add_edge("architecture","database_design")
graph.add_edge("database_design","api_plan")
graph.add_edge("api_plan","tech_stack")
graph.add_edge("tech_stack","development_roadmap")
graph.add_edge("development_roadmap","final_blueprint")
graph.add_edge("final_blueprint",END)

app = graph.compile()

topic = input("Enter Software: ")

result = app.invoke(
    {
        "user_idea": topic
    }
)

# Save output as Markdown file
file_name = topic.replace(" ", "_") + "_Software_Blueprint.md"

with open(file_name, "w", encoding="utf-8") as file:
    file.write(result["final_blueprint"])

print(f"\n Blueprint saved successfully as '{file_name}'")