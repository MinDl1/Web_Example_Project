db = db.getSiblingDB("admin");
db.createUser({
  user: process.env.TEST_MONGO_USER,
  pwd: process.env.TEST_MONGO_PASSWD,
  roles: [{ role: "readWrite", db: process.env.TEST_MONGO_DATABASE_NAME }],
});
