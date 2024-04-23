from flask import Flask, render_template, request
from Recommender import ResearchInterestRecommender

app = Flask(__name__)
recommender = ResearchInterestRecommender()
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_student_ids', methods=['GET'])
def get_student_ids():
    student_id = request.args.get('student_id')
    recommendations = recommender.recommend_professors(student_id, top_n=3)
    if isinstance(recommendations, str):
        return render_template('error.html', message=recommendations)
    elif not recommendations.empty:  # Check if recommendations DataFrame is not empty
        return render_template('recommendations.html', recommended_people=recommendations.to_dict(orient='records'), context='Professor Recommendations')
    else:
        return render_template('error.html', message="No recommendations found.")
@app.route('/get_professor_ids', methods=['GET'])
def get_professor_ids():
    professor_id = request.args.get('professor_id')
    recommendations = recommender.recommend_students(professor_id, top_n=3)
    if isinstance(recommendations, str):
        return render_template('error.html', message=recommendations)
    elif not recommendations.empty:  # Check if recommendations DataFrame is not empty
        return render_template('recommendations.html', recommended_people=recommendations.to_dict(orient='records'), context='Student Recommendations')
    else:
        return render_template('error.html', message="No recommendations found.")

@app.route('/get_student_student_ids', methods=['GET'])
def get_student_student_ids():
    student_id = request.args.get('student_id')
    recommendations = recommender.recommend_students_for_student(student_id, top_n=3)
    if isinstance(recommendations, str):
        return render_template('error.html', message=recommendations)
    elif not recommendations.empty:  # Check if recommendations DataFrame is not empty
        return render_template('recommendations.html', recommended_people=recommendations.to_dict(orient='records'), context='Student-to-Student Recommendations')
    else:
        return render_template('error.html', message="No recommendations found.")

@app.route('/get_professor_professor_ids', methods=['GET'])
def get_professor_professor_ids():
    professor_id = request.args.get('professor_id')
    recommendations = recommender.recommend_professors_for_professor(professor_id, top_n=3)
    if isinstance(recommendations, str):
        return render_template('error.html', message=recommendations)
    elif not recommendations.empty:  # Check if recommendations DataFrame is not empty
        return render_template('recommendations.html', recommended_people=recommendations.to_dict(orient='records'), context='Professor-to-Professor Recommendations')
    else:
        return render_template('error.html', message="No recommendations found.")


if __name__ == '__main__':
    app.run(debug=True)
