from typing import List

def generate_suggestions(risk_level: str, features_dict: dict) -> List[str]:
    suggestions = []
    attendance = features_dict.get('attendance', 100)
    study_time = features_dict.get('study_time', 0)
    previous_score = features_dict.get('previous_score', 0)
    assignments = features_dict.get('assignments', 0)
    internet_access = features_dict.get('internet_access', True)
    extracurricular = features_dict.get('extracurricular', False)

    if risk_level == 'HIGH':
        if attendance < 75:
            suggestions.append("Critical: Attend all classes — you're missing too many sessions. Aim for >=85%.")
        if study_time < 1:
            suggestions.append("Start with at least 1 hour of daily focused study. Use the Pomodoro technique.")
        if previous_score < 50:
            suggestions.append("Schedule weekly tutoring sessions to strengthen fundamentals.")
        if assignments < 5:
            suggestions.append("Complete all assignments — they account for a significant grade portion.")
        if not internet_access:
            suggestions.append("Visit the school library daily for online resources and practice exercises.")
        suggestions.append("Connect with your academic counselor for a personalized recovery plan.")
    elif risk_level == 'MEDIUM':
        if attendance < 85:
            suggestions.append("Improve attendance to >=85% — each class missed affects your understanding.")
        if study_time < 2:
            suggestions.append("Increase study time to at least 2 hours/day with structured revision.")
        if assignments < 7:
            suggestions.append("Aim to complete all assignments on time for consistent marks.")
        if not extracurricular:
            suggestions.append("Join a study group or academic club to stay motivated.")
        suggestions.append("Review weak subjects weekly and practice past papers.")
    elif risk_level == 'LOW':
        if attendance < 90:
            suggestions.append("Push attendance above 90% to secure your performance.")
        if not extracurricular:
            suggestions.append("Consider joining extracurricular activities to develop leadership skills.")
        suggestions.append("Challenge yourself with advanced problems to strengthen your understanding.")
        suggestions.append("Great work! Maintain your study routine and aim for >=90% attendance.")

    return suggestions
