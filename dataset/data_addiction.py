"""
Additional information about clubs
"""
import json
from pathlib import Path

if __name__ == '__main__':
    save_path = Path(__file__).parent / 'questions.json'

    additional_data = {
        "Чем отлича(е|ю)тся (Делис|Delice) (от|и) Альбион(*|а)?":
            "",
        "Кому написать, что информация о клубе неверная?":
            "Напишите участникам команды разработки бота: @anpruch",
        "Кому писать, если я хочу создать собственный клуб?":
            "Шмелёв Степан Викторович — глава внеучебной деятельности НИУ ВШЭ.",
        "Где найти информацию о мероприятиях?":
            "Это канал в Телеграме, где публикуются анонсы большинства мероприятий:\n"
            "t.me/hse_activNNik"
    }

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(additional_data, f, ensure_ascii=False, indent=4)
