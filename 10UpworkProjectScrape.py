import json
from bs4 import BeautifulSoup

def parse_job_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    base_url = "https://www.upwork.com"  # Base URL for Upwork
    job_data = []

    # Find all sections that contain job postings
    job_sections = soup.find_all('section', class_='air3-card-section')

    for section in job_sections:
        job = {}
        job['Job ID'] = section.get('data-ev-opening_uid', 'N/A')
        posted_time_span = section.find('span', {'data-test': 'posted-on'})
        job['Posted Time'] = posted_time_span.text.strip() if posted_time_span else 'N/A'
        job_title_h3 = section.find('h3', class_='job-tile-title')
        job['Job Title'] = job_title_h3.text.strip() if job_title_h3 else 'N/A'
        relative_url = job_title_h3.find('a')['href'] if job_title_h3 and job_title_h3.find('a') else 'N/A'
        job['Job URL'] = base_url + relative_url if relative_url != 'N/A' else 'N/A'
        job['Job Type'] = section.find('small', {'data-test': 'job-type'}).text.strip() if section.find('small', {'data-test': 'job-type'}) else 'N/A'
        job['Budget or Rate'] = section.find('span', {'data-test': 'budget'}).text.strip() if section.find('span', {'data-test': 'budget'}) else 'N/A'
        job['Estimated Time or Duration'] = section.find('span', {'data-test': 'duration'}).text.strip() if section.find('span', {'data-test': 'duration'}) else 'N/A'
        job['Job Description'] = section.find('span', {'data-test': 'job-description-text'}).text.strip() if section.find('span', {'data-test': 'job-description-text'}) else 'N/A'
        job['Skills/Tokens'] = [token.text.strip() for token in section.find_all('a', class_='air3-token')] if section.find_all('a', class_='air3-token') else []
        job['Payment Verification Status'] = 'Verified' if section.find('small', {'data-test': 'payment-verification-status'}) else 'Not Verified'
        job['Client Spending'] = section.find('span', {'data-test': 'formatted-amount'}).text.strip() if section.find('span', {'data-test': 'formatted-amount'}) else 'N/A'
        job['Client Location'] = section.find('small', {'data-test': 'client-country'}).text.strip() if section.find('small', {'data-test': 'client-country'}) else 'N/A'
        job['Proposals Count'] = section.find('strong', {'data-test': 'proposals'}).text.strip() if section.find('strong', {'data-test': 'proposals'}) else 'N/A'

        job_data.append(job)

    return job_data

def filter_jobs_with_valid_id(job_data):
    # Remove jobs where 'Job ID' is 'N/A'
    return [job for job in job_data if job['Job ID'] != 'N/A']

def read_and_parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        html_content = file.read()
        parsed_data = parse_job_data(html_content)
        return parsed_data

def save_json_to_file(json_data, file_path):
    filtered_data = filter_jobs_with_valid_id(json_data)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, indent=4)
    return "Data saved successfully."


# Path to the HTML file and JSON output file
html_file_path = 'storage/UpworkProjectDataSource.txt'
json_output_file_path = 'storage/UpworkProject.json'

# Read, parse, and save the JSON data
parsed_data = read_and_parse_file(html_file_path)
save_result = save_json_to_file(parsed_data, json_output_file_path)
print(save_result)
