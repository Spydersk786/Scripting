import base64
    
def main():
    with open("data/abc/data1.data", "r") as f:
        encoded = f.read()

    decoded = base64.b64decode(encoded)
    print(decoded.decode())

if __name__ == "__main__":
    main()
