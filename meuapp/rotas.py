from flask import render_template
from flask import request
import pandas as pd
import io
from meuapp import app

@app.route('/')
def home():
    return "Hello, World!"



@app.route('/compare', methods=['POST'])
def compare():
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Lê os arquivos CSV
    df1 = pd.read_csv(io.StringIO(file1.stream.read().decode("UTF8")), sep=',')
    df2 = pd.read_csv(io.StringIO(file2.stream.read().decode("UTF8")), sep=',')

    # Realiza a mesclagem
    comparacao = df1.merge(df2, indicator=True, how='outer')

    # Seleciona apenas as linhas que não têm correspondência em ambos os DataFrames
    diferencas = comparacao[comparacao['_merge'] != 'both']

    # Retorna as diferenças como uma resposta JSON
    return diferencas.to_json(orient='records')

@app.route('/upload')
def upload_file():
   return render_template('compare.html')