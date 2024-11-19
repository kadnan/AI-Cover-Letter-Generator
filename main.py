from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from google.ai.generativelanguage_v1beta.types import content
from textwrap import dedent

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def cover_letter_form():
    if request.method == 'POST':
        COVER_LETTER_PROMPT = """
        You are a skilled freelancer with expertise in writing cover letters that have successfully helped you secure many jobs. Your task is to craft a compelling cover letter that persuades the client to contact you. It should utilize persuasive techniques and convey that the freelancer is focused on delivering results and helping achieve goals, rather than solely pursuing monetary gain.

        You will be provided with information in JSON format, which will serve as the foundation for constructing the cover letter:

        {{
          "Name": "{name}",
          "JobTitle": "{jobTitle}",
          "PrimarySkills": {primarySkills},
          "Experience": {experience},
          "ClientJobPost": "{clientJobPost}",
          "RelevantProjects": {relevantProjects},
          "ClientName": "{clientName}",
          "StartDate": "{startDate}",
          "Deadline": "{deadline}",
          "Tone": "{tone}"
        }}
        """
        data = request.get_json()
        # Format the prompt with the data
        formatted_prompt = COVER_LETTER_PROMPT.format(
            name=data['name'],
            jobTitle=data['jobTitle'],
            primarySkills=str(data['primarySkills']),  # Convert list to string
            experience=data['experience'],
            clientJobPost=data['clientJobPost'].replace("\n", "\\n"),  # Escape newlines
            relevantProjects=str(data['relevantProjects']),  # Convert list to string
            clientName=data['clientName'],
            startDate=data['startDate'],
            deadline=data['deadline'],
            tone=data['tone']
        )

        generation_config = {
            "response_schema": content.Schema(
                type=content.Type.OBJECT,
                properties={
                    "answer": content.Schema(
                        type=content.Type.STRING,
                    ),
                },
            ),
            "response_mime_type": "application/json",
        }
        genai.configure(api_key=os.environ["GEMINI_KEY"])
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config=generation_config
        )
        response = model.generate_content(formatted_prompt)
        # Example: Print the received data (replace with processing logic)
        print(f"Name: {data.get('name')}")
        print(f"Job Title: {data.get('jobTitle')}")
        print(f"Primary Skills: {data.get('primarySkills')}")
        print(f"Experience: {data.get('experience')}")
        print(f"Client Job Post: {data.get('clientJobPost')}")
        print(f"Relevant Projects: {data.get('relevantProjects')}")
        print(f"Client Name: {data.get('clientName')}")
        print(f"Start Date: {data.get('startDate')}")
        print(f"Deadline: {data.get('deadline')}")
        print(f"Tone: {data.get('tone')}")
        return jsonify(response.text)


if __name__ == '__main__':
    app.run(debug=True)
