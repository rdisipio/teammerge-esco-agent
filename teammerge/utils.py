import pandas as pd
from ast import literal_eval


def load_esco_data(skills_path, occupations_path):
    """
    Load ESCO skills and occupations from CSV files.
    Parse essential and optional skill links.
    """
    skills_df = pd.read_csv(skills_path)
    skills_df = skills_df[['conceptUri', 'preferredLabel', 'description']].dropna()

    occupations_df = pd.read_csv(occupations_path)
    occupations_df = occupations_df[['conceptUri', 'preferredLabel', 'description', 'hasEssentialSkill', 'hasOptionalSkill']]

    def parse_uris(raw):
        if pd.isna(raw):
            return []
        try:
            return literal_eval(raw) if isinstance(raw, str) else raw
        except:
            return [uri.strip() for uri in raw.split("|")]

    occupations_df['essential_skills'] = occupations_df['hasEssentialSkill'].apply(parse_uris)
    occupations_df['optional_skills'] = occupations_df['hasOptionalSkill'].apply(parse_uris)

    return skills_df, occupations_df


def make_skill_lookup(skills_df):
    """
    Create a lookup dictionary for ESCO skills.
    Maps concept URIs to preferred labels.
    """
    return skills_df.set_index('conceptUri')['preferredLabel'].to_dict()


def get_occupation_skills(occupation_label, skill_lookup, occupations_df):
    """
    Fetch essential and optional skills for a given ESCO occupation.
    Returns a dictionary with occupation name, essential skills, and optional skills.   
    """

    match = occupations_df[occupations_df['preferredLabel'].str.lower() == occupation_label.lower()]
    if match.empty:
        return f"No occupation found for '{occupation_label}'"

    row = match.iloc[0]
    essential = [skill_lookup.get(uri, uri) for uri in row['essential_skills']]
    optional = [skill_lookup.get(uri, uri) for uri in row['optional_skills']]

    return {
        "occupation": row['preferredLabel'],
        "essential_skills": essential,
        "optional_skills": optional
    }



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
