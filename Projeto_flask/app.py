from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from database import init_db

app = Flask(__name__)

# Inicializa o banco de dados
init_db()

def get_db_connection():
    conn = sqlite3.connect('coxinharia.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    
    # Buscar vendas e total vendido
    vendas = conn.execute('SELECT * FROM vendas ORDER BY id DESC').fetchall()
    total_vendas = conn.execute('SELECT SUM(valor) FROM vendas').fetchone()[0] or 0.0
    
    # Buscar compras e total gasto
    compras = conn.execute('SELECT * FROM compras ORDER BY id DESC').fetchall()
    total_compras = conn.execute('SELECT SUM(valor_pago) FROM compras').fetchone()[0] or 0.0
    
    # Calcular Lucro/Saldo
    lucro = total_vendas - total_compras
    
    conn.close()
    
    return render_template(
        'index.html', 
        vendas=vendas, 
        compras=compras, 
        total_vendas=total_vendas, 
        total_compras=total_compras, 
        lucro=lucro
    )

@app.route('/nova_venda', methods=['POST'])
def nova_venda():
    cliente = request.form['cliente']
    quantidade = request.form['quantidade']
    sabores = request.form['sabores']
    valor = request.form['valor']
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO vendas (cliente, quantidade, sabores, valor) VALUES (?, ?, ?, ?)',
        (cliente, quantidade, sabores, valor)
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

@app.route('/nova_compra', methods=['POST'])
def nova_compra():
    item = request.form['item']
    quantidade = request.form['quantidade']
    unidade = request.form['unidade']
    valor_pago = request.form['valor_pago']
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO compras (item, quantidade, unidade, valor_pago) VALUES (?, ?, ?, ?)',
        (item, quantidade, unidade, valor_pago)
    )
    conn.commit()
    conn.close()
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)