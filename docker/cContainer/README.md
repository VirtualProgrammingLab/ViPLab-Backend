Erstellen des Images:
(sudo) docker build -t nameImage .

Starten des Containers mit:
(sudo) docker run --name name -v /fullpath:/pathInContainer -it nameImage bash
