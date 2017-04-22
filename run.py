from BusTrack import app

app.config.from_object('config')
app.config.from_pyfile('config.py')
#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
if __name__=='__main__':
    app.run(host='0.0.0.0')
