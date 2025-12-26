import asyncpg
import asyncio


DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"


async def create_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
            completed_at TIMESTAMPTZ DEFAULT NULL
        );
    ''')

    await conn.execute('''
        CREATE OR REPLACE FUNCTION set_completed_at()
        RETURNS TRIGGER AS $$
        BEGIN
            IF NEW.completed = TRUE THEN
                NEW.completed_at = CURRENT_TIMESTAMP;
            ELSE
                NEW.completed_at = NULL;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    ''')
    await conn.execute('DROP TRIGGER IF EXISTS trigger_completed_at ON todos;')
    await conn.execute('''
        CREATE TRIGGER trigger_completed_at
        BEFORE UPDATE ON todos
        FOR EACH ROW
        WHEN (OLD.completed IS DISTINCT FROM NEW.completed)
        EXECUTE FUNCTION set_completed_at();
    ''')

    await conn.close()

asyncio.run(create_table())
