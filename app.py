import csv
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
import openai
import time
# Set your OpenAI API key
openai.api_key = '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'
def chat_with_gpt(prompt):
   # prompt = f"generer un text descriptif apropos des condoleances avec un peux pres  244 characteres et 73 mots"
    print(prompt)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150  # Adjust as needed
    )
    time.sleep(61)
    print(response)
    return response.choices[0].text.strip()
    
categories = [
    {"name": "Category 1", "description": "Description 1", "image": "work01-hover.jpg"},
    {"name": "Category 2", "description": "Description 2", "image": "work02-hover.jpg"},
    {"name": "Category 3", "description": "Description 3", "image": "work03-hover.jpg"},
    {"name": "Category 4", "description": "Description 4", "image": "work01-hover.jpg"},
{"name": "Category 5", "description": "Description 5", "image": "work02-hover.jpg"},
    {"name": "Category 6", "description": "Description 6", "image": "work03-hover.jpg"},

    # Add more categories as needed
] 
prompt={
     "category_description_119_15":lambda category:"generer un text explicatif  de "+category+" avec un peux pres  119 characteres et 15 mots",
     "category_first_description_244_73":lambda category:"generer un text descriptif apropos "+category+" avec un peux pres  244 characteres et 73 mots",
        "category_second_description_103_30":lambda category:"generer un text descriptif apropos "+category+" avec un peux pres  103 characteres et 30 mots",
        "category_introduction_103_33":lambda category:"generer un text introduction  apropos "+category+" avec un peux pres  103 characteres et 33 mots",
        "category_first_question_28_5":lambda category:"generer une question educatrice  apropos "+category+" avec un peux pres  28 characteres et 5 mots",
        "category_first_answer_276_94":lambda question:"generer une reponse educatrice  a la question "+question+" avec un peux pres  276 characteres et 94 mots",
        "category_first_question_41_6":lambda category:"generer une question educatrice  apropos "+category+" avec un peux pres  41 characteres et 6 mots",
        "category_second_answer_345_136":lambda question:"generer une reponse educatrice  a la question "+question+" avec un peux pres  345 characteres et 136 mots",
        "category_conclusion_103_33":lambda category:"generer un text conclusion  apropos "+category+" avec un peux pres  103 characteres et 33 mots"
       }
lescategories=eval(chat_with_gpt("generer un code list python de 6 categories du sujet de condoleances sans descrition ou commentaires sans declaration variable"))
lestext={}
for i in lescategories:
 categories["name"]=i
 categories["name"]= chat_with_gpt(categories["category_description_119_15"](i))
 texts={}   
 for j in prompt.keys():    
   if not "answer" in j:  
    texts[j]=chat_with_gpt(prompt[j](i))
   else:
    texts[j]=chat_with_gpt(prompt[j](list(texts.values())[-1]))  
 lestext[i]["texts"]=texts   



   

@app.route('/')
def homepage():
    return render_template('index.html')
@app.route('/work')
def work():
    category = request.args.get('category')
    txts=lestext[category]["texts"]
    return render_template('work.html',category=category,category_first_description_244_73=category+txts["category_first_description_244_73"],category_second_description_103_30=category+txts["category_second_description_103_30"],category_first_question_28_5=category+txts["category_first_question_28_5"],category_first_answer_276_94=category+txts["category_first_answer_276_94"],category_second_question_41_6=category+txts["category_second_question_41_6"],category_second_answer_345_136=category+txts["category_second_answer_345_136"],category_conclusion_103_33=category+txts["category_conclusion_103_33"])
@app.route('/works')
def works():
   try: 
    return render_template('works.html',categories0=categories[0], categories1=categories[1],categories2=categories[2],categories3=categories[3],categories4=categories[4],categories5=categories[5])
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
