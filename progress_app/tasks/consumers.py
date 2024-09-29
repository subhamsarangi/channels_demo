import asyncio
from datetime import datetime
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class ClockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            await asyncio.sleep(2)  # Simulate waiting
            await self.send(json.dumps({
                'clock': str(datetime.now())
            }))

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        tasks = [random.randint(1, 5) for _ in range(5)]
        total_time = sum(tasks) 

        elapsed_time = 0

        for i, task_time in enumerate(tasks, 1):
            await asyncio.sleep(task_time)  # Simulate the task duration
            elapsed_time += task_time
            progress = int((elapsed_time / total_time) * 100)
            
            await self.send(json.dumps({
                'progress': progress
            }))

        await self.send(json.dumps({
            'progress': 100, 'message': 'All tasks completed!'
        }))
