import asyncpg
import asyncio


DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"


async def create_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
                       CREATE TABLE IF NOT EXISTS todoList (
                           id SERIAL PRIMARY KEY,
                           title TEXT,
                           description TEXT,
                           completed BOOLEAN DEFAULT FALSE
                       )
                       ''')
    await conn.close()


async def create_users_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(16) UNIQUE NOT NULL
        )
    ''')
    await conn.close()


async def update_todolist():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute('''
                     ALTER TABLE todoList
                     ADD COLUMN IF NOT EXISTS user_id INTEGER
                     ''')
    except Exception as e:
        print(e)

    try:
        await conn.execute("""
                     ALTER TABLE todoList
                     ADD CONSTRAINT fk_todo_user
                     FOREIGN KEY (user_id)
                     REFERENCES users(id)
                     ON DELETE CASCADE
                     """)
    except Exception as e:
        print(e)

    columns = await conn.fetch('''
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'todolist'
        ORDER BY ordinal_position
    ''')
    
    print("\n   Структура todoList:")
    for col in columns:
        print(f"     - {col['column_name']}: {col['data_type']}")
    
    await conn.close()
    print("\n🎉 Таблица todoList обновлена!")

asyncio.run(update_todolist())
