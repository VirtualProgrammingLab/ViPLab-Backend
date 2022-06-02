import json
from threading import Thread 
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import ApplicationEvent, EventInjector


class AMQPMessager(MessagingHandler):    
    def __init__(self, server, receiver_queues, sender_queue, task_queue,
                 result_queue, preparation_queue):
        super(AMQPMessager, self).__init__()
        self.server = server
        self.receiver_queues = receiver_queues
        self.sender_queue = sender_queue
        self.tasks = task_queue
        self.results = result_queue
        self.preparations = preparation_queue

    def on_start(self, event):
        conn = event.container.connect(self.server)
        for queue in self.receiver_queues:
            event.container.create_receiver(conn, queue)  
        self.sender = event.container.create_sender(conn, self.sender_queue)
        e = ApplicationEvent("result")
        e.container = event.container
        self.result_informer = ResultInformer(self.results, EventInjector(), e)
        self.result_informer.start()
        event.container.selectable(self.result_informer.injector)

    def on_message(self, event):
        # ToDO: ignore duplicate message
        if event.message.address != "preparations":
            self.tasks.put(event.message.body)
        elif event.message.address == "preparations":
            self.preparations.put(event.message.body)
    
    def on_result(self, event):
        # check if we are finished
        if type(event.subject) == str and event.subject == 'finished':
            event.receiver.close()
            self.sender.close()
            event.connection.close()
        else:
            # ToDO: should i ask the broker if i have sender credit??
            self.sender.send(Message(durable=True, body=event.subject))


class ResultInformer(Thread):
    def __init__(self, result_queue, injector, event):
        super(ResultInformer, self).__init__()
        self.result_queue = result_queue
        self.injector = injector
        self.event = event
        
    def run(self):
        while True:
            result_json = self.result_queue.get()
            result = json.dumps(result_json)
            self.event.subject = result
            self.injector.trigger(self.event)

