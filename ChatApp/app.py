from flask import Flask, redirect, session, url_for, render_template, request, flash, send_from_directory
from datetime import timedelta
import os
import re
import uuid
import hashlib
import calendar

from models import Customer, Stylist, Channel, Message
from datetime import datetime

# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 静的ファイルをキャッシュする設定
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400
# bundle_css_files(app)

# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return redirect(url_for('main_view'))


# サインアップページの表示(顧客)
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')

# サインアップページの表示(店舗)
@app.route('/signup_staff', methods=['GET'])
def signup_staff_view():
    return render_template('auth/signup_staff.html')


# サインアップ処理(顧客)
@app.route('/signup', methods=['POST'])
def signup_process():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')

    if name == '' or email =='' or phone == '' or gender == '' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        customer_id = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = Customer.find_by_email(email)

        if registered_user != None:
            flash('既に登録されているようです')
        else:
            Customer.create(customer_id, name, email, phone, gender, password)
            Channel.Create_customers_stylists(customer_id)
            UserId = str(customer_id)
            session['uid'] = UserId
            return redirect(url_for('main_view'))
    return redirect(url_for('signup_process'))

# サインアップ処理(店舗)
@app.route('/signup_staff', methods=['POST'])
def signup_staff_process():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')

    if name == '' or email =='' or phone == '' or gender == '' or password == '' or passwordConfirmation == '':
        flash('空のフォームがあるようです')
    elif password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        stylist_id = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = Stylist.find_by_email(email)

        if registered_user != None:
            flash('既に登録されているようです')
        else:
            Stylist.create(stylist_id, name, email, phone, gender, password)
            Channel.Create_stylists_customers(stylist_id)
            UserId = str(stylist_id)
            session['uid'] = UserId
            return redirect(url_for('channels_stylist_view'))
    return redirect(url_for('signup_staff_process'))


# ログインページの表示（顧客）
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')

# ログインページの表示（店舗）
@app.route('/login_staff', methods=['GET'])
def login_staff_view():
    return render_template('auth/login_staff.html')

# ログイン処理（顧客）
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = Customer.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["customer_id"]
                return redirect(url_for('main_view'))
    return redirect(url_for('login_view'))

# ログイン処理（店舗）
@app.route('/login_staff', methods=['POST'])
def login_staff_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = Stylist.find_by_email(email)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["stylist_id"]
                return redirect(url_for('channels_stylist_view'))
    return redirect(url_for('login_staff_view'))


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))


# ユーザーTOPページの表示
@app.route('/main', methods=['GET'])
def main_view():
    return render_template('main.html')


# チャンネル一覧ページの表示（顧客）
@app.route('/channels_user', methods=['GET'])
def channels_user_view():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    else:
        channels_stylist = Channel.get_all_stylists() #cid渡す
        channels_stylist.reverse()
        return render_template('channels_user.html', channels_stylist=channels_stylist, uid=uid)


@app.route('/display_profile/<path:filename>')
def display_profile_process(filename):
    return send_from_directory('uploads', filename)


# チャンネル一覧ページの表示（店舗）
@app.route('/channels_stylist', methods=['GET'])
def channels_stylist_view():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_staff_view'))
    else:
        channels_user = Channel.get_all_customers()
        channels_user.reverse()
        return render_template('channels_stylist.html', channels_user=channels_user, uid=uid)

#顧客チャンネル一覧後、チャット機能に移行する前の処理
#@app.route('/channels_user', methods=['POST'])
#def create_user_channel():
#    uid = session.get('uid')
#    if uid is None:
#        return redirect(url_for('login_view'))
#
#        #Channel.create(uid, channel_name, channel_description)
#    Channel.create(uid)
#    return redirect(url_for('main_view'))

#店舗チャンネル一覧後、チャット機能に移行する前の処理
#@app.route('/channels_stylist', methods=['POST'])
#def create_stylist_channel():
#    uid = session.get('uid')
#    if uid is None:
#        return redirect(url_for('login_staff_view'))
#    
#    Channel.create(uid)
#    return redirect(url_for('channels_stylist_view'))

#顧客チャンネル一覧後、チャット機能に移行する前の処理
@app.route('/channels_user/<cid>/messages', methods=['GET'])
def detail_user_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))

        #Channel.create(uid, channel_name, channel_description)
    channel = Channel.find_by_cid(cid)
    messages = Message.get_all(cid)

    return render_template('messages.html', messages=messages, channel=channel, uid=uid)

#店舗チャンネル一覧後、チャット機能に移行する前の処理
@app.route('/channels_stylist/<cid>/messages', methods=['GET'])
def detail_stylist_channel(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_staff_view'))
    
    channel = Channel.find_by_cid(cid)
    messages = Message.get_all(cid)

    return render_template('messages.html', messages=messages, channel=channel, uid=uid)



#顧客側メッセージの投稿
@app.route('/channels_user/<cid>/messages', methods=['POST'])
def create_user_message(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    message = request.form.get('message')

    if message:
        Message.create(uid, cid, message)

    return redirect('/channels/{cid}/messages'.format(cid = cid))

#店舗側/美容師側メッセージの投稿
@app.route('/channels_stylist/<cid>/messages',methods=['POST'])
def create_stylist_messages(cid):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('channels_stylist_view'))
    
    message = request.form.get('message')

    if message:
        Message.create(uid, cid, message)

    return redirect('/channels_stylist/{cid}/messages'.format(cid = cid))


# 美容師プロフィール編集ページの表示
@app.route('/edit_profile', methods=['GET'])
def edit_profile_view():
    return render_template('auth/edit_profile.html')

# 美容師プロフィールの登録処理
@app.route('/edit_profile', methods=['POST'])
def edit_profile_process():
    if 'file' not in request.files:
        flash('ファイルがありません')
        return redirect(url_for('edit_profile_view'))
    file = request.files['file']
    filename = file.filename
    app.config['uploads'] = 'uploads'
    file.save(os.path.join(app.config['uploads'], filename))

    comment = request.form.get('comment')

    uid = session.get('uid')
    Stylist.edit_profile(uid, filename, comment)
    return render_template('channels_stylist.html')


# 予約ページの表示
@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation_view():
    now = datetime.now()
    year = now.year
    month = now.month
    selected_date = None

    if request.method == 'POST':
        selected_date = request.form.get('date')

    cal = calendar.HTMLCalendar().formatmonth(year, month)
    return render_template('make_reservation.html', calendar=cal, selected_date=selected_date)

# 予約確認ページの表示（顧客）
@app.route('/user_reservation', methods=['GET'])
def user_reservation_view():
    return render_template('user_reservation.html')

# 予約確認ページの表示（店舗）
@app.route('/stylist_reservation', methods=['GET'])
def stylist_reservation_view():
    return render_template('stylist_reservation.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)