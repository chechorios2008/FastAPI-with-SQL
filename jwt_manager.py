from jwt import encode, decode

# encode => 
def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="my_secrete_key", algorithm= "HS256")
    return token

# decode => 
def validate_token(token: str) -> str:
    data: dict = decode(token, key="my_secrete_key", algorithms = ['HS256'])
    return data