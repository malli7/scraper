
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding

def calculate_cosine_similarity(embedding1, embedding2):
    return cosine_similarity([embedding1], [embedding2])[0][0]

def evaluate_resume(job_description, resume_text):
    prompt = f"""
    You are an AI trained to evaluate resumes against job descriptions and return:
    A dynamic score (0–100) based on context—not fixed brackets.
    4 concise, actionable review points in JSON format.
    Evaluate based on:
    Skill Alignment – Relevance and depth of technical/non-technical skills.
    Responsibility Fit – Match with core duties of the role.
    Projects & Experience – Practical, hands-on examples of ability.
    Soft Skills & Adaptability – Communication, growth, flexibility.
    Experience Level – Under/overqualified vs. role expectations.
    Scoring Notes:
    No fixed weights—score holistically.
    Let strengths offset minor gaps.
    Penalize overqualification only if misaligned.
    Credit transferable skills and relevant projects.
    Output (Strict JSON):
    {{
    "score": X,
    "review": [
        "Insight 1",
        "Insight 2",
        "Insight 3",
        "Insight 4"
    ]
    }}
    score must be a dynamic integer
    Exactly 4 direct, useful insights
    Avoid fluff or intro phrases—keep feedback sharp and specific
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
    job_embedding = get_embedding(job_description)
    resume_embedding = get_embedding(resume_text)
    similarity = calculate_cosine_similarity(job_embedding, resume_embedding)
    if similarity < 0.4:
        return {"score": similarity * 100, "review": ["Similarity score is too low"]}
    else:
        evaluation = evaluate_resume(job_description, resume_text)
        return evaluation
