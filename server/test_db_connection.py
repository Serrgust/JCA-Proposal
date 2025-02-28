from app import create_app, db

app = create_app()

with app.app_context():
    try:
        result = db.session.execute("SELECT 1")  # Correct way in SQLAlchemy 2.0
        print("✅ Successfully connected to the MySQL database!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
