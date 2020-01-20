from falcon.api import Api

app = Api()

@app.route('/home')
def home(req, resp):
    resp.text = "Hello from the HOME page"

@app.route('/about')
def about(req, resp):
    resp.text = "Hello from the ABOUT page"

@app.route('/greet/{name}')
def greet(req, resp, name):
    resp.text = f'Hello, {name}'

@app.route("/book")
class BooksHandler:

    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"

@app.route('/template/{title}/{name}')
def template_(req, resp, **kwargs):
    resp.body = app.template(
        'index.html',
        context=kwargs
    )
