# 编译错误

1. STL模板函数使用错误

   ```shell
   查找字符串 "In instantiation",即可得到什么地方实例化出错
   ```

   错误信息讲解

   ```shell
   # 实例化函数std::__find 模板参数是...
   /usr/include/c++/4.8.2/bits/stl_algo.h: In instantiation of ‘_RandomAccessIterator std::__find(_RandomAccessIterator, _RandomAccessIterator, const _Tp&, std::random_access_iterator_tag) [with _RandomAccessIterator = __gnu_cxx::__normal_iterator<_Synopsis*, std::vector<_Synopsis> >; _Tp = OuterFactoryImp::achieveLoopRotation(int)::__lambda2]’:
   
   
   # 实例化函数std::find 模板参数是...
   /usr/include/c++/4.8.2/bits/stl_algo.h:4441:45:   required from ‘_IIter std::find(_IIter, _IIter, const _Tp&) [with _IIter = __gnu_cxx::__normal_iterator<_Synopsis*, std::vector<_Synopsis> >; _Tp = OuterFactoryImp::achieveLoopRotation(int)::__lambda2]’
   
   OuterFactoryImp.h:135:5:   required from here
   
   # 找不到函数...
   /usr/include/c++/4.8.2/bits/stl_algo.h:166:17: error: no match for ‘operator==’ (operand types are ‘_Synopsis’ and ‘const OuterFactoryImp::achieveLoopRotation(int)::__lambda2’)
   
   # ===》传入的参数有问题
   ```

2. 单步调试代码走的次序不对--->出现了异常

3. 有返回值的函数，不return 值会crash，因此任何函数都要有return语句





# 异常处理

1. 访问越界

   ```c++
   try
   {
       try
       {
           std::map<int, int> m;
           m[1] = 11;
           m[2] = 22;
           m[3] = 33;
           std::cout << m.at(5) << endl; //at函数越界会抛出异常
       }
       catch (std::out_of_range& e)
       {
           stringstream os;
           os << __FILE__ << ":" << __LINE__ << ":" << __FUNCTION__;//设置异常信息,如果是函数,需要记录传入的参数和一些关键数据
           string msg = os.str();
           throw out_of_range(msg);//重新抛出异常
       }
   }
   catch (const std::exception& e)
   {
       cout << "error info : " << e.what() << endl;//最外层打印异常信息,据此查找程序的问题
   }
   ```

   