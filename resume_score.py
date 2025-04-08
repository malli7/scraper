from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_resume(job_description, resume_text):
    prompt = f"""
            You are an AI trained to evaluate resumes against job descriptions and return:
            - A dynamic score (0–100) based on context—not fixed brackets.
            - 4 concise, actionable review points in JSON format.

            Evaluate based on:
            - Skill Alignment – Relevance and depth of technical/non-technical skills.
            - Responsibility Fit – Match with core duties of the role.
            - Projects & Experience – Practical, hands-on examples of ability.
            - Soft Skills & Adaptability – Communication, growth, flexibility.
            - Experience Level – Under/overqualified vs. role expectations.

            Scoring Notes:
            - No fixed weights—score holistically.
            - Let strengths offset minor gaps.
            - Penalize overqualification only if misaligned.
            - Credit transferable skills and relevant projects.

            Output (Strict JSON format):
            {{
              "score": <dynamic_score>,
              "review": [
                "Insight 1",
                "Insight 2",
                "Insight 3",
                "Insight 4"
             ]
            }}
            
            Rules:
            - Avoid fluff. Each insight should be sharp, specific, and directly based on the job vs. resume comparison.
            - Donot generate generic 5 multiple scores like 45, 85 , be specific and absolute scores and justify the score in review points.
            
            Job Description:
            {job_description}
            
            Resume:
            {resume_text}
            """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert resume evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = response.choices[0].message.content
    return result

def calculate_score(job_description, resume_text):
    evaluation = evaluate_resume(job_description, resume_text)
    return evaluation
