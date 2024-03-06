
def main():
    print("Welcome to your favorite python testing services. 100% bugs free!")
    print("Write the code you want to test after:")
    while True:
        try:
            code = input('>>> ')
            exec(code)
        except Exception as e:
            print(e)
            print("Thanks for using our services")
            exit()

if __name__ == '__main__':
    main()
