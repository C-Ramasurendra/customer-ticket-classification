package com.ticketsystem.backend;

import org.springframework.data.jpa.repository.JpaRepository;

public interface TicketRepository extends JpaRepository<Ticket, Long> {
    // That's it! Spring Boot automatically gives us:
    // save(), findAll(), findById(), deleteById(), and more — for free.
}