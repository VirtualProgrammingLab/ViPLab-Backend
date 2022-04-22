""" ViPLab backend process 

Delegates incoming tasks to available backends
"""
import multiprocessing
import configparser
import mimetypes
import re
import json
import tempfile
import docker
import requests
import os
import url64 
import time
import datetime
import uuid
import tarfile
from proton.reactor import Container
from amqp_messager import AMQPMessager
from threading import Thread
from queue import Empty
from models import ComputationSchema, ConfigurationContainerSchema
from docker.types import Mount
import io
import time

class ViPLabBackend(object):
    def __init__(self, config_file):
        self.config = configparser.ConfigParser(converters={"list": json.loads},
                                                inline_comment_prefixes=('#'))
        self.config.read(config_file)
        if os.getenv('AMQPServer') :
            self.config.set("AMQP", "server",  os.getenv('AMQPServer'))
            print("Using env AMQPServer %s"%os.getenv('AMQPServer'))
        self.tasks = multiprocessing.Queue(3)
        self.results = multiprocessing.Queue()
        self.running_computations = {}
        self.client = docker.from_env()
        # ToDO: store errors and send them within result-message back
        self.errors = []
        # ToDo: implement logging
        # set up amqp_messager
        messager = Container(AMQPMessager(self.config["AMQP"]["server"],
                        self.config.getlist("AMQP", "computationqueues"),
                        self.config["AMQP"]["resultqueue"],
                        self.tasks,
                        self.results))
        self.messager_process = multiprocessing.Process(target=messager.run)
        self.messager_process.start()
            
    def main(self):
        while True:
            # start tasks if available
            try:
                task = self.tasks.get(block=True, timeout=1)
            except Empty:
                pass
            else:
                print("Got computation task.")
                computation = ComputationSchema().loads(task)
                tmp_dir, files = self._prepare_all_environments(computation)
                # ToDO: map start-function dynamically based on getattr
                if computation["environment"] == "Container":
                    container, image_filename, volume = \
                        self._prepare_container_backend(computation, 
                                                        tmp_dir.name)
                    if files:
                        sidekick = self._launch_sidekick(volume, computation['identifier'])
                        time.sleep(3)
                        sidekick.reload()
                        ip_add = sidekick.attrs['NetworkSettings']['Networks']['docker-development-environment_default']['IPAddress']
                        print(sidekick, ip_add)
                        self.copy_to_container(ip_add, os.path.join(tmp_dir.name, "files"), files)
                    else:
                        sidekick = None
                    files.append(image_filename)
                else:
                    raise NotImplementedError
                # attach result listener thread
                response_stream = container.attach(stdout=True, stderr=True, 
                                                   stream=True, logs=True,
                                                   demux=True)
                result_handler = ResultStreamer(response_stream, tmp_dir.name,
                                                files, self.results,
                                                computation["identifier"],
                                                sidekick)
                result_handler.start()
                self.running_computations[computation["identifier"]] = \
                        (container, result_handler, tmp_dir)
                container.start()
                print("Container started.")
            # check if computations are finished
            comp2trash = []
            for key, (cont, thread, tmp) in self.running_computations.items():
                if not thread.is_alive():
                    if not self.config.getboolean("DEFAULT", "keepcontainer"):
                        print("Cleaning up task")
                        cont.remove()
                    thread.join()
                    tmp.cleanup()
                    comp2trash.append(key)
            for key in comp2trash:
                del self.running_computations[key]
                
    def _prepare_all_environments(self, computation):
        # create tmp-dir for this computation and store files there
        tmp_dir = tempfile.TemporaryDirectory(prefix="viplab_", dir="/tmp")
        os.mkdir(os.path.join(tmp_dir.name, "files"))
        files = []
        for f in computation["files"]:
            with open(os.path.join(tmp_dir.name, "files", f["path"]), 
                      'w') as fh:
                for p in f["parts"]:
                    content = url64.decode(p["content"])
                    if not content.endswith("\n"):
                        content += "\n"
                    fh.write(content)
            files.append(f["path"])
        return tmp_dir, files
    
    def _launch_sidekick(self, volume, computation_id):
        container = self.client.containers.run(
            'viplab/volumecreator',
            auto_remove=True,
            cpu_quota=100000,
            detach=True,
            network='docker-development-environment_default',
            mem_limit="1G",
            mounts=[Mount('/tmp/shared',volume.id)],
            name='viplab-vol-creator-%s'%computation_id
        )
        return container

    def _prepare_container_backend(self, computation, tmp_dir):
        # ToDO: create in-between status messages for frontend
        comp_conf = ConfigurationContainerSchema().load(
            computation["configuration"])
        # load image
        image_filename = None
        image_uri = comp_conf["image"]
        if image_uri.startswith("file"):
            image_filename = image_uri[7:]
            # since load takes a lot of time we check if the image is already
            # in the local registry
            with tarfile.open(image_filename) as tar:
                manifest = tar.extractfile("manifest.json").read().decode('utf-8')
                image_id = json.loads(manifest)[0]["RepoTags"][0]
            if len(self.client.images.list(image_id)) == 0:
                with open(image_filename, 'rb') as bf: 
                    print("Loading image ...")
                    image_id = self.client.images.load(bf)[0].id
                    print("... Done.")
        elif image_uri.startswith("id"):
            image_id = image_uri[5:]
        # ToDO: docker run can handle both, id and name, and even pulls if not 
        # already in registry; docker start fails in doing that
        # -> check source code what docker run does
        elif image_uri.startswith("name"):
            image_id = image_uri[7:]
            image = self.client.images.list(image_id)
            if len(image) == 0:
                print("Pulling image")
                self.client.images.pull(image_id)
        else: 
            # assume accessible web resource: this can be a published dataset
            # or a s3-direct link (provided by viplab-connector)
            resp = requests.get(image_uri, stream=True)
            content_disp = resp.headers["Content-disposition"]
            image_filename = content_disp[content_disp.find("filename")+9:].strip('"') 
            with open(os.path.join(tmp_dir, image_filename), 'wb') as fh:
                for chunk in resp.iter_content(chunk_size=1024):
                    fh.write(chunk)
            with open(os.path.join(tmp_dir, image_filename), 'rb') as bf:
                image_id = self.client.images.load(bf)[0].id
        
        # create container
        if comp_conf["volume"] is not None:
            print("Creating volume ...")
            volume = self.client.volumes.create(labels={"computation": computation['identifier'].hex})

        print("Creating container ...")
        container = self.client.containers.create(
            image_id,
            command=comp_conf["command_line_arguments"], 
            auto_remove=False,
            cpu_quota=100000*comp_conf["num_cpus"], 
            detach=True,
            entrypoint=comp_conf["entrypoint"],
            mem_limit=comp_conf["memory"],
            mounts=[Mount(comp_conf["volume"],volume.id)] \
                if comp_conf["volume"] is not None else None)
        print("... Done.")
        if comp_conf["volume"] is not None:
            return container, image_filename, volume
        else:
            return container, image_filename, None

    def copy_to_container(self, ip_add, basepath, files):
        print(basepath, files)
        for f in files:
            files = {'file': (f, open(os.path.join(basepath,f),'rb'))}
            r = requests.post('http://%s:5000'%ip_add, files=files)

class ResultStreamer(Thread):
    def __init__(self, stream, tmp_dir, files, result_queue, computation_id, sidekick):
        super(ResultStreamer, self).__init__()
        self.stream = stream
        self.tmp_dir = tmp_dir
        self.computation_id = str(computation_id)
        self.results = result_queue
        self.sent_files = files
        self.sidekick = sidekick
        
    def run(self):
        std_out_chunk = ""
        std_err_chunk = ""
        chunk_time = 0
        start_time = time.time()
        current_time = 0
        for std_out, std_err in self.stream:
            if chunk_time < 2:
                if std_out:
                    std_out_chunk += std_out.decode('utf-8') + "\n"
                if std_err:
                    std_err_chunk += std_err.decode('utf-8') + "\n"
                current_time = time.time()
                chunk_time += current_time - start_time
                #print(chunk_time)
            else:
                current_time = time.time()
                self.create_result(std_out_chunk, std_err_chunk)
                chunk_time = 0
                std_out_chunk = ""
                std_err_chunk = ""
            start_time = current_time
        # the container has finished and we can create the final results
        # ToDo: ensure only finished files for intermediate results
        self.create_result(std_out_chunk, std_err_chunk, "final", files=True)
    
    def create_result(self, std_out, std_err, status="intermediate", files=False):
        print("Creating result.")
        result = {"computation": self.computation_id,
                  "identifier": str(uuid.uuid4()),
                  "status": status,
                  "timestamp": datetime.datetime.now().astimezone().replace(microsecond=0).isoformat(),
                  "output": {"stdout": url64.encode(std_out),
                             "stderr": url64.encode(std_err)},
                  "artifacts": []}
        if files:
            if self.sidekick:
                ip_add = self.sidekick.attrs['NetworkSettings']['Networks']['docker-development-environment_default']['IPAddress']
                r = requests.get('http://%s:5000/list'%ip_add)
                data = r.json()
                for filename in data:
                    print(filename)
                    fdata = requests.get('http://%s:5000/data/%s'%(ip_add,filename[1:]), stream=True)
                    if fdata.status_code == 200:
                        with open(os.path.join(self.tmp_dir, "files",filename[1:]), 'wb') as f:
                            for chunk in fdata.iter_content(1024):
                                f.write(chunk)
                self.sidekick.stop()
            (_, _, filenames) = next(os.walk(os.path.join(self.tmp_dir, "files")))
            filenames = [n for n in filenames if n not in self.sent_files]
            for name in filenames:
                # ToDO: if filesize > 1mb -> generate s3-url
                file_path = os.path.join(self.tmp_dir, "files", name)
                mimetypes.init()
                mimetypes.add_type("application/vnd.kitware", ".vtu")
                mimetypes.add_type("application/vnd.kitware", ".vtp")
                mimetypes.add_type("application/x-vgf", ".vgf")
                mimetypes.add_type("application/x-vgf3", ".vgf3")
                mimetypes.add_type("application/x-vgfc", ".vgfc")
                mime = mimetypes.guess_type(file_path)
                mimetype = "" 
                if mime[0] == "text/plain":
                    fr = open(file_path, "r")
                    file = fr.readlines()
                    is_uri = True
                    regex = re.compile(
                        r'^(?:http|ftp)s?://' # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                        r'localhost|' #localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?' # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    for line in file:
                        line_content = line.strip()
                        if re.match(regex, line_content) is None:
                            is_uri = False
                    if is_uri:
                        mimetype = "text/uri-list"
                    else: 
                        mimetype = "text/plain"
                elif mime[0]!=None:
                    mimetype = mime[0]
                else:
                    mimetype = "text/plain"
                with open(file_path, 'rb') as fh:
                    content = fh.read()
                result["artifacts"].append(
                    {"identifier": str(uuid.uuid4()),
                     "type": "file",
                     "path": name,
                     "MIMEtype": mimetype,
                     "content": url64.encode(content)})
                self.sent_files.append(name)
        self.results.put(result)
                    
        
if __name__ == '__main__':
    if os.path.isfile('config.ini'):
        conf_file = 'config.ini'
    else:
        conf_file = 'config.sample.ini'
    backend = ViPLabBackend(conf_file)
    try:
        backend.main()
    except KeyboardInterrupt:
        # ToDo: analyze clean up process and improve it
        backend.tasks.close()
        backend.tasks.join_thread()
        backend.results.put("finished")
        backend.results.close()
        backend.results.join_thread()
        backend.messager_process.terminate()
        backend.messager_process.join()
