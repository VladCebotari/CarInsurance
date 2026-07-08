CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS owners (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL CHECK (
        LENGTH(name) BETWEEN 1 AND 255
        AND name ~ '^[A-Za-z]+( [A-Za-z]+)*$'
    ),
    birthdate DATE NOT NULL CHECK (
        birthdate >= DATE '1900-01-01'
        AND birthdate <= CURRENT_DATE
    ),
    year_of_driver_license INTEGER NOT NULL CHECK (
        year_of_driver_license BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)
    ),
    driver_license_cat VARCHAR(4) CHECK (
        driver_license_cat IN ('A', 'B', 'C', 'D', 'E', 'NONE')
    ),
    email VARCHAR(255) UNIQUE
);

INSERT INTO owners (
    id,
    name,
    birthdate,
    year_of_driver_license,
    driver_license_cat,
    email
) VALUES
    (
        '11111111-1111-1111-1111-111111111111',
        'John Doe',
        '1990-05-15',
        2010,
        'B',
        'john@example.com'
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        'Jane Smith',
        '1985-08-22',
        2005,
        'B',
        'jane@example.com'
    ),
    (
        '33333333-3333-3333-3333-333333333333',
        'Alex Brown',
        '1995-03-10',
        2016,
        'A',
        'alex.brown@example.com'
    ),
    (
        '44444444-4444-4444-4444-444444444444',
        'Maria Popescu',
        '1992-11-04',
        2012,
        'C',
        'maria.popescu@example.com'
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        'Victor Ionescu',
        '1978-07-19',
        1998,
        NULL,
        'victor.ionescu@example.com'
    )
ON CONFLICT (id) DO NOTHING;
