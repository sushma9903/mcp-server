import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_agent_workflow():
    server_params = StdioServerParameters(
        command="python",
        args=["server/main.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Step 1: Search
            result1 = await session.call_tool("search_locations", {"query": "Mumbai"})
            print("Search:", result1)
            
            # Step 2: Get details
            result2 = await session.call_tool("get_location_details", {"location_id": "loc_1"})
            print("Details:", result2)
            
            # Step 3: Resolve dependencies
            result3 = await session.call_tool("resolve_location_dependencies", {"region_id": "reg_west"})
            print("Region:", result3)

if __name__ == "__main__":
    asyncio.run(run_agent_workflow())