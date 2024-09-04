from website import create_app, render_template, request, redirect, url_for
from website import db

app = create_app()
if __name__ == '__main__':
  app.run(debug=True)
