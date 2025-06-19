import pandas as pd
from ast import literal_eval
from collections import defaultdict

class ESCOContext:
    def __init__(self, skills_df, occupations_df, essential_map, optional_map):
        self.skills_df = skills_df
        self.occupations_df = occupations_df
        self.essential_map = essential_map
        self.optional_map = optional_map
        self.skill_lookup = skills_df.set_index('conceptUri')['preferredLabel'].to_dict()

    def get_occupation_skills(self, label):
        match = self.occupations_df[self.occupations_df['preferredLabel'].str.lower() == label.lower()]
        if match.empty:
            return f"No occupation found for '{label}'"
        row = match.iloc[0]
        uri = row['conceptUri']
        essential = [self.skill_lookup.get(s, s) for s in self.essential_map.get(uri, [])]
        optional = [self.skill_lookup.get(s, s) for s in self.optional_map.get(uri, [])]
        return {
            "occupation": row['preferredLabel'],
            "essential_skills": essential,
            "optional_skills": optional
        }

    @staticmethod
    def load(base_path):
        skills_df = pd.read_csv(f"{base_path}/skills_en.csv")
        occupations_df = pd.read_csv(f"{base_path}/occupations_en.csv")
        relations_df = pd.read_csv(f"{base_path}/occupationSkillRelations_en.csv")

        # Filter necessary columns
        skills_df = skills_df[['conceptUri', 'preferredLabel', 'description']].dropna()
        occupations_df = occupations_df[['conceptUri', 'preferredLabel', 'description']].dropna()

        # Build maps
        essential_map = defaultdict(list)
        optional_map = defaultdict(list)

        for _, row in relations_df.iterrows():
            if row['relationType'] == 'essential':
                essential_map[row['occupationUri']].append(row['skillUri'])
            elif row['relationType'] == 'optional':
                optional_map[row['occupationUri']].append(row['skillUri'])

        return ESCOContext(skills_df, occupations_df, essential_map, optional_map)


def calculate_skill_gap(user_skills, occupation_label, get_occupation_skills):
    user_skills_set = set(s.lower() for s in user_skills)
    skill_data = get_occupation_skills(occupation_label)
    if isinstance(skill_data, str):
        return skill_data

    def gap(skills):
        return [s for s in skills if s and s.lower() not in user_skills_set]

    missing_essential = gap(skill_data['essential_skills'])
    missing_optional = gap(skill_data['optional_skills'])

    return {
        "occupation": skill_data['occupation'],
        "missing_essential": missing_essential,
        "missing_optional": missing_optional
    }
