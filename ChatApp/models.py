from flask import abort
import pymysql
from util.DB import DB


# 初期起動時にコネクションプールを作成し接続を確立
db_pool = DB.init_db_pool()


# 顧客クラス
class Customer:
   @classmethod
   def create(cls, uid, name, email, phone, gender, password):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO customers (customer_id, customer_name, email, phone, gender, password) VALUES (%s, %s, %s, %s, %s, %s);"
               cur.execute(sql, (uid, name, email, phone, gender, password,))
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
   def create(cls, uid, name, email, phone, gender, password):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO stylists (stylist_id, stylist_name, email, phone, gender, password) VALUES (%s, %s, %s, %s, %s, %s);"
               cur.execute(sql, (uid, name, email, phone, gender, password,))
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
#    @classmethod
#    def create(cls, uid, new_channel_name, new_channel_description):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = "INSERT INTO channels (uid, name, abstract) VALUES (%s, %s, %s);"
#                cur.execute(sql, (uid, new_channel_name, new_channel_description,))
#                conn.commit()
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)

   @classmethod
   def get_all_customers(cls):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM customers;"
               cur.execute(sql)
               channels_user = cur.fetchall()
               return channels_user
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)

   @classmethod
   def get_all_stylists(cls):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "SELECT * FROM stylists;"
               cur.execute(sql)
               channels_stylist = cur.fetchall()
               return channels_stylist
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


#    @classmethod
#    def find_by_cid(cls, cid):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = "SELECT * FROM channels WHERE id=%s;"
#                cur.execute(sql, (cid,))
#                channel = cur.fetchone()
#                return channel
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)


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
   def create(cls, uid, cid, message):
       conn = db_pool.get_conn()
       try:
           with conn.cursor() as cur:
               sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
               cur.execute(sql, (uid, cid, message,))
               conn.commit()
       except pymysql.Error as e:
           print(f'エラーが発生しています：{e}')
           abort(500)
       finally:
           db_pool.release(conn)


#    @classmethod
#    def get_all(cls, cid):
#        conn = db_pool.get_conn()
#        try:
#            with conn.cursor() as cur:
#                sql = """
#                    SELECT id, u.uid, user_name, message 
#                    FROM messages AS m 
#                    INNER JOIN users AS u ON m.uid = u.uid 
#                    WHERE cid = %s 
#                    ORDER BY id ASC;
#                """
#                cur.execute(sql, (cid,))
#                messages = cur.fetchall()
#                return messages
#        except pymysql.Error as e:
#            print(f'エラーが発生しています：{e}')
#            abort(500)
#        finally:
#            db_pool.release(conn)


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