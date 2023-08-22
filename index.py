import components
from bot import run

def bot():
    try:
        run(components.new_mentions, components.backend, components.get_parent)
    except Exception as e:
        print(e)
        bot()

bot()