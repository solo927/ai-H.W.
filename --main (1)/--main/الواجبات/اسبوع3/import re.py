import re
import numpy as np

raw_data = ["3000$", "7,000.00", "9,500", "1,800$", "3,000", "6,200", "7,500", "35.000.000"]

def clean_number(value):

    value = re.sub(r'[^\d.,]', '', value)
    

    if value.count('.') > value.count(','):
        value = value.replace('.', '')
    else:
        value = value.replace(',', '')
    
    return int(float(value))

data = np.array([clean_number(x) for x in raw_data])

data.sort()

Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data < lower_bound) | (data > upper_bound)]

print("Cleaned Data:", data)
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Bound:", lower_bound)
print("Upper Bound:", upper_bound)
print("Outliers:", outliers)