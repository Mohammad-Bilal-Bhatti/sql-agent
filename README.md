# SQL-Agent

## Overview
Chat with your database with natural language. Inspired by the pattern in ai world _chat with your **'X'**_ where X could be anything you desire eg. your database, your application, your spreadsheet, your pdfs etc... 

Following is the process that SQL agent follows.
1. Question is passed to LLM to generate query.
2. LLM generate the SQL query.
3. Query is executed using db.
4. Query result is passed to LLM again for making proper response.


This project is build to top of langchain and langserve modules.

Here is the general architecture (stolen from langchain website)
![Agent Architecture](/assets/architecture.png)

> ## ⚠️ Security Note ⚠️
>
> This agent is **not production ready** and may do unexpected results. How ever you can experiment it with your local database. You can control agent behaviour using prompt engineering by limiting access to certain DML statements eg. INSERT, UPDATE, DELETE, DROP, etc... Or you can use SQL user-connection with limited privileges to certain tables or views only.

There still some work is required on this project that allow SQL agent to use tools to add advance question and reasioning capabilities. 

## Installation

Install the LangChain CLI if you haven't already

```bash
# Global installation of langchain cli
# Used for scafolding boilerplate for making agents
pip install -U langchain-cli

# Create virtual env
python -m venv venv

# Activate virtual env windows
venv/Scripts/activate

# Active virtual env unix
source venv/bin/activate

# For Unix users please ensure you have mysql-client and pkg-config installed already 
# If not follow the steps mentioned here https://github.com/PyMySQL/mysqlclient

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp sample.env .env

# > Make sure you have added your environment config in .env file

# Run agent locally
langchain serve

# Now explore swagger and try your queries using swagger
start http://localhost:8000/docs

# Or you can experiment using langchain playground
start http://localhost:8000/agent/playground
```


## Adding additional packages (optional)

```bash
# adding packages from 
# https://github.com/langchain-ai/langchain/tree/master/templates
langchain app add $PROJECT_NAME

# adding custom GitHub repo packages
langchain app add --repo $OWNER/$REPO
# or with whole git string (supports other git providers):
# langchain app add git+https://github.com/hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
langchain app add $PROJECT_NAME --api_path=/my/custom/path/rag
```

Note: you remove packages by their api path

```bash
langchain app remove my/custom/path/rag
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch LangServe

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t sql-agent
```

If you tag your image with something other than `sql-agent`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` and `DB_URL` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`) and (`$DB_URL`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -e DB_URL=$DB_URL -p 8080:8080 sql-agent
```

# License
MIT - Free to use, modify or publish without any warranty

# References

- [Langchain SQL Agent Tutorial](https://python.langchain.com/docs/tutorials/sql_qa/).
- [Building Rest apis using langchain](https://www.koyeb.com/tutorials/using-langserve-to-build-rest-apis-for-langchain-applications).
- [Prompt Engineering](https://help.openai.com/en/articles/10032626-prompt-engineering-best-practices-for-chatgpt).
- [Lang Graph](https://blog.langchain.dev/langgraph).
- [Guide to Langchain Graps](https://medium.com/@umang91999/beginners-guide-to-langchain-graphs-states-nodes-and-edges-3ca7f3de5bfe).
- [Langchain Hub for finding engineered prompts](https://smith.langchain.com/hub).
- [Instoduction to Langserve](https://blog.langchain.dev/introducing-langserve).