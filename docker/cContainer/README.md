Erstellen des Images:
(sudo) docker build -t nameImage .

Starten des Containers mit:
(sudo) docker run --name name -v /fullpath:/pathInContainer -it nameImage bash

sudo docker run --runtime=kata-fc --name name -v /home/julia/...:/src -itd nameImage bash

curl http://localhost:5555/containers/create?name=<name> -X POST -H "Content-Type: application/json" -d '{"Image":"alpine", "HostConfig":{ "Binds":["/home/julia/:/src"], "Runtime":"kata-fc"}}'
