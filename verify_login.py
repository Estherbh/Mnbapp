import json
import bcrypt

def verify():
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
        
        user = next((u for u in data['users'] if u['email'] == 'bbwende@virunga.org'), None)
        if not user:
            print("User not found")
            return

        stored_hash = user['password_hash']
        password = "virunga2025"
        
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            print("SUCCESS: Password matches!")
        else:
            print("FAILURE: Password does NOT match.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify()
