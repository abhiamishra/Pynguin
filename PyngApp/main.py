from website import create_app 
#whenever you put init.py in a folder, it becomes a package

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

