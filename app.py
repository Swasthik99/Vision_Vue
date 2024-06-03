from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'team14'  

show_eye_chart_options = False
selected_eye_chart = None
distance_result = None  # Variable to store the result of distance.py
snellen_chart_results = None  # Variable to store the result of snellen_chart_results.txt
gesture_results = None

# MySQL configuration
db_config = {
    'user': 'root',  
    'password': 'shreya',
    'host': 'localhost',
    'database': 'patient'
}

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('start_test_page'))
    return render_template('index.html', show_eye_chart_options=show_eye_chart_options)

@app.route('/', methods=['GET', 'POST'])
def patient_details():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        date = request.form['date']
        phone = request.form['phone']

        session['patient_info'] = {'name': name, 'age': age, 'date': date, 'phone': phone}

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the table
        query = "INSERT INTO details (Name, Age, Date, Phone_no) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, age, date, phone))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('home'))
    return render_template('patient_details.html')

@app.route('/eye-chart-selection', methods=['POST'])
def eye_chart_selection():
    global show_eye_chart_options
    show_eye_chart_options = True
    return render_template('index.html', show_eye_chart_options=show_eye_chart_options)

@app.route('/start-test', methods=['POST'])
def start_test():
    global selected_eye_chart
    selected_eye_chart = request.form.get('eye_chart')
    return redirect(url_for('test_page', eye_chart=selected_eye_chart))

@app.route('/test-page/<eye_chart>')
def test_page(eye_chart):
    global snellen_chart_results, distance_result, gesture_results
    if eye_chart == 'snellen':
        return render_template('snellen_test_page.html', distance_result=distance_result, snellen_chart_results=snellen_chart_results)
    elif eye_chart == 'e-chart':
        return render_template('e_chart_test_page.html', gesture_results=gesture_results)
    else:
        return "Invalid eye chart type"

@app.route('/run-distance', methods=['POST'])
def run_distance():
    global distance_result
    subprocess.run(['python', 'distance.py'])
    with open("average_distance.txt", "r") as file:
        distance_result = file.read()
    return render_template('snellen_test_page.html', distance_result=distance_result)

@app.route('/run-voice-test', methods=['POST'])
def run_voice_test():
    global snellen_chart_results
    subprocess.run(['python', 'snellen_voice.py'])
    with open("snellen_chart_results.txt", "r") as file:
        snellen_chart_results = file.read()

        # Update the Snellen_result column in the database
    patient_info = session.get('patient_info')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE details SET Snellen_result = %s WHERE Name = %s AND Phone_no = %s"
    cursor.execute(query, (snellen_chart_results, patient_info['name'], patient_info['phone']))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('show_result', content=snellen_chart_results))

@app.route('/run-e-chart', methods=['POST'])
def run_e_chart():
    global gesture_results

    subprocess.run(['python', 'e_chart_new.py'])

    with open("gesture_results.txt", "r") as file:
        gesture_results = file.read()

         # Update the E_result column in the database
    patient_info = session.get('patient_info')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE details SET E_result = %s WHERE Name = %s AND Phone_no = %s"
    cursor.execute(query, (gesture_results, patient_info['name'], patient_info['phone']))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('show_result', content=gesture_results))

@app.route('/result', methods=['GET'])
def show_result():
    file_content = request.args.get('content')
    patient_info = session.get('patient_info', {})
    return render_template('result_page.html', file_content=file_content, patient_info=patient_info)

if __name__ == '__main__':
    app.run(debug=True)
