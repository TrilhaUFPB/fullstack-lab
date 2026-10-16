-- Retorne o nome de cada participante do evento:event_id, em ordem de nome.
-- Consulte users e registrations; o teste fornece o parametro:event_id.

SELECT users.name
FROM registrations
JOIN users ON users.id = registrations.user_id
WHERE registrations.event_id = :event_id
ORDER BY users.name;
