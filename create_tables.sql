CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    device VARCHAR(255) NOT NULL,
    sensor_type VARCHAR(255) NOT NULL,
    sensor_value VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT current_timestamp
);
CREATE TABLE rules (
    rule_id SERIAL PRIMARY KEY,
    device VARCHAR(255) NOT NULL,
    sensor_type VARCHAR(255) NOT NULL,
    operator enum(E, NE, G, NG, EG, NEG, L, NL, EL, NEL) NOT NULL,
    /*
    E - Equal
    G - Greater
    L - Less
    N - Not
    */
    unusual_value VARCHAR(255) NOT NULL,
    compare_to_last_event BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT current_timestamp
);