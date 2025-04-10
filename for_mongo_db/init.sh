#!/bin/bash

# Configuration
ADMIN_USER="cinemaAdmin"
ADMIN_PASSWORD="SecurePassword123!"
DB_NAME="cinema_db"

# Install MongoDB
echo "🔧 Installing MongoDB..."
sudo apt-get update > /dev/null
sudo apt-get install -y gnupg curl > /dev/null

# Add MongoDB repo
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb.gpg
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install packages
sudo apt-get update > /dev/null
sudo apt-get install -y mongodb-org > /dev/null

# Start MongoDB service
echo "🚀 Starting MongoDB service..."
sudo systemctl start mongod
sudo systemctl enable mongod

# Wait for MongoDB to start
sleep 5

# Check if MongoDB is running
if ! systemctl is-active --quiet mongod; then
    echo "❌ Failed to start MongoDB!"
    exit 1
fi

# Create admin user
echo "🛠️ Creating admin user..."
mongosh --quiet <<EOF
use admin
db.createUser({
  user: "$ADMIN_USER",
  pwd: "$ADMIN_PASSWORD",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})
EOF

# Enable authentication
echo "🔒 Enabling authentication..."
sudo sed -i 's/#security:/security:\n  authorization: enabled/' /etc/mongod.conf

# Restart MongoDB
sudo systemctl restart mongod

# Create database
echo "💾 Creating database..."
mongosh --quiet -u $ADMIN_USER -p $ADMIN_PASSWORD --authenticationDatabase admin <<EOF
use $DB_NAME
db.createCollection("films")
db.createCollection("persons")
db.createCollection("admins")
EOF

echo -e "\n✅ Setup completed successfully!"
echo "-----------------------------------"
echo "Admin username: $ADMIN_USER"
echo "Admin password: $ADMIN_PASSWORD"
echo "Database name: $DB_NAME"
echo "Connection URI: mongodb://$ADMIN_USER:$ADMIN_PASSWORD@localhost:27017/$DB_NAME?authSource=admin"