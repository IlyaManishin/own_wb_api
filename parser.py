import requests
import traceback
import json
import time 
from datetime import datetime, timedelta

def get_promotions(token: str):
    headers = {"Authorization" : token}
    all_adverts = _get_all_adverts_ids(headers)
    if len(all_adverts) == 0:
        return {"adverts" : []}
    
    all_results = []
    url = "https://advert-api.wildberries.ru/adv/v2/fullstats"
    
    end_period_str = datetime.strftime(datetime.now(), r"%Y-%m-%d")
    start_period_str = datetime.strftime(datetime.now() - timedelta(days=7), r"%Y-%m-%d")
    
    for i in range((len(all_adverts)-1)//90 + 1):
        try:
            adverts_query = all_adverts[i*90: (i + 1) * 90]
            post_data = []
            for advert in adverts_query:
                entry = {
                    "id" : advert,
                    "interval": {
                        "begin": start_period_str,
                        "end": end_period_str,
                    }
                }
                post_data.append(entry)
            resp = requests.post(url, headers=headers, json=post_data, timeout=60)
            text = resp.text
            result = json.loads(text)
            
            if "error" not in result and isinstance(result, list):
                all_results += result

        except:
            traceback.print_exc()
        finally:
            time.sleep(60)
    results_to_response = []
    for i in all_results:
        id = i.get("advertId", "")
        days = i.get("days", [])
        for day in days:
            entry = {
                "id" : id,
                "date" : day.get("date", "").split("T")[0],
                "views" : day.get("views", ""),
                "clicks" : day.get("clicks", ""),
                "ctr" : day.get("ctr", ""),
                "cpc" : day.get("cpc", ""),
                "sum" : day.get("sum", ""),
                "atbs" : day.get("atbs", ""),
                "orders" : day.get("orders", ""),
                "cr" : day.get("cr", ""),
                "shks" : day.get("shks", ""),
                "sum_price" : day.get("sum_price", ""),
            }
            results_to_response.append(entry)
    return results_to_response

def get_keywords_stats(token):
    headers = {"Authorization" : token}
    all_adverts_ids = _get_all_adverts_ids(headers)
    if len(all_adverts_ids) == 0:
        return {"adverts" : []}
    all_results = []
    
    for id in all_adverts_ids:
        url = f"https://advert-api.wildberries.ru/adv/v1/stat/words?id={id}"
        try:
            req = requests.get(url, headers=headers)
            text = req.text
            data = json.loads(text)
            stats = data.get("stat", [])
            for i in stats[1::]:
                all_results.append(dict(i))   
        except:
            continue
        finally:
            time.sleep(0.25)
    return all_results

def get_clusters(token):
    headers = {"Authorization" : token}
    all_adverts_ids = _get_all_adverts_ids(headers)
    if len(all_adverts_ids) == 0:
        return {"adverts" : []}
    all_results = []
    
    for id in all_adverts_ids:
        url = f"https://advert-api.wildberries.ru/adv/v2/auto/stat-words?id={id}"
        try:
            req = requests.get(url, headers=headers)
            text = req.text
            data = json.loads(text)
            clusters = data.get("clusters", [])
            for cluster in clusters:
                name = cluster.get("cluster", "")
                keywords = cluster.get("keywords", [])
                for key in keywords:
                    entry = {
                        "advertId" : id,
                        "cluster" : name,
                        "keyword" : key,
                    }
                    all_results.append(entry)
        except:
            continue
        finally:
            time.sleep(0.25)
    return all_results
    
def _get_all_adverts_ids(headers):
    all_adverts = []
    try:
        url = "https://advert-api.wildberries.ru/adv/v1/promotion/count"
        resp = requests.get(url=url, headers=headers)
        text = resp.text
        data = json.loads(text)
        
        for i in data["adverts"]:
            for j in i["advert_list"]:
                all_adverts.append(j["advertId"])
                
    except Exception as err:
        print(err)
    return all_adverts