# Kubernetes


# What is Kubernetes or K8s

Kubernetes also known as K8s was built by Google based on their expreience running containers in production. It is now an open-source project and is arguably one of the best and most pupular contaniner orchestrations technologies out there.

To understand Kubernetes, we must first understand two things - `Container` and `Orchestration`.

# Containers

## Why do you need containers?

<img src="/images/kubernetes/kubernetes-1.png" />

In one of my previos projects, I had this requirement to setup an end-to-end stack including various different technologies like a Web Server using NodeJS and database such as MongoDB/CouchDB, messaging system like Redis and an orchestration tool like Ansible. We had a lot of issues developing this application with all these different components. First, their compatibility with the underlying OS. We had to ensure that all these different services were compatible with the version of the OS we were planning to use. There have been times when certain version of these services were not compatible with the OS, and we have had to go back and look for another OS that was compatible with all of these different services.

Secondly, we had to check the compatibility between these services and the libraries and dependencies on the OS. We have had issues were one service requires one version of a dependent library whereas another service required another version.

The architecture of our application changed over time, we have had to upgrade to newer versions of these components, or change the database etc and everytime something changed we had to go through the same process of checking compatibility between these various components and the underlying infrastructure. This compatibility matrix issue is usually referred to as the matrix from hell.

Next, everytime we had a new developer on board, we found it really difficult to setup a new environment. The new developers had to follow a large set of instructions and run 100s of commands to finally setup their environments. They had to make sure they were using the right Operating System, the right versions of each of these components and each developer had to set all that up by himself each time.

We also had different development test and production environments. One developer may be comfortable using one OS, and the others may be using another one and so we couldn’t gurantee the application that we were building would run the same way in different environments. And So all of this made our life in developing, building and shipping the application really difficult.

## What can it do?

<img src="/images/kubernetes/kubernetes-2.png"/>

So I needed something that could help us with the compatibility issue. And
something that will allow us to modify or change these components without affecting
the other components and even modify the underlying operating systems as
required. And that search landed me on Docker. With Docker I was able to run each
component in a separate container – with its own libraries and its own dependencies.
All on the same VM and the OS, but within separate environments or containers. We
just had to build the docker configuration once, and all our developers could now get
started with a simple “docker run” command. Irrespective of what underlying OS they
run, all they needed to do was to make sure they had Docker installed on their
systems.

## What is Containers?

<img src="/images/kubernetes/kubernetes-3.png"/>

Containers are completely isolated enviroments, as in they can have their own processes or services, their own network interfaces, their own mounts, just like Virtual machines, except that they all share the same OS Kernel. W

But its also important to note that containers are not new with Docker. Containers have existed for about 10 years now and some of the different types of containers are LXC, LXD, LXCFS etc. Docker utilized LXC and that is were Docker offeres a high-level tool with several powerful functionalities making it really easy for end users like us.

## Operating system

To understand how Docker works let us revisit some basics concepts of Operating
Systems first. If you look at operating systems like Ubuntu, Fedora, Suse or Centos –
they all consist of two things. An OS Kernel and a set of software. The OS Kernel is
responsible for interacting with the underlying hardware. While the OS kernel
remains the same– which is Linux in this case, it’s the software above it that make
these Operating Systems different. This software may consist of a different User
Interface, drivers, compilers, File managers, developer tools etc. SO you have a
common Linux Kernel shared across all Oses and some custom softwares that
differentiate Operating systems from each other.

## Sharing the Kernel

<img src="/images/kubernetes/kubernetes-4.png"/>

We said earlier that Docker containers share the underlying kernel. What does that
actually mean – sharing the kernel? Let’s say we have a system with an Ubuntu OS
with Docker installed on it. Docker can run any flavor of OS on top of it as long as they
are all based on the same kernel – in this case Linux. If the underlying OS is Ubuntu,
docker can run a container based on another distribution like debian, fedora, suse or
centos. Each docker container only has the additional software, that we just talked
about in the previous slide, that makes these operating systems different and docker
utilizes the underlying kernel of the Docker host which works with all Oses above.

So what is an OS that do not share the same kernel as these? Windows ! And so you
wont be able to run a windows based container on a Docker host with Linux OS on it.
For that you would require docker on a windows server.

You might ask isn’t that a disadvantage then? Not being able to run another kernel on
the OS? The answer is No! Because unlike hypervisors, Docker is not meant to
virtualize and run different Operating systems and kernels on the same hardware. The
main purpose of Docker is to containerize applications and to ship them and run
them.

## Containers VS Virtual Machines

<img src="/images/kubernetes/kubernetes-5.png"/>

So that brings us to the differences between virtual machines and containers.
Something that we tend to do, especially those from a Virtualization.

As you can see on the right, in case of Docker, we have the underlying hardware
infrastructure, then the OS, and Docker installed on the OS. Docker then manages the
containers that run with libraries and dependencies alone.

In case of a Virtual
Machine, we have the OS on the underlying hardware, then the Hypervisor like a ESX
or virtualization of some kind and then the virtual machines. As you can see each
virtual machine has its own OS inside it, then the dependencies and then the
application.

This overhead causes higher utilization of underlying resources as there are multiple
virtual operating systems and kernel running. The virtual machines also consume
higher disk space as each VM is heavy and is usually in Giga Bytes in size, wereas
docker containers are lightweight and are usually in Mega Bytes in size.

This allows docker containers to boot up faster, usually in a matter of seconds
whereas VMs we know takes minutes to boot up as it needs to bootup the entire OS.

It is also important to note that, Docker has less isolation as more resources are
shared between containers like the kernel etc. Whereas VMs have complete isolation
from each other. Since VMs don’t rely on the underlying OS or kernel, you can run
different types of OS such as linux based or windows based on the same hypervisor.

## How is it done?

There are a lot of containerized versions of applications readily
available as of today. So most organizations have their products containerized and
available in a public docker registry called dockerhub/or docker store already. For
example you can find images of most common operating systems, databases and
other services and tools. Once you identify the images you need and you install
Docker on your host bringing up an application stack, is as easy as running a docker run command with
the name of the image.

In this case running a docker run ansible command will run an
instance of ansible on the docker host. Similarly run an instance of mongodb, redis
and nodejs using the docker run command. And then when you run nodejs just point
to the location of the code repository on the host. If we need to run multiple
instances of the web service, simply add as many instances as you need, and
configure a load balancer of some kind in the front. In case one of the instances was
to fail, simply destroy that instance and launch a new instance.

## Container VS Image

<img src="/images/kubernetes/kubernetes-6.png"/>

An image is a package or a template, just like a VM template that you might have worked with in the virtualization world. It is used to create one or more containers.

Containers are running instances of images that are isolated and have their own enviroments and set of processes.

## Container Advantage

Traditionally developers developed applications. Then they hand it
over to Ops team to deploy and manage it in production environments. They do that
by providing a set of instructions such as information about how the hosts must be
setup, what pre-requisites are to be installed on the host and how the dependencies
are to be configured etc. Since the Ops team did not develop the application on their
own, they struggle with setting it up. When they hit an issue, they work with the
developers to resolve it.

With Docker, a major portion of work involved in setting up the infrastructure is now
in the hands of the developers in the form of a Docker file. The guide that the
developers built previously to setup the infrastructure can now easily put together
into a Dockerfile to create an image for their applications. This image can now run on
any container platform and is guaranteed to run the same way everywhere. So the
Ops team now can simply use the image to deploy the application. Since the image
was already working when the developer built it and operations are not modifying it,
it continues to work the same when deployed in production.

# Container Orchestration

<img src="/images/kubernetes/kubernetes-7.png"/>

So we learned about containers and we now have our application packaged into a
docker container. But what next? How do you run it in production? What if your
application relies on other containers such as database or messaging services or
other backend services? What if the number of users increase and you need to scale
your application? You would also like to scale down when the load decreases.

To enable these functionalities you need an underlying platform with a set of
resources. The platform needs to orchestrate the connectivity between the
containers and automatically scale up or down based on the load. This whole process
of automatically deploying and managing containers is known as `Container Orchestration`.

## Orchestration Technologies

Kubernetes is thus a container orchestration technology. There are multiple such
technologies available today – Docker has its own tool called Docker Swarm.
Kubernetes from Google and Mesos from Apache. While Docker Swarm is really easy
to setup and get started, it lacks some of the advanced autoscaling features required
for complex applications. Mesos on the other hand is quite difficult to setup and get
started, but supports many advanced features. Kubernetes - arguably the most
popular of it all – is a bit difficult to setup and get started but provides a lot of options
to customize deployments and supports deployment of complex architectures.
Kubernetes is now supported on all public cloud service providers like GCP, Azure and
AWS and the kubernetes project is one of the top ranked projects in Github.

## Kubernetes Advantage

<img src="/images/kubernetes/kubernetes-8.png"/>

There are various advantages of container orchestration. Your application is now
highly available as hardware failures do not bring your application down because you
have multiple instances of your application running on different nodes. The user
traffic is load balanced across the various containers. When demand increases,
deploy more instances of the application seamlessly and within a matter of second
and we have the ability to do that at a service level. When we run out of hardware
resources, scale the number of nodes up/down without having to take down the
application. And do all of these easily with a set of declarative object configuration
files.

It is a container Orchestration technology used to
orchestrate the deployment and management of 100s and 1000s of containers in a
clustered environment.

# Architecture

## Nodes(Minions)

<img src="/images/kubernetes/kubernetes-9.png"/>

A node is a machine – physical or virtual – on which
kubernetes is installed. A node is a worker machine and this is were containers will be
launched by kubernetes.

It was also known as Minions in the past. So you might here these terms used inter
changeably.

But what if the node on which our application is running fails? Well, obviously our
application goes down. So you need to have more than one nodes.

## Cluster

<img src="/images/kubernetes/kubernetes-10.png"/>

A cluster is a set of nodes grouped together. This way even if one node fails you have
your application still accessible from the other nodes. Moreover having multiple
nodes helps in sharing load as well.

## Master

<img src="/images/kubernetes/kubernetes-11.png"/>

Now we have a cluster, but who is responsible for managing the cluster? Were is the
information about the members of the cluster stored? How are the nodes
monitored? When a node fails how do you move the workload of the failed node to
another worker node?

That’s were the Master comes in. The master is another node
with Kubernetes installed in it, and is configured as a Master. The master watches
over the nodes in the cluster and is responsible for the actual orchestration of
containers on the worker nodes.

## Components

<img src="/images/kubernetes/kubernetes-12.png"/>

When you install Kubernetes on a System, you are actually installing the following
components. An API Server. An ETCD service. A kubelet service. A Container Runtime,
Controllers and Schedulers.

The API server acts as the front-end for kubernetes. The users, management devices,
Command line interfaces all talk to the API server to interact with the kubernetes
cluster.

Next is the ETCD key store. ETCD is a distributed reliable key-value store used by
kubernetes to store all data used to manage the cluster. Think of it this way, when you
have multiple nodes and multiple masters in your cluster, etcd stores all that
information on all the nodes in the cluster in a distributed manner. ETCD is
responsible for implementing locks within the cluster to ensure there are no conflicts
between the Masters.

The scheduler is responsible for distributing work or containers across multiple
nodes. It looks for newly created containers and assigns them to Nodes.

The controllers are the brain behind orchestration. They are responsible for noticing
and responding when nodes, containers or endpoints goes down. The controllers
makes decisions to bring up new containers in such cases.

The container runtime is the underlying software that is used to run containers. In our
case it happens to be Docker.

And finally kubelet is the agent that runs on each node in the cluster. The agent is
responsible for making sure that the containers are running on the nodes as
expected.

## Master VS Work Nodes

<img src="/images/kubernetes/kubernetes-13.png"/>

So far we saw two types of servers – Master and Worker and a set of components
that make up Kubernetes. But how are these components distributed across different
types of servers. In other words, how does one server become a master and the
other slave?

The worker node (or minion) as it is also known, is were the containers are hosted.
For example Docker containers, and to run docker containers on a system, we need a
container runtime installed. And that’s were the container runtime falls. In this case it
happens to be Docker. This doesn’t HAVE to be docker, there are other container
runtime alternatives available such as Rocket or CRIO.

The master server has the kube-apiserver and that is what makes it a master.

Similarly the worker nodes have the kubelet agent that is responsible for interacting
with the master to provide health information of the worker node and carry out
actions requested by the master on the worker nodes.

All the information gathered are stored in a key-value store on the Master. The key
value store is based on the popular etcd framework as we just discussed.

The master also has the controller manager and the scheduler.

## Kubectl

<img src="/images/kubernetes/kubernetes-14.png"/>

And finally, we also need to learn a little bit about ONE of the command line utilities
known as the kube command line tool or kubectl or kube control as it is also called.

The kube control tool is used to deploy and manage applications on a kubernetes
cluster, to get cluster information, get the status of nodes in the cluster and many
other things.

The kubectl run command is used to deploy an application on the cluster. The kubectl
cluster-info command is used to view information about the cluster and the kubectl
get pod command is used to list all the nodes part of the cluster.

# Setup

There are lots of ways to setup Kubernetes. We can setup it up ourselves locally on
our laptops or virtual machines using solutions like Minikube and Kubeadmin.
Minikube is a tool used to setup a single instance of Kubernetes in an All-in-one setup
and kubeadmin is a tool used to configure kubernetes in a multi-node setup.

There are also hosted solutions available for setting up kubernetes in a cloud
environment such as GCP and AWS.

And finally if you don’t have the resources or if you don’t want to go through the
hassle of setting it all up yourself, and you simply want to get your hands on a
kubernetes cluster instantly to play with, checkout play-with-k8s.com.

## Minikube

<img src="/images/kubernetes/kubernetes-16.png"/>

We will start with Minikube which is the easiest way to get started with Kubernetes
on a local system. Before we head into the demo it’s good to understand how it works.
Earlier we talked about the different components of Kubernetes that make up a
Master and worker nodes such as the api server, etcd key value store, controllers and
scheduler on the master and kubelets and container runtime on the worker nodes. It
would take a lot of time and effort to setup and install all of these various
components on different systems individually by ourlselves.

Minikube bundles all of these different components into a single image providing us a
pre-configured single node kubernetes cluster so we can get started in a matter of
minutes.

The whole bundle is packaged into an ISO image and is available online for
download.

<img src="/images/kubernetes/kubernetes-17.png"/>

Now you don’t HAVE to download it yourself. Minikube provides an executable
command line utility that will AUTOMATICALLY download the ISO and deploy it in a
virtualization platform such as Oracle Virtualbox or Vmware fusion. So you must have
a Hypervisor installed on your system. For windows you could use Virtualbox or
Hyper-V and for Linux use Virtualbox or KVM.

And finally to interact with the kubernetes cluster, you must have the kubectl
kubernetes command line tool also installed on your machine. So you need 3 things
to get this working, you must have a hypervisor installed, kubectl installed and
minikube executable installed on your system.

# Setup - Kubeadm

<img src="/images/kubernetes/kubernetes-19.png"/>

With the minikube utility you could only setup a single node kubernetes cluster. The
kubeadmin tool helps us setup a multi node cluster with master and workers on
separate machines. Installing all of these various components individually on different
nodes and modifying the configuration files to make it work is a tedious task.
Kubeadmin tool helps us in doing all of that very easily.

<img src="/images/kubernetes/kubernetes-20.png"/>

First, you must have multiple systems or virtual
machines created for configuring a cluster. Once the systems are created, designate
one as master and others as worker nodes.

The next step is to install a container runtime on the hosts. We will be using Docker,
so we must install Docker on all the nodes.

The next step is to install kubeadmin tool on all the nodes. The kubeadmin tool helps
us bootstrap the kubernetes solution by installing and configuring all the required
components in the right nodes.

The third step is to initialize the Master server. During this process all the required
components are installed and configured on the master server. That way we can start
the cluster level configurations from the master server.

Once the master is initialized and before joining the worker nodes to the master, we
must ensure that the network pre-requisites are met. A normal network connectivity
between the systems is not SUFFICIENT for this. Kubernetes requires a special network between the master and worker nodes which is called as a POD network.

The last step is to join the worker nodes to the master node. We are then all set to
launch our application in the kubernetes environment.

# Install

[How to install Kubernetes?](https://kubernetes.io/docs/tasks/tools/)

[How to install Virtual Box](https://formulae.brew.sh/cask/virtualbox#default)

[How to install minikube?](https://minikube.sigs.k8s.io/docs/start/)

[Start Minikube with Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/)

{{<admonition warning>}}

```bash
😄 Darwin 14.4.1 (arm64) 의 minikube v1.33.0
✨ 유저 환경 설정 정보에 기반하여 virtualbox 드라이버를 사용하는 중

❌ Exiting due to DRV_UNSUPPORTED_OS: The driver 'virtualbox' is not supported on darwin/arm64
```

Apple M3 Pro 칩 환경은 아직 Minikube - Virtual Box를 지원하지 않는 듯 하다. 할 수 없이 Docker를 사용해본다.  
{{</admonition>}}

```bash
 {seilylook} 🔥   ~  minikube start --driver=docker
😄  Darwin 14.4.1 (arm64) 의 minikube v1.33.0
✨  유저 환경 설정 정보에 기반하여 docker 드라이버를 사용하는 중
📌  Using Docker Desktop driver with root privileges
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.43 ...
💾  쿠버네티스 v1.30.0 을 다운로드 중 ...
    > preloaded-images-k8s-v18-v1...:  319.81 MiB / 319.81 MiB  100.00% 31.20 M
    > gcr.io/k8s-minikube/kicbase...:  434.52 MiB / 434.52 MiB  100.00% 21.03 M
🔥  Creating docker container (CPUs=2, Memory=4600MB) ...
🐳  쿠버네티스 v1.30.0 을 Docker 26.0.1 런타임으로 설치하는 중
    ▪ 인증서 및 키를 생성하는 중 ...
    ▪ 컨트롤 플레인을 부팅하는 중 ...
    ▪ RBAC 규칙을 구성하는 중 ...
🔗  bridge CNI (Container Networking Interface) 를 구성하는 중 ...
🔎  Kubernetes 구성 요소를 확인...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  애드온 활성화 : storage-provisioner, default-storageclass
🏄  끝났습니다! kubectl이 "minikube" 클러스터와 "default" 네임스페이스를 기본적으로 사용하도록 구성되었습니다.
```

## Manage Cluster

Start

```bash
minikube start
```

Pause Kubernetes without impacting deployed applications:

```bash
minikube pause
```

Unpause a paused instance:

```bash
minikube unpause
```

Halt the cluster:

```bash
minikube stop
```

Change the default memory limit (requires a restart):

```bash
minikube config set memory 9001
```

Browse the catalog of easily installed Kubernetes services:

```bash
minikube addons list
```

Create a second cluster running an older Kubernetes release:

```bash
minikube start -p aged --kubernetes-version=v1.16.1
```

Delete all of the minikube clusters:

```bash
minikube delete --all
```

# Hello Minikube

[Hello Minikube](https://kubernetes.io/docs/tutorials/hello-minikube/)

## Create Deployment

1. Use the kubectl create command to create a Deployment that manages a Pod. The Pod runs a Container based on the provided Docker image.

   ```bash
   # Run a test container image that includes a webserver
   kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
   ```

2. View the Deployment

   ```bash
   kubectl get deployments
   ```

## Create Service

1. Expose the Pod to the public internet using the kubectl expose command:

   ```bash
   kubectl expose deployment hello-node --type=LoadBalancer --port=8080
   ```

   The `--type=LoadBalancer` flag indicates that you want to expose your Service outside of the cluster.

   The application code inside the test image only listens on TCP port 8080. If you used `kubectl expose` to expose a different port, clients could not connect to that other port.

# Pod

<img src="/images/kubernetes/pod-1.png" />
With kubernetes our ultimate aim is to deploy our application in the form of containers on a set of machines that are configured as worker nodes in a cluster.

However, kubernetes does not deploy containers directly
on the worker nodes. The containers are encapsulated into a Kubernetes object
known as PODs. A POD is a single instance of an application. A POD is the smallest
object, that you can create in kubernetes.

<img src="/images/kubernetes/pod-2.png"/>

Here we see the simplest of simplest cases were you have a single node kubernetes cluster with a single instance of your application running in a single docker container encapsulated in a POD. What if the number of users accessing your application increase and you need to scale your application? You need to add additional instances of your web application to share the load. Now, were would you spin up additional instances? Do we bring up a new container instance within the same POD? No! We create a new POD altogether with a new instance of the same application. As you can see we now have two instances of our web application running on two separate PODs on the same kubernetes system or node.

What if the user base FURTHER increases and your current node has no sufficient capacity? Well THEN you can always deploy additional PODs on a new node in the cluster. You will have a new node added to the cluster to expand the cluster’s physical capacity. SO, what I am trying to illustrate in this slide is that, PODs usually have a one-to-one relationship with containers running your application. To scale UP you create new PODs and to scale down you delete PODs. You do not add additional containers to an existing POD to scale your application.

# Replication Controller

<img src="/images/kubernetes/replication-controller-1.png" />

What if for some
reason, our application crashes and the POD fails? Users will no longer be able to
access our application. To prevent users from losing access to our application, we
would like to have more than one instance or POD running at the same time. That
way if one fails we still have our application running on the other one. **The replication controller helps us run multiple instances of a single POD in the kubernetes cluster thus providing High Availability.**

So does that mean you can’t use a replication controller if you plan to have a single POD? No! Even if you have a single POD, the replication controller can help by automatically bringing up a new POD when the existing one fails. Thus the replication controller ensures that the specified number of PODs are running at all times. Even if it’s just 1 or 100.

<img src="/images/kubernetes/replication-controller-2.png"/>

Another reason we need replication controller is to create multiple PODs to share the load across them. For example, in this simple scenario we have a single POD serving a set of users. When the number of users increase we deploy additional POD to balance the load across the two pods. If the demand further increases and If we were to run out of resources on the first node, we could deploy additional PODs across other nodes in the cluster. As you can see, the replication controller spans across multiple nodes in the cluster. It helps us balance the load across multiple pods on different nodes as well as scale our application when the demand increases.

