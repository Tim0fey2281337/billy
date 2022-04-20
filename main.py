from flask import *
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
from flask_login import *
from forms.login import LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Добавить')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Функция показывающая первоначальное окно с выборов Войти или зарегестрироваться
@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    users = db_sess.query(User).all()
    '''if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)'''

    # Возвращаем html с заданными данными для переменных
    return render_template("base1.html", news=news, users=users)


# Функция показывающая главную сраницу сайта,
@app.route("/pervaya")
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def pervaya():
    # Подключаем бызу данных так как используем в html от туда данные
    db_sess = db_session.create_session()

    # Задаём переменные
    news = db_sess.query(News).all()
    users = db_sess.query(User).all()

    # Проверка
    '''if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)'''

    # Возвращаем html с заданными данными для переменных
    return render_template("index.html", news=news, users=users)


# Функция показывающая сраницу сайта с добавлением записок или просмотром их.
@app.route('/fridge')
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def fridge():
    # Подключаем бызу данных так как используем в html от туда данные
    db_sess = db_session.create_session()

    # Задаём переменные
    news = db_sess.query(News).all()
    users = db_sess.query(User).all()

    # Проверка
    '''if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)'''

    # Возвращаем html с заданными данными для переменных
    return render_template('1fri.html', news=news, users=users)


# Функция показывающая сраницу сайта с записками всех пользователей.
@app.route('/fr_so')
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def fge():
    # Подключаем бызу данных так как используем в html от туда данные
    db_sess = db_session.create_session()

    # Задаём переменные
    news = db_sess.query(News).all()
    users = db_sess.query(User).all()

    # Проверка
    '''if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)'''

    # Возвращаем html с заданными данными для переменных
    return render_template('fridge.html', news=news, users=users)


# Функция показывающая сраницу сайта с личными записками пользователя.
@app.route('/fr_se')
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def fde():
    # Подключаем бызу данных так как используем в html от туда данные
    db_sess = db_session.create_session()

    # Задаём переменные
    news = db_sess.query(News).all()
    users = db_sess.query(User).all()

    # Проверка
    '''if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)'''

    # Возвращаем html с заданными данными для переменных
    return render_template('fridge_se.html', news=news, users=users)


# Функция показывающая сраницу сайта с лвидео из холодильника .
@app.route('/video_fridge', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def vid_fr():
    # Возвращаем html
    return render_template('ar.html')


# Функция показывающая сраницу сайта с картинками из морозильника.
@app.route('/image_fridge', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def img_fr():
    # Возвращаем html
    return render_template('img-fr.html')


# Функция отвечающая за процесс регистрации на сайте
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        # Переходим на страничку авторизации
        return redirect('/login')

    # Возвращаем html с заданными данными для переменных
    return render_template('register.html', title='Регистрация', form=form)


# Функция отвечающая за вход на сайт пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Если форма логина прошла валидацию, мы находим пользователя с введенной почтой, проверяем, введен ли для него
    # правильный пароль, если да, вызываем функцию login_user модуля flask-login и передаем туда объект нашего
    # пользователя, а также значение галочки «Запомнить меня».
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            # Переходим на главную страницу
            return redirect("/pervaya")

        # Возвращаем html с заданными данными для переменных
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    # Возвращаем html с заданными данными для переменных
    return render_template('login.html', title='Авторизация', form=form)


# Функция отвечающая за выход из аккаунта
@app.route('/logout')
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def logout():
    logout_user()

    # Переходим на привественную страничку
    return redirect("/")


# Функция отвечающая за добаление записок
@app.route('/news', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def add_news():
    form = NewsForm()
    # Добаляем записку
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()

        # Переходим на страницу с записками
        return redirect('/fridge')

    # Возвращаем html с заданными данными для переменных
    return render_template('news.html', title='Добавление новости',
                           form=form)


# Функция отвечающая за редактирование общедоступной записки
@app.route('/news/<int:id>', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def edit_news(id):
    form = NewsForm()
    # Если мы запросили страницу записи, ищем ее в базе по id, причем автор записки должен совпадать с
    # текущим пользователем.
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()

        # Если что-то нашли, предзаполняем форму
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private

        # Иначе показываем пользователю страницу 404.
        else:
            abort(404)

    # Такую же проверку на всякий случай делаем перед изменением записки.
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/fr_so')
        else:
            abort(404)

    # Возвращаем html с заданными данными для переменных
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


# Функция отвечающая за редактирование личной записки
@app.route('/news1/<int:id>', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def edit_news1(id):
    form = NewsForm()

    # Если мы запросили страницу записи, ищем ее в базе по id, причем автор записки должен совпадать с
    # текущим пользователем.
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        # Если что-то нашли, предзаполняем форму
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private

        # Иначе показываем пользователю страницу 404.
        else:
            abort(404)

    # Такую же проверку на всякий случай делаем перед изменением записки.
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/fr_se')
        else:
            abort(404)

    # Возвращаем html с заданными данными для переменных
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


# Функция отвечающая за удаление общедоступной записки
@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/fr_so')


# Функция отвечающая за удаление личной записки
@app.route('/news_delete1/<int:id>', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def news_delete1(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/fr_se')


# Функция отвечающая за страничку с тестом о Генадии Горине
@app.route('/test', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def test_g():
    k = 0

    # Открываем страницу с формой
    if request.method == 'GET':
        return render_template('forma_test.html')

    # Собираем ответы пользователя
    elif request.method == 'POST':

        # Проверяем ответы чтобы узнать кол-во баллов
        if request.form['class1'] == 'Орёл':
            k += 1
        if request.form['class2'] == '1972':
            k += 1
        if request.form['class3'] == 'Табуретки':
            k += 1
        if request.form['class4'] == 'Гта Сан Андреас':
            k += 1
        if request.form['class5'] == 'Горин':
            k += 1
        if request.form['class6'] == 'FL Studio':
            k += 1
        if request.form['class7'] == 'Понос':
            k += 1

        # ПОдсчёт баллов в процентах
        res = float(str(k / 7)[0:4]) * 100

        # Условия для отображения результатов
        if res < 57:
            res = str(res) + '%'

            # Возвращаем html с заданными данными для переменных
            return render_template('res_sad.html', res_p=res)
        if 57 <= res <= 71:
            res = str(res) + '%'

            # Возвращаем html с заданными данными для переменных
            return render_template('res_norm.html', res_p=res)
        if res > 71:
            res = str(res) + '%'

            # Возвращаем html с заданными данными для переменных
            return render_template('res_fun.html', res_p=res)


# Функция отвечающая за личный кабинет (профиль)
@app.route('/profile', methods=['GET', 'POST'])
# На страничку можно попасть только если пользователь вошёл в аккаунт
@login_required
def profile():
    # Подключаем бызу данных так как используем в html от туда данные
    db_sess = db_session.create_session()

    # Задаём переменные
    news = db_sess.query(News).all()
    users = db_sess.query(User).all()

    # Проверка
    '''if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)'''

    # Возвращаем html с заданными данными для переменных
    return render_template('profile.html', news=news, users=users)


# Функция отвечающая за подключение базы данных
def main():
    db_session.global_init("db/blogs.db")
    app.run()


# Запуск
if __name__ == '__main__':
    main()
