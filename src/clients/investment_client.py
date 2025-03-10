from fastapi import HTTPException
from config import config_obj
import httpx

rapid_api_url = config_obj.RAPID_API_URL
rapid_api_key = config_obj.RAPID_API_KEY
rapid_api_host = config_obj.RAPID_API_HOST

headers = {
    "x-rapidapi-key": rapid_api_key,
    "x-rapidapi-host": rapid_api_host
}


async def fetch_data_from_api(query):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(rapid_api_url, headers=headers, params=query)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error fetching data: {response.text}"
                )
            try:
                data = response.json()
                return data
            except ValueError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from API")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API Error: {str(e)}")

async def get_openended_schemes_codes(scheme_code):
    query = {"Scheme_Type": 'Open Ended Schemes'}
    data = await fetch_data_from_api(query)

    found_scheme = find_scheme_code(scheme_code, data)
    return found_scheme if found_scheme else None

def find_scheme_code(scheme_code, data):
    for scheme in data:
        if scheme["Scheme_Code"] == scheme_code:
            return scheme
    return None


async def get_fund_list_RapidAPI(queries):
    print(queries)
    query = {"Scheme_Type": 'Open Ended Schemes'}
    query.update(queries)
    data = await fetch_data_from_api(query)

    print(type(data))
    return {
        "data": data,
    }
