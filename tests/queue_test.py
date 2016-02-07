import unittest
import modules.queue
import time

class QueueTest(unittest.TestCase):
    """

    """

    def setup(self):
        print "SETUP!"

        queue_name = 'kube-minion-notifications-test'

        for i in range(0, 10):
            retrieved_message_obj = modules.queue.get_one_message(queue_name)
            modules.queue.delete_a_message(retrieved_message_obj)

        time.sleep(.5)

    def teardown(self):
        print "TEAR DOWN!"

        queue_name = 'kube-minion-notifications-test'

        for i in range(0, 10):
            retrieved_message_obj = modules.queue.get_one_message(queue_name)
            modules.queue.delete_a_message(retrieved_message_obj)

        time.sleep(.5)

    # Sends in one message and retrieves that message and compares it and then deletes the message from the queue
    def test_send_a_message_and_read(self):

        queue_name = 'kube-minion-notifications-test'
        message = 'unit test message'

        modules.queue.send_a_message(queue_name, message)
        retrieved_message_obj = modules.queue.get_one_message(queue_name)
        modules.queue.delete_a_message(retrieved_message_obj)

        assert retrieved_message_obj.body == message

        # delete the message
        modules.queue.delete_a_message(retrieved_message_obj)

        self.teardown()



