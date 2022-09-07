""" ViPLab backend process 

Delegates incoming tasks to available backends
"""
import multiprocessing
import configparser
import json
import tempfile
import docker
import requests
import time
import os
import url64 
import datetime
import uuid
import tarfile
from proton.reactor import Container
from amqp_messager import AMQPMessager
from threading import Thread
from queue import Empty
from models import ComputationSchema, ConfigurationContainerSchema
from docker.types import Mount
import boto3
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urlparse, urlunparse


class ViPLabBackend(object):
    def __init__(self, config_file):
        self.config = configparser.ConfigParser(converters={"list": json.loads},
                                                inline_comment_prefixes=('#'))
        self.config.read(config_file)
        if os.getenv('AMQPServer') :
            self.config.set("AMQP", "server",  os.getenv('AMQPServer'))
            print("Using env AMQPServer %s"%os.getenv('AMQPServer'))
        if os.getenv('endpoint_url') :
            self.config.set("S3", "EndpointURL",  os.getenv('endpoint_url'))
            print("Using env endpoint_url %s"%os.getenv('endpoint_url'))
        if os.getenv('access_key') :
            self.config.set("S3", "AWSAccessKeyID",  os.getenv('access_key'))
            print("Using env access_key %s"%os.getenv('access_key'))
        if os.getenv('secret_key') :
            self.config.set("S3", "AWSSecretAccessKey",  os.getenv('secret_key'))
            print("Using env secret_key")
        if os.getenv('rewrite_endpoint_url') :
            self.config.set("S3", "RewriteEndpoint",  os.getenv('rewrite_endpoint_url'))
            print("Using env rewrite_endpoint_url: %s"%os.getenv('rewrite_endpoint_url'))
        self.tasks = multiprocessing.Queue(3)
        self.results = multiprocessing.Queue()
        self.running_computations = {}
        self.client = docker.from_env()
        # ToDO: store errors and send them within result-message back
        self.errors = []
        # ToDo: implement logging
        # set up amqp_messager
        self.s3client = boto3.client('s3',
                                     endpoint_url=self.config["S3"]["EndpointURL"],
                                     aws_access_key_id=self.config["S3"]["AWSAccessKeyID"],
                                     aws_secret_access_key=self.config["S3"]["AWSSecretAccessKey"]
        )
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
                    try:
                        container, image_filename, volume = \
                            self._prepare_container_backend(computation, 
                                                        tmp_dir.name)
                    except: # e.g. schema validation error
                        print("Exeception occured in prepartion. Skipped task.")
                        continue
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
                                                sidekick, 
                                                self.s3client, 
                                                self.config["S3"]["RewriteEndpoint"])
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
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=3)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        for f in files:
            files = {'file': (f, open(os.path.join(basepath,f),'rb'))}
            r = s.post('http://%s:5000'%ip_add, files=files)

                

class ResultStreamer(Thread):
    def __init__(self, stream, tmp_dir, files, result_queue, computation_id, sidekick, s3client, rewrite_url = None):
        super(ResultStreamer, self).__init__()
        self.stream = stream
        self.tmp_dir = tmp_dir
        self.computation_id = str(computation_id)
        self.results = result_queue
        self.sent_files = files
        self.sidekick = sidekick
        self.s3client = s3client
        self.rewrite_url = rewrite_url
        
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
                for fileentry in [entry for entry in data if entry['name'][1:] not in self.sent_files]:
                    print(fileentry)
                    if fileentry["size"] < 4 * 1024:
                        fdata = requests.get('http://%s:5000/data/%s'%(ip_add,fileentry['name'][1:])).content
                        result["artifacts"].append(
                            {"identifier": str(uuid.uuid4()),
                             "type": "file",
                             "path": fileentry['name'][1:],
                             "MIMEtype": fileentry['mimetype'],
                             "content": url64.encode(fdata)})
                    else:
                        response = {"target" : self.s3client.generate_presigned_url('put_object', Params={'Bucket': "test-bucket", 'Key': fileentry['name'][1:]}, ExpiresIn=3600, HttpMethod='PUT')}
                        r = requests.post('http://%s:5000/upload/%s'%(ip_add,fileentry['name'][1:]), json=response)
                        target_url = self.s3client.generate_presigned_url('get_object', Params={'Bucket': "test-bucket", 'Key': fileentry['name'][1:]}, ExpiresIn=3600)
                        if self.rewrite_url:
                            target_split = urlparse(target_url)
                            rewrite_split = urlparse(self.rewrite_url)
                            target_url = urlunparse((rewrite_split[0], rewrite_split[1], target_split[2], target_split[3], target_split[4], target_split[5]))
                        result["artifacts"].append(
                            {"identifier": str(uuid.uuid4()),
                             "type": "s3file",
                             "path": fileentry['name'][1:],
                             "size": fileentry["size"],
                             "MIMEtype": 'application/octet-stream',
                             "url": target_url })
                self.sidekick.stop()
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
        backend.tasks.close()
        backend.tasks.join_thread()
        backend.results.put("finished")
        backend.results.close()
        backend.results.join_thread()
        backend.messager_process.terminate()
        backend.messager_process.join()
