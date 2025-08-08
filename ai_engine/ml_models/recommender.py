import pandas as pd

def recommend_content(user_data, content_data):
    recommended = content_data.sort_values(by='difficulty_level')[:5]
    return recommended