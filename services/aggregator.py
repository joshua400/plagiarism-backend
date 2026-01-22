def calculate_percentages(highlighted_text, total_sentences):
    """Calculate plagiarism breakdown percentages."""
    if total_sentences == 0:
        return {
            "plagiarismPercentage": 0,
            "exactMatchPercentage": 0,
            "partialMatchPercentage": 0,
            "uniquePercentage": 100
        }
    
    exact_count = sum(1 for h in highlighted_text if h["type"] == "exact")
    partial_count = sum(1 for h in highlighted_text if h["type"] == "partial")
    unique_count = sum(1 for h in highlighted_text if h["type"] == "unique")
    
    exact_pct = round((exact_count / total_sentences) * 100)
    partial_pct = round((partial_count / total_sentences) * 100)
    unique_pct = round((unique_count / total_sentences) * 100)
    
    # Ensure percentages add up to 100
    total_plag = exact_pct + partial_pct
    
    return {
        "plagiarismPercentage": total_plag,
        "exactMatchPercentage": exact_pct,
        "partialMatchPercentage": partial_pct,
        "uniquePercentage": 100 - total_plag
    }
