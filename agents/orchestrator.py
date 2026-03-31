import os
import json
from google import genai
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from agents.flight_search import FlightSearchAgent

load_dotenv()

class OrchestratorAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemma-3-1b-it"
        self.search_agent = FlightSearchAgent()

    async def process_user_input(self, user_text: str) -> Dict[str, Any]:
        """
        Main entry point for user input. 
        Detects intent, queries flights if needed, and returns final results.
        """
        # Step 1: Detect Intent
        intent_prompt = f"""
        You are a flight travel assistant. 
        Analyze the user's message: "{user_text}"
        
        Examples:
        - "Hi": OTHER
        - "Hello there": OTHER
        - "I want to fly to Paris": FLIGHT_SEARCH
        - "Find me a flight from London to NYC on June 1st": FLIGHT_SEARCH
        - "How are you?": OTHER
        - "Can you help me find a flight?": FLIGHT_SEARCH
        
        Determine if the user is asking to search for flights.
        Respond ONLY with "FLIGHT_SEARCH" or "OTHER".
        """
        
        try:
            intent_response = self.client.models.generate_content(
                model=self.model_id,
                contents=intent_prompt
            )
            intent = intent_response.text.strip().upper()
            print(f"DEBUG: Raw Intent Response: '{intent_response.text}'")
            print(f"DEBUG: Detected Intent: {intent}")

            if "FLIGHT_SEARCH" not in intent:
                # Fallback to general conversation
                chat_response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=f"You are a helpful travel assistant. The user said: '{user_text}'. Respond naturally and helpfully."
                )
                return {
                    "chat_response": chat_response.text,
                    "flights": [],
                    "intent_detected": False
                }

            # Step 2: Extract Constraints
            extraction_prompt = f"""
            You are a flight intent extraction agent.
            Analyze the user's message: "{user_text}"
            Extract: origin (3-letter IATA code), destination (3-letter IATA code), departure_date (YYYY-MM-DD), return_date (YYYY-MM-DD or null), price_limit (number or null), passengers (number or 1).
            
            IMPORTANT: 
            - Use 3-letter IATA codes (e.g., LHR, JFK, CDG).
            - Use YYYY-MM-DD format for dates. Today is Tuesday, March 31, 2026.
            - Output ONLY a valid JSON object.
            """
            
            extraction_response = self.client.models.generate_content(
                model=self.model_id,
                contents=extraction_prompt
            )
            result_text = extraction_response.text.strip()
            print(f"DEBUG: Extraction Result: {result_text}")
            
            # Extract JSON from response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            constraints = json.loads(result_text)
            
            # Step 3: Query Flight Search Agent
            flight_data = await self.search_agent.search_flights(constraints)
            
            if "error" in flight_data:
                error_msg = flight_data['error']
                details = json.dumps(flight_data.get('details', {}))
                return {
                    "chat_response": f"I encountered an error searching for flights: {error_msg}. Details: {details}",
                    "flights": [],
                    "intent_detected": True,
                    "constraints": constraints
                }
            
            offers = flight_data.get("offers", [])
            
            # Step 3: Reformat and Recommend
            reformatted_flights = self._reformat_offers(offers)
            
            # Step 4: Generate Recommendation
            recommendation_prompt = f"""
            You are a helpful travel assistant.
            The user searched for: {json.dumps(constraints)}
            We found {len(reformatted_flights)} flight options.
            
            Flight Data (first 3 options): {json.dumps(reformatted_flights[:3])}
            
            Provide a short natural-language summary and a specific recommendation (e.g., "The cheapest option is with [Airline] for [Price]").
            Be concise and helpful.
            """
            
            recommendation_response = self.client.models.generate_content(
                model=self.model_id,
                contents=recommendation_prompt
            )
            
            return {
                "chat_response": recommendation_response.text,
                "flights": reformatted_flights,
                "intent_detected": True,
                "constraints": constraints
            }

        except Exception as e:
            return {
                "chat_response": f"I'm sorry, I had trouble processing that. Error: {str(e)}",
                "flights": [],
                "intent_detected": False
            }

    def _reformat_offers(self, offers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert raw Duffel offers to frontend-friendly cards.
        """
        reformatted = []
        for offer in offers:
            try:
                price = offer.get("total_amount")
                currency = offer.get("total_currency")
                airline = offer.get("owner", {}).get("name", "Unknown Airline")
                
                slices = offer.get("slices", [])
                if not slices: continue
                
                first_slice = slices[0]
                departure_time = first_slice.get("segments", [{}])[0].get("departing_at")
                arrival_time = first_slice.get("segments", [{}])[-1].get("arriving_at")
                duration = first_slice.get("duration", "N/A")
                stops = len(first_slice.get("segments", [])) - 1
                
                reformatted.append({
                    "airline": airline,
                    "price": f"{price} {currency}",
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "duration": duration,
                    "stops": stops,
                    "id": offer.get("id")
                })
            except:
                continue
        
        return reformatted[:10]

if __name__ == "__main__":
    import asyncio
    async def test():
        agent = OrchestratorAgent()
        res = await agent.process_user_input("I want to fly from London to JFK on June 15th")
        print(json.dumps(res, indent=2))
    
    # asyncio.run(test())
