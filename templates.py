from jinja2 import Environment, FileSystemLoader

# Create the jinja2 environment.
env = Environment(loader=FileSystemLoader('./templates'))

def render_template(filename, **kwargs):
    print(kwargs.items(), kwargs)
    return env.get_template(filename).render(kwargs.items())