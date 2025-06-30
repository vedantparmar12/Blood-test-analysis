import uvicorn
import asyncio
import sys

async def main():
    """Run the server with proper async handling"""
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid some asyncio issues
        log_level="info"
    )
    server = uvicorn.Server(config)
    
    try:
        await server.serve()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await server.shutdown()

if __name__ == "__main__":
    if sys.platform == "win32":
        # Fix for Windows asyncio issues
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped")
    except Exception as e:
        print(f"Error: {e}")