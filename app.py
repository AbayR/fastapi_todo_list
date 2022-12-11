from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/contact/")
def contact(request: Request, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).all()
    return templates.TemplateResponse("contact.html",
                                      {"request": request, "todo_list": contact})

@app.post("/add")
def add(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Contact(name=name, email=email, message=message)
    db.add(new_todo)
    db.commit()

    url = app.url_path_for("contact")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

