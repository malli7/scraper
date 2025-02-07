import os
from dotenv import load_dotenv

load_dotenv()  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


BATCH_SIZE = 10

JOB_ROLES = [
    "Software Engineer",
    "Software Developer",
    "Front-End Developer",
    "Back-End Developer",
    "Full-Stack Developer",
    "Mobile App Developer",
    "Embedded Software Engineer",
    "Game Developer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Engineer",
    "Data Analyst",
    "IT Support Engineer",
    "Software Test Engineer",
    "UI/UX Designer",
    "Blockchain Developer",
    "IoT Engineer",
    "Web Developer",
]
