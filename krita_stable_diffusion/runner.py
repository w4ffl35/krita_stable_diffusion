from connect import StableDiffusionConnectionManager


def callback(msg):
    print("*** Message received ***")
    print(msg)


if __name__ == "__main__":
    StableDiffusionConnectionManager(
        callback=callback
    )