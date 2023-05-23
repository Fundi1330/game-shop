from app import app, db, User, Game


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Game': Game}
