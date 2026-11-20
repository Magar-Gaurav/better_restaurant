from app.core.jwt import create_access_token

data = {
    "sub" : "1"
}

token = create_access_token(data)
print("Generated JWWT: ")
print(token)