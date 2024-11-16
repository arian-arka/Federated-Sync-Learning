import requests
import concurrent.futures


def nodeRequest(
        url='',
        method='GET',
        data=None,
        json=None,
        headers=None
):
    try:
        req = requests.request(method, url=url, data=data, json=json, headers=headers)

        if not req.ok:
            raise Exception('Request for {} was not ok! it was {}'.format(url,req.status_code))
        return req.json()
    except Exception as e:
        return e


def concurrentNodeRequests(reqs):

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for req in reqs:
            futures.append(
                executor.submit(nodeRequest, **req)
            )
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    # print('results',results)
    return results

def areAllResponsesValid(responses,callback = None):
    for r in responses:
        if isinstance(r,Exception):return False
        if callback and not callback(r) : return False

    return True