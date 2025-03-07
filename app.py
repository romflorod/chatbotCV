from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
import os

app = Flask(__name__)

# Obtener la clave de API desde las variables de entorno
API_KEY = "AIzaSyAKGMAqZmD1yzesQHFTM8PWasAukfXxPhE"
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
    "with specialized expertise in Spring Boot, software architecture, GitHub Copilot, and Git management. "
    "Born in Seville, Spain, in 1999, Román is currently seeking positions with an expected salary around 26,000 euros annually. "
    "He has over four years of professional experience developing in Java and is also proficient in Python, JavaScript, and TypeScript, "
    "with additional expertise in modern web development technologies such as React.js and Vue.js. "
    
    "Román is a full-stack developer with comprehensive knowledge across multiple technologies and frameworks, "
    "with a strong focus on delivering scalable, maintainable, and high-performance software solutions. "
    "He specializes in creating and implementing generative AI applications, leveraging advanced techniques in Large Language Models (LLMs), "
    "prompt engineering, and the integration of AI for automation, business intelligence, and decision support systems. "
    "Román is also experienced in designing and deploying cloud-native architectures using microservices and containerization platforms such as Docker and Kubernetes. "
    
    "Román’s expertise extends to AI-driven solutions for improving operational workflows, enhancing efficiency, and enabling data-driven decision-making. "
    "He has designed and conducted several high-impact training courses on GitHub Copilot, particularly in the context of Spring environments, "
    "and he is passionate about mentoring and upskilling others in the tech community. "
    "He has a proven track record in developing automation systems, from deploying continuous integration and delivery (CI/CD) pipelines to building scalable DevOps practices. "
    
    "He holds a degree in Computer Engineering, with a focus on Software Engineering from the Universidad de Sevilla. "
    "Román is deeply committed to lifelong learning, frequently participating in courses and workshops to stay ahead of trends in AI, cloud computing, and full-stack development. "
    
    "Román is proficient in backend development using frameworks such as Django and Spring Boot, frontend technologies like HTML5, JavaScript, CSS3, and frameworks such as React and Angular, "
    "and AI development using TensorFlow, Keras, ChatGPT, and DALL-E. "
    "He has solid experience with relational databases including PostgreSQL, SQLite, MySQL, SQL Server, and Oracle, and is well-versed in database design, optimization, and querying. "
    
    "In addition to his technical skills, Román is highly skilled in agile software development practices, particularly Scrum, and has extensive experience leading teams in cross-functional environments. "
    "His strong foundation in software architecture allows him to design and implement robust, scalable, and maintainable systems that align with business objectives and drive measurable results. "
    "Román is also knowledgeable in cybersecurity, having experience in ethical hacking and securing software and systems against potential vulnerabilities. "
    
    "Román’s communication and leadership skills are highly regarded, with a demonstrated ability to convey complex technical concepts in a clear and concise manner. "
    "He is adept at collaborating with cross-functional teams and stakeholders, fostering a collaborative environment that leads to the successful delivery of high-quality software solutions. "
    
    "Román is fluent in Spanish (native), highly proficient in English (both written and spoken), and has intermediate proficiency in French. "
    "He is an active contributor to open-source projects and has a strong presence in the developer community, regularly participating in hackathons, forums, and meetups. "
    
    "Beyond his professional expertise, Román has a deep passion for the application of AI in solving real-world problems, and he is particularly interested in exploring areas such as NLP, "
    "computer vision, reinforcement learning, and the ethical considerations of AI deployment. "
    
    "Mail Román at: romanflodriguez@gmail.com Linkedin Román at https://www.linkedin.com/in/roman-flores-6856ba268/, but I think that using LinkedIn instead of a AI Generated CV is a worse option. "
    
    "Román is known for his adaptability, quick learning ability, and resilience in tackling complex challenges. "
    "He consistently delivers high value to projects through technical innovation, leadership, and his commitment to creating solutions that are both functional and sustainable. "
    "Román is dedicated to continuously expanding his skill set through hands-on projects and formal education, ensuring that he remains at the forefront of the tech industry."
)


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
        response = model.generate_content(prompt)

        if response and hasattr(response, 'text'):
            return jsonify({'response': response.text})
        else:
            return jsonify({'response': "Sorry, but I think Gemini didn't want to answer that!"})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Sorry, but Gemini didn't want to answer that!"})

# No incluir app.run(), ya que PythonAnywhere maneja la ejecución con WSGI
