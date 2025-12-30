from passlib.context import CryptContext

# Create a CryptContext for password hashing using the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def normalize_password(password: str) -> str:
    """
    Normalizes the password by truncating it to 72 bytes to ensure compatibility with bcrypt.
    """
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    """
    Takes plain password and returns hashed password
    """
    password = normalize_password(password)
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if plain_password matches hashed_password
    """
    plain_password = normalize_password(plain_password)
    return pwd_context.verify(plain_password, hashed_password)



def create_manual_token(user_id: str, expires_seconds: int = 3600) -> str:
    """
    Creates a simple token containing user_id and expiry timestamp
    """
    payload = {
        "user_id": user_id,
        "iat": int(time.time()),  # issued at
        "exp": int(time.time()) + expires_seconds  # expiry timestamp
    }
    # convert payload to JSON string
    payload_str = json.dumps(payload)
    
    # encode to base64 to make it string-safe
    token = base64.urlsafe_b64encode(payload_str.encode()).decode()
    return token

def verify_manual_token(token: str) -> dict:
    """
    Verifies the manual token and returns the payload if valid
    """
    try:
        # decode from base64
        payload_str = base64.urlsafe_b64decode(token.encode()).decode()
        payload = json.loads(payload_str)
        
        # check expiry
        if payload["exp"] < int(time.time()):
            raise ValueError("Token expired")
        
        return payload
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")

