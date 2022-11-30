from flask import Flask;
from flask import render_template;
from flaskext.mysql import MySQL;

app = Flask(__name__);

mysql = MySQL() 
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = '' 
app.config['MYSQL_DATABASE_DB'] = 'sistema22538' 
mysql.init_app(app)


@app.route('/')
def main():
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `email`, `imagen`) VALUES (NULL, 'Sofia', 'sofi@gmail.com', 'sofia.png');"
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute(sql);
    conn.commit();
    return render_template('empleados/index.html');

if __name__ == '__main__':
    app.run(debug=True);