from flask import Flask, render_template, request, jsonify
from task import extract_ingredients_to_metta, recommend
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    user_input = request.form.get('ingredients', '').strip()
    if not user_input:
        return jsonify({'error': 'Please enter some ingredients!'})
    
    # Extract ingredients
    ingredients = extract_ingredients_to_metta(user_input)
    
    # Get recommendations
    result = recommend(ingredients)
    
    return jsonify({
        'ingredients': ingredients,
        'recommendations': result
    })

if __name__ == '__main__':
    app.run(debug=True) 