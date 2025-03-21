from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Route to render the frontend
@app.route('/')
def home():
    return render_template('index.html')

# Route to scrape and process data
@app.route('/scrape', methods=['POST'])
def scrape_and_process():
    url = request.json['url']
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch the webpage."}), 400

    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    
    # Summarize the text
    summary = summarizer(text[:1000], max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
