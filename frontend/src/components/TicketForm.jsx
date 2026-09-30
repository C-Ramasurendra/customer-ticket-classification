import { useState } from "react";
import { createTicket } from "../services/api";

function TicketForm({ onTicketCreated }) {
  // "state" - this remembers what the user has typed, and whether we're waiting on a response
  const [ticketText, setTicketText] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault(); // stops the page from refreshing (default browser form behavior)

    if (!ticketText.trim()) {
      return; // don't submit empty text
    }

    setIsSubmitting(true);

    try {
      const newTicket = await createTicket(ticketText);
      console.log("Ticket created:", newTicket);

      setTicketText(""); // clear the input box after successful submit

      // Tell the parent component (App.js) a new ticket was created,
      // so it can refresh the list shown on screen
      if (onTicketCreated) {
        onTicketCreated(newTicket);
      }
    } catch (error) {
      console.error("Failed to create ticket:", error);
      alert("Something went wrong submitting the ticket. Check the console.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <textarea
        value={ticketText}
        onChange={(e) => setTicketText(e.target.value)}
        placeholder="Describe your issue..."
        rows={4}
        style={{ width: "100%", padding: "8px" }}
      />
      <button type="submit" disabled={isSubmitting} style={{ marginTop: "8px" }}>
        {isSubmitting ? "Submitting..." : "Submit Ticket"}
      </button>
    </form>
  );
}

export default TicketForm;