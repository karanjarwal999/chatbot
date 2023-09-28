from flask import Flask, render_template , request ,jsonify
import os
import openai
import json
app = Flask(__name__)
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

openai.api_key = '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'

def load_data():
    with open('data.json', 'r') as file:
        History = json.load(file)
        return History["History"]
    
def load_current():
    with open('data.json', 'r') as file:
        History = json.load(file)
        return History["current"]
    
# Save data to JSON files
def save_data():
    with open('data.json', 'w') as file:
        json.dump({"current":current,"History":History}, file, indent=4)


History=load_data()
current=load_current()


@app.route('/')
def home_route():
    return render_template('index.html',data=current)

@app.route('/history', methods=['GET'])
def history_route():
    return History

@app.route('/currentChat', methods=['GET'])
def currentChat_route():
    return current

@app.route('/newChat', methods=['GET'])
def newChat_route():
    global current
    if(len(current)>3):
        id = now.strftime("%d/%m/%Y %H:%M:%S")
        History.append({"id":id,"data":current})
        current=[  
            {"role": "system",
                "content": "you are chatbot but you have to behave like a sellsman  at flipkart , if quary is not related to e-commerce website then repones should not data found for this quary"},
            {"content": 'hii', "role": 'user'}, 
            {"content": 'Hello! Welcome to Flipkart. How can I assist you today?', "role": 'assistant'}
        ]
        save_data()
        
    return "new chat created successfully"


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json['user_input']
    current.append({"role": "user", "content": user_input})
    save_data()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=current,
        temperature=0.99,
        max_tokens=256,
        top_p=0.4,
        frequency_penalty=0.99,
        presence_penalty=0.99
    )
    chatbot_response = response.choices[0].message['content'].strip()
    current.append({"role": "assistant", "content": chatbot_response})
    save_data()
    return current

if __name__ == '__main__':
    app.run(debug=True)