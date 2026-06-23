from flask import Flask, request
from pypdf import PdfReader 
app = Flask(__name__)

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

    import os

    file_path = os.path.join("uploads", pdf.filename)
    pdf.save(file_path)

    try:
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
          text += page.extract_text() or ""

    except Exception as e:
        return f"<h2>Error reading PDF:</h2><p>{e}</p>"

    lines = text.split(".")

    quiz = """
    <body style='font-family:Arial;padding:30px;background:#f5f5f5;'>

    <h1 style='color:#2c3e50;'>📚 AI Study Assistant</h1>

    <p>Upload your notes and automatically generate revision questions.</p>
    <hr>
    <h2>Generated Quiz</h2>

    <form method="POST" action="/result">
    """


    count = 1

    for line in lines:
       if len(line.strip()) > 20 and count <= 5:
           quiz += f"""
           <div style='margin-bottom:20px;border:1px solid gray;padding:10px;border-radius:10px;'>
                <h3>Question {count}</h3>
                <p>Explain: {line.strip()}?</p>

                <input type='radio' name='q{count}' value='4'> Strongly Understand
                <input type='radio' name='q{count}' value='3'> Partially Understand
                <input type='radio' name='q{count}' value='2'> Need More Practice
                <input type='radio' name='q{count}' value='1'> Don't Know
           </div>
           """
           count += 1

    quiz += """
    <br><br>
    <button type='submit' style='padding:10px 20px;font-size:16px;'>
    Submit Quiz
    </button>
    </form>

    </body>
    """

    return quiz

@app.route("/result", methods=["POST"])
def result():

    total_score = 0
    weak_questions = []

    for i in range(1, 6):
        answer = int(request.form.get(f"q{i}", 0))
        total_score += answer

        if answer <= 2:
            weak_questions.append(i)

    percentage = (total_score / 20) * 100

    report = f"""
    <body style='font-family:Arial;padding:30px;'>

    <h1>📊 Study Report</h1>

    <h2>Study Score: {percentage:.0f}%</h2>

    """

    if weak_questions:
        report += f"""
        <h3>Need Revision:</h3>
        <p>Focus on Questions: {', '.join(map(str, weak_questions))}</p>
        """
    else:
        report += """
        <h3>Excellent!</h3>
        <p>You seem confident with all topics.</p>
        """

    report += "</body>"

    return report

if __name__ == "__main__":
    app.run(debug=True)