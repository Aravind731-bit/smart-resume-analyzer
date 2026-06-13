def find_missing_skills(role, skills):

    role_skills = {
        "Frontend Developer": [
            "HTML", "CSS", "JavaScript",
            "React", "Git", "TypeScript"
        ],

        "Python Developer": [
            "Python", "Flask",
            "Django", "SQL", "Git"
        ],

        "Data Analyst": [
            "Python", "SQL",
            "Pandas", "NumPy",
            "Excel"
        ]
    }

    required = role_skills.get(role, [])

    missing = []

    for skill in required:
        if skill not in skills:
            missing.append(skill)

    return missing