import csv
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_cors import CORS  # Import the CORS module
import json
app = Flask(__name__)
CORS(app)
import time
import os

import hashlib
import requests
from flask import Flask, render_template
import random
from bs4 import BeautifulSoup
import wget
import os
# Global variable to store data
#data = pd.DataFrame()
import zipfile
import os

zip_file_name = "static/static.zip"
extracted_dir = "static/"

with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir)
# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))+"/static"
def fetch_pexels_image(query):
    search_url = f'https://www.google.com/search?q={query}&tbm=isch'
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract image URLs from the search results (using data-src attribute)
        image_tags = soup.find_all('img')
        for image_tag in image_tags:
            
            image_url = image_tag['src']
            if  image_url.startswith('http'):
                nu=random.randint(999999,99999999)
                
                wget.download(image_url,out="static/"+str(nu)+'.png')
                
                return "/static/"+str(nu)+".png"
    
    # Return a placeholder image URL if no image with data-src is found
    return 'https://via.placeholder.com/150'
def save_to_excel(file_name, excel_data):
    file_path = os.path.join(script_dir, file_name)
    excel_data.to_excel(file_path, index=False)
    print(f"Data saved to {file_path}")

def read_from_excel(file_name):
    global data
    file_path = os.path.join(script_dir, file_name)
    try:
        return pd.read_excel(file_path)
        print(f"Data read from {file_path}")
    except FileNotFoundError:
        print(f"File {file_path} not found. Creating a new one.")
        data.to_excel(file_path, index=False)
        return pd.read_excel(file_path)
# Flask route to save data
@app.route('/save_data', methods=['POST'])
def save_data():
    file_name = request.args.get('filename')
    file = request.files['file']

    try:
        excel_data = pd.read_excel(file)
        save_to_excel(file_name, excel_data)
        return jsonify({"message": f"Data saved to {file_name}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to process Excel file. {str(e)}"}), 400

# Flask route to get the data
@app.route('/get_data', methods=['GET'])
def get_data():
    file_name = request.args.get('filename')
    
    return jsonify(read_from_excel(file_name).to_dict(orient='records'))


    
categories = [
    {"name": "Category 1", "description": "Description 1", "image": "work01-hover.jpg"},
    {"name": "Category 2", "description": "Description 2", "image": "work02-hover.jpg"},
    {"name": "Category 3", "description": "Description 3", "image": "work03-hover.jpg"},
    {"name": "Category 4", "description": "Description 4", "image": "work01-hover.jpg"},
{"name": "Category 5", "description": "Description 5", "image": "work02-hover.jpg"},
    {"name": "Category 6", "description": "Description 6", "image": "work03-hover.jpg"},

    # Add more categories as needed
] 

import pickle
filename="datas3.pickle"
with open(filename, 'rb') as file:
        global_vars = pickle.load(file)
for var_name, var_value in global_vars.items():
        globals()[var_name] = var_value



   

@app.route('/')
def homepage():
    return render_template('index.html')
@app.route('/work')
def work():
     category = request.args.get('category')
     sections=lestext[category]

 #   return render_template('work.html',category=category,category_first_description_244_73=txts["category_first_description_244_73"],category_second_description_103_30=txts["category_second_description_103_30"],category_first_question_28_5=txts["category_first_question_28_5"],category_first_answer_276_94=txts["category_first_answer_276_94"],category_second_question_41_6=txts["category_first_question_41_6"],category_second_answer_345_136=txts["category_second_answer_345_136"],category_conclusion_103_33=txts["category_conclusion_103_33"],category_introduction_103_33=["category_introduction_103_33"])
     return render_template('work.html',category=category, sections=sections) 
@app.route('/works')
def works():
   try: 
    return render_template('works.html', categories=categories)#,categories0=categories[0], categories1=categories[1],categories2=categories[2],categories3=categories[3],categories4=categories[4],categories5=categories[5])
   except Exception as err:
       return str(err)
@app.route('/about')
def about():
    return render_template('about.html')   
@app.route('/contact')
def contact():
    return render_template('contact.html')        
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')  
@app.route('/components.html')
def components():
    return render_template('components.html')    
@app.route('/index.html')
def index():
    return render_template('index.html')      
@app.route('/<string:page_name>')
def html_page(page_name):
 try:   
  if   page_name=="work.html":
    category = request.args.get('category') 
    return redirect(url_for(page_name.replace(".html",""), category=category)) 
  else:    
    return redirect(url_for(page_name.replace(".html",""))) 
 except Exception as me:
     return str(me)


# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email},{subject},{message}')


def write_to_csv(data):
    with open('database.csv', 'a', newline='') as csvfile:
        email = data['email']
        subject = data['subject']
        message = data['message']
        writer = csv.writer(csvfile)
        writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return 'Something went wrong!'
if __name__ == '__main__':
    app.run(debug=True)      
