# 一、zeromq介绍

zeromq 是一种进程间通信的方式，不需要用户处理底层的拆包，组包的问题





# 二、三种基本模型



## 2.1 Request-Reply（请求-回复）



### 描述

***

1. 以 “Hello World” 为例。客户端发起请求，并等待服务端回应请求。客户端发送一个简单的 “Hello”，服务端则回应一个 “World”。可以有 N 个客户端，一个服务端，因此是 1-N 连接。

2. 服务端和客户端无论谁先启动，效果是相同的，这点不同于 Socket。
3. 在服务端收到信息以前，程序是阻塞的，会一直等待客户端连接上来。
4. 服务端收到信息后，会发送一个 “World” 给客户端。值得注意的是一定是客户端连接上来以后，发消息给服务端，服务端接受消息然后响应客户端，这样一问一答。
5. ZMQ 的通信单元是消息，它只知道消息的长度，并不关心消息格式。因此，你可以使用任何你觉得好用的数据格式，如 Xml、Protocol Buffers、Thrift、json 等等。

![](img\req-rep.webp)

### 代码

***

1. 服务端代码

   ```python
   import time
   import zmq
   context = zmq.Context()
   socket = context.socket(zmq.REP)
   socket.bind("tcp://*:5555")
   while True:
       message = socket.recv()
       print("Received request: %s" % message)
       # Do some 'work'
       time.sleep(1)
       socket.send(b"World")
   ```

2. 客户端代码

   ```python
   import zmq
   context = zmq.Context()
   print("Connecting to hello world server...")
   socket = context.socket(zmq.REQ)
   socket.connect("tcp://localhost:5555")
   for request in range(10):
       print("Sending request %s ..." % request)
       socket.send(b"Hello")
       message = socket.recv()
       print("Received reply %s [ %s ]" % (request,message))
   ```

   



## 2.2 Publish-Subscribe（发布-订阅）



### 描述

***

1. 客户端需要设置一个过滤条件，接收自己感兴趣的消息。
2. 发布者一直不断地发布新消息，如果中途有订阅者退出，其他均不受影响。当订阅者再连接上来的时候，收到的就是后来发送的消息了。这样比较晚加入的或者是中途离开的订阅者必然会丢失掉一部分信息。这是该模式的一个问题，即所谓的 "Slow joiner" 。



![](img\pub.webp)

### 代码

***

1. 服务端代码

   ```python
   from random import randrange
   import zmq
   context = zmq.Context()
   socket = context.socket(zmq.PUB)
   socket.bind("tcp://*:5556")
   while True:
       zipcode = randrange(1, 100000)
       temperature = randrange(-80, 135)
       relhumidity = randrange(10, 60)
       socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
   ```

   

2. 客户端代码

   ```python
   import sys
   import zmq
   context = zmq.Context()
   socket = context.socket(zmq.SUB)
   print("Collecting updates from weather server...")
   socket.connect("tcp://localhost:5556")
   zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
   if isinstance(zip_filter, bytes):
       zip_filter = zip_filter.decode('ascii')
   socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)
   total_temp = 0
   for update_nbr in range(5):
       string = socket.recv_string()
       zipcode, temperature, relhumidity = string.split()
       total_temp += int(temperature)
   print("Average temperature for zipcode '%s' was %dF" % (zip_filter, total_temp / (update_nbr + 1)))
   ```

   

## 2.3 Parallel Pipeline



### 描述

***

1. ventilator 分发任务到各个 worker
2. 每个 worker 执行分配到的任务
3. 最后由 sink 收集从 worker 发来的结果



![](img\pipe.webp)

### 代码

***

1. taskvent.py

   ```python
   import zmq
   import time
   import random
   try:
       raw_input
   except NameError:
       raw_input = input
   context = zmq.Context()
   sender = context.socket(zmq.PUSH)
   sender.bind("tcp://*:5557")
   sink = context.socket(zmq.PUSH)
   sink.connect("tcp://localhost:5558")
   print("Please enter when workers are ready: ")
   _ = raw_input()
   print("Sending tasks to workers...")
   sink.send(b'0')
   random.seed()
   total_msec = 0
   for task_nbr in range(100):
       workload = random.randint(1, 100)
       total_msec += workload
       sender.send_string(u'%i' % workload)
   print("Total expected cost: %s msec" % total_msec)
   time.sleep(1)
   ```

2. taskwork.py

   ```python
   import zmq
   import time
   import sys
   context = zmq.Context()
   receiver = context.socket(zmq.PULL)
   receiver.connect("tcp://localhost:5557")
   sender = context.socket(zmq.PUSH)
   sender.connect("tcp://localhost:5558")
   while True:
       s = receiver.recv()
       sys.stdout.write('.')
       sys.stdout.flush()
       time.sleep(int(s) * 0.001)
       sender.send(b'')
   ```

3. tasksink.py

   ```python
   import time
   import zmq
   import sys
   context = zmq.Context()
   receiver = context.socket(zmq.PULL)
   receiver.bind("tcp://*:5558")
   s = receiver.recv()
   tstart = time.time()
   for task_nbr in range(1, 100):
       s = receiver.recv()
       if task_nbr % 10 == 0:
           sys.stdout.write(':')
       else:
           sys.stdout.write('.')
       sys.stdout.flush()
   tend = time.time()
   print("Total elapsed time: %d msec" % ((tend - tstart) * 1000))
   ```

   