import random, string, datetime
from app import app, db
from flask import Flask,request,render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User, Student, Test


@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        Students = Student.query.all()
        if request.method == "POST":
            if 'sow_btn' in request.values:
                num = request.form['num']
                liter = request.form['liter']
                Students = Student.query.filter_by(scClass=num + " " + liter).all()
                if liter == 'all':
                    Students = Student.query.filter_by(scClass=num + " а").all() + \
                               Student.query.filter_by(scClass=num + " б").all() + \
                               Student.query.filter_by(scClass=num + " в").all() + \
                               Student.query.filter_by(scClass=num + " г").all() + \
                               Student.query.filter_by(scClass=num + " д").all()
                if num == 'all':
                    Students = Student.query.filter_by(scClass="1 " + liter).all()
                    for i in range(2, 12):
                        Students += Student.query.filter_by(scClass=str(i) + " " + liter).all()
                if num == "all" and liter == "all":
                    Students = []
                    for ch in ['а', 'б', 'в', 'г', 'д']:
                        Students += Student.query.filter_by(scClass="1 " + ch).all()
                        for i in range(2, 12):
                            Students += Student.query.filter_by(scClass=str(i) + " " + ch).all()

        return render_template("index.html", ths=Students)
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if 'login' in request.values:
            login = request.form['login']
            pas = request.form['password']
            try:
                chk = request.form['chk']
            except:
                chk = 'off'
            print(chk)
            user = User.query.filter_by(username=login).first()
            if user is None or not user.check_password(pas):
                # print(user.check_password(pas))
                return render_template("login.html", alert=1)
            print(login, pas)
            login_user(user, remember=chk)
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if current_user.is_authenticated:
        if request.method == "POST":
            if 'add' in request.values:
                name = request.form['Name']
                sername = request.form['Sername']
                num = request.form['num']
                liter = request.form['liter']
                st = Student(Name=name, Sername=sername, scClass=num+" "+liter)
                db.session.add(st)
                db.session.commit()
                return render_template('theme-create.html')
        return render_template('theme-create.html')
    return redirect(url_for("login"))



@app.route('/del_student/<id>')
def dell_student(id):
    if current_user.is_authenticated:
        Student.query.filter_by(id=id).delete()
        Test.query.filter_by(stud_id=id).delete()
        db.session.commit()
        return redirect(url_for("index"))
    return redirect(url_for("login"))


@app.route('/del_test/<id>')
def del_test(id):
    if current_user.is_authenticated:
        Test.query.filter_by(unq_id=id).delete()
        db.session.commit()
        return redirect(url_for("tests"))
    return redirect(url_for("login"))


@app.route('/add_test', methods=['GET', 'POST'])
def add_test():
    if current_user.is_authenticated:
        Students = Student.query.all()
        if request.method == "POST":
            if 'sow_btn' in request.values:
                num = request.form['num']
                liter = request.form['liter']
                Students = Student.query.filter_by(scClass=num + " " + liter).all()
                if liter == 'all':
                    Students = Student.query.filter_by(scClass=num + " а").all() + \
                               Student.query.filter_by(scClass=num + " б").all() + \
                               Student.query.filter_by(scClass=num + " в").all() + \
                               Student.query.filter_by(scClass=num + " г").all() + \
                               Student.query.filter_by(scClass=num + " д").all()
                if num == 'all':
                    Students = Student.query.filter_by(scClass="1 " + liter).all()
                    for i in range(2, 12):
                        Students += Student.query.filter_by(scClass=str(i) + " " + liter).all()
                if num == "all" and liter == "all":
                    Students = []
                    for ch in ['а', 'б', 'в', 'г', 'д']:
                        Students += Student.query.filter_by(scClass="1 " + ch).all()
                        for i in range(2, 12):
                            Students += Student.query.filter_by(scClass=str(i) + " " + ch).all()

            if 'login' in request.values:
                ids = request.form.getlist('checkbox[]')
                unq = id_generator()
                for id in ids:
                    print(id)
                    print(unq)
                    unq_id = unq
                    test = Test(teacher=request.form['teacher'], subject=request.form['subject'],
                                result=request.form['result'+id], stud_id=id, timestamp=date_conv(request.form['date']),
                                unq_id=unq)
                    db.session.add(test)
                    db.session.commit()
                return redirect(url_for('add_test2', id=unq_id, num=request.form['numq']))
        return render_template('add-test.html', ths=Students)
    return redirect(url_for("login"))


@app.route('/add_test2', methods=['GET', 'POST'])
def add_test2():
    if current_user.is_authenticated:
        unq_id = request.args.get('id')
        n = int(request.args.get('num'))
        tests = Test.query.filter_by(unq_id=unq_id).all()
        print(tests)
        if request.method == "POST":
            if 'send' in request.values:
                for i in tests:
                    ans = request.form.getlist('ans'+str(i.id)+'[]')
                    i.anses = ''.join(ans)
                    print(i.anses)
                    db.session.commit()
                return redirect(url_for('tests'))
        return render_template('add-test1.html', ths=tests, n=n)
    return redirect(url_for("login"))


@app.route('/tests', methods=['GET', 'POST'])
def tests():
    if current_user.is_authenticated:
        tests = Test.query.all()
        idu = '......'
        ths = []
        for test in tests:
            if test.unq_id != idu:
                idu = test.unq_id
                ths.append(test)
            else:
                ...
        return render_template('tests.html', ths=ths)
    return redirect(url_for("login"))


@app.route('/test/<id>', methods=['GET', 'POST'])
def test_e(id):
    if current_user.is_authenticated:
        tests = Test.query.filter_by(unq_id=id).all()
        mid = sum(list(map(lambda x: x.result, tests)))/len(tests)
        print(mid)
        if request.method == "POST":
            if 'show' in request.values:
                return render_template('/test/1.html', ths=tests, mid=mid, asd=1, n=len(tests[0].anses))
            if 'unshow' in request.values:
                return render_template('/test/1.html', ths=tests, mid=mid, asd=0)
        return render_template('/test/1.html', ths=tests, mid=mid, asd=0)
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def date_conv(d):
    return datetime.date(int(d[0:4]), int(d[5:7]), int(d[8:10]))