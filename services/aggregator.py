def classify(score):
    if score > 0.75:
        return "Exact Match"
    elif score > 0.4:
        return "Partial Match"
    return None
