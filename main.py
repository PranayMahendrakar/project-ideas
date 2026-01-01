#!/usr/bin/env python3
"""
Project Idea Generator - Llama-Based Academic Tool
Suggests feasible project ideas based on course objectives
Author: Pranay M
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.markdown import Markdown
import json
from typing import List

console = Console()

PROJECT_TYPES = ["Research Paper", "Lab Experiment", "Software Application", "Data Analysis",
                 "Case Study", "Design Project", "Presentation", "Portfolio", "Group Project", "Capstone"]

DIFFICULTY_LEVELS = ["Beginner", "Intermediate", "Advanced", "Graduate"]


class ProjectIdeaGenerator:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.saved_ideas = []
    
    def generate_ideas(self, course: str, objectives: List[str], constraints: dict) -> dict:
        prompt = f"""Generate feasible project ideas for a course.

Course: {course}
Learning Objectives: {json.dumps(objectives)}
Constraints: {json.dumps(constraints)}

Return JSON:
{{
    "course": "{course}",
    "project_ideas": [
        {{
            "id": 1,
            "title": "project title",
            "description": "what the project involves",
            "type": "research/coding/design/etc",
            "difficulty": "beginner/intermediate/advanced",
            "objectives_addressed": ["which objectives it covers"],
            "deliverables": ["what student will produce"],
            "estimated_time": "hours/weeks",
            "skills_developed": ["skills gained"],
            "resources_needed": ["materials/tools required"],
            "feasibility_score": 85,
            "innovation_score": 70
        }}
    ],
    "recommendation": "best choice and why",
    "tips_for_success": ["general advice"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        result = self._parse_json(response['message']['content'])
        self.saved_ideas.extend(result.get('project_ideas', []))
        return result
    
    def expand_idea(self, idea: str) -> dict:
        prompt = f"""Expand this project idea into a detailed plan.

Project Idea: {idea}

Return JSON:
{{
    "project_title": "{idea}",
    "expanded_description": "detailed description",
    "objectives": ["specific project objectives"],
    "methodology": {{
        "approach": "how to tackle the project",
        "phases": [
            {{
                "phase": "phase name",
                "tasks": ["specific tasks"],
                "duration": "time estimate",
                "milestones": ["checkpoints"]
            }}
        ]
    }},
    "technical_requirements": {{
        "tools": ["software/hardware needed"],
        "skills": ["skills required"],
        "data_sources": ["if applicable"]
    }},
    "deliverables": [
        {{
            "deliverable": "name",
            "description": "what it is",
            "format": "how to submit"
        }}
    ],
    "evaluation_criteria": ["how it will be graded"],
    "potential_challenges": ["possible difficulties"],
    "solutions": ["how to overcome challenges"],
    "extension_possibilities": ["ways to enhance the project"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def assess_feasibility(self, idea: str, resources: dict) -> dict:
        prompt = f"""Assess the feasibility of this project idea.

Project: {idea}
Available Resources: {json.dumps(resources)}

Return JSON:
{{
    "project": "{idea}",
    "feasibility_assessment": {{
        "overall_score": 75,
        "verdict": "highly feasible/feasible/challenging/not recommended"
    }},
    "time_analysis": {{
        "estimated_hours": 40,
        "fits_timeline": true,
        "time_risks": ["potential delays"]
    }},
    "resource_analysis": {{
        "resources_available": ["what you have"],
        "resources_needed": ["what you need"],
        "gaps": ["missing resources"],
        "alternatives": ["workarounds for gaps"]
    }},
    "skill_analysis": {{
        "skills_required": ["needed skills"],
        "learning_curve": "steep/moderate/gentle",
        "skill_gaps": ["skills to develop"]
    }},
    "risk_assessment": [
        {{
            "risk": "potential problem",
            "likelihood": "high/medium/low",
            "impact": "high/medium/low",
            "mitigation": "how to prevent/handle"
        }}
    ],
    "recommendations": ["how to improve feasibility"],
    "go_no_go": "proceed/modify/abandon"
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def generate_timeline(self, idea: str, weeks: int) -> dict:
        prompt = f"""Create a project timeline.

Project: {idea}
Available Weeks: {weeks}

Return JSON:
{{
    "project": "{idea}",
    "total_duration": "{weeks} weeks",
    "timeline": [
        {{
            "week": 1,
            "phase": "phase name",
            "tasks": ["specific tasks"],
            "deliverables": ["what's due"],
            "hours_estimated": 10
        }}
    ],
    "milestones": [
        {{
            "milestone": "checkpoint",
            "week": 2,
            "criteria": "what to achieve"
        }}
    ],
    "buffer_time": "contingency days",
    "critical_path": ["tasks that can't be delayed"],
    "parallel_tasks": ["tasks that can overlap"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def suggest_resources(self, idea: str) -> dict:
        prompt = f"""Suggest resources for this project.

Project: {idea}

Return JSON:
{{
    "project": "{idea}",
    "learning_resources": [
        {{
            "resource": "name/title",
            "type": "tutorial/documentation/course/book",
            "url": "link if applicable",
            "relevance": "how it helps"
        }}
    ],
    "tools_and_software": [
        {{
            "tool": "name",
            "purpose": "what it's for",
            "cost": "free/paid",
            "alternatives": ["other options"]
        }}
    ],
    "datasets": ["if applicable"],
    "templates": ["useful templates"],
    "communities": ["forums/groups for help"],
    "example_projects": ["similar projects for reference"]
}}"""

        response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
        return self._parse_json(response['message']['content'])
    
    def _parse_json(self, content: str) -> dict:
        try:
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(content[start:end])
        except:
            pass
        return {"raw_response": content}


def display_menu():
    table = Table(title="💡 Project Idea Generator", show_header=True)
    table.add_column("Option", style="cyan", width=6)
    table.add_column("Feature", style="green")
    table.add_column("Description", style="white")
    
    table.add_row("1", "Generate Ideas", "Get project suggestions")
    table.add_row("2", "Expand Idea", "Detailed project plan")
    table.add_row("3", "Assess Feasibility", "Check if doable")
    table.add_row("4", "Create Timeline", "Project schedule")
    table.add_row("5", "Find Resources", "Get helpful resources")
    table.add_row("6", "View Saved", "See saved ideas")
    table.add_row("0", "Exit", "Close application")
    
    console.print(table)


def main():
    console.print(Panel.fit(
        "[bold blue]💡 Project Idea Generator[/bold blue]\n"
        "[green]AI-Powered Academic Project Suggestions[/green]\n"
        "[dim]Author: Pranay M[/dim]",
        border_style="blue"
    ))
    
    generator = ProjectIdeaGenerator()
    
    while True:
        display_menu()
        choice = Prompt.ask("\n[cyan]Select option[/cyan]", default="0")
        
        if choice == "0":
            console.print("[yellow]Goodbye! Build amazing projects! 💡[/yellow]")
            break
        
        elif choice == "6":
            if generator.saved_ideas:
                for i, idea in enumerate(generator.saved_ideas[-5:], 1):
                    console.print(f"  {i}: {idea.get('title', 'Untitled')}")
            else:
                console.print("[dim]No saved ideas.[/dim]")
            continue
        
        with console.status("[bold green]Generating ideas..."):
            if choice == "1":
                course = Prompt.ask("Course name")
                objectives = Prompt.ask("Learning objectives (comma-separated)").split(",")
                constraints = {
                    "time_weeks": Prompt.ask("Available weeks", default="4"),
                    "difficulty": Prompt.ask("Difficulty", choices=DIFFICULTY_LEVELS, default="Intermediate"),
                    "type": Prompt.ask("Project type preference", default="any"),
                    "individual_or_group": Prompt.ask("Individual or group", default="individual")
                }
                result = generator.generate_ideas(course, [o.strip() for o in objectives], constraints)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="💡 Project Ideas"))
            
            elif choice == "2":
                idea = Prompt.ask("Project idea to expand")
                result = generator.expand_idea(idea)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📋 Expanded Plan"))
            
            elif choice == "3":
                idea = Prompt.ask("Project to assess")
                resources = {
                    "time_available": Prompt.ask("Hours per week", default="10"),
                    "budget": Prompt.ask("Budget", default="$0"),
                    "tools": Prompt.ask("Tools you have", default="computer, internet"),
                    "skills": Prompt.ask("Your skills", default="")
                }
                result = generator.assess_feasibility(idea, resources)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="✓ Feasibility Assessment"))
            
            elif choice == "4":
                idea = Prompt.ask("Project for timeline")
                weeks = IntPrompt.ask("Available weeks", default=4)
                result = generator.generate_timeline(idea, weeks)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📅 Project Timeline"))
            
            elif choice == "5":
                idea = Prompt.ask("Project to find resources for")
                result = generator.suggest_resources(idea)
                console.print(Panel(Markdown(f"```json\n{json.dumps(result, indent=2)}\n```"),
                                   title="📚 Resources"))
        
        console.print("\n" + "="*50)


if __name__ == "__main__":
    main()
