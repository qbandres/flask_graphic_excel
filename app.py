from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

app.secret_key = '20011074'  # Cambia esto por una clave secreta segura

# Simula una base de datos de usuarios
usuarios = {
    'andres': '1234',
    'alonso': '4321',
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in usuarios and usuarios[username] == password:
        # Autenticación exitosa, guarda el nombre de usuario en la sesión
        session['username'] = username
        return redirect(url_for('main'))
    else:
        # Autenticación fallida, puedes mostrar un mensaje de error
        return render_template('index.html', error='Credenciales incorrectas')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' in session:
        global df_upload, html_table
        html_table = None

        if request.method == 'POST':
            file = request.files['file']
            if file and file.filename.endswith('.xlsx'):
                df = pd.read_excel(file)
                df_upload = df
                html_table = df.to_html(classes='table table-bordered table-striped', index=False)

        return render_template('main.html', html_table=html_table, img_base64=None)
    else:
        return redirect(url_for('index'))

@app.route('/graphics')
def graphics():
    global df_upload

    group_table = df_upload[['Especialidad', 'Cant']].groupby(['Especialidad']).sum()
    tgroup = group_table.transpose()
    ax = tgroup.plot(kind='bar', stacked=False)

    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

    plt.title('Distribución de Personal')

    # Guarda el gráfico como una imagen en memoria
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convierte la imagen en una cadena base64
    img_base64 = base64.b64encode(img.read()).decode('utf-8')

    plt.close()

    return render_template('main.html',html_table=html_table, img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
