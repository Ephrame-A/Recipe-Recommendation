import os
import google.generativeai as genai
from google import genai
from dotenv import load_dotenv
from hyperon import *

metta=MeTTa()

with open('data.metta', 'r') as file:
    content = file.read()
    metta.run(content)
# test=metta.run('!(match &self ($x $y $z $w) ($x $y $z $w))')

metta.run('''(= (pattern $par)
(let* (
        ($val (match &self ($x $y $z $w) ($x $y $z $w)))
        ($ingredient (index-atom $val 1))
)
(if (== () (subtraction-atom $ingredient $par)) $val (empty))
))''')

load_dotenv()

def extract_ingredients_to_metta(user_input):
    # Configure Gemini API using environment variable
  

# Configure Gemini
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
    Extract all food ingredients from this user input, capitalize each one, 
    and format them as a MeTTa expression (space-separated in parentheses).
    Only return the MeTTa expression, nothing else. ensure that each ingredient is in singular format
    
    User input: "{user_input}"
    
    Example 1: 
    Input: "I have eggs, flour and milk"
    Output: (Eggs Flour Milk)
    
    Example 2:
    Input: "my ingredients are tomato, pasta, cheese"
    Output: (Tomato Pasta Cheese)
    If no ingredients found, return: ()
    you should consider the contect of the input example input: "i have neither banana nor meat" output: ()
    """,
    )
    return response.text
x=input()
print(extract_ingredients_to_metta(x))