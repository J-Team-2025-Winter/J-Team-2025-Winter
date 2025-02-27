from flask import Flask, redirect, session, url_for, render_template, request, flash, send_from_directory
from datetime import timedelta
import os
import re
import uuid
import hashlib

from models import Customer, Stylist, Channel, Message, Reservation

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
    cuid = session.get('cuid')
    stid = session.get('stid')

    if stid is None:
        return redirect(url_for('main_view'))
    elif cuid is None:
        return redirect(url_for('channels_stylist_view'))
    else:
        return redirect(url_for('login_view'))


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
            userid = str(customer_id)
            session['cuid'] = userid
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
            userid = str(stylist_id)
            session['stid'] = userid
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
                session['cuid'] = user["customer_id"]
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
                session['stid'] = user["stylist_id"]
                return redirect(url_for('channels_stylist_view'))
    return redirect(url_for('login_staff_view'))


# ログアウト
@app.route('/logout')
def logout():
    # cuid = session.get('cuid')
    # stid = session.get('stid')
    
    session.pop('cuid', None)

    return redirect(url_for('login_view'))
    # if stid is None:
    #     return redirect(url_for('login_view'))
    # elif cuid is None:
    #     return redirect(url_for('login_staff_view'))
    # else:
    #     return redirect(url_for('login_view'))

# ログアウト
@app.route('/logout_staff')
def logout_staff():
    
    session.pop('stid', None)

    return redirect(url_for('login_staff_view'))


# ユーザーTOPページの表示
@app.route('/main', methods=['GET'])
def main_view():
    return render_template('main.html')


# チャンネル一覧ページの表示（顧客）
@app.route('/channels_user', methods=['GET'])
def channels_user_view():
    cuid = session.get('cuid')
    if cuid is None:
        return redirect(url_for('login_view'))
    else:
        channels_stylist = Channel.get_all_stylists(cuid)
        channels_stylist.reverse()
        return render_template('channels_user.html', channels_stylist=channels_stylist)


@app.route('/display_profile/<filename>')
def display_profile_process(filename):
    return send_from_directory('uploads', filename)


# チャンネル一覧ページの表示（店舗）
@app.route('/channels_stylist', methods=['GET'])
def channels_stylist_view():
    stid = session.get('stid')
    if stid is None:
        return redirect(url_for('login_staff_view'))
    else:
        channels_user = Channel.get_all_customers(stid)
        channels_user.reverse()
        return render_template('channels_stylist.html', channels_user=channels_user)

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
@app.route('/channels_user/<int:cid>/messages', methods=['GET'])#cid→sid(stylist_id), 1.customer_stylistのレコードを作成 2.GETメソッドでメッセージを表示
def detail_user_channel(cid):
    cuid = session.get('cuid')
    if cuid is None:
        return redirect(url_for('login_view'))

        #Channel.create(uid, channel_name, channel_description)
    #channel = Channel.find_by_cid(cid)
    chatname = Message.get_name_userside(cid)
    messages = Message.get_all(cid)
    messages = messages

    #return render_template('messages.html', messages=messages, channel=channel, uid=uid)
    return render_template('messages_user.html', chatname=chatname, messages=messages, cuid=cuid, cid=cid)#render_template　処理が終わる→ redirect(WebページのURLを変更した際に、自動的に別のURLに転送する仕組み)　別のURLアクションにリダイレクトできる

#店舗チャンネル一覧後、チャット機能に移行する前の処理
@app.route('/channels_stylist/<int:cid>/messages', methods=['GET'])
def detail_stylist_channel(cid):
    stid = session.get('stid')
    if stid is None:
        return redirect(url_for('login_staff_view'))
    
    #channel = Channel.find_by_cid(cid)
    messages = Message.get_all(cid)

    #return render_template('messages.html', messages=messages, channel=channel, uid=uid)
    return render_template('messages_stylist.html', messages=messages, stid=stid, cid=cid)



#顧客側メッセージの投稿
@app.route('/channels_user/<cid>/messages', methods=['POST'])
def create_user_message(cid):
    cuid = session.get('cuid')
    if cuid is None:
        return redirect(url_for('login_view'))
    
    message = request.form.get('message')

    if message:
        uid = cuid
        Message.create(message, uid, cid)

    return redirect('/channels_user/{cid}/messages'.format(cid = cid))

#店舗側/美容師側メッセージの投稿
@app.route('/channels_stylist/<cid>/messages',methods=['POST'])
def create_stylist_messages(cid):
    stid = session.get('stid')
    if stid is None:
        return redirect(url_for('channels_stylist_view'))
    
    message = request.form.get('message')

    if message:
        uid = stid
        Message.create(message, uid, cid)

    return redirect('/channels_stylist/{cid}/messages'.format(cid = cid))


# 顧客プロフィール編集ページの表示
@app.route('/edit_user_profile', methods=['GET'])
def edit_user_profile_view():
    return render_template('auth/edit_user_profile.html')

# 顧客プロフィールの更新処理
@app.route('/edit_user_profile', methods=['POST'])
def edit_user_profile_process():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    password = request.form.get('password').strip()
    passwordConfirmation = request.form.get('password-confirmation').strip()

    if password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif email != "" and re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        cuid = session.get('cuid')
        Customer.edit_profile(cuid, name, email, phone, gender, password)
        return render_template('main.html')
    return redirect(url_for('edit_user_profile_view'))

# 美容師プロフィール編集ページの表示
@app.route('/edit_stylist_profile', methods=['GET'])
def edit_stylist_profile_view():
    return render_template('auth/edit_stylist_profile.html')

# 美容師プロフィールの更新処理
@app.route('/edit_stylist_profile', methods=['POST'])
def edit_stylist_profile_process():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    password = request.form.get('password').strip()
    passwordConfirmation = request.form.get('password-confirmation').strip()      
    file = request.files['file']
    comment = request.form.get('comment')

    if password != passwordConfirmation:
        flash('二つのパスワードの値が違っています')
    elif email != "" and re.match(EMAIL_PATTERN, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        stid = session.get('stid')
        Stylist.edit_profile(stid, name, email, phone, gender, password, file, comment)
        return redirect(url_for('channels_stylist_view'))
    return redirect(url_for('edit_stylist_profile_view'))


# 予約ページの表示
@app.route('/make_reservation/<cid>', methods=['GET', 'POST'])
def make_reservation_view(cid):
    cuid = session.get('cuid')
    if cuid is None:
        return redirect(url_for('login_view'))

    if request.method == 'POST':
        cuid = session.get('cuid')
        selected_date = request.form.get('date')
        Reservation.create(cuid, selected_date, cid)
        message = f"{selected_date}で予約しました！"
        uid = cuid
        Message.create(message, uid, cid)
        return redirect(url_for('detail_user_channel', cid=cid))

    return render_template('make_reservation.html', cid=cid)

# 予約確認ページの表示（顧客）
# @app.route('/user_reservation', methods=['GET'])
# def user_reservation_view():
#     return render_template('user_reservation.html')

# 予約確認ページの表示（店舗）
@app.route('/stylist_reservation', methods=['GET'])
def stylist_reservation_view():
    reservations = Reservation.get_all_reservations()
    return render_template('stylist_reservation.html', reservations=reservations)


# テンプレートの表示
@app.route('/template/<cid>', methods=['GET', 'POST'])
def template_view(cid):
    cuid = session.get('cuid')
    if cuid is None:
        return redirect(url_for('login_view'))

    if request.method == 'POST':
        cuid = session.get('cuid')
        uid = cuid
        cut = request.form.get('cut')
        color = request.form.get('color')
        parma = request.form.get('parma')
        message = f"CUT：{cut}\nCOLOR：{color}\nPARMA：{parma}".replace("\n", "<br>")
        Message.create(message, uid, cid)
        return redirect(url_for('detail_user_channel', cid=cid))

    return render_template('template.html', cid=cid)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)