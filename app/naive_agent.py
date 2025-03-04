
from typing_extensions import TypedDict
from typing_extensions import Annotated
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph
from langchain import hub

query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def create_agent(llm, db):
    # Generate SQL query using LLM
  def write_query(state: State):
      """Generate SQL query to fetch information."""
      prompt = query_prompt_template.invoke(
          {
              "dialect": db.dialect,
              "top_k": 10,
              "table_info": db.get_table_info(),
              "input": state["question"],
          }
      )
      structured_llm = llm.with_structured_output(QueryOutput)
      result = structured_llm.invoke(prompt)
      return {"query": result["query"]}    

  # Execute query using Alchemy
  def execute_query(state: State):
      """Execute SQL query."""
      execute_query_tool = QuerySQLDatabaseTool(db=db)
      return {"result": execute_query_tool.invoke(state["query"])}

  # Generate Answer based on query result and query question
  def generate_answer(state: State):
      """Answer question using retrieved information as context."""
      prompt = (
          "Given the following user question, corresponding SQL query, "
          "and SQL result, answer the user question.\n\n"
          f'Question: {state["question"]}\n'
          f'SQL Query: {state["query"]}\n'
          f'SQL Result: {state["result"]}'
      )
      response = llm.invoke(prompt)
      return {"answer": response.content}


  # Build Pipeline of predefined steps
  graph_builder = StateGraph(State).add_sequence(
      [write_query, execute_query, generate_answer]
  )

  graph_builder.add_edge(START, "write_query")
  naive_sql_agent = graph_builder.compile()

  return naive_sql_agent