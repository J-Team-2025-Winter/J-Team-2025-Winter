from flask import Flask, abort
import pymysql
from util.DB import DB
import hashlib
import os


app = Flask(__name__)


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# 顧客クラス
class Customer:
   @classmethod
   def create(cls, customer_id, name, email, phone, gender, password):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO customers (customer_id, customer_name, email, phone, gender, password) VALUES (%s, %s, %s, %s, %s, %s);"
               cur.execute(sql, (customer_id, name, email, phone, gender, password,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


   @classmethod
   def find_by_email(cls, email):
       conn = db_pool.get_conn()
       try:
               with conn.cursor() as cur:
                   sql = "SELECT * FROM customers WHERE email=%s;"
                   cur.execute(sql, (email,))
                   user = cur.fetchone()
               return user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

#    @classmethod
#    def find_by_uid(cls, cuid):
#        conn = db_pool.get_conn()
#        try:
#                with conn.cursor() as cur:
#                    sql = "SELECT * FROM customers WHERE customer_id=%s;"
#                    cur.execute(sql, (cuid,))
#                    customer = cur.fetchone()
#                return customer
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)

   @classmethod
   def edit_profile(cls, cuid, name, email, phone, gender, password):
       # set_clauseとparamsを定義する 
       set_clause = []
       params = []

       if name: #「nameが空文字列、None、Falseでない場合」のPythonicな書き方
           set_clause.append("customer_name=%s") # set_clauseに「customer_name=%s」を追加する
           params.append(name) # paramsに「name」を追加する
       if email:
           set_clause.append("email=%s")
           params.append(email)
       if phone:
           set_clause.append("phone=%s")
           params.append(phone)
       if gender:
           set_clause.append("gender=%s")
           params.append(gender)
       if password:
           password = hashlib.sha256(password.encode('utf-8')).hexdigest()
           set_clause.append("password=%s")
           params.append(password)

       if set_clause:
           conn = db_pool.get_conn()
           try:
                with conn.cursor() as cur: #「', '.join(set_clause)」で、set_clauseに追加したものを「, 」で結合する
                    sql = f"UPDATE customers SET {', '.join(set_clause)} WHERE customer_id=%s;"
                    params.append(cuid)
                    cur.execute(sql, params) # paramsに追加したものが「%s」に充てられる
                    conn.commit()
           except pymysql.Error as e:
                print(f'エラーが発生しています：{e}')
                abort(500)
           finally:
                db_pool.release(conn)

# 美容師クラス
class Stylist:
   @classmethod
   def create(cls, stylist_id, name, email, phone, gender, password):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO stylists (stylist_id, stylist_name, email, phone, gender, password, profile_picture_url) VALUES (%s, %s, %s, %s, %s, %s, %s);"
               cur.execute(sql, (stylist_id, name, email, phone, gender, password, 'No Images',))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

   @classmethod
   def find_by_email(cls, email):
       conn = db_pool.get_conn()
       try:
               with conn.cursor() as cur:
                   sql = "SELECT * FROM stylists WHERE email=%s;"
                   cur.execute(sql, (email,))
                   user = cur.fetchone()
               return user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

#    @classmethod
#    def find_by_uid(cls, stid):
#        conn = db_pool.get_conn()
#        try:
#                with conn.cursor() as cur:
#                    sql = "SELECT * FROM stylists WHERE stylist_id=%s;"
#                    cur.execute(sql, (stid,))
#                    stylist = cur.fetchone()
#                return stylist
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)

   @classmethod
   def edit_profile(cls, stid, name, email, phone, gender, password, file, comment):
       # set_clauseとparamsを定義する 
       set_clause = []
       params = []

       if name: #「nameが空文字列、None、Falseでない場合」のPythonicな書き方
           set_clause.append("stylist_name=%s") # set_clauseに「customer_name=%s」を追加する
           params.append(name) # paramsに「name」を追加する
       if email:
           set_clause.append("email=%s")
           params.append(email)
       if phone:
           set_clause.append("phone=%s")
           params.append(phone)
       if gender:
           set_clause.append("gender=%s")
           params.append(gender)
       if password:
           password = hashlib.sha256(password.encode('utf-8')).hexdigest()
           set_clause.append("password=%s")
           params.append(password)
       if file:
           filename = file.filename
           app.config['uploads'] = 'uploads'
           file.save(os.path.join(app.config['uploads'], filename))
           set_clause.append("profile_picture_url=%s")
           params.append(filename)
       if comment:
           set_clause.append("comment=%s")
           params.append(comment)

       if set_clause:
           conn = db_pool.get_conn()
           try:
                with conn.cursor() as cur: #「', '.join(set_clause)」で、set_clauseに追加したものを「, 」で結合する
                    sql = f"UPDATE stylists SET {', '.join(set_clause)} WHERE stylist_id=%s;"
                    params.append(stid)
                    cur.execute(sql, params) # paramsに追加したものが「%s」に充てられる
                    conn.commit()
           except pymysql.Error as e:
                print(f'エラーが発生しています：{e}')
                abort(500)
           finally:
                db_pool.release(conn)


# チャンネルクラス
class Channel:
    @classmethod
    def Create_customers_stylists(cls, customer_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # すべてのstylist_idを取得
                cur.execute("SELECT stylist_id FROM stylists;")
                stylist_ids = cur.fetchall()
                # customer_idとstylist_idを紐づける
                sql = "INSERT INTO customers_stylists (customer_id, stylist_id) VALUES (%s, %s);"
                for stylist in stylist_ids:
                    cur.execute(sql, (customer_id, stylist['stylist_id'],))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def Create_stylists_customers(cls, stylist_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                # すべてのcustomer_idを取得
                cur.execute("SELECT customer_id FROM customers;")
                customer_ids = cur.fetchall()
                # customer_idとstylist_idを紐づける
                sql = "INSERT INTO customers_stylists (customer_id, stylist_id) VALUES (%s, %s);"
                for customer in customer_ids:
                    cur.execute(sql, (customer['customer_id'], stylist_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    #app.pyのChannel.create(uid, channel_name, channel_description), cls →カーソルコマンド
    def create(cls, customer_id, stylist_id):
        #conn = db_pool.get_conn() →データベースに接続
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO customers_stylists (customer_id, stylist_id) VALUES (%s, %s);"
                cur.execute(sql, (customer_id, stylist_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all_customers(cls, stid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM customers AS c INNER JOIN customers_stylists AS cs ON c.customer_id = cs.customer_id WHERE stylist_id = (%s);"
               cur.execute(sql, (stid,))
               channels_user = cur.fetchall()
               return channels_user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

    @classmethod
    def get_all_stylists(cls, cuid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM stylists AS s INNER JOIN customers_stylists AS cs ON s.stylist_id = cs.stylist_id WHERE customer_id = (%s);"
               cur.execute(sql, (cuid,))
               channels_stylist = cur.fetchall()
               return channels_stylist
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


    @classmethod
    def find_by_cid(cls, cid):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "SELECT * FROM customers_stylists WHERE cid=%s;"
                cur.execute(sql, (cid,))
                channel = cur.fetchone()
                return channel
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)


#    @classmethod
#    def find_by_name(cls, channel_name):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = "SELECT * FROM channels WHERE name=%s;"
#                cur.execute(sql, (channel_name,))
#                channel = cur.fetchone()
#                return channel
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)


#    @classmethod
#    def update(cls, uid, new_channel_name, new_channel_description, cid):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = "UPDATE channels SET uid=%s, name=%s, abstract=%s WHERE id=%s;"
#                cur.execute(sql, (uid, new_channel_name, new_channel_description, cid,))
#                conn.commit()
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)


#    @classmethod
#    def delete(cls, cid):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = "DELETE FROM channels WHERE id=%s;"
#                cur.execute(sql, (cid,))
#                conn.commit()
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)


# メッセージクラス
class Message:
   @classmethod
   def create(cls, message, uid, cid):#message= content
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO messages(content, uid, cid) VALUES(%s, %s, %s);"
               cur.execute(sql, (message, uid, cid,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

   @classmethod
   def get_name_userside(cls, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT stylist_name FROM customers_stylists AS cs INNER JOIN stylists AS s ON cs.stylist_id = s.stylist_id WHERE customers_stylists_id = %s;" # [hiyo]「WHERE cid = %s」を追記
               cur.execute(sql, (cid,))
               chatname = cur.fetchall()
               return chatname[0]['stylist_name'] if chatname else None
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

   @classmethod
   def get_name_staffside(cls, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT customer_name FROM customers_stylists AS cs INNER JOIN customers AS c ON cs.customer_id = c.customer_id WHERE customers_stylists_id = %s;"
               cur.execute(sql, (cid,))
               chatname = cur.fetchall()
               return chatname[0]['customer_name'] if chatname else None
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

   @classmethod
   def get_all(cls, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM messages WHERE cid = %s;" # [hiyo]「WHERE cid = %s」を追記
               cur.execute(sql, (cid,))
               messages = cur.fetchall()
               return messages
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


#    @classmethod
#    def delete(cls, message_id):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = "DELETE FROM messages WHERE id=%s;"
#                cur.execute(sql, (message_id,))
#                conn.commit()
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)

# 予約クラス
class Reservation:
   @classmethod
   def create(cls, cuid, selected_date, cid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = """
               INSERT INTO reservations(customer_id, stylist_id, reservation_date)
               SELECT %s, cs.stylist_id, %s
               FROM customers_stylists AS cs
               WHERE customers_stylists_id = %s;
               """
               cur.execute(sql, (cuid, selected_date, cid))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

   @classmethod
   def get_all_reservations(cls):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM reservations AS r INNER JOIN customers AS c ON r.customer_id = c.customer_id ORDER BY reservation_date DESC;"
               cur.execute(sql)
               reservations = cur.fetchall()
               return reservations
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)