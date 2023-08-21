import components

def run(new_mentions, backend, get_parent):
    for mention in new_mentions:
        print("mention")
        if "!hCoins" in mention.body:
            parent = get_parent(mention).author.name
            if backend.get_user(mention.author.name) == False:
                if backend.create_user(mention.author.name) == False:
                    mention.reply("an internal unknown error occurred. you can report it here: https://github.com/hcorporation/hcoins") 
            if backend.get_user(parent) == False:
                if backend.create_user(parent) == False:
                    mention.reply("an internal unknown error occurred. you can report it here: https://github.com/hcorporation/hcoins")  
            if (backend.get_user(mention.author.name) and backend.get_user(parent)) == True:
                if "/u/h_corp" in mention.body:
                    mention_parsed = mention.body.replace("/u/h_corp !hCoins ", "")
                else:
                    mention_parsed = mention.body.replace("u/h_corp !hCoins ", "")
                if "+" in mention_parsed:
                    mention.reply(backend.update_user(mention.author.name, parent, mention_parsed.replace("+",""), 1))
                elif "-" in mention_parsed:
                    mention.reply(backend.update_user(mention.author.name, parent, mention_parsed.replace("-",""), 0)) 
                else:
                    mention.reply("use + or - to set what you want to do with your hCoins.")
        elif "!balance" in mention.body:
            mention.reply(backend.get_coins(mention.author.name))
        else:
            mention.reply("I require a command, H sentient.")