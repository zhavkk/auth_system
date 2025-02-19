CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL, 
    email VARCHAR(255) UNIQUE NOT NULL,    
    password_hash TEXT,                    
    yandex_id VARCHAR(255) UNIQUE,         
    vk_id VARCHAR(255) UNIQUE,             
    role_id INT NOT NULL,                  
    first_name VARCHAR(255),               
    last_name VARCHAR(255),                
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE auth_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(100),
    success BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO roles (name, description) VALUES ('admin', 'Администратор');
INSERT INTO roles (name, description) VALUES ('user', 'Пользователь');