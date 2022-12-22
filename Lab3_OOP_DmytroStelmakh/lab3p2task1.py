from abc import ABC, abstractmethod
import mysql.connector


class ICourse(ABC):
    @property
    @abstractmethod
    def title(self):
        pass

    @title.setter
    @abstractmethod
    def title(self, value):
        pass

    @property
    @abstractmethod
    def teachers(self):
        pass

    @teachers.setter
    @abstractmethod
    def teachers(self, value):
        pass

    @property
    @abstractmethod
    def program(self):
        pass

    @program.setter
    @abstractmethod
    def program(self, value):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def add_teacher(self):
        pass


class Course(ICourse):
    def init(self, title, teachers, program):
        self.title = title
        self.teachers = teachers
        self.program = program

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError('Назва курсу повинна бути текстом')
        self.__title = value

    @property
    def teachers(self):
        return self.__teachers

    @teachers.setter
    def teachers(self, value):
        if not isinstance(value, (Teacher, list)):
            raise TypeError('Уведіть викладача або список викладачів.')
        if isinstance(value, list) and not all(isinstance(teacher, Teacher) for teacher in value):
            raise ValueError('У списку не всі елементи є викладачами.')

        if isinstance(value, Teacher):
            self.__teachers = [value]  # реалізовано саме таким чином, щоб можна було додати викладача до курсу
        else:  # elif isinstance(value, list):
            self.__teachers = value

    @property
    def program(self):
        return self.__program

    @program.setter
    def program(self, value):
        if not isinstance(value, (str, list)):
            raise TypeError('Уведіть тему або список тем.')
        if isinstance(value, list) and not all(isinstance(topic, str) for topic in value):
            raise ValueError('У списку не всі елементи є текстовими стрічками.')

        if isinstance(value, str):
            self.__program = [value]  # ідентично як із сетером викладача
        else:  # elif isinstance(value, list):
            self.__program = value

    """ НАПИСАТИ ЩЕ ФУНКЦІЇ add() І add_teacher() !!! """


class ILocalCourse(ABC):
    @property
    @abstractmethod
    def room(self):
        pass

    @room.setter
    @abstractmethod
    def room(self, value):
        pass


class LocalCourse(Course, ILocalCourse):
    def __init__(self, title, teachers, program, room):
        super().init(title, teachers, program)
        self.room = room

    @property
    def room(self):
        return self.__room

    @room.setter
    def room(self, value):
        if not isinstance(value, (str, int)):
            raise TypeError('Номер аудиторії повинен бути текстовою стрічкою або числом.')

        if isinstance(value, int):
            self.__room = str(value)
        else:
            self.__room = value


class IOffsiteCourse(ABC):
    @property
    @abstractmethod
    def place(self):
        pass

    @place.setter
    @abstractmethod
    def place(self, value):
        pass


class OffsiteCourse(Course, IOffsiteCourse):
    def __init__(self, title, teachers, program, place):
        super().init(title, teachers, program)
        self.place = place

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if not isinstance(value, str):
            raise TypeError('Місце проведення занять повинне бути текстовою стрічкою.')
        self.__place = value


class ITeacher(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, val):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def get_courses(self):
        pass


class Teacher(ITeacher):
    def __init__(self, name):
        self.name = name

    def add(self):
        database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )
        cursor = database.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS db;
                          CREATE TABLE IF NOT EXISTS db.teachers (
                          id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          name VARCHAR(100) NOT NULL);""")
        database.commit()
        # cursor.execute("""SELECT MAX(id) FROM db.teachers;""")
        # last_id = cursor.fetchone()[0]
        # if not last_id:
        #     last_id = 0
        cursor.execute(f"""SELECT id FROM db.teachers WHERE name = '{self.name}'; """)
        existing_id = cursor.fetchone()
        if existing_id:
            raise ValueError('\033[93mЦей викладач уже доданий\033[0m')
        else:
            cursor.execute(f"""INSERT INTO db.teachers (name) VALUES ('{self.name}');""")
            database.commit()
        cursor.close()

    def get_courses(self):
        database = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
        )
        cursor = database.cursor()
        cursor.execute("""SELECT count(*) FROM db.courses""")
        if not cursor.fetchone()[0]:
            raise ValueError('\033[93mКурси відсутні\033[0m')
        else:
            cursor.execute(f"""SELECT name, topics FROM courses WHERE teacher = '{self.name}';""")
            courses = cursor.fetchall()
            cursor.close()

            return courses

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('\033[93mНекоретний тип даних! Використовуйте літери.\033[0m')
        if len(value.split()) != 3:
            raise ValueError('\033[93mНекоретний формат імені! Введіть ПІБ.\033[0m')

        self.__name = value

    def str(self):
        return f"Викладач: {self.name}"


class ICourseFactory(ABC):
    @staticmethod
    @abstractmethod
    def add_teacher(name):
        pass

    @staticmethod
    @abstractmethod
    def create_local_course(title, teachers, program, room):
        pass

    @staticmethod
    @abstractmethod
    def create_offsite_course(title, teachers, program, place):
        pass


class CourseFactory(ICourseFactory):
    @staticmethod
    def add_teacher(name):
        return Teacher(name)

    @staticmethod
    def create_local_course(title, teachers, program, room):
        return LocalCourse(title, teachers, program, room)

    @staticmethod
    def create_offsite_course(title, teachers, program, place):
        return OffsiteCourse(title, teachers, program, place)


def main():
    pass


main()
