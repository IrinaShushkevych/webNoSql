from mongo import fetch_authors, fetch_quotes

def func_help():
    print('Commands:')
    print(' - name:<name>[, <name>,...] - Search authors')
    print(' - tag:<tag>[, <tag>,...] - Search quotes')
    print(' - exit - Close programm')
    print(' - help')

def func_exit():
    print('Goodby!')
    quit()


def get_authors(name):
    if isinstance(name, list):
        name_select = '|'.join([el.strip() for el in name])
    elif isinstance(name, str):
        name_select = name.strip()
    else:
        print('Wrong type of parametr')
        return None
 
    result = fetch_authors(name_select)

    print_author(result)

def get_quotes(tags):
    if isinstance(tags, list):
        tags_select = '|'.join([el.strip() for el in tags])
    elif isinstance(tags, str):
        tags_select = tags.strip()
    else:
        print('Wrong type of parametr')
        return None

    result = fetch_quotes(tags_select)

    print_quotes(result)

def print_author(author):
    for el in author:
        print('Name: ', el['fullname'])
        print('Born date: ', el['born_date'])
        print('Born location: ', el['born_location'])
        print('Description: ', el['description'])
        print('--------------------------------------------------------------------------------------')

def print_quotes(quotes):
    for el in quotes:
        print('Tags: ', ', '.join(el['tags']))
        print('Author: ', el['author'])
        print('Quote: ', el['quote'])
        print('--------------------------------------------------------------------------------------')


commands = {
    'name': get_authors,
    'tag': get_quotes,
    'exit': func_exit,
    'help': func_help
}

def main():
    while True:
        print('-------------------------------------------------------------------------')
        cmd = input("Enter command (enter 'help' if you don't know commands): ")
        print('-------------------------------------------------------------------------')
        cmd_list = cmd.split(':')
        if not cmd_list or len(cmd_list)> 2 or cmd_list[0] not in commands:
            print('Wrong command')
        else:
            if len(cmd_list) >= 2:
                commands[cmd_list[0]](cmd_list[1].split(','))
            else:
                commands[cmd_list[0]]()

if __name__ == '__main__':
    # seeds()
    main()