import json
from datetime import datetime
import os

# Load JSON data
try:
    with open("textdata.json", 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: The file 'textdata.json' was not found.")
    data = []
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    data = []

def find_order(query_time_of_patient, plan_start_date):
    try:
        # Convert 'query_time_of_patient' to a datetime object
        time_of_query_date = datetime.strptime(query_time_of_patient, "%B %d, %Y, %I:%M %p")

        # Convert 'plan_start_date' to a datetime object
        plan_start_date_date = datetime.strptime(plan_start_date, "%Y-%m-%dT%H:%M:%SZ")

        # Extract only the date part from both datetime objects
        time_of_query_date = time_of_query_date.date()
        plan_start_date_date = plan_start_date_date.date()

        # Calculate the difference in days
        difference_in_days = (time_of_query_date - plan_start_date_date).days

        # Determine the order
        order = difference_in_days + 1
        print(f"ORDER : {order}")
        return order
    except ValueError as e:
        print(f"Error parsing dates: {e}")
        return None

def find_meals_by_order(order_number, i):
    orders_list = data[i].get("profile_context", {}).get("diet_chart", {}).get("meals_by_days", [])
    for meal_day in orders_list:
        if meal_day.get("order") == order_number:
            return meal_day.get("meals", []), orders_list
    return None, orders_list

def is_within_60_minutes(query_time, meal_time):
    """
    Check if the query time is within 60 minutes of the meal time.
    """
    fmt = '%I:%M %p'
    query_time = datetime.strptime(query_time, fmt)
    meal_time = datetime.strptime(meal_time, fmt)
    
    # Calculate the difference in time
    time_difference = abs((query_time - meal_time).total_seconds())
    
    # Check if the difference is within 60 minutes (3600 seconds)
    return time_difference <= 3600

def get_meal_names_around_query_time(query_time_of_patient, meals):
    meal_names = []
    if meals is None:
        return meal_names

    # Extract the time portion from 'query_time_of_patient'
    query_time_only = datetime.strptime(query_time_of_patient, "%B %d, %Y, %I:%M %p").strftime("%I:%M %p")

    for meal in meals:
        if is_within_60_minutes(query_time_only, meal.get("timings", "")):
            for meal_option in meal.get("meal_options", []):
                for item in meal_option.get("meal_option_food_items", []):
                    food_name = item.get("Food", {}).get("name", "Unknown Food Item")
                    meal_names.append(food_name)
                
    return meal_names

# Initialize a list to hold the relevant data for output
output_data = []

# Process each entry in the data
for i in range(len(data)):

    try:
        query_time_of_patient = data[i]["chat_context"]["chat_history"][-1]["timestamp"]
        plan_start_date = data[i]["profile_context"]["diet_chart"]["start_date"]
        patient_profile = data[i]["profile_context"]["patient_profile"]

        print(patient_profile)
        print(query_time_of_patient)
        print(plan_start_date)

        order_number = find_order(query_time_of_patient, plan_start_date)

        if order_number is None:
            print(f"Skipping entry {i} due to invalid order number calculation.")
            continue

        meals, meals_by_days = find_meals_by_order(order_number, i)

        meal_names = get_meal_names_around_query_time(query_time_of_patient, meals)

        food_description = data[i]
        # Collect the relevant data
        user_contents = [query["content"] for query in data[i]["latest_query"] if query["role"] == "user"]

        # Combine the extracted content into a single string
        all_content = "\n".join(user_contents)
        output_data.append({
            "ticket_id" : data[i]["chat_context"]["ticket_id"],
            "patient_profile": patient_profile,
            "query_time": query_time_of_patient,
            "plan_start_date": plan_start_date,
            "meals_to_take" : meal_names,
            "ideal_response" : data[i]["ideal_response"],
            "user_query" : all_content,
        })

        print(f"Meal Period is around {query_time_of_patient} and the recommended meals are {meal_names}")
        print("========================================================================")
        
    except KeyError as e:
        print(f"Error processing entry {i}: Missing key {e}")
    except Exception as e:
        print(f"Unexpected error processing entry {i}: {e}")

# Write the collected data to a JSON file
with open("output_data.json", 'w') as file:
    json.dump(output_data, file, indent=4)

print("Relevant data has been written to 'output_data.json'")


# for i in data:
#     response = [for i in data[i]["ideal_response"]]
#     all_response = "\n".join(response)