# История читательских билетов

GET `/api/ticket-history/`

POST `/api/ticket-history/`

POST тело:
```json
{ "reader": 1, "ticket_number": "T-000001", "valid_from": "2025-12-01", "valid_to": null }
```