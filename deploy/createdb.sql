CREATE TABLE IF NOT EXISTS public.users (
    ID SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    age INTEGER NOT NULL
);