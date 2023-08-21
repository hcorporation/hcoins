import components
from bot import run

try:
    run(components.new_mentions, components.backend, components.get_parent)
except Exception as e:
    print(e)
    run()
