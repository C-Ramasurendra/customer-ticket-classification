import axios from "axios";

const API_BASE_URL = "http://localhost:8080/tickets";

export const createTicket = async (text) => {
  const response = await axios.post(API_BASE_URL, { text });
  return response.data;
};

export const getAllTickets = async () => {
  const response = await axios.get(API_BASE_URL);
  return response.data;
};

// NEW: deletes a ticket by its id
export const deleteTicket = async (id) => {
  await axios.delete(`${API_BASE_URL}/${id}`);
};