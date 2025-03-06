# filepath: d:\cv_chatbot\app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
import os

app = Flask(__name__)

# Solicita la clave de API de Gemini por consola
API_KEY = input('Please enter your Gemini API key: ')
if not API_KEY:
    raise ValueError("No API_KEY provided. Please enter the GEMINI_APIKEY.")

genai.configure(api_key=API_KEY)

# Inicializa el modelo de Gemini
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# Contexto inicial para el asistente
initial_context = (
    "You are a virtual assistant that exclusively knows the CV and professional experience of Román Flores Rodríguez. "
    "You must provide information based only on his background, expertise, and skills, and respond in the language in which you are asked. "
    "Here is the relevant information: "
    "Román Flores Rodríguez is a Generative AI Engineer & High Responsibility Engineer at NTT Data, specializing in "
    "Spring Boot, software architecture, GitHub Copilot, and Git administration. "
    "He was born in Seville, Spain in 1999 and is currently seeking positions with compensation around 26,000 euros annually. "
    "He has over four years of experience developing in Java and is also proficient in Python and JavaScript. "
    "He is a full-stack developer with extensive knowledge of multiple technologies and frameworks. "
    "His expertise includes working with generative AI, implementing automation solutions, and conducting training courses on GitHub Copilot, "
    "particularly in Spring environments. He has deep knowledge in AI automation and integration. "
    "Román is an expert in Large Language Models (LLMs), prompt engineering, and AI application development, keeping up with the latest advancements in the field. "
    "He holds a degree in Computer Engineering with a focus on Software Engineering from Universidad de Sevilla. "
    "His digital skills include backend development (Django, Spring Boot), frontend (HTML, JavaScript), AI (TensorFlow, Keras, ChatGPT, DALL-E), "
    "and database management (PostgreSQL, SQLite, SQL Server, MySQL, Oracle). "
    "He is highly skilled in automation and AI-driven solutions, optimizing workflows and improving efficiency through intelligent systems. "
    "Román is an agile practitioner familiar with Scrum methodologies and has ethical hacking knowledge. "
    "He is a passionate self-learner, results-oriented, and highly adaptable to new technologies and challenges. "
    "He consistently delivers high value to projects through innovation, problem-solving, and technical leadership. "
    "Román has also worked on various projects involving cloud computing, microservices architecture, and containerization using Docker and Kubernetes. "
    "He has experience with CI/CD pipelines and DevOps practices, ensuring smooth and efficient software delivery. "
    "Regarding languages, Román is a native Spanish speaker with a high proficiency level in English (both written and spoken) and medium proficiency in French. "
    "He has contributed to open-source projects and has a strong presence in the developer community. "
    "Román is also knowledgeable in machine learning and data science, having worked with libraries such as scikit-learn, pandas, and NumPy. "
    "He has implemented several successful AI solutions using state-of-the-art techniques, demonstrating practical applications of theoretical AI concepts. "
    "He has a keen interest in emerging technologies and continuously seeks to expand his skill set through ongoing education and practical projects. "
    "Román is known for his excellent communication skills, ability to work under pressure, and commitment to delivering high-quality results."
)

# Define tu manejador de errores 404 para redirigir a la página principal
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.route('/')
def home():
    # Renderiza la plantilla HTML para la página principal
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Obtiene el mensaje del usuario desde el formulario
        user_input = request.form['message']
        prompt = initial_context + " " + user_input

        # Genera la respuesta usando el modelo de Gemini
        response = model.generate_content(prompt)

        if response and hasattr(response, 'text'):
            return jsonify({'response': response.text})
        else:
            return jsonify({'response': "Sorry, but I think Gemini didn't want to answer that!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Sorry, but Gemini didn't want to answer that!"})

if __name__ == '__main__':
    # Inicia la aplicación Flask en modo de depuración
    app.run(host='0.0.0.0', port=8080)
