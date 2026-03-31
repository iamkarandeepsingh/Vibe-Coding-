import os
import httpx
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

load_dotenv()

class FlightSearchAgent:
    def __init__(self):
        self.api_key = os.getenv("DUFFEL_API_KEY")
        self.base_url = "https://api.duffel.com/air"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Duffel-Version": "v2",
            "Content-Type": "application/json"
        }

    async def search_flights(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query Duffel API for flight offers.
        query schema: { "origin": "string", "destination": "string", "departure_date": "YYYY-MM-DD", 
                        "return_date": "YYYY-MM-DD | null", "passengers": "number | 1" }
        """
        if not self.api_key:
            return {"error": "DUFFEL_API_KEY not found in environment."}

        # Prepare slices
        slices = [
            {
                "origin": query.get("origin"),
                "destination": query.get("destination"),
                "departure_date": query.get("departure_date")
            }
        ]
        
        # If return date is provided, add second slice
        if query.get("return_date"):
            slices.append({
                "origin": query.get("destination"),
                "destination": query.get("origin"),
                "departure_date": query.get("return_date")
            })

        # Prepare passengers
        num_passengers = query.get("passengers", 1)
        passengers = [{"type": "adult"} for _ in range(int(num_passengers))]

        payload = {
            "data": {
                "slices": slices,
                "passengers": passengers,
                "cabin_class": "economy"
            }
        }
        
        print(f"DEBUG: Duffel Payload: {payload}")

        try:
            async with httpx.AsyncClient() as client:
                # 1. Create offer request
                response = await client.post(
                    f"{self.base_url}/offer_requests",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code != 201:
                    return {
                        "error": f"Duffel API Error: {response.status_code}",
                        "details": response.json()
                    }
                
                offer_request_data = response.json()["data"]
                offers = offer_request_data.get("offers", [])
                
                # If no offers in the immediate response, we might need to fetch them (though Duffel usually returns some)
                # But typically 'offers' is populated if 'return_offers' wasn't set to false.
                
                return {
                    "offers": offers,
                    "id": offer_request_data.get("id")
                }

        except Exception as e:
            return {"error": f"Internal Search Agent Error: {str(e)}"}

if __name__ == "__main__":
    # Quick test
    import asyncio
    async def test():
        agent = FlightSearchAgent()
        # Mock query
        query = {
            "origin": "LHR",
            "destination": "JFK",
            "departure_date": "2026-06-15",
            "passengers": 1
        }
        res = await agent.search_flights(query)
        print(res)
    
    # asyncio.run(test()) # Uncomment to test
