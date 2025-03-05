# Backend & Frontend: app.py (Flask with Jinja templates)
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import random
import requests

app = Flask(__name__)
app.secret_key = 'História de Portugal'
CORS(app)

# Mock questions for now
test_questions = [
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh", "Claude Monet"],
        "answer": "Leonardo da Vinci"
    },
    {
        "question": "Albert Einstein was born in Germany.",
        "options": ["True", "False"],
        "answer": "True"
    },
    {
        "question": "In which year did World War II end?",
        "options": ["1942", "1945", "1939", "1950"],
        "answer": "1945"
    }
]

############################ QUERIES ############################
def query_graphdb(endpoint_url, sparql_query):
    # Set up the headers
    headers = {
        'Accept': 'application/json',  # You can change this based on the response format you need
    }
    
    # Make the GET request to the GraphDB endpoint
    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON response from the GraphDB endpoint
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
endpoint = "http://localhost:7200/repositories/HistoriaPT"
quiz_contents = dict()
already_done = dict()

def reset_dicts():
    quiz_contents.clear()
    already_done.clear()

def query_0_pick_question():
    if not quiz_contents.get('cognomes'):
        sparql_query = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?nomeRei ?cognomesRei WHERE {
        	?s a ?o .
            FILTER(?o = :Rei || ?o = :Rainha)
            ?s :nome ?nomeRei ;
               :cognomes ?cognomesRei .
        }
        """
        q_results = query_graphdb(endpoint, sparql_query)

        lista_content = list()
        for r in q_results['results']['bindings']:
            temp = (r['nomeRei']['value'].split('#')[-1], r['cognomesRei']['value'].split('#')[-1].split(','))
            lista_content.append(temp)
        quiz_contents['cognomes'] = lista_content
    
    cognomes_all = quiz_contents['cognomes']
    question = {}
    random_rei_index = int()
    random_cognome_index = int()
    
    picked = False
    while not picked:
        random_rei_index = random.randrange(0, len(cognomes_all))
        random_cognome_index = random.randrange(0, len(cognomes_all[random_rei_index][1]))
        if (already_done.get('cognomes') is None):
            already_done['cognomes'] = [(random_rei_index, random_cognome_index)]
            picked = True
        elif ((random_rei_index, random_cognome_index) not in already_done['cognomes']):
            already_done['cognomes'].append((random_rei_index, random_cognome_index))
            picked = True

    question['answer'] = cognomes_all[random_rei_index][1][random_cognome_index]
    question['question'] = f"Qual dos seguintes cognomes pertence {"à Rainha" if "A" in question['answer'].split(" ") else "ao Rei"} {cognomes_all[random_rei_index][0]}?"
    question['options'] = [question['answer']]
    i = 3
    while i > 0:
        r_temp = random.randrange(0, len(cognomes_all))
        c_temp = random.randrange(0, len(cognomes_all[r_temp][1]))
        if (r_temp != random_rei_index) and (cognomes_all[r_temp][1][c_temp] not in question['options']) and (cognomes_all[r_temp][1][c_temp] not in cognomes_all[random_rei_index][1]):
            question['options'].append(cognomes_all[r_temp][1][c_temp])
            i-=1
    random.shuffle(question['options'])
    return question

def query_1_pick_question():
    if not quiz_contents.get('casas'):
        sparql_query = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?nomeCasa ?nomeRei WHERE {
        	?s a :Casa ;
               :nome ?nomeCasa ;
               :temElemento/:nome ?nomeRei .
        }
        """
        q_results = query_graphdb(endpoint, sparql_query)
        lista_content = list()
        for r in q_results['results']['bindings']:
            temp = (r['nomeCasa']['value'].split('#')[-1], r['nomeRei']['value'].split('#')[-1])
            lista_content.append(temp)
        quiz_contents['casas'] = lista_content
    
    casas_all = quiz_contents['casas']
    casas, monarcas = [], []
    for c in casas_all:
        casas.append(c[0])
        monarcas.append(c[1])
    
    question = {}
    picked = False
    random_final_tuple = tuple()
    while not picked:
        random_tuple = (random.choice(casas), random.choice(monarcas))
        random_true_tuple = random.choice(casas_all)
        random_final_tuple = random.choice([random_tuple, random_true_tuple])
        
        if (already_done.get('casas') is None):
            already_done['casas'] = [random_final_tuple]
            picked = True
        elif random_final_tuple not in already_done['casas']:
            already_done['casas'].append(random_final_tuple)
            picked = True
    
    question['question'] = f"@ monarca {random_final_tuple[1]} viveu na casa {random_final_tuple[0]}?"
    question['answer'] = "True" if random_final_tuple in casas_all else "False"
    question['options'] = ["True", "False"]
    
    return question
        
#################################################################    
    

@app.route('/')
def home():
    session['score'] = 0
    reset_dicts()
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET'])
def generate_question():
    return render_template('quiz.html', question=random.choice([query_0_pick_question(), query_1_pick_question()]))

@app.route('/quiz', methods=['POST'])
def quiz():
    user_answer = request.form.get('answer')
    correct_answer = request.form.get('correct_answer')
        
    correct = (correct_answer == user_answer)
    session['score'] = session.get('score', 0) + (1 if correct else 0)
    return render_template('result.html', correct=correct, question=request.form.get('question') , correct_answer=correct_answer, user_answer=user_answer, score=session['score'])

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)
