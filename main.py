import requests
import json
from bs4 import BeautifulSoup
import random
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

#Base Url
jooble_url = f'https://jooble.org/api/{api_key}'

# List of U.S. states with their full names
state_names = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 
    'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 
    'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 
    'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 
    'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 
    'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 
    'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 
    'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Randomly select 10 state names from the list
selected_states = random.sample(list(state_names.values()), 10)

# Get user input for their job search keyword (e.g., major)
major = input("Enter keyword: ")

# List to store collected job data
jobs_collected = []

# Loop through each selected state and query for job listings
for state in selected_states:
    # JSON query body to get jobs based on the major and state
    query_params = {
        "keywords": major,
        "location": state
    }
    
    # Make the POST request to Jooble API
    response = requests.post(jooble_url, json=query_params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response from Jooble
        job_data = response.json()
        
        # Check if there are job listings for the state
        if len(job_data['jobs']) > 0:
            # Collect the first job returned in the response
            job = job_data['jobs'][0]  # Get the first job
            
            # Extract job title and location
            job_title = job.get('title', 'Unknown')
            job_location = job.get('location', 'Unknown')
            
            # Store the job details in the jobs_collected list
            jobs_collected.append((job_title, job_location, state, job))  # Store job details
    else:
        # Print an error message if the API request fails
        print(f"Error: {response.status_code} - {response.reason}")

# URL for the crime rate data by state
crime_rate_url = 'https://worldpopulationreview.com/state-rankings/crime-rate-by-state'

# Request the crime rate page
response = requests.get(crime_rate_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all rows in the crime rate table with relevant data-state attribute
    rows = soup.find_all('tr', {'data-state': 'false'})  # Select rows with state data

    # Dictionary to store state crime data
    state_crime_data = {}

    # Loop through each row to collect crime data
    for row in rows:
        # Get all table columns in the row
        columns = row.find_all('td')
        
        # Ensure the row has enough columns to include the crime data
        if len(columns) >= 4:
            state_name = row.find('th').text.strip()  # Get the state name
            crime_reported = columns[3].text.strip().replace(',', '')  # Get the crime reported (4th column)
            
            # Store the crime data for the state in the dictionary
            state_crime_data[state_name] = float(crime_reported)
for job in jobs_collected:
    job_title, job_location, job_state, job_data = job
    
    # Check if the job's state is in the crime data
    if job_state in state_crime_data:
        crime_rate = state_crime_data[job_state]
    else:
        # Print a message if no crime data is found for the state
        print(f"Crime data for {job_state} not found.\n")

# Create a set of states that have jobs to filter cost of living data
job_states = {job[2] for job in jobs_collected}

# URL for the cost of living index by state
url = 'https://worldpopulationreview.com/state-rankings/cost-of-living-index-by-state'

# Request the cost of living page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all rows in the cost of living table with relevant data-state attribute
    rows = soup.find_all('tr', {'data-state': 'false'})  # Select rows with state data

    # List to store cost of living data
    cost_of_living_data = []

    # Loop through each row and extract the cost of living index
    for row in rows:
        state = row.find('th').text.strip()  # Get the state name
        cost_index = row.find_all('td')[0].text.strip()  # Get the cost of living index
        
        # Only append the state if it has job listings
        if state in job_states:
            cost_of_living_data.append((state, cost_index))
else:
    # Print a message if the request for cost of living data fails
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Create a list to store rows for the final DataFrame
data_rows = []

# Collect job data along with crime and cost of living information
for job in jobs_collected:
    job_title, job_location, job_state, job_data = job
    
    # Get crime rate data or 'Unavailable' if not present
    crime_rate = state_crime_data.get(job_state, 'Unavailable')
    
    # Get cost of living data or 'Unavailable' if not present
    cost_of_living_index = next((cost for state, cost in cost_of_living_data if state == job_state), 'Unavailable')

    # Collect job ID and apply link
    job_id = job_data.get('id', 'Unknown')  # Get the job ID or 'Unknown'
    apply_link = job_data.get('link', 'Unknown')  # Get the apply link or 'Unknown'

    # Append the collected data as a dictionary
    data_rows.append({
        'State': job_state,
        'Job Title': job_title,
        'Link to Apply': apply_link,
        'Crime Rate (Out of 100000)': crime_rate,
        'Cost of Living Index (Compared to a mean of 100)': cost_of_living_index
    })

# Create a DataFrame from the collected data
df_jobs = pd.DataFrame(data_rows)

# Replace NaN values with 'Unavailable'
df_jobs.fillna('Unavailable', inplace=True)

#Create a CSV File for the data
print(df_jobs)
df_jobs.to_csv('jobs_data.csv', index=False)
