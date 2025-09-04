from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  

from app.routes.user import router as user_router
from app.routes.pets import router as pets_router
from app.routes.appointments import router as appointments_router
from app.routes.messages import router as messages_router
from app.routes.medical import router as medical_router
from app.routes.store import router as store_router
from app.routes.reviews import router as reviews_router
from app.routes.schedules import router as schedules_router
from app.routes.services import router as services_router



app = FastAPI(
    title="Panel Administrativo de la Clínica",
    description="Gestión de ventas, ganancias, horarios de doctores y más.",
    version="1.0.0"
)


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(pets_router, prefix="/pets", tags=["pets"])
app.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
app.include_router(messages_router, prefix="/messages", tags=["messages"])
app.include_router(medical_router, prefix="/medical", tags=["medical"])
app.include_router(store_router, prefix="/store", tags=["store"])
app.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
app.include_router(schedules_router, prefix="/schedules", tags=["schedules"])
app.include_router(services_router, prefix="/services", tags=["services"])


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
