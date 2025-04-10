db = db.getSiblingDB("cinema_db");

// Создаем коллекции
db.createCollection("film");
db.createCollection("person");
db.createCollection("admin");

// Создаем пользователя только для cinema_db
db.createUser({
  user: "cinemaAdmin",
  pwd: "SecurePassword123!",
  roles: [
    { role: "readWrite", db: "cinema_db" },
    { role: "dbAdmin", db: "cinema_db" }
  ]
});

print("User 'cinemaAdmin' created successfully!");