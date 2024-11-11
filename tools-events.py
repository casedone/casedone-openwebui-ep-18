from datetime import datetime
import asyncio


class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints
    # Use Sphinx-style docstrings to document your tools, they will be used for generating tools specifications
    # Please refer to function_calling_filter_pipeline.py file from pipelines project for an example

    async def get_current_time(self, __event_emitter__=None) -> str:
        """
        Get the current time in a more human-readable format.
        :return: The current time.
        """
        try:
            await __event_emitter__(
                {
                    "type": "status",  # We set the type here
                    "data": {
                        "description": "I'm retrieving information.",
                        "done": False,
                    },
                    # Note done is False here indicating we are still emitting statuses
                }
            )
            
            await __event_emitter__(
                    {
                        "type": "message", # We set the type here
                        "data": {"content": "Alright, I'm doing it...\n"},
                        # Note that with message types we do NOT have to set a done condition
                    }
            )

            await asyncio.sleep(3)

            now = datetime.now()
            current_time = now.strftime(
                "%I:%M:%S %p"
            )  # Using 12-hour format with AM/PM
            current_date = now.strftime(
                "%A, %B %d, %Y"
            )  # Full weekday, month name, day, and year

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "I finished retrieving information.",
                        "done": True,
                    },
                    # Note done is True here indicating we are done emitting statuses
                }
            )

            return f"Current Date and Time = {current_date}, {current_time}"

        except Exception as e:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"An error occurred: {e}", "done": True},
                }
            )
            return f"Tell the user: {e}"
