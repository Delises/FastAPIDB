from fastapi import APIRouter
import os
import json
from elasticsearch import Elasticsearch
import datetime

router = APIRouter(tags=["Get info"])
es_url = os.environ.get("ES_URL")
es_key = os.environ.get("ES_TOKEN")
client = Elasticsearch(es_url, api_key=es_key)

@router.get("/info")
def about_me():
    inf = {
        "App": "NIST API tool",
        "Description": "This api tool developed to make NIST database requests easier",
        "Company Name": "FlawlessCat",
        "Developers": "Maksym Mospanko",
        "Contact emails": {
            "Personal": "dlisol.sing@gmail.com",
            "Work": "maksym.mospanko.kb.2021@lpnu.ua"
        }
    }
    return inf
@router.get("/get/all")
def get_all_cve():
    try:
        cve = []
        current_date = datetime.datetime.today()
        previous_date = current_date - datetime.timedelta(days=5)
        query = {
            "query": {
                "range": {
                    "dateAdded": {
                        "gte": previous_date,
                        "format": "yyyy-MM-dd'T'HH:mm:ss.SSSSSS"
                    }
                }
            },
            "sort": [
                {"dateAdded": {"order": "desc"}}
            ],
            "size": 40
        }
        response = client.search(index="cve", body=query)
        for match in response["hits"]["hits"]:
            cve.append(match["_source"])
        return cve
    except Exception as e:
        return {"Error in get_all_cve:": {e}}

@router.get("/get")
def get_cve_by_key(query: str):
    try:
        cve = []
        search_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["cveID", "vendorProject","vulnerabilityName", "shortDescription", "requiredAction", "notes",],
                    "fuzziness": "AUTO" 
                }
            },
        }
        response = client.search(index="cve", body=search_query)
        for match in response["hits"]["hits"]:
            cve.append(match["_source"])
        return cve
    except Exception as e:
        return {"Error in get_cve_by_key:": {e}}

@router.get("/get/new")
def get_new_cve():
    try:
        cve = []
        query = {
            "query": {
                "match_all": {}
            },
            "sort": [
                {"dateAdded": {"order": "desc"}}
            ],
            "size": 10
        }
        response = client.search(index="cve", body=query)
        for match in response["hits"]["hits"]:
            cve.append(match["_source"])
        return cve
    except Exception as e:
        return {"Error in get_new_cve:": {e}}

@router.get("/get/known")
def get_known():
    try:
        cve = []
        query = {
            "query": {
                "term": {
                    "knownRansomwareCampaignUse.keyword": "Known"
                }
            },
            "size": 10
        }
        response = client.search(index="cve", body=query)
        for match in response["hits"]["hits"]:
            cve.append(match["_source"])
        return cve
    except Exception as e:
        return {"Error in get_known:": {e}}