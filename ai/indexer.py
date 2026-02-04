import asyncio
import httpx
from dotenv import load_dotenv
load_dotenv()
import logging
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from config import settings

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
# Force localhost for host-side indexing since docker 'core' dns is not available here
CORE_SERVICE_URL = settings.CORE_SERVICE_URL
INTERNAL_API_KEY = settings.INTERNAL_API_KEY
CHROMA_SERVER_HOST = settings.CHROMA_SERVER_HOST
CHROMA_SERVER_HTTP_PORT = settings.CHROMA_SERVER_HTTP_PORT

async def index_challenges():
    logger.info("Starting challenge indexing...")
    logger.info(f"Using key: {INTERNAL_API_KEY}")
    
    # 1. Fetch Challenges from Core
    headers = {"X-Internal-API-Key": INTERNAL_API_KEY}
    try:
        url = f"{CORE_SERVICE_URL}/api/challenges/internal-list/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to fetch challenges: {response.status_code}")
                return
            
            challenges = response.json()
            logger.info(f"Fetched {len(challenges)} challenges")
    except Exception as e:
        logger.error(f"Error fetching challenges: {e}")
        return

    # 2. Prepare Data
    documents = []
    metadatas = []
    ids = []
    
    for chall in challenges:
        slug = chall.get("slug")
        content = f"Title: {chall.get('title')}\nDescription: {chall.get('description')}\nTest Code: {chall.get('test_code')}"
        documents.append(content)
        metadatas.append({"slug": slug, "title": chall.get("title")})
        ids.append(slug)

    # 3. Initialize Embeddings and Vector DB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Use HttpClient to connect to the separate Chroma container
    vector_db = Chroma(
        client=chromadb.HttpClient(host=CHROMA_SERVER_HOST, port=CHROMA_SERVER_HTTP_PORT),
        embedding_function=embeddings,
        collection_name="challenges"
    )
    
    # 4. Add documents (This might be sync in Langchain Chroma wrapper, or we wrap it)
    # The current LangChain Chroma implementation is synchronous for add_texts
    try:
        vector_db.add_texts(
            texts=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Indexing complete. {len(documents)} documents indexed.")
    except Exception as e:
        logger.error(f"Error adding to Chroma: {e}")

if __name__ == "__main__":
    asyncio.run(index_challenges())


