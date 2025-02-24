from app import app, db

with app.app_context():
    try: 
        #drop all tables

        db.drop_all()
        print("database dropped succesfully")

        #create all tables
        db.create_all()
        print("database initialised succesfully")
    except Exception as e:
        print(f"error initialising database: {e}")
