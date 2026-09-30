import { deleteTicket } from "../services/api";

function TicketList({ tickets, onTicketDeleted }) {
  if (tickets.length === 0) {
    return <p>No tickets submitted yet.</p>;
  }

  const handleDelete = async (id) => {
    try {
      await deleteTicket(id);
      if (onTicketDeleted) {
        onTicketDeleted(); // tells App.js to refresh the ticket list
      }
    } catch (error) {
      console.error("Failed to delete ticket:", error);
      alert("Something went wrong deleting the ticket.");
    }
  };

  return (
    <div>
      <h3>Submitted Tickets</h3>
      {tickets.map((ticket) => {
        const isLowConfidence =
          ticket.confidence != null && ticket.confidence < 0.6;

        return (
          <div
            key={ticket.id}
            style={{
              border: isLowConfidence ? "2px solid #d9534f" : "1px solid #ccc",
              borderRadius: "6px",
              padding: "12px",
              marginBottom: "10px",
              backgroundColor: isLowConfidence ? "#fdf3f2" : "white",
            }}
          >
            {isLowConfidence && (
              <p style={{ color: "#d9534f", fontWeight: "bold", margin: "0 0 8px 0" }}>
                ⚠ Low confidence — needs review
              </p>
            )}

            <p><strong>Text:</strong> {ticket.text}</p>
            <p><strong>Category:</strong> {ticket.category || "Processing..."}</p>
            <p>
              <strong>Confidence:</strong>{" "}
              {ticket.confidence != null
                ? `${(ticket.confidence * 100).toFixed(1)}%`
                : "N/A"}
            </p>
            {ticket.suggestedResponse && (
              <p><strong>Suggested Response:</strong> {ticket.suggestedResponse}</p>
            )}

            <button
              onClick={() => handleDelete(ticket.id)}
              style={{ marginTop: "8px", color: "red" }}
            >
              Delete
            </button>
          </div>
        );
      })}
    </div>
  );
}

export default TicketList;
