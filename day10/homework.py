from databases import Database
from fastapi import FastAPI, HTTPException, Query, status
from contextlib import asynccontextmanager
from pydantic import BaseModel
import datetime
from typing import Optional, List
from zoneinfo import ZoneInfo


DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"

database = Database(DATABASE_URL)


class TodoIn(BaseModel):
    title: str
    description: str


class TodoReturn(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
    created_at: datetime.datetime
    completed_at: datetime.datetime | None = None


class CompletedUpdate:
    id: int
    completed: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
input_data_pattern = r'\d{4}-\d{2}-\d{2}'


@app.post('/todos')
async def add_todo(todo: TodoIn):
    query = '''
            INSERT INTO todos (title, description)
            VALUES (:title, :description)
            RETURNING *
            '''
    res = await database.fetch_all(query=query,
                                   values=todo.model_dump(mode="json"))
    if res:
        return res
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.get('/todos', response_model=List[TodoReturn])
async def get_todos(offset: int = Query(default=0, ge=0),
                    limit: int = Query(ge=10, le=100),
                    sort_by: Optional[str | None] = None,
                    completed: Optional[bool] = None,
                    created_before: Optional[str | None] =
                    Query(default=None, pattern=input_data_pattern),
                    created_after: Optional[str | None] =
                    Query(default=None, pattern=input_data_pattern),
                    title_contains: Optional[str] = None
                    ):
    where_clauses = []
    order_by = []
    values = {}
    if completed is not None:
        where_clauses.append("completed = :completed")
        values["completed"] = completed

    if sort_by is not None:
        if sort_by.startswith('-'):
            field = sort_by[1:]
            direction = "DESC"
        else:
            field = sort_by
            direction = 'ASC'

        if field == 'created_at':
            order_by.append(f'created_at {direction}')
        elif field == 'title':
            order_by.append(f'title {direction}')
        elif field == 'completed_at':
            order_by.append(f'completed_at {direction}')

    if title_contains is not None:
        where_clauses.append("title ILIKE :title_contains")
        values["title_contains"] = f'%{title_contains}%'

    if created_after is not None:
        where_clauses.append("created_at >= :created_after")
        values["created_after"] = created_after + " 00:00:00"

    if created_before is not None:
        where_clauses.append("created_at <= :created_before")
        values["created_before"] = created_before + " 23:59:59"

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    values['offset'] = offset
    values['limit'] = limit
    order_by_sql = ""
    if order_by:
        order_by_sql = "ORDER BY " + ", ".join(order_by)
    query = f"""
            SELECT * FROM todos
            {where_sql}
            {order_by_sql}
            LIMIT :limit OFFSET :offset
            """
    try:
        result = await database.fetch_all(query=query, values=values)
        if not result:
            return []
    except Exception as e:
        print(e)


@app.get('/todos/analytics')
async def get_analytics(tz: str =
                        Query(default='Europe/Moscow')):
    try:
        ZoneInfo(tz)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    anal = {}
    all_task = await database.fetch_val(
        "SELECT COUNT(*) FROM todos"
    )
    if all_task:
        anal['total'] = all_task

    avg_completed = await database.fetch_val("""
            SELECT AVG(EXTRACT(EPOCH FROM (completed_at - created_at)) / 3600)
            FROM todos
            WHERE completed = true
                                       """)
    if avg_completed:
        anal['avg_completion_time_hours'] = avg_completed

    completed_stats = await database.fetch_all('''
                      SELECT completed, COUNT(*)
                      FROM todos
                      GROUP BY completed;
                      ''')
    if completed_stats:
        completed_stats = {str(row['completed']).lower(): row['count'] for row
                           in completed_stats}
        anal["completed_stats"] = completed_stats

    query = """
            SELECT EXTRACT(DOW FROM created_at AT TIME ZONE :tz)
            as day_index, COUNT(*)
            FROM todos
            GROUP BY day_index
            ORDER BY day_index;
            """
    weekday_distribution = await database.fetch_all(query=query,
                                                    values={'tz': tz})
    days_names = {
                    0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday",
                    4: "Thursday", 5: "Friday", 6: "Saturday"
                 }
    distribution = {name: 0 for name in days_names.values()}
    for row in weekday_distribution:
        day_name = days_names[int(row['day_index'])]
        distribution[day_name] = row['count']
    anal['weekday_distribution'] = distribution
    return anal


@app.patch('/todos')
async def patch_completed(ids: list[int] = Query(default=[]),
                          completed: bool = Query(default=True)):
    if not ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    query = '''
            UPDATE todos t
            SET completed = :completed
            WHERE id = ANY(:ids)
            RETURNING id
            '''
    res = await database.fetch_all(query=query,
                                   values={
                                            'ids': ids,
                                            'completed': completed
                                           })
    return {'updated_count': len(res)}
