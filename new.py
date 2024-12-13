import json
import pandas as pd

file_path = '/mnt/data/DataEngineeringQ2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

patient_details = [item['patientDetails'] for item in data]
df = pd.DataFrame(patient_details)

columns_to_check = ['firstName', 'lastName', 'birthDate']


missing_percentages = {
    column: round(df[column].isnull().mean() * 100, 2) + round((df[column] == "").mean() * 100, 2)
    for column in columns_to_check
}

from datetime import datetime

gender_mode = df['gender'].mode()[0]
df['gender'] = df['gender'].fillna(gender_mode)
female_percentage = round((df['gender'] == 'F').mean() * 100, 2)


current_year = datetime.now().year
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
df['age'] = current_year - df['birthDate'].dt.year

def age_group(age):
    if pd.isnull(age):
        return None
    if age <= 12:
        return 'Child'
    elif 13 <= age <= 19:
        return 'Teen'
    elif 20 <= age <= 59:
        return 'Adult'
    else:
        return 'Senior'

df['ageGroup'] = df['age'].apply(age_group)
adult_count = df['ageGroup'].value_counts().get('Adult', 0)

medicine_counts = [len(item['consultationData']['medicines']) for item in data]
average_medicines = round(sum(medicine_counts) / len(medicine_counts), 2)


all_medicines = [
    medicine['medicineName']
    for item in data
    for medicine in item['consultationData']['medicines']
]
medicine_series = pd.Series(all_medicines)
third_most_frequent_medicine = medicine_series.value_counts().index[2]

female_percentage, adult_count, average_medicines, third_most_frequent_medicine


missing_percentages

total_medicines = len(all_medicines)
active_medicines = sum(
    1 for item in data for medicine in item['consultationData']['medicines'] if medicine['isActive']
)
inactive_medicines = total_medicines - active_medicines

active_percentage = round((active_medicines / total_medicines) * 100, 2)
inactive_percentage = round((inactive_medicines / total_medicines) * 100, 2)

active_percentage, inactive_percentage


