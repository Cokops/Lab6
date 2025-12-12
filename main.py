from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class NewWeapon(BaseModel):
    name: str
    calibre: str

weapons = [
    {
        "id": 1,           
        "name": "AR-15",   
        "calibre": "5.56", 
    },
    {
        "id": 2,
        "name": "AK-12",
        "calibre": "5.45",
    }   
]

@app.get("/weapons",tags=["Оружия"],summary="Получить весь список оружия.")
def read_weapons():
    return weapons

@app.get("/weapons/{weapon_id}",tags=["Оружия"],summary="Получить оружие по ID.")
def get_weapons(weapon_id: int):
    for weapon in weapons:
        if weapon["id"] == weapon_id:
            return weapon
    raise HTTPException(status_code=404,detail="Не найдено!")


@app.post("/weapons")
def add_weapons(new_weapon:NewWeapon):
    weapons.append(
        {
        "id":len(weapons) + 1,
        "name":new_weapon.name,
        "calibre":new_weapon.calibre,
    })
    return {"succes":True}



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)