# Authorization and signin app
Written in python
## How to run
```bash
pip install requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
***
## Testing endpoints
### 1. Signup
```curl
curl -X POST "http://localhost:8000/auth/signup" \
-H "Content-Type: application/json" \
-d '{
  "email": "user@example.com",
  "password": "securepassword123"
}'
```
### 2. Signin
```curl
curl -X POST "http://localhost:8000/auth/signin" \
-H "Content-Type: application/json" \
-d '{
  "email": "user@example.com",
  "password": "securepassword123"
}'
```
### 3. Authorize
```curl
curl -X GET "http://localhost:8000/auth/authorize" \
-H "Authorization: Bearer <your_access_token>"
```
### 4. Revoke Token
```curl
curl -X POST "http://localhost:8000/token/revoke" \
-H "Content-Type: application/json" \
-d '{"token": "<your_refresh_token>"}'
```
### 5. Refresh Token
```curl
curl -X POST "http://localhost:8000/token/refresh" \
-H "Content-Type: application/json" \
-d '{"token": "<your_refresh_token>"}'
```