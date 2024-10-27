from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

app = Flask(__name__)

# Cargar las variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Endpoint para analizar la imagen del INE
@app.route('/analyze_ine', methods=['POST'])
def analyze_ine_endpoint():
    data = request.json
    image_url = data.get('image_url')
    
    if not image_url:
        return jsonify({'success': False, 'error': 'No image URL provided'}), 400
    
    try:
        # Llamar a la función analyze_ine
        result = analyze_ine(image_url)
        return jsonify({'success': True, 'result': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# La función analyze_ine que interactúa con OpenAI
def analyze_ine(image_ine):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze the following image and extract the personal details visible on the ID card. Return the information in JSON format with the following fields: name, date_of_birth, sex, address, voter_id, curp, registration_year, state, municipality, section, locality, issue_year, and validity."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_ine,
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
