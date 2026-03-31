const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const flightResults = document.getElementById('flight-results');
const searchStatus = document.getElementById('search-status');

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage('user', text);
    userInput.value = '';
    
    const assistantMessageDiv = appendMessage('assistant', 'Thinking...');

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        assistantMessageDiv.innerText = data.chat_response;

        if (data.intent_detected && data.flights.length > 0) {
            renderFlights(data.flights, data.constraints);
        } else if (data.intent_detected && data.flights.length === 0) {
            searchStatus.innerText = `No flights found for your request.`;
            flightResults.innerHTML = '';
        }

    } catch (error) {
        assistantMessageDiv.innerText = "I'm sorry, I couldn't reach the flight search engine.";
        console.error(error);
    }
}

function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerText = text;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    return div;
}

function renderFlights(flights, constraints) {
    searchStatus.innerText = `Showing results for ${constraints.origin} to ${constraints.destination}`;
    flightResults.innerHTML = '';

    flights.forEach(flight => {
        const card = document.createElement('div');
        card.className = 'boarding-pass';
        
        const depTime = new Date(flight.departure_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const arrTime = new Date(flight.arrival_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        const depDate = new Date(flight.departure_time).toLocaleDateString();

        card.innerHTML = `
            <div class="pass-main">
                <div class="pass-header">
                    <div class="airline-name">${flight.airline}</div>
                    <div class="flight-number">FLIGHT ID: ${flight.id.substring(0,8).toUpperCase()}</div>
                </div>
                <div class="pass-content">
                    <div class="airport">
                        <span class="airport-code">${constraints.origin}</span>
                        <span class="airport-name">Departure</span>
                    </div>
                    <div class="pass-icon">✈</div>
                    <div class="airport" style="text-align: right;">
                        <span class="airport-code">${constraints.destination}</span>
                        <span class="airport-name">Arrival</span>
                    </div>
                </div>
                <div class="pass-details">
                    <div>
                        <span class="detail-label">Date</span>
                        <span class="detail-value">${depDate}</span>
                    </div>
                    <div>
                        <span class="detail-label">Departs</span>
                        <span class="detail-value">${depTime}</span>
                    </div>
                    <div>
                        <span class="detail-label">Stops</span>
                        <span class="detail-value">${flight.stops === 0 ? 'DIRECT' : flight.stops}</span>
                    </div>
                </div>
            </div>
            <div class="pass-stub">
                <div class="stub-price">${flight.price}</div>
                <button class="stub-btn">Book Now</button>
            </div>
        `;
        flightResults.appendChild(card);
    });
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
