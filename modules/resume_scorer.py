def calculate_score(text):
    score = 0

    text = text.lower()

    if "@" in text:
        score += 10

    if any(char.isdigit() for char in text):
        score += 10

    if "skill" in text:
        score += 20

    if "project" in text:
        score += 20

    if "certificate" in text or "certification" in text:
        score += 20

    if "github" in text:
        score += 10

    if "linkedin" in text:
        score += 10

    return min(score, 100)