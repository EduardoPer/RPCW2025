# Backend & Frontend: app.py (Flask with Jinja templates)
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import random
import requests
from datetime import datetime

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
    now = datetime.now().timestamp()
    while not picked:
        random_rei_index = random.randrange(0, len(cognomes_all))
        random_cognome_index = random.randrange(0, len(cognomes_all[random_rei_index][1]))
        if (already_done.get('cognomes') is None):
            already_done['cognomes'] = [(random_rei_index, random_cognome_index)]
            picked = True
        elif ((random_rei_index, random_cognome_index) not in already_done['cognomes']):
            already_done['cognomes'].append((random_rei_index, random_cognome_index))
            picked = True
        elif (datetime.now().timestamp() - now > 5.0):
            return "Full"

    question['answer'] = cognomes_all[random_rei_index][1][random_cognome_index]
    question['question'] = f"Qual dos seguintes cognomes pertence {"à Rainha" if "A" in question['answer'].split(" ") else "ao Rei"} {cognomes_all[random_rei_index][0]}?"
    question['options'] = [question['answer']]
    i = 3
    now = datetime.now().timestamp()
    while i > 0:
        r_temp = random.randrange(0, len(cognomes_all))
        c_temp = random.randrange(0, len(cognomes_all[r_temp][1]))
        if (r_temp != random_rei_index) and (cognomes_all[r_temp][1][c_temp] not in question['options']) and (cognomes_all[r_temp][1][c_temp] not in cognomes_all[random_rei_index][1]):
            question['options'].append(cognomes_all[r_temp][1][c_temp])
            i-=1
        elif (datetime.now().timestamp() - now > 10.0):
            return "Full"
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
    now = datetime.now().timestamp()
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
        elif (datetime.now().timestamp() - now > 5.0):
            return "Full"
    
    question['question'] = f"@ monarca {random_final_tuple[1]} viveu na casa {random_final_tuple[0]}?"
    question['answer'] = "True" if random_final_tuple in casas_all else "False"
    question['options'] = ["True", "False"]
    
    return question

def query_2_pick_question():
    if not quiz_contents.get('batalhas'):
        sparql_query = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?nomeBatalha ?localBatalha ?resultadoBatalha WHERE {
        	?s a :Batalha ;
               :nome ?nomeBatalha ;
               :temLocal/:nome ?localBatalha ;
               :resultado ?resultadoBatalha .
        }
        """
        q_results = query_graphdb(endpoint, sparql_query)
        lista_content = list()
        for r in q_results['results']['bindings']:
            temp = (r['nomeBatalha']['value'].split('#')[-1], r['localBatalha']['value'].split('#')[-1], r['resultadoBatalha']['value'].split('#')[-1])
            lista_content.append(temp)
        quiz_contents['batalhas'] = lista_content
    
    batalhas, locais, resultados = [], [], []
    for b in quiz_contents['batalhas']:
        batalhas.append(b[0])
        locais.append(b[1])
        resultados.append(b[2])
    
    picked = False
    random_final_question = tuple()
    now = datetime.now().timestamp()
    while not picked:
        random_question = (random.choice(batalhas), random.choice(locais), random.choice(resultados))
        random_true_question = random.choice(quiz_contents['batalhas'])
        random_final_question = random.choice([random_question, random_true_question])
        if already_done.get('batalhas') is None:
            already_done['batalhas'] = [random_final_question]
            picked = True
        elif random_final_question not in already_done['batalhas']:
            already_done['batalhas'].append(random_final_question)
            picked = True
        elif (datetime.now().timestamp() - now > 5.0):
            return "Full"
    
    question = dict()
    question['question'] = f"A batalha denominada de {random_final_question[0]}, que ocorreu no local {random_final_question[1]}, teve o seu resultado dado como {random_final_question[2]}."
    question['answer'] = "True" if random_final_question in quiz_contents['batalhas'] else "False"
    question['options'] = ["True", "False"]
    
    return question

def query_3_pick_question():
    if not quiz_contents.get('descobrimentos'):
        sparql_query = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?notas ?data ?começoReinado ?fimReinado WHERE {
        	?s a :Descobrimento ;
               :notas ?notas ;
               :data ?data ;
               :temReinado/:comeco ?começoReinado ;
               :temReinado/:fim ?fimReinado .
        }
        """
        q_results = query_graphdb(endpoint, sparql_query)
        lista_content = list()
        for r in q_results['results']['bindings']:
            temp = (r['notas']['value'].split('#')[-1], r['data']['value'].split('#')[-1].replace(" ", "").replace("–", "-"), r['começoReinado']['value'].split('#')[-1].split(" ")[-1], r['fimReinado']['value'].split('#')[-1].split(" ")[-1])
            lista_content.append(temp)
        quiz_contents['descobrimentos'] = lista_content
    
    picked = False
    random_question = tuple()
    now = datetime.now().timestamp()
    while not picked:
        random_question = random.choice(quiz_contents['descobrimentos'])
        if already_done.get('descobrimentos') is None:
            already_done['descobrimentos'] = [random_question]
            picked = True
        elif random_question not in already_done['descobrimentos']:
            already_done['descobrimentos'].append(random_question)
            picked = True
        elif (datetime.now().timestamp() - now > 5.0):
            return "Full"
    
    options = [random_question[1]]
    i = 3
    now = datetime.now().timestamp()
    while i > 0:
        if "-" in random_question[1]:
            auxI = int(random_question[1].split("-")[0])
            auxF = int(random_question[1].split("-")[-1])
            diff = auxF - auxI
            
            auxI = int(random_question[2])
            auxF = int(random_question[3])
            
            optI = random.randint(auxI, auxF - diff)
            optF = optI + diff
            opt = str(optI) + "-" + str(optF)
            if opt not in options:
                options.append(opt)
                i-=1
                
        elif "ou" in random_question[1]:
            auxI = int(random_question[1].split("ou")[0])
            auxF = int(random_question[1].split("ou")[-1])
            diff = auxF - auxI
            
            auxI = int(random_question[2])
            auxF = int(random_question[3])
            
            optI = random.randint(auxI, auxF - diff)
            optF = optI + diff
            opt = str(optI) + "ou" + str(optF)
            if opt not in options:
                options.append(opt)
                i-=1
        elif (datetime.now().timestamp() - now > 10.0):
            return "Full"
        else:
            auxI = int(random_question[2])
            auxF = int(random_question[3])
            opt = str(random.randint(auxI, auxF))
            if opt not in options:
                options.append(opt)
                i-=1
    random.shuffle(options)
    
    question = {}
    question['options'] = options
    question['answer'] = random_question[1]
    question['question'] = f"Qual {"o período" if "-" in random_question[1] else "a data"} do seguinte descobrimento?\n'{random_question[0]}'"
    
    return question

def query_4_pick_question():
    if not quiz_contents.get('reinadosPorDinastia'):
        sparql_query = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT ?nomeDinastia (count (?reinado) as ?nReinados) WHERE {
        	?s a :Dinastia ;
               :nome ?nomeDinastia.
            ?reinado a :Reinado ;
               :dinastia ?s .
        } group by ?nomeDinastia
        """
        q_results = query_graphdb(endpoint, sparql_query)
        lista_content = list()
        for r in q_results['results']['bindings']:
            temp = (r['nomeDinastia']['value'].split('#')[-1], r['nReinados']['value'].split('#')[-1])
            lista_content.append(temp)
        quiz_contents['reinadosPorDinastia'] = lista_content
    
    auxL = [] 
    for nR in quiz_contents['reinadosPorDinastia']:
        auxL.append(int(nR[1]))
    auxL.sort()
    max = auxL[-1]
    
    picked = False
    random_question = tuple()
    random_num = int()
    now = datetime.now().timestamp()
    while not picked:
        random_question = random.choice(quiz_contents['reinadosPorDinastia'])
        random_num = random.choice([random.randint(1, max), int(random_question[1])])
        if (already_done.get('reinadosPorDinastia') is None):
            already_done['reinadosPorDinastia'] = [(random_question[0], str(random_num))]
            picked = True
        elif ((random_question[0], str(random_num)) not in already_done['reinadosPorDinastia']):
            if random_question not in already_done['reinadosPorDinastia']:
                already_done['reinadosPorDinastia'].append((random_question[0], str(random_num)))
                picked = True
        elif (datetime.now().timestamp() - now > 5.0):
            return "Full"
    
    question = {}
    question['question'] = f"Ao longo da dinastia {random_question[0]} ocorreram {str(random_num)} reinados."
    question['answer'] = str(random_question[1] == str(random_num))
    question['options'] = ["True", "False"]
    
    return question

def query_5_pick_question():
    if not quiz_contents.get('reiDisnastia'):
        sparql_query = """
        PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        select DISTINCT ?nomeRei ?dinastia where {
            ?s a ?o .
            FILTER(?o = :Rei || ?o = :Rainha)
            ?s :nome ?nomeRei ;
               :temReinado/:dinastia/:nome ?dinastia .
        }
        """
        q_results = query_graphdb(endpoint, sparql_query)
        lista_content = list()
        for r in q_results['results']['bindings']:
            temp = (r['nomeRei']['value'].split('#')[-1], r['dinastia']['value'].split('#')[-1])
            lista_content.append(temp)
        quiz_contents['reiDisnastia'] = lista_content
    
    dinastiasSet = set()
    for _, d in quiz_contents['reiDisnastia']:
        dinastiasSet.add(d)
    
    random_reis = []
    correct_answers = []
    now = datetime.now().timestamp()
    i = 4
    while i > 0:
        random_rei_din = random.choice(quiz_contents['reiDisnastia'])
        if (already_done.get('reiDisnastia') is None):
            already_done['reiDisnastia'] = [random_rei_din]
            random_reis.append(random_rei_din[0])
            correct_answers.append(random_rei_din)
            i-=1
        elif (random_rei_din not in already_done['reiDisnastia']):
            already_done['reiDisnastia'].append(random_rei_din)
            random_reis.append(random_rei_din[0])
            correct_answers.append(random_rei_din)
            i-=1
        elif (datetime.now().timestamp() - now > 5.0):
            return "Full"
    
    question = {}
    question['question'] = f"Corresponda cada rei à dinastia na qual governou"
    question['left_items'] = random_reis
    question['right_items'] = dinastiasSet
    question['correct_matches'] = correct_answers
    
    return question
    

available_questions = [query_0_pick_question, query_1_pick_question, query_2_pick_question, query_3_pick_question, query_4_pick_question, query_5_pick_question]
#################################################################
@app.route('/')
def home():
    session['score'] = 0
    reset_dicts()
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET'])
def generate_question():
    question_type = random.choice(available_questions)
    question = question_type()
    now = datetime.now().timestamp()
    while (question == "Full") and (datetime.now().timestamp() - now <= 5):
        print(f"Removed {str(question_type)} from the question type pool")
        available_questions.remove(question_type)
        question_type = random.choice(available_questions)
        question = question_type()
    
    if question != "Full":
        if question_type == query_5_pick_question:
            return render_template('quiz_match.html', question=question)
        else:
            return render_template('quiz.html', question=question)
    else:
        return render_template('score.html', score=session.get('score', 0))

@app.route('/quiz', methods=['POST'])
def quiz():
    if request.form.get('match') == "True":
        user_answer = [request.form.get('match_1'), request.form.get('match_2'), request.form.get('match_3'), request.form.get('match_4')]
        correct_answer = [request.form.get('correct_match_1'), request.form.get('correct_match_2'), request.form.get('correct_match_3'), request.form.get('correct_match_4')]
        correct = (correct_answer == user_answer)
    else:
        user_answer = request.form.get('answer')
        correct_answer = request.form.get('correct_answer')
        correct = (correct_answer == user_answer)
    
    session['score'] = session.get('score', 0) + (1 if correct else 0)
    return render_template('result.html', question=request.form.get('question') , correct_answer=correct_answer, user_answer=user_answer, score=session['score'])

@app.route('/score')
def score():
    return render_template('score.html', score=session.get('score', 0))

if __name__ == '__main__':
    app.run(debug=True)
