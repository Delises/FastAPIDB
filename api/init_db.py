from fastapi import APIRouter
import json
import os
from api import create_db
from elasticsearch import Elasticsearch

router = APIRouter(tags=["Init Database"])
es_url = os.environ.get("ES_URL")
es_key = os.environ.get("ES_TOKEN")
cve_file = os.environ.get("CVE_FILE")
with open(cve_file, 'r') as file:
    data = json.load(file)

@router.get("/init-db")
def upload_json():
    try:
        index_name="cve"
        client = Elasticsearch(es_url, api_key=es_key)
        if not client.indices.exists(index=index_name):
            create_db.create_ind(index_name)
        all_cve = data.get("vulnerabilities", [])
        for cve in all_cve:
            cve_id = cve.get("cveID", {})
            client.index(index="cve", id=cve_id, document=cve)

        return {"message": "Successs"}
    except Exception as e:
        return {"Error in upload_json:": {e}}