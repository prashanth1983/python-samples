#pip install fastapi uvicorn
import uvicorn
from fastapi import FastAPI 

app = FastAPI()

@app.get('/')
def index():
    return {'message' : 'Hello word'}

@app.get('/Welcome')
def get_name(name: str):
    return {'Welcome to Prashanth you tube channel' : f'{name}'}



if __name__ =='__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

#use below command to run
#uvicorn main:app --reload
#http://127.0.0.1:8000/
#http://127.0.0.1:8000/Welcome?name=Prashanth