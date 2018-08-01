from datetime import datetime
from pony.orm import *

db = Database("sqlite", "database.sqlite", create_db=True)

class Client(db.Entity):
    _table_ = "clients"
    id = PrimaryKey(int, auto=True)
    name = Required(str, 150)
    email = Required(str)
    password = Required(str, 100)
    modify = Required(datetime)
    created = Required(datetime)

sql_debug(True)

db.generate_mapping(create_tables=True)

@db_session
def add_client():
    client = Client(
        name="Test", email="test@email.com", password='test', modify=datetime.now(),
        created=datetime.now()
    )
add_client()

@db_session
def select_clients():
    print("--- select ---")
    return select(c for c in Client)[:]

@db_session
def insert_clients(Object, values):
    print("--- insert ---")
    object = Object(**values)
    return object

@db_session
def update_client(Object, id, values):
    print("--- update ---")
    client = Client.get(id=id)
    if values['name']:
        client.name = values['name']

@db_session
def delete_object(object, id):
    print("--- delete ---")
    object.get(id=id).delete() if object.get(id=id) else None

# insert
client = insert_clients(Client, {
    'name': 'Willem', 'email': 'willemarf@gmail.com', 'password': 'senha', 
    'modify': datetime.now(), 'created': datetime.now()
})
print(client.id)

# update
client = update_client(Client, 1,{
    'name': 'Wendell', 'email': 'wendellmrf@gmail.com', 'password': 'senha', 
    'modify': datetime.now(), 'created': datetime.now()
})

# delete
delete_object(Client, 4)

# select
clients = select_clients()
print('id | name | email | created')
for c in clients:
    print(c.id, ' | ', c.name, ' | ', c.email, ' | ', c.created)

with db_session:
    for q in select(c for c in Client).filter(lambda: c.name == 'Wendell'):
        print(q.id, q.name)