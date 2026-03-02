from app.db.connection import get_conn

DDL = """
        CREATE TABLE IF NOT EXISTS hotels (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        city VARCHAR(50) NOT NULL,
        address VARCHAR(100) NOT NULL,
        stars FLOAT NOT NULL CHECK (stars BETWEEN 1 AND 5)
        );
            
        CREATE TABLE IF NOT EXISTS room_type (
            id BIGSERIAL PRIMARY KEY,
            type_name VARCHAR(50) NOT NULL UNIQUE
        );
        
        CREATE TABLE IF NOT EXISTS room (
            id BIGSERIAL PRIMARY KEY,
            h_id BIGINT NOT NULL,
            room_number TEXT NOT NULL,
            r_t_id BIGINT NOT NULL,
            capacity INT NOT NULL CHECK (capacity > 0),
            price_per_day FLOAT NOT NULL CHECK (price_per_day > 0),
            floor INT NOT NULL CHECK (floor >= 0),
            CONSTRAINT fk_room_hotel FOREIGN KEY (h_id) REFERENCES hotels(id) ON DELETE CASCADE,
            CONSTRAINT fk_room_type FOREIGN KEY (r_t_id) REFERENCES room_type(id)
        );
    
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL CHECK (length(password) >= 8),
            role VARCHAR(10) NOT NULL CHECK (role IN ('USER', 'ADMIN')) DEFAULT 'USER'
        );
            
        CREATE TABLE IF NOT EXISTS booking (
            id BIGSERIAL PRIMARY KEY,
            r_id BIGINT NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            status VARCHAR(10) NOT NULL CHECK (status IN ('confirmed', 'pending', 'completed', 'canceled')),
            user_id BIGINT NOT NULL,
            CONSTRAINT fk_booking_room FOREIGN KEY (r_id) REFERENCES room(id) ON DELETE CASCADE,
            CONSTRAINT fk_booking_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
            
        CREATE INDEX IF NOT EXISTS idx_booking_room_dates
        ON booking (r_id, check_in, check_out);
            
        CREATE INDEX IF NOT EXISTS idx_booking_user
        ON booking (user_id);
            
        """

def migrate():
    statements =[s.strip() for s in DDL.split(';') if s.strip()]
    with get_conn() as conn:
        for s in statements:
            conn.execute(s)
if __name__ == "__main__":
    migrate()
    print("Migration completed successfully")


