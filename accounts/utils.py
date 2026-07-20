import os
import pdfplumber
import re
from docx import Document

#global skill library
SKILLS_LIBRARY = [
    "python",
    "django",
    "flask",
    "java",
    "javascript",
    "react",
    "angular",
    "html",
    "css",
    "bootstrap",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "rest",
    "api",
    "linux",
]

ROLE_LIBRARY = [
    "python developer",
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "django developer",
    "data analyst",
    "web developer"
]

EDUCATION_LIBRARY = [
    "b.tech",
    "btech",
    "m.tech",
    "mtech",
    "bca",
    "mca",
    "b.sc",
    "bsc",
    "m.sc",
    "msc",
    "mba",
    "phd"
]

def extract_pdf_text(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_docx_text(file_path):

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text


def extract_resume_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    return "Unsupported file format."


def clean_resume_text(text):

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"\n+", "\n", text)

    text = text.strip()

    return text


def tokenize_text(text):

    text = text.lower()

    tokens = re.findall(r'\b\w+\b', text)

    return tokens
def extract_skills(text):

    skills = []

    text = text.lower()

    for skill in SKILLS_LIBRARY:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            skills.append(skill)

    return skills
def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group()

    return None


def extract_phone(text):

    match = re.search(
        r"\b\d{10}\b",
        text
    )

    if match:
        return match.group()

    return None

def extract_experience(text):

    match = re.search(
        r"(\d+\+?\s*(?:years?|yrs?))",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group()

    return "Not Found"

def extract_role(text):

    text = text.lower()

    for role in ROLE_LIBRARY:

        if role in text:
            return role.title()

    return "Not Found"

def extract_education(text):

    text = text.lower()

    for education in EDUCATION_LIBRARY:

        if education in text:
            return education.upper()

    return "Not Found"