from flask import Flask, request
from pypdf import PdfReader
import google.generativeai as genai
app = Flask(__name__)
genai.configure(API_KEY = "YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-2.0-flash")
@app.route("/")
def home():
    return """
    <h1>AI PDF Quiz Generator</h1>

    <form method="POST" action="/upload" enctype="multipart/form-data">
        <input type="file" name="pdf_file">
        <button type="submit">Upload PDF</button>
    </form>
    """
@app.route("/upload", methods=["POST"])
def upload():
    pdf = request.files["pdf_file"]

    file_path = f"uploads/{pdf.filename}"
    pdf.save(file_path)

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    lines = text.split(".")

    quiz = """
    <body style='font-family:Arial;padding:30px;background:#f5f5f5;'>

    <h1 style='color:#2c3e50;'>📚 AI Study Assistant</h1>

    <p>Upload your notes and automatically generate revision questions.</p>
    <hr>
    <h2>Generated Quiz</h2>
    """

    count = 1

    for line in lines:
       if len(line.strip()) > 20 and count <= 5:
           quiz += f"""
           <div style='margin-bottom:20px;border:1px solid gray;padding:10px;border-radius:10px;'>
                <h3>Question {count}</h3>
                <p>Explain: {line.strip()}?</p>

                <input type='radio' name='q1'> Strongly Understand
                <input type='radio' name='q1'> Partially Understand
                <input type='radio' name='q1'> Need More Practice
                <input type='radio' name='q1'> Don't Know
           </div>
           """
           count += 1

    quiz += """
    <br><br>
    <button style='padding:10px 20px;font-size:16px;'>
    Submit Quiz
    </button>

    </body>
    """

    return quiz
if __name__ == "__main__":
    app.run(debug=True)