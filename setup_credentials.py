import base64, json
B64_DATA = "[STRIPPED 552 bytes]"
with open("credentials.json", "w") as f:
    f.write(base64.b64decode(B64_DATA).decode())
print("credentials.json created")
