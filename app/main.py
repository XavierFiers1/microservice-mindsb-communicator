import pymysql
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.payload import Info, PayLoad
from services.database_service import DatabaseService
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

database_service = DatabaseService()

app = FastAPI()
limiter = Limiter(key_func=get_remote_address, default_limits=["1/minute"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)


@app.get("/")
def index() -> str:
    return "mindsdb communicator"


@app.post("/collect_info")
def collect_info(req: PayLoad) -> Info:
    load_dotenv()
    database_service.open_database_connection()
    try:
        if req.author is not None:
            cursor = database_service.database.cursor()
            cursor.execute(
                f'''SELECT response from mindsdb.{req.db_model} WHERE text="{req.text}" AND author="{req.author}"'''
            )

        text = ""
        results = cursor.fetchall()
        for row in results:
            text += row[0]
        return {"info": text}

    except pymysql.Error as e:
        print(f"error executing query: {e}")
    finally:
        cursor.close()
        database_service.close()
