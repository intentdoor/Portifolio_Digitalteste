#!/usr/bin/env python3
"""
Script to reset admin password and verify login credentials
"""

from werkzeug.security import generate_password_hash, check_password_hash
from models.data_store import data_store, init_data_store

def reset_admin_password():
    """Reset admin password to 'admin123'"""
    # Initialize data store
    init_data_store()
    
    # Find admin user
    admin_user = None
    for user in data_store['users']:
        if user.get('is_admin', False):
            admin_user = user
            break
    
    if admin_user:
        # Reset password
        new_password = 'admin123'
        admin_user['password_hash'] = generate_password_hash(new_password)
        
        print("✅ Admin password reset successfully!")
        print(f"📧 Email: {admin_user['email']}")
        print(f"🔑 Password: {new_password}")
        
        # Verify the password works
        if check_password_hash(admin_user['password_hash'], new_password):
            print("✅ Password verification successful!")
        else:
            print("❌ Password verification failed!")
    else:
        print("❌ Admin user not found!")

if __name__ == "__main__":
    reset_admin_password()