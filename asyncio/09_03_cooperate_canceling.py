# такой пример мы можем увидеть при работе с ткинтером - библиотека для построения графического пользовательного
# интерфейса, в котором asyncio loop и loop обработки событий, поступающих от пользователя, находятся в разных потоках
# и вот этот многопоточный сценарий снизу мог бы там запросто встретиться

import asyncio
import threading


async def fetch_doc(doc):  # метод для загрузки документов
    await asyncio.sleep(1)  # эмулируем работу
    return doc


# token - типа спец маркер, который будет показывать, пора ли свалить с цикла
async def get_docs(docs, token):
    pages = []
    for cur_doc in docs:
        if token.is_set():
            break
        doc = await fetch_doc(cur_doc)

        for page in doc:
            pages.append(page)

    return pages


# метод, который запрашивает у пользователя отмену, принимает токен, т.к. выставляем флажок здесь
def get_response(token):
    response = input('are you about to cancel?')
    if response == 'y':
        token.set()


async def main():
    token = threading.Event()
    task = asyncio.create_task(get_docs(['doc1', 'doc2', 'doc3'], token))

    t = threading.Thread(target=get_response, args=(token,))
    t.start()
    result = await task

    for res in result:
        print(f'{res}', end='')

if __name__ == '__main__':
    asyncio.run(main())
