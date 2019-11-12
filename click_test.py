import click

#from caesar_encryption import encrypt

@click.command()
@click.option(
    '--api_key',
    '-key',
    '-k',
    default='b3fa360a82cd459e8f1b459b3cf9127c',
    help='The hash/alpha-numeric key to use in the blockchain network.'
)
@click.option(
    '--api_key',
    '-key',
    '-k',
    default='b3fa360a82cd459e8f1b459b3cf9127c',
    help='The hash/alpha-numeric key to use in the blockchain network.'
)

def caesar(input_file, output_file, decrypt, key):
    if input_file:
        text = input_file.read()
    else:
        text = click.prompt('Enter a text', hide_input=not decrypt)
    if decrypt:
        key = -key
    #cyphertext = encrypt(text, key)
    if output_file:
        output_file.write(cyphertext)
    else:
        click.echo(cyphertext)

if __name__ == '__main__':
    caesar()