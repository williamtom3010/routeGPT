# Context-Aware Multi-LLM Chatbot

A **Streamlit-based chatbot** that intelligently routes user queries to the most suitable Large Language Model (LLM) based on the prompt length (token count). The application also allows users to manually override the automatic model selection. All user prompts and generated responses are stored in both **PostgreSQL** and **MongoDB** for persistence and future analysis.

---

# Prerequisites

## 1. Create a Python Environment

Create and activate a Conda environment, then install the required dependencies.

```bash
pip install -r requirements.txt
```

---

## 2. Project Structure

Ensure that the following files are located in the same directory:

- `app.py`
- `test.py`

> **Note:** `app.py` imports `test.py`, so both files must remain in the same folder.

---

## 3. Install PostgreSQL and MongoDB

### PostgreSQL (pgAdmin 4)

Install PostgreSQL and pgAdmin 4 by following the guide below:

https://www.youtube.com/watch?v=4qH-7w5LZsA

### MongoDB

Install MongoDB by following the guide below:

https://www.youtube.com/watch?v=KYIOJrE3zjk

These databases are used to store user prompts and generated responses.

---

## 4. Configure PostgreSQL

Create a new PostgreSQL database using pgAdmin 4.

Update the database connection in your code:

```python
conn = psycopg2.connect(
    dbname="YOUR_DATABASE_NAME",
    user="postgres",
    password="YOUR_PASSWORD",
    host="localhost",
    port="5432"
)
```

Replace:

- `YOUR_DATABASE_NAME` with your PostgreSQL database name.
- `YOUR_PASSWORD` with your PostgreSQL password.

Unless modified during installation, the following values remain unchanged:

- **User:** `postgres`
- **Host:** `localhost`
- **Port:** `5432`

---

# Running the Application

Start the Streamlit application by running:

```bash
streamlit run app.py
```

This command launches the chatbot interface in your default web browser.

---

# Application Workflow

## Step 1: User Input

The user enters a prompt through the Streamlit interface.

Example:

> Explain the difference between supervised and unsupervised learning.

---

## Step 2: Model Selection

The application asks whether the user wants to manually select an LLM.

### Override Mode

If the user chooses **Yes**, a list of available models is displayed.

The selected model is used to generate the response.

---

### Automatic Model Selection

If the user chooses **No**, the application automatically selects the most suitable model based on the prompt length.

```python
if no_of_tokens > 0 and no_of_tokens < 400:
    model = "gemma2-9b-it"

elif no_of_tokens >= 400 and no_of_tokens < 800:
    model = "mixtral-8x7b-32768"

else:
    model = "llama-3.1-8b-instant"
```

This eliminates the need for users to manually choose an LLM for every query.

---

## Step 3: Response Generation

The selected model is invoked through the Groq API, and the generated response is displayed in the Streamlit interface.

---

## Step 4: Data Storage

After the response is generated, both the user prompt and the generated response are stored in:

- PostgreSQL
- MongoDB

---

# Project Structure

```
.
├── app.py
├── test.py
├── requirements.txt
└── README.md
```

---

# File Descriptions

## `app.py`

This file contains the Streamlit application.

Responsibilities:

- Launches the GUI.
- Accepts user prompts.
- Handles manual model selection (Override Mode).
- Calls functions defined in `test.py`.

---

## `test.py`

This file contains the backend logic of the application.

### `fetch_from_groq(prompt, model, api_key, temperature=0.3, max_new_tokens=1048)`

- Sends the user's prompt to the selected Groq LLM.
- Returns the generated response.

---

### `save_to_database(prompt, response)`

- Stores the user prompt and generated response in the PostgreSQL database.

---

### `save_to_no_sql_database(prompt, response)`

- Stores the user prompt and generated response in the MongoDB database.

---

### `main_app(prompt, override)`

This is the main processing function.

Responsibilities:

1. Receives the user's prompt.
2. Calculates the number of tokens (or words) in the prompt.
3. Checks whether Override Mode is enabled.
4. If Override Mode is enabled, the user-selected model is used.
5. Otherwise, an appropriate model is automatically selected based on the prompt length.
6. Calls the Groq API to generate the response.
7. Saves the prompt and response to PostgreSQL.
8. Saves the prompt and response to MongoDB.
9. Returns the generated response to the Streamlit interface.

---

# Features

- Context-aware LLM selection
- Manual model override
- Automatic model routing based on prompt length
- Streamlit-based graphical user interface
- Groq API integration
- PostgreSQL integration
- MongoDB integration
- Persistent storage of prompts and responses
- Modular and easy-to-extend project architecture