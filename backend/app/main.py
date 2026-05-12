# @trace TASK-005
# @trace TASK-007
# @trace TASK-011
# @trace TASK-014
from fastapi import FastAPI
from app.routers import auth, admin, campaigns
from app.database import SessionLocal, engine
from app import models, crud, schemas
from contextlib import asynccontextmanager
import logging

# Ensure tables are created (useful if running without migrations temporarily)
models.Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Seed initial admin user if not exists
    db = SessionLocal()
    try:
        admin_user = crud.get_user_by_username(db, username="admin")
        if not admin_user:
            logger.info("Seeding initial admin user...")
            new_admin = schemas.UserCreate(
                username="admin",
                email="admin@example.com",
                password="admin"
            )
            crud.create_user(db, new_admin, role="Admin")
            logger.info("Admin user created (username: admin, password: admin).")
    except Exception as e:
        logger.error(f"Error seeding admin user: {e}")
    finally:
        db.close()
    yield
    # Shutdown

app = FastAPI(title="Pathcamp Backend", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(campaigns.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Pathcamp API"}
