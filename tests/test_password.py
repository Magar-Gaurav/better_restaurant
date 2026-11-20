from app.core.security import hash_password, verify_password

password = "hellouser#123"

hashed = hash_password(password)

print("Original password: ", password)
print("Hashed password: ", hashed)

print("Correct password: ", verify_password(password, hashed))

print("Incorrect password: ", verify_password("hellouser@123", hashed))