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
        driver_license_cat IN ('A', 'B', 'C', 'D', 'E', 'none')
    ),
    email VARCHAR(255) UNIQUE
);

CREATE INDEX IF NOT EXISTS ix_owners_email ON owners (email);

CREATE TABLE IF NOT EXISTS cars (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vin VARCHAR(16) UNIQUE NOT NULL CHECK (
        LENGTH(vin) BETWEEN 1 AND 16
        AND vin ~ '^[A-Za-z0-9]+$'
    ),
    make VARCHAR(150) CHECK (
        make IS NULL OR (
            LENGTH(make) BETWEEN 1 AND 150
            AND make ~ '^[A-Za-z0-9]+( [A-Za-z0-9]+)*$'
        )
    ),
    model VARCHAR(150) CHECK (
        model IS NULL OR (
            LENGTH(model) BETWEEN 1 AND 150
            AND model ~ '^[A-Za-z0-9]+( [A-Za-z0-9]+)*$'
        )
    ),
    year_of_manufacture INTEGER NOT NULL CHECK (
        year_of_manufacture BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)
    ),
    category VARCHAR(8) CHECK (
        category IN ('EURO3', 'EURO4', 'EURO5', 'EURO6', 'HYBRID', 'ELECTRIC')
    ),
    cc INTEGER NOT NULL CHECK (cc BETWEEN 1 AND 10000),
    power INTEGER NOT NULL CHECK (power BETWEEN 1 AND 500),
    owner_id UUID NOT NULL REFERENCES owners(id)
);

CREATE TABLE IF NOT EXISTS insurance_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    car_id UUID NOT NULL REFERENCES cars(id),
    provider VARCHAR(100) CHECK (
        provider IS NULL OR (
            LENGTH(provider) BETWEEN 1 AND 100
            AND provider ~ '^[A-Za-z0-9]+( [A-Za-z0-9]+)*$'
        )
    ),
    start_date DATE NOT NULL CHECK (
        EXTRACT(YEAR FROM start_date) BETWEEN 1900
        AND 2100
    ),
    end_date DATE NOT NULL CHECK (
        EXTRACT(YEAR FROM end_date) BETWEEN 1900
        AND 2100
    ),
    status VARCHAR(50),
    paid_amount NUMERIC(12, 2) NOT NULL CHECK (
        paid_amount > 0
        AND paid_amount < 1000000
    ),
    CHECK (end_date >= start_date)
);

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    car_id UUID NOT NULL REFERENCES cars(id),
    claim_date DATE NOT NULL CHECK (
        claim_date >= DATE '1900-01-01'
        AND claim_date <= CURRENT_DATE
    ),
    description TEXT NOT NULL CHECK (
        LENGTH(description) BETWEEN 1 AND 2000
        AND description ~ '^[A-Za-z0-9]+( [A-Za-z0-9]+)*$'
    ),
    amount NUMERIC(12, 2) NOT NULL CHECK (
        amount > 0
        AND amount < 1000000
    ),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

TRUNCATE TABLE claims, insurance_policies, cars, owners CASCADE;

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
        '12121212-1212-1212-1212-121212121212',
        'Alex Rider',
        '1995-02-11',
        2016,
        'A',
        'alex@example.com'
    ),
    (
        '23232323-2323-2323-2323-232323232323',
        'Maria Popescu',
        '1978-11-03',
        1999,
        'C',
        'maria@example.com'
    ),
    (
        '34343434-3434-3434-3434-343434343434',
        'Victor Ionescu',
        '1982-07-19',
        2003,
        'D',
        'victor@example.com'
    ),
    (
        '45454545-4545-4545-4545-454545454545',
        'Elena Marin',
        '1992-12-05',
        2014,
        'E',
        'elena@example.com'
    ),
    (
        '56565656-5656-5656-5656-565656565656',
        'No License Owner',
        '2000-01-20',
        2020,
        NULL,
        'nolicense@example.com'
    );

INSERT INTO cars (
    id,
    vin,
    make,
    model,
    year_of_manufacture,
    category,
    cc,
    power,
    owner_id
) VALUES
    (
        '33333333-3333-3333-3333-333333333333',
        'VIN123456789',
        'Dacia',
        'Logan',
        2020,
        'EURO6',
        1600,
        100,
        '11111111-1111-1111-1111-111111111111'
    ),
    (
        '44444444-4444-4444-4444-444444444444',
        'VIN987654321',
        'Volkswagen',
        'Golf',
        2019,
        'EURO5',
        2000,
        150,
        '11111111-1111-1111-1111-111111111111'
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        'VIN456789123',
        'BMW',
        'X3',
        2022,
        'HYBRID',
        2500,
        190,
        '22222222-2222-2222-2222-222222222222'
    ),
    (
        '13131313-1313-1313-1313-131313131313',
        'VINA00000001',
        'Yamaha',
        'MT 07',
        2021,
        'EURO5',
        689,
        74,
        '12121212-1212-1212-1212-121212121212'
    ),
    (
        '24242424-2424-2424-2424-242424242424',
        'VINC00000001',
        'Mercedes Benz',
        'Actros',
        2018,
        'EURO6',
        10000,
        420,
        '23232323-2323-2323-2323-232323232323'
    ),
    (
        '35353535-3535-3535-3535-353535353535',
        'VIND00000001',
        'Mercedes Benz',
        'Sprinter',
        2020,
        'EURO6',
        2200,
        160,
        '34343434-3434-3434-3434-343434343434'
    ),
    (
        '46464646-4646-4646-4646-464646464646',
        'VINE00000001',
        'Volvo',
        'FH',
        2017,
        'EURO6',
        10000,
        500,
        '45454545-4545-4545-4545-454545454545'
    ),
    (
        '57575757-5757-5757-5757-575757575757',
        'VINNONE00001',
        'Renault',
        'Zoe',
        2022,
        'ELECTRIC',
        1,
        108,
        '56565656-5656-5656-5656-565656565656'
    );

INSERT INTO insurance_policies (
    id,
    car_id,
    provider,
    start_date,
    end_date,
    status,
    paid_amount
) VALUES
    (
        '66666666-6666-6666-6666-666666666666',
        '33333333-3333-3333-3333-333333333333',
        'Groupama',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        1200.00
    ),
    (
        '77777777-7777-7777-7777-777777777777',
        '33333333-3333-3333-3333-333333333333',
        'Groupama',
        '2023-01-01',
        '2024-12-31',
        'EXPIRED',
        900.00
    ),
    (
        '88888888-8888-8888-8888-888888888888',
        '44444444-4444-4444-4444-444444444444',
        'Allianz',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        900.00
    ),
    (
        '99999999-9999-9999-9999-999999999999',
        '44444444-4444-4444-4444-444444444444',
        'Allianz',
        '2023-01-01',
        '2024-12-31',
        'EXPIRED',
        900.00
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        '55555555-5555-5555-5555-555555555555',
        'Generali',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        900.00
    ),
    (
        'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
        '55555555-5555-5555-5555-555555555555',
        'Allianz',
        '2023-01-01',
        '2024-12-31',
        'EXPIRED',
        900.00
    ),
    (
        'abababab-abab-abab-abab-abababababab',
        '13131313-1313-1313-1313-131313131313',
        'Omniasig',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        650.00
    ),
    (
        'bcbcbcbc-bcbc-bcbc-bcbc-bcbcbcbcbcbc',
        '24242424-2424-2424-2424-242424242424',
        'Generali',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        3200.00
    ),
    (
        'cdcdcdcd-cdcd-cdcd-cdcd-cdcdcdcdcdcd',
        '35353535-3535-3535-3535-353535353535',
        'Allianz',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        2100.00
    ),
    (
        'dededede-dede-dede-dede-dededededede',
        '46464646-4646-4646-4646-464646464646',
        'Groupama',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        4100.00
    ),
    (
        'efefefef-efef-efef-efef-efefefefefef',
        '57575757-5757-5757-5757-575757575757',
        'Omniasig',
        '2025-01-01',
        '2027-12-31',
        'ACTIVE',
        800.00
    );

INSERT INTO claims (
    id,
    car_id,
    claim_date,
    description,
    amount
) VALUES
    (
        'cccccccc-cccc-cccc-cccc-cccccccccccc',
        '44444444-4444-4444-4444-444444444444',
        '2024-04-08',
        'Minor front bumper damage',
        1200.00
    ),
    (
        'dddddddd-dddd-dddd-dddd-dddddddddddd',
        '33333333-3333-3333-3333-333333333333',
        '2024-08-19',
        'Broken windshield',
        2500.00
    ),
    (
        'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
        '33333333-3333-3333-3333-333333333333',
        '2024-03-23',
        'Rear end collision repair',
        3500.00
    ),
    (
        'fafafafa-fafa-fafa-fafa-fafafafafafa',
        '13131313-1313-1313-1313-131313131313',
        '2024-05-12',
        'Side mirror replacement',
        300.00
    ),
    (
        'fbfbfbfb-fbfb-fbfb-fbfb-fbfbfbfbfbfb',
        '24242424-2424-2424-2424-242424242424',
        '2024-09-14',
        'Cargo door repair',
        1800.00
    ),
    (
        'fcfcfcfc-fcfc-fcfc-fcfc-fcfcfcfcfcfc',
        '35353535-3535-3535-3535-353535353535',
        '2024-10-02',
        'Passenger step damage',
        950.00
    ),
    (
        'fdfdfdfd-fdfd-fdfd-fdfd-fdfdfdfdfdfd',
        '57575757-5757-5757-5757-575757575757',
        '2024-11-18',
        'Charging port replacement',
        700.00
    );
