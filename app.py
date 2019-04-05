from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'movies'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

#routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM movies')
    data = cur.fetchall()
    return render_template('index.html', movies = data)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        year = request.form['year']
        print(title)
        print(genre)
        print(year)
        #prmite ejecutar consutlas de mysql
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO movies (title, genre, year) VALUES (%s, %s, %s)',
        (title, genre, year))
        mysql.connection.commit()
        flash('Movie Added Successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_movie(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM movies WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-movie.html', movie = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_movie(id):
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        genre = request.form['genre']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE movies
            SET title = %s,
                genre = %s,
                year = %s
            WHERE id = %s
        """, (title, genre, year, id))
        mysql.connection.commit()
        flash('Movie Updated Successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_movie(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM movies WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Movie Removed Successfully')
    return redirect(url_for('Index'))

#server
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
