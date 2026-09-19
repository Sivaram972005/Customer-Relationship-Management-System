from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from db import fetch_all,fetch_one,execute,get_connection
from config import SECRET_KEY
app=Flask(__name__); app.secret_key=SECRET_KEY

@app.route('/')
def home():
 counts={t:fetch_one(f'SELECT COUNT(*) n FROM {t}')['n'] for t in ['customers','products','employees','orders','transactions']}
 return render_template('index.html',counts=counts)

@app.route('/customers')
def customers(): return render_template('customers.html',rows=fetch_all('SELECT * FROM customers ORDER BY customer_id DESC'))
@app.post('/customers/add')
def add_customer():
 try: execute('INSERT INTO customers(name,email,phone,address) VALUES(%s,%s,%s,%s)',(request.form['name'],request.form['email'],request.form.get('phone'),request.form.get('address'))); flash('Customer added successfully.')
 except Exception as e: flash('Error: '+str(e))
 return redirect(url_for('customers'))

@app.route('/products')
def products(): return render_template('products.html',rows=fetch_all('SELECT * FROM products ORDER BY product_id DESC'))
@app.post('/products/add')
def add_product():
 try: execute('INSERT INTO products(product_name,price,stock) VALUES(%s,%s,%s)',(request.form['product_name'],request.form['price'],request.form['stock'])); flash('Product added successfully.')
 except Exception as e: flash('Error: '+str(e))
 return redirect(url_for('products'))

@app.route('/employees')
def employees(): return render_template('employees.html',rows=fetch_all('SELECT * FROM employees ORDER BY employee_id DESC'))
@app.post('/employees/add')
def add_employee():
 try: execute('INSERT INTO employees(employee_name,department) VALUES(%s,%s)',(request.form['employee_name'],request.form['department'])); flash('Employee added successfully.')
 except Exception as e: flash('Error: '+str(e))
 return redirect(url_for('employees'))

@app.route('/orders')
def orders():
 rows=fetch_all('SELECT o.order_id,c.name customer_name,e.employee_name,o.order_date,o.total_amount FROM orders o JOIN customers c ON o.customer_id=c.customer_id LEFT JOIN employees e ON o.employee_id=e.employee_id ORDER BY o.order_id DESC')
 return render_template('orders.html',rows=rows)
@app.route('/transactions')
def transactions():
 rows=fetch_all('SELECT t.transaction_id,t.order_id,c.name customer_name,t.amount,t.payment_status,t.transaction_date FROM transactions t JOIN orders o ON t.order_id=o.order_id JOIN customers c ON o.customer_id=c.customer_id ORDER BY t.transaction_id DESC')
 return render_template('transactions.html',rows=rows)

@app.get('/api/customers')
def api_customers(): return jsonify(fetch_all('SELECT * FROM customers'))
@app.post('/api/customers')
def api_create_customer():
 d=request.get_json() or {}
 if not d.get('name') or not d.get('email'): return jsonify(error='name and email are required'),400
 try:
  cid=execute('INSERT INTO customers(name,email,phone,address) VALUES(%s,%s,%s,%s)',(d['name'],d['email'],d.get('phone'),d.get('address')))
  return jsonify(message='created',customer_id=cid),201
 except Exception as e: return jsonify(error=str(e)),400
@app.put('/api/customers/<int:cid>')
def api_update_customer(cid):
 d=request.get_json() or {}
 try:
  execute('UPDATE customers SET name=%s,email=%s,phone=%s,address=%s WHERE customer_id=%s',(d['name'],d['email'],d.get('phone'),d.get('address'),cid)); return jsonify(message='updated')
 except Exception as e: return jsonify(error=str(e)),400
@app.delete('/api/customers/<int:cid>')
def api_delete_customer(cid):
 try: execute('DELETE FROM customers WHERE customer_id=%s',(cid,)); return jsonify(message='deleted')
 except Exception as e: return jsonify(error=str(e)),400
@app.get('/api/customers/<int:cid>/orders')
def api_customer_orders(cid):
 con=get_connection(); cur=con.cursor(dictionary=True)
 try:
  cur.callproc('GetCustomerOrders',(cid,)); out=[]
  for r in cur.stored_results(): out.extend(r.fetchall())
  return jsonify(out)
 finally: cur.close(); con.close()
@app.get('/api/customer-orders-view')
def api_view(): return jsonify(fetch_all('SELECT * FROM customer_orders'))

if __name__=='__main__': app.run(debug=True)
