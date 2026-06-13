def predict_role(skills):

    skills = [skill.lower() for skill in skills]

    if "react" in skills or "javascript" in skills:
        return "Frontend Developer"

    elif "python" in skills and ("flask" in skills or "django" in skills):
        return "Python Developer"

    elif "python" in skills and "sql" in skills:
        return "Data Analyst"

    elif "java" in skills:
        return "Java Developer"

    return "General Software Developer"