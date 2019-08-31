from MyORM import BaseORM


class MyTable(BaseORM):
    __tablename__ = "wtf"

    id = ("int")
    name = ("str")
    soname = ("str")
    age = "int"
    

if __name__ == "__main__":
    #пример использования
    test = MyTable()
    test.connection("mydatabase.db")
    test.create_table()
    test.insert(filds={"id":1,"age":20,"name":"Vasya","soname":"Vasilev"}).execute()
    test.insert(filds={"id":2,"age":30,"name":"Ivan","soname":"Ivanov"}).execute()
    rezult = test.select('id','name', 'age').execute()
    print(rezult)   
    test.update(filds={"name":"Petya"}).where('id',1).execute()
    test.delete().where('id',2).execute()
    rezult = test.select('id','name', 'soname','age').where('id',1).execute()
    print(rezult)
    test.delete_table()
