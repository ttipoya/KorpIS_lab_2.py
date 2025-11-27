import logging, time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from app import models
from app.routers import (clubs, arenas, rooms, pcspecs, stations, players, memberships,
    sessions, tournaments, matches, staff, bookings, configkv, pricekv)
from sqlalchemy.orm import Session

# Logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.FileHandler('api.log'), logging.StreamHandler()])
logger = logging.getLogger('colizeum')

app = FastAPI(title='Colizeum API', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)
    logger.info('Database tables ensured')

@app.middleware('http')
async def log_requests(request: Request, call_next):
    start = time.time()
    response = Response('Internal server error', status_code=500)
    try:
        response = await call_next(request)
        return response
    finally:
        duration_ms = int((time.time() - start) * 1000)
        status_code = getattr(response, 'status_code', 500)
        logger.info(f"{request.method} {request.url.path} {status_code} {duration_ms}ms")
        # persist to DB (best-effort, non-blocking)
        try:
            db = next(get_db())
            log = models.RequestLog(method=request.method, path=request.url.path, status_code=status_code, duration_ms=duration_ms, client_host=request.client.host if request.client else None)
            db.add(log)
            db.commit()
        except Exception as e:
            logger.exception('Failed to write RequestLog')

# include routers
app.include_router(clubs.router)
app.include_router(arenas.router)
app.include_router(rooms.router)
app.include_router(pcspecs.router)
app.include_router(stations.router)
app.include_router(players.router)
app.include_router(memberships.router)
app.include_router(sessions.router)
app.include_router(tournaments.router)
app.include_router(matches.router)
app.include_router(staff.router)
app.include_router(bookings.router)
app.include_router(configkv.router)
app.include_router(pricekv.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
