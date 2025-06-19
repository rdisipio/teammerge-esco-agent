def calculate_skill_gap(user_skills, occupation_label, get_occupation_skills):
    """
    Compare user's skills against ESCO occupation requirements.
    Returns a summary of missing essential and optional skills.
    """
    user_skills_set = set(s.lower() for s in user_skills)
    
    # Fetch required skills for the target occupation
    skill_data = get_occupation_skills(occupation_label)
    if isinstance(skill_data, str):
        return skill_data  # Error message

    def gap(skills):
        return [s for s in skills if s and s.lower() not in user_skills_set]

    missing_essential = gap(skill_data['essential_skills'])
    missing_optional = gap(skill_data['optional_skills'])

    return {
        "occupation": skill_data['occupation'],
        "missing_essential": missing_essential,
        "missing_optional": missing_optional
    }
