import logging
import asyncio
import nest_asyncio
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, InlineQueryHandler, CallbackQueryHandler, ContextTypes

# Setup
nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# Global data
games = {}
user_scores = {}  # {user_id: score}

# Game Winner & Score Logic
def update_score(user_id, points):
    if user_id not in user_scores:
        user_scores[user_id] = 0
    user_scores[user_id] += points
    # Score 0 se niche na jaye, uske liye:
    if user_scores[user_id] < 0:
        user_scores[user_id] = 0
    return user_scores[user_id]

def get_winner_logic(p1_id, p1_move, p1_name, p2_id, p2_move, p2_name):
    if p1_move == p2_move:
        return f"🤝 <b>It's a Tie!</b>\n\n{p1_name}: {user_scores.get(p1_id, 0)}\n{p2_name}: {user_scores.get(p2_id, 0)}"
    
    wins = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    
    if wins[p1_move] == p2_move:
        s1 = update_score(p1_id, 10) # Jeetne par +10
        s2 = update_score(p2_id, -5) # Harne par -5
        return f"🏆 <b>{p1_name} Wins!</b> (+10)\n💀 <b>{p2_name} Lost!</b> (-5)\n\n<b>Scores:</b>\n{p1_name}: {s1}\n{p2_name}: {s2}"
    else:
        s1 = update_score(p1_id, -5)
        s2 = update_score(p2_id, 10)
        return f"🏆 <b>{p2_name} Wins!</b> (+10)\n💀 <b>{p1_name} Lost!</b> (-5)\n\n<b>Scores:</b>\n{p1_name}: {s1}\n{p2_name}: {s2}"

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_id = str(update.inline_query.id)
    results = [
        InlineQueryResultArticle(
            id=game_id,
            title="Stone Paper Scissors 🎮",
            input_message_content=InputTextMessageContent("<b>S-P-S Game Arena</b>\n\nChallenge bheja gaya hai! Kaun khelega?"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Game 🎮", callback_data=f"join_{game_id}")]])
        )
    ]
    await update.inline_query.answer(results, cache_time=0)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data, user = query.data, query.from_user
    
    if data.startswith("join_"):
        game_id = data.split("_")[1]
        if game_id not in games: games[game_id] = {'moves': {}}
        
        keyboard = [[
            InlineKeyboardButton("Rock 🪨", callback_data=f"m_{game_id}_rock"),
            InlineKeyboardButton("Paper 📄", callback_data=f"m_{game_id}_paper"),
            InlineKeyboardButton("Scissors ✂️", callback_data=f"m_{game_id}_scissors")
        ]]
        await query.edit_message_text(f"Player: {user.first_name}\nApna move chuniye!", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("m_"):
        _, game_id, move = data.split("_")
        if game_id not in games: return
        
        if user.id not in games[game_id]['moves'] and len(games[game_id]['moves']) < 2:
            games[game_id]['moves'][user.id] = {'name': user.first_name, 'move': move}
            await query.answer(f"Aapne {move} chuna!", show_alert=True)
        
        if len(games[game_id]['moves']) == 2:
            p_ids = list(games[game_id]['moves'].keys())
            p1_info = games[game_id]['moves'][p_ids[0]]
            p2_info = games[game_id]['moves'][p_ids[1]]
            
            result_text = get_winner_logic(
                p_ids[0], p1_info['move'], p1_info['name'],
                p_ids[1], p2_info['move'], p2_info['name']
            )
            
            final_msg = f"<b>Khel Ka Parinam:</b>\n{p1_info['name']}: {p1_info['move']}\n{p2_info['name']}: {p2_info['move']}\n\n{result_text}"
            await query.edit_message_text(final_msg, parse_mode="HTML")
            del games[game_id]

async def start_bot():
    TOKEN = "YOUR_BOT_TOKEN_HERE" 
    app = Application.builder().token(TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(button_click))
    print("🚀 Bot starting with Score System...")
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.start()
    await app.updater.start_polling()
    while True: await asyncio.sleep(10)

if __name__ == '__main__':
    try: asyncio.run(start_bot())
    except: pass
import logging
import asyncio
import nest_asyncio
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, InlineQueryHandler, CallbackQueryHandler, ContextTypes

# Setup
nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# Global data
games = {}
user_scores = {}  # {user_id: score}

# Game Winner & Score Logic
def update_score(user_id, points):
    if user_id not in user_scores:
        user_scores[user_id] = 0
    user_scores[user_id] += points
    # Score 0 se niche na jaye, uske liye:
    if user_scores[user_id] < 0:
        user_scores[user_id] = 0
    return user_scores[user_id]

def get_winner_logic(p1_id, p1_move, p1_name, p2_id, p2_move, p2_name):
    if p1_move == p2_move:
        return f"🤝 <b>It's a Tie!</b>\n\n{p1_name}: {user_scores.get(p1_id, 0)}\n{p2_name}: {user_scores.get(p2_id, 0)}"
    
    wins = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    
    if wins[p1_move] == p2_move:
        s1 = update_score(p1_id, 10) # Jeetne par +10
        s2 = update_score(p2_id, -5) # Harne par -5
        return f"🏆 <b>{p1_name} Wins!</b> (+10)\n💀 <b>{p2_name} Lost!</b> (-5)\n\n<b>Scores:</b>\n{p1_name}: {s1}\n{p2_name}: {s2}"
    else:
        s1 = update_score(p1_id, -5)
        s2 = update_score(p2_id, 10)
        return f"🏆 <b>{p2_name} Wins!</b> (+10)\n💀 <b>{p1_name} Lost!</b> (-5)\n\n<b>Scores:</b>\n{p1_name}: {s1}\n{p2_name}: {s2}"

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    game_id = str(update.inline_query.id)
    results = [
        InlineQueryResultArticle(
            id=game_id,
            title="Stone Paper Scissors 🎮",
            input_message_content=InputTextMessageContent("<b>S-P-S Game Arena</b>\n\nChallenge bheja gaya hai! Kaun khelega?"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Game 🎮", callback_data=f"join_{game_id}")]])
        )
    ]
    await update.inline_query.answer(results, cache_time=0)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data, user = query.data, query.from_user
    
    if data.startswith("join_"):
        game_id = data.split("_")[1]
        if game_id not in games: games[game_id] = {'moves': {}}
        
        keyboard = [[
            InlineKeyboardButton("Rock 🪨", callback_data=f"m_{game_id}_rock"),
            InlineKeyboardButton("Paper 📄", callback_data=f"m_{game_id}_paper"),
            InlineKeyboardButton("Scissors ✂️", callback_data=f"m_{game_id}_scissors")
        ]]
        await query.edit_message_text(f"Player: {user.first_name}\nApna move chuniye!", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("m_"):
        _, game_id, move = data.split("_")
        if game_id not in games: return
        
        if user.id not in games[game_id]['moves'] and len(games[game_id]['moves']) < 2:
            games[game_id]['moves'][user.id] = {'name': user.first_name, 'move': move}
            await query.answer(f"Aapne {move} chuna!", show_alert=True)
        
        if len(games[game_id]['moves']) == 2:
            p_ids = list(games[game_id]['moves'].keys())
            p1_info = games[game_id]['moves'][p_ids[0]]
            p2_info = games[game_id]['moves'][p_ids[1]]
            
            result_text = get_winner_logic(
                p_ids[0], p1_info['move'], p1_info['name'],
                p_ids[1], p2_info['move'], p2_info['name']
            )
            
            final_msg = f"<b>Khel Ka Parinam:</b>\n{p1_info['name']}: {p1_info['move']}\n{p2_info['name']}: {p2_info['move']}\n\n{result_text}"
            await query.edit_message_text(final_msg, parse_mode="HTML")
            del games[game_id]

async def start_bot():
    TOKEN = "YOUR_BOT_TOKEN_HERE" 
    app = Application.builder().token(TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(button_click))
    print("🚀 Bot starting with Score System...")
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.start()
    await app.updater.start_polling()
    while True: await asyncio.sleep(10)

if __name__ == '__main__':
    try: asyncio.run(start_bot())
    except: pass
        
