# Vector Database POC - QDrant
Welcome to the Vector Database - QDrant Repository!

# Getting started
To get started with this project in local, please follow these steps:

1. **Create virtual environment and install dependencies**
    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r app/requirements.txt
    ```
    > **_NOTE:_** To deactivate your virtual environment, just: `deactivate`

## Start Qdrant Server
1. **Pull qdrant docker image for seting up a local qdrant database**
    ```
    docker pull qdrant/qdrant
    ```

2. **Start your qdrant server**
    ```
    docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
    ```
    Starting a Qdrant vector search engine instance in Docker, making it accessible on your machine (via ports), and ensuring its data persists between restarts using a local folder.
3. **Navigate to `localhost:6333/dashboard` to visit the Qdrant.**

## Create Collection in Qdrant
1. **Add in the `--collection` for the Collection name.**
    ```
    python src/qdrant/create_collection.py --collection {{collectionName}}
    ```

## Query Chunks
1. **Upload chunks to qdrant**
    ```
    python main.py --input {{pdf_file_path}} --collection {{collection_name}}

    ```
2. **Start the local server**
    ```
    python app.py
    ```
3. **Query the chunks using POSTMAN or BRUNO**
    ```
    POST /localhost:6335/query
    body: {
        "collection_name": "Medicine",
        "query": "What is the active ingredient for STELARA?",
        "limit": 1
    }
    ```