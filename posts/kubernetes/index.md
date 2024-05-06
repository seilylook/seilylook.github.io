# Kubernetes


# What is Kubernetes or K8s

Kubernetes also known as K8s was built by Google based on their expreience running containers in production. It is now an open-source project and is arguably one of the best and most pupular contaniner orchestrations technologies out there.

To understand Kubernetes, we must first understand two things - `Container` and `Orchestration`.

# Containers

## Why do you need containers?

<img src="/images/kubernetes-1.png" />

In one of my previos projects, I had this requirement to setup an end-to-end stack including various different technologies like a Web Server using NodeJS and database such as MongoDB/CouchDB, messaging system like Redis and an orchestration tool like Ansible. We had a lot of issues developing this application with all these different
components. First, their compatibility with the underlying OS. We had to ensure that
all these different services were compatible with the version of the OS we were
planning to use. There have been times when certain version of these services were
not compatible with the OS, and we have had to go back and look for another OS that
was compatible with all of these different services.

Secondly, we had to check the compatibility between these services and the libraries
and dependencies on the OS. We have had issues were one service requires one
version of a dependent library whereas another service required another version.

The architecture of our application changed over time, we have had to upgrade to
newer versions of these components, or change the database etc and everytime
something changed we had to go through the same process of checking compatibility
between these various components and the underlying infrastructure. This compatibility matrix issue is usually referred to as the matrix from hell.

Next, everytime we had a new developer on board, we found it really difficult to
setup a new environment. The new developers had to follow a large set of
instructions and run 100s of commands to finally setup their environments. They had
to make sure they were using the right Operating System, the right versions of each
of these components and each developer had to set all that up by himself each time.

We also had different development test and production environments. One
developer may be comfortable using one OS, and the others may be using another
one and so we couldn’t gurantee the application that we were building would run the
same way in different environments. And So all of this made our life in developing,
building and shipping the application really difficult.

## What can it do?

<img src="/images/kubernetes-2.png"/>

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

<img src="/images/kubernetes-3.png"/>

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

<img src="/images/kubernetes-4.png"/>

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

<img src="/images/kubernetes-5.png"/>

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

<img src="/images/kubernetes-6.png"/>

An image is a package or a template, just like a VM template that you might have worked with in the virtualization world. It is used to create one or more containers.

Containers are running instances of images that are isolated and have their own enviroments and set of processes.

