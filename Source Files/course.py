import collections
import shutil
import os
import subprocess
import pickle
import threading

Options = collections.namedtuple('Options', ['output', 'inline_comments', 'functions', 'function_docstring',
                                             'classes', 'class_docstring', 'module_docstring',
                                             'function_set', 'class_set'])

class GradeThread(threading.Thread):
    def __init__(self, course_obj, assignment_obj, stud_obj):
        threading.Thread.__init__(self)
        self._course_obj = course_obj
        self._assignment_obj = assignment_obj
        self._stud_obj = stud_obj
        self._threadLock = threading.Lock()

    def run(self):
            #stud_obj = self._course_obj.get_student(stud)
            self._threadLock.acquire()
            grade = self._assignment_obj.grade(self._stud_obj)
            self._threadLock.release()

            if grade != False:
                self._stud_obj.add_grade(self._assignment_obj.get_title(), grade)
            else:
                print('Error grading for ' + self._stud_obj.get_name() + " " + self._stud_obj.get_id() + ' on ' + \
                      self._assignment_obj.get_title() + ' in ' + self._course_obj.get_title())



def grade_students(section_obj, assignment_obj, student_id_list):
    for stud in student_id_list:
        stud_obj = section_obj.get_student(stud)
        GradeThread(section_obj, assignment_obj, stud_obj).start()

def save(obj):
    pickle_out = open("savedata.pickle", "wb")
    pickle.dump(obj, pickle_out)
    pickle_out.close()

def load(obj):
    try:
        pickle_in = open("savedata.pickle", "rb")
        obj = pickle.load(pickle_in)
    except: pass

class Section(object):
    """Represents a single course run by a professor"""

    def __init__(self, title, topic, course_acronym, course_number, section_number, language="Python"): #UPDATE
        """
        Constructor: Initializes self with non-optional arguments
        :param title:
        :param language:
        :param course_number:
        :param section_number:
        """
        self._title = title
        self._topic = topic
        self._language = language
        self._course_acronym = course_acronym
        self._course_number = course_number
        self._section_number = section_number

        self._conditions = Options(
            output = 1, #Amount of points output is worth
            inline_comments = (0, 0), #(amount to check for, points each quantity is weighted)
            functions = (0, 0),
            function_docstring = 0, #number of points, amount to check is based on functions
            classes = (0, 0),
            class_docstring = 0, #see function_docstring
            module_docstring = 0,
            function_set = (set(),0), # (names of functions, points for each)
            class_set = (set(),0) #(names of classes, points for each)
        )

        self._assignments = []
        self._students = []

    def __repr__(self):
        """Returns Formal representation of object"""
        return ""

    def __str__(self):
        """Returns informal representation of object"""
        return ""

    def update_title(self, title):
        """Updates current attribute to argument"""
        self._title = title

    def update_topic(self, topic):
        """Updates current attribute to argument"""
        self._topic = topic

    def update_language(self, language):
        """Updates current attribute to argument"""
        self._language = language

    def update_course_acronym(self, course_acronym): #NEW
        """Updates current attribute to argument"""
        self._course_acronym = course_acronym

    def update_course_number(self, course_number):
        """Updates current attribute to argument"""
        self._course_number = course_number

    def update_section_number(self, section_number):
        """Updates current attribute to argument"""
        self._section_number = section_number

    def get_title(self):
        """Returns member variable"""
        return self._title

    def get_topic(self):
        """Returns member variable"""
        return self._topic

    def get_language(self):
        """Returns member variable"""
        return self._language

    def get_course_acronym(self): #NEW
        """Returns member variable"""
        return self._course_acronym

    def get_course_number(self):
        """Returns member variable"""
        return self._course_number

    def get_section_number(self):
        """Returns member variable"""
        return self._section_number

    def get_assignment(self, assignment_title):
        for hw in self._assignments:
            if hw.get_title() == assignment_title:
                return hw

    def get_student(self, student_id):
        for stud in self._students:
            if stud.get_id() == student_id:
                return stud

    def students(self):
        """Returns list of students"""
        return self._students

    def assignments(self):
        """Returns list of assignments"""
        return self._assignments

    def add_student(self, name, id): #UPDATED -- took out directory
        """Adds student to list"""
        for student in self._students:
            if student.get_id() == id:
                pass
        self._students.append(Student(name, id, (self._title, self._section_number)))

    def remove_student(self, name, id):
        """Removes student from list"""
        for student in self._students:
            if student.get_id() == id and student.get_name() == name:
                self._students.remove(student)

    def add_assignment(self, title="Assignment Title", description="Assignment Description"): #UPDATE - got rid of assignment parameter
        """Adds assignment to list"""
        hw = Assignment(self._conditions, title, description)
        self._assignments.append(hw)

    def remove_assignment(self, assignment):
        """Removes assignment from list"""
        for assignment in self._assignments:
            if assignment.get_title() == assignment.title:
                self._assignments.remove(assignment)

    def conditions(self):
        """Returns access to course's default grading criteria"""
        return self._conditions

    def grade(self, assignment_index, student_set):
        """Calls appropriate grade function with the appropriate assignment for
        point distribution"""

    def set_condition_output(self, points):
        self._conditions = self._conditions._replace(output=points)

    def set_condition_inline_comments(self, new_tuple):
        self._conditions = self._conditions._replace(inline_comments=new_tuple)

    def set_condition_functions(self, new_tuple):
        self._conditions = self._conditions._replace(functions=new_tuple)

    def set_condition_function_docstring(self, points):
        self._conditions = self._conditions._replace(function_docstring=points)

    def set_condition_classes(self, new_tuple):
        self._conditions = self._conditions._replace(classes=new_tuple)

    def set_condition_class_docstring(self, points):
        self._conditions = self._conditions._replace(class_docstring=points)

    def set_condition_module_docstring(self, new_tuple):
        self._conditions = self._conditions._replace(module_docstring=new_tuple)

class Assignment(object):
    """Represents a single assignment per course"""

    def __init__(
            self,
            default_options,
            title="Assignment Title",
            description="Assignment Description",
            filetype=".py",
    ):
        """
        Constructor: Initializes attributes
        :param default_options:
        :param title:
        :param description:
        :param filetype:
        """
        #include school, hours
        self._input_file = ""
        self._output_file = ""

        self._input_str = ""
        self._output_str = ""

        self._title = title
        self._description = description
        self._filetype = filetype

        self._conditions = default_options

        self._max_points = self._calc_max_points()

    def grade(self, stud_obj):
        """Runs and assigns points to program"""
        pass # Returns dictionary of points
        score_dict = {'output':0, 'inline_comments':0, 'functions':0, 'function_docstring':0,
                      'classes':0, 'class_docstring':0, 'module_docstring':0,
                      'function_set':0, 'class_set':0}
        for file in os.listdir(stud_obj.get_directory() + "\\" + self._title):
            if file == "main.py":
                #stud_obj = subprocess.Popen(,stdout=PIPE, stdin=PIPE, stderr=PIPE)
                main_file = stud_obj.get_directory() + "\\" + self._title.replace(' ','_') + "\\" + file
                try: stud_output = subprocess.run('python ' + main_file, universal_newlines=True, stdout=subprocess.PIPE, input=self._input_str).stdout
                except: stud_output = "EXECUTION_FAILED"
                if stud_output == self._output_str:
                    score_dict['output'] = self._conditions.output

                line_count = 1
                func_flag = False
                class_flag = False

                for line in open(main_file.replace('\\', r'\\'), 'r').readlines():

                    if '"""' in line and line_count == 1:
                        score_dict['module_docstring'] += int(self._conditions.module_docstring)

                    if '"""' in line and func_flag:
                        func_flag = False
                        if score_dict['function_docstring'] < int(self._conditions.functions[0]) * \
                                int(self._conditions.function_docstring):
                            score_dict['function_docstring'] += int(self._conditions.function_docstring)

                    if '"""' in line and class_flag:
                        class_flag = False
                        if score_dict['class_docstring'] < int(self._conditions.classes[0]) * \
                                int(self._conditions.class_docstring):
                            score_dict['class_docstring'] += int(self._conditions.class_docstring)

                    if '# ' in line:
                        if score_dict['inline_comments'] < int(self._conditions.inline_comments[0]) * \
                                int(self._conditions.inline_comments[1]):
                            score_dict['inline_comments'] += int(self._conditions.inline_comments[1])

                    if 'def ' in line:
                        if score_dict['functions'] < int(self._conditions.functions[0]) * \
                                int(self._conditions.functions[1]):
                            score_dict['functions'] += int(self._conditions.functions[1])
                            func_flag = True
                        for funcname in self._conditions.function_set[0]:
                            if funcname in line and score_dict['function_set'] < \
                                            int(self._conditions.function_set[1]) * int(self._conditions.functions[1]):
                                score_dict['function_set'] += int(self._conditions.function_set[1])

                    if 'class ' in line:
                        if score_dict['classes'] < int(self._conditions.classes[0]) * \
                                int(self._conditions.classes[1]):
                            score_dict['classes'] += int(self._conditions.classes[1])
                            class_flag = True
                        for classname in self._conditions.class_set[0]:
                            if classname in line and score_dict['class_set'] < \
                                            int(self._conditions.class_set[1]) * int(self._conditions.classes[1]):
                                score_dict['class_set'] += self._conditions.class_set[1]

                    line_count += 1
                return score_dict

        return False

    def add_input_file(self, filename):
        """Add file to input file list"""
        self._input_file = filename
        self._input_str = open(self._input_file, 'r').read()

    def add_output_file(self, filename):
        """Add file to output file list"""
        self._output_file = filename
        self._output_str = open(self._output_file, 'r').read()

    def set_title(self, title):
        """Assign parameters to member variable"""
        self._title = title

    def set_description(self, description):
        """Assign parameters to member variable"""
        self._description = description

    def set_filetype(self, filetype=".py"):
        """Assign parameters to member variable"""
        self._filetype = filetype

    def conditions(self):
        """Returns options object"""
        return self._conditions

    def get_input_files(self):
        """Returns member variables"""
        return self._input_file

    def get_output_files(self):
        """Returns member variables"""
        return self._output_file

    def get_title(self):
        """Returns member variables"""
        return self._title

    def get_description(self):
        """Returns member variables"""
        return self._description

    def get_filetype(self):
        """Returns member variables"""
        return self._filetype

    def _calc_max_points(self):
        """Nonpublic method - Calculates number of possible points to sore"""
        total_score = 0
        for condition in self._conditions:
            try: total_score += int(condition[1])
            except: total_score += int(condition)

    def set_condition_output(self, points):
        self._conditions = self._conditions._replace(output=points)

    def set_condition_inline_comments(self, new_tuple):
        self._conditions = self._conditions._replace(inline_comments=new_tuple)

    def set_condition_functions(self, new_tuple):
        self._conditions = self._conditions._replace(functions=new_tuple)

    def set_condition_function_docstring(self, points):
        self._conditions = self._conditions._replace(function_docstring=points)

    def set_condition_classes(self, new_tuple):
        self._conditions = self._conditions._replace(classes=new_tuple)

    def set_condition_class_docstring(self, points):
        self._conditions = self._conditions._replace(class_docstring=points)

    def set_condition_module_docstring(self, new_tuple):
        self._conditions = self._conditions._replace(module_docstring=new_tuple)

    def add_condition_function(self, new_function, points):
        temp_set = self._conditions.function_set[0]
        temp_set.add(new_function)
        self._conditions = self._conditions._replace(function_set=(temp_set, points))

    def add_condition_class(self, new_class, points):
        temp_set = self._conditions.class_set[0]
        temp_set.add(new_class)
        self._conditions = self._conditions._replace(class_set=(temp_set, points))

class Person(object):
    """Represents an abstract person class created for inheritance"""
    def __init__(self, name, address=None, gender=None, email=None, birthday=None):
        """
        Constructor: Initializes self
        :param file_directory:
        """
        #self._directory = file_directory
        self._name = name
        self._address = address
        self._gender = gender
        self._email = email
        self._birthday = birthday

    def __repr__(self):
        """Returns Formal representation of object"""
        return ""

    def __str__(self):
        """Returns informal representation of object"""
        return ""

    def set_name(self, name):
        self._name = name

    def set_address(self, address):
        self._address = address

    def set_gender(self, gender):
        self._gender = gender

    def set_email(self, email):
        self._email = email

    def set_birthday(self, birthday):
        self._birthday = birthday

    def get_name(self):
        return self._name

    def get_address(self):
        return self._address

    def get_gender(self):
        return self._gender

    def get_email(self):
        return self._email

    def get_birthday(self):
        return self._birthday


class Professor(Person):
    """Represents the user of program
    Only allowed one instance"""

    def __init__(self, name, address=None, gender=None, email=None, birthday=None):
        """
        Constructor: Initializes self using Programmer parentclass
        :param file_directory:
        """
        Person.__init__(self,  name, address, gender, email, birthday)
        self._courses = []

    def __repr__(self):
        """Returns Formal representation of object"""
        return ""

    def __str__(self):
        """Returns informal representation of object"""
        return ""

    def add_student(self, course_index, name, id):
        """Adds student to a course"""
        if not self._courses:
            pass
        self._courses[course_index].add_student(name, id)

    def remove_student(self, course_index, name, id):
        """Removes student from course"""
        if not self._courses:
            pass
        for course in self._courses:
            course.remove_student()

    def add_course(self, title, topic, course_acronym, course_number, section_number, language="Python"): #UPDATE
        """Adds course to list"""
        self._courses.append(Section(title,topic,course_acronym, course_number,section_number,language))

    def remove_course(self, course_number, section_number):
        """Removes course from list"""
        for course in self._courses:
            if course.get_course_number() == course_number and course.get_section_number() == section_number:
                self._courses.remove(course)

    def courses(self):
        """Returns list of courses"""
        return self._courses

    def get_course(self, course_name, section_number): #NEW
        """Returns the course asked for"""
        if not self._courses: return False
        for prof_course in self._courses:
            if prof_course.get_title() == course_name and prof_course.get_section_number() == section_number:
                return prof_course
        return False

class Student(Person):
    """Represents a single student to be graded and assigned points"""

    def __init__(self, name, id, course_tuple, address=None, gender=None, email=None, school=None): #UPDATED
        Person.__init__(self, name, address, gender, email, school) #take into account the none
        #Create directory
        self._course_attending = () #(course name, section number)
        self._id = id
        self._total_grade = 0
        self._grades = {} #key: assignment, value:Score obj\\dict
        self._filedirectory = os.getcwd() + "\\PythonGrader_Files\\Courses\\" + course_tuple[0].replace(' ','_') + "_" + course_tuple[1] + "\\Students\\" \
                              + self._name + "_" + self._id

        self._calc_total_grade()

    def __repr__(self):
        """Returns Formal representation of object"""
        return ""

    def __str__(self):
        """Returns informal representation of object"""
        return ""

    def set_name(self, name):
        """Sets member variables to parameter"""
        self._name = name

    def set_id(self, id):
        """Sets member variables to parameter"""
        self._id = id

    def get_name(self):
        """Returns member variable"""
        return self._name

    def get_id(self):
        """Returns member variable"""
        return self._id

    def get_directory(self):
        return self._filedirectory

    def grades_dict(self):
        """Returns grades dictionary"""
        return self._grades

    def add_grade(self, ass_name, grade):
        """Adds grade to dict"""
        self._grades[ass_name] = grade
        self._calc_total_grade()

    def _calc_total_grade(self):
        for assignment in self._grades.values():
            for score in assignment.values():
                self._total_grade += int(score)

    def save_grades(self):
        pickle_out = open(self._filedirectory + "\\grades.pickle", "wb")
        pickle.dump(self._grades, pickle_out)
        pickle_out.close()

    def load_grades(self):
        pickle_in = open(self._filedirectory + "\\grades.pickle", "rb")
        self._grades = pickle.load(pickle_in)

    def upload(self, file, ass_name):
        path = self._filedirectory +  "\\" + ass_name
        if not os.path.exists(path):
            os.makedirs(path)

        shutil.copy(file, path)

