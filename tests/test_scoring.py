from src.matching.scoring_engine import calculate_weighted_score


def test_calculate_weighted_score():
    results = [
        {"priority": "MANDATORY", "status": "MATCHED"},
        {"priority": "MANDATORY", "status": "MISSING"},
        {"priority": "PREFERRED", "status": "MATCHED"},
    ]
    score = calculate_weighted_score(results)
    assert score > 0
