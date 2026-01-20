from fastapi import FastAPI

app = FastAPI()

# Endpoint test cơ bản
@app.get("/")
def read_root():
    return {"message": "Hello, backend is running!"}

# Endpoint test database (nếu muốn)
# @app.get("/test-db")
# def test_db():
#     return {"status": "DB connection OK (giả lập)"}
