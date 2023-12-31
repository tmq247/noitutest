import random
import db
from src import log
logger = log.setup_logger(__name__)
import time
# Load danh sách các từ có 2 từ vào một list
with open('src/assets/tudien.txt', 'r') as f:
    list_words = [word.strip().lower() for word in f.readlines()]


def last_word(word):
    return word.split()[-1]

# trích xuất từ đầu tiên của một từ


def first_word(word):
    return word.split()[0]


def get_word_starting_with(start):
    matching_words = [word for word in list_words if word.split()[0] == start]
    if matching_words:
        word = random.choice(matching_words)
        return word
    else:
        return False


def unique_word(start):
    matching_words = [word for word in list_words if word.split()[0] == start]
    return True if len(matching_words) == 0 else False


def new_word():
    word = random.choice(list_words)
    return word if not unique_word(last_word(word)) else new_word() + word


def check_channel(player_word, id_channel, id_user):
    return 'test'
    global sai, current_word, data
    id = str(id)
    if id in data["word"]:
        print('ok')
    else:
        print('ok 2')
        return start()

    if not current_word:
        current_word = new_word()

    if last_word(current_word) == first_word(player_word) and sai != 1:
        if player_word in history:
            return 'Đã trả lời từ, vui lòng tìm từ khác'
        if player_word in list_words:
            # Tìm một từ mới từ danh sách các từ có 2 từ để đưa ra
            next_word = get_word_starting_with(last_word(player_word))
            current_word = next_word
            if not next_word:
                return win()
            response = 'Từ tiếp theo: **' + next_word + '**'
            return response
        else:
            print('Không tồn tại từ, vui lòng tìm từ khác')
            sai -= 1
            response = 'Không tồn tại từ, vui lòng tìm từ khác, **còn ' + \
                str(sai) + ' lần thử** \nTừ hiện tại: **' + current_word + '**'
            return response
    # else:
    #     return loss()


def check_user(player_word, id_user):
    """
    Hàm trả về từ tiếp theo trong trò chơi Nối từ dựa trên từ người chơi nhập vào từ tin nhắn DM
    """
    start_time = time.time() 
    id_user = str(id_user)
    user_data = db.read('users').get(id_user, {})
    current_word = user_data.get('word')
    history = user_data.get('history', [])
    streak = user_data.get('streak', 0)
    sai = user_data.get('sai', 0)

    # nếu không tồn tại user thì tạo user mới
    if not current_word:
        current_word = new_word()
        db.store('users', {id_user: {'word': current_word,
                 'history': [current_word], 'streak': 0, 'sai': 0}})
        logger.info(f"DM: [{id_user}] \x1b[31mNEW\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")           
        return f'Từ hiện tại: **{current_word}**'

    # nếu từ cuối không giống từ đầu
    if last_word(current_word) != first_word(player_word):
        sai += 1
        if sai == 3:
            current_word = new_word()
            db.store('users', {id_user: {'word': current_word,
                     'history': [], 'streak': 0, 'sai': 0}})
            logger.info(f"DM: [{id_user}] \x1b[31mLOSS\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")           
            return f'> Thua cuộc, từ đầu bạn đưa ra phải trùng với từ cuối của bot hoặc từ phải có nghĩa! Chuỗi đúng: **{streak}** \nTừ mới: **{current_word}**'
        else:
            db.store('users', {id_user: {'word': current_word,
                     'history': history, 'streak': streak, 'sai': sai}})
            logger.info(f"DM: [{id_user}] \x1b[31mERROR\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")           
            return f'> Từ đầu bạn đưa ra phải trùng với từ cuối của bot hoặc từ phải có nghĩa!, vui lòng tìm từ khác. Bạn đã trả lời sai **{sai}** lần.\nTừ hiện tại: **{current_word}**'

    # nếu từ không có hoặc đã trả lời
    if player_word in history or player_word not in list_words:
        sai += 1
        if sai == 3:
            current_word = new_word()
            db.store('users', {id_user: {'word': current_word,
                     'history': [], 'streak': 0, 'sai': 0}})
            logger.info(f"DM: [{id_user}] \x1b[31mLOSS\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")           
            return f'> Thua cuộc, từ của bạn không hợp hoặc đã được trả lời! Chuỗi đúng: **{streak}** \nTừ mới: **{current_word}**'
        else:
            db.store('users', {id_user: {'word': current_word,
                     'history': history, 'streak': streak, 'sai': sai}})
            logger.info(f"DM: [{id_user}] \x1b[31mERROR\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")           
            return f'> Đã trả lời từ hoặc từ không hợp lệ, vui lòng tìm từ khác. Bạn đã trả lời sai **{sai}** lần.\nTừ hiện tại: **{current_word}**'

    next_word = get_word_starting_with(last_word(player_word))
    current_word = next_word

    # nếu từ tiếp theo không có trong từ điển
    if not next_word and not next_word in history:
        current_word = new_word()
        db.store('users', {id_user: {'word': current_word,
                 'history': [], 'streak': 0, 'sai': 0}})
        logger.info(f"DM: [{id_user}] \x1b[31mWIN\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")      
        return f'**BẠN ĐÃ THẮNG!** \nChuỗi đúng: **{streak+1}**\n Từ mới: **{current_word}**'

    response = f'Từ tiếp theo: **{next_word}**'

    # nếu đây là từ duy nhất có thể trả lời
    if unique_word(last_word(next_word)):
        current_word = new_word()
        db.store('users', {id_user: {'word': current_word,
                 'history': [], 'streak': 0, 'sai': 0}})
        logger.info(f"DM: [{id_user}] \x1b[31mLOSS\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")      
        return f'{response}\n> Thua cuộc, đây là từ cuối trong từ điển của bot, Chuỗi đúng: **{streak}**\nTừ mới: **{current_word}**'

    # nếu không thì ra từ tiếp theo và thêm vào lịch sử
    history.extend([player_word, current_word])
    print('cc')
    db.store(
        'users', {id_user: {'word': current_word, 'history': history, 'streak': streak+1}})
    logger.info(f"DM: [{id_user}] \x1b[31mNEXT\x1b[0m '{player_word}' -> '{current_word} [{round(time.time() - start_time, 4)}s]")
    return response