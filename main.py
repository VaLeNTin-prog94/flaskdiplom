from flask import Flask, render_template, request, flash
from sqlalchemy.orm import sessionmaker
from models.model import *

app = Flask(__name__)
# подключение к базе данных
DBSession = sessionmaker(bind=engine)
db = DBSession()
engine = create_engine('sqlite:///diplom.db?check_same_thread=False')

# секретный ключ для отображения и шифрования
app.config['SECRET_KEY'] = 'ffdfdfdf3232fdfff2ds'

# список для отображения главного меню и ссылок к ним
menu = [{'title': "Главная", 'url_name': 'index'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Регистрация", 'url_name': 'registration'},
        {'title': "Войти", 'url_name': 'login'},
        ]
# Записываем все обхекты класса Category для дальнейшей обработки
category = db.query(Category).all()
# Записываем все обхекты класса Bakes для дальнейшей обработки
bakes = db.query(Bakes).all()
# Записываем все обхекты класса User для дальнейшей обработки
user = db.query(User).all()


@app.route("/index")
@app.route("/")
def index():
    """
    Функция вывода общей информации
    :return:Отображает шаблон template_name_or_list из папки шаблонов с заданным контекстом context
    """
    return render_template('index.html', menu=menu, category=category, bakes=bakes)


@app.route("/about")
def about():
    """
    Функция вывода информации о сайте
    :return:Отображает шаблон template_name_or_list из папки шаблонов с заданным контекстом context
    """
    "Функция выводит информаицю о сайте"
    return render_template('about.html', menu=menu, category=category)


@app.route("/contact")
def contact():
    """
    Функция вывода информации о контактов сайта
    :return: Отображает шаблон template_name_or_list из папки шаблонов с заданным контекстом context
    """
    return render_template('contact.html', menu=menu, category=category)


@app.route("/add_page", methods=['POST', "GET"])
def add_page():
    """
    Функция добавления в базу данных информации о Выпечка. Пользователь заполняет
    Форму и отправляет данные.
    'flash' вывод если данные не корректны
    :return: Отображает шаблон template_name_or_list из папки шаблонов с заданным контекстом context
    """
    if request.method == "POST":
        newbakes = Bakes(title=request.form['title'],
                         text=request.form['text'],
                         cat_id=db.query(Category).filter(Category.name == request.form['category']).first().id)
        db.add(newbakes)
        db.commit()
    return render_template('add_page.html', menu=menu, category=category)


@app.route("/login", methods=['POST', "GET"])
def login():
    """
        Функция входа в систему, проверка логина и пароля пользователя.
        'flash' вывод если данные не корректны
        :return: Отображает шаблон template_name_or_list из папки шаблонов с заданным контекстом context
        """
    if request.method == "POST":
        if request.form['username'] not in [b.username for b in user]:
            flash('Такого пользователя не существует', category='error')
        elif request.form['username'] in [b.username for b in user] and \
                request.form['password'] != db.query(User).filter(
            User.username == request.form['username']).first().password:
            flash('Введенный пароль не правильный, повторите попытку', category='error')
        else:
            flash('Поздравялем с успешным входом в систему', category='succes')

    return render_template('login.html', menu=menu, category=category)


#
@app.route("/registration", methods=['POST', "GET"])
def registrtion():
    """
            Функция регистрации в системе. Проверяется валидация данных.
            Длина логина, равенство паролей и првоерка возраста
            'flash' вывод если данные не корректны
            'flash' вывод "Успешная регистрация " данные коррентны и добавились в базу данных
            :return: Отображает шаблон template_name_or_list из папки шаблонов с заданным контекстом context
    """
    if request.method == "POST":
        if len(request.form['username']) < 7:
            flash('Логин должен состоять из 8 или больше символов', category='error')
        elif len(request.form['password']) < 5:
            flash('Пароль должен состоять из 5 или больше символов', category='error')
        elif request.form['password'] != request.form['repeat_password']:
            flash("Пароли не совпадают", category='error')
        elif int(request.form['age']) < 18:
            flash("Возраст должен быть больше 18 лет", category='error')
        elif request.form['username'] in [b.username for b in user]:
            flash("Такой пользователь существует", category='error')
        else:
            users = User(username=request.form['username'],
                         password=request.form['password'],
                         age=request.form['age'])
            flash("Успешная регистрация", category='succes')
            db.add(users)
            db.commit()
    return render_template('registration.html', menu=menu, category=category)


if __name__ == "__main__":
    app.run(debug=True)
