import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os
from dotenv import load_dotenv
load_dotenv()

app= FastAPI(title="Blog Post Generator API", description="An API to generate blog posts based on a given topic.", version="1.0.0")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


## API endpoint to generate a blog post based on a given topic

@app.post("/blogs")
async def create_blog(request: Request):
      data = await request.json()
      topic = data.get("topic",)
      language = data.get("language")

      ## Initialize the LLM and GraphBuilder
      groqllm = GroqLLM()
      llm = groqllm.get_llm()
      graph_builder = GraphBuilder(llm)

      if topic and language:
            graph= graph_builder.setup_graph(usecase="language")
            state = graph.invoke({"topic": topic,"current_language":language})
      elif topic:
           graph= graph_builder.setup_graph(usecase="topic")
           state = graph.invoke({"topic": topic})
           
      return {"data":state}      

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

