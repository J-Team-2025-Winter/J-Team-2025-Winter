from flask import abort
import pymysql
from util.DB import DB


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

# 美容師クラス
class Stylist:
   @classmethod
   def create(cls, stylist_id, name, email, phone, gender, password):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO stylists (stylist_id, stylist_name, email, phone, gender, password) VALUES (%s, %s, %s, %s, %s, %s);"
               cur.execute(sql, (stylist_id, name, email, phone, gender, password,))
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

   @classmethod
   def edit_profile(cls, uid, filename, comment):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "UPDATE stylists SET profile_picture_url=%s, comment=%s WHERE stylist_id=%s;"
               cur.execute(sql, (filename, comment, uid,))
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
    def get_all_customers(cls, uid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM customers AS c INNER JOIN customers_stylists AS cs ON c.customer_id = cs.customer_id WHERE stylist_id = (%s);"
               cur.execute(sql, (uid,))
               channels_user = cur.fetchall()
               return channels_user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

    @classmethod
    def get_all_stylists(cls, uid):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM stylists AS s INNER JOIN customers_stylists AS cs ON s.stylist_id = cs.stylist_id WHERE customer_id = (%s);"
               cur.execute(sql, (uid,))
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
                sql = "SELECT * FROM customers_stylists WHERE customers_stylists_id=%s;"
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
   def create(cls, message_id, content, image_url, sent_at, reservation_id, customers_stylists_id):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO Messages(message_id, content, image_url, sent_at, reservation_id, customers_stylists_id) VALUES(%s, %s, %s, %s, %s, %s);"
               cur.execute(sql, (message_id, content, image_url, sent_at, reservation_id, customers_stylists_id,))
               conn.commit()
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
               sql = "SELECT * FROM Messages WHERE customers_stylists_id = %s;" # [hiyo]「WHERE customers_stylists_id = %s」を追記
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