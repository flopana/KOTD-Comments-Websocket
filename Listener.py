import asyncio
import json
from asyncio import Queue
from typing import Any

from config import reddit


# https://stackoverflow.com/a/72579725/11844720
class Listener:
    def __init__(self):
        # Every incoming websocket conneciton adds it own Queue to this list called
        # subscribers.
        self.subscribers: list[Queue] = []
        # This will hold an asyncio task which will receives messages and broadcasts them
        # to all subscribers.
        self.listener_task = None

    async def subscribe(self, q: Queue):
        # Every incoming websocket connection must create a Queue and subscribe itself to
        # this class instance
        self.subscribers.append(q)

    async def start_listening(self):
        # Method that must be called on startup of application to start the listening
        # process of external messages.
        self.listener_task = asyncio.create_task(self._listener())

    async def _listener(self) -> None:
        subreddit = await reddit.subreddit("kickopenthedoor")
        async for comment in subreddit.stream.comments():
            for q in self.subscribers:
                await q.put({
                    'body': comment.body,
                    'author': comment.author.name,
                    'link_id': comment.link_id,
                    'author_flair_text': comment.author_flair_text,
                    'author_flair_css_class': comment.author_flair_css_class,
                    'permalink': comment.permalink,
                })

    async def stop_listening(self):
        # closing off the asyncio task when stopping the app. This method is called on
        # app shutdown
        if self.listener_task.done():
            self.listener_task.result()
        else:
            self.listener_task.cancel()

    async def receive_and_publish_message(self, msg: Any):
        # this was a method that was called when someone would make a request
        # to /add_item endpoint as part of earlier solution to see if the msg would be
        # broadcasted to all open websocket connections (it does)
        for q in self.subscribers:
            try:
                q.put_nowait(str(msg))
            except Exception as e:
                raise e

    # Note: missing here is any disconnect logic (e.g. removing the queue from the list of subscribers
    # when a websocket connection is ended or closed.)
