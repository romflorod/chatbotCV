from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
import os
import binascii
import sqlite3

app = Flask(__name__)

# Clave API codificada en binario
binary_api_key = "01000001 01001001 01111010 01100001 01010011 01111001 01000001 01001011 01000111 01001101 01000001 01110001 01011010 01101101 01000100 00110001 01111001 01111010 01100101 01110011 01010001 01001000 01000110 01010100 01001101 00111000 01010000 01010111 01100001 01110011 01000001 01110101 01101011 01100110 01011000 01111000 01010000 01101000 01000101"

# Decodificar la clave API
API_KEY = ''.join([chr(int(b, 2)) for b in binary_api_key.split()])
if not API_KEY:
    raise ValueError("No API_KEY found. Set GEMINI_API_KEY in environment variables.")

genai.configure(api_key=API_KEY)

# Inicializa el modelo de Gemini
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# Contexto inicial para el asistente
initial_context = (
    "You are a virtual assistant who exclusively knows the CV and professional background of Román Flores Rodríguez. "
    "Your responses must be based solely on his qualifications, experience, and skills, and provided in the language requested. "
    "Here is the relevant information: "

    "Román Flores Rodríguez is a highly skilled Generative AI Engineer & High Responsibility Engineer at NTT Data, "
    "specialized in Spring Boot, software architecture, GitHub Copilot, and DevOps practices. "
    "Born in Seville, Spain, in 1999, he has over four years of experience in Java development and is also proficient in Python, JavaScript, and TypeScript. "
    "He has deep expertise in modern web development with frameworks such as React.js and Vue.js, as well as backend technologies like Django and Spring Boot. "

    "As a full-stack developer, Román excels in designing scalable, maintainable, and high-performance applications. "
    "He has significant experience in cloud-native architectures, microservices, and containerization with Docker and Kubernetes. "
    "His work focuses on integrating AI-driven automation, business intelligence, and decision-support systems using Large Language Models (LLMs), "
    "prompt engineering, and AI technologies such as TensorFlow, Keras, ChatGPT, and DALL-E. "

    "Román has designed and delivered high-impact training sessions on GitHub Copilot, particularly in Spring environments. "
    "He actively contributes to enhancing development workflows through automation, continuous integration/delivery (CI/CD), and DevOps best practices, "
    "with strong expertise in platforms like Azure and cloud deployment strategies. "

    "Holding a degree in Computer Engineering with a focus on Software Engineering from the Universidad de Sevilla, "
    "Román is committed to continuous learning, participating in courses and workshops on AI, cloud computing, and full-stack development. "
    "He has extensive experience working with relational databases such as PostgreSQL, MySQL, SQLite, SQL Server, and Oracle, specializing in database design, optimization, and querying. "

    "Beyond his technical skills, Román is experienced in agile methodologies, particularly Scrum, and has led cross-functional teams to successful software delivery. "
    "He is also knowledgeable in cybersecurity, including ethical hacking and securing applications against vulnerabilities. "
    
    "Fluent in Spanish (native), highly proficient in English, and with intermediate French skills, Román is an active contributor to the tech community, "
    "regularly engaging in hackathons, forums, and meetups. His passion for AI extends to NLP, computer vision, reinforcement learning, and ethical AI deployment. "

    "Román is known for his adaptability, fast learning, and resilience in tackling complex challenges. "
    "He consistently delivers high-value solutions through technical innovation and leadership. "
    "For contact, mail him at romanflodriguez@gmail.com or connect via LinkedIn: https://www.linkedin.com/in/roman-flores-6856ba268/. "
)

# Crear la base de datos y la tabla para almacenar los prompts
def init_db():
    conn = sqlite3.connect('prompts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Define el manejador de errores 404 para redirigir a la página principal
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['message']
        prompt = initial_context + " " + user_input
        
        # Guardar el prompt en la base de datos
        conn = sqlite3.connect('prompts.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prompts (prompt) VALUES (?)', (user_input,))
        conn.commit()
        conn.close()

        response = model.generate_content(prompt)

        if response and hasattr(response, 'text'):
            return jsonify({'response': response.text})
        else:
            return jsonify({'response': "Sorry, but I think Gemini didn't want to answer that!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Sorry, but Gemini didn't want to answer that!"})

# No incluir app.run(), ya que PythonAnywhere maneja la ejecución con WSGI
#if __name__ == '__main__':
#    app.run(debug=True)