def get_suggestions(score, ats_score, missing_skills):

    suggestions = []

    if score < 80:
        suggestions.append("Add more projects to improve resume strength.")

    if ats_score < 70:
        suggestions.append("Add sections like Experience, Projects and Certifications.")

    for skill in missing_skills:
        suggestions.append(f"Learn {skill}")

    return suggestions