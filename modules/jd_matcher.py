def calculate_match(resume_skills, jd_text):

    jd_text = jd_text.lower()

    matched = []

    for skill in resume_skills:
        if skill.lower() in jd_text:
            matched.append(skill)

    if len(resume_skills) == 0:
        return 0, matched

    score = int((len(matched) / len(resume_skills)) * 100)

    return score, matched