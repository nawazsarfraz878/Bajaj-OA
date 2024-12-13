import json
from datetime import datetime
from math import sqrt


with open('/mnt/data/DataEngineeringQ2.json', 'r') as file:
    data = json.load(file)

def is_valid_indian_number(phone_number):
    if phone_number.startswith('+91'):
        phone_number = phone_number[3:]
    elif phone_number.startswith('91'):
        phone_number = phone_number[2:]
    if len(phone_number) == 10 and phone_number.isdigit() and 6000000000 <= int(phone_number) <= 9999999999:
        return True
    return False

def calculate_age(birth_date_str):
    if not birth_date_str:
        return None
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

valid_count = 0
for record in data:
    phone_number = record.get('phoneNumber', '')
    valid = is_valid_indian_number(phone_number)
    record['isValidMobile'] = valid
    if valid:
        valid_count += 1

ages = []
medicine_counts = []

for record in data:
    
    birth_date = record['patientDetails'].get('birthDate')
    age = calculate_age(birth_date)
    
    medicines = record['consultationData'].get('medicines', [])
    medicine_count = len(medicines)
    
    if age is not None:  
        ages.append(age)
        medicine_counts.append(medicine_count)

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator_x = sqrt(sum((xi - mean_x) ** 2 for xi in x))
    denominator_y = sqrt(sum((yi - mean_y) ** 2 for yi in y))
    return numerator / (denominator_x * denominator_y) if denominator_x and denominator_y else 0

pearson_corr = pearson_correlation(ages, medicine_counts)

valid_count, round(pearson_corr, 2)
