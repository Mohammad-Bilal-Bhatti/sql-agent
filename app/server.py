from decouple import config
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from .sql_agent import create_agent

app = FastAPI()

# Establish connection with your database
db = SQLDatabase.from_uri(config("DB_URL"))

# Create Modal
llm = init_chat_model("gpt-4o-mini", model_provider="openai", api_key=config("OPEN_API_KEY"))

agent = create_agent(llm, db)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, agent, path="/agent")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
