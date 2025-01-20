# 第一章 安装

集群使用一个Master节点和两个Node节点



## 1.1 提前准备

1. 设置主机名

   ```ini
   ;Master节点操作
   cmd = hostnamectl set-hostname Kubernetes-Master 
   
   ;Node1节点操作
   cmd = hostnamectl set-hostname Kubernetes-Node1 
   
   ;Node2节点操作
   cmd = hostnamectl set-hostname Kubernetes-Node2  
   ```

2. Master节点添加hosts

   ```shell
   cat >> /etc/hosts << EOF
   192.168.1.10 kubernetes-master
   192.168.1.11 kubernetes-node1
   192.168.1.12 kubernetes-node2
   EOF
   ```

3. 以下操作三个节点都执行

   + 关闭系统防火墙

     ```shell
     systemctl stop firewalld
     systemctl disable firewalld
     ```

   + 关闭selinux

     ```shell
     sed -i 's/enforcing/disabled/' /etc/selinux/config  
     ```

   + 关闭swap

     ```shell
     sed -ri 's/.*swap.*/#&/' /etc/fstab
     ```

   + 将桥接的IPv4流量传递到iptables的链

     ```shell
     cat > /etc/sysctl.d/k8s.conf << EOF
     net.bridge.bridge-nf-call-ip6tables = 1
     net.bridge.bridge-nf-call-iptables = 1
     EOF
     
     # 执行命令sysctl --system 使其生效
     ```

   + 重启机器



## 1.2 安装docker

docker好像有版本需求，下次使用指定版本试试看

1. 安装Docker：参考Docker文档

2. 配置Docker

   vim /etc/docker/daemon.json

   ```shell
   {"exec-opts": ["native.cgroupdriver=systemd"  ],"registry-mirrors": ["http://docker-registry-mirror.kodekloud.com"  ]}
   ```

3. 启动docker服务

   ```shell
   systemctl enable docker
   systemctl start docker
   ```

   

   

   

   ## 1.3 安装Kubernetes

   1. 创建yum仓库

      ```shell
      cd /etc/yum.repos.d/
      
      cat > kubernetes.repo << EOF
      [Kubernetes]
      name=kubernetes Release
      baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
      enabled=1
      gpgcheck=0
      EOF
      
      yum makecache
      ```

   2. 安装Kubernetes组件

      ```shell
      yum install -y kubelet-1.23.0 kubeadm-1.23.0 kubectl-1.23.0
      ```

   3. 将Kubernetes代理服务设置为开机启动

      ```shell
      # 负责接受Master的命令并且执行
      systemctl enable kubelet
      ```

   4. 初始化Master节点

      ```shell
      kubeadm init --image-repository registry.aliyuncs.com/google_containers --pod-network-cidr=10.244.0.0/16
      ```

   5. 使用服务

      ```shell
      # 可以把该命令放到/etc/profile里面
      export KUBECONFIG=/etc/kubernetes/admin.conf
      ```

   6. Master安装网卡

      ```shell
      wget https://docs.projectcalico.org/v3.18/manifests/calico.yaml
      
      # 修改配置, 把 CALICO_IPV4POOL_CIDR 的 value 改为 "10.244.0.0/16"
      
      kubectl apply -f calico.yaml
      ```

   

## 1.3 Node节点加入集群

   1. 在master接点上生成加入命令

      ```shell
      kubeadm token create --print-join-command
      ```

   2. 把命令贴到node接点执行

   3. 在master接点查看node接点的状态

      ```shell
      kubectl get nodes
      ```

   

   

   ## 1.4 常见问题

1. 节点状态为NotReady

   出现这种情况常常是因为docker镜像未下载完成，解决方案如下

   + 查看各个节点的docker镜像列表

     ```shell
     docker image ls
     
     # 正常情况下应该有这几个
     registry.aliyuncs.com/google_containers/kube-proxy   v1.23.17   f21c8d21558c   19 months ago   111MB
     calico/node                                          v3.18.6    13143ba4a4e2   2 years ago     173MB
     calico/pod2daemon-flexvol                            v3.18.6    3d0771521a98   2 years ago     21.7MB
     calico/cni                                           v3.18.6    1f4b3a79aa0e   2 years ago     131MB
     registry.aliyuncs.com/google_containers/pause        3.6        6270bb605e12   3 years ago     683kB
     ```

   + 给docker服务增加代理[docker 已经被封杀，正常网络无法访问]

2. node节点加入集群失败

   ```shell
   kubeadm reset -f 重置,然后再次加入
   ```

3. 如何重置Master节点

   ```shell
   kubeadnim reset -f
   ```





# 第二章  部署步骤

Node：一台物理机或者虚拟机称为一个Node

## 2.1 创建命名空间

一个应用对应一个命名空间，比如rummy游戏的全部服务部署在命名空间rummy下

```ini
创建 = kubectl create -f nginx-namespace.yaml 或者 kubectl create namespace test-env

查询 = kubectl get -f namespaces

查询指定命名空间 = kubectl get -f namespace nginx

查看详情 = kubectl describe namespace nginx

删除命名空间 = kubectl delete namespace nginx
```





## 2.2 发布Pod

StatefulSet：有状态服务

Deployment：无状态服务

DaemonSet：每个Node运行一个Pod，常用于监控，日志收集（配合elk）

Job：一次性任务，比如批处理程序，完成后容器就退出

CronJob：定时任务

ReplicaSet：控制由其管理的pod，使pod副本的数量始终维持在预设的个数

ReplicationController：和ReplicaSet一样

```ini
创建 = kubectl create -f nginx-deployment.yaml

更新 = kubectl apply -f nginx-deployment.yaml

查询 = kubectl get deployment -n nginx

查看pods列表 = kubectl describe pods -n nginx

查看pod详情 = kubectl describe pod rook-ceph-mon-a-7cc457848f-pzfbt -n ceph

删除 = kubectl delete deploy nginx-deployment -n nginx
```





## 2.3 创建service

service 用于对外暴露端口或者对内rpc调用暴露端口

```shell
vim nginx-service.yaml
apiVersion: v1
kind: Service
metadata:
  labels:
   app: nginx
  name: nginx-deployment1
  namespace: nginx
spec:
  ports:
  - port: 9000
    name: nginx-service80
    protocol: TCP
    targetPort: 80
    nodePort: 31090
  selector:
    app: nginx
  type: NodePort
```





## 2.4 例子

+ nginx-namespace.yaml

  ```yaml
  apiVersion: v1
  kind: Namespace
  metadata:
    name: nginx
    labels:
      name: nginx
  ```

+ mysql-deployment.yaml

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: mysql-deployment1
    labels:
      app: nginx
    namespace: nginx
  spec:
    containers:
    - name: mysql-container
      image: mysql:5.7.44
      ports:
      - containerPort: 3306  # 容器对外暴露端口
      env:
      - name: MYSQL_ROOT_PASSWORD    ## 配置Root用户默认密码
        value: "123456"
    restartPolicy: Always
  ```

+ nginx-namespace.yaml

  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: mysql-deployment1
    labels:
      app: nginx
    namespace: nginx
  spec:
    containers:
    - name: mysql-container
      image: mysql:5.7.44
      ports:
      - containerPort: 3306
      env:
      - name: MYSQL_ROOT_PASSWORD    ## 配置Root用户默认密码
        value: "123456"
    restartPolicy: Always
  ```

+ nginx-service.yaml

  ```yaml
  apiVersion: v1
  kind: Service
  metadata:
    labels:
     app: nginx
    name: nginx-deployment1
    namespace: nginx
  spec:
    ports:
    - port: 9000     # k8s内部rpc调用端口
      name: nginx-service80
      protocol: TCP
      targetPort: 80 # 上游服务端口
      nodePort: 31090    # k8s对外表露端口
    - port: 9001
      name: mysql-service
      protocol: TCP
      targetPort: 3306
      nodePort: 31091
    selector:
      app: nginx
    type: NodePort
  ```

  



# 第三章 常用命令



## 3.1 获取信息

1. kubectl get:获取Kubernetes资源的信息，例如节点,服务,Pod,配置等。
2. kubectl  describe: 显示特定资源的详细信息。
3. kubectl logs: 获取Pod的日志。
4. kubectl top: 查看节点和Pod的CPU和内存使用情况。



## 3.2 调试和诊断

1. kubectl exec:在容器中执行命令
2. kubectl port-forward:将本地端口转发到Pod端口
3. kubectl run:在集群中创建一个新的Pod,并在其中运行一个容器
4. kubectl attach:连接到正在运行的容器
5. kubectl debug:启动一个调试容器并将其连接到指定的Pod上



## 3.3 状态管理

1. kubectl create:创建K8S资源
2. kubectl apply:对已存在的K8S资源进行更新操作
3. kubectl delete:删除K8S资源
4. kubectl edit: 在编辑器中编辑资源配置文件
5. kubectl label:为资源添加或修改标签
6. kubectl annotate: 为资源添加或修改注释



## 3.4 扩缩容

1. kubectl scale:扩展或缩小 Deployment,StatefulSet等的副本数
2. kubectl autoscale:创建Horizontal Pod Autoscaler对象,根据CPU或自定义指标来自动扩缩容Pod



## 3.5 部署管理

1. kubectl rollout:对Deployment,DaemonSet,StatefulSet等进行滚动升级
2. kubectl rollout history:查看部署历史记录.
3. kubectl rollout undo:回滚部署操作
4. kubectl patch:通过部分更改来更新Kubernetes资源



## 3.6 安全和身份验证

1. kubectl auth:管理身份验证和授权
2. kubectl create secret: 创建用于身份验证和授权的Kubernetes密钥
3. kubectl certificate:管理TLS证书和私钥
