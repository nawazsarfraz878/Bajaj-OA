import json
import pandas as pd

# Load the JSON file content
file_path = '/mnt/data/DataEngineeringQ2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract patientDetails and flatten into a DataFrame
patient_details = [item['patientDetails'] for item in data]
df = pd.DataFrame(patient_details)

# Define columns to check for missing values
columns_to_check = ['firstName', 'lastName', 'birthDate']

# Calculate the percentage of missing values for each column
missing_percentages = {
    column: round(df[column].isnull().mean() * 100, 2) + round((df[column] == "").mean() * 100, 2)
    for column in columns_to_check
}

from datetime import datetime

# 2. Gender Imputation and Percentage of Females
# Impute missing gender values with the mode
gender_mode = df['gender'].mode()[0]
df['gender'] = df['gender'].fillna(gender_mode)
female_percentage = round((df['gender'] == 'F').mean() * 100, 2)

# 3. Adding Age Group and Counting Adults
# Convert birthDate to datetime and calculate age
current_year = datetime.now().year
df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
df['age'] = current_year - df['birthDate'].dt.year

# Define age groups
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

# 4. Average Number of Medicines Prescribed
# Extract medicine details and calculate average
medicine_counts = [len(item['consultationData']['medicines']) for item in data]
average_medicines = round(sum(medicine_counts) / len(medicine_counts), 2)

# 5. Third Most Frequently Prescribed Medicine
# Flatten all prescribed medicine names and find frequencies
all_medicines = [
    medicine['medicineName']
    for item in data
    for medicine in item['consultationData']['medicines']
]
medicine_series = pd.Series(all_medicines)
third_most_frequent_medicine = medicine_series.value_counts().index[2]

female_percentage, adult_count, average_medicines, third_most_frequent_medicine


missing_percentages


# Calculate the total active and inactive medicines
total_medicines = len(all_medicines)
active_medicines = sum(
    1 for item in data for medicine in item['consultationData']['medicines'] if medicine['isActive']
)
inactive_medicines = total_medicines - active_medicines

# Calculate the percentage distribution
active_percentage = round((active_medicines / total_medicines) * 100, 2)
inactive_percentage = round((inactive_medicines / total_medicines) * 100, 2)

active_percentage, inactive_percentage


