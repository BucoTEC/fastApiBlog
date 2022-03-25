from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return({'message':'welcome to fastAPI'})


@app.get('/about')
def about():
    return ({'data':{ 'message': 'The about page'}})


@app.get('/blog/{id}')
def get_post(id : int):
    return ({'data':{'message':f'your path param is {id}'}})
