from abc import ABC, abstractmethod
import mysql.connector


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
    def get_courses(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Teacher(ITeacher):
    def __init__(self, name):
        self.name = name

        self.add()  # аналогічно як із курсами

    def get_courses(self):  # беремо дані з бази даних, щоб у викладача не було змінної "courses"
        database = mysql.connector.connect(host='localhost', user='root', password='password')
        cursor = database.cursor()
        cursor.execute("""SELECT count(*) FROM db.courses""")
        if not cursor.fetchone()[0]:
            raise ValueError('\033[93mКурси відсутні\033[0m')
        else:
            cursor.execute(f"""SELECT name, topics FROM db.courses WHERE teacher = '{self.name}';""")
            courses = cursor.fetchall()
            cursor.close()

            return courses

    def add(self):
        database = mysql.connector.connect(host='localhost', user='root', password='password')
        cursor = database.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS db;""")
        database.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS db.teachers (
                          id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          name VARCHAR(100) NOT NULL);""")
        database.commit()

        cursor.execute(f"""SELECT id FROM db.teachers WHERE name = '{self.__name}'; """)
        existing_id = cursor.fetchone()
        if not existing_id:
            cursor.execute(f"""INSERT INTO db.teachers (name) VALUES ('{self.__name}');""")
            database.commit()
        cursor.close()

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

    def __str__(self):
        return f"{self.__name}"


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
    def get_teachers(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def add_teacher(self, teacher):
        pass

    @abstractmethod
    def delete_teacher(self, teacher):
        pass

    @abstractmethod
    def add_topic(self, topic):
        pass

    @abstractmethod
    def delete_topic(self, topic):
        pass


class Course(ICourse):
    def __init__(self, title, teachers, program):
        self.title = title
        self.teachers = teachers
        self.program = program

        self.add()  # зміст цієї функції міг бути прямо тут в інітері, але її ліпше винести окремо

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

    def get_teachers(self):
        str_teachers = []
        for teacher in self.__teachers:
            str_teachers.append(str(teacher))
        return str_teachers

    def add(self):
        database = mysql.connector.connect(host='localhost', user='root', password='password')
        cursor = database.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS db;""")
        database.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS db.courses (
                          id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          title VARCHAR(150) NOT NULL,
                          teachers VARCHAR(180) NOT NULL,
                          program VARCHAR(220) NOT NULL);""")
        database.commit()

        cursor.execute(f"SELECT id FROM db.courses WHERE title = '{self.__title}';")
        existing_id = cursor.fetchone()
        if not existing_id:
            query = """INSERT INTO db.courses (title, teachers, program) VALUES (?, ?, ?)"""
            cursor.execute(query, (self.__title, ', '.join(self.get_teachers()), ', '.join(self.__program)))
            database.commit()
        cursor.close()

    def add_teacher(self, teacher):
        if isinstance(teacher, Teacher):
            if teacher not in self.__teachers:
                self.__teachers.append(teacher)
                self.update_teachers()
            else:
                raise ValueError('\033[93mТакий викладач вже є на цьому курсі.\033[0m')
        else:
            raise TypeError('\033[93mВи намагаєтеся додати до списку викладачів НЕ викладача.\033[0m')

    def delete_teacher(self, teacher):
        if isinstance(teacher, Teacher):
            if teacher in self.__teachers:
                self.__teachers.remove(teacher)
                self.update_teachers()
            else:
                raise ValueError('\033[93mТакого викладача немає на цьому курсі.\033[0m')
        else:
            raise TypeError('\033[93mВи намагаєтеся видалити зі списку викладачів НЕ викладача.\033[0m')

    def update_teachers(self):
        database = mysql.connector.connect(host='localhost', user='root', password='password')
        cursor = database.cursor()
        cursor.execute(f"""UPDATE db.courses
                           SET teachers = '{', '.join(self.get_teachers())}'
                           WHERE title = '{self.__title}';""")
        database.commit()
        cursor.close()

    def add_topic(self, topic):
        if isinstance(topic, str):
            if topic not in self.__program:
                self.__program.append(topic)
                self.update_program()
            else:
                raise ValueError('\033[93mТака тема вже є у програмі цього курсу.\033[0m')
        else:
            raise TypeError('\033[93mВи намагаєтеся додати до списку тем НЕ тему.\033[0m')

    def delete_topic(self, topic):
        if isinstance(topic, str):
            if topic in self.__program:
                self.__program.remove(topic)
                self.update_program()
            else:
                raise ValueError('\033[93mТакої теми немає у програмі цього курсу.\033[0m')
        else:
            raise TypeError('\033[93mВи намагаєтеся видалити із списку тем НЕ тему.\033[0m')

    def update_program(self):
        database = mysql.connector.connect(host='localhost', user='root', password='password')
        cursor = database.cursor()
        cursor.execute(f"""UPDATE db.courses
                                       SET program = '{', '.join(self.__program)}' \
                                       WHERE title = '{self.__title}';""")
        database.commit()
        cursor.close()


class ILocalCourse(ABC):
    @property
    @abstractmethod
    def room(self):
        pass

    @room.setter
    @abstractmethod
    def room(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass


class IOffsiteCourse(ABC):
    @property
    @abstractmethod
    def place(self):
        pass

    @place.setter
    @abstractmethod
    def place(self, value):
        pass

    @abstractmethod
    def __str__(self):
        pass


class LocalCourse(Course, ILocalCourse):
    def __init__(self, title, teachers, program, room):
        super().__init__(title, teachers, program)  # батьківський інітер викличе метод add()

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

    def __str__(self):
        return f"\033[92m\033[1mКурс:\033[0m {self.title}\n" \
               f"\033[92m\033[1mВикладач(і):\033[0m {', '.join(self.get_teachers())}\n" \
               f"\033[92m\033[1mПрограма:\033[0m {', '.join(self.program)}\n" \
               f"\033[92m\033[1mАудиторія:\033[0m {self.__room}\n"


class OffsiteCourse(Course, IOffsiteCourse):
    def __init__(self, title, teachers, program, place):
        super().__init__(title, teachers, program)  # батьківський інітер викличе метод add()
        self.place = place

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if not isinstance(value, str):
            raise TypeError('Місце проведення занять повинне бути текстовою стрічкою.')
        self.__place = value

    def __str__(self):
        return f"\033[92m\033[1mКурс:\033[0m {self.title}\n" \
               f"\033[92m\033[1mВикладач(і):\033[0m {', '.join(self.get_teachers())}\n" \
               f"\033[92m\033[1mПрограма:\033[0m {', '.join(self.program)}\n" \
               f"\033[92m\033[1mМісце проведення занять:\033[0m {self.__place}\n"


class ICourseFactory(ABC):
    @staticmethod
    @abstractmethod
    def add_teacher(name):
        pass

    @staticmethod
    @abstractmethod
    def add_local_course(title, teachers, program, room):
        pass

    @staticmethod
    @abstractmethod
    def add_offsite_course(title, teachers, program, place):
        pass


class CourseFactory(ICourseFactory):
    @staticmethod
    def add_teacher(name):
        return Teacher(name)

    @staticmethod
    def add_local_course(title, teachers, program, room):
        return LocalCourse(title, teachers, program, room)

    @staticmethod
    def add_offsite_course(title, teachers, program, place):
        return OffsiteCourse(title, teachers, program, place)


def main():
    try:
        factory = CourseFactory()
        teacher_one = factory.add_teacher('Денисенко Віктор Андрійович')
        teacher_two = factory.add_teacher('Лемчук Анатолій Ігорович')
        teacher_three = factory.add_teacher('Кряковська Вікторія Михайлівна')
        teacher_four = factory.add_teacher('Рябко Олена Костянтинівна')
        teacher_five = factory.add_teacher('Коваль Леонід Сергійович')

        programming = factory.add_offsite_course('Основи програмування', teacher_one,
                                                 ['цикли', 'функції', 'вказівники', 'I/O'], 'online')
        maths = factory.add_local_course('Математичний аналіз', [teacher_two, teacher_three],
                                         ['границі', 'похідна', 'невизначений інтеграл', 'ряди'], 314)

        programming.add_teacher(teacher_four)
        programming.add_topic('структури')
        programming.delete_topic('I/O')

        maths.delete_teacher(teacher_three)
        maths.add_teacher(teacher_five)
        maths.delete_topic('ряди')
        maths.add_topic('визначений інтеграл')
        maths.room = 410

        print('\n', programming, '\n', maths, sep='')

    except TypeError as tError:
        print(tError)
    except ValueError as vError:
        print(vError)


main()
