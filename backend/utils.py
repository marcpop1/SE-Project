def snake_to_camel(snake_repr: str) -> str:
    tokens = snake_repr.split('_')
    return tokens[0] + ''.join(x.title() for x in tokens[1:])
