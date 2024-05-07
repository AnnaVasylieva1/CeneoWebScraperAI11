from app import app 
from flask import render_template, request, url_for, redirect
import requests
from bs4 import BeautifulSoup
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/extract', methods=['GET', 'POST'])
def extract():        
    if request.method == "POST":
        product_id = request.form.get('product_id')
        url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
        response = requests.get(url)
        if response.status_code == requests.codes['ok']:
            page_dom = BeautifulSoup(response.text, "html.parser")
            try:
                opinions_count = page_dom.select_one('a.product-review__link > span').get_text().strip()
            except AttributeError:
                opinions_count = 0
            if opinions_count:
                return redirect(url_for('product', product_id=product_id))
            return render_template("extract.html", error = "Product has no opinions")
        render_template("extract.html", error = "Poduct does not exist")
    return render_template("extract.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product.html", product_id=product_id)

