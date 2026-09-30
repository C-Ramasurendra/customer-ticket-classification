import { useState, useEffect } from "react";
import TicketForm from "./components/TicketForm";
import TicketList from "./components/TicketList";
import { getAllTickets } from "./services/api";

function App() {
  const [tickets, setTickets] = useState([]);

  // Fetch all existing tickets once, when the page first loads
  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      const data = await getAllTickets();
      setTickets(data);
    } catch (error) {
      console.error("Failed to load tickets:", error);
    }
  };

  // Called by TicketForm whenever a new ticket is successfully created
  const handleTicketCreated = () => {
    loadTickets();
  };

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Ticket Classification System</h1>
      <TicketForm onTicketCreated={handleTicketCreated} />
      {/* onTicketDeleted reuses the same loadTickets function - */}
      {/* no separate delete-handling logic needed here */}
      <TicketList tickets={tickets} onTicketDeleted={loadTickets} />
    </div>
  );
}

export default App;
