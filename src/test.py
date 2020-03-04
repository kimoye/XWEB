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

        # for k,v in attrs.items():
        #     if isinstance(v,Field):
        #         mapping[k] = v
        #         if v.primaryKey
        #             if primaryKey:
        #                 raise RuntimeError('Double primarykey found:{},{}'.format(primaryKey, v.primaryKey))
        #             else:
        #                 primaryKey = k
        #         else:
        #             fields.append[k]

        # if not primaryKey: raise RuntimeError('No primarykey')
        for k,v in attrs.items():
            mapping[k] = v
            print(k,v)
            if isinstance(v, dict):
                print(k,v)

        # for k in mapping.keys():
        #     print(k)
        #     attrs.pop(k)

        # 以下都是要返回的东西了，刚刚记录下的东西，如果不返回给这个类，又谈得上什么动态创建呢？
        # 到此，动态创建便比较清晰了，各个子类根据自己的字段名不同，动态创建了自己
        # 下面通过attrs返回的东西，在子类里都能通过实例拿到，如self
        # attrs['__mapping__'] = mapping
        # attrs['__table__'] = tableName
        # attrs['__primaryKey__'] = primaryKey
        # attrs['__fields__'] = fields
        # 只是为了Model编写方便，放在元类里和放在Model里都可以
        # attrs['__select__'] = "select %s ,%s from %s " % (primaryKey,','.join(map(lambda f: '%s' % (mapping.get(f).name or f ),fields )),tableName)
        # attrs['__update__'] = "update %s set %s where %s=?"  % (tableName,', '.join(map(lambda f: '`%s`=?' % (mapping.get(f).name or f), fields)),primaryKey)
        # attrs['__insert__'] = "insert into %s (%s,%s) values (%s);" % (tableName,primaryKey,','.join(map(lambda f: '%s' % (mapping.get(f).name or f),fields)),create_args_string(len(fields)+1))
        # attrs['__delete__'] = "delete from %s where %s= ? ;" % (tableName,primaryKey)
        return type.__new__(cls,name,bases,attrs)      

class lym(dict, metaclass = ModelMetaCls):
    def __init__(self):
        self.primaryKey1 = 1222
    
    def llljj(self):
        print('fuckllljjj')
    aaaf = dict()
if __name__ == '__main__':
    pab = lym()
    

    