# -*- coding: utf-8 -*-
"""DS_&_ML_TASK_NO_1_MANISH_KUMAR.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hm5kAb6z2Qv41FIDgY3OQvY0VhYH3vOK
"""

!pip install fuzzywuzzy

!pip install python-Levenshtein

# Import necessary libraries
import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation
from fuzzywuzzy import fuzz  # For fuzzy string matching
from fuzzywuzzy import process  # For advanced fuzzy operations

# Load the dataset
df = pd.read_csv('tested.csv')  # Replace 'test.csv' with your dataset filename

# Display the first few rows of the dataset
print("Dataset Preview:")
print(df.head())

# Display dataset information
print("\nDataset Information:")
print(df.info())

# Display summary statistics
print("\nDataset Summary Statistics:")
print(df.describe(include='all'))

# Check for missing values
print("\nMissing Values in the Dataset:")
print(df.isnull().sum())

# Display columns with missing values
columns_with_na = df.columns[df.isnull().any()]
print("\nColumns with Missing Values:", columns_with_na)

# Handle missing values
df['Age'].fillna(df['Age'].mean(), inplace=True)  # Fill missing 'Age' with mean
df['Fare'].fillna(df['Fare'].median(), inplace=True)  # Fill missing 'Fare' with median
df.drop('Cabin', axis=1, inplace=True)  # Drop 'Cabin' column due to excessive missing data

# Verify no missing values remain
print("\nMissing Values After Processing:")
print(df.isnull().sum())

# Display unique values in specific columns
print("\nUnique Values in Embarked Column:")
print(df['Embarked'].unique())

# Count distribution of a specific column
print("\nValue Counts for 'Survived':")
print(df['Survived'].value_counts())

# Function to find potential duplicates using fuzzy matching
def find_duplicates(dataframe, column, threshold=80):
    duplicates = []
    for i, name in enumerate(dataframe[column]):
        for j, other_name in enumerate(dataframe[column]):
            if i != j:  # Avoid self-comparison
                similarity = fuzz.token_sort_ratio(name, other_name)
                if similarity >= threshold:
                    duplicates.append((name, other_name, similarity))
    return duplicates

# Apply the function to the 'Name' column
potential_duplicates = find_duplicates(df, 'Name', threshold=80)

# Display potential duplicates
print("\nPotential Duplicates Found:")
for duplicate in potential_duplicates[:10]:  # Show only the first 10 for brevity
    print(duplicate)

# Deduplicate dataset by retaining unique names
unique_names = set()
deduplicated_rows = []

for _, row in df.iterrows():
    name = row['Name']
    if name not in unique_names:
        deduplicated_rows.append(row)
        unique_names.add(name)

# Create a new DataFrame with deduplicated rows
df_cleaned = pd.DataFrame(deduplicated_rows)

# Check the shape of the cleaned dataset
print("\nShape of Cleaned Dataset:")
print(df_cleaned.shape)

# Save the cleaned dataset
df_cleaned.to_csv('cleaned_data.csv', index=False)

print("\nCleaned dataset has been saved as 'cleaned_data.csv'.")
