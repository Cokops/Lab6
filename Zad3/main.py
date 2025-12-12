from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import models  
from database import engine, get_db, SessionLocal 
from pydantic import BaseModel
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class NoteCreate(BaseModel):
    title: str
    text: Optional[str] = None

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None

class Note(NoteCreate):
    id: int
    
    class Config:
        orm_mode = True  


@app.get("/notes", response_model=List[Note])
def get_all(db: Session = Depends(get_db)):
    notes = db.query(models.NoteDB).all()
    return notes

@app.get("/notes/{note_id}", response_model=Note)
def get_note_id(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.NoteDB).filter(models.NoteDB.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail=f"Заметка {note_id} не найдена")
    return note

@app.post("/notes", response_model=Note)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = models.NoteDB(title=note.title, text=note.text)
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)  
    
    return db_note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: int, note_update: NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(models.NoteDB).filter(models.NoteDB.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail=f"Заметка {note_id} не найдена")
    
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.text is not None:
        db_note.text = note_update.text
    
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.NoteDB).filter(models.NoteDB.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail=f"Заметка {note_id} не найдена")
    
    db.delete(db_note)
    db.commit()
    
    return {"message": f"Заметка {note_id} удалена"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)