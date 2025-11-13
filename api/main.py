from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import financials_route
from api.routes import advanced_analytics


app = FastAPI(

    title="Banking Health API",
    description="""
    API REST para consultar indicadores financieros del Sistema Bancario Ecuatoriano.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(

    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando"}

app.include_router(financials_route.router)
app.include_router(advanced_analytics.router)

if __name__ == "__main__":
    import uvicorn
    
    print("Inciando API")
    print("Documentación: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
