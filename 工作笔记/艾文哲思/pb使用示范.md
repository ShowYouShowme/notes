## Proto文件

```protobuf
syntax = "proto3";
package tutorial;
message Goods
{
	int32 id = 1;
	int32 count = 2;
}
message Person {
  int32 id = 1;
  string name = 2;
  string email = 3;

  repeated string friendNames = 4;
	map<int32, int32> salary = 5;
	Goods		goods = 6;

	repeated Goods table = 7;
	map<int32, Goods> mg = 8;
}
```

## 成员是基本类型

1. 集合类型

   11. repeated 类型

       ```c++
       // 插入数据
       person.add_friendnames("Nash Jonh");
       // 遍历数据
       for (size_t i = 0; i < new_person.friendnames_size(); ++i)
       {
           string name = new_person.friendnames(i);
           cout << "name : " << name << endl;
       }
       ```

   12. map类型

       ```c++
       //插入数据
       auto ptr = person.mutable_salary();
       for (size_t i = 1; i < 15; ++i)
       {
           (*ptr)[i] = i * i;
       }
       
       //遍历数据
       for (auto it = new_person.salary().begin(); it != new_person.salary().end(); ++it)
       {
           int key = it->first;
           int value = it->second;
           cout << it->first << " : " << it->second << endl;
       }
       ```

       

2. 非集合类型

   ```c++
   // 读
   cout << "ID: " << new_person.id() << endl;
   
   // 写
   person.set_id(123456);
   ```

   

## 成员是自定义类型

1. 集合类型

   11. repeated类型

       ```c++
       // 写
       auto ptr = person.add_table();
       ptr->set_count(11);
       ptr->set_id(22);
       
       ptr = person.add_table();
       ptr->set_count(33);
       ptr->set_id(44);
       
       
       // 读
       auto& table = person.table();
       for (auto it = table.begin(); it != table.end(); ++it)
       {
           cout << it->count() << " : " << it->id() << endl;
       }
       ```

   12. map类型

       ```c++
       // 写
       auto mg = person.mutable_mg();
       tutorial::Goods goods;
       goods.set_count(999);
       goods.set_id(888);
       (*mg)[128] = goods;
       
       
       goods.set_count(666);
       goods.set_id(777);
       (*mg)[512] = goods;
       
       
       // 读
       auto& mg = person.mg();
       for (auto it = mg.begin(); it != mg.end(); ++it)
       {
           cout << "key : " << it->first << ", value : " << it->second.count() << " : " << it->second.id() << endl;
       }
       ```

       

2. 非集合类型

   ```c++
   // 写
   auto ptr = person.mutable_goods();
   ptr->set_count(96);
   ptr->set_id(156);
   
   // 读
   auto& goods = new_person.goods();
   cout << goods.count() << " : " << goods.id() << endl;
   ```

   