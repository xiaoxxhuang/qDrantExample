# Vector Database POC - QDrant
Welcome to the Vector Database - QDrant Repository!

## Getting started
To get started with this project in local, please follow these steps:

1. **Create virtual environment and install dependencies**
    ```
    python -m venv venv
    source venv/bin/activate
    pip install -r app/requirements.txt
    ```
    > **_NOTE:_** To deactivate your virtual environment, just: `deactivate`
2. **Pull qdrant docker image for seting up a local qdrantdatabase**
    ```
    docker pull qdrant/qdrant
    ```
3. **Start your qdrant **