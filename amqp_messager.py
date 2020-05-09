import json
from threading import Thread 
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import ApplicationEvent, EventInjector


class AMQPMessager(MessagingHandler):    
    def __init__(self, server, receiver_queues, sender_queue, task_queue,
                 result_queue):
        super(AMQPMessager, self).__init__(auto_accept=False)
        self.server = server
        self.receiver_queues = receiver_queues
        self.sender_queue = sender_queue
        self.tasks = task_queue
        self.results = result_queue

        self.expected = 1000000
        self.received = 0

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
        if event.message.id and event.message.id < self.received:
            # ignore duplicate message
            return
        if self.expected == 0 or self.received < self.expected:
            print(event.message.body)
            self.tasks.put(event.message.body)
            self.received += 1
            # ToDO: bind body to class and don't accept message if
            # this is not working
            self.accept(event.delivery)
            # ToDO: implement cleanup in different method (on_delete??)
            if self.received == self.expected:
                event.receiver.close()
                event.sender.close()
                event.connection.close()
    
    def on_result(self, event):
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

