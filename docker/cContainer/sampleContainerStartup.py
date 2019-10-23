import docker

client= docker.from_env()
containerObject = client.containers.run("python_flask_c", runtime="kata-fc", publish_all_ports=True, detach=True, stdin_open=True)
containerId= vars(containerObject)["attrs"]["Id"]
containerIp = vars(containerObject)["attrs"]["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]
print(containerIp)
