from fastapi import BackgroundTasks, FastAPI


app = FastAPI()


def write_noticication(email: str, msg=''):
    with open('log.txt', mode='a') as email_file:
        content = f"notification for {email}: {msg}\n"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_noticication, email,
                              msg='some notification')
    return {"message": "Notification sent in the background"}
