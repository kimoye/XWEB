import asyncio, aiomysql

#本来想用sqlite，毕竟轻量级。最后因为其无法异步以及mysql有现成的代码可以参考
#故选用可以异步的mysql
#连接池建立函数后期再修改 部署的时候参数得改改
async def create_pool(loop, **kw):
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],                                        #数据库用户名
        password=kw['password'],                                #对应用户密码
        db=kw['db'],                                            #表名？maybe
        charset=kw.get('charset', 'utf8'),                      #字符集
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),                          #最大链接数
        minsize=kw.get('minsize', 1),                           #最小连接数
        loop=loop
    )

async def select(sql, args, size=None):
    global __pool

    #下面打开线程池pool，为异步操作
    #此处语法经深度学习后 改正 按道理with yeild from 等效于  with await
    #但是aiomysql官方sample以及PEP为 async with ，这的确更容易想通：上下文管理器嘛~
    #但是若是with await很矛盾他是什么东西 上下文管理器？

    async with __pool.acquire() as conn: 
        #DictCursor 字典形式的游标                       
        cur = await conn.cursor()
        await cur.excute(sql.replace('?','%s'), args or ())
        #输出信息
        print(cur.description)
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        #输出获取的列数
        print('rows returned: %s' % len(rs))
        return rs

async def execute(sql, args):
    global __pool
    print(sql)
    async with __pool as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise  e
        return affected

#***********************************************************#
#                  以上为数据库操作函数                       #
#                  以下为ORM中元类的代码                      #
#***********************************************************#
class ModelMetaCls(type):
    def __new__(cls,name,bases,attrs):
        if name == "Model":
            print('base class:{}'.format(name))
            return type.__new__(cls,name,bases,attrs)

        tableName = name or attrs.get('__table__', None)

        print('create table\'s class:{}<-->{}'.format(name, tableName))
        
        mapping = dict()
        fields = []
        primaryKey = None

        for k,v in attrs.items():
            if isinstance(v,Field):
                mapping[k] = v
                if v.primaryKey
                    if primaryKey:
                        raise RuntimeError('Double primarykey found:{},{}'.format(primaryKey, v.primaryKey))
                    else:
                        primaryKey = k
                else:
                    fields.append[k]

        if not primaryKey: raise RuntimeError('No primarykey')

        for k in mapping.keys():
            attrs.pop(k)

        # 以下都是要返回的东西了，刚刚记录下的东西，如果不返回给这个类，又谈得上什么动态创建呢？
        # 到此，动态创建便比较清晰了，各个子类根据自己的字段名不同，动态创建了自己
        # 下面通过attrs返回的东西，在子类里都能通过实例拿到，如self
        attrs['__mapping__'] = mapping
        attrs['__table__'] = tableName
        attrs['__primaryKey__'] = primaryKey
        attrs['__fields__'] = fields
        # 只是为了Model编写方便，放在元类里和放在Model里都可以
        attrs['__select__'] = "select %s ,%s from %s " % (primaryKey,','.join(map(lambda f: '%s' % (mapping.get(f).name or f ),fields )),tableName)
        attrs['__update__'] = "update %s set %s where %s=?"  % (tableName,', '.join(map(lambda f: '`%s`=?' % (mapping.get(f).name or f), fields)),primaryKey)
        attrs['__insert__'] = "insert into %s (%s,%s) values (%s);" % (tableName,primaryKey,','.join(map(lambda f: '%s' % (mapping.get(f).name or f),fields)),create_args_string(len(fields)+1))
        attrs['__delete__'] = "delete from %s where %s= ? ;" % (tableName,primaryKey)
        return type.__new__(cls,name,bases,attrs)      


class Model(dict, metaclass = ModelMetaCls):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise e
    def __setattr__(self, key, value):
        self[key] = value
    
  # 取默认值，字段(Field)类有一个默认值属性，默认值也可以是函数
    def getValueOrDefault(self,key): 
      value=getattr(self,key)
      if value is None:
          field=self.__mappings__[key]
          if field.default is not None:
              value=field.default() if callable(field.default) else field.default
              setattr(self,key,value)
      return value

# save fn
    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getVauleOrDefault(self.__primaryKey__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            print('failed to insert record: {} rows'.format(rows))
