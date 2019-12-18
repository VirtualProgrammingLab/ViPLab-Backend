# ViPLab-Backend
Virtual Programming Laboratory Backend

This is the project INF or Bachelor research project of the University of Stuttgart by Sven Dyhr, Julia Christoph and Miriam Awad.

The aim of this project is to develop a new Vip-Lab backend for the University of Stuttgart. A new architecture based on Kata containers has been developed, which pulls up a new container for each task to be processed, compiles and executes the task within and returns the corresponding results.

Short installation guide:
1. Download/clone git
2. Build the dockerfile and name it "python_socket_c"

Starting the Backend:
1. Start the Flask server (-> controller_socket_client.py)
2. Start the triggering script (-> findLanguage.py)
