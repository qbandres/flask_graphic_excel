# Se configuro para deploy render rev2

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global df_upload
    html_table = None

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
            df_upload = df
            html_table = df.to_html(classes='table table-bordered table-striped', index=False)
    
    return render_template('index.html', html_table=html_table)

@app.route('/graphics')
def graphics():

    # pivot_table = df_upload.pivot(index='item', columns='Especialidad', values='Cant')
    group_table = df_upload[['Especialidad','Cant']].groupby(['Especialidad']).sum()
    tgroup = group_table.transpose()
    ax = tgroup.plot(kind='bar', stacked = False)
    # Agregar etiquetas de cantidad a las barras importante
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom')

    plt.title('Distribución de Personal')
    # plt.xlabel('Cargo')
    # plt.ylabel('Cant.')

    plt.show()
    plt.close()

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)


