# Unified People API – Specification

## Base URL
http://localhost:8000

Authentication:
Send header:
X-API-Key: <your_key>

---

## GET /search
Search dataset using filters.

### Query Parameters
q = global search  
first_name  
last_name  
company  
email  
country  
limit  
offset  

### Response
{
  "items": [...],
  "count": 10,
  "limit": 10,
  "offset": 0,
  "response_time_ms": 122
}

---

## POST /admin/add_credits
Add credits to a user.

Body:
{
  "api_key": "abc123",
  "credits": 1000
}

---

## GET /logs
View recent API calls.

