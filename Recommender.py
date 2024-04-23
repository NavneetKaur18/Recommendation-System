import time
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from DAO.dataaccess import DAO

class ResearchInterestRecommender:
    def __init__(self):
        self.dao = DAO()
        self.df_student = self.dao.get_student_database_instance()
        self.df_prof = self.dao.get_prof_database_instance()
        self._make_combined_dataset()
        self.vectorize_data()

    def _make_combined_dataset(self):
        self.combined_df = pd.concat([self.df_student['Research Interests'], self.df_prof['Research Interests']], ignore_index=True)

    def vectorize_data(self):
        """Vectorize the research interests using TF-IDF."""
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.combined_df)
        # Compute cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix)

    def get_student_index(self, student_guid):
        """Get index from student GUID."""
        if student_guid in self.df_student['Student GUID'].values:
            return self.df_student[self.df_student['Student GUID'] == student_guid].index[0]
        else:
            return None

    def get_professor_index(self, professor_guid):
        """Get index from professor GUID."""
        if professor_guid in self.df_prof['Professor GUID'].values:
            return self.df_prof[self.df_prof['Professor GUID'] == professor_guid].index[0] + len(self.df_student)
        else:
            return None

    def recommend_professors(self, student_guid, top_n=3):
        """Recommend professors for a student based on research interests similarity."""
        student_index = self.get_student_index(student_guid)
        if student_index is not None:
            student_sim_scores = self.cosine_sim[student_index, len(self.df_student):]
            prof_indices = student_sim_scores.argsort()[-top_n:][::-1]
            return self.df_prof.iloc[prof_indices]
        else:
            print(student_guid)
            return "Student GUID not found."

    def recommend_students(self, professor_guid, top_n=3):
        """Recommend students for a professor based on research interests similarity."""
        prof_index = self.get_professor_index(professor_guid)
        if prof_index is not None:
            prof_sim_scores = self.cosine_sim[prof_index, :len(self.df_student)]
            student_indices = prof_sim_scores.argsort()[-top_n:][::-1]
            return self.df_student.iloc[student_indices]
        else:
            return "Professor GUID not found."

    def recommend_students_for_student(self, student_guid, top_n=3):
        """Recommend students for a student based on research interests similarity."""
        student_index = self.get_student_index(student_guid)
        if student_index is not None:
            student_sim_scores = self.cosine_sim[student_index, :len(self.df_student)]
            student_indices = student_sim_scores.argsort()[-top_n:][::-1]
            return self.df_student.iloc[student_indices]
        else:
            return "Student GUID not found."
    
    def recommend_professors_for_professor(self, professor_guid, top_n=3):
        """Recommend professors for a professor based on research interests similarity."""
        prof_index = self.get_professor_index(professor_guid)
        if prof_index is not None:
            prof_sim_scores = self.cosine_sim[prof_index, len(self.df_student):]
            prof_indices = prof_sim_scores.argsort()[-top_n:][::-1]
            return self.df_prof.iloc[prof_indices]
        else:
            return "Professor GUID not found."