from langchain_community.agent_toolkits import create_sql_agent


def create_agent(llm, db):
  # This SQL Agent is capable to perform all DDL and DML operations (⚠️Note)
  sql_agent = create_sql_agent(llm, db=db, agent_type="openai-tools")

  return sql_agent