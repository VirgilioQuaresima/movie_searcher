from flask import Flask, render_template, request, redirect, url_for
from tmdb_API import search_all, get_providers
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        q = request.form["query"]
        return redirect(url_for('searches', query=q))
    return render_template('home.html')


@app.route("/search/<query>")
def searches(query):
    lista = search_all(query)
    return render_template('search.html', lista=lista)


@app.route("/providers/<type>/<id>")
def providers(id, type):
    lista = get_providers(id, type)
    return render_template('providers.html', lista=lista)
