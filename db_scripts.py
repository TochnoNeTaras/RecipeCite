import sqlite3

class DBManager():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = None
        self.cursor = None
    
    def open_db(self):
        self.conn = sqlite3.connect(self.dbname) #створюємо з'єднання з базою даних
        self.cursor = self.conn.cursor() # створили вказівник на базу даних

    def get_categories(self):
        self.open_db()
        self.cursor.execute('''SELECT * FROM categories''') # виконуємо SQL-запит
        data = self.cursor.fetchall() # отримуємо відповідь і зберігаємо у змінну data
        self.conn.close() # закриваємо базу даних
        return data # повертаємо результат з бази даних
    
    def get_articles(self):
        self.open_db()
        self.cursor.execute('''SELECT * FROM articles''')
        data = self.cursor.fetchall()
        self.conn.close()
        return data
    
    def get_articles_by_category(self, category_id):
        self.open_db()
        self.cursor.execute('''SELECT * FROM articles WHERE category_id=?''', [category_id])
        data = self.cursor.fetchall()
        self.conn.close()
        return data
    
    def get_article_by_id(self, article_id):
        self.open_db()
        self.cursor.execute('''SELECT * FROM articles WHERE id=?''', [article_id])
        data = self.cursor.fetchone()
        self.conn.close()
        return data
    
    def create_article(self, title,  description, text, image, author_id, category_id):
        self.open_db()
        self.cursor.execute('''INSERT INTO articles(title,  description, text, image, author_id, category_id) 
                            VALUES(?,?,?,?,?,?)''', [title,  description, text, image, author_id, category_id])
        self.conn.commit()
        self.conn.close()
        
    def search_articles(self, query):
        self.open_db()
        query = '%' + query + '%'
        self.cursor.execute('''SELECT * FROM articles WHERE (title LIKE ? OR description LIKE ?)''', [query, query])
        data = self.cursor.fetchall()   
        self.conn.close()
        return data


    

