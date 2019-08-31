import sqlite3


def check_filds(method_to_decorate):
    """
    Декоратор проверяющий, что все элементы множества args (переданные имена
    колонок) принадлежат множеству _filds (имена колонок таблицы)
    """
    def wrapper(self, *args, **kwargs):
        if not set(args).issubset(self._filds):
            raise AttributeError
        
        if kwargs and not set(kwargs['filds'].keys()).issubset(self._filds):
            raise AttributeError

        return method_to_decorate(self, *args, **kwargs)
    return wrapper


def shielding():
    """
    Экранированиие значений для строки запроса
    """
    return lambda val :"'{}'".format(val)


class BaseORM():
    
    def __init__(self, *args, **kwargs):
        self._table = self.__tablename__
        self._filds = {fild for fild in self.__class__.__dict__.keys() 
                        if not fild.startswith('__')}
        self._sql_text = None
        self.connect = None

    def execute(self):
        
        cursor = self.connect.cursor()
        try:
            cursor.execute(self._sql_text)
            self.connect.commit()
        except Exception as e:
            print(f'Request Execution Error: {e}')
        
        return cursor.fetchall()      
        
    @check_filds
    def select(self, *args):
        filds = args or self._filds
        self._sql_text = 'SELECT {} FROM {}'.format(', '.join(filds), self._table)
        return self

    @check_filds
    def insert(self, **kwargs):
        filds = kwargs['filds']
        self._sql_text = "INSERT INTO {} ({}) VALUES ({})".format(
                                    self._table, 
                                    ', '.join(filds.keys()), 
                                    ', '.join(map(shielding(), filds.values()))
                                                                    )
        return self

    @check_filds
    def update(self, **kwargs):
        key_value = [f"{k} = '{v}'" for k,v in kwargs['filds'].items()]
        filds = ', '.join(key_value) 
        self._sql_text = f'UPDATE {self._table} SET {filds}'
        return self

    def where(self, fild, value, compare='='):  
        self._sql_text = f'{self._sql_text} WHERE {fild} {compare} {value}'
        return self

    def create_table(self):
        filds = [f'{fild} {getattr(self, fild)}' for fild in self._filds]
        try:
            cursor = self.connect.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(self._table,', '.join(filds)))
        except Exception as e:
            print(f'Error creating table: {e}')        
    
    def delete_table(self):
        #не знаю, нужен ли тут квалификаторов базы или достаточно 
        #соединения чтобы удалить таблицу из конкретной базы 
        try:
            cursor = self.connect.cursor()
            cursor.execute('DROP TABLE IF EXISTS {}'.format(self._table))
        except Exception as e:
            print(f'Error delete table: {e}')  

    def delete(self):
        self._sql_text = f'DELETE FROM {self._table}'
        return self

    def connection(self, name_db):
        try:
            con = sqlite3.connect("mydatabase.db")
        except Exception as e:
            print(f'Error connect db: {e}')
            raise Exception
        else:
            self.connect = con

