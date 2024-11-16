import uvicorn
import asyncio
from src.Lib.Cli import Cli
from src.Lib.Api import api
from src.Lib.Config import config
from src.Lib.Route import readAll


async def run():
    error: Exception | None = None

    try:

        print('Cli', Cli.parseWithFirstAsCommand())

        from src.Event.Start import onStart
        onStart()

        from src.bootstrap import bootstrap
        bootstrap()

        readAll()

        from src.Event.Ready import onReady
        onReady()

        uConfig = uvicorn.Config('main:api',
                                 host=config('server.host'),
                                 port=config('server.port'),
                    reload=config('server.debug')
                                 )

        uServer = uvicorn.Server(uConfig)

        await uServer.serve()


    except Exception as e:
        error = e
        from src.Event.Error import onError
        onError(e)

    finally:
        from src.Event.Close import onClose
        onClose(error)


if __name__ == "__main__":
    asyncio.run(run())