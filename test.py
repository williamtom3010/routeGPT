# import the libraries
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
import time
from groq import Groq
import psycopg2
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")



# Function to call API
def fetch_from_groq(prompt, model, api_key, temperature=0.3, max_new_tokens=1048):
    client = Groq(api_key=api_key)
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            max_tokens=max_new_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content if response.choices else None
    except Exception as e:
        return f"Error: {e}"

# Function to save data in PostgreSQLnew
def save_to_database(prmpt, response):
    conn = psycopg2.connect(
        dbname="your database name",
        user="postgres",
        password="input your password",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (PROMPT VARCHAR, GEN_ANS VARCHAR)''')
    cursor.execute("INSERT INTO users (PROMPT, GEN_ANS) VALUES (%s, %s)", (prmpt, response))
    conn.commit()
    conn.close()


def save_to_no_sql_database(prmpt, response):
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    # print(client)    

    db = client["User_database"]
    collection = db["User_sample_collection"]

    new_user = { 
            "input":prmpt,
            "response":response
            }

    collection.insert_one(new_user)
    # print("-------------------------------------------")


def main_app(prmpt, over_ride):

    tokens = word_tokenize(prmpt)
    no_of_tokens = len(tokens)

    if over_ride == "Yes":
        model_choice = st.selectbox("Choose your model", ["gemma2", "mixtral", "llama-3.1"])
        model_mapping = {"gemma2": "gemma2-9b-it", "mixtral": "mixtral-8x7b-32768", "llama-3.1": "llama-3.1-8b-instant"}
        model = model_mapping[model_choice]
    else:
        if no_of_tokens > 0 and no_of_tokens < 400:
            print("model_1")
            model = "gemma2-9b-it"
        elif no_of_tokens >= 400 and no_of_tokens < 800:
            print("model_2")
            model = "mixtral-8x7b-32768"
        else:
            print("model_3")
            model = "llama-3.1-8b-instant"

    # response = ""
    api_key = API_KEY
    
    response = fetch_from_groq(prmpt, model, api_key)
    return response