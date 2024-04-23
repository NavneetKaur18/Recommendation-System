import pandas as pd
from Constants.constants import Constant

class DAO:
    def __init__(self) -> None:
        self.constants = Constant()
        self.df_prof = None
        self.df_student = None
        self._connect_to_student_database()
        self._connect_to_professor_database()

    def _connect_to_student_database(self):
        try:
            self.df_student = pd.read_excel(self.constants.STUDENT_PATH)
        except Exception as e:
            print(e)
            print("ERROR READING STUDENT DATABASE")

    def _connect_to_professor_database(self):
        try:
            self.df_prof = pd.read_excel(self.constants.PROFESSOR_PATH)
        except Exception as e:
            print(e)
            print("ERROR READING PROFESSOR DATABASE")

    def get_student_database_instance(self):
        return self.df_student

    def get_prof_database_instance(self):
        return self.df_prof
