from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import time
app = Flask(__name__)

# Function to delete a record 
def delete_record(topic):
    # Open the meetings.txt file in read mode
    with open('meetings.txt', 'r') as file:
        # Read the content of the file and convert it to a list of dictionaries
        data = json.loads("[" + file.read()[:-1].replace("\n", ",") + "]")

    found = False
    # Iterate through the list of meetings
    for record in data:
        # Check if the topic matches the given topic
        if 'topic' in record and record['topic'] == topic:
            # If a matching topic is found, remove the record
            data.remove(record)
            found = True
            break
    
    # If the topic is not found 
    if not found:
        print("Topic not found")
        return
    
    # Write the updated data back to the meetings.txt file
    with open('meetings.txt', 'w') as file:
        # Convert the list of dictionaries back to JSON format and write to file
        formatted = (json.dumps(data)[1:-1].replace("}, {", "}\n{"))
        if formatted:
            file.write(formatted + "\n")
        else:
            file.write(formatted)

# Function to update a record 
def update_record(topic, new_data):
    # Open the meetings.txt file in read mode
    with open('meetings.txt', 'r') as file:
        # Read the content of the file and convert it to a list of dictionaries
        data = json.loads("[" + file.read()[:-1].replace("\n", ",") + "]")
        
    found = False
    # Iterate through the list of meetings
    for record in data:
        # Check if the topic matches the given topic
        if 'topic' in record and record['topic'] == topic:
            # Update the record with the new data
            record.update(new_data)
            found = True
            break
    
    # If the topic is not found in any record, print a message
    if not found:
        print("Topic not found")
        return
    
    # Write the updated data back to the meetings.txt file
    with open('meetings.txt', 'w') as file:
        # Convert the list of dictionaries back to JSON format and write to file
        formatted = (json.dumps(data)[1:-1].replace("}, {", "}\n{"))
        file.write(formatted + "\n")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':# If the request is a POST request
        
        meeting = request.json
        if meeting.get('operation') == 1:
            # If operation is 1, it indicates adding a new meeting
            with open('meetings.txt', 'a') as file:
                file.write(str(meeting).replace("'", '"') + '\n')
        if meeting.get('operation') == 2: # update
            # If operation is 2, it indicates updating an existing meeting
            update_record(meeting.get('ex_topic'), request.json)
        if meeting.get('operation') == 3: # delete
            # If operation is 3, it indicates deleting an existing meeting
            delete_record(meeting.get('topic'))
        time.sleep(1)
        return redirect(url_for('index'))

    else:# If it's a GET request
        
        meetings = []
        with open('meetings.txt', 'r') as file:
            for line in file:
                if line != '\n':
                    meetings.append(eval(line))  
        return render_template('client.html', meetings=meetings)

if __name__ == '__main__':
    app.run(debug=True)
