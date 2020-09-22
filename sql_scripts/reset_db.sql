CREATE TABLE IF NOT EXISTS transactions(
	id SERIAL NOT NULL PRIMARY KEY UNIQUE,
	item TEXT NOT NULL,
	price INTEGER CHECK(price > 0),
	vendor TEXT,
	category_id INTEGER NOT NULL,
	date_of_purchase DATE DEFAULT CURRENT_DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS categories(
	id SERIAL NOT NULL PRIMARY KEY UNIQUE,
	category TEXT NOT NULL UNIQUE,
	descr TEXT
)