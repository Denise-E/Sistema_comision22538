from flask import Flask;
from flask import render_template, request, redirect, send_from_directory, url_for;
from flaskext.mysql import MySQL;
from datetime import datetime;
import os;

app = Flask(__name__);

mysql = MySQL() 
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 
app.config['MYSQL_DATABASE_USER'] = 'root' 
app.config['MYSQL_DATABASE_PASSWORD'] = '' 
app.config['MYSQL_DATABASE_DB'] = 'sistema22538' 
mysql.init_app(app)

CARPETA = os.path.join("uploads")
app.config["CARPETA"] = CARPETA;

@app.route("/uploads/<nombreImg>")
def uploads(nombreImg):
    return send_from_directory(app.config["CARPETA"], nombreImg)


@app.route('/')
def main():
    sql = "SELECT * FROM empleados"
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute(sql);
    empleados = cursor.fetchall();
    print(empleados);
    conn.commit();
    return render_template('empleados/index.html', empleados = empleados);

@app.route('/create')
def create():
    return render_template('empleados/create.html');

@app.route('/storage', methods=['POST'])
def storage():
    nombre = request.form['nombreValue']
    email = request.form['emailValue']
    imagen = request.files['fileValue']

    nuevoNombreImg = '';

    if imagen.filename != '':
        now = datetime.now();
        moment = now.strftime('%Y%M%S');
        nuevoNombreImg = moment + "-" + imagen.filename;
        imagen.save('uploads/'+nuevoNombreImg)

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `email`, `imagen`) VALUES (NULL, %s, %s, %s);"
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute(sql,(nombre,email,nuevoNombreImg));
    #print(imagen)
    conn.commit();

    return redirect('/')
    #return render_template("empleados/index.html")

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect();
    cursor = conn.cursor();

    cursor.execute("SELECT imagen FROM empleados WHERE id=%s", id)
    imagen = cursor.fetchall();
    os.remove(os.path.join(app.config["CARPETA"], imagen[0][0]))

    sql = "DELETE FROM empleados WHERE id=%s";
    cursor.execute(sql,id)
    conn.commit();
    return redirect('/');

@app.route("/edit/<int:id>")
def edit(id):
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute("SELECT * FROM empleados WHERE id=%s", id)
    empleado = cursor.fetchall()
    conn.commit();
    return render_template("empleados/edit.html", empleado = empleado)

@app.route("/modify", methods=["POST"])
def modify():
    nombre = request.form['nombreValue']
    email = request.form['emailValue']
    imagen = request.files['fileValue']
    id = request.form["idValue"]

    conn = mysql.connect();
    cursor = conn.cursor();

    nuevoNombreImg = '';

    if imagen.filename != '':
        now = datetime.now();
        moment = now.strftime('%Y%M%S');
        nuevoNombreImg = moment + "-" + imagen.filename;
        imagen.save('uploads/'+nuevoNombreImg)

        cursor.execute("SELECT imagen FROM empleados WHERE id=%s", id)
        imagen = cursor.fetchall();
        os.remove(os.path.join(app.config["CARPETA"], imagen[0][0]))

        cursor.execute("UPDATE empleados SET imagen=%s WHERE id=%s",(nuevoNombreImg,id))
        conn.commit();

    sql = "UPDATE empleados SET nombre=%s, email=%s WHERE id=%s"
    
    cursor.execute(sql,(nombre,email,id));
    conn.commit();

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True);