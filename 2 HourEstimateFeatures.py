#2 HourEstimateFeatures.py
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from OpenAIModels.Complexity import complexity

def parse_complexity_category(complexity_string):
    categories = {
        "Very Simple": 2,
        "Simple": 4,
        "Moderately Complex": 6,
        "Complex": 8,
        "Very Complex": 12,
        "Unknown": 0  # Default case if no keyword is found
    }
    for category in categories:
        if category in complexity_string:
            return category, categories[category]
    return "Unknown", 0

def Complexity_Analysis(Tasks, SubFeature, Feature):
    system_context = "You're an AI trained to analyze software development tasks and estimate their complexity. Your task is to categorize each task into one of the following complexity levels: Very Simple, Simple, Moderately Complex, Complex, Very Complex."
    assistant_context = (
        "Rules: Provide the complexity level as your response. Choose from one of these five categories: "
        "'Very Simple' for tasks that are extremely easy and quick to complete, "
        "'Simple' for tasks that are straightforward without much complexity, "
        "'Moderately Complex' for tasks that require a moderate amount of time and effort, "
        "'Complex' for tasks that are challenging and time-consuming, "
        "'Very Complex' for tasks that are extremely challenging and require a significant amount of time and expertise. "
        "Example responses: 'Very Simple', 'Simple', 'Moderately Complex', 'Complex', 'Very Complex'. "
        "Only Provide one of these tags as your response based on the task description."
    )
    initial_prompt = f"Please indicate the complexity of the Task: {Tasks} for the Feature: {Feature} and SubFeature: {SubFeature}."

    complexity_string = complexity(system_context, assistant_context, initial_prompt)
    complexity_category, hours = parse_complexity_category(complexity_string)
    return complexity_category, hours

def load_json_Hours(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_json_Hours(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved successfully in {filename}.")

def process_task(feature, subfeature, feature_name, task_key=None):
    if "EstimatedHours" in feature:
        return feature["EstimatedHours"]

    task_description = feature["TaskDescription"] if task_key is None else feature["TaskDescription"][task_key]
    complexity_category, hours = Complexity_Analysis(task_description, subfeature, feature_name)

    if task_key is None:
        feature["TaskDescription"] = {"Description": task_description, "EstimatedHours": hours}
    else:
        feature["TaskDescription"][task_key]["EstimatedHours"] = hours

    return hours
def process_feature(feature_list):
    feature_list_id = feature_list['FeatureListID']
    total_hours_for_feature_list = 0  # Initialize total hours for this feature list
    task_futures = []

    with ThreadPoolExecutor() as task_executor:
        for feature in feature_list['Features']:
            subfeature = feature["SubFeature"]
            feature_name = feature["Feature"]
            task_description = feature["TaskDescription"]
            task_name = feature.get("TaskName", "Unnamed Task")  # Retrieve the task name

            print(f"Processing Task: {task_name} in Feature: {feature_name}, SubFeature: {subfeature}")

            if isinstance(task_description, dict):
                for task_key in task_description:
                    if "EstimatedHours" not in task_description[task_key]:
                        future = task_executor.submit(process_task, feature, subfeature, feature_name, task_key)
                        task_futures.append(future)
            else:
                if "EstimatedHours" not in feature:
                    future = task_executor.submit(process_task, feature, subfeature, feature_name)
                    task_futures.append(future)

        # Wait for all tasks to complete and aggregate hours
        for future in as_completed(task_futures):
            hours = future.result()
            total_hours_for_feature_list += hours

    # Update the total hours for the feature list
    feature_list['TotalHours'] = total_hours_for_feature_list
    return feature_list

def main():
    feature_lists = load_json_Hours('storage/FeatureListDatabase.json')
    processed_feature_lists = []

    # Using ThreadPoolExecutor to process each feature list concurrently
    with ThreadPoolExecutor() as executor:
        # Submit each feature list processing task to the executor
        future_to_feature_list = {executor.submit(process_feature, feature_list): feature_list for feature_list in feature_lists}

        # Process the results as they complete
        for future in as_completed(future_to_feature_list):
            processed_feature_list = future.result()
            processed_feature_lists.append(processed_feature_list)

    # Save the processed feature lists and calculate total estimated hours
    save_json_Hours(processed_feature_lists, 'storage/HourEstimate.json')
    total_estimated_hours = sum(feature_list['TotalHours'] for feature_list in processed_feature_lists)
    print(f"Total Estimated Hours for the Project: {total_estimated_hours}")

if __name__ == "__main__":
    main()