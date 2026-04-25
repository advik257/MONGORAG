from exceptions import *
# AWS
import boto3
logger = boto3.client("logs")

def main():
    print("Hello from ragmongodb!")


if __name__ == "__main__":
    main()
