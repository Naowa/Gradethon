from appJar import gui
from course import Student, Section, Assignment, Professor, grade_students, save, load
import pickle

def press(name):
    print("press")
    print(win.getCheckBox(name))


def back_press(prev_frame, args):
    if prev_frame is prof_frame: prev_frame()
    else: prev_frame(*args, prof_frame, None)

def add_student_press(name, course_name, section_number):

    def enter_student_press(name):
        if name == "Enter":
            prof.get_course(course_name, section_number).add_student(win.getEntry("Student Name: "), win.getEntry("Student ID: "))
            win.destroySubWindow("add_student_win")
            course_frame(course_name, section_number, prof_frame, [None])
        if name == "Close":
            win.destroySubWindow("add_student_win")

    win.startSubWindow("add_student_win", title="Add Student", modal=True, transient=True, blocking=False)
    win.setSubWindowLocation("add_student_win", 500, 350)
    win.hideTitleBar()
    win.setPadding(2, 4)
    win.addGrip(row=0, column=1)
    win.addLabelEntry("Student Name: ", row=0, column=0)
    win.addLabelEntry("Student ID: ")
    win.addLabelEntry("Address: ")
    win.addLabelEntry("Email: ")
    win.addLabelEntry("Gender: ")
    win.addButtons(["Enter", "Close"], enter_student_press)
    win.stopSubWindow()
    win.showSubWindow("add_student_win")


def assignment_details(ass_name, hw, student, course_name, section_number, stud_id):

    def close_window(name):
        win.destroySubWindow("assignment_details_win")

    grades_dict = prof.get_course(course_name, section_number).get_student(stud_id).grades_dict()
    win.startSubWindow("assignment_details_win", title=ass_name, modal=True, transient=True, blocking=False)
    win.setSubWindowLocation("assignment_details_win", 500, 350)
    win.hideTitleBar()
    win.addGrip(row=0, column=1)

    try: win.addMessage("output_score", 'Correct Output: ' + str(grades_dict[hw.get_title()]["output"]) + ' / ' + str(hw.conditions().output), row=0, column=0)
    except: win.addMessage("output_score", "Correct Output: 0 / " + str(hw.conditions().output), row=0, column=0)

    try: win.addMessage("inline_score", 'Inline Comments: ' + str(grades_dict()[hw.get_title()]["inline_comments"]) + ' / ' + str(hw.conditions().inline_comments[1]))
    except: win.addMessage("inline_score", "Inline Comments: 0 / " + str(hw.conditions().inline_comments[1]))

    try:win.addMessage('function_score', 'Functions: ' + str(grades_dict[hw.get_title()]['functions']) + ' / ' + str(hw.conditions().functions[1]))
    except: win.addMessage("function_score", "Functions: 0 / " + str(hw.conditions().functions[1]))

    try:win.addMessage('function_doc_score', 'Function Docstring: ' + str(grades_dict()[hw.get_title()]['function_docstring']) + ' / ' + str(hw.conditions().function_docstring))
    except: win.addMessage('function_doc_score', "Function Docstring: 0 / " + str(hw.conditions().function_docstring))

    try:win.addMessage('classes_score', 'Classes: ' + str(grades_dict[hw.get_title()]['classes']) + ' / ' + str(hw.conditions().classes[1]))
    except: win.addMessage('classes_score', "Classes: 0 / " + str(hw.conditions().classes[1]))

    try:win.addMessage('classes_doc_score', 'Class Docstring: ' + str(grades_dict[hw.get_title()]['class_docstring']) + ' / ' + str(hw.conditions().class_docstring))
    except: win.addMessage('classes_doc_score', "Class Docstring: 0 / " + str(hw.conditions().class_docstring))

    try:win.addMessage('module_doc_score', 'Module Docstring: ' + str(grades_dict[hw.get_title()]['module_docstring']) + ' / ' + str(hw.conditions().module_dcostring))
    except: win.addMessage('module_doc_score', "Module Docstring: 0 / " + str(hw.conditions().module_docstring))

    try:win.addMessage('spec_function_score', 'Specific Functions: ' + str(grades_dict[hw.get_title()]['function_set']) + ' / ' + str(hw.conditions().function_set[1]))
    except: win.addMessage('spec_function_score', "Specific Functions: 0 / " + str(hw.conditions().function_set[1]))

    try:win.addMessage('spec_class_score', 'Specific Classes: ' + str(grades_dict[hw.get_title()]['class_set']) + ' / ' + str(hw.conditions().class_set[1]))
    except: win.addMessage('spec_class_score', "Specific Classes: 0 / " + str(hw.conditions().class_set[1]))

    win.addButton("Close", close_window)
    win.stopSubWindow()
    win.showSubWindow("assignment_details_win")

def student_frame(stud_id, stud_name, course_name, section_number, student, stud_grade, prev_frame, prev_args):

    win.removeAllWidgets()

    win.addLabel("page title", stud_name.upper())
    win.setLabelFg("page title", "white")

    win.setPadding(2, 4)
    for hw in prof.get_course(course_name, section_number).assignments():
        win.addNamedButton(hw.get_title(), hw.get_title(), lambda name: assignment_details(name, hw, student, course_name, section_number, stud_id))
        win.setButtonRelief(hw.get_title(), "solid")
        win.setButtonBg(hw.get_title(), "white")

    win.addButton("<", lambda name: back_press(prev_frame, prev_args))
    win.setButtonBg("<", "white")
    win.setButtonRelief("<", "solid")
    win.setButtonWidth("<", 5)
    win.setButtonSticky("<", "ws")

def add_course_press(name):


    def enter_course_press(name):
        if name == "Enter":
            prof.add_course(win.getEntry("Course Name: "), win.getEntry("Course Topic: "),
                            win.getEntry("Course Acronym: "), win.getEntry("Course Number: "),
                            win.getEntry("Section Number: "))
            win.destroySubWindow("add_course_win")
            prof_frame()
        if name == "Close":
            win.destroySubWindow("add_course_win")

    win.startSubWindow("add_course_win", title="Add Course", modal=True, transient=True, blocking=False)
    win.setSubWindowLocation("add_course_win", 500, 350)
    win.hideTitleBar()
    win.setPadding(2, 4)
    win.addGrip(row=0, column=1)
    win.addLabelEntry("Course Name: ", row=0, column=0)
    win.addLabelEntry("Course Topic: ")
    win.addLabelEntry("Course Acronym: ")
    win.addLabelEntry("Course Number: ")
    win.addLabelEntry("Section Number: ")
    win.addButtons(["Enter", "Close"], enter_course_press)
    win.stopSubWindow()
    win.showSubWindow("add_course_win")

def add_assignment_press(name, course_name, section_number):
    def enter_assignment_press(name):
        if name == "Enter":
            global in_file, out_file
            if in_file and out_file:
                section = prof.get_course(course_name, section_number)
                section.add_assignment(win.getEntry("Assignment Name: "), win.getTextArea("description_text"))
                hw = section.get_assignment(win.getEntry("Assignment Name: "))
                hw.add_input_file(in_file)
                hw.add_output_file(out_file)
                win.removeTextArea("description_text")
                win.destroySubWindow("add_assignment_win")
                course_frame(course_name, section_number, prof_frame, [None])
            else:
                win.errorBox("missing_files", "You must upload an input file as well as either upload an output file or"
                                              "generate one.")
        if name == "Close":
            win.removeTextArea("description_text")
            win.destroySubWindow("add_assignment_win")

    def upload_input(name):
        try:
            global in_file
            in_file = win.openBox(title="Upload Input File", dirName=None, fileTypes=[('input files', '*.in')], asFile=False)
        except: pass

    def upload_output(name):
        try:
            global out_file
            out_file = win.openBox(title="Upload Output File", dirName=None, fileTypes=[('output files', '*.out')], asFile=False)
        except: pass

    in_file = ""
    out_file = ""
    win.startSubWindow("add_assignment_win", title="Add Assignment", modal=True, transient=True, blocking=False)
    win.hideTitleBar()
    win.setPadding(2, 4)
    win.addGrip(row=0, column=1)
    win.addLabelEntry("Assignment Name: ", row=0, column=0)
    win.addLabel("description_label", "Description: ", row=1)
    win.addTextArea("description_text", row=2)
    win.addButton("Upload Input", upload_input, row=3)
    win.addButton("Upload Output", upload_output, row=4, column=0)
    win.addButtons(["Enter", "Close"], enter_assignment_press)
    win.stopSubWindow()
    win.showSubWindow("add_assignment_win")

def prof_frame():
    win.removeAllWidgets()
    win.addLabel("page title", "COURSES")
    win.setLabelFg("page title", "white")

    win.startFrame("prof_frame")
    for prof_course in prof.courses():
        win.addNamedButton(prof_course.get_title(), prof_course.get_title(),
                           lambda name: course_frame(name,
                                                  prof_course.get_section_number(), prof_frame, [None]))
        win.setButtonRelief(prof_course.get_title(), "solid")
        win.setButtonBg(prof_course.get_title(), "white")
    win.addNamedButton("+", "plus_but", add_course_press)
    win.setButtonRelief("plus_but", "solid")
    win.setButtonBg("plus_but", "white")
    win.stopFrame()

def course_frame(course_name, section_number, prev_frame, prev_args):

    win.removeAllWidgets()

    win.addLabel("page title", course_name.upper())
    win.setLabelFg("page title", "white")

    win.startToggleFrame("ASSIGNMENTS")
    win.setToggleFrameBg("ASSIGNMENTS", "white")
    win.setToggleFrameRelief("ASSIGNMENTS", "solid")
    win.setPadding(2,4)
    for hw in prof.get_course(course_name, section_number).assignments():
        win.addNamedButton(hw.get_title(), hw.get_title(), lambda name: assignment_frame(name, course_name, section_number, course_frame, [course_name, section_number]))
        win.setButtonRelief(hw.get_title(), "solid")
        win.setButtonBg(hw.get_title(), "white")
    win.setInPadding(54, 2)
    win.addNamedButton("+", "ass_plus_but", lambda name: add_assignment_press(name, course_name, section_number))
    win.setButtonRelief("ass_plus_but", "solid")
    win.setButtonBg("ass_plus_but", "white")
    win.stopToggleFrame()

    win.setPadding(20, 20)
    win.startToggleFrame("STUDENTS")
    win.setToggleFrameBg("STUDENTS", "white")
    win.setToggleFrameRelief("STUDENTS", "solid")
    win.setPadding(2, 4)
    for stud in prof.get_course(course_name, section_number).students():
        win.addNamedButton(stud.get_name(), stud.get_id(), lambda stud_id: student_frame(stud_id, stud.get_name(), course_name, section_number, stud, stud.grades_dict(), prev_frame, prev_args))
        win.setButtonRelief(stud.get_id(), "solid")
        win.setButtonBg(stud.get_id(), "white")
    win.setInPadding(54, 2)
    win.addNamedButton("+", "stud_plus_but", lambda name: add_student_press(name, course_name, section_number))
    win.setButtonRelief("stud_plus_but", "solid")
    win.setButtonBg("stud_plus_but", "white")
    win.stopToggleFrame()

    options_pane(prof.get_course(course_name, section_number))

    win.addButton("<", lambda name: back_press(prev_frame, prev_args))
    win.setButtonBg("<", "white")
    win.setButtonRelief("<", "solid")
    win.setButtonWidth("<", 5)
    win.setButtonSticky("<", "ws")



def assignment_frame(ass_name, course_name, section_number, prev_frame, prev_args):

    def upload_press(but_name, ass_name):
        stud = prof.get_course(course_name, section_number).get_student(but_name[3:])
        try:
            stud.upload(win.openBox(title="Upload Files", dirName=None, fileTypes=[('python files', '*.py')], asFile=False),
                        ass_name)
            win.setCheckBox(stud.get_name() + "_" + stud.get_id(), True)
        except:
            pass


    def grade_press(ass_name):
        students = []
        for stud in prof.get_course(course_name, section_number).students():
            if win.getCheckBox(stud.get_name() + "_" + stud.get_id()): students.append(stud.get_id())
        grade_students(prof.get_course(course_name, section_number),
                       prof.get_course(course_name, section_number).get_assignment(ass_name),
                       students)

    win.removeAllWidgets()
    win.addLabel("page title", ass_name.upper())
    win.setLabelFg("page title", "white")

    win.addMessage(str(ass_name) + "_desc",
                   prof.get_course(course_name, section_number).get_assignment(ass_name).get_description())
    win.setMessageRelief(str(ass_name) + "_desc", "solid")
    win.setMessageBg(str(ass_name) + "_desc", "white")
    win.setMessageWidth(str(ass_name) + "_desc", 200)

    win.startFrame("stud_prop_frame")

    but_count = 0
    for stud in prof.get_course(course_name, section_number).students():
        win.setPadding(2, 2)
        win.addCheckBox(stud.get_name() + "_" + stud.get_id(), row=but_count, column=0)
        win.setCheckBoxBg(stud.get_name() + "_" + stud.get_id(), "white")
        win.setCheckBoxRelief(stud.get_name() + "_" + stud.get_id(), "solid")
        win.disableCheckBox(stud.get_name() + "_" + stud.get_id())

        win.setButtonFont(8)
        win.addNamedButton("UPLOAD", "up_" + stud.get_id(), lambda but_name: upload_press(but_name, ass_name),
                           row=but_count, column=1)
        win.setButtonBg("up_" + stud.get_id(), "white")
        win.setButtonRelief("up_" + stud.get_id(), "solid")
        but_count += 1

    win.stopFrame()

    course_obj = prof.get_course(course_name, section_number)
    options_pane(course_obj, specific=True, ass_obj = course_obj.get_assignment(ass_name))

    win.setButtonFont(12)
    win.addButton("GRADE", lambda name: grade_press(ass_name))
    win.setButtonBg("GRADE", "white")
    win.setButtonRelief("GRADE", "solid")

    win.addButton("<", lambda name: back_press(prev_frame, prev_args))
    win.setButtonBg("<", "white")
    win.setButtonRelief("<", "solid")
    win.setButtonWidth("<", 5)
    win.setButtonSticky("<", "ws")


def options_pane(course_obj, specific = False, ass_obj = None):


    def update(cb_name):
        try:
            if cb_name == "Inline Comments: ":
                if not win.getCheckBox("Inline Comments: "):
                    win.disableEntry("inline_comment_number")
                    win.disableEntry("inline_points")
                else:
                    win.enableEntry("inline_comment_number")
                    win.enableEntry("inline_points")

            elif cb_name == "Functions: ":
                if not win.getCheckBox("Functions: "):
                    win.disableEntry("function_number")
                    win.disableCheckBox("Function Docstring")
                    win.disableEntry("function_points")
                    if specific: win.disableTextArea("Specific Functions: ")
                else:
                    win.enableEntry("function_number")
                    win.enableCheckBox("Function Docstring")
                    win.enableEntry("function_points")
                    if specific: win.enableTextArea("Specific Functions: ")

            elif cb_name == "Function Docstring":
                if not win.getCheckBox("Function Docstring"):
                    win.disableEntry("function_docstring_points")
                else:
                    win.enableEntry("function_docstring_points")

            elif cb_name == "Classes: ":
                if not win.getCheckBox("Classes: "):
                    win.disableEntry("class_number")
                    win.disableCheckBox("Class Docstring")
                    win.disableEntry("class_points")
                    if specific: win.disableTextArea("Specific Classes: ")
                else:
                    win.enableEntry("class_number")
                    win.enableCheckBox("Class Docstring")
                    win.enableEntry("class_points")
                    if specific: win.enableTextArea("Specific Classes: ")

            elif cb_name == "Class Docstring":
                if not win.getCheckBox("Class Docstring"):
                    win.disableEntry("class_docstring_points")
                else:
                    win.enableEntry("class_docstring_points")

            elif cb_name == "Module Docstring":
                if not win.getCheckBox("Module Docstring"):
                    win.disableEntry("module_docstring_points")
                else:
                    win.enableEntry("module_docstring_points")
        except:
            pass

    def apply_press(name):
        if not specific:
            if win.getCheckBox("Inline Comments: "):
                course_obj.set_condition_inline_comments((win.getEntry("inline_comment_number"), win.getEntry("inline_points")))
            if win.getCheckBox("Functions: "):
                course_obj.set_condition_functions((win.getEntry("function_number"), win.getEntry("function_points")))
            if win.getCheckBox("Function Docstring"):
                course_obj.set_condition_function_docstring(win.getEntry("function_docstring_points"))
            if win.getCheckBox("Classes: "):
                course_obj.set_condition_classes((win.getEntry("class_number"), win.getEntry("class_comment_points")))
            if win.getCheckBox("Class Docstring"):
                course_obj.set_condition_class_docstring(win.getEntry("class_docstring_points"))
            if win.getCheckBox("Module Docstring"):
                course_obj.set_condition_module_docstring(win.getEntry("module_docstring_points"))
            course_obj.set_condition_output(win.getEntry("Correct Output points: "))

        else:
            if win.getCheckBox("Inline Comments: "):
                ass_obj.set_condition_inline_comments((win.getEntry("inline_comment_number"), win.getEntry("inline_points")))
            if win.getCheckBox("Functions: "):
                ass_obj.set_condition_functions((win.getEntry("function_number"), win.getEntry("function_points")))
            if win.getCheckBox("Function Docstring"):
                ass_obj.set_condition_function_docstring(win.getEntry("function_docstring_points"))
            if win.getCheckBox("Classes: "):
                ass_obj.set_condition_classes((win.getEntry("class_number"), win.getEntry("class_points")))
            if win.getCheckBox("Class Docstring"):
                ass_obj.set_condition_class_docstring(win.getEntry("class_docstring_points"))
            if win.getCheckBox("Module Docstring"):
                ass_obj.set_condition_module_docstring(win.getEntry("module_docstring_points"))
            for func in win.getEntry("Specific Functions: ").split():
                ass_obj.add_condition_function(func, win.getEntry("spec_func_points"))
            for classname in win.getEntry("Specific Classes: ").split():
                ass_obj.add_condition_class(classname, win.getEntry("spec_class_points"))
            ass_obj.set_condition_output(win.getEntry("Correct Output points: "))

    win.setPadding(20, 20)
    win.startToggleFrame("OPTIONS")
    win.setToggleFrameBg("OPTIONS", "white")
    win.setToggleFrameRelief("OPTIONS", "solid")
    win.setPadding(20, 20)

    win.addCheckBox("Inline Comments: ", row=1, column=0)
    win.addEntry("inline_comment_number", row=1, column=1)
    win.setEntry("inline_comment_number", course_obj.conditions().inline_comments[0])
    win.registerEvent(lambda: update("Inline Comments: "))

    win.setPadding(20, 2)
    win.addCheckBox("Functions: ", row=2, column=0)
    win.addEntry("function_number", row=2, column=1)
    win.registerEvent(lambda: update("Functions: "))
    win.setEntry("function_number", course_obj.conditions().functions[0])
    win.addCheckBox("Function Docstring", row=3)
    win.registerEvent(lambda: update("Function Docstring"))

    win.addCheckBox("Classes: ", row=4, column=0)
    win.addEntry("class_number", row=4, column=1)
    win.registerEvent(lambda: update("Classes: "))
    win.setEntry("class_number", course_obj.conditions().classes[0])
    win.addCheckBox("Class Docstring", row=5)
    win.registerEvent(lambda: update("Class Docstring"))

    win.addCheckBox("Module Docstring", row=6, column=0)
    win.registerEvent(lambda: update("Module Docstring"))

    win.addVerticalSeparator(row=0, column=3, colspan=0, rowspan=7, colour=None)

    win.addLabel("points", "Points", row=0, column=4)
    win.addEntry("inline_points", row=1, column=4)
    win.setEntry("inline_points", course_obj.conditions().inline_comments[1])
    win.addEntry("function_points", row=2, column=4)
    win.setEntry("function_points", course_obj.conditions().functions[1])
    win.addEntry("function_docstring_points", row=3, column=4)
    win.setEntry("function_docstring_points", course_obj.conditions().function_docstring)
    win.addEntry("class_points", row=4, column=4)
    win.setEntry("class_points", course_obj.conditions().classes[1])
    win.addEntry("class_docstring_points", row=5, column=4)
    win.setEntry("class_docstring_points", course_obj.conditions().class_docstring)
    win.addEntry("module_docstring_points", row=6, column=4)
    win.setEntry("module_docstring_points", course_obj.conditions().module_docstring)

    if specific:
        win.addLabelEntry("Specific Functions: ", row=7, column=0)
        win.setEntry("Specific Functions: ", list(ass_obj.conditions().function_set[0]))
        win.addEntry("spec_func_points", row=7, column=4)
        win.setEntry("spec_func_points", ass_obj.conditions().function_set[1])
        win.addLabelEntry("Specific Classes: ", row=8, column=0)
        win.setEntry("Specific Classes: ", list(ass_obj.conditions().class_set[0]))
        win.addEntry("spec_class_points", row=8, column=4)
        win.setEntry("spec_class_points", ass_obj.conditions().class_set[1])

    win.addLabelEntry("Correct Output points: ")
    win.setEntry("Correct Output points: ", course_obj.conditions().output)
    win.addButton("APPLY", apply_press)
    win.setButtonBg("APPLY", "white")
    win.setButtonRelief("APPLY", "solid")
    win.stopToggleFrame()

def on_start():
    try:
        global prof
        #load(prof)
        pickle_in = open("savedata.pickle", "rb")
        prof = pickle.load(pickle_in)
    except: print('No file to load from.')

def on_close():
    global prof
    #save(prof)
    pickle_out = open("savedata.pickle", "wb")
    pickle.dump(prof, pickle_out)
    pickle_out.close()
    return True

prof = Professor("user")
# prof.add_course("Fundamentals of CSII - Python", "Python", "CS", "3C", "1")
# prof.add_course("Python Programming", "Python", "SCI", "1", "1")
# prof.get_course("Fundamentals of CSII - Python", "1").add_assignment(description="test desc line line")
# prof.get_course("Fundamentals of CSII - Python", "1").add_student("steve", "1234")
# prof.get_course("Fundamentals of CSII - Python", "1").add_student("jeff", "3542")
on_start()
win = gui("Gradethon")

win.setFont(12)
#win.setIcon("pyIcon.png")
win.setSticky("")
win.setStretch("column")
#win.addLabel("page title", "COURSES")
#win.setLabelFg("page title", "white")
#win.setPadding(4, 20)

#win.setGeometry(600,600)
win.setBg("#1EB277")
#win.setBgImage("pink-brown-blue-polka-dot-pattern.gif")
#win.setResizable(canResize=False)
#win.startScrollPane("body")
#----
""""
win.setStretch("both")
win.setSticky("nesw")
win.setPadding(20, 40)
win.setGeometry(400, 400)
win.addListBox("list")
win.setListBoxCursor("list", "hand1")
win.setListBoxActiveBg("list", "#FF8972")
#win.setListBoxBg("list", "#1EB277")
for prof_course in prof.courses():
    win.addListItem("list", prof_course.get_title())
    win.setListItemBg("list", prof_course.get_title(), "#1EB277")
    win.setListItemFg("list", prof_course.get_title(), "white")
"""
#----
#win.stopScrollPane()
win.setStopFunction(on_close)
prof_frame()

win.go()