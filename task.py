import os
import google.generativeai as genai
from dotenv import load_dotenv
from hyperon import *

# Load environment variables at the start
load_dotenv()

def initialize_metta():
    try:
        metta = MeTTa()
        with open('data.metta', 'r') as file:
            content = file.read()
            metta.run(content)
        
        metta.run('''(= (pattern $par)
        (let* (
                ($val (match &self ($x $y $z $w) ($x $y $z $w)))
                ($ingredient (index-atom $val 1))
        )
        (if (== () (subtraction-atom $ingredient $par)) $val (empty))
        ))''')
        return metta
    except FileNotFoundError:
        raise Exception("data.metta file not found. Please ensure the file exists in the correct location.")
    except Exception as e:
        raise Exception(f"Error initializing MeTTa: {str(e)}")

metta = initialize_metta()

def extract_ingredients_to_metta(user_input):
    try:
        # Configure Gemini API using environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        response = model.generate_content(f"""
        Extract all food ingredients from this user input, capitalize each one, 
        and format them as a python string of MeTTa expression (space-separated in parentheses).
        Only return the MeTTa expression, nothing else. ensure that each ingredient is in singular format
        
        User input: "{user_input}"
        
        Example 1: 
        Input: "I have eggs, flour and milk"
        Output: (Eggs Flour Milk)
        
        Example 2:
        Input: "my ingredients are tomato, pasta, cheese"
        Output: (Tomato Pasta Cheese)
        If no ingredients found, return: ()
        you should consider the content of the input example input: "i have neither banana nor meat" output: ()
        """,
        )
        return response.text
    except Exception as e:
        raise Exception(f"Error extracting ingredients: {str(e)}")

def recommend(ing):
    try:
        value = metta.run(f'!(pattern {ing})')
        if str(value) == '[[]]':
            return "Sorry, you have insufficient ingredients"
        
        result = []
        for val in value[0]:
            food, ingredients, time, restriction = val.get_children()
            ingredients = ','.join(map(str, ingredients.get_children()))
            result.append(f'You can cook {food} with {ingredients} in {time}min if you are {restriction}.')
        return '\n'.join(result)
    except Exception as e:
        raise Exception(f"Error getting recommendations: {str(e)}")

if __name__ == "__main__":
    try:
        print("Welcome to recipe recommender")
        x = input("Enter ingredients you have: ")
        
        my_ingredients = extract_ingredients_to_metta(x)
        print(my_ingredients)
        
        result = recommend(my_ingredients)
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")