# История читателя

## Закрепление за залом (Reader Hall History)
GET `/api/reader-hall-history/`

POST `/api/reader-hall-history/`

POST тело:
```json
{ "reader": 1, "hall": 1, "valid_from": "2025-12-01", "valid_to": null }
```