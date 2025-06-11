from fastapi import FastAPI, Request, Response, status
import uvicorn
from jsonschema import validate, ValidationError
import csv
import json
import datetime 

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/wishlist")
async def add_to_wishlist(request: Request, response: Response):
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "author": {"type": "string"}
        },
        "required": ["title", "author"]
    }

    body = await request.json()
    print(json.dumps(body, indent=2, default=str))

    is_valid = False
    try: 
        validate(instance = body, schema = schema)
        is_valid = True
        print("data is valid")
    except ValidationError as e:
        error_msg = f"Data not valid. {e}"
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": error_msg, 
                "is_valid": is_valid}
    
    # TODO: Use a database and not a csv
    try:
        with open("wishlist.csv", "x") as file:
            print("file does not exist")
            instance = csv.writer(file)
            instance.writerow(["Title", "Author", "Date Added"])
            instance.writerow([body["title"], body["author"], datetime.date.today()])
    except FileExistsError:
        print("File already exists.")
        with open("wishlist.csv", "a") as file:
            instance = csv.writer(file)
            instance.writerow([body["title"], body["author"], datetime.date.today()])

    response.status_code = status.HTTP_201_CREATED
    return {"message": "item added to wishlist"}

@app.get("/wishlist")
async def get_wishlist(request: Request, response: Response):
    try:
        data = []
        with open("wishlist.csv", "r") as file:
            instance = csv.DictReader(file)
            for row in instance:
                data.append(row)
        
        response.status_code = status.HTTP_202_ACCEPTED
        return {json.dumps(data, indent=None)}
    except FileNotFoundError as e:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)