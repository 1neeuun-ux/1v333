import sqlite3
import os

path = os.path.join(os.getcwd() ,"v3","data","db.db")

db_path = path
DB = None
cursor = None


def db_deck(funk):
    def open_close(*args, **kwargs):
        db_open()
        data = funk(*args, **kwargs)
        db_close()
        return data
    return open_close

def db_open():
    global DB,cursor
    DB = sqlite3.connect(db_path)
    cursor = DB.cursor()
    
def db_close():
    DB.commit()
    cursor.close()
    DB.close()


@db_deck
def db_create():
    cursor.execute("""PRAGMA foreign_key=on """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS  category(
                   id INTEGER PRIMARY KEY,
                   title VARCHAR(50) 
    ) """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS  tag(
                   id INTEGER PRIMARY KEY,
                   title VARCHAR(150)    
                    ) """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS  user(
               id INTEGER PRIMARY KEY,
               email VARCHAR(250),    
               hash_password VARCHAR(500),
               sale VARCHAR(500)
                ) """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS  discussion_topic(
                   id INTEGER PRIMARY KEY,
                   id_category INTEGER,
                   id_user INTEGER,
                   title VARCHAR(150),
                   text VARCHAR,
                   FOREIGN KEY (id_category) REFERENCES category(id),
                   FOREIGN KEY (id_user) REFERENCES user (id)
                    ) """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS  talk_topic_tag(
                   id INTEGER PRIMARY KEY,
                   id_discussion_topic INTEGER,
                   id_tag INTEGER,
                   FOREIGN KEY (id_discussion_topic) REFERENCES discussion_topic(id),
                   FOREIGN KEY (id_tag) REFERENCES tag (id)
                    ) """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS comment(
                   id INTEGER PRIMARY KEY,
                   id_user INTEGER,
                   id_discussion_topic INTEGER,
                   text VARCHAR,
                   date DATETIME,
                   FOREIGN KEY (id_user) REFERENCES user(id)
                    ) """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS category_reply(
                   id INTEGER PRIMARY KEY,
                   id_comment INTEGER,
                   id_user INTEGER,
                   text VARCHAR,
                   date DATETIME,
                   FOREIGN KEY (id_comment) REFERENCES comment(id),
                   FOREIGN KEY (id_user) REFERENCES user(id)
                    ) """)


@db_deck
def db_delete():
    cursor.execute("""DROP TABLE IF EXISTS category""")
    cursor.execute("""DROP TABLE IF EXISTS comment""")
    cursor.execute("""DROP TABLE IF EXISTS  talk_topic_tag""")
    cursor.execute("""DROP TABLE IF EXISTS  discussion_topic""")
    cursor.execute("""DROP TABLE IF EXISTS  user""")
    cursor.execute("""DROP TABLE IF EXISTS tag""")
    cursor.execute("""DROP TABLE IF EXISTS  category""")
    
    
@db_deck    
def add_category(title:str):
    try:
        title = title.strip()
        if title == "" and check_category(title):
            return False
        
        cursor.execute("""INSERT INTO category(title)
                        VALUES (?)""",(title,))

        id_category = cursor.lastrowid
        return id_category
    
    except:
        return False


@db_deck
def update_category(id_category:int, title:str):
    try:
        title = title.strip()
        if title == "" and id_category <= 0:
            return False
        
        cursor.execute("""UPDATE category
                        SET title = ?
                        WHERE id = ?
                """, (title, id_category))

        
        return True
    except:
        return False
        
        
@db_deck
def del_category(id_category: int):
    try:
        cursor.execute("""DELETE FROM category 
                       WHERE id = ?,
                       """, (id_category,))
        return True
    except:
        return False

    
@db_deck 
def check_category(title:str):
    try:
        title = title.strip()
        if title == "":
            return False
        cursor.execute("""SELECT * FROM category
                       WHERE title = ?
                       ORDER BY id
                       """, (title,))
        data = cursor.fetchall()
        return (not data is None and len(data) != 0)
    
    except:
        return False
    
    
@db_deck
def get_category(id_category: int):
    try:
        cursor.execute("""SELECT * FROM category 
                       WHERE id = ?
                       """, (id_category,))
        data = cursor.fetchone()
        return data
    except:
        return None


@db_deck 
def get_all_category(): 
    try:
        cursor.execute("""SELECT * FROM category
                        ORDER BY id
                       """)
        return cursor.fetchall()
    except:
        return False
    


# ====================  user  =================================
import os
import binascii
import hashlib
import re

def is_valid_email(email):
    "asdf@asdf.asdf"
    regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\/[a-zA-Z]{2,}"
    return re.match(regex, email) is not None

def hash_pass(password:str,salt:str):
    password_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    
    combined_bytes = salt_bytes + password_bytes
    
    hash_pwd = hashlib.sha256(combined_bytes).hexdigest()
    return hash_pwd

@db_deck
def registration_user(email:str, password:str, password2:str):
    password = password.strip()
    if is_valid_email(email) or password != password2 or check_user(email):
        return False
    
    salt = binascii.hexlify(os.urandom(16)).decode("utf-8")
    
    hash_password = hash_pass(password,salt)
    
    cursor.execute("""INSERT INTO user(email, hash_password, sale)
                   VALUES (?,?,?)""", (email, hash_password,salt,))
    id_user = cursor.lastrowid
    return id_user

@db_deck
def login_user(email:str,password:str):
    password = password.split()
    if is_valid_email(email) or password != "" or not check_user(email):
        return False

    cursor.execute("""SELECT id,hash_password,sale FROM user
                   WHERE email = ? """, (email,))
    id_user,hash_password,sale = cursor.fetchone()
    
    if hash_password == hash_pass(password, sale):
        return id_user
    return False


def _user():
    pass
def _user():
    pass

def check_user(email:str):
    try:
        email = email.strip()
        if email == "":
            return False
        
        cursor.execute("""SELECT email FROM user
                       WHERE email = ? """, (email,))
        data = cursor.fetchone()
        return (data is not None and len(data) != 0)
    except:
        return False

    
    

# ====================_discussion_topic==================
@db_deck
def add_discussion_topic(id_category: int, id_user: int, title: str, text: str):
    try:
        title = title.strip()
        text = text.strip()
        if title == "" or text == "" or id_category <= 0 or id_user <= 0:
            return False
        
        cursor.execute("""INSERT INTO discussion_topic (id_category, id_user, title, text)
                          VALUES (?, ?, ?, ?)""",
                       (id_category, id_user, title, text))
        return cursor.lastrowid
    except:
        return False

@db_deck
def update_discussion_topic(id_discussion: int, id_category: int, id_user: int, title: str, text: str):
    try:
        title = title.strip()
        text = text.strip()
        if id_discussion <= 0 or id_category <= 0 or id_user <= 0 or title == "" or text == "":
            return False
        
        cursor.execute("""UPDATE discussion_topic
                          SET id_category = ?, id_user = ?, title = ?, text = ?
                          WHERE id = ?""",
                       (id_category, id_user, title, text, id_discussion))
        return True
    except:
        return False
    
@db_deck
def del_discussion_topic(id_discussion: int):
    try:
        cursor.execute("""DELETE FROM discussion_topic WHERE id = ?""", (id_discussion,))
        return True
    except:
        return False

@db_deck
def get_all_category_or_discussion_topic(pages:int = 1, limit:int = 16 ,id_category: int = None):
    """
    discussion_topic.id, discussion_topic.title, user.id, user.email
    LIMIT (Сколько)+1 OFFSET (c какого);
    """
    try:
        if id_category is not None:
            cursor.execute("""SELECT discussion_topic.id, discussion_topic.title,
                                    user.id, user.email
                                FROM discussion_topic, user
                                WHERE discussion_topic.id_user = user.id 
                                AND id_category = ?
                                ORDER BY discussion_topic.id DESC
                                LIMIT ? OFFSET ?
                        """, (id_category, limit + 1 , (pages - 1) * limit))
            data = cursor.fetchall()
        else:
            cursor.execute("""SELECT discussion_topic.id, discussion_topic.title,
                                    user.id, user.email
                                FROM discussion_topic, user
                                WHERE discussion_topic.id_user = user.id
                                ORDER BY discussion_topic.id DESC
                                LIMIT ? OFFSET ?
                        """, (limit + 1 , (pages - 1) * limit))
            data = cursor.fetchall()

        j = {"discussion_topic_list":[]}
        for item in data:
            j["discussion_topic_list"].append({
                "id":item[0],
                "title":item[1],
                "id_user":item[2],
                "email_user":item[3]
            })
        return data

        
    except Exception as error:
        print("error get_all_discussion_topic:", error)
    return False



@db_deck
def get_discussion_topic(id_discussion_topic:int):
    try:
        if id_discussion_topic is not None:
            cursor.execute("""SELECT * FROM discussion_topic
                              WHERE id_discussion_topic = ?
                           """, (id_discussion_topic,))
            return cursor.fetchone()
        return False
    except Exception as error:
        print("error get_discussion_topic:", error)
    return False




# ==================== comment ===================       
@db_deck
def add_comment_(id_discussion: int, id_user: int, text: str, date: str):
    try:
        text = text.strip()
        if text == "":
            return False
        
        cursor.execute("""INSERT INTO comment(id_discussion, id_user, text, date)
                          VALUES (?, ?, ?, ?)""",
                       (id_discussion, id_user, text, date))
        return cursor.lastrowid
    except:
        return False



@db_deck
def update_comment(id_comment: int, text: str):
    try:
        text = text.strip()
        if id_comment <= 0 or text == "":
            return False
        
        cursor.execute("""UPDATE comment
                          SET text = ?
                          WHERE id_comment = ?""",
                       (text, id_comment))
        return cursor.lastrowid
    except:
        return False
    
    
@db_deck
def del_comment(id_comment: int):
    try:
        if id_comment <= 0:
            return False
        
        cursor.execute("""DELETE FROM comment
                          WHERE id_comment = ?""", (id_comment,))
        return cursor.lastrowid
    except:
        return False
    

@db_deck
def get_all_(id_discussion: int):
    try:
        if id_discussion <= 0:
            return False
        
        cursor.execute("""SELECT * FROM comment
                          WHERE id_discussion = ?
                          ORDER BY id_comment DESC""", (id_discussion,))
        return cursor.fetchall()
    except:
        return False




# ==================== add_category_reply ===================       
@db_deck
def add_category_reply(id_comment: int, id_user: int, text: str, date: str):
    try:
        text = text.strip()
        if text == "" or id_comment <= 0 or id_user <= 0 or date.strip() == "":
            return False
        
        cursor.execute("""INSERT INTO category_reply(id_comment, id_user, text, date)
                          VALUES (?, ?, ?, ?)""", 
                          (id_comment, id_user, text, date))
        
        id_reply = cursor.lastrowid
        
        return id_reply
    except:
        return False


@db_deck
def del_category_reply(id_reply: int):
    try:
        if id_reply is not None and id_reply > 0:
            cursor.execute("""DELETE FROM category_reply
                              WHERE id_reply = ?""", (id_reply,))
        return False
    except Exception as error:
        print("error del_category_reply:", error)
    return False





# ==================== add_tag ===================        
@db_deck
def add_tag(title: str):
    try:
        title = title.strip()
        if title == "":
            return False
        
        cursor.execute("""INSERT INTO tag(title) 
                       VALUES (?)""", (title,))
        
        id_tag = cursor.lastrowid
        return id_tag
    except:
        return False


@db_deck
def del_tag(id_tag: int):
    try:
        if id_tag <= 0:
            return False

        cursor.execute("""DELETE FROM tag 
                          WHERE id_tag = ?""", (id_tag,))
    except Exception as error:
        print("error del_tag:", error)
        return False





# ====================  add_talk_topic_tag  ===================
@db_deck
def add_talk_topic_tag(id_discussion_topic: int, id_tag: int):
    try:
        if id_discussion_topic <= 0 or id_tag <= 0:
            return False
        
        cursor.execute("""INSERT INTO talk_topic_tag(id_discussion_topic, id_tag)
                          VALUES (?, ?)""", 
                          (id_discussion_topic, id_tag))
        
        id_link = cursor.lastrowid
        return id_link
    except:
        return False


@db_deck
def del_discussion_topic(id_category: int = None):
    try:
        if id_category is not None:
            cursor.execute("""DELETE FROM discussion_topic
                              WHERE id_category = ?""", (id_category,))
        else:
            cursor.execute("""DELETE FROM discussion_topic""")
    except Exception as error:
        print("error del_discussion_topic:", error)
        return False


    
    
if __name__ == "__main__":
    db_delete()
    db_create()
    
    print(registration_user("email@mail.com", "password", "password"))

    add_tag("tag1")
    add_tag("tag2")
    add_tag("tag3")
    add_category("category1")
    add_category("category2")
    add_category("category3")

    add_discussion_topic(1, 1, "Title1", "TEXT_TEXT_TEXT_TEXT_TEXT_TEXT_TEXT1")
    add_discussion_topic(2, 1, "Title2", "TEXT_TEXT_TEXT_TEXT_TEXT_TEXT_TEXT2")
    add_discussion_topic(2, 1, "Title3", "TEXT_TEXT_TEXT_TEXT_TEXT_TEXT_TEXT3")
    add_discussion_topic(3, 1, "Title4", "TEXT_TEXT_TEXT_TEXT_TEXT_TEXT_TEXT4")
    add_discussion_topic(3, 1, "Title5", "TEXT_TEXT_TEXT_TEXT_TEXT_TEXT_TEXT5")
    add_discussion_topic(3, 1, "Title6", "TEXT_TEXT_TEXT_TEXT_TEXT_TEXT_TEXT6")

    add_talk_topic_tag(1, 3)
    add_talk_topic_tag(2, 2)
    add_talk_topic_tag(3, 2)
    add_talk_topic_tag(4, 1)
    add_talk_topic_tag(5, 1)
    add_talk_topic_tag(6, 1)

    print("+")


    #print( add_category("1"))
    #print( check_category("1"))
    #print( get_category(1))
    #print( update_category(1,"2"))
    #print( del_category(1))
    
    # salt = binascii.hexlify(os.urandom(16)).decode("utf-8")
    # print(salt)
 
 