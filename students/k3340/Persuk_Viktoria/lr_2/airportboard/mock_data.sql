-- === Моковые данные для Flight ===

INSERT INTO flight_flight (flight_number, airline, departure, arrival, flight_type, gate, created_at, updated_at, seats_count, description)
VALUES
('SU101', 'Aeroflot', '2025-11-03 09:00:00', '2025-11-03 13:00:00', 'departure', 'A12', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 180, 'Москва — Париж'),
('LH202', 'Lufthansa', '2025-11-03 10:30:00', '2025-11-03 14:45:00', 'departure', 'B03', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 150, 'Берлин — Рим'),
('KL303', 'KLM', '2025-11-04 06:00:00', '2025-11-04 10:00:00', 'arrival', 'C07', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 200, 'Амстердам — Москва'),
('AF404', 'Air France', '2025-11-05 12:00:00', '2025-11-05 15:00:00', 'arrival', 'A05', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 220, 'Париж — Москва'),
('BA505', 'British Airways', '2025-11-06 08:00:00', '2025-11-06 10:15:00', 'departure', 'D09', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 190, 'Москва — Лондон'),
('SU106', 'Aeroflot', '2025-11-07 09:30:00', '2025-11-07 13:30:00', 'departure', 'A10', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 180, 'Москва — Мадрид'),
('LH207', 'Lufthansa', '2025-11-08 11:00:00', '2025-11-08 13:50:00', 'arrival', 'B04', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 150, 'Берлин — Москва'),
('KL308', 'KLM', '2025-11-09 06:30:00', '2025-11-09 09:45:00', 'departure', 'C08', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 200, 'Москва — Амстердам'),
('AF409', 'Air France', '2025-11-10 07:45:00', '2025-11-10 11:15:00', 'departure', 'A06', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 220, 'Москва — Париж'),
('BA510', 'British Airways', '2025-11-11 13:30:00', '2025-11-11 16:10:00', 'arrival', 'D10', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 190, 'Лондон — Москва'),
('SU111', 'Aeroflot', '2025-11-12 09:10:00', '2025-11-12 13:25:00', 'departure', 'A13', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 180, 'Москва — Берлин'),
('LH212', 'Lufthansa', '2025-11-13 10:45:00', '2025-11-13 13:30:00', 'departure', 'B06', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 150, 'Москва — Цюрих'),
('KL313', 'KLM', '2025-11-14 06:15:00', '2025-11-14 09:30:00', 'arrival', 'C09', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 200, 'Амстердам — Москва'),
('AF414', 'Air France', '2025-11-15 12:30:00', '2025-11-15 15:45:00', 'arrival', 'A07', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 220, 'Париж — Москва'),
('BA515', 'British Airways', '2025-11-16 08:10:00', '2025-11-16 10:25:00', 'departure', 'D12', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 190, 'Москва — Лондон'),
('SU116', 'Aeroflot', '2025-11-17 09:45:00', '2025-11-17 13:55:00', 'departure', 'A14', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 180, 'Москва — Рим'),
('LH217', 'Lufthansa', '2025-11-18 11:20:00', '2025-11-18 14:10:00', 'arrival', 'B07', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 150, 'Берлин — Москва'),
('KL318', 'KLM', '2025-11-19 07:00:00', '2025-11-19 10:00:00', 'departure', 'C10', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 200, 'Москва — Амстердам'),
('AF419', 'Air France', '2025-11-20 07:55:00', '2025-11-20 11:25:00', 'departure', 'A08', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 220, 'Москва — Париж'),
('BA520', 'British Airways', '2025-11-21 13:10:00', '2025-11-21 15:50:00', 'arrival', 'D14', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 190, 'Лондон — Москва');

-- === Моковые данные для Reservation ===
INSERT INTO flight_reservation (user_id, flight_id, seat_number, ticket_number, created_at, updated_at, status)
VALUES
(1, 1, '12A', 'SU101-001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(2, 1, '12B', 'SU101-002', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(3, 2, '14C', 'LH202-003', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'cancelled'),
(1, 3, '15A', 'KL303-004', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(2, 4, '11D', 'AF404-005', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(3, 5, '18E', 'BA505-006', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'checked_in'),
(4, 6, '22F', 'SU106-007', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(1, 7, '9A', 'LH207-008', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(2, 8, '10B', 'KL308-009', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(3, 9, '19C', 'AF409-010', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'cancelled'),
(1, 10, '13D', 'BA510-011', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(2, 11, '7E', 'SU111-012', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'checked_in'),
(3, 12, '8F', 'LH212-013', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(4, 13, '17A', 'KL313-014', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(1, 14, '6B', 'AF414-015', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(2, 15, '12C', 'BA515-016', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'cancelled'),
(3, 16, '5D', 'SU116-017', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(4, 17, '3E', 'LH217-018', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(1, 18, '2F', 'KL318-019', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved'),
(2, 19, '4A', 'AF419-020', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'checked_in'),
(3, 20, '1B', 'BA520-021', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'reserved');

-- === Моковые данные для Comment ===
INSERT INTO flight_comment (flight_id, author_id, flight_date, text, rating, created_at)
VALUES
(1, 1, '2025-11-03', 'Очень удобный рейс, всё по расписанию!', 9, CURRENT_TIMESTAMP),
(1, 2, '2025-11-03', 'Было немного холодно в салоне.', 7, CURRENT_TIMESTAMP),
(2, 3, '2025-11-03', 'Прекрасное обслуживание, но задержка на 20 минут.', 8, CURRENT_TIMESTAMP),
(3, 1, '2025-11-04', 'Прилет без опозданий, экипаж отличный.', 10, CURRENT_TIMESTAMP),
(4, 2, '2025-11-05', 'Долго ждали багаж.', 6, CURRENT_TIMESTAMP),
(5, 3, '2025-11-06', 'Пилот молодец, мягкая посадка.', 10, CURRENT_TIMESTAMP),
(6, 4, '2025-11-07', 'Обычный рейс, ничего особенного.', 8, CURRENT_TIMESTAMP),
(7, 1, '2025-11-08', 'Сервис на уровне.', 9, CURRENT_TIMESTAMP),
(8, 2, '2025-11-09', 'Много турбулентности, но всё ок.', 7, CURRENT_TIMESTAMP),
(9, 3, '2025-11-10', 'Приятная атмосфера и вкусная еда.', 10, CURRENT_TIMESTAMP);
