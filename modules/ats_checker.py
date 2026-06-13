def calculate_ats_score(text):
    score = 0

    text = text.lower()

    keywords = [
        "skills",
        "education",
        "project",
        "experience",
        "certification",
        "github",
        "linkedin"
    ]

    for keyword in keywords:
        if keyword in text:
            score += 10

    return min(score, 100)
