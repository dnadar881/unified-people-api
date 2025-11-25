# Credit System

Each user has:
- api_key
- credits
- rate_limit (requests per minute)

Rules:
1. Every /search request deducts 1 credit.
2. If credits = 0 → API returns:
   {
     "error": "Insufficient credits"
   }
3. Every request logged in api_logs table.
4. Logs include:
   - timestamp
   - used credits
   - duration
   - endpoint
   - parameters
5. Admin can add credits using /admin/add_credits
