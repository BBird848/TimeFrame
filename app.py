from flask import Flask, abort, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/subjects")
def subjects():
    return render_template("subjects.html")

@app.route("/generate", methods=["POST"])
def generate():
    selected_grade = request.form.get("grade", type=int)
    if selected_grade not in range(7, 13):
        abort(400, description="Please select a grade between 7 and 12.")

    selected_subjects = request.form.getlist("subjects")

    print("Selected grade:", selected_grade)
    print("Selected subjects:", selected_subjects)

    return render_template(
        "timetable.html",
        grade=selected_grade,
        subjects=selected_subjects,
        selected_grade=selected_grade,
        selected_subjects=selected_subjects,
    )

if __name__ == "__main__":
    app.run(debug=True)

