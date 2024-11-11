from datetime import datetime
import asyncio


class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints
    # Use Sphinx-style docstrings to document your tools, they will be used for generating tools specifications
    # Please refer to function_calling_filter_pipeline.py file from pipelines project for an example

    async def get_product_info(self, __event_emitter__=None) -> str:
        """
        Get information of products we are selling.
        :return: product information.
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
            
            asyncio.sleep(2)
            
            await __event_emitter__(
                    {
                        "type": "message", # We set the type here
                        "data": {"content": "Alright, hang on tight...\n"},
                        # Note that with message types we do NOT have to set a done condition
                    }
            )
            
            asyncio.sleep(2)

            product_info = """
            1. Coffee bean, houseblend, weight 250 g, $30 price.
            2. Tea bags, imported, weight 100 g, $30 price.
            3. Blueberry muffin, $5 a piece.
            """

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

            return product_info

        except Exception as e:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"An error occurred: {e}", "done": True},
                }
            )
            return f"Tell the user: {e}"

