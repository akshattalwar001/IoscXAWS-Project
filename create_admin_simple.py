import psycopg2
from argon2 import PasswordHasher

# Initialize password hasher
ph = PasswordHasher()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='mydb',
    user='postgres',
    password='Waqar@0802'
)
cursor = conn.cursor()

# Hash the password
admin_password_hash = ph.hash('TcM#7kP$9vL@2wQx')

# Insert admin user
try:
    cursor.execute(
        "INSERT INTO users (username, role, password_hash, password_changed) VALUES (%s, %s, %s, %s)",
        ('AdminIA100', 'admin', admin_password_hash, True)
    )
    conn.commit()
    print('✓ Admin AdminIA100 created successfully!')
    print('  Password: TcM#7kP$9vL@2wQx')
except psycopg2.IntegrityError:
    print('✓ Admin AdminIA100 already exists')
    conn.rollback()
finally:
    cursor.close()
    conn.close()
