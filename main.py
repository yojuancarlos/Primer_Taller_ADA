from views.ui import UI


def main():
    ''' Application initializer. '''
    app: UI = UI()
    app.cmd()


if __name__ == '__main__':
    main()
