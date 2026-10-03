from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from priority_queue import PriorityQueue
from database import create_tables, get_connection
from priority import get_priority


app = FastAPI(
    title="WhitePriorix",
    description="Dynamic Priority-Based Service Queue Management System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

queue = PriorityQueue()

# Create database tables
create_tables()


# Load waiting requests from database into Max Heap
def load_waiting_requests():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, student_name, problem, request_type, priority
        FROM requests
        WHERE status = 'waiting'
    """)

    requests = cursor.fetchall()
    connection.close()

    for request in requests:
        queue.add_request(dict(request))


# Load saved requests when server starts
load_waiting_requests()


@app.get("/")
def home():
    return {
        "project": "WhitePriorix",
        "message": "WhitePriorix backend is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "OK"
    }


@app.post("/requests")
def add_request(
    student_name: str,
    problem: str,
    request_type: str
):
    # Automatically determine priority
    priority = get_priority(request_type)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO requests
        (student_name, problem, request_type, priority)
        VALUES (?, ?, ?, ?)
        """,
        (student_name, problem, request_type, priority)
    )

    request_id = cursor.lastrowid

    connection.commit()
    connection.close()

    request = {
        "id": request_id,
        "student_name": student_name,
        "problem": problem,
        "request_type": request_type,
        "priority": priority
    }

    # Add request to Max Heap
    queue.add_request(request)

    return {
        "message": "Request added successfully",
        "request": request
    }


@app.get("/queue")
def get_queue():
    return {
        "queue": queue.get_queue()
    }


@app.post("/serve-next")
def serve_next():
    request = queue.serve_next()

    if request is None:
        return {
            "message": "Queue is empty"
        }

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE requests
        SET status = 'completed'
        WHERE id = ?
        """,
        (request["id"],)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Request served successfully",
        "served_request": request
    }