import asyncio
from cowsay import cowsay, list_cows

clients = {}
cows_list = list_cows()


async def chat(reader, writer):
    registered = False
    me = ""
    queue = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for query in done:
            if query is send:
                send = asyncio.create_task(reader.readline())
                message = query.result().decode().split()
                if len(message < 1):
                    continue
                elif message[0] == "login":
                    if registered:
                        writer.write(f"Вы уже зарегистрированы как {me}\n".encode())
                    elif (message[1] in cows_list) and not registered:
                        me = message[1]
                        clients[me] = asyncio.Queue()
                        cows_list.remove(message[1])
                        registered = True
                        writer.write("Вы успешно зарегистрированы\n".encode())
                        await writer.drain()
                        receive.cancel()
                        receive = asyncio.create_task(clients[me].get())
                    else:
                        writer.write("Имя недействительно или уже занято\n".encode())
                        await writer.drain()
                elif message[0] == "quit":
                    send.cancel()
                    receive.cancel()
                    if registered:
                        del clients[me]
                        cows_list.append(me)
                    writer.close()
                    await writer.wait_closed()
                    return
                elif message[0] == 'cows':
                    writer.write(f"Доступные имена пользователей (коровы): {', '.join(cows_list)}\n".encode())
                    await writer.drain()
                elif message[0] == 'who':
                    writer.write(f"Зарегистрированные пользователи: {', '.join(clients.keys())}\n".encode())
                    await writer.drain()
                elif message[0] == "say":
                    if not registered:
                        writer.write("Пожалуйста, зарегистрируйтесь, чтобы иметь возможность отправлять сообщения\n".encode())
                        await writer.drain()
                        continue
                    if message[1] in clients.keys():
                        await clients[message[1]].put(
                            f"Сообщение от {me}:\n {cowsay.cowsay((' '.join(message[2:])).strip(), cow=me)}")
                        writer.write("Сообщение отправлено\n".encode())
                        await writer.drain()
                    else:
                        writer.write("Пользователь с этим именем не зарегистрирован\n".encode())
                        await writer.drain()
                elif message[0] == 'yield':
                    if not registered:
                        writer.write("Пожалуйста, зарегистрируйтесь, чтобы иметь возможность отправлять сообщения\n".encode())
                        await writer.drain()
                        continue
                    for dst in clients.values():
                        if dst is not clients[me]:
                            await dst.put(
                                f"Сообщение от {me}:\n {cowsay(' '.join(message[1:]).strip(), cow=me)}")
                    writer.write("Сообщение отправлено \n".encode())
                    await writer.drain()
                else:
                    writer.write("Неверная команда \n".encode())
                    await writer.drain()
            elif query is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{query.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 8000)
    async with server:
        await server.serve_forever()


asyncio.run(main())
