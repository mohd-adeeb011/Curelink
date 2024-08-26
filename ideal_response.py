import openai
import json
import os
# Load the JSON data
with open("output_data.json", 'r') as file:
    data = json.load(file)

output = []
# Set up the OpenAI API key
openai.api_key = "Your API Key"
# Generate a response using OpenAI
for i in range(len(data)):
    patient_profile = data[i]["patient_profile"]
    query_time = data[i]["query_time"]
    meals_to_take = data[i]["meals_to_take"]
    user_query = data[i]["user_query"]

    prompt = f'''
<Persona:>
You are a professional dietician who is knowledgeable, supportive, and focused on helping patients achieve their health goals through proper diet adherence.

<Task:>
Assess the patient's current meal description against the prescribed diet plan meals and offer constructive response accordingly like if there are some prescribed meals and elements missing then ask and question about it, if all the meals and prescribed elements are present then encourage and compliment them.

<Exemplar:>
Below are the few example responses.
- "Great job for having methi water, continue having it daily, it will help boost your metabolism.\nVarsha, but i also noticed that you are having figs and raisins but they are not      presrcibed in the diet plan, can i know why you have added them ?
- "Varsha, i noticed you are having upma instead of poha as prescribed in your diet plan, can you let me know why ?"
- "Shobhita, I noticed aap oats le rhe ho, which is a healthy choice, but maine aapki diet mein aloo parantha + curd likha tha, aapne vo nhi khaya ?",
- "Great job on following your diet plan, keep it up!"
- "Good job, coconut water is great source of potassium. Why have you not included seeds with this ?

<Inputs:>
- Patient's Current Meal Description: ```{user_query}```
- Suggested Meal for This Time: ```{meals_to_take}```

<Format:>
- The response should be very comprehensive, brief and to the point. The response should be in the same language as of patients's query lanugage.

    '''

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" or "gpt-4" depending on your access
        messages=[
            {"role": "system", "content": "You are a dietician providing dietary feedback."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # You can adjust the length of the response
        temperature=0.7,  # Control the creativity of the response
        top_p=0.9,  # Control the diversity of the response
        frequency_penalty=0,
        presence_penalty=0
    )
    
    generated_reponse = response.choices[0].message['content'].strip()
    output.append({
            "ticket_id" : data[i]["ticket_id"],
            "latest_query" : user_query,
            "generated_response" : generated_reponse,
            "ideal_response" : data[i]["ideal_response"],
        }
    )

with open("output_data.json", 'w') as file:
    json.dump(output, file, indent=4)
    


