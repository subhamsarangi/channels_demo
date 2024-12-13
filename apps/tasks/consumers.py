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
            await self.send(json.dumps({"clock": str(datetime.now())}))


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        tasks = [random.randint(1, 3) for _ in range(5)]
        total_time = sum(tasks)

        elapsed_time = 0

        for i, task_time in enumerate(tasks, 1):
            await asyncio.sleep(task_time)
            elapsed_time += task_time
            progress = int((elapsed_time / total_time) * 100)

            await self.send(json.dumps({"progress": progress}))

        await self.send(
            json.dumps({"progress": 100, "message": "All tasks completed!"})
        )


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        player_move = data["move"]

        # Computer makes a move
        computer_move = random.choice(["rock", "paper", "scissors"])

        # Determine the winner
        result = self.determine_winner(player_move, computer_move)

        # Send the result back to the player
        await self.send(
            text_data=json.dumps(
                {
                    "computer_move": computer_move,
                    "result": result,
                }
            )
        )

    def determine_winner(self, player_move, computer_move):
        if player_move == computer_move:
            return "draw"
        elif (
            (player_move == "rock" and computer_move == "scissors")
            or (player_move == "paper" and computer_move == "rock")
            or (player_move == "scissors" and computer_move == "paper")
        ):
            return "win"
        else:
            return "lose"
