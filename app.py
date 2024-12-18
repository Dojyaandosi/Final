from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


# Connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname="dosya",  # Replace with your actual database name
        user="postgres",  # Replace with your database username
        password="doston",  # Replace with your password
        host="host.docker.internal",
        port="5432"
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the main index page."""
    return render_template("index.html")


@app.route("/timetable", methods=["GET"])
def timetable():
    """Render the timetable page filtered by level."""
    level = request.args.get("level")  # Get the selected level from the dropdown
    if not level:
        return "Level not provided", 400

    # Connect to the database and fetch data
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch courses based on the selected level
    query = """
        SELECT id, course_name, day, time_slot, room
        FROM timetable
        WHERE level = %s;
    """
    cur.execute(query, (level,))
    rows = cur.fetchall()

    # Close database connection
    cur.close()
    conn.close()

    # Prepare message for no data
    if not rows:
        message = f"No courses found for Level {level}."
    else:
        message = None

    # Render timetable.html with fetched data
    return render_template("timetable.html", level=level, data=rows, message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
