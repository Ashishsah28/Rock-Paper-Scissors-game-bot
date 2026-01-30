import logging
import asyncio
import nest_asyncio
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, InlineQueryHandler, CallbackQueryHandler, ContextTypes

# Setup
nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# Global dictionary to store game data
games = {}

# Game Winner Logic
def get_winner_text(p1, p2):
    m1, m2 = p1['move'], p2['move']
    if m1 == m2: return "It's a Tie! 🤝"
    wins = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    if wins[m1] == m2:
        return f"🏆 {p1['name']} JEET GAYA!"
    return f"🏆 {p2['name']} JEET GAYA!"

# Inline Query Handler
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

# Button Interaction Handler
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
        await query.edit_message_text("Apna move chuniye!", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("m_"):
        parts = data.split("_")
        game_id = parts[1]
        move = parts[2]
        
        if game_id not in games: return
        
        # User move record karein
        if user.id not in games[game_id]['moves'] and len(games[game_id]['moves']) < 2:
            games[game_id]['moves'][user.id] = {'name': user.first_name, 'move': move}
            await query.answer(f"Aapne {move} chuna!", show_alert=True)
        
        # Result announce karein jab dono players move chun lein
        if len(games[game_id]['moves']) == 2:
            p_ids = list(games[game_id]['moves'].keys())
            p1, p2 = games[game_id]['moves'][p_ids[0]], games[game_id]['moves'][p_ids[1]]
            result = get_winner_text(p1, p2)
            await query.edit_message_text(
                f"<b>Khel Ka Parinam:</b>\n{p1['name']}: {p1['move']}\n{p2['name']}: {p2['move']}\n\n{result}", 
                parse_mode="HTML"
            )
            del games[game_id]

# Bot Startup Function
async def main():
    # --- APNA TOKEN YAHAN DALEIN ---
    TOKEN = "8229009580:AAHxTvrvM4NYIjGFO86cE6YpcGV4Cd8khT8" 
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("🚀 Bot starting...")
    await app.initialize()
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.start()
    await app.updater.start_polling()
    
    # Keep running
    while True:
        await asyncio.sleep(10)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
