from fastapi.requests import Request


def log(tag = "Myapp", message = "no message", request: Request = None):
    with open("log.txt", "w+") as log:
        log.write(f"{tag}: {message}\n")
        log.write(f"\t{request.url}\n")