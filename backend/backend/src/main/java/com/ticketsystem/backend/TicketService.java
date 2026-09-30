package com.ticketsystem.backend;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Service
public class TicketService {

    @Autowired
    private TicketRepository ticketRepository;

    private final RestTemplate restTemplate = new RestTemplate();

    private static final String ML_SERVICE_URL = "http://localhost:8000/predict";

    public Ticket processNewTicket(Ticket ticket) {
        // 1. Build the request body Python expects: {"text": "..."}
        Map<String, String> requestBody = new HashMap<>();
        requestBody.put("text", ticket.getText());

        // 2. Call the Python ML service
        Map<String, Object> mlResponse = restTemplate.postForObject(
                ML_SERVICE_URL, requestBody, Map.class
        );

        // 3. Extract the results and attach them to the ticket
        if (mlResponse != null) {
            ticket.setCategory((String) mlResponse.get("category"));

            Object confidenceValue = mlResponse.get("confidence");
            if (confidenceValue != null) {
                ticket.setConfidence(((Number) confidenceValue).doubleValue());
            }

            ticket.setSuggestedResponse((String) mlResponse.get("suggested_response"));
        }

        // 4. Save the fully-completed ticket to MySQL
        return ticketRepository.save(ticket);
    }
}